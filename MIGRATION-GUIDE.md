# FastMCP Migration Guide

This guide explains how the FastMCP implementation was created and how to migrate between the original and FastMCP versions.

## 📋 Table of Contents

- [Migration Approach](#migration-approach)
- [What Changed](#what-changed)
- [What Stayed the Same](#what-stayed-the-same)
- [Files Created](#files-created)
- [Architecture Comparison](#architecture-comparison)
- [Code Comparison](#code-comparison)
- [Migration Benefits](#migration-benefits)
- [Running Both Versions](#running-both-versions)

## 🎯 Migration Approach

We chose the **wrapper approach** instead of full migration:

- ✅ **Zero changes** to original server code
- ✅ **Reuses existing services** (WebSearchService, PatentSearchService, etc.)
- ✅ **Adds FastMCP layer** on top of existing functionality
- ✅ **Both servers can run simultaneously** (ports 8001 and 8003)

This approach provides all FastMCP benefits with minimal effort (2-4 hours vs 92 hours).

## 🔄 What Changed

### 1. Tool Implementation Style

**Original (Class-Based):**
```python
# app/mcp_tools/web_search.py (168 lines)
class WebSearchTool(BaseMCPTool):
    def __init__(self):
        super().__init__(
            name="web_search_tool",
            description="Search the web for information",
            version="1.0.0"
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "default": 10, "minimum": 1, "maximum": 10}
            },
            "required": ["query"]
        }
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        query = parameters.get("query", "").strip()
        max_results = parameters.get("max_results", 10)
        # ... implementation
```

**FastMCP (Decorator-Based):**
```python
# fastmcp_server.py (~30 lines per tool)
@mcp.tool
async def web_search(
    query: Annotated[str, Field(description="Search query", min_length=2)],
    max_results: Annotated[int, Field(default=10, ge=1, le=10)] = 10,
    ctx: Context = None
) -> str:
    """Search the web for information using Google Custom Search API."""
    if ctx:
        await ctx.info(f"Starting web search for query: {query}")
    
    # ... implementation (reuses existing services)
```

### 2. Schema Definition

**Original:** Manual JSON schemas (40+ lines per tool)
**FastMCP:** Automatic from Python type hints (5-10 lines per tool)

### 3. Server Setup

**Original (`app/main.py`):**
- 380+ lines of FastAPI setup
- Manual JSON-RPC 2.0 handling
- Custom error handling
- Manual method routing

**FastMCP (`fastmcp_server.py`):**
- ~400 lines total (including all 4 tools)
- Automatic protocol handling
- Built-in error handling
- Automatic method routing

### 4. Transport

**Original:** HTTP with JSON-RPC 2.0
**FastMCP:** SSE (Server-Sent Events) for better streaming

## ✅ What Stayed the Same

### No Changes Required

The following components remain completely unchanged:

1. **Service Layer** (`app/services/`)
   - `WebSearchService` - unchanged
   - `PatentSearchService` - unchanged
   - `ClaimDraftingService` - unchanged
   - `ClaimAnalysisService` - unchanged
   - `LLMClient` - unchanged

2. **Configuration** (`app/core/config.py`)
   - All settings remain the same
   - Same environment variables
   - Same API key management

3. **Prompt Templates** (`app/prompts/`)
   - All prompt files unchanged
   - Same prompt loading logic

4. **Utilities** (`app/utils/`)
   - All utility functions unchanged

5. **Environment Variables**
   - Same `.env` file
   - Same API keys and configuration

## 📁 Files Created

### New Files for FastMCP

1. **`fastmcp_server.py`** (400 lines)
   - Main FastMCP server implementation
   - All 4 tools with decorator interface
   - Reuses existing services

2. **`fastmcp.json`** (30 lines)
   - FastMCP configuration
   - Deployment settings
   - Dependencies list

3. **`requirements-fastmcp.txt`** (15 lines)
   - Additional FastMCP dependencies
   - Installed alongside original requirements

4. **`Dockerfile.fastmcp`** (60 lines)
   - Docker build for FastMCP server
   - Multi-stage build for optimization

5. **`docker-compose-fastmcp.yml`** (80 lines)
   - Docker Compose configuration
   - Runs both servers side-by-side

6. **`run-fastmcp.sh`** (40 lines)
   - Startup script for FastMCP server
   - Environment setup and checks

7. **`test_fastmcp_server.py`** (200 lines)
   - Test suite for FastMCP server
   - Tests all 4 tools

8. **`README-FASTMCP.md`** (500+ lines)
   - Complete documentation
   - Usage examples
   - Deployment guide

9. **`MIGRATION-GUIDE.md`** (this file)
   - Migration documentation
   - Code comparisons
   - Architecture explanation

### Files Not Modified

All original files remain unchanged:
- ✅ `app/main.py` - original server
- ✅ `app/mcp_tools/*.py` - all tool classes
- ✅ `app/services/*.py` - all services
- ✅ `app/core/*.py` - configuration
- ✅ `requirements.txt` - original dependencies
- ✅ `Dockerfile` - original Docker build
- ✅ `docker-compose.yml` - original compose file

## 🏗️ Architecture Comparison

### Original Architecture

```
app/main.py (380 lines)
├── FastAPI app
├── Manual JSON-RPC handling
├── Manual error handling
└── Tool instances
    ├── WebSearchTool (168 lines)
    ├── PriorArtSearchTool (150 lines)
    ├── ClaimDraftingTool (160 lines)
    └── ClaimAnalysisTool (170 lines)
        └── Services (unchanged)
            ├── WebSearchService
            ├── PatentSearchService
            ├── ClaimDraftingService
            └── ClaimAnalysisService
```

### FastMCP Architecture

```
fastmcp_server.py (400 lines)
├── FastMCP app
├── Automatic protocol handling
├── Built-in error handling
└── Decorated functions
    ├── @web_search (30 lines)
    ├── @prior_art_search (40 lines)
    ├── @claim_drafting (30 lines)
    └── @claim_analysis (35 lines)
        └── Services (REUSED, unchanged)
            ├── WebSearchService
            ├── PatentSearchService
            ├── ClaimDraftingService
            └── ClaimAnalysisService
```

## 💻 Code Comparison

### Web Search Tool

**Original:** 168 lines
```python
class WebSearchTool(BaseMCPTool):
    def __init__(self): # 40 lines
        # Schema definition
        # Metadata
        # Examples
        
    async def validate_parameters(self, parameters): # 10 lines
        # Manual validation
        
    async def execute(self, parameters): # 80 lines
        # Manual parameter extraction
        # Service calls
        # Error handling
        # Response formatting
```

**FastMCP:** 30 lines
```python
@mcp.tool
async def web_search(
    query: Annotated[str, Field(description="...", min_length=2)],
    max_results: Annotated[int, Field(default=10, ge=1, le=10)] = 10,
    ctx: Context = None
) -> str:
    # Automatic validation from type hints
    # Service calls (same code)
    # Built-in error handling via Context
    # Response formatting (same code)
```

### Prior Art Search Tool

**Original:** 150 lines with complex schemas
**FastMCP:** 40 lines with Pydantic models

**Original Schema Definition:**
```python
self.input_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "minLength": 3, "maxLength": 1000},
        "context": {"type": "string"},
        "conversation_history": {"type": "string"},
        "max_results": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100}
    },
    "required": ["query"]
}
```

**FastMCP Pydantic Model:**
```python
class PriorArtSearchParams(BaseModel):
    query: Annotated[str, Field(min_length=3, max_length=1000)]
    context: Optional[str] = None
    conversation_history: Optional[str] = None
    max_results: Annotated[int, Field(default=20, ge=1, le=100)] = 20
```

## 🎁 Migration Benefits

### Code Reduction

| Component | Original | FastMCP | Reduction |
|-----------|----------|---------|-----------|
| **Web Search Tool** | 168 lines | 30 lines | 82% |
| **Prior Art Tool** | 150 lines | 40 lines | 73% |
| **Claim Drafting** | 160 lines | 30 lines | 81% |
| **Claim Analysis** | 170 lines | 35 lines | 79% |
| **Main Server** | 380 lines | 50 lines* | 87% |
| **Total** | ~1028 lines | ~400 lines | 61% |

*Main server logic excluding tool definitions

### Features Added

- ✅ **Context-aware logging** - Better debugging and monitoring
- ✅ **SSE transport** - Better client compatibility
- ✅ **Automatic schemas** - From type hints
- ✅ **Built-in validation** - Pydantic models
- ✅ **Production features** - Deployment tools, etc.

### Maintenance Benefits

- ✅ **Less code to maintain** - 61% reduction
- ✅ **Clearer intent** - Decorator-based is more readable
- ✅ **Faster development** - New tools are easier to add
- ✅ **Better testing** - FastMCP testing tools

## 🔄 Running Both Versions

You can run both servers simultaneously for comparison or gradual migration:

### Terminal Setup

```bash
# Terminal 1: Original server (port 8001)
cd /Users/Mariam/novitai-patent-mcp-server
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2: FastMCP server (port 8003)
cd /Users/Mariam/novitai-patent-mcp-server
source venv/bin/activate
python fastmcp_server.py
```

### Docker Compose

```bash
# Run both servers with Docker Compose
docker-compose -f docker-compose-fastmcp.yml up

# This starts:
# - Original server on port 8001
# - FastMCP server on port 8003
```

### Testing Both

```bash
# Test original server
python test_mcp_server.py  # Tests port 8001

# Test FastMCP server
python test_fastmcp_server.py  # Tests port 8003
```

## 🎯 Recommended Approach

### For New Projects

✅ **Use FastMCP** (`fastmcp_server.py`)
- Faster development
- Modern patterns
- Better features

### For Existing Deployments

✅ **Run both side-by-side**
- Keep original on port 8001
- Test FastMCP on port 8003
- Gradual migration when ready

### For Learning

✅ **Study both implementations**
- Original shows MCP protocol details
- FastMCP shows high-level patterns
- Compare approaches

## 📚 Next Steps

1. **Try FastMCP server:**
   ```bash
   ./run-fastmcp.sh
   ```

2. **Run tests:**
   ```bash
   python test_fastmcp_server.py
   ```

3. **Compare results:**
   - Test same queries on both ports
   - Compare response times
   - Compare features

4. **Choose your approach:**
   - Stick with original (port 8001)
   - Switch to FastMCP (port 8003)
   - Run both (ports 8001 and 8003)

## 🤝 Support

For questions about the migration:
- Review this guide
- Check `README-FASTMCP.md`
- Compare code examples
- Test both servers

---

**Migration completed with zero changes to original code!**

