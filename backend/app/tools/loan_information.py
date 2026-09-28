
from app.rag.qa import ask_helb


def get_loan_information(question: str):
    result = ask_helb(
        question=question,
        k=3,
    )

    return {
        "tool": "loan_information",
        "answer": result["answer"],
        "sources": result["sources"],
    }

