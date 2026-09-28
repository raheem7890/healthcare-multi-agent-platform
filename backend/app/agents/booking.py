from app.schemas.chat import AgentResponse


class BookingAgent:
    async def run(self, message: str) -> AgentResponse:
        normalized = message.lower()
        if "cancel" in normalized:
            response_text = (
                "I can help cancel an appointment. Open Appointments, find the confirmed appointment, "
                "and choose Cancel. The application will ask you to confirm before changing it."
            )
            recommended_action = "Open Appointments and choose the appointment to cancel."
        elif "reschedule" in normalized or "change" in normalized:
            response_text = (
                "I can help reschedule an appointment. Open Appointments, choose Reschedule, select the "
                "new date and time, and confirm the change."
            )
            recommended_action = "Open Appointments and choose Reschedule."
        else:
            response_text = (
                "I can help you book an appointment using the local scheduling system. Open Appointments "
                "to choose the patient profile, specialty, date range, and an available slot."
            )
            recommended_action = "Search available appointment slots."
        return AgentResponse(
            response_text=response_text,
            category="booking",
            urgency="routine",
            recommended_action=recommended_action,
            follow_up_questions=["Which specialty do you need?", "What dates work for you?"],
            appointment_handoff=True,
            disclaimer_required=False,
        )
