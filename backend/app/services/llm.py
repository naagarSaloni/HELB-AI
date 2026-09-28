
from langchain_groq import ChatGroq

from app.config import settings


def get_llm():
    if settings.LLM_PROVIDER != "groq":
        raise ValueError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
        )

    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured in the .env file."
        )

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=settings.GROQ_API_KEY,
    )

