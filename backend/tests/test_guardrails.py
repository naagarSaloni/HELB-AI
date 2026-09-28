from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.guardrails.validation import validate_evidence


def main():

    print("=" * 80)
    print("TEST 1: Valid HELB sources")
    print("=" * 80)

    result = validate_evidence(
        answer="HELB provides undergraduate loans.",
        sources=[
            {
                "name": "Undergraduate Loans",
                "url": "https://www.helb.co.ke/helb-products/helb-loans/undergraduate-loans/",
            },
            {
                "name": "Undergraduate Loans",
                "url": "https://www.helb.co.ke/helb-products/helb-loans/undergraduate-loans/",
            },
        ],
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 2: No sources")
    print("=" * 80)

    result = validate_evidence(
        answer="Some unsupported answer.",
        sources=[],
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 3: Non-HELB source")
    print("=" * 80)

    result = validate_evidence(
        answer="Some answer.",
        sources=[
            {
                "name": "Random Website",
                "url": "https://example.com",
            }
        ],
    )

    print(result)


if __name__ == "__main__":
    main()