# Python Code Executer MCP

This is a Model Context Protocol (MCP) server written in Python that allows LLMs to execute Python code locally and get the result.

## Setup

1. Create a virtual environment and install the dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

You can run the server directly:
```bash
python3 server.py
```
This will start an SSE server running on `http://127.0.0.1:8000`.

### Inspecting with the MCP Inspector
To test the server interactively, use the MCP CLI inspector provided by Model Context Protocol:
```bash
# Provide the SSE URL to the inspector
npx @modelcontextprotocol/inspector http://127.0.0.1:8000/sse
```

### Programmatic Usage
You can connect to the server programmatically using the `mcp.client.sse.sse_client`. We provide an example in `test_client_sse.py`:
```bash
# Keep the server running in another tab, then run:
python3 test_client_sse.py
```

## Tools

* **`execute_python_code(code: str) -> str`**: Executes a block of Python code and returns its standard output and standard error. It writes the code to a temporary file and runs it with `python3`. It includes a 10-second timeout.
