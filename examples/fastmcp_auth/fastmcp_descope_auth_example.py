#!/usr/bin/env python3
"""FastMCP server example with Descope authentication and scope validation.

This example demonstrates how to use FastMCP v3.0.0 with Descope authentication
and various authorization patterns including scope-based access control.
"""

import os
import sys
from pathlib import Path

# Add the SDK to the Python path if running from example directory
# In production, the SDK would be installed via pip
example_dir = Path(__file__).parent
root_dir = example_dir.parent.parent
sdk_src = root_dir / "src"
if sdk_src.exists():
    sys.path.insert(0, str(sdk_src))

from fastmcp import FastMCP
from fastmcp.server.auth import (
    AuthContext,
    require_auth,
    require_scopes,
    restrict_tag,
)
from fastmcp.server.auth.providers.descope import DescopeProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import AuthMiddleware


def example_basic_auth():
    """Example: Basic authentication with Descope."""
    
    # Set up environment variables
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    # The DescopeProvider automatically discovers Descope endpoints
    # and configures JWT token validation
    auth_provider = DescopeProvider(
        config_url=well_known_url,  # Your MCP Server .well-known URL
        base_url=server_url,         # Your server's public URL
    )
    
    # Create FastMCP server with auth
    mcp = FastMCP(
        name="My Descope Protected Server",
        auth=auth_provider
    )
    
    # Public tool - no auth required
    @mcp.tool
    def public_info() -> str:
        """Get public information. No authentication required."""
        return "This is public information available to everyone."
    
    # Protected tool - requires authentication
    @mcp.tool(auth=require_auth)
    def protected_info() -> str:
        """Get protected information. Requires authentication."""
        return "This is protected information only for authenticated users."
    
    print("✅ Basic auth example created")
    print("Tools:")
    print("  - public_info (no auth)")
    print("  - protected_info (requires auth)")
    
    return mcp


def example_scope_based_auth():
    """Example: Scope-based authorization."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    mcp = FastMCP(
        name="Scoped Descope Server",
        auth=auth_provider
    )
    
    # Tool requiring single scope
    @mcp.tool(auth=require_scopes("read"))
    def read_data() -> str:
        """Read data. Requires 'read' scope."""
        return "Data read successfully"
    
    # Tool requiring multiple scopes (AND logic - all must be present)
    @mcp.tool(auth=require_scopes("read", "write"))
    def read_write_data() -> str:
        """Read and write data. Requires both 'read' AND 'write' scopes."""
        return "Data read and written successfully"
    
    # Tool requiring admin scope
    @mcp.tool(auth=require_scopes("admin"))
    def admin_operation() -> str:
        """Admin operation. Requires 'admin' scope."""
        return "Admin operation completed"
    
    # Tool with combined checks (auth AND scopes)
    @mcp.tool(auth=[require_auth, require_scopes("admin")])
    def secure_admin_action() -> str:
        """Secure admin action. Requires authentication AND 'admin' scope."""
        return "Secure admin action completed"
    
    print("✅ Scope-based auth example created")
    print("Tools:")
    print("  - read_data (requires 'read' scope)")
    print("  - read_write_data (requires 'read' AND 'write' scopes)")
    print("  - admin_operation (requires 'admin' scope)")
    print("  - secure_admin_action (requires auth AND 'admin' scope)")
    
    return mcp


def example_tag_based_auth():
    """Example: Tag-based authorization with middleware."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    # Create server with tag-based auth middleware
    mcp = FastMCP(
        name="Tag-Based Auth Server",
        auth=auth_provider,
        middleware=[
            # Apply 'admin' scope requirement to components tagged 'admin'
            AuthMiddleware(auth=restrict_tag("admin", scopes=["admin"])),
            # Apply 'write' scope requirement to components tagged 'write'
            AuthMiddleware(auth=restrict_tag("write", scopes=["write"])),
        ]
    )
    
    # Tagged with 'admin' - requires 'admin' scope
    @mcp.tool(tags={"admin"})
    def delete_all_data() -> str:
        """Delete all data. Tagged 'admin', so requires 'admin' scope."""
        return "All data deleted"
    
    # Tagged with 'write' - requires 'write' scope
    @mcp.tool(tags={"write"})
    def update_record(id: str, data: str) -> str:
        """Update a record. Tagged 'write', so requires 'write' scope."""
        return f"Record {id} updated with {data}"
    
    # No tag - accessible to all (no scope requirement from middleware)
    @mcp.tool
    def read_record(id: str) -> str:
        """Read a record. No tag restrictions, accessible to all."""
        return f"Record {id} content"
    
    # Multiple tags - requires scopes for all tags
    @mcp.tool(tags={"admin", "write"})
    def admin_write_operation() -> str:
        """Admin write operation. Requires both 'admin' AND 'write' scopes."""
        return "Admin write operation completed"
    
    print("✅ Tag-based auth example created")
    print("Tools:")
    print("  - delete_all_data (tagged 'admin', requires 'admin' scope)")
    print("  - update_record (tagged 'write', requires 'write' scope)")
    print("  - read_record (no tags, public)")
    print("  - admin_write_operation (tags 'admin' and 'write')")
    
    return mcp


