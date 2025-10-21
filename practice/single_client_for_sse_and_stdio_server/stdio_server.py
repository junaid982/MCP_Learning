

from mcp.server.fastmcp import FastMCP
import time


mcp = FastMCP("STDIO_SERVER")


@mcp.tool()
async def get_time():
    """
    This tool is used to return the current date and time 
    """
    
    date_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return {"date_time" : date_time}

@mcp.tool()
async def greet_user(name : str) :
    """
    This tool is used to return the greeting as per the time 
    """
    
    current_time = int(time.strftime("%H"))
    
    if current_time >= 0 and current_time < 12:
        greet = f"Good Morning {name}"
        
    elif current_time >= 12 and current_time <= 16:
        greet = f"Good Afternoon {name}"
        
    else:
        greet = f"Good Evening {name}"
        
    return {"greeting" : greet}


if __name__ == "__main__":
    mcp.run(transport="stdio")