# 01-01: Design API Schema

**Epic:** MVP Core

## Goal

Define REST API endpoints for AutoSME: tasks, inventory, orders, webhooks.

## Acceptance Criteria

- OpenAPI/Swagger spec (YAML or Python dict)
- Endpoints:
  - `POST /api/v1/tasks` (create scheduled task)
  - `GET /api/v1/tasks` (list)
  - `POST /api/v1/inventory` (add product)
  - `PATCH /api/v1/inventory/{id}` (adjust stock)
  - `POST /api/v1/orders` (WhatsApp order webhook)
  - `GET /api/v1/reports/sales` (generate PDF)
- Authentication: API key per tenant (simple)
- Documented with examples

## Tasks

1. Draft OpenAPI spec in `api/spec.yaml`
2. Define data models (Task, Product, Order, Report)
3. Write docstrings; generate interactive docs with FastAPI
4. Review for consistency; fix naming

## Dependencies

None

## Time Estimate

4 hours
