"""Typer CLI: generate | validate | list-templates."""
from __future__ import annotations

import os
import typer

from .generator import generate as gen_doc
from .pdf import render_html, html_to_pdf
from .qa import validate_html, validate_pdf

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
    html = render_html(doc, style=style)
    ok, reasons = validate_html(html, cta, min_sections=4)
    if not ok:
        typer.echo(f"QA-HTML FAIL: {reasons}")
        raise typer.Exit(2)
    engine = html_to_pdf(html, out, title=doc.title)
    ok2, reasons2 = validate_pdf(out)
    if not ok2:
        typer.echo(f"QA-PDF FAIL: {reasons2}")
        raise typer.Exit(3)
    typer.echo(f"OK [{engine}] {out} — QA stamp: pages+TOC+CTA verified")


@app.command(name="validate")
def validate_cmd(path: str = typer.Argument(...)) -> None:
    ok, reasons = validate_pdf(path)
    typer.echo(f"{'PASS' if ok else 'FAIL'} {reasons}")
    if not ok:
        raise typer.Exit(1)


@app.command(name="list-templates")
def list_templates() -> None:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "templates")
    for f in sorted(os.listdir(base) if os.path.exists(base) else []):
        typer.echo(f)


if __name__ == "__main__":
    app()
