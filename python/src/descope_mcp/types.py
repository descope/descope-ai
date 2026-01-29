"""Type definitions for MCP Descope SDK."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class DescopeConfig(BaseModel):
    """Configuration for Descope MCP server."""

    well_known_url: str = Field(..., description="MCP server well-known URL")
    management_key: Optional[str] = Field(
        None, description="Descope management API key (optional)"
    )


class TokenRequest(BaseModel):
    """Base token request model."""

    app_id: str = Field(..., description="Application ID")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")


class UserTokenRequest(TokenRequest):
    """Request for user token operations."""

    user_id: str = Field(..., description="User ID")
    scopes: Optional[List[str]] = Field(None, description="Required scopes")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional options")


class TenantTokenRequest(TokenRequest):
    """Request for tenant token operations."""

    scopes: Optional[List[str]] = Field(None, description="Required scopes")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional options")


class TokenResponse(BaseModel):
    """Response containing token information."""

    token: str = Field(..., description="The fetched token")
    expires_at: Optional[int] = Field(None, description="Token expiration timestamp")
    scopes: Optional[List[str]] = Field(None, description="Token scopes")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
