from typing import TypedDict, Optional, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    # optional document path
    input_file: Optional[str]

    # conversation history
    messages: Annotated[list[AnyMessage], add_messages]