"""Build the otto-rules.md that ships inside every skill folder.

The installed skills can't see docs/AUTHORING.md, so the parts a running skill needs are copied
into each skill as otto-rules.md. Source of truth stays docs/AUTHORING.md: edit there, then run
templates/build.py (which calls this).
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = ["How every skill talks to the user", "Brand brain (shared memory)", "Rules learned from live test runs",
            "Otto MCP: verified facts", "Writing style"]   # matched by prefix, so a date in the heading can change


def build_rules():
    src = (ROOT / "docs/AUTHORING.md").read_text(encoding="utf8")
    parts = re.split(r"(?m)^## ", src)
    keep = []
    for p in parts:
        title = p.split("\n", 1)[0].strip()
        if any(title.startswith(s) for s in SECTIONS):
            keep.append("## " + p.rstrip())
    assert len(keep) == len(SECTIONS), f"expected {len(SECTIONS)} sections in AUTHORING.md, found {len(keep)}"
    body = "\n\n".join(keep)
    body = body.replace("docs/AUTHORING.md", "this file")
    head = ("# Otto skill rules\n\nShared rules for every Otto Content Skill. The SKILL.md next to this file says what the skill does; "
            "this file says how every skill talks to the user, what to check before calling tools, and the verified facts about the Otto MCP tools. "
            "Read it before the first Otto tool call.\n\n")
    text = head + body + "\n"
    for d in sorted((ROOT / "skills").iterdir()):
        if (d / "SKILL.md").exists():
            (d / "otto-rules.md").write_text(text, encoding="utf8", newline="\n")
    return len(text)


def fix_references():
    n = 0
    for f in (ROOT / "skills").glob("*/SKILL.md"):
        t = f.read_text(encoding="utf8")
        new = re.sub(r"`?docs/AUTHORING\.md`?", "`otto-rules.md` (in this skill's folder)", t)
        new = new.replace("(see AUTHORING)", "(see `otto-rules.md`)")
        if new != t:
            f.write_text(new, encoding="utf8", newline="\n"); n += 1
    return n


if __name__ == "__main__":
    print("rules chars", build_rules(), "skills fixed", fix_references())
