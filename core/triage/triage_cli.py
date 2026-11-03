"""Triage CLI: classify a ticket into a CCS2 component from logs + ticket text.

Usage:
  python core/triage/triage_cli.py --ticket-text ticket.txt --logs <file|dir> [...]
Output: compact JSON (signal names + evidence only; never raw log content).
This tool never writes to Jira; the TriageAgent handles gated updates.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import scorer  # noqa: E402
import signals  # noqa: E402


def run(ticket_text, log_paths, kb_dir=scorer.KB_DIR, current_sub_delivery=None,
        current_component=""):
    cmap, index, generic = scorer.load_kb(kb_dir)
    limits = []
    if not cmap["components"]:
        limits.append("component-map.json is empty")
    if not index["signals"]:
        limits.append("signature-index.json is empty; run build_knowledge.py")
    ticket_text = signals.narrative(ticket_text)
    try:
        with open(os.path.join(kb_dir, "domain-knowledge.json")) as f:
            domain = json.load(f)
    except OSError:
        domain = None
    sig = signals.extract_from_lines(ticket_text.splitlines())
    skipped = []
    if log_paths:
        log_sig, skipped = signals.extract_from_paths(log_paths)
        signals.merge(sig, log_sig)
    else:
        limits.append("no logs supplied; classification relies on ticket text only")
    all_kw = [k for c in cmap["components"] for k in c.get("keywords", [])]
    kw_hits = signals.keyword_hits(ticket_text, all_kw)
    result = scorer.score(sig, kw_hits, cmap, index, generic, domain, ticket_text,
                          current_component)
    valid = {c["sub_delivery"] for c in cmap["components"] if c.get("sub_delivery")}
    top = result["candidates"][0]["sub_delivery"] if result["candidates"] else None
    result["sub_delivery_valid"] = top in valid if top else False
    result["current_sub_delivery"] = current_sub_delivery
    result["signals_found"] = {k: len(v) for k, v in sig.items()}
    result["limitations"] = limits + skipped
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticket-text", help="file with summary/description/comments")
    ap.add_argument("--logs", nargs="*", default=[])
    ap.add_argument("--current", help="current Sub-Delivery value")
    ap.add_argument("--current-component", default="", help="SW Component already set in Jira")
    ap.add_argument("--kb", default=scorer.KB_DIR)
    a = ap.parse_args()
    text = ""
    if a.ticket_text:
        with open(a.ticket_text, errors="ignore") as f:
            text = f.read()
    print(json.dumps(run(text, a.logs, a.kb, a.current, a.current_component), indent=2))


if __name__ == "__main__":
    main()
