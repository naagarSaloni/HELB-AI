from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.graph.workflow import workflow


def main():
    questions = [
        "How do I apply for a HELB loan?",
        "Can I repay my HELB loan using M-PESA?",
        "What scholarships does HELB offer?",
        "I lost my HELB card and need to know the exact procedure for replacing it.",
    ]

    for question in questions:
        print()
        print("=" * 100)
        print("QUESTION:")
        print(question)

        result = workflow.invoke({"question": question})

        print()
        print("INTENT:")
        print(result.get("intent"))

        print()
        print("AGENT:")
        print(result.get("agent"))

        print()
        print("EVIDENCE SUPPORTED:")
        print(result.get("evidence_supported"))

        print()
        print("ESCALATE:")
        print(result.get("escalate"))

        print()
        print("GUARDRAIL:")
        print(result.get("guardrail_reason"))

        print()
        print("ANSWER:")
        print(result.get("answer"))

        print()
        print("TICKET ID:")
        print(result.get("ticket_id"))

        print()
        print("TICKET STATUS:")
        print(result.get("ticket_status"))

        print()
        print("SOURCES:")

        for source in result.get("sources", []):
            print(
                "-",
                source.get("name"),
                "|",
                source.get("url"),
            )


if __name__ == "__main__":
    main()