


# server.py


from mcp.server.fastmcp import FastMCP
import time


mcp = FastMCP("SIMPLE_STDIO_SERVER")


@mcp.tool()
async def get_time():
    """
    This tool is used to get the current date and time 
    """
    
    date_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return {"date_time" : date_time}


if __name__ == "__main__":
    mcp.run(transport="stdio")