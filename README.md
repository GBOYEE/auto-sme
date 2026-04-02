# AutoSME 🚀

AI automation for African small businesses. Production-ready FastAPI backend with inventory, orders, WhatsApp integration, and PDF reporting.

[![CI](https://github.com/GBOYEE/auto-sme/actions/workflows/ci.yml/badge.svg)](https://github.com/GBOYEE/auto-sme/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **Inventory Management** — add products, adjust stock levels
- **Order Processing** — create orders, automatic stock deduction
- **WhatsApp Integration** — receive orders via Twilio webhook
- **Sales Reports** — generate PDF reports for date ranges
- **Scheduled Tasks** — cron-like automation (future)
- **Observability** — health checks, metrics, structured logging
- **Secure** — API key authentication, CORS controls

---

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/GBOYEE/auto-sme
cd auto-sme
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]

# Set a strong API key
export AUTOSME_API_KEY=super-secret-key

# Run development server
auto-sme

# Or directly:
uvicorn src.auto_sme.main:app --reload
```

Open API docs: http://localhost:8000/docs

---

## 🔐 Authentication

All endpoints (except `/webhook/whatsapp`) require an API key:

```
X-API-Key: your-secret-key
```

Set via `AUTOSME_API_KEY` environment variable.

---

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/inventory` | Add product |
| `GET` | `/api/v1/inventory` | List products |
| `PATCH` | `/api/v1/inventory/{id}?delta=N` | Adjust stock (+/-) |
| `POST` | `/api/v1/orders` | Create order (deducts stock) |
| `GET` | `/api/v1/reports/sales?start_date=...&end_date=...` | PDF sales report |
| `POST` | `/webhook/whatsapp` | Twilio WhatsApp webhook (public) |

---

## 🏗️ Architecture

See [Production Guide](README-PRODUCTION.md#architecture) for system diagram and component overview.

---

## 🛠️ Development

```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v

# Type checking
mypy src/auto_sme
```

---

## 📡 Observability

- **Health**: `GET /health` — returns `{status, timestamp, version, environment}`
- **Metrics**: `GET /metrics` — returns `{requests_total, requests_failed}`

---

## 🚢 Deployment

- **Docker**: `docker-compose up -d`
- **Systemd**: See `README-PRODUCTION.md` for unit file
- **Nginx**: Reverse proxy to `localhost:8000`

Full deployment guide: [README-PRODUCTION.md](README-PRODUCTION.md)

---

## 🔒 Security

- Change default `AUTOSME_API_KEY` before deploying
- Use HTTPS in production
- Restrict `AUTOSME_CORS_ORIGINS` to your domains
- Keep `AUTOSME_ENV=production` in production

---

## 📄 License

MIT — see [LICENSE](LICENSE).
