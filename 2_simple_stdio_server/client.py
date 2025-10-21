

from mcp import ClientSession , StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


async def main():
    
    # configure the server 
    stdio_params = StdioServerParameters(
        command="python",
        args=['server.py']
    )
    
    # Connect the server 
    async with stdio_client(stdio_params) as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            
            # initialize the session
            await session.initialize()
    
            print(f"initialize the session...")
            
            
            # get all the tool List
            all_tools = await session.list_tools()
            for tool in all_tools.tools:
                print(f"{tool.name} : {tool.description}")
             

            # Call tool 1 : get_squar
            squar = await session.call_tool("get_squar" , arguments={"number" : 4}) 
            print(f"squar : {squar.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())