def example_custom_auth_checks():
    """Example: Custom authorization checks based on token claims."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    mcp = FastMCP(
        name="Custom Auth Server",
        auth=auth_provider
    )
    
    # Custom check: require premium user
    def require_premium_user(ctx: AuthContext) -> bool:
        """Check for premium user status in token claims."""
        if ctx.token is None:
            return False
        return ctx.token.claims.get("premium", False) is True
    
    # Factory function for level-based authorization
    def require_access_level(minimum_level: int):
        """Factory function for level-based authorization."""
        def check(ctx: AuthContext) -> bool:
            if ctx.token is None:
                return False
            user_level = ctx.token.claims.get("level", 0)
            return user_level >= minimum_level
        return check
    
    # Custom check with explicit denial message
    from fastmcp.exceptions import AuthorizationError
    
    def require_verified_email(ctx: AuthContext) -> bool:
        """Require verified email with explicit denial message."""
        if ctx.token is None:
            raise AuthorizationError("Authentication required")
        if not ctx.token.claims.get("email_verified", False):
            raise AuthorizationError("Email verification required")
        return True
    
    # Tool requiring premium user
    @mcp.tool(auth=require_premium_user)
    def premium_feature() -> str:
        """Premium feature. Only for premium users."""
        return "Premium content unlocked"
    
    # Tool requiring access level 5
    @mcp.tool(auth=require_access_level(5))
    def advanced_feature() -> str:
        """Advanced feature. Requires access level 5 or higher."""
        return "Advanced feature unlocked"
    
    # Tool requiring verified email
    @mcp.tool(auth=require_verified_email)
    def email_verified_feature() -> str:
        """Feature requiring verified email."""
        return "Email verified feature"
    
    # Combined custom checks
    @mcp.tool(auth=[require_auth, require_premium_user, require_access_level(3)])
    def premium_level3_feature() -> str:
        """Premium feature requiring level 3+. Multiple checks combined."""
        return "Premium level 3+ feature"
    
    print("✅ Custom auth checks example created")
    print("Tools:")
    print("  - premium_feature (requires premium claim)")
    print("  - advanced_feature (requires level >= 5)")
    print("  - email_verified_feature (requires verified email)")
    print("  - premium_level3_feature (multiple custom checks)")
    
    return mcp


def example_token_access_in_tools():
    """Example: Accessing tokens in tools for personalized responses."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    mcp = FastMCP(
        name="Token Access Server",
        auth=auth_provider
    )
    
    @mcp.tool
    def personalized_greeting() -> str:
        """Greet the user based on their token claims."""
        token = get_access_token()
        
        if token is None:
            return "Hello, guest!"
        
        name = token.claims.get("name", "user")
        return f"Hello, {name}!"
    
    @mcp.tool(auth=require_auth)
    def user_dashboard() -> dict:
        """Return user-specific data based on token."""
        token = get_access_token()
        
        if token is None:
            return {"error": "Not authenticated"}
        
        return {
            "client_id": token.client_id,
            "scopes": token.scopes,
            "claims": token.claims,
            "expires_at": token.expires_at.isoformat() if token.expires_at else None,
        }
    
    @mcp.tool(auth=require_scopes("read"))
    def user_profile() -> dict:
        """Get user profile. Requires 'read' scope."""
        token = get_access_token()
        
        if not token:
            return {"error": "No token"}
        
        # Extract user info from claims
        return {
            "user_id": token.claims.get("sub", "unknown"),
            "email": token.claims.get("email", "unknown"),
            "premium": token.claims.get("premium", False),
            "level": token.claims.get("level", 0),
            "scopes": token.scopes,
        }
    
    @mcp.tool(auth=require_scopes("admin"))
    def admin_dashboard() -> dict:
        """Admin dashboard. Requires 'admin' scope."""
        token = get_access_token()
        
        return {
            "admin": True,
            "client_id": token.client_id if token else None,
            "all_scopes": token.scopes if token else [],
            "claims": token.claims if token else {},
        }
    
    print("✅ Token access example created")
    print("Tools:")
    print("  - personalized_greeting (uses token claims)")
    print("  - user_dashboard (requires auth, shows token info)")
    print("  - user_profile (requires 'read' scope)")
    print("  - admin_dashboard (requires 'admin' scope)")
    
    return mcp


