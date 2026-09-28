from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import (
    User,
    Conversation,
    Message,
    SupportTicket,
    Feedback,
    AuditLog,
)


def create_user(
    db: Session,
    email: str,
    name: Optional[str] = None,
) -> User:
    user = User(
        email=email,
        name=name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email: str,
) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_conversation(
    db: Session,
    user_id: Optional[int] = None,
    title: Optional[str] = None,
) -> Conversation:
    conversation = Conversation(
        user_id=user_id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
    agent: Optional[str] = None,
    intent: Optional[str] = None,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        agent=agent,
        intent=intent,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def create_support_ticket(
    db: Session,
    ticket_id: str,
    question: str,
    reason: str,
    user_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
) -> SupportTicket:
    ticket = SupportTicket(
        ticket_id=ticket_id,
        question=question,
        reason=reason,
        user_id=user_id,
        conversation_id=conversation_id,
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def create_feedback(
    db: Session,
    rating: int,
    message_id: Optional[int] = None,
    comment: Optional[str] = None,
) -> Feedback:
    feedback = Feedback(
        message_id=message_id,
        rating=rating,
        comment=comment,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


def create_audit_log(
    db: Session,
    action: str,
    details: Optional[str] = None,
    user_id: Optional[int] = None,
    success: bool = True,
) -> AuditLog:
    log = AuditLog(
        action=action,
        details=details,
        user_id=user_id,
        success=success,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log