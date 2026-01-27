"""Basic tests for the MCP Descope SDK."""

import pytest
from pydantic import ValidationError

from mcp_descope import (
    DescopeConfig,
    TokenResponse,
    ErrorResponse,
    UserTokenRequest,
    TenantTokenRequest,
)


class TestConfig:
    """Test configuration models."""

    def test_descope_config_valid(self):
        """Test valid DescopeConfig creation."""
        config = DescopeConfig(
            project_id="test-project",
            management_key="test-key",
            base_url="https://api.descope.com",
        )
        assert config.project_id == "test-project"
        assert config.management_key == "test-key"
        assert config.base_url == "https://api.descope.com"

    def test_descope_config_minimal(self):
        """Test minimal DescopeConfig creation."""
        config = DescopeConfig(
            project_id="test-project",
            management_key="test-key",
        )
        assert config.project_id == "test-project"
        assert config.management_key == "test-key"
        assert config.base_url is None

    def test_descope_config_invalid(self):
        """Test invalid DescopeConfig creation."""
        with pytest.raises(ValidationError):
            DescopeConfig(
                project_id="",  # Empty project_id should fail
                management_key="test-key",
            )


class TestTokenResponse:
    """Test token response models."""

    def test_token_response_valid(self):
        """Test valid TokenResponse creation."""
        response = TokenResponse(
            token="test-token",
            expires_at=1234567890,
            scopes=["read", "write"],
            metadata={"key": "value"},
        )
        assert response.token == "test-token"
        assert response.expires_at == 1234567890
        assert response.scopes == ["read", "write"]
        assert response.metadata == {"key": "value"}

    def test_token_response_minimal(self):
        """Test minimal TokenResponse creation."""
        response = TokenResponse(token="test-token")
        assert response.token == "test-token"
        assert response.expires_at is None
        assert response.scopes is None
        assert response.metadata is None

    def test_token_response_invalid(self):
        """Test invalid TokenResponse creation."""
        with pytest.raises(ValidationError):
            TokenResponse(token="")  # Empty token should fail


class TestErrorResponse:
    """Test error response models."""

    def test_error_response_valid(self):
        """Test valid ErrorResponse creation."""
        error = ErrorResponse(
            error="Test error message",
            code="TEST_ERROR",
            details={"key": "value"},
        )
        assert error.error == "Test error message"
        assert error.code == "TEST_ERROR"
        assert error.details == {"key": "value"}

    def test_error_response_minimal(self):
        """Test minimal ErrorResponse creation."""
        error = ErrorResponse(error="Test error message")
        assert error.error == "Test error message"
        assert error.code is None
        assert error.details is None


class TestRequestModels:
    """Test request models."""

    def test_user_token_request_valid(self):
        """Test valid UserTokenRequest creation."""
        request = UserTokenRequest(
            app_id="test-app",
            user_id="test-user",
            scopes=["read", "write"],
            options={"refreshToken": True},
            tenant_id="test-tenant",
        )
        assert request.app_id == "test-app"
        assert request.user_id == "test-user"
        assert request.scopes == ["read", "write"]
        assert request.options == {"refreshToken": True}
        assert request.tenant_id == "test-tenant"

    def test_tenant_token_request_valid(self):
        """Test valid TenantTokenRequest creation."""
        request = TenantTokenRequest(
            app_id="test-app",
            tenant_id="test-tenant",
            scopes=["read", "write"],
            options={"refreshToken": True},
        )
        assert request.app_id == "test-app"
        assert request.tenant_id == "test-tenant"
        assert request.scopes == ["read", "write"]
        assert request.options == {"refreshToken": True}


class TestImports:
    """Test that all imports work correctly."""

    def test_main_imports(self):
        """Test that main module imports work."""
        from mcp_descope import (
            DescopeMCPClient,
            DescopeMCPServer,
            create_default_client,
            create_server,
        )
        
        # Just test that imports don't raise exceptions
        assert DescopeMCPClient is not None
        assert DescopeMCPServer is not None
        assert create_default_client is not None
        assert create_server is not None


if __name__ == "__main__":
    pytest.main([__file__]) 