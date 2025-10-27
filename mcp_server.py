"""
FastMCP Server for Novitai Patent MCP Server

This is a lightweight FastMCP wrapper that exposes your existing tools
through FastMCP's high-level interface.

Approach: Instead of proxying, we directly wrap your existing service classes
with FastMCP decorators, giving you all FastMCP benefits with minimal code.

Features:
- FastMCP's high-level decorator interface
- Automatic schema generation
- Context-aware logging
- SSE transport support
- Production deployment features
- Built-in error handling

Usage:
    python fastmcp_server.py
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated

# Set up verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import your existing services
from app.services.web_search_service import WebSearchService
from app.services.patent_search_service import PatentSearchService
from app.services.claim_drafting_service import ClaimDraftingService
from app.services.claim_analysis_service import ClaimAnalysisService

# Create FastMCP server with debug logging
mcp = FastMCP(
    name="Novitai Patent MCP Server",
    version="1.0.0",
    instructions="""
    Novitai Patent MCP Server - AI-powered patent analysis and search platform.
    
    This server provides four main capabilities:
    1. Web Search - Search the web for patent-related information
    2. Prior Art Search - Search PatentsView API for prior art patents
    3. Claim Drafting - Generate patent claims using AI
    4. Claim Analysis - Analyze patent claims for quality and compliance
    
    All tools are powered by Azure OpenAI and real-time API integrations.
    """
)

# Note: FastMCP doesn't support before_request middleware
# We'll add logging to individual tool functions instead


# ============================================================================
# Tool 1: Web Search Tool
# ============================================================================

@mcp.tool
async def web_search(
    query: Annotated[str, Field(description="Search query", min_length=2)],
    max_results: Annotated[int, Field(description="Maximum number of results", default=10, ge=1, le=10)] = 10,
    ctx: Context = None
) -> str:
    """
    Search the web for information using Google Custom Search API.
    
    This tool provides real-time web search results including:
    - Titles and URLs
    - Snippets and descriptions
    - Relevance ranking
    
    Returns markdown-formatted search results.
    """
    logger.info(f"Web search called with query='{query}', max_results={max_results}, ctx={ctx}")
    if ctx:
        await ctx.info(f"Starting web search for query: {query}")
    
    try:
        # Use existing service
        async with WebSearchService() as search_service:
            search_results = await search_service.search_google(
                query=query,
                max_results=max_results,
                include_abstracts=True
            )
        
        if search_results:
            # Format results
            result_text = f"# Web Search Results for: {query}\n\n"
            for i, result in enumerate(search_results, 1):
                result_text += f"## {i}. {result.get('title', 'No title')}\n"
                result_text += f"**URL**: {result.get('link', 'No URL')}\n"
                result_text += f"**Snippet**: {result.get('snippet', 'No snippet')}\n\n"
            
            if ctx:
                await ctx.info(f"Web search completed - found {len(search_results)} results")
            
            return result_text
        else:
            if ctx:
                await ctx.warning(f"No search results found for query: {query}")
            return f"# Web Search Results for: {query}\n\nNo search results found."
    
    except Exception as e:
        logger.error(f"Web search failed: {str(e)}", exc_info=True)
        if ctx:
            await ctx.error(f"Web search failed: {str(e)}")
        return f"# Web Search Error\n\n**Error**: {str(e)}"


# ============================================================================
# Tool 2: Prior Art Search Tool
# ============================================================================

@mcp.tool
async def prior_art_search(
    query: Annotated[str, Field(description="Search query describing the invention or technology", min_length=3, max_length=1000)],
    context: Annotated[Optional[str], Field(None, description="Additional context from document or conversation")] = None,
    ctx: Context = None
) -> str:
    """
    Search for prior art patents using PatentsView API with AI-powered query generation.
    
    This tool:
    1. Uses LLM to generate 5 optimized PatentsView API queries
    2. Executes searches against PatentsView API
    3. Retrieves patent details including claims
    4. Generates a comprehensive markdown report
    
    Returns detailed prior art analysis report.
    """
    if ctx:
        await ctx.info(f"Starting prior art search for: {query}")
    
    try:
        # Use existing service (PatentSearchService doesn't use async context manager)
        patent_service = PatentSearchService()
        
        search_result, generated_queries = await patent_service.search_patents(
            query=query,
            context=context,
            conversation_history=None,
            max_results=20
        )
        
        if ctx:
            await ctx.info(f"Prior art search completed - found {search_result['results_found']} patents")
        
        return search_result["report"]
    
    except ValueError as e:
        if ctx:
            await ctx.error(f"Prior art search validation error: {str(e)}")
        return f"# Prior Art Search Report\n\n**Query**: {query}\n\n**Error**: {str(e)}"
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Prior art search failed: {str(e)}")
        return f"# Prior Art Search Report\n\n**Query**: {query}\n\n**Error**: An unexpected error occurred. {str(e)}"


# ============================================================================
# Tool 3: Claim Drafting Tool
# ============================================================================

@mcp.tool
async def claim_drafting(
    user_query: Annotated[str, Field(description="Description of the invention or feature to draft claims for", min_length=10)],
    context: Annotated[Optional[str], Field(None, description="Additional context from document")] = None,
    ctx: Context = None
) -> str:
    """
    Generate patent claims using AI-powered claim drafting.
    
    This tool uses Azure OpenAI to:
    1. Analyze the invention description
    2. Generate independent and dependent claims
    3. Ensure proper claim structure and formatting
    4. Follow patent claim drafting best practices
    
    Returns AI-generated patent claims in proper format.
    """
    if ctx:
        await ctx.info(f"Starting claim drafting for: {user_query[:100]}...")
    
    try:
        # Use existing service with async context manager
        async with ClaimDraftingService() as drafting_service:
                draft_result = await drafting_service.draft_claims(
                    user_query=user_query,
                    conversation_context=None,
                    document_reference=context
                )
        
        if ctx:
            await ctx.info("Claim drafting completed successfully")
        
        # Return the drafting_report string from the result dict
        return draft_result[0].get("drafting_report", "Error: No drafting report generated")
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Claim drafting failed: {str(e)}")
        return f"# Claim Drafting Error\n\n**Error**: {str(e)}"


# ============================================================================
# Tool 4: Claim Analysis Tool
# ============================================================================

class Claim(BaseModel):
    """A single patent claim"""
    claim_text: Annotated[str, Field(description="The text of the patent claim")]


@mcp.tool
async def claim_analysis(
    claims: Annotated[List[Claim], Field(description="List of claims to analyze", min_length=1)],
    context: Annotated[Optional[str], Field(None, description="Additional context for analysis")] = None,
    ctx: Context = None
) -> str:
    """
    Analyze patent claims for quality, structure, and compliance.
    
    This tool uses AI to:
    1. Evaluate claim structure and clarity
    2. Identify potential issues or weaknesses
    3. Suggest improvements
    4. Check for proper claim dependencies
    5. Assess claim scope and coverage
    
    Returns comprehensive claim analysis report.
    """
    if ctx:
        await ctx.info(f"Starting claim analysis for {len(claims)} claims")
    
    try:
        # Use existing service with async context manager
        async with ClaimAnalysisService() as analysis_service:
            # Convert Pydantic models to dict format expected by service
            claims_list = [{"claim_text": claim.claim_text} for claim in claims]
            
            analysis_result = await analysis_service.analyze_claims(
                claims=claims_list,
                analysis_type="comprehensive",
                focus_areas=[]
            )
        
        if ctx:
            await ctx.info("Claim analysis completed successfully")
        
        # Return the analysis_report string from the result dict
        result_dict = analysis_result[0]
        return result_dict.get("analysis_report", f"# Claim Analysis\n\nAnalyzed {result_dict.get('claims_analyzed', 0)} claims")
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Claim analysis failed: {str(e)}")
        return f"# Claim Analysis Error\n\n**Error**: {str(e)}"


# ============================================================================
# Server Entry Point
# ============================================================================

def main():
    """
    Start the FastMCP server.
    
    This will run the server with:
    - SSE transport (better client compatibility)
    - Port 8002 (keeping original server on 8001)
    - All 4 tools exposed through FastMCP
    """
    print("=" * 70)
    print("🚀 Novitai Patent MCP Server - FastMCP Edition")
    print("=" * 70)
    print()
    print("📡 Transport: HTTP (JSON-RPC)")
    print("🌐 Host: 0.0.0.0")
    print("🔌 Port: 8003")
    print()
    print("✨ FastMCP Features Enabled:")
    print("   - High-level decorator interface")
    print("   - Automatic schema generation")
    print("   - Context-aware logging")
    print("   - Production-ready error handling")
    print("   - Enhanced client compatibility")
    print()
    print("🛠️  Available Tools:")
    print("   1. web_search - Web search via Google API")
    print("   2. prior_art_search - Patent search via PatentsView API")
    print("   3. claim_drafting - AI-powered claim generation")
    print("   4. claim_analysis - AI-powered claim evaluation")
    print()
    print("=" * 70)
    print()
    
    # Run the server
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8003
    )


if __name__ == "__main__":
    main()

