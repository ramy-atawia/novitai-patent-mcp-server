"""
Test script for FastMCP Server

This script tests all 4 tools on the FastMCP server using FastMCP's built-in testing capabilities.

Usage:
    python test_fastmcp_server.py
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastmcp import Client
from fastmcp_server import mcp


class FastMCPTester:
    """Test client for FastMCP server using FastMCP's built-in client"""
    
    def __init__(self):
        self.client = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = Client(mcp)
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a tool using FastMCP client"""
        if not self.client:
            raise RuntimeError("Client not initialized")
        
        result = await self.client.call_tool(name, arguments)
        return result


async def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("🧪 FastMCP Server Test Suite")
    print("=" * 70)
    print()
    
    async with FastMCPTester() as tester:
        # Test 1: Web Search Tool
        print("1️⃣  Testing web_search tool...")
        try:
            search_response = await tester.call_tool("web_search", {
                "query": "patent search best practices",
                "max_results": 3
            })
            print("   ✅ Web search successful")
            print(f"   Results preview: {str(search_response)[:200]}...")
        except Exception as e:
            print(f"   ❌ Web search error: {str(e)}")
        print()
        
        # Test 2: Prior Art Search Tool
        print("2️⃣  Testing prior_art_search tool...")
        try:
            prior_art_response = await tester.call_tool("prior_art_search", {
                "params": {
                    "query": "machine learning image recognition",
                    "max_results": 5
                }
            })
            print("   ✅ Prior art search successful")
            print(f"   Results preview: {str(prior_art_response)[:200]}...")
        except Exception as e:
            print(f"   ❌ Prior art search error: {str(e)}")
        print()
        
        # Test 3: Claim Drafting Tool
        print("3️⃣  Testing claim_drafting tool...")
        try:
            drafting_response = await tester.call_tool("claim_drafting", {
                "params": {
                    "user_query": "A system for detecting objects in images using deep learning"
                }
            })
            print("   ✅ Claim drafting successful")
            print(f"   Results preview: {str(drafting_response)[:200]}...")
        except Exception as e:
            print(f"   ❌ Claim drafting error: {str(e)}")
        print()
        
        # Test 4: Claim Analysis Tool
        print("4️⃣  Testing claim_analysis tool...")
        try:
            analysis_response = await tester.call_tool("claim_analysis", {
                "params": {
                    "claims": [
                        {"claim_text": "A system comprising a processor configured to analyze data."}
                    ],
                    "analysis_type": "basic"
                }
            })
            print("   ✅ Claim analysis successful")
            print(f"   Results preview: {str(analysis_response)[:200]}...")
        except Exception as e:
            print(f"   ❌ Claim analysis error: {str(e)}")
        print()
    
    print("=" * 70)
    print("🎉 Test suite completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_tests())

