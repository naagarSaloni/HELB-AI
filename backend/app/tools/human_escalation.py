from typing import Dict, Any
from datetime import datetime, timezone
import uuid


def create_support_ticket(
    question: str,
    reason: str,
) -> Dict[str, Any]:
    """
    Create a human-support ticket when the AI
    cannot confidently answer a user's question.
    """

    ticket_id = f"HELB-{uuid.uuid4().hex[:8].upper()}"

    ticket = {
        "ticket_id": ticket_id,
        "status": "open",
        "question": question,
        "reason": reason,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "message": (
            "I couldn't find enough reliable information "
            "in the available official HELB information "
            "to answer your question. "
            f"Your support ticket ID is {ticket_id}. "
            "A human support representative can assist you further."
        ),
    }

    return {
        "tool": "human_escalation",
        "ticket": ticket,
    }