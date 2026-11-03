"""Score extracted signals against the shared signature index."""
import json
import os

KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge")

WEIGHTS = {"tag": 3.0, "proc": 3.0, "lib": 3.0, "aidl": 4.0, "service": 3.0,
           "pkg": 2.0, "cls": 2.0, "module": 2.0, "kw": 1.0}


def load_kb(kb_dir=KB_DIR):
    def _load(name, default):
        p = os.path.join(kb_dir, name)
        if not os.path.exists(p):
            return default
        with open(p) as f:
            return json.load(f)
    return (
        _load("component-map.json", {"components": [], "thresholds": {}}),
        _load("signature-index.json", {"signals": {}}),
        _load("generic-signals.json", {"ignore": [], "max_components": 4}),
    )


def _lookup(index, kind, value):
    sig = index["signals"].get(f"{kind}:{value}")
    if sig:
        return sig
    if kind in ("pkg", "cls"):
        parts = value.split(".")
        for n in range(len(parts) - 1, 2, -1):
            sig = index["signals"].get("pkg:" + ".".join(parts[:n]))
            if sig:
                return sig
    return None


def score(signals, text_keyword_hits, cmap, index, generic, domain=None, text="",
          current_component=""):
    ignore = {s.lower() for s in generic.get("ignore", [])}
    max_comp = generic.get("max_components", 4)
    scores, evidence = {}, {}

    def credit(comp, pts, desc):
        scores[comp] = scores.get(comp, 0.0) + pts
        evidence.setdefault(comp, []).append((pts, desc))

    for kind, vals in signals.items():
        for value, count in vals.items():
            if value.lower() in ignore:
                continue
            sig = _lookup(index, kind, value)
            if not sig or len(sig["c"]) > max_comp:
                continue
            total = sum(sig["c"].values())
            rep = min(1.0 + 0.1 * (count - 1), 1.5)
            for comp, n in sig["c"].items():
                credit(comp, WEIGHTS.get(kind, 1.0) * (n / total) * rep, f"{kind}={value}")

    name_by_kw = {}
    for c in cmap["components"]:
        for k in c.get("keywords", []):
            name_by_kw.setdefault(k, []).append(c["name"])
    for k in text_keyword_hits:
        for comp in name_by_kw.get(k, []):
            credit(comp, WEIGHTS["kw"], f"kw={k}")

    if domain:
        import re
        low = text.lower()
        flat = [(k.lower(), v) for kind in signals.values() for k, v in kind.items()]
        for comp, d in domain.get("domains", {}).items():
            for w in d.get("symptom", []):
                if re.search(r"(?<![a-z0-9])" + re.escape(w.strip()) + r"(?![a-z0-9])", low):
                    credit(comp, 1.0, f"symptom={w}")
            for w in d.get("strong", []):
                if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low):
                    credit(comp, 2.0, f"strong={w}")
            log_hits = 0
            for h in d.get("log", []):
                hl = h.lower()
                if log_hits < 2 and hl not in ignore and any(hl in k for k, _ in flat):
                    credit(comp, 2.0, f"log={h}")
                    log_hits += 1

    for c in cmap["components"]:
        for pre in c.get("pkg_prefixes", []):
            hit = next((v for v in signals.get("pkg", {}) if v.startswith(pre)), None)
            if hit:
                credit(c["name"], WEIGHTS["pkg"], f"pkg={pre}.*")

    # A triager's existing SW Component (not a SW_UNKNOWN placeholder) is a prior
    cur = current_component.strip().lower()
    if cur and "unknown" not in cur:
        for c in cmap["components"]:
            if cur in [s.lower() for s in c.get("sw_components", [])]:
                credit(c["name"], 3.0, f"existing_sw_component={current_component}")

    ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:3]
    by_name = {c["name"]: c for c in cmap["components"]}
    top = ranked[0][1] if ranked else 0.0
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    strength = top / (top + 3.0) if top else 0.0
    dominance = top / (top + second) if top else 0.0
    confidence = round(strength * dominance, 3)

    cands = []
    for comp, s in ranked:
        ev = sorted(evidence[comp], key=lambda e: -e[0])
        sw = by_name.get(comp, {}).get("sw_components", [])
        cands.append({
            "component": comp,
            "sub_delivery": by_name.get(comp, {}).get("sub_delivery"),
            "sw_component": sw[0] if len(sw) == 1 else None,
            "sw_component_options": sw if len(sw) > 1 else [],
            "layer": by_name.get(comp, {}).get("layer"),
            "score": round(s, 2),
            "evidence": [d for _, d in ev[:8]],
        })
    th = cmap.get("thresholds", {})
    high_t, review_t = th.get("high", 0.6), th.get("review", 0.3)
    min_ev = th.get("min_distinct_evidence", 2)
    n_ev = len({d for _, d in evidence.get(ranked[0][0], [])}) if ranked else 0
    if not ranked:
        decision = "no_match"
    elif confidence >= high_t and n_ev >= min_ev and cands[0]["sub_delivery"]:
        decision = "high_confidence"
    elif confidence >= review_t:
        decision = "needs_human_review"
    else:
        decision = "low_confidence_no_change"
    return {"decision": decision, "confidence": confidence,
            "distinct_evidence": n_ev, "candidates": cands}
