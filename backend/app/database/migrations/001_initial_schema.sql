-- Reference SQLite schema. Local startup creates the same tables through SQLAlchemy.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    external_auth_id TEXT NOT NULL UNIQUE,
    display_name TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patient_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    profile_type TEXT NOT NULL,
    display_name TEXT NOT NULL,
    relationship_to_user TEXT,
    date_of_birth DATE,
    pregnancy_due_date DATE,
    medical_notes TEXT,
    memory_consent INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    session_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT
);

CREATE TABLE IF NOT EXISTS memory_summaries (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    profile_id TEXT REFERENCES patient_profiles(id),
    memory_type TEXT NOT NULL,
    summary_text TEXT NOT NULL,
    importance_score REAL NOT NULL DEFAULT 0.5,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    profile_id TEXT NOT NULL REFERENCES patient_profiles(id),
    provider_id TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'confirmed',
    booking_reference TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    user_id TEXT,
    event_type TEXT NOT NULL,
    agent_type TEXT,
    event_payload TEXT,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_profiles_user_id ON patient_profiles(user_id);
CREATE INDEX IF NOT EXISTS ix_memory_user_id ON memory_summaries(user_id);
CREATE INDEX IF NOT EXISTS ix_appointments_user_id ON appointments(user_id);
CREATE INDEX IF NOT EXISTS ix_audit_request_id ON audit_events(request_id);
