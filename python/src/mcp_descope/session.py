"""Session validation functions for Descope MCP SDK.

This module provides functions for validating MCP server access tokens
and extracting user information from validated tokens.
"""

import logging
from typing import Dict, Optional, Any

from descope import DescopeClient

# Import context lazily to avoid circular dependency
def _get_context():
    from .descope_mcp import _context
    return _context

logger = logging.getLogger(__name__)


def validate_token(
    access_token: str,
    descope_client: Optional[DescopeClient] = None,
    audience: Optional[str] = None
) -> Dict[str, Any]:
    """Validate MCP server access token and return full validation result.
    
    This function validates a Descope access token using the Descope Python SDK's
    validate_session method and returns the complete validation result, including
    user ID, tenant information, scopes, and other token claims.
    
    Args:
        access_token: MCP server access token from the request
        descope_client: Optional Descope client instance (uses global context if not provided)
        audience: Optional audience claim to validate (uses MCP server URL from context if not provided)
        
    Returns:
        Dictionary containing the full validation result from Descope, including:
        - sub/userId: User ID
        - tenant: Tenant information (if available)
        - scopes: Token scopes
        - Other JWT claims and user information
        
    Raises:
        ValueError: If token is invalid or no client available
        Exception: If token validation fails
        
    Example:
        ```python
        from mcp_descope import DescopeMCP, validate_token
        
        # Initialize once
        DescopeMCP(
            well_known_url="...",
            mcp_server_url="https://your-mcp-server.com"
        )
        
        # Get full validation result
        result = validate_token(access_token)
        user_id = result.get('sub') or result.get('userId')
        tenant_id = result.get('tenant') or result.get('tenantId')
        scopes = result.get('scopes', [])
        ```
    """
    # Use provided client or global context
    if descope_client is None:
        context = _get_context()
        descope_client = context.get_client()
        if descope_client is None:
            raise ValueError(
                "No Descope client available. "
                "Either call DescopeMCP() first or pass descope_client parameter."
            )
    
    # Use provided audience or get from global context
    if audience is None:
        context = _get_context()
        audience = context.get_mcp_server_url()
    
    # Ensure audience is always validated for security
    if not audience:
        raise ValueError(
            "MCP server URL (audience) is required for token validation. "
            "Call DescopeMCP() with mcp_server_url parameter to set the audience."
        )
    
    try:
        # Use Descope SDK's validate_session method
        # This properly validates the token signature, expiration, and audience claim
        # The audience parameter validates the 'aud' claim in the JWT token
        # This ensures tokens are only accepted if they were issued for this specific MCP server
        validation_result = descope_client.validate_session(
            session_token=access_token,
            audience=audience
        )
        
        # Return the full validation result
        # This includes user ID, tenant info, scopes, and all other token claims
        return validation_result
    except Exception as e:
        # If validate_session fails, provide helpful error message
        error_msg = str(e)
        if "invalid" in error_msg.lower() or "expired" in error_msg.lower() or "audience" in error_msg.lower():
            raise ValueError(f"Token validation failed: {error_msg}")
        raise Exception(f"Token validation failed: {error_msg}")


def validate_token_and_get_user_id(
    access_token: str,
    descope_client: Optional[DescopeClient] = None,
    audience: Optional[str] = None
) -> str:
    """Validate MCP server access token and extract user ID using Descope SDK.
    
    This is a convenience function that validates a token and returns just the user ID.
    For full token information (including tenant, scopes, etc.), use validate_token() instead.
    
    Args:
        access_token: MCP server access token from the request
        descope_client: Optional Descope client instance (uses global context if not provided)
        audience: Optional audience claim to validate (uses MCP server URL from context if not provided)
        
    Returns:
        User ID extracted from the validated token
        
    Raises:
        ValueError: If token is invalid or user ID not found, or if no client available
        Exception: If token validation fails
        
    Example:
        ```python
        from mcp_descope import DescopeMCP, validate_token_and_get_user_id
        
        # Initialize once
        DescopeMCP(
            well_known_url="...",
            mcp_server_url="https://your-mcp-server.com"
        )
        
        # Use without passing client - audience is automatically validated
        user_id = validate_token_and_get_user_id(access_token)
        ```
    """
    # Use the full validate_token function and extract user_id
    validation_result = validate_token(access_token, descope_client, audience)
    
    # Extract user ID from validation result
    # Descope's validate_session returns user information
    user_id = validation_result.get('sub') or validation_result.get('userId') or validation_result.get('user_id')
    
    # If not in top-level, check nested user object
    if not user_id and 'user' in validation_result:
        user_info = validation_result['user']
        user_id = user_info.get('userId') or user_info.get('id') or user_info.get('sub')
    
    if not user_id:
        raise ValueError("User ID not found in token validation result")
        
    return user_id
