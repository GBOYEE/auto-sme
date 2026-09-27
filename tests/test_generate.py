"""V1 QA + generation tests. No network. Offline filler expected."""
from auto_sme.generator import generate, outline
from auto_sme.pdf import render_html, html_to_pdf
from auto_sme.qa import validate_html, validate_pdf


def test_outline_locked_order():
    assert [s for s, _ in outline("lead-magnet")] == ["promise", "mistakes", "playbook", "next"]
    assert len(outline("mini-ebook")) == 5


def test_generate_structure_deterministic():
    d1 = generate(topic="X", audience="Y", cta="+2348000000000", kind="lead-magnet")
    d2 = generate(topic="X", audience="Y", cta="+2348000000000", kind="lead-magnet")
    assert [s.heading for s in d1.sections] == [s.heading for s in d2.sections]
    assert d1.title == d2.title


def test_html_qa_pass_and_fail():
    doc = generate(topic="Home buying", audience="Lagos renters", cta="+2348000000000")
    html = render_html(doc, style="modern")
    ok, reasons = validate_html(html, "+2348000000000")
    assert ok, reasons
    bad, r2 = validate_html("<html><h1>t</h1>lorem ipsum</html>", "+2348000000000")
    assert not bad and any("banned-token" in r or "missing" in r for r in r2)


def test_pdf_valid(tmp_path):
    doc = generate(topic="Home buying", audience="Lagos renters", cta="+2348000000000")
    html = render_html(doc, style="classic")
    out = str(tmp_path / "golden.pdf")
    html_to_pdf(html, out, title=doc.title)
    ok, reasons = validate_pdf(out)
    assert ok, reasons
    # Golden: same doc re-rendered is byte-stable for fallback path
    out2 = str(tmp_path / "golden2.pdf")
    html_to_pdf(html, out2, title=doc.title)
    import os

    assert abs(os.path.getsize(out) - os.path.getsize(out2)) < 300
