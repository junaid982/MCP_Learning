


from mcp.server.fastmcp import FastMCP
import math
import random
import time

mcp = FastMCP(
    name = "SSE_SERVER",
    host = "0.0.0.0",
    port = 8001,
    stateless_http = True # Expose 
)



@mcp.tool()
async def greet_user(name : str):
    """
    This tool is used to greet the user as per the time
    """
    current_time = int(time.strftime("%H"))
    
    if current_time >= 0 and current_time < 12:
        great = f"Good Morning {name}"
    
    elif current_time >= 12 and current_time < 16:
        great = f"Good Afternoon {name}"
        
    else:
        great = f"Good Evening {name}"
    
    return {"message" : great }



@mcp.tool()
async def get_squar(number : float):
    """
    This tool is used to calculate the squar of the given number
    """
    
    return {"squar" : number**2 }


@mcp.tool()
async def get_sqrt(number : float):
    """
    This tool is used to calculate the squar root of the given number 
    """
    
    return {"squar_root" : math.sqrt(number) }



@mcp.tool()
async def random_number(min_val : int = 0 , max_val : int = 100):
    """
    This tool is used to generate the random number between 0 to 100
    """
    
    ran = random.randint(min_val , max_val) 
    return {"random_number" : ran}


if __name__ == "__main__":
    
    mcp.run(transport="sse")
    
    
    