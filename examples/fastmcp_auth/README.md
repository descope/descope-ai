# FastMCP Descope Authentication Example

This example demonstrates FastMCP v3.0.0 authentication features with Descope, including basic auth, scope-based auth, tag-based auth, and custom auth checks.

## Prerequisites

- Python 3.8 or higher
- Descope project with MCP server URL configured
- FastMCP v3.0.0+ (if using FastMCP-specific auth features)

## Setup

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to this directory
cd examples/fastmcp_auth

# Install dependencies
uv sync

# Run the example
uv run python fastmcp_descope_auth_example.py
```

### Option 2: Using pip

```bash
# Navigate to this directory
cd examples/fastmcp_auth

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the SDK in development mode from the root directory
cd ../..
pip install -e .
cd examples/fastmcp_auth

# Run the example
python fastmcp_descope_auth_example.py
```

## Configuration

Set the following environment variables before running:

```bash
export DESCOPE_MCP_WELL_KNOWN_URL="https://api.descope.com/your-project-id/.well-known/openid-configuration"
export SERVER_URL="http://localhost:8000"
```

Or create a `.env` file in this directory:

```
DESCOPE_MCP_WELL_KNOWN_URL=https://api.descope.com/your-project-id/.well-known/openid-configuration
SERVER_URL=http://localhost:8000
```

## What This Example Shows

1. **Basic Authentication**: Requiring authentication without scope checks
2. **Scope-Based Authorization**: Requiring specific scopes (e.g., `read`, `write`)
3. **Tag-Based Authorization**: Restricting access based on tags
4. **Custom Auth Checks**: Creating custom authentication logic
5. **Token Access**: Accessing tokens in tools

## Key Features

- ✅ Basic authentication
- ✅ Scope-based access control
- ✅ Tag-based access control
- ✅ Custom auth checks
- ✅ Token access in tools

## Running

```bash
python fastmcp_descope_auth_example.py
```

## Notes

- This example demonstrates FastMCP v3.0.0 authentication patterns
- Some features may require FastMCP v3.0.0+ to work properly
- Adjust imports based on your FastMCP version
