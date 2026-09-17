# Security

- Never commit `.env`, production secrets, database credentials or signing keys.
- Use HTTPS and `COOKIE_SECURE=1` in production.
- Add CSRF protection, rate limiting, email/phone verification and secure media scanning before public deployment.
- Owner/admin access must use explicit roles and audited credentials; no hidden backdoor is included.
