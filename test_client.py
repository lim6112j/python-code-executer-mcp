import asyncio
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_server():
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print("--- Available Tools ---")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
                
            print("\n--- Testing Code Execution ---")
            
            # Simple code
            code1 = 'print("Hello from Python MCP Server!")\n' + \
                    'x = 5\n' + \
                    'y = 10\n' + \
                    'print(f"Result: {x + y}")'
            
            print(f"Executing:\n{code1}")
            result = await session.call_tool("execute_python_code", {"code": code1})
            # FastMCP returns output as a list of content blocks
            # We can print the text of the first block
            print(f"\nOutput:\n{result.content[0].text}")
            
            # Code with error
            code2 = 'print("Starting...")\n' + \
                    'raise ValueError("Intentionally throwing an error")'
                    
            print(f"\n--- Testing Code Error ---\nExecuting:\n{code2}")
            result2 = await session.call_tool("execute_python_code", {"code": code2})
            print(f"\nOutput:\n{result2.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())
