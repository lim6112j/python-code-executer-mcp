import asyncio
import os
import uvicorn
import pathlib
import threading
from mcp.server.fastmcp import FastMCP
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
import httpx

# Define and create a workspace directory where Python code will execute
WORKSPACE_DIR = pathlib.Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)
(WORKSPACE_DIR / "test.txt").write_text("ok")

mcp = FastMCP("test")
mcp._custom_starlette_routes.append(
    Mount("/workspace", app=StaticFiles(directory=str(WORKSPACE_DIR)), name="workspace")
)

def run_server():
    mcp.run(transport='sse')

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

import time; time.sleep(2)
try:
    r = httpx.get("http://0.0.0.0:8000/workspace/test.txt")
    print("Static GET:", r.status_code, r.text)
except Exception as e:
    print("Err:", e)
