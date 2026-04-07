# auto-sme Architecture

## Pipeline Stages

1. **Template Loading** — Jinja2 template defines document structure and placeholders
2. **Content Generation** — LLM (Ollama/OpenRouter) fills each placeholder via prompts
3. **Assembly** — Content inserted into template, Markdown → HTML
4. **PDF Generation** — WeasyPrint converts HTML to print-ready PDF
5. **QA Validation** — Checks page counts, vocabulary terms, multiple choice counts
6. **Asset Generation** — Creates SVG diagrams, NGSS alignment, differentiation notes

## Determinism

- Templates are static — same template always produces same structure
- LLM prompts are templated with clear constraints
- QA layer rejects out-of-spec outputs; requires manual review or retry
- Entire pipeline is reproducible end-to-end

## Usage

```bash
auto-sme generate --template science_earth_water_cycle.j2 --output unit.pdf
```

## Extending

- Add new templates in `templates/`
- Add new QA checks in `qa/`
- Add new asset generators in `assets/
