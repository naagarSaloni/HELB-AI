from app.graph.state import AgentState

from app.agents.supervisor import classify_question
from app.agents.loan_agent import run_loan_agent
from app.agents.repayment_agent import run_repayment_agent
from app.agents.knowledge_agent import run_knowledge_agent

from app.guardrails.validation import validate_evidence


# ============================================================
# SUPERVISOR
# ============================================================

def supervisor_node(state: AgentState) -> AgentState:

    question = state["question"]

    intent = classify_question(question)

    return {
        "intent": intent,
    }


# ============================================================
# LOAN AGENT
# ============================================================

def loan_node(state: AgentState) -> AgentState:

    question = state["question"]

    result = run_loan_agent(question)

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


# ============================================================
# REPAYMENT AGENT
# ============================================================

def repayment_node(state: AgentState) -> AgentState:

    question = state["question"]

    result = run_repayment_agent(question)

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


# ============================================================
# KNOWLEDGE AGENT
# ============================================================

def knowledge_node(state: AgentState) -> AgentState:

    question = state["question"]

    result = run_knowledge_agent(question)

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


# ============================================================
# DIRECT HUMAN SUPPORT
# ============================================================

def support_node(state: AgentState) -> AgentState:

    """
    This node is ONLY for cases where the user explicitly
    asks for human support.

    Example:
        "I want to talk to human support."

    In this situation, ticket creation is immediate.
    """

    from app.services.escalation_service import escalate_to_human

    result = escalate_to_human(
        question=state["question"],
        reason="User explicitly requested human support.",
    )

    ticket = result["ticket"]

    answer = (
        "Your request has been escalated to human support.\n\n"
        f"**Ticket ID:** {ticket['ticket_id']}\n\n"
        "A human support representative can assist you further."
    )

    return {
        "agent": "human_support",
        "answer": answer,
        "sources": [],
        "evidence_supported": False,
        "escalate": True,
        "escalation_pending": False,
        "ticket_id": ticket["ticket_id"],
        "ticket_status": ticket["status"],
        "guardrail_reason": (
            "User explicitly requested human support."
        ),
    }


# ============================================================
# EVIDENCE / GUARDRAIL
# ============================================================

def guardrail_node(state: AgentState) -> AgentState:

    result = validate_evidence(
        answer=state.get("answer", ""),
        sources=state.get("sources", []),
    )

    # --------------------------------------------------------
    # NO RELIABLE EVIDENCE
    # --------------------------------------------------------

    if not result["supported"]:

        confirmation_message = (
            "I couldn't find enough reliable information "
            "in the available official HELB information "
            "to answer that question.\n\n"
            "Would you like me to connect you with human support?"
        )

        return {
            "answer": confirmation_message,
            "sources": [],
            "evidence_supported": False,
            "escalate": False,
            "escalation_pending": True,
            "guardrail_reason": result["reason"],
        }

    # --------------------------------------------------------
    # RELIABLE EVIDENCE FOUND
    # --------------------------------------------------------

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "evidence_supported": True,
        "escalate": False,
        "escalation_pending": False,
        "guardrail_reason": result["reason"],
    }


# ============================================================
# ROUTING AFTER SUPERVISOR
# ============================================================

def route_after_supervisor(state: AgentState) -> str:

    return state["intent"]


# ============================================================
# ROUTING AFTER GUARDRAIL
# ============================================================

def route_after_guardrail(state: AgentState) -> str:

    if state.get("evidence_supported", False):
        return "answer"

    # IMPORTANT:
    # Do NOT route to an escalation node.
    #
    # The API will return the confirmation question.
    # The user's next message decides whether a ticket
    # should actually be created.

    return "confirm"