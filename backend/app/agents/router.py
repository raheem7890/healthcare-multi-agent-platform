def route_intent(message: str, profile_type: str | None) -> str:
    text = message.lower()
    if any(word in text for word in ("appointment", "book", "reschedule", "cancel", "availability")):
        return "booking"
    if profile_type in {"maternity"} or any(
        word in text for word in ("pregnant", "pregnancy", "postpartum", "fetal", "trimester")
    ):
        return "maternity_care"
    if profile_type in {"baby", "child"} or any(
        word in text for word in ("baby", "infant", "newborn", "toddler", "child", "pediatric")
    ):
        return "baby_care"
    return "general_care"
