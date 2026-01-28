# Descope Python MCP SDK

Python SDK for integrating Descope authentication and authorization with MCP (Model Context Protocol) servers.

## Overview

The Descope Python MCP SDK provides a policy-enforced authorization layer for MCP servers, enabling:

- **Token validation** with scope and audience enforcement
- **Connection token retrieval** using MCP server access tokens (default) or management keys
- **Policy enforcement** through Descope's Access Control Plane
- **Seamless integration** with FastMCP and the official MCP SDK

## Installation

```bash
pip install mcp-descope
```

## Quick Start

### Basic Setup

```python
from mcp_descope import DescopeMCP

# Initialize the SDK
mcp = DescopeMCP(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    mcp_server_url="https://your-mcp-server.com"  # Used for audience validation
)

# Validate an MCP server access token
user_id = mcp.validate_token_and_get_user_id("access-token-from-client")
```

### Using with FastMCP

```python
from mcp.server import FastMCP
from mcp_descope import DescopeMCP, validate_token_and_get_user_id, get_connection_token

# Initialize SDK
DescopeMCP(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    mcp_server_url="https://your-mcp-server.com"
)

mcp = FastMCP("my-server")

@mcp.tool()
async def get_calendar_events(mcp_access_token: str) -> str:
    """Get calendar events for the authenticated user."""
    # Validate token and get user ID
    user_id = validate_token_and_get_user_id(mcp_access_token)
    
    # Get connection token using MCP access token (enables policy enforcement)
    google_token = get_connection_token(
        user_id=user_id,
        app_id="google-calendar",
        scopes=["https://www.googleapis.com/auth/calendar"],
        access_token=mcp_access_token  # Uses access token by default
    )
    
    # Use token to call external API
    # ... make API call with google_token
    return "Events retrieved"
```

## Core Concepts

### Authentication Methods

The SDK supports two methods for retrieving connection tokens:

#### 1. MCP Server Access Tokens (Default, Recommended)

Uses the MCP server access token to fetch connection tokens. This enables:
- **Policy enforcement** through Descope's Access Control Plane
- **Real-time authorization** decisions based on user identity, roles, and scopes
- **No management keys required** in your MCP server code

```python
# Access token is automatically used when provided
token = get_connection_token(
    user_id=user_id,
    app_id="google-calendar",
    access_token=mcp_access_token  # MCP server access token
)
```

#### 2. Management Keys (Fallback)

Management keys can be used as a fallback, particularly for:
- Tenant-level tokens
- Server-to-server operations
- When access tokens aren't available

```python
# Initialize with management key
mcp = DescopeMCP(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    management_key="your-management-key"  # Optional, fallback only
)

# Uses management key when no access token provided
token = mcp.get_connection_token(
    user_id=user_id,
    app_id="google-calendar"
)
```

### Token Validation

The SDK validates MCP server access tokens with:
- **Signature verification** using Descope's public keys
- **Expiration checking** to ensure tokens are still valid
- **Audience validation** to prevent token reuse across servers
- **Scope extraction** for authorization decisions

```python
from mcp_descope import validate_token, validate_token_and_get_user_id

# Get full validation result
result = validate_token(access_token, audience="https://your-mcp-server.com")
# Returns: {"sub": "user-123", "scopes": ["read", "write"], "tenant": {...}, ...}

# Or just get user ID
user_id = validate_token_and_get_user_id(access_token)
```

### Connection Tokens

Connection tokens are OAuth tokens for third-party services (Google Calendar, Slack, etc.) stored in Descope's Connections vault.

```python
from mcp_descope import get_connection_token

# Get token with specific scopes
token = get_connection_token(
    user_id="user-123",
    app_id="google-calendar",
    scopes=["https://www.googleapis.com/auth/calendar.readonly"],
    access_token=mcp_access_token  # Recommended: enables policy enforcement
)

# Get latest token (any scopes)
token = get_connection_token(
    user_id="user-123",
    app_id="google-calendar",
    access_token=mcp_access_token
)
```

## API Reference

### DescopeMCP Class

Main SDK client class, similar to `DescopeClient` in the Descope Python SDK.

