# 01-03: Integrate WhatsApp via Twilio

**Epic:** MVP Core

## Goal

Connect Twilio WhatsApp Business API to AutoSME orders webhook.

## Acceptance Criteria

- Twilio number purchased, webhook URL configured to `POST /webhook/whatsapp`
- Incoming messages parsed: customer sends product name + quantity → creates Order
- Auto‑reply confirms order and inventory deduction
- Status updates sent to customer (e.g., "out for delivery")
- Handle opt‑out keywords (STOP)
- Tested with sandbox or test number

## Tasks

1. Create Twilio account; buy number (use trial credits)
2. Implement `/webhook/whatsapp` endpoint (validate signature)
3. Parse incoming WhatsApp message (use regex or simple NL)
4. Create Order in DB; adjust inventory
5. Send reply via Twilio client
6. Add error handling (invalid product, out of stock)
7. Log all WhatsApp interactions for debugging

## Dependencies

01-02 (backend running)

## Time Estimate

6 hours