def example_component_level_vs_middleware():
    """Example: Component-level auth vs middleware enforcement."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    # Server with component-level auth (filters list, doesn't block execution)
    mcp_component = FastMCP(
        name="Component-Level Auth Server",
        auth=auth_provider
    )
    
    @mcp_component.tool(auth=require_auth)
    def component_level_tool() -> str:
        """Component-level auth: filters from list but doesn't block execution."""
        return "This tool is filtered from lists for unauthenticated users"
    
    # Server with middleware enforcement (filters list AND blocks execution)
    mcp_middleware = FastMCP(
        name="Middleware Enforcement Server",
        auth=auth_provider,
        middleware=[AuthMiddleware(auth=require_auth)]
    )
    
    @mcp_middleware.tool
    def middleware_protected_tool() -> str:
        """Middleware-protected: filtered from list AND blocked from execution."""
        return "This tool is fully protected by middleware"
    
    print("✅ Component vs middleware example created")
    print("Component-level auth:")
    print("  - Filters list responses: Yes")
    print("  - Blocks execution: No")
    print("Middleware enforcement:")
    print("  - Filters list responses: Yes")
    print("  - Blocks execution: Yes (raises AuthorizationError)")
    
    return mcp_component, mcp_middleware


def example_comprehensive_server():
    """Example: Comprehensive server with all auth patterns."""
    
    well_known_url = os.getenv(
        "DESCOPE_MCP_WELL_KNOWN_URL",
        "https://api.descope.com/your-project-id/.well-known/openid-configuration"
    )
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    
    auth_provider = DescopeProvider(
        config_url=well_known_url,
        base_url=server_url,
    )
    
    # Custom auth checks
    def require_premium(ctx: AuthContext) -> bool:
        if ctx.token is None:
            return False
        return ctx.token.claims.get("premium", False) is True
    
    # Create server with tag-based middleware
    mcp = FastMCP(
        name="Comprehensive Descope Server",
        auth=auth_provider,
        middleware=[
            AuthMiddleware(auth=restrict_tag("admin", scopes=["admin"])),
            AuthMiddleware(auth=restrict_tag("write", scopes=["write"])),
        ]
    )
    
    # Public tools
    @mcp.tool
    def public_info() -> str:
        """Public information available to everyone."""
        return "Public information"
    
    @mcp.tool
    def health_check() -> str:
        """Health check endpoint."""
        return "Server is healthy"
    
    # Authenticated tools
    @mcp.tool(auth=require_auth)
    def user_info() -> dict:
        """Get current user information."""
        token = get_access_token()
        return {
            "authenticated": True,
            "client_id": token.client_id if token else None,
            "scopes": token.scopes if token else [],
        }
    
    # Scope-based tools
    @mcp.tool(auth=require_scopes("read"))
    def read_data(id: str) -> str:
        """Read data. Requires 'read' scope."""
        return f"Data for {id}"
    
    @mcp.tool(auth=require_scopes("write"))
    def write_data(id: str, data: str) -> str:
        """Write data. Requires 'write' scope."""
        return f"Data written for {id}: {data}"
    
    @mcp.tool(auth=require_scopes("read", "write"))
    def read_write_data(id: str, data: str) -> str:
        """Read and write data. Requires both scopes."""
        return f"Data read and written for {id}: {data}"
    
    # Tag-based tools (enforced by middleware)
    @mcp.tool(tags={"admin"})
    def admin_delete(id: str) -> str:
        """Delete data. Tagged 'admin', requires 'admin' scope."""
        return f"Deleted {id}"
    
    @mcp.tool(tags={"write"})
    def admin_update(id: str, data: str) -> str:
        """Update data. Tagged 'write', requires 'write' scope."""
        return f"Updated {id} with {data}"
    
    # Custom check tools
    @mcp.tool(auth=require_premium)
    def premium_content() -> str:
        """Premium content. Requires premium claim."""
        return "Premium content unlocked"
    
    # Combined auth tools
    @mcp.tool(auth=[require_auth, require_scopes("admin")])
    def secure_admin_action() -> str:
        """Secure admin action. Requires auth AND admin scope."""
        return "Secure admin action completed"
    
    print("✅ Comprehensive server example created")
    print("Includes:")
    print("  - Public tools (no auth)")
    print("  - Authenticated tools (require_auth)")
    print("  - Scope-based tools (require_scopes)")
    print("  - Tag-based tools (restrict_tag middleware)")
    print("  - Custom check tools (premium user)")
    print("  - Combined auth tools")
    
    return mcp


def main():
    """Run all examples."""
    print("🚀 FastMCP Descope Authentication Examples")
    print("=" * 60)
    
    print("\n1. Basic Authentication:")
    print("-" * 60)
    example_basic_auth()
    
    print("\n2. Scope-Based Authorization:")
    print("-" * 60)
    example_scope_based_auth()
    
    print("\n3. Tag-Based Authorization:")
    print("-" * 60)
    example_tag_based_auth()
    
    print("\n4. Custom Auth Checks:")
    print("-" * 60)
    example_custom_auth_checks()
    
    print("\n5. Token Access in Tools:")
    print("-" * 60)
    example_token_access_in_tools()
    
    print("\n6. Component-Level vs Middleware:")
    print("-" * 60)
    example_component_level_vs_middleware()
    
    print("\n7. Comprehensive Server:")
    print("-" * 60)
    example_comprehensive_server()
    
    print("\n✨ All examples completed!")
    print("\nNote: Set DESCOPE_MCP_WELL_KNOWN_URL and SERVER_URL environment variables")
    print("      before running these examples in production.")


if __name__ == "__main__":
    main()
