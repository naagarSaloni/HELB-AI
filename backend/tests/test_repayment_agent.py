import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.agents.repayment_agent import (
    run_repayment_agent,
)


def main():

    questions = [
        "How do I repay my HELB loan?",
        "Can I repay my HELB loan using M-PESA?",
        "How can I check my HELB loan statement?",
    ]

    for question in questions:

        print()
        print("=" * 80)

        print("QUESTION:")
        print(question)

        print("=" * 80)

        result = run_repayment_agent(
            question
        )

        print()
        print("AGENT:")
        print(
            result["agent"]
        )

        print()
        print("ANSWER:")
        print(
            result["answer"]
        )

        print()
        print("SOURCES:")

        for source in result["sources"]:

            print(
                f"- {source['name']} | "
                f"{source['url']}"
            )


if __name__ == "__main__":
    main()