```python
from mcp_descope import DescopeMCP

mcp = DescopeMCP(
    well_known_url: str,           # Required: MCP server well-known URL
    management_key: Optional[str], # Optional: Fallback for tenant tokens
    mcp_server_url: Optional[str] # Optional: Audience for token validation
)
```

#### Methods

- `validate_token(access_token: str, audience: Optional[str] = None) -> Dict[str, Any]`
  - Validates token and returns full validation result

- `validate_token_and_get_user_id(access_token: str, audience: Optional[str] = None) -> str`
  - Validates token and returns user ID

- `get_connection_token(user_id: str, app_id: str, scopes: Optional[List[str]] = None, access_token: Optional[str] = None, ...) -> str`
  - Retrieves connection token (uses access_token by default)

### Standalone Functions

For convenience, you can also use standalone functions:

```python
from mcp_descope import (
    validate_token,
    validate_token_and_get_user_id,
    get_connection_token,
    init_descope_mcp
)

# Initialize global state
init_descope_mcp(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    mcp_server_url="https://your-mcp-server.com"
)

# Use functions without passing config
user_id = validate_token_and_get_user_id(access_token)
token = get_connection_token(user_id="user-123", app_id="google-calendar", access_token=access_token)
```

### FastMCP Integration

#### Using with FastMCP 2.0

```python
from mcp.server import FastMCP
from mcp_descope import DescopeMCP, validate_token_and_get_user_id, get_connection_token

DescopeMCP(well_known_url="...", mcp_server_url="...")

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(mcp_access_token: str) -> str:
    user_id = validate_token_and_get_user_id(mcp_access_token)
    # ... use user_id
    return "Result"
```

#### Adding Descope Tools to FastMCP

```python
from mcp.server import FastMCP
from mcp_descope import add_descope_tools, DescopeConfig

mcp = FastMCP("my-server")

add_descope_tools(
    mcp,
    DescopeConfig(
        well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
        management_key="your-management-key"  # Optional
    )
)

# Descope tools are now available on your MCP server
mcp.run()
```

## Examples

See the [examples directory](./examples/) for complete working examples:

- **[Basic Usage](./examples/basic_usage/)** - Simple token validation and connection token retrieval
- **[FastMCP Calendar](./examples/fastmcp_calendar/)** - Google Calendar integration with FastMCP
- **[Tenant Tokens](./examples/tenant_token/)** - Fetching tenant-level connection tokens

## Configuration

### Environment Variables

You can configure the SDK using environment variables:

```bash
export DESCOPE_MCP_WELL_KNOWN_URL="https://api.descope.com/your-project-id/.well-known/openid-configuration"
export MCP_SERVER_URL="https://your-mcp-server.com"
export DESCOPE_MANAGEMENT_KEY="your-management-key"  # Optional
```

### Well-Known URL Format

The well-known URL follows the OpenID Connect discovery pattern:

```
https://api.descope.com/{project_id}/.well-known/openid-configuration
```

The SDK automatically extracts the project ID from this URL when needed.

## Security Best Practices

1. **Always provide `mcp_server_url`** for audience validation to prevent token reuse
2. **Use access tokens by default** to enable policy enforcement
3. **Validate tokens on every request** - don't cache validation results
4. **Use minimal scopes** when requesting connection tokens
5. **Store management keys securely** - only use as fallback for tenant tokens

## Testing

Run the test suite:

```bash
cd python
pytest tests/
```

See [tests/README.md](./tests/README.md) for more information.

## Compatibility

- **Python**: 3.8+
- **MCP SDK**: 1.0.0+
- **Descope SDK**: 1.0.0+
- **FastMCP**: 2.0+ (FastMCP 3.0 support coming soon)

The SDK can be imported alongside the official Descope Python SDK without conflicts:

```python
import descope  # Official Descope SDK
import mcp_descope  # MCP Descope SDK

# Both work together without issues
```

## License

MIT

## Support

- [Documentation](https://docs.descope.com)
- [GitHub Issues](https://github.com/your-org/mcp-descope/issues)
- [Community Slack](https://www.descope.com/community)
