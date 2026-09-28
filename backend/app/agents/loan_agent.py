from typing import Dict, Any

from app.tools.loan_information import (
    get_loan_information,
)


def run_loan_agent(
    question: str,
) -> Dict[str, Any]:

    result = get_loan_information(
        question
    )

    return {
        "agent": "loan_agent",
        "answer": result["answer"],
        "sources": result["sources"],
    }