from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.graph.nodes import (
    supervisor_node,
    loan_node,
    repayment_node,
    knowledge_node,
    support_node,
    guardrail_node,
    route_after_supervisor,
    route_after_guardrail,
)


# ============================================================
# BUILD WORKFLOW
# ============================================================

def build_workflow():

    graph = StateGraph(AgentState)

    # --------------------------------------------------------
    # NODES
    # --------------------------------------------------------

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
        "support",
        support_node,
    )

    graph.add_node(
        "guardrail",
        guardrail_node,
    )

    # --------------------------------------------------------
    # ENTRY POINT
    # --------------------------------------------------------

    graph.set_entry_point("supervisor")

    # --------------------------------------------------------
    # SUPERVISOR → AGENT
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "loan": "loan_agent",
            "repayment": "repayment_agent",
            "knowledge": "knowledge_agent",
            "support": "support",
        },
    )

    # --------------------------------------------------------
    # AGENTS → GUARDRAIL
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # GUARDRAIL
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "guardrail",
        route_after_guardrail,
        {
            # Reliable answer
            "answer": END,

            # Unsupported question.
            #
            # IMPORTANT:
            # This does NOT create a ticket.
            # The API waits for the user's Yes/No response.
            "confirm": END,
        },
    )

    # --------------------------------------------------------
    # DIRECT HUMAN SUPPORT
    # --------------------------------------------------------

    graph.add_edge(
        "support",
        END,
    )

    # --------------------------------------------------------
    # COMPILE
    # --------------------------------------------------------

    return graph.compile()


# ============================================================
# GLOBAL WORKFLOW
# ============================================================

workflow = build_workflow()