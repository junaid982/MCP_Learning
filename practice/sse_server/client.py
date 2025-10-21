
# activate enviroment 
# C:\Users\opo119738\Desktop\mcp_learning\env-mcp-server\Scripts\activate

# 
# cd C:\Users\opo119738\Desktop\mcp_learning\mcp_leaning\practice\sse_server

# client.py

from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio


SSE_SERVER_URL = "http://localhost:8001/sse"



async def main():
    async with sse_client(SSE_SERVER_URL) as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            
            # initialize the session
            await session.initialize()
            print("session Initialized..")

            # Get all available tools 
            all_tools = await session.list_tools()
            
            for tool in all_tools.tools:
                print(f"{tool.name} : {tool.description}")
            
            
            # call tool 1
            random_number = await session.call_tool("random_number")
            print(f"Tool Name : random_number")
            print(f"random_number : {random_number.content[0].text}")
            print()
            
            # call tool 2
            greet = await session.call_tool("greet_user" , arguments={"name" : "Junaid"})
            print(f"greet : {greet.content[0].text}")
            

if __name__ == "__main__":
    
    asyncio.run(main()) 