"""Content + visual QA. Fail closed with named reasons."""
from __future__ import annotations

import os
import re

BANNED = ("lorem", "todo", "tbd", "[insert", "xxx", "placeholder")


def validate_html(html: str, cta: str, min_sections: int = 4) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    low = html.lower()
    if "<h1" not in low:
        reasons.append("missing-h1-title")
    if "toc" not in low and "contents" not in low:
        reasons.append("missing-toc")
    if cta.strip().lower() not in low:
        reasons.append("missing-cta")
    if sum(low.count(f"<h2") for _ in [0]) < min_sections and len(re.findall(r"<h2", html)) < min_sections:
        reasons.append(f"too-few-sections(min={min_sections})")
    for token in BANNED:
        if token in low:
            reasons.append(f"banned-token:{token}")
            break
    # Grade band: avg words/sentence under 26 (simple readability proxy)
    text = re.sub(r"<[^>]+>", " ", html)
    words = re.findall(r"[A-Za-z']+", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if sentences and len(words) / max(len(sentences), 1) > 26:
        reasons.append("too-complex-sentences")
    return (len(reasons) == 0, reasons)


def validate_pdf(path: str, min_bytes: int = 1500) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not os.path.exists(path):
        return False, ["pdf-missing"]
    size = os.path.getsize(path)
    if size < min_bytes:
        reasons.append(f"pdf-too-small({size}b)")
    with open(path, "rb") as f:
        head = f.read(5)
    if head != b"%PDF-":
        reasons.append("not-a-pdf")
    return (len(reasons) == 0, reasons)
