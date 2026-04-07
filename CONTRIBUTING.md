# Contributing to xander-nexus

Thank you for considering contributions! This document outlines the process.

## 🛠️ Development Setup

1. Fork the repo and clone your fork
2. Install deps: `pip install -r requirements.txt` and `npm install` in `app/`
3. Copy `.env.example` to `.env` and fill values (see `docs/configuration.md`)
4. Run migrations: `python scripts/migrate.py`
5. Start services: `docker compose up -d postgres redis`
6. Run API: `uvicorn app.main:app --reload`
7. Run frontend: `cd app && npm run dev`

## 🧪 Testing

```bash
# Backend tests
pytest tests/ -v --cov=app

# Frontend tests
npm test
```

Aim for >80% coverage on backend.

## 📝 Code Style

- **Python:** Black, isort, flake8. Run `pre-commit install`.
- **TypeScript/React:** ESLint + Prettier (included in pre-commit).

Commit messages: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)

## 🔄 Pull Request Process

1. Create a feature branch from `main`
2. Make changes, add tests, ensure CI passes
3. Update README or docs if needed
4. Open PR with clear description and linked issue
5. Wait for review (1–2 maintainers)
6. Once approved, we’ll squash-merge

## 🐛 Bug Reports

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml). Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python/Node versions, Docker)

## 💡 Feature Requests

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml). Describe:
- The problem you’re solving
- Proposed solution
- Alternatives considered
- Mockups if UI-related

## 📜 Code of Conduct

Please read and follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Harassment or abuse will not be tolerated.

## 🔒 Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## ❓ Questions

Open a [GitHub Discussion](https://github.com/GBOYEE/xander-nexus/discussions) or join our Discord (link in README).
