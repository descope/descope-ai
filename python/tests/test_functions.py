"""End-to-end tests for SDK functions directly (no MCP server)."""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from mcp_descope import (
    DescopeMCP,
    validate_token_and_get_user_id,
    get_connection_token,
    fetch_tenant_token,
    fetch_tenant_token_by_scopes,
    DescopeConfig,
)


class TestDirectFunctions:
    """Test SDK functions directly without MCP server."""

    @pytest.fixture
    def mock_descope_client(self):
        """Create a mock DescopeClient."""
        client = Mock()
        client.validate_session = Mock(return_value={"sub": "user-123"})
        client.mgmt = Mock()
        client.mgmt.outbound_application = Mock()
        client.mgmt.outbound_application.fetch_token = Mock(return_value="connection-token-123")
        client.mgmt.outbound_application.fetch_token_by_scopes = Mock(return_value="connection-token-123")
        client.mgmt.outbound_application.fetch_tenant_token = Mock(return_value="tenant-token-123")
        client.mgmt.outbound_application.fetch_tenant_token_by_scopes = Mock(return_value="tenant-token-123")
        return client

    def test_validate_token_and_get_user_id(self, mock_descope_client):
        """Test token validation function."""
        DescopeMCP(
            well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
            mcp_server_url="https://test-mcp-server.com"
        )
        
        with patch('mcp_descope.session._get_descope_client', return_value=mock_descope_client):
            user_id = validate_token_and_get_user_id("test-token")
            assert user_id == "user-123"
            mock_descope_client.validate_session.assert_called_once()

    def test_get_connection_token(self, mock_descope_client):
        """Test connection token retrieval."""
        DescopeMCP(
            well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
            management_key="test-key"
        )
        
        with patch('mcp_descope.connections._get_context') as mock_context:
            mock_context.return_value.get_client.return_value = mock_descope_client
            
            token = get_connection_token(
                user_id="user-123",
                app_id="google-calendar",
                scopes=["calendar.readonly"]
            )
            
            assert token == "connection-token-123"
            mock_descope_client.mgmt.outbound_application.fetch_token_by_scopes.assert_called_once()

    def test_fetch_tenant_token(self, mock_descope_client):
        """Test tenant token fetching."""
        config = DescopeConfig(
            well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
            management_key="test-key"
        )
        
        with patch('mcp_descope.descope_mcp._get_descope_client', return_value=mock_descope_client):
            import asyncio
            result = asyncio.run(fetch_tenant_token(
                config=config,
                app_id="slack-workspace",
                tenant_id="tenant-123"
            ))
            
            # Result is JSON string
            import json
            token_data = json.loads(result)
            assert "token" in token_data

    def test_fetch_tenant_token_by_scopes(self, mock_descope_client):
        """Test tenant token fetching with scopes."""
        config = DescopeConfig(
            well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
            management_key="test-key"
        )
        
        with patch('mcp_descope.descope_mcp._get_descope_client', return_value=mock_descope_client):
            import asyncio
            result = asyncio.run(fetch_tenant_token_by_scopes(
                config=config,
                app_id="slack-workspace",
                tenant_id="tenant-123",
                scopes=["channels:read"]
            ))
            
            import json
            token_data = json.loads(result)
            assert "token" in token_data

    def test_descope_mcp_class_based(self, mock_descope_client):
        """Test class-based API."""
        with patch('mcp_descope.descope_mcp._get_descope_client', return_value=mock_descope_client):
            client = DescopeMCP(
                well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
                management_key="test-key",
                mcp_server_url="https://test-mcp-server.com"
            )
            
            user_id = client.validate_token_and_get_user_id("test-token")
            assert user_id == "user-123"
            
            token = client.get_connection_token(
                user_id="user-123",
                app_id="google-calendar"
            )
            assert token == "connection-token-123"
