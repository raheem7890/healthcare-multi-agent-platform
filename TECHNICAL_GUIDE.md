# Technical Guide

## 1. System Responsibilities

The React frontend is responsible for presentation, form validation, authenticated requests, and explicit user confirmation. It must not make clinical urgency decisions or contact booking providers directly.

The FastAPI backend is responsible for authentication, authorization, LangGraph orchestration, safety screening, agent invocation, memory persistence, local appointment scheduling, and audit events.

## 2. Service Boundaries

```text
frontend
  -> backend API only

backend
  -> Redis for temporary session context
  -> SQLite for durable application data
  -> LLM / retrieval provider for LangGraph agents
  -> Local appointment service for scheduling
```


## 3. LangGraph State and Nodes

Use one explicit state model for all graph nodes.

```python
class HealthcareState(TypedDict):
    request_id: str
    user_id: str
    session_id: str
    profile_id: str | None
    message: str
    profile: dict | None
    recent_messages: list[dict]
    long_term_memory: list[dict]
    intent: str | None
    urgency: str | None
    red_flags: list[str]
    agent_response: dict | None
    booking_draft: dict | None
```

Required graph nodes:

1. `load_context`: validates profile ownership; reads Redis history and relevant SQLite memory.
2. `safety_gate`: evaluates deterministic and model-assisted red flags.
3. `route_intent`: selects a specialist or booking workflow.
4. `general_care`, `baby_care`, `maternity_care`, or `booking_adapter`: produces a typed result.
5. `validate_response`: blocks unsafe or malformed clinical output.
6. `persist_session`: appends bounded context to Redis.
7. `audit_event`: records routing, booking mutations, and safety escalations.

Routing priority is always: emergency safety > booking intent > maternity/baby specialty > general care.

## 4. Agent Contract

All agents return the same validated model.

```python
class AgentResponse(BaseModel):
    response_text: str
    category: Literal['general_care', 'baby_care', 'maternity_care', 'booking', 'emergency']
    urgency: Literal['routine', 'soon', 'urgent', 'emergency']
    recommended_action: str
    follow_up_questions: list[str] = []
    appointment_handoff: bool = False
    disclaimer_required: bool = True
    citations: list[str] = []
```

Clinical prompts must require cautious language, prohibit diagnosis/prescribing, and instruct the agent to surface uncertainty. The response validator should reject content that claims certainty, invents health history, or provides prohibited prescribing instructions.

## 5. Safety Design

The safety gate is a backend requirement, not a prompt-only feature.

### Deterministic red flags

Maintain versioned rules for phrases and structured symptom patterns involving:

- Difficulty breathing, chest pain, severe allergic reactions, seizure, stroke symptoms, severe bleeding, loss of consciousness.
- Self-harm or suicidal intent.
- Pregnancy and postpartum emergencies.
- Infant/child symptoms requiring age-specific urgent evaluation.

### Emergency behavior

For an emergency result, the graph terminates normal routing and returns urgent directions to contact local emergency services or seek immediate emergency care. The event is audited. Do not continue normal diagnosis-style questioning.

## 6. Memory Model

### Redis: short-term memory

Redis contains only limited, expiring state:

```text
healthcare:session:{user_id}:{session_id}:messages   TTL 24h
healthcare:session:{user_id}:{session_id}:context    TTL 24h
healthcare:session:{user_id}:{session_id}:booking    TTL 30m
```

Keep a bounded window, such as the last 12 messages plus a session summary. Do not use Redis as the permanent medical record.

### SQLite: long-term data

SQLite stores users, profiles, conversation metadata, approved summaries, appointments, and audits. Durable memory must be selective: persist consented summaries or preferences rather than every raw message.

Essential tables:

```text
users
patient_profiles
consents
conversations
conversation_messages
memory_summaries
appointments
audit_events
```

Every profile, memory, conversation, and appointment query must include `user_id` authorization filtering.

## 7. Booking Integration

The Booking Agent is part of the LangGraph workflow. The local `AppointmentService` generates weekday slots, checks availability in SQLite, and performs confirmed create, reschedule, and cancellation operations.

Booking mutations require:

- A verified user and authorized profile.
- Explicit confirmation immediately before mutation.
- A server-generated idempotency key.
- SQLite persistence with a local booking reference.
- Conflict checks that prevent duplicate bookings.

## 8. API Contracts

### Chat

```http
POST /v1/chat
```

```json
{
  "session_id": "session-id",
  "profile_id": "profile-id",
  "message": "I need an appointment with a pediatrician."
}
```

The response includes a request ID, selected agent category, urgency, text, follow-up questions, and optional booking handoff details.

### Appointments

```text
GET    /v1/appointments
POST   /v1/appointments/slots/search
POST   /v1/appointments
PATCH  /v1/appointments/{appointment_id}
DELETE /v1/appointments/{appointment_id}
```

### Profiles and Memory

```text
GET/POST             /v1/profiles
PATCH/DELETE         /v1/profiles/{profile_id}
GET/DELETE           /v1/memory/{memory_id}
```

## 9. React Design

### Required pages

```text
/login
/chat
/appointments
/profiles
/memory
/privacy
```

### State ownership

- TanStack Query manages data fetched from the backend: profiles, appointments, memories, slot results.
- A small Zustand store manages transient UI state: active session ID, selected profile, composer state.
- The backend remains the source of truth for appointment status, authorization, urgency, and memory.

### UX requirements

- Clearly label the responding care category.
- Render emergency responses in an interruptive, accessible alert component.
- Require a confirmation screen before booking changes.
- Do not persist raw health chat in browser local storage by default.
- Support keyboard navigation, focus management, and readable error states.

## 10. Security and Operations

- Use TLS in every deployed environment.
- Prefer HTTP-only, secure, same-site cookies for browser authentication; otherwise handle bearer tokens only in memory.
- Encrypt sensitive data at rest and in transit.
- Redact health content from application logs and error-monitoring payloads.
- Record audit events for record access, profile changes, bookings, consent changes, safety escalations, and agent routing.
- Use timeouts and safe fallback messages for Redis and LLM failures, and maintain SQLite backup and restore procedures.
- Version prompts, safety rules, database migrations, and API contracts.

## 11. Test Strategy

| Test type | Focus |
|---|---|
| Unit | routers, safety rules, memory keying, mapping functions |
| Integration | Redis, SQLite repositories, and local appointment lifecycle |
| Safety evaluation | emergency, baby, maternity, and self-harm cases |
| End-to-end | sign-in, profile selection, chat routing, booking confirmation |
| Security | authorization isolation, secret handling, logging redaction |

Release only when emergency-routing, authorization-isolation, booking-idempotency, and audit-event tests are passing.
