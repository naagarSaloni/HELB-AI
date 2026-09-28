from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.graph.workflow import workflow
from app.database.database import SessionLocal
from app.database.repository import (
    create_conversation,
    create_message,
)


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    question: str
    conversation_id: int
    user_message_id: int
    assistant_message_id: int
    intent: str | None = None
    agent: str | None = None
    answer: str
    sources: list
    evidence_supported: bool
    escalate: bool
    ticket_id: str | None = None
    ticket_status: str | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    db = SessionLocal()

    try:
        # --------------------------------------------------
        # 1. Create conversation if this is a new chat
        # --------------------------------------------------
        conversation_id = request.conversation_id

        if conversation_id is None:
            conversation = create_conversation(
                db=db,
                title=question[:100],
            )
            conversation_id = conversation.id

        # --------------------------------------------------
        # 2. Save user message
        # --------------------------------------------------
        user_message = create_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        # --------------------------------------------------
        # 3. Run LangGraph
        # --------------------------------------------------
        result = workflow.invoke(
            {
                "question": question,
            }
        )

        # --------------------------------------------------
        # 4. Save assistant message
        # --------------------------------------------------
        assistant_message = create_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=result.get("answer", ""),
            agent=result.get("agent"),
            intent=result.get("intent"),
        )

        # --------------------------------------------------
        # 5. Return complete API response
        # --------------------------------------------------
        return ChatResponse(
            question=question,
            conversation_id=conversation_id,
            user_message_id=user_message.id,
            assistant_message_id=assistant_message.id,
            intent=result.get("intent"),
            agent=result.get("agent"),
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            evidence_supported=result.get(
                "evidence_supported",
                False,
            ),
            escalate=result.get(
                "escalate",
                False,
            ),
            ticket_id=result.get("ticket_id"),
            ticket_status=result.get("ticket_status"),
        )

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(error)}",
        )

    finally:
        db.close()