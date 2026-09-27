# AUTO-SME V1 — Build Contract (service-production engine)

> Status: DRAFT for review. No code changes land until this doc is approved.
> Repo: `github.com/GBOYEE/auto-sme` @ `c42bfdc` (2026-09-27).
> Local TPT/FEM factory (`Default Project/FEM-001`) is OUT OF SCOPE. Borrow patterns only. No import of product, assets, templates, or business logic.

## 1. Mission (one line)

A customer gives topic + audience + CTA → AUTO-SME produces a professional, QA-passed PDF ready to deliver in 24h.

Optimize for that measurable outcome. Do not build a SaaS platform.

## 2. Current truth (verified 2026-09-27)

- Code is inventory API, not generator:
  - `src/auto_sme/cli.py` (7 lines): `create_app() + uvicorn.run`, no `generate`.
  - `src/auto_sme/main.py`: FastAPI `AutoSME v0.2.0`, `/health`, `/metrics`, routers `tasks,inventory,orders,reports,whatsapp`.
  - `src/auto_sme/models.py`: `Product, Order, Task, OptOut` (SQLAlchemy).
  - `tests/test_api.py, test_crud.py` only. No QA tests.
  - `pyproject.toml`: `fastapi, sqlalchemy, twilio, reportlab` present; `jinja2, weasyprint, openai` absent.
  - `templates/` 404 on GitHub. `docker-compose.yml` runs `postgres:16 + redis:7 + api`.
- Docs are split:
  - `README.md + docs/architecture.md + docs/api.md` promise content pipeline (`generate -t *.j2 -o *.pdf`, `Pipeline.run()`, Ollama/OpenRouter).
  - `README-PRODUCTION.md + DEPLOYMENT.md + PILOT.md` describe WhatsApp shop for 5 SMEs Lagos/Nairobi/Addis.
- `pyproject version 0.1.0` vs `APP_VERSION 0.2.0` drift.

Conclusion: 2 products in 1 repo. V1 locks content-engine as truth, archives API.

## 3. Promise (v1 sellable)

- Offer: 24h Lead-Magnet / Mini-Ebook — $250 fixed (US) ; Naija church volume is v1.1, not v1.
- Input: topic + audience + CTA (phone/link) + tone (optional).
- Output: 8-12p PDF (lead-magnet) or 12p (mini-ebook) with cover, TOC, body, CTA page, footer page numbers, QA stamp on last page.
- Delivery: PDF via WhatsApp/email + source files. 50% upfront, balance on delivery.

## 4. Non-goals (v1 will NOT build)

SaaS multi-tenancy, auth/billing portal, EPUB/DOCX/audiobook, web builder UI, dashboard, WhatsApp shop/inventory, ads funnel, TPT/FEM import. If encountered, stop and ask — do not silently expand scope.

## 5. Target tree (v1)

```text
src/auto_sme/
  cli.py            # Typer: generate | validate | list-templates
  generator.py      # OpenAI primary, Ollama fallback, per-section prompts, retry max 2
  pdf.py            # WeasyPrint ONLY (remove ReportLab)
  qa.py             # content + visual validators
templates/
  lead-magnet.j2    # 8-10p
  mini-ebook.j2     # 12p
  _cover.j2 _toc.j2 _cta.j2 _footer.j2
styles/
  modern.css classic.css bold.css   # --style= switch
tests/
  test_generate.py test_qa.py + golden snapshot
samples/
  realtor-buyer-guide.pdf coach-meal-plan.pdf
legacy-api/ branch: main.py, api/, routers/, models.py, crud.py, database.py, dependencies.py, test_api/crud.py
```

## 6. Acceptance criteria (18 — report as Completed X/18 — Z%)

1. Architecture/spec [ ] — this doc + `03-architecture.md + 04-contracts.md` approved.
2. Legacy API isolated [ ] — `legacy-api` branch holds API; `main` has 0 `from .routers` imports; `pytest` collects 0 API tests.
3. Structured generation [ ] — same topic → same section order; no lorem; CTA injected.
4. Lead Magnet template [ ] — 8-10p renders with no missing vars.
5. Mini-Ebook template [ ] — 12p renders with no missing vars.
6. Reusable components [ ] — both templates use `_cover/_toc/_cta/_footer`, no duplicated HTML.
7. 3 visual styles [ ] — same content → 3 distinct PDFs, all QA pass.
8. WeasyPrint renderer [ ] — `reportlab` removed; fonts embedded; tables don't split mid-row.
9. Content QA [ ] — page-count ±1, TOC present, CTA present, no placeholder, grade band. Bad fixture fails with named reason.
10. Visual/PDF QA [ ] — margins, contrast, alt text, no overflow, footer every page. Faulty PDF fails.
11. OpenAI integration [ ] — `OPENAI_API_KEY` only, redacted logs, <3min for 10p.
12. Fallback provider [ ] — `OLLAMA_HOST` (default `llama3.1`) same interface; offline draft works.
13. CLI [ ] — `generate --topic --audience --cta --template --style -o`, `validate`, `list-templates`; `--help` clean-clone.
14. Golden/regression tests [ ] — `pytest -v` green; CI blocks on fail; 1 golden hash + visual tolerance.
15. Realtor sample [ ] — `samples/realtor-buyer-guide.pdf` QA-stamped, phone-clean.
16. Coach sample [ ] — `samples/fitness-meal-plan.pdf` same.
17. Clean-clone verification [ ] — fresh clone + `pip install -e .` + `cp .env.example .env` → both samples, 0 fixes. Transcript required.
18. Docker verification [ ] — `docker compose up --build` generates inside container. Log + `ls -lh samples/`.
19. Commercial README [ ] — promise + $250 + order link slot + 2 thumbs + Loom slot, 60-sec comprehension, no TPT claims.

Progress reports must list files changed, tests run, runtime evidence, remaining, blockers.

## 7. Config (v1 defaults — change only by decision)

- LLM: OpenAI primary, Ollama `llama3.1` fallback (matches `docs/architecture.md`).
- Styles: Modern / Classic / Bold.
- Samples: Realtor Buyer Guide + Fitness Meal Plan.
- Deploy: Docker only for v1; Railway later.
- Env: `OPENAI_API_KEY` required, `OLLAMA_HOST` optional, `AUTOSME_*` API keys archived with legacy branch.

## 8. v1.1 Church Pack (DISCUSSION ONLY — no build in v1)

Naija volume idea (many churches, weekly flyers/programs, low price high volume, minister images in → solid design out, WhatsApp review loop). Captured as GitHub issue for scoping after v1 sellable. Needs decisions: flyer-first vs program-first, image-quality rule (phone pics), revision limit, price (per-flyer vs 30k/8-designs monthly), per-church brand lock, JPG for IG/WhatsApp + PDF for print.

## 9. Risks

Tool market saturated (Inkfluence $9.99/mo, Designrr $29/mo, Canva $12.99/mo) — v1 wins as rush service, not SaaS. Upwork 50-bid competition — win via niche + 24h + Loom proof + DM where buyers live. Secrets — no keys committed; `.env.example` only.
