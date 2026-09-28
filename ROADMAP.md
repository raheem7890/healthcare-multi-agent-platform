# Functionality-Centric Development Roadmap

The project is implemented in four ordered phases. Each phase produces a usable layer with explicit interfaces for the following phase. Development should complete the acceptance criteria for a phase before treating the next phase as stable.

## Phase 0 — Database and Persistence Layer

### Objective

Establish the durable data model, Redis session memory, consent rules, repositories, and development database before exposing APIs or agent behavior.

### Phase 0.1 — Configuration and database connection

Implement environment configuration and a SQLAlchemy connection for a zero-configuration SQLite database.

Files:

```text
backend/app/config.py
backend/app/database/connection.py
backend/.env.example
backend/requirements.txt
```

Deliverables:

- Environment-based database selection.
- Managed SQLAlchemy sessions.
- Startup schema initialization for local development.
- Persistent SQLite database path for local and deployed single-instance environments.

### Phase 0.2 — Relational data model

Create entities for users, patient profiles, conversations, durable memories, appointments, and audit events.

Files:

```text
backend/app/database/models.py
backend/app/database/migrations/001_initial_schema.sql
```

Deliverables:

- User-to-profile ownership relationships.
- Separate adult, baby, child, and maternity profiles.
- Appointment records linked to users and profiles.
- Consent-aware durable memory records.
- Audit records that avoid raw health-message storage.

### Phase 0.3 — Repository layer

Place database queries behind repository classes so API, service, and agent code do not contain SQLAlchemy query details.

Files:

```text
backend/app/database/repositories/profiles.py
backend/app/database/repositories/appointments.py
backend/app/database/repositories/memory.py
backend/app/database/repositories/audit.py
```

Deliverables:

- User-scoped list, create, update, and delete operations.
- Appointment persistence using locally generated booking references.
- Durable memory retrieval filtered by user and profile.
- Centralized audit-event creation.

### Phase 0.4 — Short- and long-term memory

Implement an abstract session store, Redis implementation, local in-memory fallback, and SQLite-backed long-term memory service.

Files:

```text
backend/app/memory/session_models.py
backend/app/memory/session_store.py
backend/app/memory/long_term_memory.py
```

Deliverables:

- Redis session keys isolated by user and session.
- Configurable expiration and bounded message history.
- In-memory fallback when Redis is not configured.
- Long-term memory saved only when profile consent is enabled.

### Phase 0 acceptance criteria

- SQLite works without external infrastructure.
- The SQLite location can be configured using `DATABASE_URL`.
- Redis can be enabled using `REDIS_URL`.
- Every protected record is scoped to its owning user.
- Database and memory unit tests pass.

---

## Phase 1 — FastAPI and Application API Layer

### Objective

Expose authenticated, validated HTTP endpoints over the Phase 0 data layer and implement the service layer that coordinates business behavior.

### Phase 1.1 — FastAPI application bootstrap

Files:

```text
backend/app/main.py
backend/app/api/router.py
backend/app/api/routes_health.py
backend/app/schemas/common.py
```

Deliverables:

- FastAPI application startup.
- CORS configuration for the React frontend.
- `/health` readiness endpoint.
- Versioned `/v1` API prefix.
- OpenAPI documentation at `/docs`.

### Phase 1.2 — Authentication and authorization

Files:

```text
backend/app/security/auth.py
backend/app/security/authorization.py
```

Deliverables:

- Development identity using `X-User-ID` only when explicitly enabled.
- JWT verification for production.
- Profile, memory, and appointment ownership checks.
- Automatic rejection of cross-user resource access.

### Phase 1.3 — Profile and memory APIs

Files:

```text
backend/app/api/routes_profiles.py
backend/app/api/routes_memory.py
backend/app/schemas/profiles.py
backend/app/schemas/memory.py
```

Deliverables:

- Create, list, update, and delete patient profiles.
- Record and revoke long-term-memory consent.
- List and delete saved memory.

### Phase 1.4 — Appointment API and service

Files:

```text
backend/app/api/routes_appointments.py
backend/app/services/appointment_service.py
backend/app/schemas/appointments.py
```

Deliverables:

- Search appointment availability.
- Create, reschedule, and cancel appointments.
- Require explicit confirmation before every mutation.
- Generate weekday availability locally.
- Prevent conflicting bookings for the same care team and time.
- Persist confirmed appointment changes in SQLite.

### Phase 1.5 — Chat API shell

Files:

```text
backend/app/api/routes_chat.py
backend/app/services/chat_service.py
backend/app/schemas/chat.py
```

Deliverables:

- Validated chat request and response contracts.
- Profile-ownership validation before chat execution.
- Short- and long-term context loading.
- Audit record for every completed route decision.

### Phase 1 acceptance criteria

- Every `/v1` endpoint is authenticated.
- Invalid or unauthorized profile IDs are rejected.
- Appointment mutations fail without confirmation.
- OpenAPI accurately describes request and response models.
- API integration tests pass.

---

## Phase 2 — AI, LangGraph, and Clinical Safety Layer

### Objective

Build the supervisor graph, specialized agents, safety gates, model adapter, and memory-aware agent execution over the Phase 1 chat service.

### Phase 2.1 — Shared graph state

