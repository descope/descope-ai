# FastMCP Calendar Example

This example demonstrates how to protect MCP tools with Descope authentication and use connection tokens to call external APIs (Google Calendar).

## Prerequisites

- Python 3.8 or higher
- Descope project with:
  - Outbound application configured for Google Calendar
  - MCP server URL configured for audience validation
- Google Calendar API access (OAuth app configured in Descope)

## Setup

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to this directory
cd examples/fastmcp_calendar

# Install dependencies
uv sync

# Run the example
uv run python fastmcp_example.py
```

### Option 2: Using pip

```bash
# Navigate to this directory
cd examples/fastmcp_calendar

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the SDK in development mode from the root directory
cd ../..
pip install -e .
cd examples/fastmcp_calendar

# Run the example
python fastmcp_example.py
```

## Configuration

Set the following environment variables before running:

```bash
export DESCOPE_MCP_WELL_KNOWN_URL="https://api.descope.com/your-project-id/.well-known/openid-configuration"
export DESCOPE_MANAGEMENT_KEY="your-management-key"
export MCP_SERVER_URL="https://your-mcp-server.com"
export GOOGLE_CALENDAR_APP_ID="google-calendar"
```

Or create a `.env` file in this directory:

```
DESCOPE_MCP_WELL_KNOWN_URL=https://api.descope.com/your-project-id/.well-known/openid-configuration
DESCOPE_MANAGEMENT_KEY=your-management-key
MCP_SERVER_URL=https://your-mcp-server.com
GOOGLE_CALENDAR_APP_ID=google-calendar
```

## What This Example Shows

1. **Session Validation**: Validating MCP server access tokens with audience claim checking
2. **Scope-Based Authorization**: Requiring specific scopes (e.g., `calendar.read`) for tools
3. **Connection Tokens**: Retrieving OAuth tokens for external services (Google Calendar) from Descope
4. **External API Integration**: Using connection tokens to call Google Calendar API

## Key Features

- ✅ Token validation with audience claim
- ✅ Scope-based access control
- ✅ Connection token retrieval
- ✅ Google Calendar API integration
- ✅ Error handling

## Running

```bash
python fastmcp_example.py
```

## Example Flow

1. User authenticates and receives an MCP server access token
2. Tool receives request with access token
3. SDK validates token and checks for required scopes
4. SDK retrieves Google Calendar OAuth token from Descope
5. Tool uses Google Calendar token to fetch calendar events

## Notes

- This is a demonstration example. In production, integrate with FastMCP's actual authentication system
- The access token would come from FastMCP's request context in a real implementation
- Make sure your Descope project has the Google Calendar outbound app configured
