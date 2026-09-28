# API Reference

Interactive OpenAPI documentation is available at `http://localhost:8000/docs` while the backend is running.

All `/v1` routes require authentication. Development mode accepts `X-User-ID`; production must disable `DEV_AUTH_BYPASS` and use a signed bearer token.

## Profiles

- `GET /v1/profiles`
- `POST /v1/profiles`
- `PATCH /v1/profiles/{profile_id}`
- `DELETE /v1/profiles/{profile_id}`

## Chat

- `POST /v1/chat`

The backend owns safety screening and agent routing. Clients should display the returned `urgency`, `recommended_action`, and `disclaimer` fields.

## Appointments

- `GET /v1/appointments`
- `POST /v1/appointments/slots/search`
- `POST /v1/appointments`
- `PATCH /v1/appointments/{appointment_id}`
- `DELETE /v1/appointments/{appointment_id}`

Mutation requests include `confirmed: true`. The backend still generates the provider idempotency key and enforces ownership.

## Memory

- `GET /v1/memory`
- `DELETE /v1/memory/{memory_id}`

