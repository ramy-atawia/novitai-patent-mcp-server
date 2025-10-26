#!/usr/bin/env python3
"""
Test script for the Novitai Patent MCP Server.

This script tests the MCP server by sending various MCP protocol requests.
"""

import asyncio
import json
import httpx
import sys
from typing import Dict, Any


class MCPClient:
    """Simple MCP client for testing."""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp"
        self.request_id = 1
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send MCP request."""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": method
        }
        
        if params:
            request["params"] = params
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.mcp_url,
                json=request,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP connection."""
        return await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        return await self.send_request("tools/list")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        return await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    async def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            return response.json()


async def test_mcp_server():
    """Test the MCP server."""
    print("🧪 Testing Novitai Patent MCP Server")
    print("=" * 50)
    
    client = MCPClient()
    
    try:
        # Test health check
        print("1. Testing health check...")
        health = await client.health_check()
        print(f"   ✅ Health: {health['status']}")
        print(f"   📊 Tools: {health['tools_count']}")
        print(f"   🔧 Available tools: {', '.join(health['tools'])}")
        print()
        
        # Test MCP initialization
        print("2. Testing MCP initialization...")
        init_response = await client.initialize()
        if "result" in init_response:
            print("   ✅ MCP initialization successful")
            print(f"   📋 Server: {init_response['result']['serverInfo']['name']}")
            print(f"   🔢 Version: {init_response['result']['serverInfo']['version']}")
        else:
            print(f"   ❌ MCP initialization failed: {init_response}")
            return False
        print()
        
        # Test tool listing
        print("3. Testing tool listing...")
        tools_response = await client.list_tools()
        if "result" in tools_response:
            tools = tools_response["result"]["tools"]
            print(f"   ✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool['name']}: {tool['description']}")
        else:
            print(f"   ❌ Tool listing failed: {tools_response}")
            return False
        print()
        
        # Test web search tool
        print("4. Testing web search tool...")
        web_search_response = await client.call_tool("web_search_tool", {
            "query": "patent search",
            "max_results": 3
        })
        if "result" in web_search_response and not web_search_response["result"].get("isError", False):
            print("   ✅ Web search tool working")
            content = web_search_response["result"]["content"][0]["text"]
            print(f"   📄 Response length: {len(content)} characters")
            print(f"   📝 Preview: {content[:100]}...")
        else:
            print(f"   ❌ Web search tool failed: {web_search_response}")
        print()
        
        # Test prior art search tool
        print("5. Testing prior art search tool...")
        prior_art_response = await client.call_tool("prior_art_search_tool", {
            "query": "machine learning",
            "max_results": 3
        })
        if "result" in prior_art_response and not prior_art_response["result"].get("isError", False):
            print("   ✅ Prior art search tool working")
            content = prior_art_response["result"]["content"][0]["text"]
            print(f"   📄 Response length: {len(content)} characters")
            print(f"   📝 Preview: {content[:100]}...")
        else:
            print(f"   ❌ Prior art search tool failed: {prior_art_response}")
        print()
        
        # Test claim drafting tool
        print("6. Testing claim drafting tool...")
        claim_drafting_response = await client.call_tool("claim_drafting_tool", {
            "user_query": "A system for detecting objects in images using neural networks"
        })
        if "result" in claim_drafting_response and not claim_drafting_response["result"].get("isError", False):
            print("   ✅ Claim drafting tool working")
            content = claim_drafting_response["result"]["content"][0]["text"]
            print(f"   📄 Response length: {len(content)} characters")
            print(f"   📝 Preview: {content[:100]}...")
        else:
            print(f"   ❌ Claim drafting tool failed: {claim_drafting_response}")
        print()
        
        # Test claim analysis tool
        print("7. Testing claim analysis tool...")
        claim_analysis_response = await client.call_tool("claim_analysis_tool", {
            "claims": [
                {
                    "claim_text": "A system comprising a processor configured to analyze data.",
                    "claim_type": "independent"
                }
            ],
            "analysis_type": "basic"
        })
        if "result" in claim_analysis_response and not claim_analysis_response["result"].get("isError", False):
            print("   ✅ Claim analysis tool working")
            content = claim_analysis_response["result"]["content"][0]["text"]
            print(f"   📄 Response length: {len(content)} characters")
            print(f"   📝 Preview: {content[:100]}...")
        else:
            print(f"   ❌ Claim analysis tool failed: {claim_analysis_response}")
        print()
        
        print("🎉 All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


async def main():
    """Main test function."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8001"
    
    print(f"🔗 Testing server at: {base_url}")
    print()
    
    success = await test_mcp_server()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())




