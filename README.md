# auto-sme — Deterministic AI Content Pipeline

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](docker-compose.yml)
[![CI](https://github.com/GBOYEE/auto-sme/actions/workflows/ci.yml/badge.svg)](https://github.com/GBOYEE/auto-sme/actions)
[![Coverage](https://img.shields.io/codecov/c/github/GBOYEE/auto-sme)](https://codecov.io/gh/GBOYEE/auto-sme)

**AI-assisted content generation that's deterministic, reproducible, and production-ready.** auto-sme uses templates, LLMs, and QA validation to generate structured documents (e.g., educational units) end-to-end.

<p align="center">
  <img src="https://raw.githubusercontent.com/GBOYEE/auto-sme/main/screenshots/pipeline.png" alt="auto-sme pipeline" width="700"/>
</p>

## ✨ Features

- 📝 **Template-Driven** — Jinja2 templates ensure consistent structure every time
- 🤖 **LLM Integration** — Fills content using OpenAI or Ollama
- 📄 **PDF Generation** — WeasyPrint produces print-ready, styled PDFs
- ✅ **QA Validation** — Automated checks for page counts, vocabulary, multiple choice questions
- 🎨 **Asset Generation** — SVGs, NGSS alignment, differentiation notes
- 🐳 **Docker Ready** — One-command pipeline execution

## 🚀 Quick Start

```bash
git clone https://github.com/GBOYEE/auto-sme.git
cd auto-sme
pip install -e .
auto-sme generate -t templates/earth_science_water_cycle.j2 -o water_cycle.pdf
```

## 🏗️ Pipeline Stages

1. **Template Loading** — Jinja2 defines document structure
2. **Content Generation** — LLM fills placeholders via prompts
3. **Assembly** — Insert content into template
4. **PDF Generation** — WeasyPrint renders HTML to PDF
5. **QA Validation** — Checks page counts, vocab terms, MC counts
6. **Asset Generation** — Creates diagrams, alignment notes

See [docs/architecture.md](docs/architecture.md) for details.

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| Templates | Jinja2 |
| LLM | OpenAI / Ollama |
| PDF | WeasyPrint (CSS-based) |
| QA | Custom validators (coverage, structure) |
| DevOps | Docker, CI |

## 🧪 Testing & CI

```bash
pytest tests/ -v --cov=auto_sme
```

CI runs lint, type-check, tests, and coverage upload on every push.

## 📚 Documentation

- [Getting Started](docs/README.md)
- [API Reference](docs/api.md)
- [Creating Templates](docs/templates.md)
- [Contributing](CONTRIBUTING.md)

## 🎯 Roadmap

- [ ] More output formats (EPUB, DOCX)
- [ ] Interactive template builder (web UI)
- [ ] Multi-language support
- [ ] Cloud storage backends (S3, GCS)
- [ ] Collaborative template editing

## 🤝 Contributing

We need help with:
- New template examples (different subjects)
- QA validators for new content types
- PDF styling improvements
- Performance optimizations for large documents

See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
Built by <a href="https://github.com/GBOYEE">Oyebanji Adegboyega</a> • 
<a href="https://gboyee.github.io">Portfolio</a> • 
<a href="https://twitter.com/Gboyee_0">@Gboyee_0</a>
</p>
