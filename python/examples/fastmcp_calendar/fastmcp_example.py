#!/usr/bin/env python3
"""FastMCP integration example with Descope authentication and connection tokens.

This example demonstrates:
1. Protecting MCP tools with Descope session validation and scope validation
2. Getting connection tokens from Descope when required by tools
3. Using connection tokens to call external APIs (Google Calendar)
"""

import os
import sys
from pathlib import Path
from typing import Optional
import json

example_dir = Path(__file__).parent
root_dir = example_dir.parent.parent
sdk_src = root_dir / "src"
if sdk_src.exists():
    sys.path.insert(0, str(sdk_src))

from mcp.server import FastMCP
from mcp_descope import (
    DescopeMCP,
    validate_token_and_get_user_id,
    get_connection_token,
    create_auth_check,
)
try:
    import httpx
except ImportError:
    httpx = None


def example_google_calendar_tool():
    """Example: Google Calendar tool with Descope auth and connection token."""
    
    DescopeMCP(
        well_known_url=os.getenv(
            "DESCOPE_MCP_WELL_KNOWN_URL",
            "https://api.descope.com/your-project-id/.well-known/openid-configuration"
        ),
        mcp_server_url=os.getenv("MCP_SERVER_URL", "https://your-mcp-server.com")
    )
    
    GOOGLE_CALENDAR_APP_ID = os.getenv("GOOGLE_CALENDAR_APP_ID", "google-calendar")
    mcp = FastMCP("descope-calendar-server")
    calendar_read_check = create_auth_check(["calendar.read"])
    
    @mcp.tool(auth=calendar_read_check)
    async def get_calendar_events(
        max_results: int = 10,
        time_min: Optional[str] = None
    ) -> str:
        """Get Google Calendar events for the authenticated user."""
        raise NotImplementedError("Requires FastMCP v3.0.0 auth integration")
    
    @mcp.tool()
    async def get_calendar_events_simple(
        mcp_access_token: str,
        max_results: int = 10
    ) -> str:
        """Get Google Calendar events."""
        try:
            user_id = validate_token_and_get_user_id(mcp_access_token)
            
            # Get connection token using MCP access token (default, enables policy enforcement)
            # Falls back to management key if access token method fails
            google_token = get_connection_token(
                user_id=user_id,
                app_id=GOOGLE_CALENDAR_APP_ID,
                scopes=["https://www.googleapis.com/auth/calendar"],
                access_token=mcp_access_token  # Uses access token by default
            )
            
            if not httpx:
                raise ImportError("httpx required for API calls. Install with: pip install httpx")
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {google_token}",
                    "Accept": "application/json"
                }
                
                params = {
                    "maxResults": max_results,
                    "singleEvents": True,
                    "orderBy": "startTime"
                }
                
                response = await client.get(
                    "https://www.googleapis.com/calendar/v3/calendars/primary/events",
                    headers=headers,
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                
                events = response.json()
                formatted_events = []
                for item in events.get("items", [])[:max_results]:
                    formatted_events.append({
                        "id": item.get("id"),
                        "summary": item.get("summary", "No title"),
                        "start": item.get("start", {}).get("dateTime") or item.get("start", {}).get("date"),
                        "end": item.get("end", {}).get("dateTime") or item.get("end", {}).get("date"),
                        "location": item.get("location"),
                        "description": item.get("description", "")[:100] if item.get("description") else None,
                    })
                
                return json.dumps({
                    "status": "success",
                    "user_id": user_id,
                    "events_count": len(formatted_events),
                    "events": formatted_events
                }, indent=2)
                
        except httpx.HTTPStatusError as e:
            return json.dumps({
                "error": f"Google Calendar API error: {e.response.status_code}",
                "details": e.response.text[:200]
            })
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "type": type(e).__name__
            })
    
    @mcp.tool(auth=create_auth_check(["calendar.read"]))
    async def list_calendars() -> str:
        """List user's Google Calendars."""
        return json.dumps({"message": "This tool requires 'calendar.read' scope"})
    
    return mcp


def example_protected_tools():
    """Example: Various protected tools with different scope requirements."""
    
    DescopeMCP(
        well_known_url=os.getenv("DESCOPE_MCP_WELL_KNOWN_URL", ""),
    )
    
    mcp = FastMCP("descope-protected-server")
    
    @mcp.tool()
    def public_info() -> str:
        """Public information."""
        return "This is public information"
    
    @mcp.tool(auth=create_auth_check([]))
    def authenticated_info() -> str:
        """Requires authentication."""
        return "Authenticated user information"
    
    @mcp.tool(auth=create_auth_check(["read"]))
    def read_data() -> str:
        """Requires 'read' scope."""
        return "Data read successfully"
    
    @mcp.tool(auth=create_auth_check(["read", "write"]))
    def read_write_data() -> str:
        """Requires 'read' and 'write' scopes."""
        return "Data read and written successfully"
    
    return mcp




def main():
    """Run all examples."""
    example_google_calendar_tool()
    example_protected_tools()


if __name__ == "__main__":
    main()
