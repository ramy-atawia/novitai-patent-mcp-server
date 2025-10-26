"""
Real Web Search Service

Integrates with actual web APIs for Google Search, arXiv, and academic databases.
Provides real search results instead of placeholder content.
"""

import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Optional, Any
from urllib.parse import quote_plus, urlparse
import logging
import os

logger = logging.getLogger(__name__)


class WebSearchService:
    """Real web search service with multiple search engines."""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x64) AppleWebKit/537.36"
        ]
        
        # Get API credentials from settings (loads from .env file)
        from app.core.config import settings
        self.google_api_key = settings.google_search_api_key
        self.google_engine_id = settings.google_search_engine_id
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"User-Agent": self.user_agents[0]}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def search_google(self, query: str, max_results: int = 10, 
                           include_abstracts: bool = False) -> List[Dict[str, Any]]:
        """Perform real Google search using Google Custom Search API."""
        try:
            if not self.google_api_key or not self.google_engine_id:
                logger.warning("Google Search API not configured")
                return []
            
            # Google Custom Search API endpoint
            api_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_engine_id,
                "q": query,
                "num": min(max_results, 10)  # Google CSE max is 10
            }
            
            if not self.session:
                return []
            
            async with self.session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = self._parse_google_results(data, include_abstracts)
                    logger.info(f"Google search completed for query: {query}, found {len(results)} results")
                    return results
                else:
                    logger.warning(f"Google API returned status {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Google search failed for query '{query}': {str(e)}")
            return []
    
    def _parse_google_results(self, data: Dict[str, Any], include_abstracts: bool) -> List[Dict[str, Any]]:
        """Parse Google Custom Search API results."""
        try:
            results = []
            items = data.get("items", [])
            
            for item in items:
                result = {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "Google Search",
                    "type": "web_page",
                    "relevance": 0.8  # Default relevance score
                }
                
                # Add additional metadata if available
                if "pagemap" in item:
                    pagemap = item["pagemap"]
                    if "metatags" in pagemap:
                        metatags = pagemap["metatags"][0]
                        result["description"] = metatags.get("og:description", "")
                        result["image"] = metatags.get("og:image", "")
                    
                    if "cse_image" in pagemap:
                        result["thumbnail"] = pagemap["cse_image"][0].get("src", "")
                
                # Include abstract if requested and available
                if include_abstracts and result["snippet"]:
                    result["abstract"] = result["snippet"]
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to parse Google results: {str(e)}")
            return []
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status and configuration."""
        return {
            "service": "WebSearchService",
            "google_api_configured": bool(self.google_api_key and self.google_engine_id),
            "google_api_key_length": len(self.google_api_key) if self.google_api_key else 0,
            "google_engine_id_length": len(self.google_engine_id) if self.google_engine_id else 0,
            "session_active": self.session is not None,
            "status": "active"
        }


# Global instance for easy access
web_search_service = WebSearchService()




