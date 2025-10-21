

from contextlib import AsyncExitStack

from mcp import ClientSession , StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
import asyncio
from typing import Dict


# Global Variables 

session_dict = {
    "sse_session" : None,
    "stdio_session" : None
}

tools_dict = {
    "sse_tools" : [],
    "stdio_tools" : []
}

exit_stack = AsyncExitStack()


# SSE 
SSE_SERVER_URL = "http://localhost:8001/sse"


# STDIO 
STDIO_COMMAND = "python"
STDIO_SCRIPT = "stdio_server.py"



async def initialize_server():
    
    global session_dict , tools_dict
    
    # 1 - Connecting to the SSE Server 
    
    sse_transport = await exit_stack.enter_async_context(sse_client(SSE_SERVER_URL))
    read_sse , write_sse = sse_transport
    
    sse_session = await exit_stack.enter_async_context(ClientSession(read_sse , write_sse))
    
    # Initialize SSE Server 
    await sse_session.initialize()
    
    
    # Store SSE Session Object into dict 
    session_dict['sse_session'] = sse_session
     
    print("Initialize SSE Server")  
    
    
    # Get SSE Tools 
    sse_tools = []
    
    all_tools = await sse_session.list_tools()
    for tool in all_tools.tools:
        sse_tools.append(
            tool.name
        )
        
    # Store all sse tools into a global tools_dict
    tools_dict['sse_tools'] = sse_tools
    
    
    
    
    # 2 - Connecting to the STDIO Server 
    
    stdio_params = StdioServerParameters(
        command = STDIO_COMMAND,
        args = [STDIO_SCRIPT]
    )  
    
    stdio_transport = await exit_stack.enter_async_context(stdio_client(stdio_params))
    readd_stdio , write_stdio = stdio_transport
    
    stdio_session = await exit_stack.enter_async_context(ClientSession(readd_stdio , write_stdio))
    
    # Initialize STDIO Server
    await stdio_session.initialize()
    
    # Store SSE Session Object into dict 
    session_dict['stdio_session'] = stdio_session

    print("Initialize STDIO Server")  
    
    
    # Get STDIO Tools 
    stdio_tools = []
    
    all_tools = await stdio_session.list_tools()
    for tool in all_tools.tools:
        stdio_tools.append(
            tool.name
        )
        
    # Store all stdio tools into a global tools_dict
    tools_dict['stdio_tools'] = stdio_tools
        
    
    
    
async def call_tool(tool_name : str , arguments : Dict = {}):
    
    global session_dict , tools_dict
    
    # get the session from the session_dict 
    sse_session =  session_dict.get("sse_session")
    stdio_session =  session_dict.get("stdio_session")
    
    
    # Get all the tools from cache
    sse_tools =  tools_dict.get("sse_tools")
    stdio_tools =  tools_dict.get("stdio_tools")

    
    if sse_session and tool_name in sse_tools:
        result = await sse_session.call_tool( tool_name , arguments = arguments )
        return result.content[0].text
    
    
    if stdio_session and tool_name in stdio_tools:
        result = await stdio_session.call_tool( tool_name , arguments = arguments )
        return result.content[0].text
    
    return f"{tool_name} not in sse server or stdio server"
    
    

async def main():
    
    await initialize_server()


    # CAll tool 
    
    greet = await call_tool("greet_user" , arguments = {"name" : "Junaid"})
    print(f"greet : {greet}")
    
    
    squar = await call_tool("get_squar" , arguments = {"number" : 4})
    print(f"squar : {squar}")
    
    get_sqrt = await call_tool("get_sqrt" , arguments = {"number" : 144})
    print(f"get_sqrt : {get_sqrt}")
    
    
    
    # Cleanup 
    await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
    