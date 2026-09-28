# Product and Technical Requirements

## 1. Product Objective

Provide a secure multi-agent healthcare education and appointment application with general care, baby care, maternity care, and appointment-management capabilities through one React interface.

## 2. User Roles

### Authenticated user

Can manage personal or dependent profiles, ask care-navigation questions, manage appointments, control memory consent, and delete saved memories.

### Guardian

An authenticated user managing a baby or child profile. The system treats the adult account owner as responsible for the dependent profile.

### Platform operator

Configures identity, SQLite, optional Redis, and the LLM provider; monitors safety and audit events.

## 3. Functional Requirements

### FR-001 — Authentication

- The API shall authenticate every `/v1` request.
- Development bypass shall be disabled automatically for production configuration.
- The API shall validate JWT signature, subject, and configured issuer/audience.

### FR-002 — Profile management

- Users shall create adult, baby, child, and maternity profiles.
- Users shall update and delete only profiles they own.
- Maternity due date and health notes shall remain optional.
- Long-term-memory consent shall be explicit and revocable.

### FR-003 — Unified chat

- Users shall submit a message with a session ID and optional profile ID.
- The backend shall return agent category, urgency, response, recommended action, follow-up questions, and disclaimer.
- All specialist agents shall use the same response contract.

### FR-004 — Clinical safety

- Every message shall pass through emergency screening before specialist routing.
- Emergency results shall bypass normal care-agent responses.
- The system shall not claim a definitive diagnosis or prescribe treatment.
- Generated responses shall pass through a post-generation validator.

### FR-005 — Agent routing

- Appointment intent shall route to booking.
- Pregnancy and postpartum intent shall route to maternity care.
- Baby and child intent shall route to baby care.
- All remaining health questions shall route to general care.

### FR-006 — Short-term memory

- Recent messages shall be isolated by user ID and session ID.
- Redis history shall be bounded and expire automatically.
- Local development shall work without Redis using in-process memory.

### FR-007 — Long-term memory

- Durable memory shall require profile consent.
- Users shall view and delete stored memories.
- Retrieval shall be limited to the authenticated user and relevant profile.
- Emergency and booking requests shall not be stored as automatic long-term memories.

### FR-008 — Appointment search

- Users shall select a profile, specialty, and date range.
- The backend shall generate weekday appointment slots from local scheduling rules.
- Confirmed or occupied slots shall not be returned as available.

### FR-009 — Appointment mutations

- Users shall create, reschedule, and cancel appointments.
- Every mutation shall require explicit confirmation.
- The service shall prevent duplicate bookings for the same provider and time.
- SQLite shall store the local booking reference and latest status.

### FR-010 — Auditability

- The platform shall audit chat routing and appointment mutations.
- Audit payloads shall avoid raw health-message content.
- Every audit event shall include a request ID and user ID when available.

### FR-011 — React application

- The application shall provide dashboard, chat, appointments, profiles, memory, and privacy pages.
- Emergency results shall use an accessible `role="alert"` presentation.
- Raw chat shall not be stored in browser local storage by default.
- The application shall work at desktop and mobile widths.

### FR-012 — Node.js development workflow

- `npm run setup` shall prepare Python and React dependencies.
- `npm run dev` shall run FastAPI and React concurrently.
- Developers shall be able to run either service independently.
- The project shall not require Docker for local development.

## 4. Non-Functional Requirements

### NFR-001 — Security

- Production communication shall use TLS.
- Secrets shall not be committed to source control.
- Authorization shall be enforced at the backend, never only in React.
- Sensitive health data shall be excluded from normal logs.

### NFR-002 — Privacy

- The system shall minimize stored health information.
- Consent and deletion behavior shall be auditable.
- Retention periods shall be configurable for deployed environments.

### NFR-003 — Reliability

- Local booking operations shall complete transactionally.
- Booking retries shall not create duplicate appointments.
- Appointment conflicts shall produce clear, recoverable errors.

### NFR-004 — Maintainability

- API routes, services, repositories, and external adapters shall remain separate.
- Frontend API calls shall remain separate from page components.
- Shared request and response structures shall be typed.

### NFR-005 — Accessibility

- Interactive controls shall be keyboard accessible.
- Forms shall use associated labels.
- Dynamic chat results shall use appropriate live regions.
- Meaning shall not be communicated by color alone.

### NFR-006 — Performance

- Redis session history shall remain bounded.
- Database queries shall use user/profile indexes.
- Frontend server data shall use controlled caching and invalidation.

### NFR-007 — Testability

- Routing, safety, repositories, APIs, and booking adapters shall be independently testable.
- CI shall run backend tests, frontend linting, and frontend production build.

## 5. External Dependencies

- Python 3.11 or later.
- Node.js 20 or later.
- SQLite for durable storage.
- Redis for deployed short-term memory.
- Configured LLM provider for generated care responses.
- Organizational identity provider or JWT issuer.

## 6. Constraints

- The project uses Python for FastAPI and LangGraph; Node.js cannot directly replace the FastAPI runtime.
- The Node.js root runner replaces the need for Docker during local development.
- Clinical output remains informational until reviewed and approved by qualified clinical stakeholders.
- SQLite deployment is intended for a single API instance; horizontal scaling requires a future database migration.

## 7. MVP Acceptance Criteria

- A user can create and select a care profile.
- The same chat page reaches all four capabilities.
- Red-flag input returns emergency guidance.
- Session context is maintained across multiple messages.
- Consented long-term memory can be listed and deleted.
- Appointment slots can be searched and explicitly booked.
- Appointments can be rescheduled and cancelled.
- Cross-user profile, memory, and appointment access is rejected.
- `npm run dev` starts the API and web application without Docker.
- `npm test` succeeds in the development and CI environments.

## 8. Production Exit Criteria

- Clinical safety review completed.
- Privacy and regulatory review completed for the deployment jurisdiction.
- Security penetration and dependency reviews completed.
- SQLite backup, restore, permissions, and migration procedures validated.
- Redis TLS and retention verified.
- Local booking collision and lifecycle integration tests pass.
- Identity provider integration tests pass.
- Monitoring, alerting, backup, and incident procedures are operational.
