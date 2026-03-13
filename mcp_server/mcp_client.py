from langchain_mcp_adapters.client import MultiServerMCPClient

def get_mcp_client():
    return MultiServerMCPClient({
        "weather": {
            "transport": "stdio",
            "command": "python",
            "args": ["server.py"]
        },
        "search": {
            "transport": "stdio",
            "command": "python",
            "args": ["search_server.py"]
        }
    })