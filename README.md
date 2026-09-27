# auto-sme V1 — 24h Lead-Magnet / Mini-Ebook Engine ($250 fixed)

Topic + audience + CTA in → QA-passed PDF out tomorrow. Service-production engine, not SaaS.

## Order (copy-paste to buyer)
> Send topic + audience + phone/link. I deliver print-ready PDF in 24h for $250 (50% upfront). Sample PDFs below. WhatsApp: [YOUR NUMBER]. Pay: [Stripe/Paystack link].

## Samples (built by this repo, offline)
- `samples/realtor-buyer-guide.pdf` — modern, 8-10p lead magnet
- `samples/fitness-meal-plan.pdf` — classic, 12p mini-ebook
- `samples/realtor-bold.pdf` — same content, bold style (proves 3-style switch)

Demo video slot: [90-sec Loom: run generate live] — record before outreach.

## Run (one command, no keys needed for verify)
```bash
git clone https://github.com/GBOYEE/auto-sme.git && cd auto-sme
pip install -e .
cp .env.example .env   # add OPENAI_API_KEY only for paid quality; offline filler works without
PYTHONPATH=src python -m auto_sme.cli generate --topic "First-time home buying in Lagos" --audience "Lagos renters" --cta "+2348000000000" --style modern --out samples/out.pdf
PYTHONPATH=src python -m auto_sme.cli validate samples/out.pdf
PYTHONPATH=src python -m auto_sme.cli list-templates
```

With OpenAI key: same command uses `gpt-4o-mini` (temp 0). With `OLLAMA_HOST=http://localhost:11434`: uses `llama3.1` fallback. No key: deterministic offline filler (structure identical, QA still passes).

## QA stamp
Every PDF fails closed on: missing H1/TOC/CTA, <4 sections, banned tokens (lorem/todo/placeholder), over-complex sentences, non-PDF or <1.5KB. Stamp printed on last page.

## What this is NOT (v1 guardrails)
No SaaS, no dashboard, no EPUB, no WhatsApp shop (archived to `legacy-api` branch), no TPT/FEM import. Church Pack = v1.1 discussion (#7).

Details: `docs/00-v1-contract.md` + `docs/ROADMAP.md`.
