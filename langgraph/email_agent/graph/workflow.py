from langgraph.graph import StateGraph, START, END

from state.email_state import EmailState

from nodes.read_email import read_email
from nodes.classify_email import classify_email
from nodes.spam_handler import handle_spam
from nodes.draft_response import draft_response
from nodes.notify_user import notify_user

from routing.router import route_email


def build_graph():

    graph = StateGraph(EmailState)

    graph.add_node("read_email", read_email)
    graph.add_node("classify_email", classify_email)
    graph.add_node("handle_spam", handle_spam)
    graph.add_node("draft_response", draft_response)
    graph.add_node("notify", notify_user)

    graph.add_edge(START, "read_email")

    graph.add_edge("read_email", "classify_email")

    graph.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "spam": "handle_spam",
            "legit": "draft_response"
        }
    )

    graph.add_edge("handle_spam", END)

    graph.add_edge("draft_response", "notify")

    graph.add_edge("notify", END)

    return graph.compile()