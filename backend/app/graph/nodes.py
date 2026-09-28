from app.graph.state import AgentState

from app.agents.supervisor import classify_question
from app.agents.loan_agent import run_loan_agent
from app.agents.repayment_agent import run_repayment_agent
from app.agents.knowledge_agent import run_knowledge_agent

from app.guardrails.validation import validate_evidence
from app.services.escalation_service import escalate_to_human


def supervisor_node(state: AgentState) -> AgentState:
    question = state["question"]

    intent = classify_question(question)

    return {
        "intent": intent
    }


def loan_node(state: AgentState) -> AgentState:
    result = run_loan_agent(state["question"])

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


def repayment_node(state: AgentState) -> AgentState:
    result = run_repayment_agent(state["question"])

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


def knowledge_node(state: AgentState) -> AgentState:
    result = run_knowledge_agent(state["question"])

    return {
        "agent": result["agent"],
        "answer": result["answer"],
        "sources": result["sources"],
    }


def guardrail_node(state: AgentState) -> AgentState:
    result = validate_evidence(
        answer=state.get("answer", ""),
        sources=state.get("sources", []),
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "evidence_supported": result["supported"],
        "guardrail_reason": result["reason"],
        "escalate": not result["supported"],
    }


def escalation_node(state: AgentState) -> AgentState:
    """
    Create a human support ticket when evidence
    is not sufficient.
    """

    result = escalate_to_human(
        question=state["question"],
        reason=state.get(
            "guardrail_reason",
            "Insufficient evidence",
        ),
    )

    ticket = result["ticket"]

    return {
        "escalate": True,
        "ticket_id": ticket["ticket_id"],
        "ticket_status": ticket["status"],
        "answer": ticket["message"],
    }


def route_after_supervisor(state: AgentState) -> str:
    return state["intent"]


def route_after_guardrail(state: AgentState) -> str:
    if state.get("evidence_supported", False):
        return "answer"

    return "escalate"