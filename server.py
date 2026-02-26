import asyncio
import subprocess
import tempfile
import pathlib

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("python-executor")

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
        # Execute the python code using a subprocess
        result = subprocess.run(
            ["python3", str(temp_file_path)],
            capture_output=True,
            text=True,
            timeout=10 # Add a sensible timeout (10 seconds)
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\n--- STDERR ---\n{result.stderr}"
            
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
    # Run the server using SSE transport (defaults to localhost:8000 usually, can be configured)
    mcp.run(transport='sse')
