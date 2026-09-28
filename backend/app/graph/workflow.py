from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.graph.nodes import (
    supervisor_node,
    loan_node,
    repayment_node,
    knowledge_node,
    guardrail_node,
    escalation_node,
    route_after_supervisor,
    route_after_guardrail,
)


def build_workflow():

    graph = StateGraph(AgentState)

    # -----------------------------
    # Nodes
    # -----------------------------

    graph.add_node(
        "supervisor",
        supervisor_node,
    )

    graph.add_node(
        "loan_agent",
        loan_node,
    )

    graph.add_node(
        "repayment_agent",
        repayment_node,
    )

    graph.add_node(
        "knowledge_agent",
        knowledge_node,
    )

    graph.add_node(
        "guardrail",
        guardrail_node,
    )

    graph.add_node(
        "escalation",
        escalation_node,
    )

    # -----------------------------
    # Entry
    # -----------------------------

    graph.set_entry_point("supervisor")

    # -----------------------------
    # Supervisor routing
    # -----------------------------

    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "loan": "loan_agent",
            "repayment": "repayment_agent",
            "knowledge": "knowledge_agent",
        },
    )

    # -----------------------------
    # Agents -> Guardrail
    # -----------------------------

    graph.add_edge(
        "loan_agent",
        "guardrail",
    )

    graph.add_edge(
        "repayment_agent",
        "guardrail",
    )

    graph.add_edge(
        "knowledge_agent",
        "guardrail",
    )

    # -----------------------------
    # Guardrail routing
    # -----------------------------

    graph.add_conditional_edges(
        "guardrail",
        route_after_guardrail,
        {
            "answer": END,
            "escalate": "escalation",
        },
    )

    # -----------------------------
    # Escalation -> End
    # -----------------------------

    graph.add_edge(
        "escalation",
        END,
    )

    return graph.compile()


workflow = build_workflow()