# Security Policy

## Supported Versions

Only the latest `main` branch receives security updates.

## Reporting a Vulnerability

If you discover a security vulnerability, please do **not** open a public issue. Instead, email the maintainer directly:

**Email:** Oyebanjiadegboyee@gmail.com

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

We aim to respond within 48 hours and will work with you to resolve the issue promptly. Once fixed, we will publicly acknowledge your contribution (if desired) in the release notes.

## Best Practices for Deployers

- Use strong, randomly generated passwords for database and admin accounts
- Keep Docker images updated (`docker compose pull`)
- Enable HTTPS in production (use a reverse proxy like Nginx with TLS)
- Restrict access to the API (use firewall rules or VPN)
- Regularly rotate secrets and API keys
- Monitor logs for suspicious activity

## Known Issues

None at this time.
