from typing import Dict, Any

from app.rag.qa import ask_helb


def run_knowledge_agent(question: str) -> Dict[str, Any]:
    """
    Handle general HELB knowledge questions
    using the HELB RAG knowledge base.
    """

    result = ask_helb(
        question=question,
        k=5,
    )

    return {
        "agent": "knowledge_agent",
        "answer": result["answer"],
        "sources": result["sources"],
    }