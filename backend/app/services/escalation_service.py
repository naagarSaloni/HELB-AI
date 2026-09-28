from typing import Dict, Any

from app.tools.human_escalation import create_support_ticket
from app.database.database import SessionLocal
from app.database.repository import create_support_ticket as save_support_ticket


def escalate_to_human(
    question: str,
    reason: str,
) -> Dict[str, Any]:

    # Create the ticket using the existing escalation tool
    result = create_support_ticket(
        question=question,
        reason=reason,
    )

    ticket = result["ticket"]

    # Save the ticket in PostgreSQL
    db = SessionLocal()

    try:
        saved_ticket = save_support_ticket(
            db=db,
            ticket_id=ticket["ticket_id"],
            question=question,
            reason=reason,
        )

        return {
            "tool": "human_escalation",
            "ticket": {
                "ticket_id": saved_ticket.ticket_id,
                "status": saved_ticket.status,
                "question": saved_ticket.question,
                "reason": saved_ticket.reason,
                "created_at": saved_ticket.created_at.isoformat(),
                "message": (
                    "Your question requires human support. "
                    f"Your support ticket ID is "
                    f"{saved_ticket.ticket_id}."
                ),
            },
        }

    finally:
        db.close()