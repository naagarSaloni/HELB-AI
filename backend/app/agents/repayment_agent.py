from typing import Dict, Any

from app.tools.repayment_information import (
    get_repayment_information,
)


def run_repayment_agent(
    question: str,
) -> Dict[str, Any]:

    result = get_repayment_information(
        question
    )

    return {
        "agent": "repayment_agent",
        "answer": result["answer"],
        "sources": result["sources"],
    }