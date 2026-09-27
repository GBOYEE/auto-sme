"""Visual hierarchy scorer tests: target look vs fallback reality."""
from auto_sme.generator import generate
from auto_sme.pdf import render_html, load_css
from auto_sme.qa import validate_visual


def test_target_look_scores_high_without_pdf():
    for style in ("modern", "classic", "bold"):
        doc = generate(topic="T", audience="A", cta="+2348000000000")
        html = render_html(doc, style=style)
        s, _ = validate_visual(html, load_css(style), pdf_path="", engine="preview")
        assert s >= 80, (style, s)


def test_fallback_pdf_caps_footer_points_honestly(tmp_path):
    from auto_sme.pdf import html_to_pdf

    doc = generate(topic="T", audience="A", cta="+2348000000000")
    html = render_html(doc, style="modern")
    out = str(tmp_path / "f.pdf")
    engine = html_to_pdf(html, out, title=doc.title)
    s, breakdown = validate_visual(html, load_css("modern"), pdf_path=out, engine=engine)
    assert engine == "fallback"
    assert s >= 70  # structure strong, render capped
    assert any("footer" in b for b in breakdown)


def test_broken_html_scores_low():
    s, _ = validate_visual("<html><p>lorem xxx</p></html>", "body{color:#fff}", "", "preview")
    assert s < 40
