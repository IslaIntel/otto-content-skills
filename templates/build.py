"""Build the shipped dashboard templates.

Source of truth: templates/dashboard.src.html (+ otto-icon.b64, otto-wordmark.svg, sample-data.json, samples.py).
Run: python templates/build.py   -> writes dashboard.html into each skill that uses it.
Edit the source, never the generated copies.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / "templates"
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from samples import SAMPLES, REEL_SAMPLE
from make_rules import build_rules, fix_references
SKILLS = ["weekly-social-review", "daily-pulse", "content-audit", "reel-diagnosis"] + list(SAMPLES)

src = (T / "dashboard.src.html").read_text(encoding="utf8")
icon = (T / "otto-icon.b64").read_text(encoding="utf8").strip()
wordmark = (T / "otto-wordmark.svg").read_text(encoding="utf8").strip()
sample = json.loads((T / "sample-data.json").read_text(encoding="utf8"))

for s in SKILLS:
    data = dict(SAMPLES[s]) if s in SAMPLES else dict(sample)
    data["meta"] = dict(data["meta"])
    if s == "daily-pulse":
        data["meta"].update(title="Daily pulse", start="Mar 09", end="Mar 09, 2026",
                            verdict="Yesterday's reels, early read. Final calls happen once each reel is 3 days old.")
        data.pop("plan", None); data.pop("groups", None); data.pop("decisions", None)
    if s == "reel-diagnosis":
        data["meta"].update(title="Reel diagnosis", focusPost="ex3", verdict="The first second lost people: skip rate 41% vs your usual 33%.")
        data["posts"] = [p for p in sample["posts"] if p["id"] == "ex3"]
        data["meta"]["platforms"] = ["instagram"]
        for k in ("plan", "groups", "decisions", "search", "daily"): data.pop(k, None)
        data["kpis"] = [k for k in sample["kpis"] if k["platform"] == "instagram"][1:4]
    if s == "content-audit":
        data["meta"].update(title="Content audit", start="Feb 08", baselineLabel="your median for the period")
    html = src.replace("__OTTO_ICON__", icon).replace("__OTTO_WORDMARK__", wordmark).replace("__DATA__", json.dumps(data, indent=1, ensure_ascii=False))
    out = ROOT / "skills" / s / "dashboard.html"
    out.write_text(html, encoding="utf8", newline="\n")
    (ROOT / "skills" / s / "dashboard-data.md").write_text((T / "dashboard-data.md").read_text(encoding="utf8"), encoding="utf8", newline="\n")
    print("wrote", out.relative_to(ROOT))

print("otto-rules.md:", build_rules(), "chars; references fixed:", fix_references())

# reel-breakdown: its own layout, the dashboard's base styles and the same Otto mark
import re as _re
_base = _re.search(r"<style>(.*?)</style>", src, _re.S).group(1)
_rb = (T / "reel-breakdown.src.html").read_text(encoding="utf8")
_rb = _rb.replace("__BASE_CSS__", _base).replace("__OTTO_ICON__", icon).replace("__OTTO_WORDMARK__", wordmark).replace("__DATA__", json.dumps(REEL_SAMPLE, indent=1, ensure_ascii=False))
(ROOT / "skills/reel-breakdown/reel-breakdown.html").write_text(_rb, encoding="utf8", newline=chr(10))
(ROOT / "skills/reel-breakdown/reel-breakdown-data.md").write_text((T / "reel-breakdown-data.md").read_text(encoding="utf8"), encoding="utf8", newline=chr(10))
print("wrote skills/reel-breakdown/reel-breakdown.html")
