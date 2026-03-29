# Deployment Guide

AutoSME can be deployed on a VPS using Docker Compose.

## Prerequisites

- Ubuntu 22.04 (or similar)
- Docker Engine (20.10+)
- Docker Compose (v2)
- Domain name pointing to VPS IP (e.g., `api.autosme.io`)
- Optional: Nginx + Certbot for HTTPS

## Steps

1. **Provision VPS**
   - Recommended: DigitalOcean Droplet, Hetzner Cloud, or AWS EC2 (t3.micro)
   - OS: Ubuntu 22.04 LTS
   - Ensure ports 80 and 443 are open.

2. **Install Docker & Compose**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   sudo apt-get install docker-compose-plugin
   ```

3. **Clone repository**
   ```bash
   git clone https://github.com/your-org/auto-sme.git
   cd auto-sme
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env` and edit:
     ```bash
     cp .env.example .env
     # edit .env: set API_KEY_SECRET to a strong random string
     ```
   - For production, you should also set up PostgreSQL and update `DATABASE_URL`.

5. **Run with Docker Compose**
   ```bash
   docker compose up -d
   ```
   This builds the image and starts the API on port 8000.

6. **Set up Nginx + TLS (optional but recommended)**
   - Install Nginx and Certbot:
     ```bash
     sudo apt-get install nginx certbot python3-certbot-nginx
     ```
   - Copy `nginx.conf` to `/etc/nginx/sites-available/autosme` and adapt `server_name`.
   - Enable site: `sudo ln -s /etc/nginx/sites-available/autosme /etc/nginx/sites-enabled/`
   - Test Nginx: `sudo nginx -t`
   - Reload: `sudo systemctl reload nginx`
   - Obtain TLS cert: `sudo certbot --nginx -d api.autosme.io`
   - The nginx config proxies to `127.0.0.1:8000`.

7. **Verify installation**
   - Health: `https://api.autosme.io/health` should return `{"status":"ok"}`
   - Swagger UI: `https://api.autosme.io/docs` (if you expose directly; otherwise use port 8000)

8. **Seed initial data (optional)**
   - Use API to create products and test orders.

9. **Monitoring**
   - Check logs: `docker compose logs -f api`
   - Set up Prometheus/Grafana if needed (future phase).

## Updating

```bash
git pull
docker compose build --no-cache
docker compose up -d
```

## Notes

- For production, use a managed PostgreSQL (RDS, Supabase, etc.) and set `DATABASE_URL`.
- Store API keys securely; rotate regularly.
- Enable rate limiting and WAF (Cloudflare) for public endpoints.
