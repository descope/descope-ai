#!/usr/bin/env python3
"""Example: MCP server using tenant tokens fetched with management key.

This example demonstrates:
1. An MCP server that requires tenant-level access (not user-specific)
2. Fetching tenant tokens using management key (no user session required)
3. Using tenant tokens to access tenant resources
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

example_dir = Path(__file__).parent
root_dir = example_dir.parent.parent
sdk_src = root_dir / "src"
if sdk_src.exists():
    sys.path.insert(0, str(sdk_src))

from mcp.server import FastMCP

from descope_mcp import DescopeMCP, fetch_tenant_token, fetch_tenant_token_by_scopes
from descope_mcp.types import DescopeConfig


def example_tenant_token_mcp_server():
    """Example: MCP server using tenant tokens."""

    # Initialize SDK - management key is required for tenant token operations
    DescopeMCP(
        well_known_url=os.getenv(
            "DESCOPE_MCP_WELL_KNOWN_URL",
            "https://api.descope.com/your-project-id/.well-known/openid-configuration",
        ),
        management_key=os.getenv("DESCOPE_MANAGEMENT_KEY", ""),
        mcp_server_url=os.getenv("MCP_SERVER_URL", "https://your-mcp-server.com"),
    )

    # Outbound app ID configured in Descope for tenant access
    TENANT_APP_ID = os.getenv("TENANT_APP_ID", "slack-workspace")
    TENANT_ID = os.getenv("TENANT_ID", "tenant-123")

    mcp = FastMCP("tenant-token-mcp-server")

    @mcp.tool()
    async def get_tenant_token(
        app_id: str = TENANT_APP_ID,
        tenant_id: str = TENANT_ID,
        scopes: Optional[list] = None,
    ) -> str:
        """Get tenant token using management key.

        No user session required - uses management key for tenant-level access.
        """
        try:
            config = DescopeConfig(
                well_known_url=os.getenv("DESCOPE_MCP_WELL_KNOWN_URL", ""),
                management_key=os.getenv("DESCOPE_MANAGEMENT_KEY", ""),
            )

            if scopes:
                token_response = await fetch_tenant_token_by_scopes(
                    config=config, app_id=app_id, tenant_id=tenant_id, scopes=scopes
                )
            else:
                token_response = await fetch_tenant_token(
                    config=config, app_id=app_id, tenant_id=tenant_id
                )

            # Parse token from JSON response
            token_data = json.loads(token_response)
            token = token_data.get("token", "")

            return json.dumps(
                {
                    "status": "success",
                    "tenant_id": tenant_id,
                    "app_id": app_id,
                    "token": token,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e), "type": type(e).__name__})

    @mcp.tool()
    async def get_slack_workspace_info() -> str:
        """Get Slack workspace information using tenant token."""
        try:
            config = DescopeConfig(
                well_known_url=os.getenv("DESCOPE_MCP_WELL_KNOWN_URL", ""),
                management_key=os.getenv("DESCOPE_MANAGEMENT_KEY", ""),
            )

            token_response = await fetch_tenant_token(
                config=config, app_id=TENANT_APP_ID, tenant_id=TENANT_ID
            )

            token_data = json.loads(token_response)
            token = token_data.get("token", "")

            if not token:
                return json.dumps({"error": "Failed to get tenant token"})

            return json.dumps(
                {"status": "success", "tenant_id": TENANT_ID, "token": token}
            )
        except Exception as e:
            return json.dumps({"error": str(e), "type": type(e).__name__})

    return mcp


def main():
    """Run the example."""
    example_tenant_token_mcp_server()


if __name__ == "__main__":
    main()
