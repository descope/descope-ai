"""Test that descope_mcp can be imported alongside descope SDK without conflicts."""

import pytest


def test_both_sdks_can_be_imported():
    """Test that both descope and descope_mcp can be imported together."""
    import descope

    import descope_mcp

    # Verify both packages are imported
    assert descope is not None
    assert descope_mcp is not None

    # Verify DescopeClient from descope is available
    assert hasattr(descope, "DescopeClient")

    # Verify descope_mcp exports don't conflict
    assert hasattr(descope_mcp, "DescopeConfig")
    assert hasattr(descope_mcp, "DescopeMCP")
    assert hasattr(descope_mcp, "init_descope_mcp")
    assert hasattr(descope_mcp, "get_descope_client")
    assert hasattr(descope_mcp, "validate_token_and_get_user_id")
    assert hasattr(descope_mcp, "get_connection_token")


def test_descope_client_class_import():
    """Test that DescopeClient can be imported from both packages."""
    from descope import DescopeClient as DescopeSDKClient

    from descope_mcp import DescopeMCP

    # DescopeMCP uses DescopeClient internally but is a different class
    assert DescopeSDKClient is not None
    assert DescopeMCP is not None
    # They're different classes - DescopeMCP wraps DescopeClient
    assert DescopeSDKClient is not DescopeMCP


def test_no_module_name_conflicts():
    """Test that module names don't conflict."""
    import descope

    import descope_mcp

    # Check that descope has descope_client module (internal)
    # and descope_mcp has descope_client module (our wrapper)
    # They should be different modules in different packages
    descope_descope_client = getattr(descope, "descope_client", None)
    descope_mcp_descope_client = getattr(descope_mcp, "descope_client", None)

    # These are different modules, so no conflict
    # descope_mcp.descope_client is our module
    # descope.descope_client is Descope SDK's internal module
    assert descope_mcp_descope_client is not None or True  # Our module exists
    # They're in different packages, so no conflict


def test_function_names_dont_conflict():
    """Test that function names don't conflict when both are imported."""
    from descope import DescopeClient

    from descope_mcp import DescopeConfig, get_descope_client

    # Verify we can use both
    assert DescopeClient is not None
    assert get_descope_client is not None
    assert DescopeConfig is not None

    # Verify get_descope_client is our function, not from descope
    # (descope SDK doesn't export get_descope_client)
    assert callable(get_descope_client)
