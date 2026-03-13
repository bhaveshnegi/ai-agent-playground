from llama_index.retrievers.bm25 import BM25Retriever
from langchain_core.tools import Tool
from loadData import docs

bm25_retriever = BM25Retriever.from_defaults(nodes=docs)

def get_guest_info_retriever(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = bm25_retriever.retrieve(query)
    if results:
        return "\n\n".join([doc.text for doc in results[:3]])
    else:
        return "No matching guest information found."

def get_conversation_started_tool(query: str) -> str:
    """Retrieves detailed information about gala guests to start conversation."""
    results = bm25_retriever.retrieve(query)
    if results:
        return "\n\n".join([doc.text for doc in results[:3]])
    else:
        return "No matching guest information found."
    
def get_total_guest(query: str) -> str:
    """Retrieves the total number of guests attending the gala."""
    results = bm25_retriever.retrieve(query)
    if results:
        return "\n\n".join([doc.text for doc in results[:3]])
    else:
        return "No matching guest information found."

# Initialize the tool
guest_info_tool = Tool(
    name="guest_info_retriever",
    func=get_guest_info_retriever,
    description="Retrieves detailed information about gala guests based on their name or relation."
)

conversation_started_tool = Tool(
    name="conversation_started_tool",
    func=get_conversation_started_tool,
    description="Retrieves detailed information about gala guests to start conversation."
)

get_guest_total_tool = Tool(
    name="get_guest_total_tool",
    func=get_total_guest,
    description="Retrieves the total number of guests attending the gala."
)
