# Healthcare Multi-Agent Platform

A React and FastAPI healthcare-assistant platform with four LangGraph agents, local appointment booking, optional Redis short-term memory, and SQLite durable storage.

## Product Scope

The application provides four capabilities through one patient-facing React interface:

| Capability | Implementation |
|---|---|
| General care guidance | LangGraph General Care Agent |
| Baby and child care guidance | LangGraph Baby Care Agent |
| Maternity and postpartum guidance | LangGraph Maternity Care Agent |
| Appointment management | LangGraph Booking Agent with local SQLite scheduling |

The clinical agents provide informational support and care-navigation assistance. They must not diagnose, prescribe, or replace a licensed clinician. Red-flag situations are handled by a mandatory backend safety workflow.

## Architecture

```text
React + TypeScript frontend
            |
            | HTTPS, authenticated API requests
            v
FastAPI application and LangGraph supervisor
      |              |                 |
      |              |                 +-- Local appointment service
      |              +-- Redis session memory
      +-- SQLite profiles, memory, appointments, and audit records
```

## Documentation

- [Functionality roadmap](ROADMAP.md): development phases, implementation sub-phases, and file-level deliverables.
- [System design](design.md): layer boundaries, runtime architecture, data flow, and technical decisions.
- [Requirements](requirements.md): functional, non-functional, MVP, and production requirements.
- [Technical guide](TECHNICAL_GUIDE.md): target architecture, contracts, data model, workflows, safety, and API design.
- [API reference](docs/API.md): implemented HTTP routes and client responsibilities.
- [Deployment guide](docs/DEPLOYMENT.md): production configuration and release gates.

## Repository Layout

```text
.
├── backend/                # FastAPI, LangGraph, SQLite, Redis and local booking
├── frontend/               # React + TypeScript patient application
├── tools/                  # Node.js setup, development, and test runners
├── docs/                   # API and deployment documentation
├── package.json            # Root Node.js commands
├── ROADMAP.md
├── design.md
├── requirements.md
├── TECHNICAL_GUIDE.md
└── README.md
```

## Development Phases

| Phase | Layer | Primary output |
|---|---|---|
| Phase 0 | Database | SQLite models, repositories, Redis and durable memory |
| Phase 1 | FastAPI | Authentication, profiles, chat, memory, and appointment APIs |
| Phase 2 | AI | LangGraph supervisor, safety gate, specialist agents, model adapter |
| Phase 3 | React | Patient interface and Node.js development workflow |

See [ROADMAP.md](ROADMAP.md) for sub-phases, files, deliverables, and acceptance criteria.

## Run Locally with Node.js

Node.js manages project setup and starts the React and FastAPI development processes. FastAPI and LangGraph still run in Python.

Install all dependencies and create local environment files:

```bash
npm run setup
```

In Windows PowerShell, use `npm.cmd` instead of `npm` if script execution policy blocks `npm.ps1`, for example `npm.cmd run setup`.

Start the backend and frontend together:

```bash
npm run dev
```

Then open:

- React application: `http://localhost:5173`
- FastAPI documentation: `http://localhost:8000/docs`
- Backend health check: `http://localhost:8000/health`

Run one layer independently when needed:

```bash
npm run dev:api
npm run dev:web
```

Run the backend tests, frontend lint, and frontend production build:

```bash
npm test
```

The same checks run automatically on pushes and pull requests through GitHub Actions.

The application uses SQLite for profiles, memories, appointments, and audit events. Redis is optional; without it, development uses in-process session memory. Without an LLM key, care agents use deterministic safe responses.

## Local Prerequisites

- Python 3.11+
- Node.js 20+
- Redis endpoint when testing Redis-backed short-term memory
- LLM provider credentials for generated responses

## Environment Variables

Do not commit secrets. Create backend and frontend `.env` files from their respective examples.

```text
# backend/.env
APP_ENV=development
DATABASE_URL=sqlite:///./healthcare.db
JWT_ISSUER=
JWT_AUDIENCE=
REDIS_URL=redis://localhost:6379/0
LLM_API_KEY=
```

```text
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## Delivery Principles

- Build backend safety, authorization, and auditability before enabling clinical chat.
- Keep appointment mutations behind the local appointment service and require confirmation.
- Use Redis for expiring session context only; use SQLite for consented, durable records.
- Require explicit confirmation before appointment creation, cancellation, or rescheduling.
- Treat all health information as sensitive: minimize storage, redact logs, and enforce access control.
