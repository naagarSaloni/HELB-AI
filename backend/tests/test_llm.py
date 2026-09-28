import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.services.llm import get_llm


def main():
    llm = get_llm()

    response = llm.invoke(
        "Explain what HELB is in one short sentence."
    )

    print("\nLLM RESPONSE:")
    print(response.content)


if __name__ == "__main__":
    main()