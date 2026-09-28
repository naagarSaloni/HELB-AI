from app.tools.human_escalation import create_support_ticket
from app.database.database import SessionLocal
from app.database.repository import create_support_ticket as save_support_ticket


def escalate_to_human(
    question: str,
    reason: str,
):
    """
    Escalate a question to human support and
    persist the support ticket in PostgreSQL.
    """

    # 1. Create the ticket using the escalation tool
    result = create_support_ticket(
        question=question,
        reason=reason,
    )

    ticket = result["ticket"]

    # 2. Save the ticket in PostgreSQL
    db = SessionLocal()

    try:
        saved_ticket = save_support_ticket(
            db=db,
            ticket_id=ticket["ticket_id"],
            question=question,
            reason=reason,
        )

        # 3. Return the database-backed ticket
        return {
            "tool": "human_escalation",
            "ticket": {
                "ticket_id": saved_ticket.ticket_id,
                "status": saved_ticket.status,
                "question": saved_ticket.question,
                "reason": saved_ticket.reason,
                "created_at": saved_ticket.created_at.isoformat(),
                "message": ticket["message"],
            },
        }

    finally:
        db.close()