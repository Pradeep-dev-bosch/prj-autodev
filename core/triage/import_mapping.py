"""Import the CCS2 mapping Excel into knowledge/component-map.json.

  python core/triage/import_mapping.py --xlsx "<MasterList...xlsx>"          # dry-run (diff only)
  python core/triage/import_mapping.py --xlsx "<MasterList...xlsx>" --write  # apply

Reads sheet 'ALL_Component_Subdelivery_Map' (Topic / SW Component / Sub-Delivery; Owner is ignored, Jira assigns it).
Preserves curated keywords/repos/layer. Never silently merges near-duplicate spellings:
those are reported as conflicts and skipped until resolved.
"""
import argparse
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import scorer  # noqa: E402

SHEET = "ALL_Component_Subdelivery_Map"


def _clean(v):
    return re.sub(r"\s+", " ", str(v)).strip() if v is not None else ""


def read_sheet(xlsx):
    import openpyxl
    ws = openpyxl.load_workbook(xlsx, data_only=True)[SHEET]
    rows = list(ws.iter_rows(values_only=True))
    hdr = next(i for i, r in enumerate(rows) if any(_clean(c) == "Sub-Delivery" for c in r))
    sub = next(j for j, c in enumerate(rows[hdr]) if _clean(c) == "Sub-Delivery")
    out = []
    for r in rows[hdr + 1:]:
        topic, sw, sd = (_clean(r[sub + k]) for k in (-2, -1, 0))
        if (topic or sw or sd) and not (topic == "Topic" and sw == "Component"):
            out.append({"topic": topic, "sw": sw, "sub": sd})
    return out


def merge(cmap, rows):
    comps = {c["sub_delivery"]: c for c in cmap["components"]}
    report = {"added": [], "updated": [], "conflicts": [], "unassigned": []}
    seen = {}
    for r in rows:
        sd = r["sub"]
        if not sd:
            report["unassigned"].append({"sw_component": r["sw"], "topic": r["topic"],
                                         "note": "no Sub-Delivery in mapping"})
            continue
        if sd not in comps:
            near = [n for n in list(comps) + list(seen)
                    if n.lower() == sd.lower() or difflib.SequenceMatcher(None, n.lower(), sd.lower()).ratio() > 0.92]
            if near:
                report["conflicts"].append(f"'{sd}' looks like existing '{near[0]}' (case/spelling); not merged")
                continue
            comps[sd] = {"name": sd, "sub_delivery": sd, "sw_components": [],
                         "layer": None, "repos": [], "path_prefixes": [], "keywords": []}
            report["added"].append(sd)
        seen[sd] = True
        c = comps[sd]
        before = list(c["sw_components"])
        if r["sw"] and r["sw"] not in c["sw_components"]:
            c["sw_components"].append(r["sw"])
        if before != c["sw_components"] and sd not in report["added"]:
            report["updated"].append(sd)
    report["not_in_sheet"] = [s for s in comps if s not in seen]
    cmap["components"] = list(comps.values())
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--kb", default=scorer.KB_DIR)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    path = os.path.join(a.kb, "component-map.json")
    with open(path) as f:
        cmap = json.load(f)
    report = merge(cmap, read_sheet(a.xlsx))
    if a.write:
        cmap["unassigned_topics"] = report["unassigned"]
        with open(path, "w") as f:
            json.dump(cmap, f, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k != "unassigned"}
                     | {"unassigned_count": len(report["unassigned"]), "written": a.write}, indent=2))


if __name__ == "__main__":
    main()
