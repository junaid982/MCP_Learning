



# activate enviroment 
# C:\Users\opo119738\Desktop\mcp_learning\env-mcp-server\Scripts\activate

# 
# cd C:\Users\opo119738\Desktop\mcp_learning\mcp_leaning\practice\sse_server

# server.py


from mcp.server.fastmcp import FastMCP
import random


mcp = FastMCP(
    name="SSE_Server",
    host="0.0.0.0",
    port=8001,
    stateless_http=True # Expose Rst Endpoints at /rest/tools/<tool_name>
)




@mcp.tool()
async def random_number(min_val : str = 0 , max_val : str = 100) :
    
    """
    This tool is used to generate random number default between 0 to 100
    """
    
    ran = random.randint(min_val , max_val)
    
    return {"random" : ran}

@mcp.tool()
async def greet_user(name : str):
    """
    This tool is used to greet user 
    """
    
    return {"message" : f"Hello {name}"}


if __name__ == "__main__":
    mcp.run(transport="sse")


