# MCP Descope SDK

Multi-language SDK for integrating Descope authentication with MCP (Model Context Protocol) servers.

Descope serves as the **Authorization Server (AS)** for your MCP Servers, providing:
- [Full authorization and scoping](https://docs.descope.com/agentic-identity-hub/mcp-servers) - Token validation, scope enforcement, and audience validation
- [External token storage](https://docs.descope.com/agentic-identity-hub/connections) - Secure storage and retrieval of OAuth tokens for third-party services (Google Calendar, Slack, etc.)
- [Policy enforcement](https://docs.descope.com/agentic-identity-hub/policies) - Real-time authorization decisions based on user identity, roles, and scopes

## Languages

- [Python SDK](./python/README.md) - Python SDK for MCP Descope integration
- TypeScript SDK - Coming soon

## Quick Links

- [Python Documentation](./python/README.md)
- [Python Examples](./python/examples/)
- [Contributing](./CONTRIBUTING.md) (coming soon)

## Repository Structure

```
.
├── python/          # Python SDK
│   ├── src/        # Source code
│   ├── tests/      # Tests
│   ├── examples/   # Example code
│   └── README.md   # Python SDK documentation
└── typescript/     # TypeScript SDK (coming soon)
```
