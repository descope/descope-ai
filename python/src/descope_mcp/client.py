"""Client interface for Descope MCP server."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import CallToolRequest

from .types import DescopeConfig, ErrorResponse, TokenResponse

logger = logging.getLogger(__name__)


class DescopeMCPClient:
    """Client for interacting with Descope MCP server."""

    def __init__(self, server_command: List[str]):
        """Initialize the Descope MCP client.

        Args:
            server_command: Command to start the MCP server
        """
        self.server_command = server_command
        self.session: Optional[ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def connect(self):
        """Connect to the MCP server."""
        if self.session is not None:
            return

        read_stream, write_stream = await stdio_client(self.server_command)
        self.session = ClientSession(read_stream, write_stream)
        await self.session.initialize()

    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def fetch_user_token_by_scopes(
        self,
        app_id: str,
        user_id: str,
        scopes: List[str],
        options: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None,
    ) -> TokenResponse:
        """Fetch user token with specific scopes.

        Args:
            app_id: Application ID
            user_id: User ID
            scopes: Required scopes
            options: Additional options (e.g., refreshToken)
            tenant_id: Tenant ID (optional)

        Returns:
            Token response with the fetched token

        Raises:
            Exception: If the request fails
        """
        arguments = {
            "app_id": app_id,
            "user_id": user_id,
            "scopes": scopes,
        }

        if options:
            arguments["options"] = options
        if tenant_id:
            arguments["tenant_id"] = tenant_id

        result = await self._call_tool("fetch_user_token_by_scopes", arguments)
        return self._parse_token_response(result)

    async def fetch_user_token(
        self,
        app_id: str,
        user_id: str,
        tenant_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> TokenResponse:
        """Fetch latest user token.

        Args:
            app_id: Application ID
            user_id: User ID
            tenant_id: Tenant ID (optional)
            options: Additional options (e.g., forceRefresh)

        Returns:
            Token response with the fetched token

        Raises:
            Exception: If the request fails
        """
        arguments = {
            "app_id": app_id,
            "user_id": user_id,
        }

        if tenant_id:
            arguments["tenant_id"] = tenant_id
        if options:
            arguments["options"] = options

        result = await self._call_tool("fetch_user_token", arguments)
        return self._parse_token_response(result)

    async def fetch_tenant_token_by_scopes(
        self,
        app_id: str,
        tenant_id: str,
        scopes: List[str],
        options: Optional[Dict[str, Any]] = None,
    ) -> TokenResponse:
        """Fetch tenant token with specific scopes.

        Args:
            app_id: Application ID
            tenant_id: Tenant ID
            scopes: Required scopes
            options: Additional options (e.g., refreshToken)

        Returns:
            Token response with the fetched token

        Raises:
            Exception: If the request fails
        """
        arguments = {
            "app_id": app_id,
            "tenant_id": tenant_id,
            "scopes": scopes,
        }

        if options:
            arguments["options"] = options

        result = await self._call_tool("fetch_tenant_token_by_scopes", arguments)
        return self._parse_token_response(result)

    async def fetch_tenant_token(
        self,
        app_id: str,
        tenant_id: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> TokenResponse:
        """Fetch latest tenant token.

        Args:
            app_id: Application ID
            tenant_id: Tenant ID
            options: Additional options (e.g., forceRefresh)

        Returns:
            Token response with the fetched token

        Raises:
            Exception: If the request fails
        """
        arguments = {
            "app_id": app_id,
            "tenant_id": tenant_id,
        }

        if options:
            arguments["options"] = options

        result = await self._call_tool("fetch_tenant_token", arguments)
        return self._parse_token_response(result)

    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result as JSON string

        Raises:
            Exception: If the tool call fails
        """
        if self.session is None:
            raise RuntimeError("Client not connected. Call connect() first.")

        request = CallToolRequest(name=name, arguments=arguments)
        result = await self.session.call_tool(request)

        if not result.content:
            raise Exception("No content in tool result")

        # Extract text content
        text_content = None
        for content in result.content:
            if content.get("type") == "text":
                text_content = content.get("text", "")
                break

        if text_content is None:
            raise Exception("No text content in tool result")

        return text_content

    def _parse_token_response(self, json_response: str) -> TokenResponse:
        """Parse token response from JSON.

        Args:
            json_response: JSON response string

        Returns:
            Parsed token response

        Raises:
            Exception: If parsing fails or response indicates error
        """
        try:
            data = json.loads(json_response)

            # Check if it's an error response
            if "error" in data:
                error_response = ErrorResponse(**data)
                raise Exception(f"Tool call failed: {error_response.error}")

            # Parse as token response
            return TokenResponse(**data)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {e}")
        except Exception as e:
            if "Tool call failed" not in str(e):
                raise Exception(f"Failed to parse token response: {e}")
            raise


def create_client(server_command: List[str]) -> DescopeMCPClient:
    """Create a Descope MCP client instance.

    Args:
        server_command: Command to start the MCP server

    Returns:
        Configured Descope MCP client
    """
    return DescopeMCPClient(server_command)


# Convenience function for creating client with default server command
def create_default_client() -> DescopeMCPClient:
    """Create a client with default server command.

    Returns:
        Configured Descope MCP client
    """
    return create_client(["python", "-m", "descope_mcp.server"])


# Example usage functions
async def example_usage():
    """Example usage of the Descope MCP client."""
    # Create client
    client = create_default_client()

    try:
        async with client:
            # Fetch user token with scopes
            user_token = await client.fetch_user_token_by_scopes(
                app_id="my-app-id",
                user_id="user-id",
                scopes=["read", "write"],
                options={"refreshToken": True},
                tenant_id="tenant-id",
            )
            print(f"User token: {user_token.token}")

            # Fetch latest user token
            latest_user_token = await client.fetch_user_token(
                app_id="my-app-id",
                user_id="user-id",
                tenant_id="tenant-id",
                options={"forceRefresh": True},
            )
            print(f"Latest user token: {latest_user_token.token}")

            # Fetch tenant token with scopes
            tenant_token = await client.fetch_tenant_token_by_scopes(
                app_id="my-app-id",
                tenant_id="tenant-id",
                scopes=["read", "write"],
                options={"refreshToken": True},
            )
            print(f"Tenant token: {tenant_token.token}")

            # Fetch latest tenant token
            latest_tenant_token = await client.fetch_tenant_token(
                app_id="my-app-id",
                tenant_id="tenant-id",
                options={"forceRefresh": True},
            )
            print(f"Latest tenant token: {latest_tenant_token.token}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(example_usage())
