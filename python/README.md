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

#### Basic Token Validation

```python
from mcp_descope import validate_token, validate_token_and_get_user_id, TokenValidationResult

# Get full validation result
result: TokenValidationResult = validate_token(access_token)
# Returns: {"sub": "user-123", "scopes": ["read", "write"], "tenant": {...}, ...}

# Access token fields
user_id = result.get("sub") or result.get("userId")
scopes = result.get("scopes", [])
tenant_id = result.get("tenant") or result.get("tenantId")

# Or just get user ID (convenience function)
user_id = validate_token_and_get_user_id(access_token)
```

#### TokenValidationResult Type

The `validate_token()` function returns a `TokenValidationResult` dictionary with the following fields:

- `sub` (str): User ID (JWT standard subject claim)
- `userId` (str): Alternative user ID field
- `scopes` (List[str]): List of OAuth scopes granted to the token
- `tenant` (str): Tenant ID (if available)
- `tenantId` (str): Alternative tenant ID field
- `aud` (str): Audience claim (MCP server URL)
- `user` (Dict[str, Any]): Nested user object with additional information
- Other JWT claims (`exp`, `iat`, `iss`, etc.)

**Note:** Not all fields may be present in every token. Always use `.get()` with defaults when accessing fields.

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
    management_key: Optional[str], # Optional: Fallback for user/tenant connection token fetching
    mcp_server_url: Optional[str] # Optional: Audience for token validation
)
```

#### Methods

- `validate_token(access_token: str, audience: Optional[str] = None) -> TokenValidationResult`
  - Validates token and returns full validation result
  - Returns a dictionary with user ID, scopes, tenant info, and other JWT claims

- `validate_token_and_get_user_id(access_token: str, audience: Optional[str] = None) -> str`
  - Validates token and returns user ID (convenience method)

- `require_scopes(token_result: TokenValidationResult, required_scopes: List[str], error_description: Optional[str] = None) -> None`
  - Validates that token has required scopes
  - Raises `InsufficientScopeError` if any scopes are missing
  - Follows MCP spec for insufficient scope errors

- `get_connection_token(user_id: str, app_id: str, scopes: Optional[List[str]] = None, access_token: Optional[str] = None, ...) -> str`
  - Retrieves connection token (uses access_token by default)
  - Enables policy enforcement when access_token is provided

### Standalone Functions

For convenience, you can also use standalone functions:

```python
from mcp_descope import (
    validate_token,
    validate_token_and_get_user_id,
    require_scopes,
    InsufficientScopeError,
    get_connection_token,
    init_descope_mcp,
    TokenValidationResult
)

# Initialize global state
init_descope_mcp(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    mcp_server_url="https://your-mcp-server.com"
)

# Validate token and get full result
result: TokenValidationResult = validate_token(access_token)
user_id = result.get("sub") or result.get("userId")
scopes = result.get("scopes", [])

# Or use convenience function
user_id = validate_token_and_get_user_id(access_token)

# Require specific scopes
try:
    require_scopes(result, ["read", "write"])
except InsufficientScopeError as e:
    # Handle insufficient scope error
    error_response = e.to_json()

# Get connection token
token = get_connection_token(
    user_id="user-123",
    app_id="google-calendar",
    access_token=access_token
)
```

### Exceptions

#### InsufficientScopeError

Raised when a token lacks required scopes. This follows the MCP spec’s **Runtime Insufficient Scope Errors** behavior (HTTP 403 + `WWW-Authenticate: Bearer error="insufficient_scope", scope="..."`) as described in the MCP Authorization spec: [Runtime Insufficient Scope Errors](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization#runtime-insufficient-scope-errors).

```python
from mcp_descope import InsufficientScopeError

try:
    require_scopes(token_result, ["calendar.read"])
except InsufficientScopeError as e:
    # Access error information
    missing = e.missing_scopes  # ["calendar.read"]
    combined = e.combined_scopes  # ["read", "write", "calendar.read"]
    scope_param = e.scope_parameter  # "read write calendar.read"
    
    # Get MCP spec-compliant JSON response
    error_json = e.to_json()
    
    # Or get as dictionary
    error_dict = e.to_dict()
```

### Scope Validation

The SDK provides a clean API for validating required scopes, following the MCP spec for insufficient scope errors.

#### Using require_scopes()

```python
from mcp_descope import validate_token, require_scopes, InsufficientScopeError
import json

@mcp.tool()
def my_tool(mcp_access_token: str) -> str:
    try:
        # Validate token
        token_result = validate_token(mcp_access_token)
        
        # Require specific scopes - raises InsufficientScopeError if missing
        require_scopes(token_result, ["read", "write"])
        
        # If we get here, all scopes are present
        return "Success"
    except InsufficientScopeError as e:
        # Return MCP spec-compliant error response
        return e.to_json()
