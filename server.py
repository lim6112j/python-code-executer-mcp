import asyncio
import subprocess
import tempfile
import pathlib
import uvicorn

from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from mcp.server.fastmcp import FastMCP

# Define and create a workspace directory where Python code will execute
WORKSPACE_DIR = pathlib.Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

# Initialize FastMCP Server bound to 0.0.0.0 so external clients (like n8n) can connect
mcp = FastMCP("python-executor", host="0.0.0.0", port=8000)

@mcp.tool()
def execute_python_code(code: str) -> str:
    """Executes a block of Python code and returns its stdout and stderr.
    
    Args:
        code: The Python code to execute.
    
    Returns:
        The combined standard output and standard error from the execution.
    """
    # Create a temporary file to store the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = pathlib.Path(temp_file.name)
    
    try:
        # Execute the python code using a subprocess inside the workspace director
        result = subprocess.run(
            ["python3", str(temp_file_path)],
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE_DIR),
            timeout=10 # Add a sensible timeout (10 seconds)
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\n--- STDERR ---\n{result.stderr}"
            
        output += f"\n\n[System] Any generated files are available via HTTP at http://<server_ip>:8000/workspace/..."
        return output
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out after 10 seconds."
    except Exception as e:
        return f"Error executing code: {str(e)}"
    finally:
        # Clean up the temporary file
        if temp_file_path.exists():
            temp_file_path.unlink()

if __name__ == "__main__":
    # Get the underlying Starlette app from FastMCP
    app = mcp.sse_app("/sse")
    
    # Mount the workspace directory to be served statically
    app.routes.append(
        Mount("/workspace", app=StaticFiles(directory=str(WORKSPACE_DIR)), name="workspace")
    )
    
    print("Starting MCP Server with static file serving on http://0.0.0.0:8000")
    print("SSE endpoint: http://0.0.0.0:8000/sse")
    print("Static files: http://0.0.0.0:8000/workspace/")
    
    # Run the server using uvicorn correctly configured for 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=8000)
