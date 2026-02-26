import pathlib
from mcp.server.fastmcp import FastMCP
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

mcp = FastMCP("test")

# Create workspace
WORKSPACE_DIR = pathlib.Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)
(WORKSPACE_DIR / "test.txt").write_text("Hello from workspace")

app = mcp.sse_app()
app.routes.append(
    Mount("/workspace", app=StaticFiles(directory=str(WORKSPACE_DIR)), name="workspace")
)

import uvicorn
print("About to run uvicorn on port 8001")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
