import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_server_sse():
    # Connect to the SSE stream at /sse endpoint provided by FastMCP
    url = "http://127.0.0.1:8000/sse"
    print(f"Connecting to {url}...")
    
    # We must ensure the server is already running in another terminal
    # python3 server.py
    
    try:
        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # List tools
                tools = await session.list_tools()
                print("--- Available Tools ---")
                for tool in tools.tools:
                    print(f"- {tool.name}: {tool.description}")
                    
                print("\n--- Testing Code Execution ---")
                
                # Simple code
                code1 = 'print("Hello from Python MCP Server over SSE!")\n' + \
                        'x = 5\n' + \
                        'y = 10\n' + \
                        'print(f"Result: {x + y}")'
                
                print(f"Executing:\n{code1}")
                result = await session.call_tool("execute_python_code", {"code": code1})
                print(f"\nOutput:\n{result.content[0].text}")
    except Exception as e:
        print(f"Failed to connect or test: {e}\nIs the server running on {url}?")

if __name__ == "__main__":
    asyncio.run(test_server_sse())
