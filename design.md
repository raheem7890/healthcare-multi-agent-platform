# System Design

## 1. Purpose

The platform provides one patient-facing application backed by four specialized capabilities: general care, baby care, maternity care, and appointment management. The design separates presentation, API/business logic, AI orchestration, and persistence so that each layer can be developed and tested independently.

The care agents provide education and navigation only. They do not diagnose, prescribe, or replace a licensed clinician.

## 2. Runtime Architecture

```text
React application (Node.js/Vite development runtime)
                         |
                         | HTTPS + JSON
                         v
FastAPI application (Python/Uvicorn runtime)
     |                   |                    |
     |                   |                    +-- Local appointment service
     |                   +-- LangGraph supervisor and care agents
     +-- Repositories and memory adapters
              |                         |
              +-- Redis                 +-- SQLite
                  short-term                durable data
```

Node.js is the project-level development runner and the React toolchain. FastAPI and LangGraph remain Python services. This preserves the requested FastAPI architecture without requiring Docker.

## 3. Layer Responsibilities

### Database layer

Owns persistent entities, queries, transactions, consent-aware memory, and session-memory adapters. It must not contain HTTP or React logic.

### FastAPI layer

Owns HTTP validation, authentication, authorization, error translation, and service invocation. Routes remain thin and delegate business behavior.

### AI layer

Owns safety screening, state orchestration, intent routing, prompts, care-agent execution, response validation, and conversational context.

### React layer

Owns browser navigation, forms, UI state, API calls, accessibility, emergency presentation, and explicit confirmation of booking mutations.

## 4. Component Connections

```text
ChatPage
  -> frontend/src/api/chat.ts
  -> POST /v1/chat
  -> routes_chat.py
  -> ChatService
  -> Redis + SQLite context
  -> LangGraph workflow
  -> Safety gate
  -> Specialist agent
  -> Response validator
  -> Redis persistence + SQLite audit
  -> ChatResponse
  -> MessageBubble / EmergencyAlert
```

```text
AppointmentsPage
  -> frontend/src/api/appointments.ts
  -> /v1/appointments endpoints
  -> ownership validation
  -> local AppointmentService
  -> SQLite appointment repository
  -> UI confirmation/status
```

## 5. LangGraph Design

The graph uses `HealthcareState` as a shared typed state. Nodes return state updates rather than mutating state directly.

```text
START
  -> load_context
  -> safety_gate
       -> emergency -----------+
       -> route_intent         |
            -> general_care    |
            -> baby_care       |
            -> maternity_care  |
            -> booking         |
                               v
                     validate_response
                               |
                     persist_session
                               |
                              END
```

Routing priority:

1. Emergency red flags override every other intent.
2. Explicit appointment intent routes to booking.
3. Maternity or baby context routes to the matching specialist.
4. Remaining health questions route to general care.

## 6. Data Design

### Relational entities

```text
User
  ├── PatientProfile
  │     ├── MemorySummary
  │     └── Appointment
  ├── Conversation
  └── AuditEvent
```

SQLite is the durable database for local and deployed single-instance environments. SQLAlchemy repositories keep persistence logic separate from the API and agent layers.

### Short-term memory

Redis key:

```text
healthcare:session:{user_id}:{session_id}:messages
```

The list is bounded and expires. When Redis is not configured, the local process uses an in-memory implementation.

### Long-term memory

Long-term memory is stored in SQLite only when the selected profile has enabled memory consent. Emergency and booking messages are excluded from automatic memory creation.

## 7. Booking and Model Design

The Booking Agent is a LangGraph node like the other three agents. It recognizes booking, cancellation, and rescheduling language and directs the user to the appointment workflow. `AppointmentService` generates weekday availability locally, prevents conflicting bookings, and persists confirmed changes in SQLite.

The model is wrapped by `LLMService`. Without `LLM_API_KEY`, the care agents return deterministic safe fallbacks.

## 8. Security Design

- Development authentication is permitted only when `DEV_AUTH_BYPASS=true`.
- Production uses signed JWT bearer tokens.
- Every profile, memory, and appointment operation verifies ownership.
- Raw health messages are not included in normal application audit payloads.
- Appointment mutations require explicit confirmation and local conflict checks.
- Secrets remain in environment variables or a deployment secret store.

## 9. Failure Behavior

- Missing LLM credentials: use agent fallback responses.
- Missing Redis: use in-process session memory.
- Appointment conflict: reject the mutation and ask the user to choose another slot.
- Invalid resource ownership: return `404` without disclosing another user's record.
- Unsafe agent output: replace it with clinician-directed guidance.
- Emergency red flag: bypass standard care-agent execution.

## 10. Development Runtime

The root Node.js scripts provide a container-free workflow:

```text
npm run setup     Install backend and frontend dependencies
npm run dev       Start FastAPI and React together
npm run dev:api   Start FastAPI only
npm run dev:web   Start React only
npm test          Run all available verification
```

The Node runner launches Uvicorn as a child process and Vite as a second child process, forwarding output and shutdown signals to both.
