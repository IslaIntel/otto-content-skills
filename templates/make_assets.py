"""Render the README banner (assets/banner.png, also used as the GitHub social preview).

Run after templates/build.py and after refreshing the dashboard screenshots in assets/.
Needs Python Playwright (pip install playwright; playwright install chromium).
"""
import base64, pathlib, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / "templates"
n = len([d for d in (ROOT / "skills").iterdir() if (d / "SKILL.md").exists()])
icon = "data:image/png;base64," + (T / "otto-icon.b64").read_text().strip()
wm = (T / "otto-wordmark.svg").read_text(encoding="utf8").strip()
shot = "data:image/png;base64," + base64.b64encode((ROOT / "assets/weekly-review-dark.png").read_bytes()).decode()
mascot = "data:image/png;base64," + base64.b64encode((T / "otto-mascot.png").read_bytes()).decode()
shot2 = "data:image/png;base64," + base64.b64encode((ROOT / "assets/reel-diagnosis-dark.png").read_bytes()).decode()
html = (T / "banner.src.html").read_text(encoding="utf8")
html = re.sub(r"\b\d+ free skills", f"{n} free skills", html)
html = html.replace("__ICON__", icon).replace("__WORDMARK__", wm).replace("__SHOT__", shot).replace("__SHOT2__", shot2).replace("__MASCOT__", mascot)
tmp = ROOT / "assets/_banner.html"; tmp.write_text(html, encoding="utf8")
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 640}, device_scale_factor=2)
    pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(400)
    pg.screenshot(path=str(ROOT / "assets/banner.png")); b.close()
tmp.unlink()
print("assets/banner.png:", n, "skills")
