from app.safety.screener import detect_red_flags


def test_detects_emergency_phrase() -> None:
    assert "breathing_emergency" in detect_red_flags("I cannot breathe")


def test_routine_message_has_no_red_flags() -> None:
    assert detect_red_flags("I have a mild headache") == []

