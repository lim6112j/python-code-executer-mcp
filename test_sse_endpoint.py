import asyncio
from mcp.server.fastmcp import FastMCP
from starlette.testclient import TestClient

# FastMCP defaults to 127.0.0.1. n8n might be trying to connect via 0.0.0.0 or localhost
mcp = FastMCP("test", host="0.0.0.0", port=8000)

app = mcp.sse_app("/sse")

client = TestClient(app, base_url="http://0.0.0.0:8000")
response = client.get("/sse")
print(f"GET /sse on 0.0.0.0: {response.status_code}")
