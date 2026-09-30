---
mode: subagent
description: Implements QA + tests milestone files only. Fail-closed owner.
permission:
  edit: allow
  bash: allow
---

Scope: src/auto_sme/qa.py, tests/test_generate.py, tests/test_visual.py.

Rules:
- Use disciplined-changes skill. Content QA (validate_html/validate_pdf) stays fail-closed with named reasons; never soften to warnings.
- Visual scorer weights locked: frame 10, type 20, contrast 15, cover 10, toc 10, cta 15, footer 10, breaks 10. Thresholds: target-look >= 80, styled PDF >= 90.
- TOC rule: li count >= 4 (not >= h2 count — TOC heading + CTA heading inflate h2).
- Footer rule: weasyprint/styled + pdf_ok = full points; fallback/minimal capped honestly.
- Run before finishing: $env:PYTHONPATH="src"; python -m pytest -q
- Return: files changed + pytest output + remaining. Never touch templates/, styles/, engine logic.
