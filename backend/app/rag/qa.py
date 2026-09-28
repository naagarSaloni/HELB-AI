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
You are the HELB AI Support Agent.

HELB means the Higher Education Loans Board of Kenya.

Answer the user's question using ONLY the official HELB context provided below.

RESPONSE STYLE:
- Act like a professional customer-support chatbot.
- Be concise and direct.
- Usually keep the answer between 60 and 150 words.
- Do not repeat the user's question.
- Do not create Markdown tables unless a table is absolutely necessary.
- Prefer short paragraphs.
- Use numbered steps for procedures.
- Use bullet points for requirements.
- Use bold text only for important terms.
- Do not include raw URLs in your answer.
- Do not mention RAG, embeddings, vector databases, agents,
  retrieved documents, prompts, or internal systems.
- Do not add unnecessary background information.
- Answer exactly what the user asked.

GROUNDING RULES:
1. Use ONLY the information in the provided HELB context.
2. Never invent information.
3. Never guess missing requirements, fees, deadlines or procedures.
4. If the information is not available, say:

"I couldn't find enough information in the available official HELB information to answer that."

5. Do not provide information that is not supported by the context.

HELB CONTEXT:
{context}
""",
        ),
        ("human", "{question}"),
    ]
)


def format_documents(documents: List[Document]) -> str:
    formatted = []

    for index, document in enumerate(documents, start=1):
        source_name = document.metadata.get(
            "source_name",
            "Unknown source",
        )

        source_url = document.metadata.get(
            "source",
            "",
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


def ask_helb(question: str, k: int = 3):
    documents = retrieve_documents(query=question, k=k)

    if not documents:
        return {
            "answer": (
                "I couldn't find enough information in the available "
                "official HELB information to answer that."
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

    # --------------------------------------------------
    # REMOVE DUPLICATE SOURCES
    # --------------------------------------------------
    sources = []
    seen_urls = set()

    for document in documents:
        source_url = document.metadata.get("source", "")
        source_name = document.metadata.get(
            "source_name",
            "Unknown source"
        )

        # Skip duplicate URLs
        if source_url in seen_urls:
            continue

        seen_urls.add(source_url)

        sources.append(
            {
                "name": source_name,
                "url": source_url,
            }
        )

    return {
        "answer": response.content,
        "sources": sources,
    }