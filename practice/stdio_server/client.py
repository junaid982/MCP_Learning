

from mcp import ClientSession , StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


async def main():
    
    # Configure the server
    
    stdio_params = StdioServerParameters(
        command="python",
        args=['server.py']
    ) 
    
    # Connect to the server 
    async with stdio_client(stdio_params) as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            
            # Initialize the session 
            await session.initialize()
            
            print("Initialize the session ...")
            
            
            # Get all the tools
            all_tools = await session.list_tools()
            for tool in all_tools.tools:
                print(f"{tool.name} : {tool.description}")


            # Call tool : get_time
            
            get_time = await session.call_tool("get_time")
            print(f"Current Date Time is : { get_time.content[0].text }")
            



if __name__ == "__main__":
    asyncio.run(main())