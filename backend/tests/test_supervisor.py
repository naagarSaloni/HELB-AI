import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.agents.supervisor import (
    classify_question,
)


def main():

    questions = [
        "How do I apply for a HELB loan?",
        "What documents are required for an undergraduate loan?",
        "How can I repay my HELB loan?",
        "Can I repay using M-PESA?",
        "What is HELB?",
        "What scholarships does HELB offer?",
    ]

    for question in questions:

        intent = classify_question(
            question
        )

        print()
        print("=" * 80)
        print("QUESTION:")
        print(question)

        print()
        print("SUPERVISOR INTENT:")
        print(intent)


if __name__ == "__main__":
    main()