# End-to-End Tests

This directory contains comprehensive end-to-end tests for the MCP Descope SDK, covering all integration scenarios.

## Test Files

### `test_functions.py`
Tests SDK functions directly without any MCP server framework. This verifies core functionality:
- Token validation
- Connection token retrieval
- Tenant token fetching
- Class-based API usage

### `test_mcpserver.py`
Tests integration with the official Python MCP SDK (`MCPServer`):
- Tool registration
- Resource registration
- Prompt registration
- Descope-protected tools

### `test_fastmcp2.py`
Tests integration with FastMCP 2.0 (`mcp.server.FastMCP`):
- Public tools
- Auth check integration
- Token validation
- Connection token usage
- Scope-based authorization

### `test_fastmcp3.py`
Tests integration with FastMCP 3.0 (`fastmcp.FastMCP` with auth providers):
- Basic authentication
- Scope-based authentication
- DescopeProvider integration
- Comprehensive auth patterns

### `conftest.py`
Shared pytest fixtures and configuration:
- Test environment setup
- Mock DescopeClient fixtures

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_functions.py
pytest tests/test_mcpserver.py
pytest tests/test_fastmcp2.py
pytest tests/test_fastmcp3.py
```

### Run with coverage
```bash
pytest tests/ --cov=mcp_descope --cov-report=html
```

### Run specific test class
```bash
pytest tests/test_functions.py::TestDirectFunctions
```

## Test Structure

All tests use mocking to avoid requiring actual Descope API credentials. The tests verify:
1. **Functionality**: SDK functions work correctly
2. **Integration**: SDK integrates properly with MCP frameworks
3. **Error Handling**: Proper error handling and validation
4. **API Compatibility**: Correct usage of MCP framework APIs

## Notes

- FastMCP 3.0 tests are skipped if `fastmcp` package is not available
- All tests use mocked DescopeClient to avoid external API calls
- Tests verify both class-based and function-based API usage
- Environment variables are automatically set via `conftest.py`
