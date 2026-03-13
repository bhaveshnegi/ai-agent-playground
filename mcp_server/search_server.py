from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun


# Create an MCP server
mcp = FastMCP("Search Service")

# Tool implementation
@mcp.tool()
def search_tool(query: str) -> str:
    search_tool = DuckDuckGoSearchRun()
    return search_tool.run(query)

# Run the server
if __name__ == "__main__":
    mcp.run()