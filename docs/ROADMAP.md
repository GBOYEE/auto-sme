# ROADMAP — AUTO-SME V1 to sellable (nothing generic)

Target: topic + audience + CTA in → QA-passed PDF out in <60min, 24h rush service $250. 2 sales = $500.
Contract: `docs/00-v1-contract.md` (18 criteria). Issues #1-#7 track it.

## M0 Spec — DONE 2026-09-27
- `docs/00-v1-contract.md` @ `5c93094`, issues #1-#7 open.

## M1 Legacy isolation (#2) — today
- Branch `legacy-api` holds: `src/auto_sme/main.py, api/, routers/, models.py, crud.py, database.py, dependencies.py, tests/test_api.py, test_crud.py`, compose postgres/redis.
- Main deletes them, archives `PILOT.md → docs/later-africa.md`.
- Accept: `grep -r "from .routers" src/ = 0`, `pytest collects 0 API tests`.

## M2 Engine rebuild (#3) — today
- Files: `src/auto_sme/cli.py (Typer), generator.py (OpenAI→Ollama llama3.1), pdf.py (WeasyPrint only)`.
- Deps: add `jinja2, weasyprint, openai, typer, httpx`; remove `reportlab` core, demote `fastapi/sqlalchemy/twilio` to extra.
- Accept: `auto-sme --help` clean-clone, 10p <3min live, offline fallback drafts.

## M3 Templates + styles (#4) — today
- `templates/lead-magnet.j2 (8-10p), mini-ebook.j2 (12p), _cover/_toc/_cta/_footer.j2`, `styles/modern|classic|bold.css`.
- Accept: same content → 3 distinct QA-pass PDFs.

## M4 QA + golden (#5) — today
- `qa.py`: pages ±1, TOC, CTA phone/link, no lorem, grade band; visual: margins, contrast, footer-every-page.
- `tests/test_generate.py + test_qa.py` + 1 golden hash. CI blocks on fail.
- Accept: `pytest -v` green, bad fixtures fail with named reason.

## M5 Samples + verify + README (#6) — today
- `samples/realtor-buyer-guide.pdf + fitness-meal-plan.pdf` QA-stamped, phone-clean.
- Clean-clone + `docker compose up --build` transcripts. Commercial README (promise+$250+order link+thumbs+Loom, no TPT).
- Accept: 2 PDFs + logs + 60-sec comprehension.

## Out of scope v1
SaaS, EPUB/DOCX, dashboard, WhatsApp shop. v1.1 Church Pack = #7 discussion only.

Progress format: `Completed X/18 — Z%` + files + tests + evidence.
