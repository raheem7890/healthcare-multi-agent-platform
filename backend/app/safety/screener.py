from app.safety.red_flags import RED_FLAGS


def detect_red_flags(message: str) -> list[str]:
    normalized = " ".join(message.lower().split())
    return [flag.name for flag in RED_FLAGS if any(phrase in normalized for phrase in flag.phrases)]

