

# This  is same client but with AsyncExitStack


from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
import json
import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI


# Load env
load_dotenv(".env")

# get the Openai from .env and initialize openai object
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = AsyncOpenAI(api_key = OPENAI_API_KEY)
model = "gpt-4o"

# Create AsyncExitStack object 
exit_stack = AsyncExitStack()


# SSE Server Url 
SSE_SERVER_URL = "http://localhost:8001/sse"


# Session State Object 
session_dict = {
    "sse_session" : None
}


# Initialize the server connection 
async def initialize_server():
    global session_dict
    
    server_protocol = await exit_stack.enter_async_context(sse_client(SSE_SERVER_URL))
    
    read_sse , write_sse = server_protocol
    
    sse_session = await exit_stack.enter_async_context(ClientSession(read_sse , write_sse))
    
    await sse_session.initialize()
    
    # Store session object into the session dict 
    session_dict['sse_session'] = sse_session
    
    print(f"Initialize server...")




async def get_sse_tools():
    global session_dict
    
    tools = []
    
    sse_session = session_dict.get('sse_session')
    
    all_tools = await sse_session.list_tools()

    for tool in all_tools.tools:
        
        tools.append({
            "type" : "function",
            "function" : {
                "name" : tool.name,
                "description" : tool.description,
                "parameters" : tool.inputSchema
            }
        })
        
    return tools



async def handle_user_query(query):
    
    global session_dict
    
    # get all the tools from the server   
    tools = await get_sse_tools()

    # print(f"tools : {tools}")
    
    # Initialize Openai call 
    
    response = await openai_client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : query}],
        tools = tools,
        tool_choice = "auto"
    )
    
    assistant_message = response.choices[0].message
    
    # print(f"assistant_message : {assistant_message}")
    
    message = [
        {"role" : "user" , "content" : query},
        assistant_message
    ]
    
    if assistant_message.tool_calls:
        
        for tool_call in assistant_message.tool_calls:
            # print(f"tool_call : {tool_call}\n")
            
            tool_name = tool_call.function.name
            tool_argument = json.loads(tool_call.function.arguments)
            
            # tool Call 
            tool_result = await session_dict['sse_session'].call_tool(tool_name , arguments = tool_argument)
            tool_result = tool_result.content[0].text
            
            
            # add these to message 
            message.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : tool_result
            })
            
            # print(f"tool_result : {tool_result}")

        final_response = await openai_client.chat.completions.create(
            model=model,
            messages=message,
            tools=tools,
            tool_choice="none"
        )
        # print(f"final_response : {final_response}")
        
        final_response = final_response.choices[0].message.content
        
        return final_response
    
    
    return assistant_message.content





async def main(query):
    
    # Initialize the server connection 
    await initialize_server()
    
    response =  await handle_user_query(query)
    
    print(f"\nResponse : {response}")
    
    
    # Cleanup 
    await exit_stack.aclose()
    
    





if __name__ == "__main__":
    
    query = "hello my name is junadi can you please calculate squar of 12 and also squar root of this number"
    
    asyncio.run(main(query))


