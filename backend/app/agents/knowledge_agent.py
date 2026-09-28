
from app.rag.qa import ask_helb


def run_knowledge_agent(question: str) -> dict:
    result = ask_helb(
        question=question,
        k=3,
    )

    return {
        "agent": "knowledge_agent",
        "answer": result["answer"],
        "sources": result["sources"],
    }

