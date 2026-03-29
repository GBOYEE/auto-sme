# 01-04: Deploy to VPS and Pilot with 5 SMEs

**Epic:** MVP Core

## Goal

Launch AutoSME on a VPS, onboard 5 real small businesses, collect feedback.

## Acceptance Criteria

- Server (Ubuntu 22.04) with domain (e.g., api.autosme.io)
- TLS via Let's Encrypt (certbot)
- PostgreSQL + backups
- Systemd service for FastAPI + Gunicorn
- 5 pilot SMEs signed up (friends/network), each with tenant ID and API key
- Manual pilot: they place orders via WhatsApp, view inventory, receive reports
- Feedback documented in `pilot-feedback.md`

## Tasks

1. Provision VPS (Hetzner, DigitalOcean)
2. Install Docker or native Python; set up PostgreSQL
3. Clone repo, install deps, run migrations
4. Configure Nginx reverse proxy + TLS
5. Create admin script to add tenants and API keys
6. Onboard pilots: send API keys, quick guide
7. Monitor logs for 1 week; collect feedback
8. Iterate quickly on bugs

## Dependencies

01-03 (WhatsApp working locally)

## Time Estimate

8 hours (plus 1 week pilot monitoring)