Files:

```text
backend/app/graph/state.py
backend/app/runtime.py
```

Deliverables:

- Typed state shared by every graph node.
- Runtime construction of the model, memory, booking, and agent dependencies.

### Phase 2.2 — Safety screening and response validation

Files:

```text
backend/app/safety/red_flags.py
backend/app/safety/screener.py
backend/app/safety/emergency_response.py
backend/app/safety/response_validator.py
```

Deliverables:

- Deterministic emergency red-flag screening before normal routing.
- Emergency responses that terminate the normal care flow.
- Post-generation checks for prohibited diagnostic or medication language.
- Safety audit events.

### Phase 2.3 — Specialist agents

Files:

```text
backend/app/agents/llm.py
backend/app/agents/general_care.py
backend/app/agents/baby_care.py
backend/app/agents/maternity_care.py
backend/app/agents/booking.py
```

Deliverables:

- General care, baby care, and maternity care prompts.
- Consistent `AgentResponse` output contract.
- Safe deterministic fallbacks when an LLM key is absent.
- Appointment handoff response from the booking agent.

### Phase 2.4 — Supervisor routing

Files:

```text
backend/app/agents/router.py
backend/app/graph/workflow.py
```

Deliverables:

- Routing priority: emergency, booking, maternity/baby specialty, general care.
- LangGraph conditional edges for specialist selection.
- Relevant Redis history and consented SQLite memories supplied as context.
- Response validation and Redis persistence before graph completion.

### Phase 2.5 — AI and safety tests

Files:

```text
backend/tests/unit/test_routing.py
backend/tests/safety/test_red_flags.py
backend/tests/integration/test_api.py
```

Deliverables:

- Tests for specialist selection.
- Tests for emergency bypass behavior.
- End-to-end profile-to-chat execution test.

### Phase 2 acceptance criteria

- Every message passes through the safety gate first.
- Emergency requests never continue to a normal care agent.
- All agents return the shared structured response.
- The system operates using safe fallbacks without an LLM key.
- Agent and safety regression tests pass.

---

## Phase 3 — React Frontend Layer

### Objective

Build the patient-facing React application over the stable APIs and expose chat, profile, appointment, memory, privacy, and emergency experiences.

### Phase 3.1 — React foundation

Files:

```text
frontend/package.json
frontend/vite.config.ts
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/components/layout/AppShell.tsx
frontend/src/styles/global.css
```

Deliverables:

- React, TypeScript, Vite, and browser routing.
- TanStack Query provider.
- Responsive application shell and navigation.
- Accessible global styling.

### Phase 3.2 — API and state clients

Files:

```text
frontend/src/api/client.ts
frontend/src/api/chat.ts
frontend/src/api/profiles.ts
frontend/src/api/appointments.ts
frontend/src/api/memory.ts
frontend/src/stores/chatStore.ts
frontend/src/types/index.ts
```

Deliverables:

- Typed HTTP client and error handling.
- API modules aligned with FastAPI contracts.
- Local conversation and selected-profile state.
- No raw health-chat persistence in browser local storage.

### Phase 3.3 — Profile and chat experience

Files:

```text
frontend/src/pages/ProfilesPage.tsx
frontend/src/pages/ChatPage.tsx
frontend/src/components/common/ProfileSelector.tsx
frontend/src/components/chat/MessageBubble.tsx
frontend/src/components/chat/EmergencyAlert.tsx
```

Deliverables:

- Adult, baby, child, and maternity profile creation.
- Unified chat interface for all agents.
- Visible agent category, urgency, next action, and disclaimer.
- Interruptive, accessible emergency presentation.

### Phase 3.4 — Appointment and memory experience

Files:

```text
frontend/src/pages/AppointmentsPage.tsx
frontend/src/pages/MemoryPage.tsx
frontend/src/pages/PrivacyPage.tsx
frontend/src/pages/DashboardPage.tsx
```

Deliverables:

- Availability search and slot selection.
- Explicit booking, rescheduling, and cancellation confirmation.
- Appointment status display from backend data.
- Saved-memory review and deletion.
- Clear explanation of memory and clinical limitations.

### Phase 3.5 — Node.js project workflow

Files:

```text
package.json
tools/setup.mjs
tools/dev.mjs
tools/test.mjs
```

Deliverables:

- `npm run setup` installs Python and frontend dependencies.
- `npm run dev` starts FastAPI and React together.
- `npm run dev:api` starts only FastAPI.
- `npm run dev:web` starts only React.
- `npm test` runs backend tests, frontend linting, and the production build.

### Phase 3 acceptance criteria

- Users can manage profiles and consent.
- Users can chat with all care categories from one screen.
- Emergency responses are visually prominent.
- Users can search, book, reschedule, and cancel appointments.
- Users can inspect and delete long-term memories.
- The frontend builds and passes linting.

---

## Cross-Phase Release Gate

The implementation is ready for a controlled pilot only after:

- SQLite migrations, backup, and restore behavior are validated.
- Local appointment collision and lifecycle tests pass.
- Authentication is connected to the deployment identity provider.
- Clinical experts approve prompts, red flags, and fallbacks.
- Security and privacy teams approve PHI handling, retention, and logging.
- `npm test` passes in CI.
