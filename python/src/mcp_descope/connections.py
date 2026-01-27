"""Connection token functions for Descope MCP SDK.

This module provides functions for retrieving OAuth access tokens for
outbound applications (connections) configured in Descope.
"""

import logging
from typing import Any, Dict, List, Optional

from descope import DescopeClient

# Import context lazily to avoid circular dependency
def _get_context():
    from .descope_mcp import _context
    return _context

logger = logging.getLogger(__name__)


def get_connection_token(
    user_id: str,
    app_id: str,
    scopes: Optional[List[str]] = None,
    tenant_id: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    descope_client: Optional[DescopeClient] = None,
    project_id: Optional[str] = None,
    management_key: Optional[str] = None,
) -> str:
    """Get connection token from Descope for a user.
    
    This function retrieves an OAuth access token for a connection/outbound application
    (like Google Calendar, Slack, etc.) that was configured in Descope.
    The token is fetched using the user's ID from the validated MCP server token.
    
    You can authenticate either by:
    1. Passing a DescopeClient instance (uses its configured management key)
    2. Passing project_id and management_key directly (uses format PROJECT_ID:MANAGEMENT_KEY)
    
    Args:
        user_id: User ID from the validated MCP server token
        app_id: Connection/outbound application ID configured in Descope
        scopes: Optional scopes to request (if None, uses default scopes)
        tenant_id: Optional tenant ID for tenant-level tokens
        options: Optional additional options (e.g., {"refreshToken": True})
        descope_client: Optional DescopeClient instance (if not provided, project_id and management_key required)
        project_id: Optional project ID (required if descope_client not provided)
        management_key: Optional management key (required if descope_client not provided)
        
    Returns:
        Connection access token string
        
    Raises:
        ValueError: If neither descope_client nor (project_id and management_key) are provided
        Exception: If token retrieval fails
        
    Example:
        ```python
        from mcp_descope import get_connection_token
        
        # Using DescopeClient
        google_token = get_connection_token(
            user_id="user-123",
            app_id="google-calendar",
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
            descope_client=client
        )
        
        # Using project_id and management_key directly
        google_token = get_connection_token(
            user_id="user-123",
            app_id="google-calendar",
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
            project_id="P123456",
            management_key="your-management-key"
        )
        ```
    """
    try:
        # Determine which authentication method to use
        if descope_client:
            # Use provided DescopeClient
            client = descope_client
        elif project_id and management_key:
            # Create DescopeClient with provided credentials
            client = DescopeClient(
                project_id=project_id,
                management_key=management_key,
            )
        else:
            # Try to use global context
            context = _get_context()
            client = context.get_client()
            if client is None:
                raise ValueError(
                    "No authentication method provided. "
                    "Either call DescopeMCP() first, pass descope_client, or provide project_id and management_key."
                )
        
        # Fetch token using Descope SDK
        if scopes:
            token = client.mgmt.outbound_application.fetch_token_by_scopes(
                app_id=app_id,
                user_id=user_id,
                scopes=scopes,
                options=options or {},
                tenant_id=tenant_id
            )
        else:
            token = client.mgmt.outbound_application.fetch_token(
                app_id=app_id,
                user_id=user_id,
                tenant_id=tenant_id,
                options=options or {}
            )
        return token
    except Exception as e:
        raise Exception(f"Failed to get connection token: {e}")
