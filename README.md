# MCP Descope SDK

A Python SDK for integrating Descope authentication with MCP (Model Context Protocol) servers. This SDK provides easy-to-use tools for fetching user and tenant tokens from Descope's outbound applications.

## Features

- 🔐 **Descope Integration**: Seamless integration with Descope's outbound applications
- 🚀 **MCP Protocol**: Built on top of the MCP Python SDK
- 🐍 **Python Native**: Uses the official Descope Python SDK
- 🔧 **Easy Setup**: Simple configuration and usage
- 📦 **Type Safe**: Full type hints and Pydantic models
- 🛡️ **Error Handling**: Comprehensive error handling and validation

## Installation

### Prerequisites

- Python 3.8 or higher
- Descope project with outbound applications configured

### Install from source

```bash
# Clone the repository
git clone https://github.com/your-org/mcp-descope.git
cd mcp-descope

# Install in development mode
pip install -e .
```

### Install dependencies

```bash
pip install mcp descope pydantic typing-extensions
```

## Quick Start

### 1. Set up environment variables

```bash
export DESCOPE_MCP_WELL_KNOWN_URL="https://api.descope.com/your-project-id/mcp"
export DESCOPE_MANAGEMENT_KEY="your-management-key"  # Optional
```

### 2. Basic usage

```python
import asyncio
from mcp_descope import create_default_client

async def main():
    client = create_default_client()

    async with client:
        # Fetch user token with scopes
        user_token = await client.fetch_user_token_by_scopes(
            app_id="my-app-id",
            user_id="user-123",
            scopes=["read", "write"],
            options={"refreshToken": True},
            tenant_id="tenant-456",
        )
        print(f"User token: {user_token.token}")

asyncio.run(main())
```

### 3. Run the server

```bash
python -m mcp_descope.server
```

## API Reference

### Client API

#### `DescopeMCPClient`

Main client class for interacting with the Descope MCP server.

```python
from mcp_descope import DescopeMCPClient

# Create client with custom server command
client = DescopeMCPClient(["python", "-m", "mcp_descope.server"])
```

#### `fetch_user_token_by_scopes`

Fetch user token with specific scopes.

```python
async def fetch_user_token_by_scopes(
    self,
    app_id: str,
    user_id: str,
    scopes: List[str],
    options: Optional[Dict[str, Any]] = None,
    tenant_id: Optional[str] = None,
) -> TokenResponse:
```

**Parameters:**

- `app_id`: Application ID
- `user_id`: User ID
- `scopes`: Required scopes (list of strings)
- `options`: Additional options (e.g., `{"refreshToken": True}`)
- `tenant_id`: Tenant ID (optional)

**Returns:**

- `TokenResponse`: Object containing the token and metadata

#### `fetch_user_token`

Fetch latest user token.

```python
async def fetch_user_token(
    self,
    app_id: str,
    user_id: str,
    tenant_id: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
) -> TokenResponse:
```

**Parameters:**

- `app_id`: Application ID
- `user_id`: User ID
- `tenant_id`: Tenant ID (optional)
- `options`: Additional options (e.g., `{"forceRefresh": True}`)

#### `fetch_tenant_token_by_scopes`

Fetch tenant token with specific scopes.

```python
async def fetch_tenant_token_by_scopes(
    self,
    app_id: str,
    tenant_id: str,
    scopes: List[str],
    options: Optional[Dict[str, Any]] = None,
) -> TokenResponse:
```

**Parameters:**

- `app_id`: Application ID
- `tenant_id`: Tenant ID
- `scopes`: Required scopes (list of strings)
- `options`: Additional options (e.g., `{"refreshToken": True}`)

#### `fetch_tenant_token`

Fetch latest tenant token.

```python
async def fetch_tenant_token(
    self,
    app_id: str,
    tenant_id: str,
    options: Optional[Dict[str, Any]] = None,
) -> TokenResponse:
```

**Parameters:**

- `app_id`: Application ID
- `tenant_id`: Tenant ID
- `options`: Additional options (e.g., `{"forceRefresh": True}`)

### Server API

#### `DescopeMCPServer`

MCP server implementation for Descope authentication operations.

