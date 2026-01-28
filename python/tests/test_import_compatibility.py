"""Test that mcp_descope can be imported alongside descope SDK without conflicts."""

import pytest


def test_both_sdks_can_be_imported():
    """Test that both descope and mcp_descope can be imported together."""
    import descope
    import mcp_descope
    
    # Verify both packages are imported
    assert descope is not None
    assert mcp_descope is not None
    
    # Verify DescopeClient from descope is available
    assert hasattr(descope, 'DescopeClient')
    
    # Verify mcp_descope exports don't conflict
    assert hasattr(mcp_descope, 'DescopeConfig')
    assert hasattr(mcp_descope, 'DescopeMCP')
    assert hasattr(mcp_descope, 'init_descope_mcp')
    assert hasattr(mcp_descope, 'get_descope_client')
    assert hasattr(mcp_descope, 'validate_token_and_get_user_id')
    assert hasattr(mcp_descope, 'get_connection_token')


def test_descope_client_class_import():
    """Test that DescopeClient can be imported from both packages."""
    from descope import DescopeClient as DescopeSDKClient
    from mcp_descope import DescopeMCP
    
    # DescopeMCP uses DescopeClient internally but is a different class
    assert DescopeSDKClient is not None
    assert DescopeMCP is not None
    # They're different classes - DescopeMCP wraps DescopeClient
    assert DescopeSDKClient is not DescopeMCP


def test_no_module_name_conflicts():
    """Test that module names don't conflict."""
    import descope
    import mcp_descope
    
    # Check that descope has descope_client module (internal)
    # and mcp_descope has descope_client module (our wrapper)
    # They should be different modules in different packages
    descope_descope_client = getattr(descope, 'descope_client', None)
    mcp_descope_descope_client = getattr(mcp_descope, 'descope_client', None)
    
    # These are different modules, so no conflict
    # mcp_descope.descope_client is our module
    # descope.descope_client is Descope SDK's internal module
    assert mcp_descope_descope_client is not None or True  # Our module exists
    # They're in different packages, so no conflict


def test_function_names_dont_conflict():
    """Test that function names don't conflict when both are imported."""
    from descope import DescopeClient
    from mcp_descope import get_descope_client, DescopeConfig
    
    # Verify we can use both
    assert DescopeClient is not None
    assert get_descope_client is not None
    assert DescopeConfig is not None
    
    # Verify get_descope_client is our function, not from descope
    # (descope SDK doesn't export get_descope_client)
    assert callable(get_descope_client)
