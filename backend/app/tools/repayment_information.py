from typing import Dict, Any

from app.rag.qa import ask_helb


def get_repayment_information(
    question: str,
) -> Dict[str, Any]:
    """
    Get HELB loan repayment information
    from the official HELB knowledge base.
    """

    result = ask_helb(
        question=question,
        k=5,
    )

    return {
        "tool": "repayment_information",
        "answer": result["answer"],
        "sources": result["sources"],
    }