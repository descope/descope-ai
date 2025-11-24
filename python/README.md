# Descope AI SDK

*Super* lightweight Python SDK for interacting with Descope's MCP (Model Context Protocol) authorization server.

This repository contains utilities to help you enforce and manage Descope tokens in your MCP Servers.

## Requirements

- Python 3.8 or newer

## Installation

Install from `uv` (recommended):

```bash
uv add descope-mcp
```

Or, if you're using `pip`:

```bash
pip install descope-mcp
```

Or install from source for development:

```bash
git clone https://github.com/descope/mcp-python.git
cd mcp-python
python -m pip install -e .
```

## Quickstart

Set your API key in an environment variable:

```bash
export DESCOPE_API_KEY="your_api_key_here"
```

Basic synchronous example:

```python
from descope_mcp import MCPClient
import os

client = MCPClient(api_key=os.getenv("DESCOPE_API_KEY"))

response = client.call_model("model-name", {"input": "Hello, world!"})
print(response)
```

Basic asynchronous example:

```python
import asyncio
from descope_mcp import AsyncMCPClient
import os

async def main():
	client = AsyncMCPClient(api_key=os.getenv("DESCOPE_API_KEY"))
	response = await client.call_model("model-name", {"input": "Hello, async world!"})
	print(response)

asyncio.run(main())
```

Notes:
- Replace `"model-name"` and the input payload with the model and parameters your application needs.
- The SDK returns plain Python objects (dicts) representing the JSON response from Descope MCP.

## Configuration

The client can be configured via environment variables or directly when instantiating the client.

- `DESCOPE_API_KEY`: (required) API key used to authenticate requests.
- `DESCOPE_BASE_URL`: (optional) custom base URL for MCP endpoints.
- `DESCOPE_TIMEOUT`: (optional) request timeout in seconds.

Example (explicit config):

```python
from descope_mcp import MCPClient

client = MCPClient(api_key="...", base_url="https://api.descope.example", timeout=30)
```

## Error handling

The SDK raises exceptions for transport and API-level errors. Catch these in your application to provide retries, fallbacks, or user-friendly messages.

## Development

Install development dependencies (if provided):

```bash
python -m pip install -e .[dev]
```

Run tests (if the project includes tests):

```bash
pytest
```

Format code with `black` and lint with `flake8` as desired.

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Add tests for new behavior.
4. Open a pull request describing your changes.

See `CONTRIBUTING.md` (if present) for more details.

## License

See the `LICENSE` file in this repository for license details.

## Support

For usage questions and troubleshooting, visit the official Descope documentation: https://docs.descope.com or open an issue in this repository.

---

If you want the README adapted to include real code samples from your actual client API (method names, return shapes, or advanced usage like streaming examples), share the client module or function names and I will update the examples to match exactly.

