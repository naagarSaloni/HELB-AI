from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.escalation_service import escalate_to_human
from app.database.database import SessionLocal
from app.database.models import SupportTicket


def main():

    question = "I lost my HELB card and need help replacing it."

    reason = (
        "The available official HELB documents do not "
        "contain enough information."
    )

    print("Creating support ticket...")

    result = escalate_to_human(
        question=question,
        reason=reason,
    )

    ticket = result["ticket"]

    print()
    print("Ticket created:")
    print("Ticket ID:", ticket["ticket_id"])
    print("Status:", ticket["status"])
    print("Question:", ticket["question"])

    db = SessionLocal()

    try:
        saved_ticket = (
            db.query(SupportTicket)
            .filter(
                SupportTicket.ticket_id == ticket["ticket_id"]
            )
            .first()
        )

        print()

        if saved_ticket:
            print("PostgreSQL verification: SUCCESS")
            print(
                "Saved ticket:",
                saved_ticket.ticket_id,
            )
        else:
            print("PostgreSQL verification: FAILED")

    finally:
        db.close()


if __name__ == "__main__":
    main()