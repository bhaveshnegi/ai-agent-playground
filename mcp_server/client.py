import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():

    # define how to start the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    # start server + connect client
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # initialize session
            await session.initialize()

            # list available tools
            tools = await session.list_tools()
            print("Available tools:", tools)

            # call tool
            result = await session.call_tool(
                "get_weather",
                {"location": "Delhi"}
            )

            print("Tool result:", result)
            
            # read resource
            resource = await session.read_resource("weather://Delhi")
            print("Resource:", resource)

            # get prompt
            prompt = await session.get_prompt(
                "weather_report",
                {"location": "Paris"}
            )

            print("Prompt:", prompt)



asyncio.run(main())