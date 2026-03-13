import asyncio
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

from mcp.client.stdio import StdioServerParameters
from mcp_client import get_mcp_client

load_dotenv()


async def main():
    # LLM
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3.1-70B-Instruct",
        temperature=0.7,
        max_new_tokens=200,
        task="conversational"
    )

    chat = ChatHuggingFace(llm=endpoint)

    client = get_mcp_client()
    
    # Load MCP tools
    tools = await client.get_tools()

    print([t.name for t in tools])

    chat_with_tools = chat.bind_tools(tools)

    # Agent State
    class AgentState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    async def assistant(state: AgentState):
        response = await chat_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}

    # Graph
    builder = StateGraph(AgentState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")

    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )

    builder.add_edge("tools", "assistant")

    alfred = builder.compile()

    messages = [
        HumanMessage(content="What is the capital of India?")
    ]

    response = await alfred.ainvoke({"messages": messages})

    print("Alfred's Response:")
    print(response["messages"][-1].content)


asyncio.run(main())