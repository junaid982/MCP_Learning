

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

SSE_SERVER_URL = "http://localhost:8001/sse"



async def main():
   async with sse_client(SSE_SERVER_URL) as (read_stream , write_stream):
       async with ClientSession(read_stream , write_stream) as session:
           
        # Initialize Session
        
        await session.initialize()
        print("Initialize Session...")
        
        # List All Tools 
        list_tools = await session.list_tools()
        
        print("*"*10 , " All Available Tools " , "*"*10 , "\n")
        for tool in list_tools.tools:
            print(f"{tool.name} : {tool.description}")
            
            
        # Tool Call 1
        result = await session.call_tool("greet_user" , arguments={"name" : "Junaid"})    
        print(f"result : {result.content[0].text}")
            
        
        result = await session.call_tool("generate_random_number" )
        print(f"Random Number : {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
