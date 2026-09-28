# Deployment Guide

The repository does not require Docker. Build and verification are driven from the root Node.js scripts, while the API is deployed as a Python/Uvicorn service and the React build is deployed as static web assets.

## Build artifacts

```bash
npm run setup
npm test
npm run build
```

The frontend output is written to `frontend/dist`. Start the API in its target Python environment with:

```bash
python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

Use the deployment platform's native process manager, health checks, TLS termination, secret store, and static-site hosting.

## Production configuration

1. Set `APP_ENV=production` and `DEV_AUTH_BYPASS=false`.
2. Configure a strong JWT validation secret or replace the local validator with the organization's OIDC/JWKS integration.
3. Set `DATABASE_URL` to a persistent SQLite location such as `sqlite:///./data/healthcare.db` and ensure only the API process can access it.
4. Back up the SQLite database file and use one API worker for write safety. If horizontal scaling is later required, plan a deliberate database migration.
5. Set `REDIS_URL` to a TLS-enabled managed Redis endpoint when shared session memory is required.
6. Configure `LLM_API_KEY` only in the workload secret store.
7. Set the exact frontend origins in `CORS_ORIGINS`.

The application creates the SQLite schema at startup. The reference DDL is available in `backend/app/database/migrations/001_initial_schema.sql` for controlled deployments.

## Required release gates

- Clinical safety review of prompts, red flags, and fallback messages.
- Security review of authentication, authorization, encryption, and secret handling.
- Privacy review of consent, retention, deletion, and audit behavior.
- End-to-end validation of local slot generation, booking, rescheduling, cancellation, and collision prevention.
- Load, timeout, retry, and dependency-failure testing.
