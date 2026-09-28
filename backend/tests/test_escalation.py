from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.escalation_service import escalate_to_human


def main():

    result = escalate_to_human(
        question="I have a problem with my HELB account.",
        reason="The available documents do not contain enough information.",
    )

    print("=" * 80)
    print("HUMAN ESCALATION TEST")
    print("=" * 80)

    print()
    print("TOOL:")
    print(result.get("tool"))

    print()
    print("TICKET:")

    ticket = result.get("ticket", {})

    print("Ticket ID:", ticket.get("ticket_id"))
    print("Status:", ticket.get("status"))
    print("Question:", ticket.get("question"))
    print("Reason:", ticket.get("reason"))
    print("Message:", ticket.get("message"))
    print("Created:", ticket.get("created_at"))


if __name__ == "__main__":
    main()