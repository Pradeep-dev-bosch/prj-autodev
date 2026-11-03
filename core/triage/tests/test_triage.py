import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TRIAGE = os.path.dirname(HERE)
sys.path.insert(0, TRIAGE)
import triage_cli  # noqa: E402

LOG_DTV = """\
10-28 10:00:01.100  1000  1001 E DtvTuner: lock failed ch=12
10-28 10:00:01.200  1000  1001 E AndroidRuntime: FATAL EXCEPTION: main
10-28 10:00:01.300  1000  1001 E AndroidRuntime: Process: com.acme.dtv.service, PID: 1000
\tat com.acme.dtv.service.TunerManager.lock(TunerManager.java:42)
"""
LOG_GENERIC = """\
10-28 10:00:01.200  1000  1001 E AndroidRuntime: FATAL EXCEPTION: main
10-28 10:00:01.300  1000  1001 E ActivityManager: ANR in something
"""


def make_fixture(root):
    kb = os.path.join(root, "kb")
    os.makedirs(kb)
    cmap = {"thresholds": {"high": 0.5, "review": 0.2, "min_distinct_evidence": 2},
            "components": [
                {"name": "DTV", "sub_delivery": "DTV Service", "layer": "Service",
                 "repos": ["vendor/acme/dtv"], "keywords": ["tuner"]},
                {"name": "EXT_MEDIA_IN", "sub_delivery": "Ext Media In", "layer": "HAL",
                 "path_prefixes": ["vendor/acme/media"], "keywords": ["aux"]}]}
    json.dump(cmap, open(os.path.join(kb, "component-map.json"), "w"))
    json.dump({"max_components": 4, "ignore": ["AndroidRuntime", "ActivityManager"]},
              open(os.path.join(kb, "generic-signals.json"), "w"))
    src = os.path.join(root, "src")
    dtv = os.path.join(src, "vendor/acme/dtv")
    med = os.path.join(src, "vendor/acme/media_in")
    os.makedirs(dtv)
    os.makedirs(med)
    open(os.path.join(dtv, "T.java"), "w").write(
        'package com.acme.dtv.service;\nclass T { static final String TAG = "DtvTuner"; }\n')
    open(os.path.join(dtv, "dtv.rc"), "w").write("service dtvd /vendor/bin/dtvd\n  class main\n")
    open(os.path.join(med, "m.cpp"), "w").write('#define LOG_TAG "ExtMediaHal"\n')
    manifest = os.path.join(root, "default.xml")
    open(manifest, "w").write(
        '<manifest><project path="vendor/acme/dtv" name="acme/dtv"/>'
        '<project path="vendor/acme/media_in" name="acme/media_in"/></manifest>')
    return kb, manifest, src


class TriageTest(unittest.TestCase):
    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            kb, manifest, src = make_fixture(d)
            subprocess.run([sys.executable, os.path.join(TRIAGE, "build_knowledge.py"),
                            "--manifest", manifest, "--source-root", src, "--kb", kb],
                           check=True, capture_output=True)
            log = os.path.join(d, "dtv.log")
            open(log, "w").write(LOG_DTV)
            r = triage_cli.run("Channel scan fails", [log], kb)
            self.assertEqual(r["candidates"][0]["component"], "DTV")
            self.assertEqual(r["decision"], "high_confidence")
            self.assertTrue(r["sub_delivery_valid"])

            gen = os.path.join(d, "gen.log")
            open(gen, "w").write(LOG_GENERIC)
            r = triage_cli.run("something crashed", [gen], kb)
            self.assertEqual(r["decision"], "no_match")

            r = triage_cli.run("tuner problem", [], kb)
            self.assertNotEqual(r["decision"], "high_confidence")
            self.assertTrue(any("no logs" in x for x in r["limitations"]))

            r = triage_cli.run("x", [os.path.join(d, "nope.log")], kb)
            self.assertTrue(any("missing" in x for x in r["limitations"]))


if __name__ == "__main__":
    unittest.main()
