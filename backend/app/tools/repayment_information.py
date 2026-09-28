
from app.rag.qa import ask_helb


def get_repayment_information(question: str):
    result = ask_helb(
        question=question,
        k=3,
    )

    return {
        "tool": "repayment_information",
        "answer": result["answer"],
        "sources": result["sources"],
    }

