

from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
import os
import json

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = AsyncOpenAI(api_key = OPENAI_API_KEY)
model = "gpt-4o"

SSE_SERVER_URL = "http://localhost:8001/sse"



async def get_mcp_tools(session):
    
    tools = []
    
    all_tools = await session.list_tools()

    for mcp_tool in all_tools.tools:
        
        
        tools.append( {
            "type" : "function",
            "function" : {
                "name" : mcp_tool.name,
                "description" : mcp_tool.description,
                "parameters" : mcp_tool.inputSchema
            }
        })
        return tools


async def handle_user_message(query ,session):
    # Get all the tools from the server 
    tools = await get_mcp_tools( session )
    
    print()
    print(f"tools : {tools}")
    print()
    
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role" : "user" , "content" : query} ],
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_response = response.choices[0].message
    print(f"assistant_response : {assistant_response}")
    
    messages = [
        {"role" : "user" , "content" : query},
        assistant_response
    ]
    
    
    if assistant_response.tool_calls:
        for tool in assistant_response.tool_calls:
            print(tool)
            print()
            
            tool_name = tool.function.name
            tool_arguments = json.loads(tool.function.arguments) or {}
            
            # Call tool
            
            tool_result = await session.call_tool(tool_name , arguments = tool_arguments)
            
            tool_result = tool_result.content[0].text
            print(f"tool_result : {tool_result}")
            
            messages.append({
                "role" : "tool",
                "tool_call_id" : tool.id,
                "content" :  tool_result
            })
            
            
            final_response = await openai_client.chat.completions.create(
                model=model,
                messages=[{"role" : "user" , "content" : query} ],
                tools=tools,
                tool_choice="none"
            )
            
            final_response = final_response.choices[0].message.content
            
            return final_response
            
            
            
    
    else:
        return assistant_response.content



async def main(query):
    
    async with sse_client(SSE_SERVER_URL) as (read_sse , write_sse):
        async with ClientSession(read_sse , write_sse) as session:
            
            await session.initialize()
            
            
            response = await handle_user_message(query ,session)
            
            print(f"response : {response}")
            



if __name__ == "__main__":
    
    query = "Greet the User Junaid"

    
    asyncio.run(main(query))