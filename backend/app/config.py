import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "HELB AI Support Agent"
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    LLM_PROVIDER = os.getenv(
        "LLM_PROVIDER",
        "groq"
    )

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    CHROMA_PERSIST_DIRECTORY = os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        "./data/chroma"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        ""
    )


settings = Settings()