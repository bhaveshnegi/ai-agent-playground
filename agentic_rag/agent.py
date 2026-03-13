from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv
from retrival import guest_info_tool, conversation_started_tool, get_guest_total_tool
from hg_hug_tool import hub_stats_tool
from weathertool import weather_info_tool
from webtool import search_tool

load_dotenv()

# Generate the chat interface, including the tools
# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
#     huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
# )

endpoint = HuggingFaceEndpoint(
    # repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    repo_id="meta-llama/Meta-Llama-3.1-70B-Instruct",
    temperature=0.7,
    max_new_tokens=200,
    task="conversational"
)

# Wrap in chat interface
chat = ChatHuggingFace(llm=endpoint)
tools = [guest_info_tool, conversation_started_tool, get_guest_total_tool, hub_stats_tool, weather_info_tool, search_tool]
chat_with_tools = chat.bind_tools(tools)

# Generate the AgentState and Agent graph
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):
    return {
        "messages": [chat_with_tools.invoke(state["messages"])],
    }

## The graph
builder = StateGraph(AgentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message requires a tool, route to tools
    # Otherwise, provide a direct response
    tools_condition,
)
builder.add_edge("tools", "assistant")
alfred = builder.compile()

# messages = [HumanMessage(content="Tell me about our guest named 'Lady Ada Lovelace'.")]
messages = [HumanMessage(content="How can i start a conversation with lady ada lovelace?")]
# messages = [HumanMessage(content="Who is Facebook and what's their most popular model?")]
# messages = [HumanMessage(content="What is the weather like in New York?")]
# messages = [HumanMessage(content="Who is the current Prime Minister of India?")]
# messages = [HumanMessage(content="Give me total number of guest attening?")]
# messages = [HumanMessage(content="Tell me about our guest named 'Bhavesh Negi'.")]
# messages = [HumanMessage(content="whent the nikola tesla born and died?")]
response = alfred.invoke({"messages": messages})

print("Alfred's Response:")
print(response['messages'][-1].content)