```

#### InsufficientScopeError

When `require_scopes()` detects missing scopes, it raises an `InsufficientScopeError` exception that follows the MCP spec (RFC 6750 Section 3.1).

The error includes:
- `error`: "insufficient_scope"
- `scope`: Space-separated list of all scopes (existing + required) - uses recommended approach
- `error_description`: Human-readable description
- `missing_scopes`: List of missing scopes
- `token_scopes`: List of scopes in the token
- `required_scopes`: List of required scopes

**Example error response:**
```json
{
  "error": "insufficient_scope",
  "scope": "read write calendar.read",
  "error_description": "Token missing required scopes: calendar.read",
  "missing_scopes": ["calendar.read"],
  "token_scopes": ["read", "write"],
  "required_scopes": ["read", "write", "calendar.read"]
}
```

The `scope` parameter uses the **recommended approach** - it includes both existing scopes from the token and newly required scopes. This prevents clients from losing previously granted permissions.

#### Complete Example with Scope Validation

```python
from mcp.server import FastMCP
from mcp_descope import (
    DescopeMCP,
    validate_token,
    require_scopes,
    InsufficientScopeError,
    get_connection_token
)
import json

DescopeMCP(well_known_url="...", mcp_server_url="...")
mcp = FastMCP("my-server")

@mcp.tool()
async def get_calendar_events(mcp_access_token: str) -> str:
    """Get calendar events - requires 'calendar.read' scope."""
    try:
        # Validate token and require scopes
        token_result = validate_token(mcp_access_token)
        require_scopes(token_result, ["calendar.read"])
        
        # Get user ID and connection token
        user_id = token_result.get("sub") or token_result.get("userId")
        google_token = get_connection_token(
            user_id=user_id,
            app_id="google-calendar",
            scopes=["https://www.googleapis.com/auth/calendar"],
            access_token=mcp_access_token
        )
        
        # Make API call...
        return json.dumps({"status": "success"})
    except InsufficientScopeError as e:
        # Return MCP spec-compliant error
        return e.to_json()
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

- **[FastMCP Calendar](./examples/fastmcp_calendar/)** - Google Calendar integration with FastMCP, including token validation, scope checking, and connection token retrieval
- **[Tenant Tokens](./examples/tenant_token/)** - Fetching tenant-level connection tokens using management keys

### Example: Protected Tool with Scope Validation

```python
from mcp.server import FastMCP
from mcp_descope import (
    DescopeMCP,
    validate_token,
    require_scopes,
    InsufficientScopeError,
    get_connection_token
)
import json

# Initialize SDK
DescopeMCP(
    well_known_url="https://api.descope.com/your-project-id/.well-known/openid-configuration",
    mcp_server_url="https://your-mcp-server.com"
)

mcp = FastMCP("calendar-server")

@mcp.tool()
async def get_calendar_events(
    mcp_access_token: str,
    max_results: int = 10
) -> str:
    """Get Google Calendar events.
    
    Requires 'calendar.read' scope in the MCP access token.
    """
    try:
        # Validate token
        token_result = validate_token(mcp_access_token)
        
        # Require specific scope - raises InsufficientScopeError if missing
        require_scopes(token_result, ["calendar.read"])
        
        # Get user ID and connection token
        user_id = token_result.get("sub") or token_result.get("userId")
        google_token = get_connection_token(
            user_id=user_id,
            app_id="google-calendar",
            scopes=["https://www.googleapis.com/auth/calendar"],
            access_token=mcp_access_token
        )
        
        # Make API call with connection token
        # ... (API call code)
        
        return json.dumps({"status": "success", "events": [...]})
    except InsufficientScopeError as e:
        # Return MCP spec-compliant error response
        return e.to_json()
    except Exception as e:
        return json.dumps({"error": str(e)})

mcp.run()
```

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

## Types and Models

### TokenValidationResult

Type definition for token validation results. All fields are optional as the exact structure may vary based on token claims.

```python
from mcp_descope import TokenValidationResult

result: TokenValidationResult = validate_token(access_token)

# Common fields:
user_id = result.get("sub") or result.get("userId")
scopes = result.get("scopes", [])
tenant_id = result.get("tenant") or result.get("tenantId")
audience = result.get("aud")
```

### InsufficientScopeError

Exception raised when token lacks required scopes. Follows MCP spec (RFC 6750 Section 3.1).

**Properties:**
- `required_scopes`: List of scopes required for the operation
- `token_scopes`: List of scopes present in the token
- `missing_scopes`: List of missing scopes
- `combined_scopes`: List of all scopes (existing + required) - recommended approach
- `scope_parameter`: Space-separated scope string for MCP spec compliance
- `error_description`: Human-readable error description

**Methods:**
- `to_dict()`: Convert error to dictionary
- `to_json()`: Convert error to JSON string (MCP spec-compliant)

## Security Best Practices

1. **Always provide `mcp_server_url`** for audience validation to prevent token reuse
2. **Use access tokens by default** to enable policy enforcement
3. **Validate tokens on every request** - don't cache validation results
4. **Use `require_scopes()` for scope validation** - ensures MCP spec compliance
5. **Handle `InsufficientScopeError` properly** - return error responses using `e.to_json()`
6. **Use minimal scopes** when requesting connection tokens
7. **Store management keys securely** - only use as fallback for tenant tokens

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
