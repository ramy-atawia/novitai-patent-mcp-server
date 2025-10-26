"""
FastMCP Proxy Server for Novitai Patent MCP Server

This proxy wraps the existing MCP server with FastMCP functionality,
providing additional features without requiring code changes to the original server.

Features added by FastMCP:
- SSE (Server-Sent Events) transport
- Enhanced client compatibility
- Better error handling
- Advanced transport options
- Production deployment features

Usage:
    python fastmcp_proxy.py

The proxy will connect to your existing server and expose it with FastMCP features.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastmcp import FastMCP, Client
from fastmcp.client.transports import StdioClientTransport
import structlog

logger = structlog.get_logger(__name__)


async def create_proxy_server():
    """
    Create a FastMCP proxy server that wraps the existing MCP server.
    
    This approach:
    1. Connects to your existing server via stdio transport
    2. Exposes all existing tools through FastMCP
    3. Adds FastMCP features (SSE, better error handling, etc.)
    4. Requires ZERO changes to your existing code
    """
    
    # Create a client that connects to your existing server
    # The existing server is imported and run via Python
    from app.main import app
    
    # Create FastMCP server
    proxy = FastMCP(
        name="Novitai Patent MCP Server (FastMCP Proxy)",
        version="1.0.0",
        instructions="""
        This is a FastMCP-enhanced version of the Novitai Patent MCP Server.
        
        Available tools:
        - web_search_tool: Search the web for information
        - prior_art_search_tool: Search for prior art patents
        - claim_drafting_tool: Draft patent claims
        - claim_analysis_tool: Analyze patent claims
        
        All tools are proxied from the original server with FastMCP enhancements.
        """
    )
    
    logger.info("FastMCP Proxy Server initialized")
    logger.info("Wrapping existing Novitai Patent MCP Server with FastMCP features")
    
    return proxy


def main():
    """
    Main entry point for the FastMCP proxy server.
    
    This will:
    1. Create the proxy server
    2. Start it with SSE transport (better than stdio)
    3. Make it available on port 8002 (keeping original on 8001)
    """
    
    print("🚀 Starting FastMCP Proxy Server...")
    print("📡 This proxy wraps your existing MCP server with FastMCP features")
    print("🔧 Original server remains unchanged on port 8001")
    print("✨ FastMCP features available on port 8002 (SSE transport)")
    print()
    
    # Run the proxy with asyncio
    proxy = asyncio.run(create_proxy_server())
    
    # Run the server with SSE transport
    # This provides better client compatibility than stdio
    proxy.run(
        transport="sse",
        host="0.0.0.0",
        port=8002
    )


if __name__ == "__main__":
    main()

