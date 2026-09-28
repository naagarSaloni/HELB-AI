from typing import Any, Dict, List, TypedDict


class AgentState(TypedDict, total=False):
    question: str

    intent: str
    agent: str

    answer: str
    sources: List[Dict[str, Any]]

    evidence_supported: bool
    guardrail_reason: str

    escalate: bool
    escalation_pending: bool

    ticket_id: str
    ticket_status: str