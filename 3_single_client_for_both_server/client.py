



'''
AsyncExitStack :
    is a context manager helper in Python that makes it easy to manage multiple asynchronous resources (like connections, sessions, or streams) and ensure they are cleanly closed when done, even if an error occurs.


Example :
    Think of AsyncExitStack like a stack of plates. 
    Every time you open a server session, 
    you put a “plate” on the stack. 
    When you’re done, the stack automatically clears all plates in reverse order, 
    so nothing is left dirty.

'''





from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
import asyncio
from typing import Dict

exit_stack = AsyncExitStack()

# Fixed keys
session_dict = {
    "sse_session": None,
    "stdio_session": None
}

# Cache tools to avoid repeated list_tools calls
tools_cache = {
    "sse": [],
    "stdio": []
}

SSE_SERVER_URL = "http://localhost:8001/sse"
STDIO_COMMANDS = "python"
STDIO_SCRIPTS = "stdio_server.py"


async def initialize_servers():
    global session_dict, tools_cache, exit_stack

    try:
        # Keep sessions alive in ExitStack
        await exit_stack.__aenter__()

        # 1️ - SSE server
        sse_transport = await exit_stack.enter_async_context(sse_client(SSE_SERVER_URL))
        read_sse, write_sse = sse_transport
        sse_session = await exit_stack.enter_async_context(ClientSession(read_sse, write_sse))
        await sse_session.initialize()
        session_dict["sse_session"] = sse_session

        # Cache SSE tools
        sse_tools = await sse_session.list_tools()
        tools_cache["sse"] = [tool.name for tool in sse_tools.tools]

        # 2️ - StdIO server
        stdio_params = StdioServerParameters(command=STDIO_COMMANDS, args=[STDIO_SCRIPTS])
        stdio_transport = await exit_stack.enter_async_context(stdio_client(stdio_params))
        read_stdio, write_stdio = stdio_transport
        stdio_session = await exit_stack.enter_async_context(ClientSession(read_stdio, write_stdio))
        await stdio_session.initialize()
        session_dict["stdio_session"] = stdio_session

        # Cache StdIO tools
        stdio_tools = await stdio_session.list_tools()
        tools_cache["stdio"] = [tool.name for tool in stdio_tools.tools]

        print(" SSE and StdIO servers initialized successfully!")
        print(f"SSE tools: {tools_cache['sse']}")
        print(f"StdIO tools: {tools_cache['stdio']}")

    except Exception as e:
        print(f"Error initializing servers: {e}")


async def call_tool(tool_name: str, arguments: Dict = {}):
    """
    Call a tool from either SSE or StdIO server depending on availability.
    """
    sse_session = session_dict.get("sse_session")
    stdio_session = session_dict.get("stdio_session")

    # Check SSE tools first
    if sse_session and tool_name in tools_cache["sse"]:
        result = await sse_session.call_tool(tool_name, arguments)
        return result.content[0].text

    # Then check StdIO tools
    if stdio_session and tool_name in tools_cache["stdio"]:
        result = await stdio_session.call_tool(tool_name, arguments)
        return result.content[0].text

    return f"Tool '{tool_name}' not found in any server."


async def main():
    await initialize_servers()

    greet = await call_tool("greet_user", {"name": "Junaid"})
    print(f"greet_user: {greet}")

    squar = await call_tool("get_squar", {"number": 4})
    print(f"get_squar: {squar}")

    # Close all sessions at the end
    await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
