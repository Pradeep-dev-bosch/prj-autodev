"""Build the shared triage signature index (run by maintainers, not by users).

  python core/triage/build_knowledge.py --manifest default.xml --source-root /path/to/aosp \
      [--history history.json] [--kb core/triage/knowledge]

Steps (all CPU-only, no LLM):
  1. Map manifest projects -> components using component-map.json (repos / path_prefixes).
  2. Scan those repos for identifiers (LOG_TAG, AIDL interfaces, init.rc services,
     Android.bp modules, Java/Kotlin packages).
  3. Optionally mine validated historical tickets: history.json =
     [{"key": "...", "sub_delivery": "<valid value>", "text": "<summary + filtered logs>"}]
  4. Write signature-index.json. Re-run incrementally with --only-repos to refresh a subset.
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
import scorer  # noqa: E402
import signals  # noqa: E402

SRC_EXTS = {".java", ".kt", ".cpp", ".cc", ".c", ".h", ".hpp", ".aidl", ".bp", ".rc"}
SKIP_DIRS = {".git", "out", "prebuilts", "third_party", "node_modules", "test", "tests", "build"}
MAX_SRC_BYTES = 2 * 1024 * 1024

TAG_RES = [
    re.compile(r'LOG_TAG\s*(?:=|\s)\s*"([^"]+)"'),
    re.compile(r'\bTAG\s*=\s*"([^"]+)"'),
    re.compile(r'#define\s+LOG_TAG\s+"([^"]+)"'),
]
PKG_RE = re.compile(r"^\s*package\s+([\w.]+)\s*;?", re.M)
AIDL_RE = re.compile(r"^\s*interface\s+(I\w+)", re.M)
SERVICE_RE = re.compile(r"^\s*service\s+(\S+)\s+(\S+)", re.M)
BP_NAME_RE = re.compile(r'\bname:\s*"([^"]+)"')


def parse_manifest(path):
    root = ET.parse(path).getroot()
    return {p.get("path") or p.get("name"): p.get("name") for p in root.iter("project")}


def repo_component(path, name, components):
    for c in components:
        if path in c.get("repos", []) or name in c.get("repos", []):
            return c["name"]
        if any(path.startswith(pfx) for pfx in c.get("path_prefixes", [])):
            return c["name"]
    return None


def scan_repo(repo_dir):
    found = {}
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            ext = os.path.splitext(fn)[1]
            if ext not in SRC_EXTS and fn != "Android.bp":
                continue
            fp = os.path.join(root, fn)
            try:
                if os.path.getsize(fp) > MAX_SRC_BYTES:
                    continue
                with open(fp, errors="ignore") as f:
                    txt = f.read()
            except OSError:
                continue
            for rx in TAG_RES:
                for m in rx.findall(txt):
                    signals._add(found, "tag", m)
            if ext in (".java", ".kt", ".aidl"):
                pm = PKG_RE.search(txt)
                if pm:
                    parts = pm.group(1).split(".")
                    for n in range(3, len(parts) + 1):
                        signals._add(found, "pkg", ".".join(parts[:n]))
            if ext == ".aidl":
                for m in AIDL_RE.findall(txt):
                    signals._add(found, "aidl", m)
            if ext == ".rc":
                for name, exe in SERVICE_RE.findall(txt):
                    signals._add(found, "service", name)
                    signals._add(found, "proc", os.path.basename(exe))
            if fn == "Android.bp":
                for m in BP_NAME_RE.findall(txt):
                    signals._add(found, "module", m)
                    signals._add(found, "lib", f"{m}.so")
    return found


def add_to_index(index, comp, found, scale=1):
    for kind, vals in found.items():
        for value, count in vals.items():
            sig = index["signals"].setdefault(f"{kind}:{value}", {"c": {}})
            sig["c"][comp] = sig["c"].get(comp, 0) + min(count, 5) * scale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest")
    ap.add_argument("--source-root")
    ap.add_argument("--history")
    ap.add_argument("--kb", default=scorer.KB_DIR)
    ap.add_argument("--only-repos", nargs="*", help="refresh only these manifest paths")
    ap.add_argument("--reset", action="store_true", help="start from an empty index")
    a = ap.parse_args()

    cmap, index, _ = scorer.load_kb(a.kb)
    if not cmap["components"]:
        sys.exit("component-map.json has no components; fill it in first.")
    if a.reset or not index["signals"]:
        index = {"version": 1, "signals": {}}
    valid = {c["sub_delivery"]: c["name"] for c in cmap["components"] if c.get("sub_delivery")}

    stats = {"repos_scanned": 0, "repos_unmapped": 0, "history_used": 0, "history_rejected": 0}
    if a.manifest and a.source_root:
        for path, name in parse_manifest(a.manifest).items():
            if a.only_repos and path not in a.only_repos:
                continue
            comp = repo_component(path, name, cmap["components"])
            d = os.path.join(a.source_root, path)
            if not comp:
                stats["repos_unmapped"] += 1
                continue
            if not os.path.isdir(d):
                continue
            add_to_index(index, comp, scan_repo(d))
            stats["repos_scanned"] += 1

    if a.history:
        with open(a.history) as f:
            for t in json.load(f):
                comp = valid.get(t.get("sub_delivery"))
                if not comp:
                    stats["history_rejected"] += 1
                    continue
                found = signals.extract_from_lines(t.get("text", "").splitlines())
                add_to_index(index, comp, found, scale=2)
                stats["history_used"] += 1

    with open(os.path.join(a.kb, "signature-index.json"), "w") as f:
        json.dump(index, f)
    print(json.dumps({**stats, "signals": len(index["signals"])}, indent=2))


if __name__ == "__main__":
    main()
