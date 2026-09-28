from app.agents.router import route_intent


def test_routes_booking_before_specialty() -> None:
    assert route_intent("Book a pediatric appointment", "baby") == "booking"


def test_routes_from_profile_type() -> None:
    assert route_intent("I need help", "maternity") == "maternity_care"
    assert route_intent("I need help", "baby") == "baby_care"
    assert route_intent("I need help", "adult") == "general_care"

