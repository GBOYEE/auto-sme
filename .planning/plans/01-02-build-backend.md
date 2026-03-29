# 01-02: Build FastAPI Backend with agent‑core + automation‑engine

**Epic:** MVP Core

## Goal

Implement API endpoints using existing frameworks; glue code only.

## Acceptance Criteria

- `main.py` starts FastAPI app
- Endpoints from 01‑01 functional
- Agent‑core used for: interpreting natural‑language task creation (e.g., "remind me to restock every Monday")
- Automation‑engine used for: scheduling, webhook handling
- SQLite DB with tenant isolation (tenant_id in tables)
- All endpoints tested with pytest (client calls)

## Tasks

1. Set up project: `src/`, `tests/`, `requirements.txt`
2. Create FastAPI app with routers
3. Integrate agent‑core Agent for NLU of task descriptions
4. Use automation‑engine Scheduler to enqueue tasks
5. Implement CRUD for inventory + orders
6. Write integration tests (pytest + TestClient)
7. Document `.env` variables (DB path, secret keys)

## Dependencies

01-01 (API spec)

## Time Estimate

8 hours
