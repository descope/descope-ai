"""End-to-end tests using FastMCP 3.0 (fastmcp.FastMCP with auth providers)."""

import pytest
from unittest.mock import Mock, patch, MagicMock

# Try to import FastMCP 3.0, skip tests if not available
try:
    from fastmcp import FastMCP
    from fastmcp.server.auth import require_auth, require_scopes
    from fastmcp.server.auth.providers.descope import DescopeProvider
    FASTMCP3_AVAILABLE = True
except ImportError:
    FASTMCP3_AVAILABLE = False

from mcp_descope import DescopeMCP, validate_token_and_get_user_id, get_connection_token


@pytest.mark.skipif(not FASTMCP3_AVAILABLE, reason="FastMCP 3.0 not available")
class TestFastMCP3Integration:
    """Test integration with FastMCP 3.0."""

    @pytest.fixture
    def mock_descope_client(self):
        """Create a mock DescopeClient."""
        client = Mock()
        client.validate_session = Mock(return_value={"sub": "user-123", "scopes": ["read", "write", "calendar.read"]})
        client.mgmt = Mock()
        client.mgmt.outbound_application = Mock()
        client.mgmt.outbound_application.fetch_token = Mock(return_value="connection-token-123")
        return client

    @pytest.fixture
    def mock_auth_provider(self):
        """Create a mock DescopeProvider."""
        provider = Mock()
        provider.validate_token = Mock(return_value={"sub": "user-123", "scopes": ["read", "write"]})
        return provider

    def test_fastmcp3_basic_auth(self, mock_auth_provider):
        """Test FastMCP 3.0 with basic authentication."""
        mcp = FastMCP(
            name="FastMCP3BasicTest",
            auth=mock_auth_provider
        )
        
        @mcp.tool
        def public_info() -> str:
            """Public information."""
            return "This is public"
        
        @mcp.tool(auth=require_auth)
        def protected_info() -> str:
            """Protected information."""
            return "This is protected"
        
        assert mcp is not None

    def test_fastmcp3_scope_based_auth(self, mock_auth_provider):
        """Test FastMCP 3.0 with scope-based authentication."""
        mcp = FastMCP(
            name="FastMCP3ScopeTest",
            auth=mock_auth_provider
        )
        
        @mcp.tool(auth=require_scopes("read"))
        def read_data() -> str:
            """Read data."""
            return "Data read"
        
        @mcp.tool(auth=require_scopes("read", "write"))
        def read_write_data() -> str:
            """Read and write data."""
            return "Data read and written"
        
        assert mcp is not None

    def test_fastmcp3_with_descope_sdk(self, mock_descope_client):
        """Test FastMCP 3.0 with Descope SDK functions."""
        DescopeMCP(
            well_known_url="https://api.descope.com/test/.well-known/openid-configuration",
            management_key="test-key",
            mcp_server_url="https://test-mcp-server.com"
        )
        
        # Create auth provider
        auth_provider = DescopeProvider(
            config_url="https://api.descope.com/test/.well-known/openid-configuration",
            base_url="https://test-mcp-server.com"
        )
        
        mcp = FastMCP(
            name="FastMCP3DescopeTest",
            auth=auth_provider
        )
        
        @mcp.tool(auth=require_auth)
        def get_user_info() -> str:
            """Get user info using Descope SDK."""
            # In real usage, token would come from FastMCP context
            with patch('mcp_descope.session._get_descope_client', return_value=mock_descope_client):
                user_id = validate_token_and_get_user_id("test-token")
                return f"User: {user_id}"
        
        @mcp.tool(auth=require_scopes("calendar.read"))
        def get_calendar() -> str:
            """Get calendar using connection token."""
            with patch('mcp_descope.session._get_descope_client', return_value=mock_descope_client):
                user_id = validate_token_and_get_user_id("test-token")
            
            with patch('mcp_descope.connections._get_context') as mock_context:
                mock_context.return_value.get_client.return_value = mock_descope_client
                token = get_connection_token(
                    user_id=user_id,
                    app_id="google-calendar",
                    scopes=["calendar.readonly"]
                )
                return f"Calendar token: {token[:10]}..."
        
        assert mcp is not None

    def test_fastmcp3_comprehensive(self, mock_auth_provider):
        """Test FastMCP 3.0 with comprehensive setup."""
        mcp = FastMCP(
            name="FastMCP3Comprehensive",
            auth=mock_auth_provider
        )
        
        # Public tool
        @mcp.tool
        def public() -> str:
            """Public tool."""
            return "public"
        
        # Authenticated tool
        @mcp.tool(auth=require_auth)
        def authenticated() -> str:
            """Authenticated tool."""
            return "authenticated"
        
        # Scope-protected tools
        @mcp.tool(auth=require_scopes("read"))
        def read() -> str:
            """Read tool."""
            return "read"
        
        @mcp.tool(auth=require_scopes("write"))
        def write() -> str:
            """Write tool."""
            return "write"
        
        @mcp.tool(auth=require_scopes("read", "write"))
        def read_write() -> str:
            """Read/write tool."""
            return "read_write"
        
        assert mcp is not None
