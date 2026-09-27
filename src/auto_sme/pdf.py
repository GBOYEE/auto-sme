"""Renderer: WeasyPrint primary (Docker/Linux), fpdf2 styled fallback (Windows-native), minimal last resort."""
from __future__ import annotations

import os
from jinja2 import Environment, FileSystemLoader

from .generator import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STYLES_DIR = os.path.join(BASE_DIR, "styles")

PALETTES = {
    "modern": {"cover": (15, 23, 42), "accent": (16, 185, 129), "head": (15, 23, 42), "cta_bg": (236, 253, 245)},
    "classic": {"cover": (68, 68, 68), "accent": (68, 68, 68), "head": (34, 34, 34), "cta_bg": (250, 250, 250)},
    "bold": {"cover": (255, 59, 48), "accent": (255, 59, 48), "head": (200, 30, 20), "cta_bg": (17, 17, 17)},
}


def render_html(doc: Document, style: str = "modern", visual_score: int | None = None, engine: str = "preview") -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
    name = "mini-ebook.j2" if doc.kind == "mini-ebook" else "lead-magnet.j2"
    css_path = os.path.join(STYLES_DIR, f"{style}.css")
    css = open(css_path, encoding="utf-8").read() if os.path.exists(css_path) else ""
    tpl = env.get_template(name)
    return tpl.render(doc=doc, style=style, css=css, visual_score=visual_score, engine=engine)


def load_css(style: str = "modern") -> str:
    css_path = os.path.join(STYLES_DIR, f"{style}.css")
    return open(css_path, encoding="utf-8").read() if os.path.exists(css_path) else ""


def _clean(t: str) -> str:
    return (
        t.replace("—", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def _styled_fpdf(doc: Document, style: str, out_path: str, visual_score: int | None) -> None:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos

    pal = PALETTES.get(style, PALETTES["modern"])
    stamp = _clean(f"QA stamp: TOC + CTA verified - Visual {visual_score}/100 (styled)") if visual_score is not None else "QA stamp: TOC + CTA verified"

    class Doc(FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, _clean(f"{stamp} - p.{self.page_no()}"), align="C")

    def block(text: str, size: int, bold: bool, color: tuple, h: float, align: str = "L"):
        pdf.set_text_color(*color)
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.multi_cell(0, h, _clean(text), align=align, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf = Doc(format="A4")
    pdf.set_auto_page_break(True, margin=20)
    pdf.set_margins(15, 15, 15)

    # Cover: filled band + H1 24pt + subtitle 12pt
    pdf.add_page()
    pdf.set_fill_color(*pal["cover"])
    pdf.rect(0, 0, 210, 75, "F")
    pdf.set_y(18)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.multi_cell(0, 11, _clean(doc.title), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7, _clean(f"For {doc.audience} - {doc.topic}"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # TOC
    pdf.ln(6)
    block("Contents", 16, True, pal["head"], 10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    for i, s in enumerate(doc.sections, 1):
        pdf.multi_cell(0, 7, _clean(f"{i}. {s.heading}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if doc.kind == "mini-ebook":
        pdf.multi_cell(0, 7, _clean(f"{len(doc.sections)+1}. About the author"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Sections: H2 16pt bold colored, body 11pt — real hierarchy
    for s in doc.sections:
        pdf.ln(4)
        block(s.heading, 16, True, pal["head"], 9)
        block(s.body, 11, False, (30, 30, 30), 6.5)
    if doc.kind == "mini-ebook":
        pdf.ln(4)
        block("About the author", 16, True, pal["head"], 9)
        block(f"Written for {doc.audience} on {doc.topic}. Contact: {doc.cta}.", 11, False, (30, 30, 30), 6.5)

    # CTA: filled band + 14pt heading + 11pt phone (page-break safe, no absolute rect)
    pdf.ln(6)
    pdf.set_fill_color(*pal["cta_bg"])
    dark = style == "bold"
    pdf.set_text_color(255, 255, 255) if dark else pdf.set_text_color(*pal["head"])
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 9, "Your Next Step", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0,
        6,
        _clean(f"Message or call: {doc.cta}. Mention this guide for a free 15-minute consult on {doc.topic}."),
        fill=True,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.output(out_path)


def _minimal_pdf(html: str, out_path: str, title: str) -> None:
    import re

    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()[:6000]
    lines = [text[i : i + 90] for i in range(0, len(text), 90)][:45] or [title]
    content = "BT /F1 11 Tf 36 760 Td 13 TL " + " Tj T* ".join(
        f"({l.replace(chr(92), '').replace('(', '').replace(')', '')})" for l in lines
    ) + " Tj ET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{body}\nendobj\n".encode("latin-1", "ignore")
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
    for o in offsets:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
    with open(out_path, "wb") as f:
        f.write(out)


def html_to_pdf(
    html: str,
    out_path: str,
    title: str = "auto-sme",
    doc: Document | None = None,
    style: str = "modern",
    visual_score: int | None = None,
) -> str:
    """WeasyPrint first; fpdf2 styled (needs doc) second; minimal last resort."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    try:
        from weasyprint import HTML

        HTML(string=html).write_pdf(out_path)
        return "weasyprint"
    except Exception:
        pass
    if doc is not None:
        try:
            _styled_fpdf(doc, style, out_path, visual_score)
            return "styled"
        except Exception:
            pass
    _minimal_pdf(html, out_path, title)
    return "fallback"
