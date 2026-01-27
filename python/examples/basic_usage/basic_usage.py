#!/usr/bin/env python3
"""Basic usage example for Descope MCP SDK."""

import asyncio
import os
from typing import Dict, Any

from mcp_descope import DescopeMCPClient, create_default_client


async def basic_example():
    """Basic example showing all available token operations."""
    
    # Set up environment variables (in production, use proper secret management)
    os.environ["DESCOPE_PROJECT_ID"] = "your-project-id"
    os.environ["DESCOPE_MANAGEMENT_KEY"] = "your-management-key"
    
    # Create client
    client = create_default_client()
    
    try:
        async with client:
            print("🔐 Descope MCP SDK - Basic Usage Example")
            print("=" * 50)
            
            # Example 1: Fetch user token with specific scopes
            print("\n1. Fetching user token with scopes...")
            try:
                user_token = await client.fetch_user_token_by_scopes(
                    app_id="my-app-id",
                    user_id="user-123",
                    scopes=["read", "write"],
                    options={"refreshToken": True},
                    tenant_id="tenant-456",
                )
                print(f"✅ User token fetched: {user_token.token[:20]}...")
            except Exception as e:
                print(f"❌ Error fetching user token: {e}")
            
            # Example 2: Fetch latest user token
            print("\n2. Fetching latest user token...")
            try:
                latest_user_token = await client.fetch_user_token(
                    app_id="my-app-id",
                    user_id="user-123",
                    tenant_id="tenant-456",
                    options={"forceRefresh": True},
                )
                print(f"✅ Latest user token fetched: {latest_user_token.token[:20]}...")
            except Exception as e:
                print(f"❌ Error fetching latest user token: {e}")
            
            # Example 3: Fetch tenant token with scopes
            print("\n3. Fetching tenant token with scopes...")
            try:
                tenant_token = await client.fetch_tenant_token_by_scopes(
                    app_id="my-app-id",
                    tenant_id="tenant-456",
                    scopes=["read", "write"],
                    options={"refreshToken": True},
                )
                print(f"✅ Tenant token fetched: {tenant_token.token[:20]}...")
            except Exception as e:
                print(f"❌ Error fetching tenant token: {e}")
            
            # Example 4: Fetch latest tenant token
            print("\n4. Fetching latest tenant token...")
            try:
                latest_tenant_token = await client.fetch_tenant_token(
                    app_id="my-app-id",
                    tenant_id="tenant-456",
                    options={"forceRefresh": True},
                )
                print(f"✅ Latest tenant token fetched: {latest_tenant_token.token[:20]}...")
            except Exception as e:
                print(f"❌ Error fetching latest tenant token: {e}")
            
            print("\n🎉 Basic example completed!")
            
    except Exception as e:
        print(f"❌ Client error: {e}")


async def advanced_example():
    """Advanced example showing error handling and different options."""
    
    # Set up environment variables
    os.environ["DESCOPE_PROJECT_ID"] = "your-project-id"
    os.environ["DESCOPE_MANAGEMENT_KEY"] = "your-management-key"
    
    client = create_default_client()
    
    try:
        async with client:
            print("\n🔐 Descope MCP SDK - Advanced Usage Example")
            print("=" * 50)
            
            # Example with different scope combinations
            scopes_combinations = [
                ["read"],
                ["write"],
                ["read", "write"],
                ["admin", "read", "write"],
            ]
            
            for i, scopes in enumerate(scopes_combinations, 1):
                print(f"\n{i}. Testing with scopes: {scopes}")
                try:
                    token = await client.fetch_user_token_by_scopes(
                        app_id="my-app-id",
                        user_id="user-123",
                        scopes=scopes,
                        tenant_id="tenant-456",
                    )
                    print(f"   ✅ Success: {token.token[:20]}...")
                except Exception as e:
                    print(f"   ❌ Failed: {e}")
            
            # Example with different options
            options_combinations = [
                {"refreshToken": True},
                {"forceRefresh": True},
                {"refreshToken": True, "forceRefresh": True},
                {},
            ]
            
            for i, options in enumerate(options_combinations, 1):
                print(f"\n{i + len(scopes_combinations)}. Testing with options: {options}")
                try:
                    token = await client.fetch_user_token(
                        app_id="my-app-id",
                        user_id="user-123",
                        tenant_id="tenant-456",
                        options=options,
                    )
                    print(f"   ✅ Success: {token.token[:20]}...")
                except Exception as e:
                    print(f"   ❌ Failed: {e}")
            
            print("\n🎉 Advanced example completed!")
            
    except Exception as e:
        print(f"❌ Client error: {e}")


async def main():
    """Run all examples."""
    print("🚀 Starting Descope MCP SDK Examples")
    print("=" * 50)
    
    await basic_example()
    await advanced_example()
    
    print("\n✨ All examples completed!")


if __name__ == "__main__":
    asyncio.run(main()) 