"""Make upstream HyperFrames skills pass Claude's plugin validation.

Claude rejects a SKILL.md whose frontmatter description contains XML-like
tags (e.g. `<hf-audio-group>`). This strips the angle brackets inside the
frontmatter only; the skill body is left untouched.
"""
import pathlib
import re

TAG = re.compile(r"<([^<>\n]+)>")
changed = []
for path in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        continue
    front = m.group(1)
    fixed = TAG.sub(r"\1", front)
    if fixed != front:
        path.write_text(text[: m.start(1)] + fixed + text[m.end(1):], encoding="utf-8")
        changed.append(str(path))
print("sanitized:", changed or "nothing")
