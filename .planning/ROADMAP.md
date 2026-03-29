# Roadmap: AutoSME

## Phases

- [ ] **Phase 1: MVP Core** — Backend API, WhatsApp integration, basic scheduling
- [ ] **Phase 2: SME Features** — Inventory, sales reports, simple dashboard
- [ ] **Phase 3: Multi‑tenant & Billing** — Stripe, usage quotas, admin panel
- [ ] **Phase 4: Scale & Impact** — 500+ users, metrics, case studies, grant reports

### Phase 1 (v0.5.0)

Plans:
- 01-01: Design API schema (tasks, inventory, orders)
- 01-02: Build FastAPI backend with agent‑core + automation‑engine
- 01-03: Integrate WhatsApp via Twilio (incoming/outgoing)
- 01-04: Deploy to VPS, test with 5 pilot SMEs

### Phase 2 (v0.6.0)

Plans:
- 02-01: Inventory model (products, stock levels, low‑stock alerts)
- 02-02: Sales report generator (daily/weekly PDF)
- 03-03: Simple web dashboard (React Lite or HTML)
- 02-04: Documentation and onboarding videos

### Phase 3 (v0.7.0)

Plans:
- 03-01: Multi‑tenant database schema (tenant_id)
- 03-02: Stripe integration (subscriptions, usage caps)
- 03-03: Admin panel (view all tenants, usage, support)
- 03-04: Security hardening (HTTPS, rate limiting, audit logs)

### Phase 4 (v0.8.0 → v1.0.0)

Plans:
- 04-01: Scale to 500 users (optimizeDB, caching)
- 04-02: Impact measurement dashboard (time saved, revenue impact)
- 04-03: Create case studies and grant reports
- 04-04: Publish open‑source core; release public API docs

**Total plans:** 16
