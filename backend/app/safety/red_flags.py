from dataclasses import dataclass


@dataclass(frozen=True)
class RedFlag:
    name: str
    phrases: tuple[str, ...]


RED_FLAGS = (
    RedFlag("breathing_emergency", ("can't breathe", "cannot breathe", "difficulty breathing", "choking")),
    RedFlag("cardiac_emergency", ("chest pain", "crushing chest", "heart attack")),
    RedFlag("neurological_emergency", ("face drooping", "slurred speech", "seizure", "unconscious")),
    RedFlag("severe_bleeding", ("severe bleeding", "bleeding won't stop", "heavy bleeding")),
    RedFlag("self_harm", ("kill myself", "suicide", "hurt myself", "end my life")),
    RedFlag(
        "maternity_emergency",
        (
            "reduced fetal movement",
            "baby not moving",
            "pregnant and bleeding",
            "postpartum heavy bleeding",
            "severe headache pregnant",
        ),
    ),
    RedFlag(
        "pediatric_emergency",
        ("baby is blue", "baby not breathing", "infant seizure", "baby is unresponsive"),
    ),
)

