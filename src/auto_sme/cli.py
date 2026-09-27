"""Typer CLI: generate | validate | list-templates | score."""
from __future__ import annotations

import os
import typer

from .generator import generate as gen_doc
from .pdf import render_html, html_to_pdf, load_css
from .qa import validate_html, validate_pdf, validate_visual

app = typer.Typer(help="AUTO-SME V1 — topic+audience+CTA in, QA-passed PDF out.")


@app.command(name="generate")
def generate_cmd(
    topic: str = typer.Option(..., "--topic"),
    audience: str = typer.Option(..., "--audience"),
    cta: str = typer.Option(..., "--cta"),
    kind: str = typer.Option("lead-magnet", "--kind"),
    style: str = typer.Option("modern", "--style"),
    out: str = typer.Option("out.pdf", "--out", "-o"),
) -> None:
    doc = gen_doc(topic=topic, audience=audience, cta=cta, kind=kind)
    css = load_css(style)
    preview = render_html(doc, style=style)
    ok, reasons = validate_html(preview, cta, min_sections=4)
    if not ok:
        typer.echo(f"QA-HTML FAIL: {reasons}")
        raise typer.Exit(2)
    # Pass 1: pre-score from HTML/CSS (no PDF yet) to stamp on last page
    pre_score, _ = validate_visual(preview, css, pdf_path="", engine="preview")
    html = render_html(doc, style=style, visual_score=pre_score, engine="preview")
    engine = html_to_pdf(html, out, title=doc.title, doc=doc, style=style, visual_score=pre_score)
    ok2, reasons2 = validate_pdf(out)
    if not ok2:
        typer.echo(f"QA-PDF FAIL: {reasons2}")
        raise typer.Exit(3)
    # Pass 2: final visual score with real PDF + engine, restamp if styled/weasyprint
    final, breakdown = validate_visual(html, css, pdf_path=out, engine=engine)
    if engine in ("weasyprint", "styled") and final != pre_score:
        html2 = render_html(doc, style=style, visual_score=final, engine=engine)
        html_to_pdf(html2, out, title=doc.title, doc=doc, style=style, visual_score=final)
        final, breakdown = validate_visual(html2, css, pdf_path=out, engine=engine)
    typer.echo(f"OK [{engine}] {out} — Visual {final}/100")
    for line in breakdown:
        typer.echo(f"  {line}")


@app.command(name="validate")
def validate_cmd(path: str = typer.Argument(...)) -> None:
    ok, reasons = validate_pdf(path)
    typer.echo(f"{'PASS' if ok else 'FAIL'} {reasons}")
    if not ok:
        raise typer.Exit(1)


@app.command(name="score")
def score_cmd(
    topic: str = typer.Option("Sample topic", "--topic"),
    audience: str = typer.Option("Sample audience", "--audience"),
    cta: str = typer.Option("+2348000000000", "--cta"),
    kind: str = typer.Option("lead-magnet", "--kind"),
    style: str = typer.Option("modern", "--style"),
) -> None:
    """Score what output SHOULD look like (HTML/CSS) without writing a PDF."""
    doc = gen_doc(topic=topic, audience=audience, cta=cta, kind=kind)
    css = load_css(style)
    html = render_html(doc, style=style, visual_score=None, engine="preview")
    s, breakdown = validate_visual(html, css, pdf_path="", engine="preview")
    typer.echo(f"Visual {s}/100 (target look, no PDF)")
    for line in breakdown:
        typer.echo(f"  {line}")


@app.command(name="list-templates")
def list_templates() -> None:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "templates")
    for f in sorted(os.listdir(base) if os.path.exists(base) else []):
        typer.echo(f)


if __name__ == "__main__":
    app()
