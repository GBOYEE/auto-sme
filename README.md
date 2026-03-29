# AutoSME

AI automation for African small businesses.

## Quickstart

```bash
pip install -e .
auto-sme
```

API available at http://localhost:8000/docs (Swagger UI).

## Endpoints

* `POST /api/v1/tasks` – create scheduled task
* `GET /api/v1/tasks` – list tasks
* `POST /api/v1/inventory` – add product
* `PATCH /api/v1/inventory/{id}` – adjust stock
* `POST /api/v1/orders` – create order (WhatsApp)
* `GET /api/v1/reports/sales?start_date=...&end_date=...` – PDF report

## Env vars

See `.env.example`.

## Roadmap

See `.planning/ROADMAP.md` and `.planning/STATE.md`.
