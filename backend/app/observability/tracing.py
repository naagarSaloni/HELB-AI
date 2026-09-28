import os

from app.config import settings


def is_langfuse_enabled() -> bool:
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    return bool(public_key and secret_key)


def get_langfuse_handler():
    if not is_langfuse_enabled():
        return None

    try:
        from langfuse import get_client
        from langfuse.langchain import CallbackHandler

        get_client()

        handler = CallbackHandler()

        return handler

    except Exception as error:
        print(f"Warning: Langfuse initialization failed: {error}")
        return None


def get_trace_config(conversation_id=None, user_id=None):
    config = {
        "metadata": {
            "application": settings.APP_NAME,
            "environment": settings.ENVIRONMENT,
        }
    }

    if conversation_id is not None:
        config["metadata"]["langfuse_session_id"] = str(conversation_id)

    if user_id is not None:
        config["metadata"]["langfuse_user_id"] = str(user_id)

    handler = get_langfuse_handler()

    if handler is not None:
        config["callbacks"] = [handler]

    return config