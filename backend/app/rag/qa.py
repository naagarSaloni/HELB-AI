from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from app.rag.retriever import retrieve_documents
from app.services.llm import get_llm


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a HELB AI Support Agent.

HELB means the Higher Education Loans Board of Kenya.

Answer the user's question using ONLY the provided HELB context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the context does not contain enough information, say:
   "I could not find enough information in the available HELB
   documents to answer this question."
4. Give a clear and concise answer.
5. Preserve important details such as requirements, steps,
   fees, deadlines, URLs, and repayment methods when present.

HELB CONTEXT:
{context}
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


def format_documents(documents: List[Document]) -> str:
    formatted = []

    for index, document in enumerate(documents, start=1):
        source_name = document.metadata.get(
            "source_name",
            "Unknown source"
        )

        source_url = document.metadata.get(
            "source",
            ""
        )

        content = document.page_content

        formatted.append(
            f"""
SOURCE {index}
Name: {source_name}
URL: {source_url}

Content:
{content}
"""
        )

    return "\n".join(formatted)


def ask_helb(question: str, k: int = 5):
    documents = retrieve_documents(
        query=question,
        k=k
    )

    if not documents:
        return {
            "answer": (
                "I could not find enough information in the "
                "available HELB documents to answer this question."
            ),
            "sources": [],
        }

    context = format_documents(documents)

    prompt = PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    sources = []

    for document in documents:
        sources.append(
            {
                "name": document.metadata.get(
                    "source_name",
                    "Unknown source"
                ),
                "url": document.metadata.get(
                    "source",
                    ""
                ),
                "chunk": document.metadata.get(
                    "chunk_index"
                ),
            }
        )

    return {
        "answer": response.content,
        "sources": sources,
    }