```python
from mcp_descope import DescopeMCPServer, DescopeConfig

config = DescopeConfig(
    well_known_url="https://api.descope.com/your-project-id/mcp",
    management_key="your-management-key",  # Optional
)

server = DescopeMCPServer(config)
await server.run()
```

### Data Models

#### `DescopeConfig`

Configuration for the Descope MCP server.

```python
class DescopeConfig(BaseModel):
    well_known_url: str  # MCP server well-known URL
    management_key: Optional[str] = None  # Optional management key for direct API access
```

#### `TokenResponse`

Response containing token information.

```python
class TokenResponse(BaseModel):
    token: str
    expires_at: Optional[int] = None
    scopes: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
```

## Examples

### Basic Usage

```python
import asyncio
from mcp_descope import create_default_client

async def basic_example():
    client = create_default_client()

    async with client:
        # Fetch user token with scopes
        user_token = await client.fetch_user_token_by_scopes(
            app_id="my-app-id",
            user_id="user-123",
            scopes=["read", "write"],
            options={"refreshToken": True},
            tenant_id="tenant-456",
        )
        print(f"User token: {user_token.token}")

        # Fetch latest user token
        latest_user_token = await client.fetch_user_token(
            app_id="my-app-id",
            user_id="user-123",
            tenant_id="tenant-456",
            options={"forceRefresh": True},
        )
        print(f"Latest user token: {latest_user_token.token}")

        # Fetch tenant token with scopes
        tenant_token = await client.fetch_tenant_token_by_scopes(
            app_id="my-app-id",
            tenant_id="tenant-456",
            scopes=["read", "write"],
            options={"refreshToken": True},
        )
        print(f"Tenant token: {tenant_token.token}")

        # Fetch latest tenant token
        latest_tenant_token = await client.fetch_tenant_token(
            app_id="my-app-id",
            tenant_id="tenant-456",
            options={"forceRefresh": True},
        )
        print(f"Latest tenant token: {latest_tenant_token.token}")

asyncio.run(basic_example())
```

### Advanced Usage with Error Handling

```python
import asyncio
from mcp_descope import create_default_client

async def advanced_example():
    client = create_default_client()

    try:
        async with client:
            # Test different scope combinations
            scopes_combinations = [
                ["read"],
                ["write"],
                ["read", "write"],
                ["admin", "read", "write"],
            ]

            for scopes in scopes_combinations:
                try:
                    token = await client.fetch_user_token_by_scopes(
                        app_id="my-app-id",
                        user_id="user-123",
                        scopes=scopes,
                        tenant_id="tenant-456",
                    )
                    print(f"✅ Success with scopes {scopes}: {token.token[:20]}...")
                except Exception as e:
                    print(f"❌ Failed with scopes {scopes}: {e}")

    except Exception as e:
        print(f"❌ Client error: {e}")

asyncio.run(advanced_example())
```

### Running the Server

```python
import asyncio
import os
from mcp_descope import DescopeMCPServer, DescopeConfig

async def run_server():
    # Set up environment variables
    os.environ["DESCOPE_MCP_WELL_KNOWN_URL"] = "https://api.descope.com/your-project-id/mcp"
    os.environ["DESCOPE_MANAGEMENT_KEY"] = "your-management-key"  # Optional

    config = DescopeConfig(
        well_known_url=os.getenv("DESCOPE_MCP_WELL_KNOWN_URL", ""),
        management_key=os.getenv("DESCOPE_MANAGEMENT_KEY", ""),  # Optional
    )

    server = DescopeMCPServer(config)
    await server.run()

asyncio.run(run_server())
```

### Using with FastMCP

You can use Descope tools with FastMCP in two ways:

#### Option 1: Using `add_descope_tools` helper

```python
from mcp.server import FastMCP
from mcp_descope import add_descope_tools, DescopeConfig

# Create your FastMCP server
mcp = FastMCP("my-server")

# Add Descope tools
config = DescopeConfig(
    well_known_url="https://api.descope.com/your-project-id/mcp",
    management_key="your-management-key"  # Optional
)
add_descope_tools(mcp, config)

# Add your own tools
@mcp.tool()
def my_custom_tool():
    return "Hello"

mcp.run()
```

