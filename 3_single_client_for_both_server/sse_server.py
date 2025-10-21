



from mcp.server.fastmcp import FastMCP
import random
import time

sse_server = FastMCP(
    name="Simple_SSE_Server",
    host="0.0.0.0",
    port=8001,
    stateless_http=True # Expose Rest endpoints at /rest/tool/<tool_name>
)


# Example Tool 1 : Generate a random Number
@sse_server.tool()
async def generate_random_number(min_val : int = 0 , max_val : int = 100) :
    
    """
    This tool is used to generate a random numbers from default between 0 to 100
    """
    
    ran = random.randint(min_val , max_val)
    return {"number" : ran }


# Example Tool 2 : Greet a user
@sse_server.tool()
async def greet_user(name : str):
    
    """
    This Tool is used to greet a user according to the time 
    """

    current_time = int(time.strftime("%H"))

    if 0 <= current_time < 12:
        greet = "Good Morning"
    elif 12 <= current_time < 16:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"
        
    return {"message" : f"{greet} {name}"}



if __name__ == "__main__":
    print("Starting SSE server on http://localhost:8001")
    
    
    sse_server.run(transport="sse")
    