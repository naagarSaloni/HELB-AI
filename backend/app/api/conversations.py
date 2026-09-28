from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.database.models import Conversation

router = APIRouter()


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: int):
    db = SessionLocal()

    try:
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found."
            )

        messages = sorted(
            conversation.messages,
            key=lambda message: message.created_at
        )

        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "messages": [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "agent": message.agent,
                    "intent": message.intent,
                    "created_at": message.created_at,
                }
                for message in messages
            ],
        }

    finally:
        db.close()