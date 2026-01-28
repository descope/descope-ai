"""Session validation functions for Descope MCP SDK.

This module provides functions for validating MCP server access tokens
and extracting user information from validated tokens.
"""

import logging
from typing import Optional

from descope import DescopeClient

# Import context lazily to avoid circular dependency
def _get_context():
    from .descope_mcp import _context
    return _context

logger = logging.getLogger(__name__)


def validate_token_and_get_user_id(
    access_token: str,
    descope_client: Optional[DescopeClient] = None,
    audience: Optional[str] = None
) -> str:
    """Validate MCP server access token and extract user ID using Descope SDK.
    
    This function validates a Descope access token using the Descope Python SDK's
    validate_session method and extracts the user ID from the validation result.
    It validates the audience claim to ensure the token is intended for this MCP server.
    Use this to authenticate requests and get the user identifier for fetching
    connection tokens.
    
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
            management_key="...",
            mcp_server_url="https://your-mcp-server.com"  # Used as audience
        )
        
        # Use without passing client - audience is automatically validated
        user_id = validate_token_and_get_user_id(access_token)
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
    except Exception as e:
        # If validate_session fails, provide helpful error message
        error_msg = str(e)
        if "invalid" in error_msg.lower() or "expired" in error_msg.lower() or "audience" in error_msg.lower():
            raise ValueError(f"Token validation failed: {error_msg}")
        raise Exception(f"Token validation failed: {error_msg}")
