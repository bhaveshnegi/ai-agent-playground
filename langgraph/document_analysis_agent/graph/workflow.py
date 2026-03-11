from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from state.agent_state import AgentState
from nodes.assistant import assistant
from tools.vision_tool import extract_text
from tools.math_tool import divide


tools = [extract_text, divide]


def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")

    builder.add_conditional_edges(
        "assistant",
        tools_condition
    )

    builder.add_edge("tools", "assistant")

    return builder.compile()