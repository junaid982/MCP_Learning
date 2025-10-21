

from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
from dotenv import load_dotenv
import os
import json 
from openai import AsyncOpenAI

load_dotenv(".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# model = "gpt-4o-mini"
model = "gpt-4o"


openai_client = AsyncOpenAI(api_key = OPENAI_API_KEY )


SSE_SERVER_URL = "http://localhost:8001/sse"



async def get_tools(session):
    
    tools_result = await session.list_tools()
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools_result.tools
    ]
        


async def main(query : str ):

    # Connect to the SSE Server 
    async with sse_client(SSE_SERVER_URL) as (sse_read , sse_write):

        async with ClientSession(sse_read , sse_write) as session:
            
            # Initialize the session 
            await session.initialize()
            
            # Get all the tools as per openai structure 
            tools = await get_tools(session)
            
            # Initial OpenAI API call
            response = await openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": query}],
                tools=tools,
                tool_choice="auto",
            )
            
            # Get assistant's response
            assistant_message = response.choices[0].message
            # print(f"assistant_message : {assistant_message}")

            # Initialize conversation with user query and assistant response
            messages = [
                {"role": "user", "content": query},
                assistant_message,
            ]
            
            # print(f"messages : {messages}")
            # Handle tool calls if present
            if assistant_message.tool_calls:
                # Process each tool call
                for tool_call in assistant_message.tool_calls:
                    # Execute tool call
                    result = await session.call_tool(
                        tool_call.function.name,
                        arguments=json.loads(tool_call.function.arguments),
                    )
                    
                    # Add tool response to conversation
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result.content[0].text,
                        }
                    )
                    
                
                # Get final response from OpenAI with tool results
                final_response = await openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="none",  # Don't allow more tool calls
                )

                final_response = final_response.choices[0].message.content
                
                print(f"final_response : {final_response}")
                
            else:
                # No tool calls, just return the direct response
                assistant_message = assistant_message.content
                print(f"assistant_message : {assistant_message}")
            


if __name__ == "__main__":
    
    query = "calculate the squar of 12"
    
    asyncio.run(main(query)) 


