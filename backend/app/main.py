from fastapi import FastAPI
from app.api.conversation import router as conversations_router

from app.config import settings
from app.api.health import router as health_router
from app.api.chat import router as chat_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    chat_router,
    prefix="/api",
)
app.include_router(
    conversations_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "HELB AI Support Agent API is running."
    }