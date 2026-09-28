from fastapi.testclient import TestClient

from app.main import app


def test_profile_chat_and_emergency_flow() -> None:
    with TestClient(app) as client:
        headers = {"X-User-ID": "integration-user"}
        profile_response = client.post(
            "/v1/profiles",
            headers=headers,
            json={
                "profile_type": "adult",
                "display_name": "Integration User",
                "memory_consent": False,
            },
        )
        assert profile_response.status_code == 201
        profile_id = profile_response.json()["id"]

        chat_response = client.post(
            "/v1/chat",
            headers=headers,
            json={
                "session_id": "session-integration-001",
                "profile_id": profile_id,
                "message": "I have a mild headache",
            },
        )
        assert chat_response.status_code == 200
        assert chat_response.json()["agent"] == "general_care"

        emergency_response = client.post(
            "/v1/chat",
            headers=headers,
            json={
                "session_id": "session-integration-001",
                "profile_id": profile_id,
                "message": "I cannot breathe",
            },
        )
        assert emergency_response.status_code == 200
        assert emergency_response.json()["urgency"] == "emergency"

