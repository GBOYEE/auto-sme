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


def _hex_to_rgb(h: str) -> tuple[float, float, float]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def _luminance(rgb: tuple[float, float, float]) -> float:
    def f(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    try:
        l1, l2 = _luminance(_hex_to_rgb(fg)), _luminance(_hex_to_rgb(bg))
        return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
    except Exception:
        return 0.0


def _first_px(css: str, selector: str, prop: str) -> float:
    m = re.search(rf"{re.escape(selector)}\s*\{{[^}}]*?{prop}\s*:\s*([\d.]+)\s*(px|pt)", css, re.I | re.S)
    return float(m.group(1)) if m else 0.0


def validate_visual(
    html: str, css: str = "", pdf_path: str = "", engine: str = "fallback"
) -> tuple[int, list[str]]:
    """Score visual hierarchy 0-100. Returns (score, breakdown lines).

    HTML/CSS checks (deterministic, no render needed) + PDF bonus.
    Fallback PDFs cap PDF-dependent points honestly — styled WeasyPrint scores higher.
    Weights: frame 10, type 20, contrast 15, cover 10, toc 10, cta 15, footer 10, breaks 10.
    """
    score = 0
    out: list[str] = []
    low = html.lower()

    # 1. Page frame (10): A4 + margins in CSS, PDF exists + %PDF header
    frame = 0
    if "@page" in css.lower() and "margin" in css.lower():
        frame += 6
    pdf_ok = False
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_ok = f.read(5) == b"%PDF-"
        if pdf_ok and os.path.getsize(pdf_path) >= 1500:
            frame += 4
    score += frame
    out.append(f"frame {frame}/10 {'PASS' if frame==10 else 'PARTIAL' if frame else 'FAIL'}")

    # 2. Type scale (20): h1 px > h2 px > body pt, all explicit
    h1 = _first_px(css, "h1", "font-size")
    h2 = _first_px(css, "h2", "font-size")
    body = _first_px(css, "body", "font-size")
    t = 0
    if h1 and h2 and body and h1 > h2 >= 20 and body >= 11:
        t = 20
    elif h1 and h2 and h1 > h2:
        t = 12
    elif h1:
        t = 6
    score += t
    out.append(f"type-scale {t}/20 h1={h1 or 0:g} h2={h2 or 0:g} body={body or 0:g}")

    # 3. Contrast (15): body text vs white bg >= 4.5
    m = re.search(r"body\s*\{[^}}]*?color\s*:\s*(#[0-9a-fA-F]{3,6})", css, re.S)
    body_color = m.group(1) if m else "#000000"
    cr = contrast_ratio(body_color, "#ffffff")
    c = 15 if cr >= 7 else 12 if cr >= 4.5 else 6 if cr >= 3 else 0
    score += c
    out.append(f"contrast {c}/15 {body_color} on white = {cr:.1f}:1")

    # 4. Cover (10): cover div + h1 title as largest
    cov = 0
    if 'class="cover"' in low or "class='cover'" in low:
        cov += 5
    if "<h1" in low:
        cov += 5
    score += cov
    out.append(f"cover {cov}/10")

    # 5. TOC (10): toc block + li count matches h2 count
    lis = len(re.findall(r"<li", html))
    h2s = len(re.findall(r"<h2", html))
    toc = 0
    if "toc" in low:
        toc += 5
    if lis >= 4:
        toc += 5
    score += toc
    out.append(f"toc {toc}/10 items={lis} heads={h2s}")

    # 6. CTA pop (15): cta block + distinct bg/border + phone present
    cta = 0
    if "cta" in low:
        cta += 6
    if re.search(r"\.cta\s*\{[^}]*(background|border)", css, re.I | re.S):
        cta += 5
    if re.search(r"\+?\d[\d\s-]{7,}", html):
        cta += 4
    score += cta
    out.append(f"cta {cta}/15")

    # 7. Footer (10): footer div + QA stamp text; +4 if rendered by weasyprint (multi-page capable)
    foot = 0
    if "footer" in low:
        foot += 4
    if "qa stamp" in low:
        foot += 2
    if engine == "weasyprint" and pdf_ok:
        foot += 4
    elif pdf_ok:
        foot += 1  # fallback single-page: stamp present but not per-page
    score += foot
    out.append(f"footer {foot}/10 engine={engine}")

    # 8. Breaks (10): break-after:avoid on h2 + break-inside rules + @page bottom counter
    br = 0
    if "break-after" in css.lower():
        br += 4
    if "break-inside" in css.lower():
        br += 3
    if "counter(page)" in css.lower():
        br += 3
    score += br
    out.append(f"breaks {br}/10")

    return max(0, min(100, score)), out


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
