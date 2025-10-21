


from mcp.server.fastmcp import FastMCP
import time
import math


mcp = FastMCP("Utility_server")



@mcp.tool()
async def get_squar(number : float):
    """
    This tool is used to return the squar of the number 
    """
    
    return {"squar" : number**2}


@mcp.tool()
async def get_sqrt(number : float):
    """
    This tool is used to return the squar root of the given number
    """
    
    return {"squar_root" : math.sqrt(number)}


@mcp.tool()
async def get_time():
    """
    This tool is used to return the current date and time 
    """
    
    date_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    return {"date_time" : date_time}


if __name__ == "__main__":
    mcp.run(transport="stdio")