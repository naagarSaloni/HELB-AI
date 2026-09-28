from typing import Dict, Any
from datetime import datetime
import uuid


def create_support_ticket(
    question: str,
    reason: str,
) -> Dict[str, Any]:
    """
    Create a support ticket when the AI cannot
    confidently answer a user's question.
    """

    ticket_id = f"HELB-{uuid.uuid4().hex[:8].upper()}"

    ticket = {
        "ticket_id": ticket_id,
        "status": "open",
        "question": question,
        "reason": reason,
        "created_at": datetime.utcnow().isoformat(),
        "message": (
            "Your question requires human support. "
            f"Your support ticket ID is {ticket_id}."
        ),
    }

    return {
        "tool": "human_escalation",
        "ticket": ticket,
    }