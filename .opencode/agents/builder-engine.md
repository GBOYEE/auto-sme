---
mode: subagent
description: Implements engine milestone files only (generator, CLI, PDF renderer). Smallest diff.
permission:
  edit: allow
  bash: allow
---

Scope: src/auto_sme/generator.py, src/auto_sme/cli.py, src/auto_sme/pdf.py, pyproject.toml deps, .env.example.

Rules:
- Use disciplined-changes skill: verify before acting, smallest change that works, no drive-by refactors.
- Interfaces locked by docs/04-contracts.md: generate(topic,audience,cta,kind), render_html(doc,style,visual_score,engine), html_to_pdf(html,out,title,doc,style,visual_score).
- LLM order: OpenAI primary (temp 0) -> Ollama llama3.1 fallback -> offline deterministic filler. Never log keys.
- Renderer order: WeasyPrint -> fpdf2 styled (needs doc) -> minimal. Never break offline verify.
- Run before finishing: $env:PYTHONPATH="src"; python -m pytest tests/test_generate.py -q
- Return: files changed + test output + remaining. Never touch templates/, styles/, TPT paths.
