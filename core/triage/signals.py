"""Extract triage signals (tags, processes, packages, libs) from ticket text and logs.

Pure code, no LLM. Only signal names leave this module, never raw log lines.
"""
import gzip
import io
import os
import re
import zipfile

MAX_LINES = 10_000_000
MAX_FILE_BYTES = 1024 * 1024 * 1024  # per file / per zip member (uncompressed)
MAX_TOTAL_BYTES = 3 * 1024 * 1024 * 1024
LOG_EXTS = {".txt", ".log", ".logcat", ".md", ""}

LOGCAT_RE = re.compile(
    r"^\s*(?:\d{2}-\d{2}\s+)?\d{2}:\d{2}:\d{2}\.\d+\s+(?:\S+\s+)?(\d+)\s+(\d+)\s+([VDIWEF])\s+(\S{1,48}?)\s*:"
)
TAG_OK = re.compile(r"[A-Za-z_][\w.\-$@]{1,47}")
PROC_RE = re.compile(r"(?:Process:|Cmd line:|>>>)\s*([\w.\-/:]+)")
FRAME_RE = re.compile(r"\bat\s+((?:[a-z_][\w]*\.){2,}[A-Za-z_][\w$]*)\.[\w$<>]+\(")
LIB_RE = re.compile(r"#\d+\s+pc\s+[0-9a-fA-F]+\s+(\S+\.(?:so|oat|vdex|odex|apk))")
AIDL_RE = re.compile(r"\b((?:[a-z_][\w]*\.){2,}I[A-Z]\w+)(?:/\w+)?\b")


def _add(out, kind, value):
    value = value.strip()
    if value:
        out.setdefault(kind, {})
        out[kind][value] = out[kind].get(value, 0) + 1


def extract_from_lines(lines):
    """Return {kind: {value: count}}; logcat tags only from W/E/F lines."""
    out = {}
    for i, line in enumerate(lines):
        if i >= MAX_LINES:
            break
        m = LOGCAT_RE.match(line)
        if m:
            if m.group(3) not in "EFW":
                continue
            if TAG_OK.fullmatch(m.group(4)):
                _add(out, "tag", m.group(4))
        for pm in PROC_RE.finditer(line):
            _add(out, "proc", os.path.basename(pm.group(1)).split(":")[0])
        fm = FRAME_RE.search(line)
        if fm:
            cls = fm.group(1)
            _add(out, "pkg", cls.rsplit(".", 1)[0])
            _add(out, "cls", cls)
        lm = LIB_RE.search(line)
        if lm:
            _add(out, "lib", os.path.basename(lm.group(1)))
        for sm in AIDL_RE.finditer(line):
            _add(out, "aidl", sm.group(1).rsplit(".", 1)[-1])
    return out


def merge(a, b):
    for kind, vals in b.items():
        for v, c in vals.items():
            a.setdefault(kind, {})
            a[kind][v] = a[kind].get(v, 0) + c
    return a


def _text_stream(binary):
    return io.TextIOWrapper(binary, encoding="utf-8", errors="ignore", newline=None)


def _scan_zip(path, out, skipped, budget):
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        skipped.append(f"bad zip: {os.path.basename(path)}")
        return
    with zf:
        for info in zf.infolist():
            name = os.path.basename(info.filename)
            if info.is_dir():
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in LOG_EXTS:
                continue  # media, images, binaries inside bugreports
            if info.file_size > MAX_FILE_BYTES or budget[0] + info.file_size > MAX_TOTAL_BYTES:
                skipped.append(f"too large: {os.path.basename(path)}!{name}")
                continue
            budget[0] += info.file_size
            with zf.open(info) as raw:
                merge(out, extract_from_lines(_text_stream(raw)))


def extract_from_paths(paths):
    """Walk files/dirs (incl. .zip/.gz) and extract signals; skips unsupported/oversized files."""
    out, skipped, files, budget = {}, [], [], [0]
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, n) for n in names]
        elif os.path.isfile(p):
            files.append(p)
        else:
            skipped.append(f"missing: {p}")
    for f in sorted(files):
        base = os.path.basename(f)
        ext = os.path.splitext(f)[1].lower()
        try:
            if ext == ".zip":
                _scan_zip(f, out, skipped, budget)
            elif ext == ".gz":
                with gzip.open(f, "rb") as raw:
                    merge(out, extract_from_lines(_text_stream(raw)))
            elif ext in LOG_EXTS:
                if os.path.getsize(f) > MAX_FILE_BYTES:
                    skipped.append(f"too large: {base}")
                    continue
                with open(f, "r", errors="ignore") as fh:
                    merge(out, extract_from_lines(fh))
            else:
                skipped.append(f"unsupported: {base}")
        except (OSError, EOFError) as e:
            skipped.append(f"unreadable: {base} ({e.__class__.__name__})")
    return out, skipped


def keyword_hits(text, keywords):
    low = text.lower()
    return [k for k in keywords
            if re.search(r"(?<![a-z0-9])" + re.escape(k.lower().strip()) + r"(?![a-z0-9])", low)]


def narrative(text):
    """Drop Jira table rows (HW/version/environment blocks) to avoid false keyword hits."""
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("|"))