#### Option 2: Using functions directly with FastMCP decorators

You don't need a separate wrapper - just use the functions directly:

```python
from mcp.server import FastMCP
from mcp_descope import fetch_user_token, fetch_user_token_by_scopes, DescopeConfig

mcp = FastMCP("my-server")
config = DescopeConfig(
    well_known_url="https://api.descope.com/your-project-id/mcp",
    management_key="your-management-key"  # Optional
)

# Use Descope functions directly with FastMCP decorators
@mcp.tool()
async def get_user_token(app_id: str, user_id: str) -> str:
    """Get a user token using Descope."""
    return await fetch_user_token(config, app_id, user_id)

@mcp.tool()
async def get_user_token_with_scopes(
    app_id: str, user_id: str, scopes: list[str]
) -> str:
    """Get a user token with specific scopes."""
    return await fetch_user_token_by_scopes(config, app_id, user_id, scopes)

# Add your own tools
@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

mcp.run()
```

## Using with Descope Python SDK

This SDK is designed to work alongside the official Descope Python SDK (`descope`) without conflicts:

- **Different package names**: This SDK uses `mcp_descope` package, while Descope SDK uses `descope` package
- **No naming conflicts**: Function and class names are prefixed appropriately (e.g., `DescopeMCPClient` vs `DescopeClient`)
- **Shared DescopeClient**: This SDK imports and uses `DescopeClient` from the `descope` package, so you can use both SDKs together

Example:
```python
# Import both SDKs
from descope import DescopeClient  # Official Descope SDK
from mcp_descope import DescopeMCP, validate_token_and_get_user_id  # MCP Descope SDK

# Use Descope SDK directly
descope_client = DescopeClient(project_id="...", management_key="...")

# Use MCP Descope SDK
DescopeMCP(well_known_url="...", management_key="...", mcp_server_url="...")
```

## Examples

The SDK includes several examples demonstrating different use cases. Each example is in its own directory with its own dependencies.

### Running Examples

#### Using uv (Recommended)

```bash
# Navigate to any example directory
cd examples/basic_usage  # or fastmcp_calendar, fastmcp_auth

# Install dependencies
uv sync

# Run the example
uv run python <example_file>.py
```

#### Using pip

```bash
# Navigate to any example directory
cd examples/basic_usage  # or fastmcp_calendar, fastmcp_auth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install SDK in development mode
cd ../..
pip install -e .
cd examples/<example_name>

# Run the example
python <example_file>.py
```

### Available Examples

- **Basic Usage** (`examples/basic_usage/`): Basic token operations
- **FastMCP Calendar** (`examples/fastmcp_calendar/`): Google Calendar integration with Descope auth
- **FastMCP Authentication** (`examples/fastmcp_auth/`): FastMCP v3.0.0 auth features

See [examples/README.md](examples/README.md) for detailed information about each example.

## Configuration

### Environment Variables

- `DESCOPE_MCP_WELL_KNOWN_URL`: MCP server well-known URL (required)
- `DESCOPE_MANAGEMENT_KEY`: Your Descope management API key (optional, needed for direct API access)

### Options

#### User Token Options

- `refreshToken`: Boolean - Whether to refresh the token
- `forceRefresh`: Boolean - Whether to force refresh the token

#### Tenant Token Options

- `refreshToken`: Boolean - Whether to refresh the token
- `forceRefresh`: Boolean - Whether to force refresh the token

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/mcp-descope.git
cd mcp-descope

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=mcp_descope

# Run specific test file
pytest tests/test_client.py
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Type checking with mypy
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Release Process

Releases are automated using GitHub Actions. See [RELEASE.md](RELEASE.md) for detailed instructions.

### Quick Release Steps

1. **Update version** in `pyproject.toml` and `src/mcp_descope/__init__.py`
2. **Create a git tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The workflow will automatically build and publish to PyPI

Alternatively, create a GitHub Release from the Releases page, and the workflow will handle everything automatically.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/mcp-descope/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/your-org/mcp-descope/wiki)

## Changelog

### v0.1.0

- Initial release
- Support for user and tenant token operations
- MCP server and client implementation
- Comprehensive error handling
- Type-safe API with Pydantic models
