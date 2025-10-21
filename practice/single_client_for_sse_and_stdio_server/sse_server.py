


from mcp.server.fastmcp import FastMCP
import math
import random

mcp = FastMCP(
    name="SSE_SERVER" , 
    host="0.0.0.0",
    port=8001,
    stateless_http=True # Expose Rest endpoints at /rest/tools/<tool_name>
)


@mcp.tool()
async def get_squar(number : float):
    """
    This tool is used to return the squar of the given number
    """
    
    return {"squar" : number**2}

@mcp.tool()
async def get_sqrt(number : float):
    """
    This tool is used to return the squar root of the given number
    """
    
    return {"sqrt" : math.sqrt(number)}

@mcp.tool()
async def random_number(min_val : int = 0 , max_val : int = 100):
    """
    This tool is used to return the random number between 0 to 100
    """
    
    ran = random.randint(min_val , max_val)
    return {"random_number" : ran}


if __name__ == "__main__":
    mcp.run(transport="sse")