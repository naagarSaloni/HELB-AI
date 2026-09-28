import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.rag.qa import ask_helb


def main():
    questions = [
        "How do I apply for a HELB loan?",
        "What are the requirements for an undergraduate loan?",
        "How do I repay my HELB loan?",
    ]

    for question in questions:
        print("\n" + "=" * 80)
        print("QUESTION:")
        print(question)
        print("=" * 80)

        result = ask_helb(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"- {source['name']} | "
                f"{source['url']}"
            )


if __name__ == "__main__":
    main()