from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict, total=False):
    question: str

    # Supervisor
    intent: str

    # Agent response
    agent: str
    answer: str
    sources: List[Dict[str, Any]]

    # Guardrail
    evidence_supported: bool
    guardrail_reason: str

    # Escalation
    escalate: bool
    ticket_id: str
    ticket_status: str