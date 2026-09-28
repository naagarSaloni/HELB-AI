from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.database.repository import create_conversation, create_message
from app.graph.workflow import workflow
from app.observability.tracing import get_trace_config
from app.services.escalation_service import escalate_to_human


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    sources: list = []
    agent: Optional[str] = None
    intent: Optional[str] = None
    evidence_supported: bool = True
    escalate: bool = False
    escalation_pending: bool = False
    ticket_id: Optional[str] = None
    ticket_status: Optional[str] = None


# ============================================================
# GREETINGS
# ============================================================

GREETING_RESPONSES = {
    "hi",
    "hello",
    "hey",
    "hii",
    "hiii",
    "good morning",
    "good afternoon",
    "good evening",
}


# ============================================================
# YES RESPONSES
# ============================================================

YES_RESPONSES = {
    "yes",
    "yeah",
    "yep",
    "yup",
    "sure",
    "okay",
    "ok",
    "please",
    "yes please",
    "sure please",
    "connect me",
    "connect me to support",
    "connect me with support",
    "talk to support",
    "human support",
    "i want human support",
    "i need human support",
    "talk to a human",
    "speak to a human",
    "speak to someone",
    "talk to someone",
}


# ============================================================
# NO RESPONSES
# ============================================================

NO_RESPONSES = {
    "no",
    "nope",
    "nah",
    "not now",
    "no thanks",
    "no thank you",
    "don't",
    "do not",
    "not needed",
    "i'm fine",
    "im fine",
}


# ============================================================
# HELPERS
# ============================================================

def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def is_greeting(text: str) -> bool:
    return normalize_text(text) in GREETING_RESPONSES


def is_yes_response(text: str) -> bool:
    return normalize_text(text) in YES_RESPONSES


def is_no_response(text: str) -> bool:
    return normalize_text(text) in NO_RESPONSES


def previous_message_was_support_confirmation(
    db,
    conversation_id: int,
) -> bool:
    from app.database.models import Message

    previous_assistant_message = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id,
            Message.role == "assistant",
        )
        .order_by(Message.created_at.desc())
        .first()
    )

    if not previous_assistant_message:
        return False

    answer = normalize_text(previous_assistant_message.content)

    confirmation_phrases = [
        "would you like me to connect you with human support",
        "would you like me to connect you with human support?",
        "connect you with human support",
    ]

    return any(
        phrase in answer
        for phrase in confirmation_phrases
    )


# ============================================================
# CHAT ENDPOINT
# ============================================================

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()

    # --------------------------------------------------------
    # EMPTY QUESTION
    # --------------------------------------------------------

    if not question:
        return ChatResponse(
            conversation_id=request.conversation_id or 0,
            answer="Please enter a question.",
            sources=[],
            agent="chatbot",
            intent="invalid",
            evidence_supported=False,
            escalate=False,
            escalation_pending=False,
        )

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # CREATE OR REUSE CONVERSATION
        # ----------------------------------------------------

        conversation_id = request.conversation_id

        if conversation_id is None:
            conversation = create_conversation(
                db=db,
                title=question[:80],
            )

            conversation_id = conversation.id

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        create_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        normalized_question = normalize_text(question)

        # ====================================================
        # GREETING
        # ====================================================

        if is_greeting(normalized_question):

            greeting = (
                "Hello! I'm the HELB AI Support Agent. "
                "How can I help you today?"
            )

            create_message(
                db=db,
                conversation_id=conversation_id,
                role="assistant",
                content=greeting,
                agent="chatbot",
                intent="greeting",
            )

            return ChatResponse(
                conversation_id=conversation_id,
                answer=greeting,
                sources=[],
                agent="chatbot",
                intent="greeting",
                evidence_supported=True,
                escalate=False,
                escalation_pending=False,
            )

        # ====================================================
        # CHECK IF WE ARE WAITING FOR SUPPORT CONFIRMATION
        # ====================================================

        waiting_for_confirmation = (
            previous_message_was_support_confirmation(
                db=db,
                conversation_id=conversation_id,
            )
        )

        # ====================================================
        # USER CONFIRMED HUMAN SUPPORT
        # ====================================================

        if waiting_for_confirmation and is_yes_response(question):

            from app.database.models import Message

            previous_user_message = (
                db.query(Message)
                .filter(
                    Message.conversation_id == conversation_id,
                    Message.role == "user",
                )
                .order_by(Message.created_at.desc())
                .offset(1)
                .first()
            )

            original_question = (
                previous_user_message.content
                if previous_user_message
                else question
            )

            result = escalate_to_human(
                question=original_question,
                reason=(
                    "User confirmed that they want to be "
                    "connected with human support."
                ),
            )

            ticket = result["ticket"]

            answer = (
                "Your request has been escalated to human support.\n\n"
                f"**Ticket ID:** {ticket['ticket_id']}\n\n"
                "A human support representative can assist you further."
            )

            create_message(
                db=db,
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                agent="human_support",
                intent="support",
            )

            return ChatResponse(
                conversation_id=conversation_id,
                answer=answer,
                sources=[],
                agent="human_support",
                intent="support",
                evidence_supported=False,
                escalate=True,
                escalation_pending=False,
                ticket_id=ticket["ticket_id"],
                ticket_status=ticket["status"],
            )

        # ====================================================
        # USER DECLINED HUMAN SUPPORT
        # ====================================================

        if waiting_for_confirmation and is_no_response(question):

            answer = (
                "Okay. I won't create a support ticket. "
                "If you need help later, just let me know."
            )

            create_message(
                db=db,
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                agent="chatbot",
                intent="support_confirmation",
            )

            return ChatResponse(
                conversation_id=conversation_id,
                answer=answer,
                sources=[],
                agent="chatbot",
                intent="support_confirmation",
                evidence_supported=True,
                escalate=False,
                escalation_pending=False,
            )

        # ====================================================
        # LANGGRAPH WORKFLOW + LANGFUSE TRACING
        # ====================================================

        trace_config = get_trace_config(
            conversation_id=conversation_id,
        )

        result = workflow.invoke(
            {"question": question},
            config=trace_config,
        )

        # ----------------------------------------------------
        # GET WORKFLOW RESULT
        # ----------------------------------------------------

        answer = result.get(
            "answer",
            "I couldn't process your request.",
        )

        sources = result.get(
            "sources",
            [],
        )

        agent = result.get("agent")

        intent = result.get("intent")

        evidence_supported = result.get(
            "evidence_supported",
            False,
        )

        escalate = result.get(
            "escalate",
            False,
        )

        escalation_pending = result.get(
            "escalation_pending",
            False,
        )

        ticket_id = result.get(
            "ticket_id",
        )

        ticket_status = result.get(
            "ticket_status",
        )

        # ====================================================
        # SAVE ASSISTANT MESSAGE
        # ====================================================

        create_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            agent=agent,
            intent=intent,
        )

        # ====================================================
        # RETURN RESPONSE
        # ====================================================

        return ChatResponse(
            conversation_id=conversation_id,
            answer=answer,
            sources=sources,
            agent=agent,
            intent=intent,
            evidence_supported=evidence_supported,
            escalate=escalate,
            escalation_pending=escalation_pending,
            ticket_id=ticket_id,
            ticket_status=ticket_status,
        )

    finally:

        db.close()