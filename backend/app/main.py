from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

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


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "HELB AI Support Agent API is running."
    }