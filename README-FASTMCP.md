# Novitai Patent MCP Server - FastMCP Edition

🚀 **AI-powered patent analysis and search platform with FastMCP integration**

This is the FastMCP-enhanced version of the Novitai Patent MCP Server, providing all the capabilities of the original server with additional FastMCP features and improvements.

## 📋 Table of Contents

- [Overview](#overview)
- [What is FastMCP?](#what-is-fastmcp)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Available Tools](#available-tools)
- [Testing](#testing)
- [Deployment](#deployment)
- [Comparison: Original vs FastMCP](#comparison-original-vs-fastmcp)
- [Troubleshooting](#troubleshooting)

## 🌟 Overview

The FastMCP edition provides the same 4 powerful tools as the original server:

1. **Web Search Tool** - Search the web using Google Custom Search API
2. **Prior Art Search Tool** - Search patents using PatentsView API with AI-powered queries
3. **Claim Drafting Tool** - Generate patent claims using Azure OpenAI
4. **Claim Analysis Tool** - Analyze patent claims for quality and compliance

## 🔥 What is FastMCP?

FastMCP is a high-level Python framework for building Model Context Protocol (MCP) servers. It provides:

- ✅ **High-level decorator interface** - Simple `@mcp.tool` decorators
- ✅ **Automatic schema generation** - From Python type hints
- ✅ **Context-aware logging** - Built-in structured logging
- ✅ **SSE transport** - Better client compatibility
- ✅ **Production features** - Auth, streaming, error handling
- ✅ **90% less boilerplate** - Compared to low-level MCP implementations

## ✨ Features

### FastMCP-Specific Features

- 🎯 **Simplified API** - Clean decorator-based tool definitions
- 📡 **SSE Transport** - Server-Sent Events for better streaming
- 🔍 **Context Object** - Access to logging, progress, and utilities
- 🛡️ **Enhanced Error Handling** - Built-in error management
- 📊 **Automatic Validation** - Pydantic models for input validation
- 🚀 **Production Ready** - Deployment tools and configurations

### Core Capabilities

- 🌐 **Real-time Web Search** - Google Custom Search API integration
- 📚 **Patent Search** - PatentsView API with AI-powered query generation
- ✍️ **AI Claim Drafting** - Azure OpenAI-powered claim generation
- 🔍 **Claim Analysis** - Comprehensive patent claim evaluation
- 🔒 **Secure** - Environment-based API key management
- 📝 **Well Documented** - Comprehensive documentation and examples

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Azure OpenAI API access
- Google Custom Search API credentials
- PatentsView API key

### 1. Clone and Setup

```bash
# Navigate to project directory
cd novitai-patent-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-fastmcp.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```bash
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CSE_ID=your-custom-search-engine-id
GOOGLE_PATENT_CSE_ID=your-patent-search-engine-id
PATENTSVIEW_API_KEY=your-patentsview-api-key
```

### 3. Run the Server

```bash
# Option 1: Using the startup script (recommended)
chmod +x run-fastmcp.sh
./run-fastmcp.sh

# Option 2: Direct Python execution
python fastmcp_server.py
```

The server will start on `http://0.0.0.0:8003` with SSE transport.

## 📦 Installation

### Standard Installation

```bash
# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-fastmcp.txt
```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose-fastmcp.yml up --build

# Run only FastMCP server
docker-compose -f docker-compose-fastmcp.yml up novitai-fastmcp-server
```

## ⚙️ Configuration

### FastMCP Configuration (`fastmcp.json`)

```json
{
  "source": {
    "path": "fastmcp_server.py"
  },
  "environment": {
    "python": "3.9",
    "dependencies": ["fastmcp>=2.0.0", "..."]
  },
  "deployment": {
    "transport": "sse",
    "host": "0.0.0.0",
    "port": 8003,
    "log_level": "INFO"
  }
}
```

### Environment Variables

See `env.example` for all available configuration options.

## 🏃 Running the Server

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python fastmcp_server.py
```

### Production Mode

```bash
# Using Docker Compose
docker-compose -f docker-compose-fastmcp.yml up -d

# Or using the startup script
./run-fastmcp.sh
```

### Both Servers Side-by-Side

You can run both the original and FastMCP servers simultaneously:

```bash
# Terminal 1: Original server (port 8001)
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2: FastMCP server (port 8003)
source venv/bin/activate
python fastmcp_server.py
```

## 🛠️ Available Tools

### 1. Web Search Tool

Search the web using Google Custom Search API.

**Tool Name:** `web_search`

**Parameters:**
- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum results (1-10, default: 10)

**Example:**
```json
{
  "name": "web_search",
  "arguments": {
    "query": "patent search strategies",
    "max_results": 5
  }
}
```

### 2. Prior Art Search Tool

Search for prior art patents with AI-powered query generation.

**Tool Name:** `prior_art_search`

**Parameters:**
- `params` (object, required):
  - `query` (string, required): Search query (3-1000 characters)
  - `context` (string, optional): Additional context
  - `conversation_history` (string, optional): Conversation history
  - `max_results` (integer, optional): Maximum patents (1-100, default: 20)

**Example:**
```json
{
  "name": "prior_art_search",
  "arguments": {
    "params": {
      "query": "machine learning image classification",
      "max_results": 10
    }
  }
}
```

### 3. Claim Drafting Tool

Generate patent claims using AI.

**Tool Name:** `claim_drafting`

**Parameters:**
- `params` (object, required):
  - `user_query` (string, required): Invention description (min 10 characters)
  - `context` (string, optional): Additional context
  - `conversation_history` (string, optional): Conversation history

**Example:**
```json
{
  "name": "claim_drafting",
  "arguments": {
    "params": {
      "user_query": "A system for detecting objects in autonomous vehicles using neural networks"
    }
  }
}
```

### 4. Claim Analysis Tool

Analyze patent claims for quality and compliance.

**Tool Name:** `claim_analysis`

**Parameters:**
- `params` (object, required):
  - `claims` (array, required): List of claims to analyze
  - `analysis_type` (string, optional): "basic" or "detailed" (default: "basic")
  - `context` (string, optional): Additional context

**Example:**
```json
{
  "name": "claim_analysis",
  "arguments": {
    "params": {
      "claims": [
        {"claim_text": "A system comprising a processor..."}
      ],
      "analysis_type": "detailed"
    }
  }
}
```

## 🧪 Testing

### Run Test Suite

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python test_fastmcp_server.py
```

The test suite will:
1. ✅ Initialize MCP connection
2. ✅ List available tools
3. ✅ Test web search tool
4. ✅ Test prior art search tool
5. ✅ Test claim drafting tool
6. ✅ Test claim analysis tool

### Manual Testing

You can also test individual tools using curl:

```bash
# Initialize
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "Test Client", "version": "1.0.0"}
    }
  }'

# Call web search tool
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "web_search",
      "arguments": {
        "query": "patent search",
        "max_results": 3
      }
    }
  }'
```

## 🐳 Deployment

### Docker Deployment

```bash
# Build image
docker build -f Dockerfile.fastmcp -t novitai-patent-fastmcp:latest .

# Run container
docker run -d \
  --name novitai-fastmcp \
  -p 8003:8003 \
  --env-file .env \
  novitai-patent-fastmcp:latest
```

### Docker Compose Deployment

```bash
# Start all services
docker-compose -f docker-compose-fastmcp.yml up -d

# View logs
docker-compose -f docker-compose-fastmcp.yml logs -f

# Stop services
docker-compose -f docker-compose-fastmcp.yml down
```

### Production Considerations

1. **Environment Variables**: Use proper secret management (Azure Key Vault, etc.)
2. **Logging**: Configure structured logging with appropriate log levels
3. **Monitoring**: Add health checks and monitoring (Prometheus, etc.)
4. **Security**: Use HTTPS, implement rate limiting, add authentication
5. **Scaling**: Use container orchestration (Kubernetes, Azure Container Apps)

## 📊 Comparison: Original vs FastMCP

| Feature | Original Server | FastMCP Server |
|---------|----------------|----------------|
| **Port** | 8001 | 8003 |
| **Transport** | HTTP (JSON-RPC) | SSE (Server-Sent Events) |
| **Code Style** | Class-based | Decorator-based |
| **Lines of Code** | ~1000 lines | ~400 lines |
| **Schema Definition** | Manual JSON schemas | Automatic from type hints |
| **Error Handling** | Manual | Built-in with Context |
| **Logging** | structlog | FastMCP Context logging |
| **Deployment** | Custom Docker | FastMCP deployment tools |
| **Features** | Core MCP | Core MCP + FastMCP extras |

### When to Use Each

**Use Original Server (port 8001) when:**
- ✅ You need maximum control over implementation
- ✅ You want to understand MCP protocol internals
- ✅ You have specific custom requirements

**Use FastMCP Server (port 8003) when:**
- ✅ You want rapid development
- ✅ You prefer high-level abstractions
- ✅ You need FastMCP-specific features
- ✅ You want cleaner, more maintainable code

## 🔧 Troubleshooting

### Server won't start

```bash
# Check if port 8003 is available
lsof -i :8003

# Check environment variables
cat .env

# Check logs
tail -f logs/fastmcp_server.log
```

### API Key Issues

```bash
# Verify environment variables are loaded
python -c "from app.core.config import settings; print(settings.azure_openai_api_key)"
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-fastmcp.txt
```

### Tool Execution Failures

Check the server logs for detailed error messages:
```bash
# If running with Docker
docker-compose -f docker-compose-fastmcp.yml logs -f novitai-fastmcp-server

# If running directly
# Logs will appear in terminal
```

## 📚 Additional Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io)
- [Original Server Documentation](README.md)

## 🤝 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Check server logs
4. Create an issue with detailed information

## 📄 License

See LICENSE file for details.

---

**Built with ❤️ using FastMCP**

