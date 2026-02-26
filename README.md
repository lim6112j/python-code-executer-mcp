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

### Inspecting with the MCP Inspector
To test the server interactively, use the MCP CLI inspector provided by Model Context Protocol:
```bash
# Ensure your virtual environment is activated
npx @modelcontextprotocol/inspector python3 server.py
```

## Tools

* **`execute_python_code(code: str) -> str`**: Executes a block of Python code and returns its standard output and standard error. It writes the code to a temporary file and runs it with `python3`. It includes a 10-second timeout.
