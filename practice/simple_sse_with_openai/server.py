


from mcp.server.fastmcp import FastMCP
import random
import time 



mcp = FastMCP(
    name="SIMPLE_SSE_SERVER",
    host="0.0.0.0",
    port=8001,
    stateless_http=True
)


@mcp.tool()
async def user_greeting(name : str):
    """
    This Tool is use to greet the user  
    """
    
    return {"greet" : f"Hello Good Morning {name}"}


@mcp.tool()
async def squar(number : int):
    """
    This tool is used to calculate the squar of the given number 
    """
    
    return {"number" : number**2 }


if __name__ == "__main__":
    
    mcp.run(transport="sse")