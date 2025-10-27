# Novitai Patent MCP Server

A Model Context Protocol (MCP) server providing patent-related tools including web search, prior art search, patent claim drafting, and patent claim analysis.

## Features

- **Web Search Tool**: Search the web for patent research using Google Custom Search API
- **Prior Art Search Tool**: Search for prior art patents using PatentsView API with comprehensive markdown reports
- **Claim Drafting Tool**: Draft patent claims based on invention descriptions using LLM
- **Claim Analysis Tool**: Analyze patent claims for validity, quality, and improvement opportunities using LLM

## Architecture

The server is built using:
- **FastAPI**: Web framework for the MCP server
- **Azure OpenAI**: LLM integration for claim drafting and analysis
- **Google Custom Search API**: Web search functionality
- **PatentsView API**: Patent database access
- **Docker**: Containerized deployment
- **Azure Container Apps**: Cloud deployment platform

## Quick Start

### Prerequisites

- Python 3.12+
- Azure OpenAI API key
- Google Custom Search API key and CSE ID
- PatentsView API key (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd novitai-patent-mcp-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the server**
   ```bash
   python mcp_server.py
   ```

5. **Test the server**
   ```bash
   # Health check
   curl http://localhost:8003/health
   
   # MCP endpoint
   curl http://localhost:8003/mcp
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t novitai-mcp-server:local .
   ```

2. **Run the container**
   ```bash
   docker run -d --name novitai-mcp-docker -p 8003:8003 --env-file .env novitai-mcp-server:local
   ```

3. **Test the server**
   ```bash
   # For local clients
   curl http://localhost:8003/health
   
   # For clients inside Docker containers
   curl http://host.docker.internal:8003/mcp
   ```

4. **Check logs**
   ```bash
   docker logs novitai-mcp-docker
   ```

5. **Stop the container**
   ```bash
   docker stop novitai-mcp-docker && docker rm novitai-mcp-docker
   ```

### Azure Container Apps Deployment

1. **Prerequisites**
   - Azure CLI installed and logged in
   - Azure Container Registry
   - Resource group created

2. **Deploy to Azure**
   ```bash
   cd azure-deployment
   ./deploy.sh dev your-resource-group eastus2 your-acr-name
   ```

3. **Update parameters**
   - Edit `parameters.dev.json` with your API keys
   - Update container registry name if needed

## Environment Variables

### Required
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your Azure OpenAI deployment name

### Optional
- `GOOGLE_API_KEY`: Google Custom Search API key
- `GOOGLE_CSE_ID`: Google Custom Search Engine ID
- `PATENTSVIEW_API_KEY`: PatentsView API key
- `PORT`: Server port (default: 8003)
- `LOG_LEVEL`: Logging level (default: INFO)

## MCP Protocol

The server implements the Model Context Protocol (MCP) specification and provides the following endpoints:

- `POST /mcp`: Main MCP protocol endpoint (Streamable HTTP)
- `GET /health`: Health check endpoint

### Connection URLs

- **Local access**: `http://localhost:8003/mcp`
- **Docker-internal access**: `http://host.docker.internal:8003/mcp`
- **Azure deployment**: `https://your-app.azurecontainerapps.io/mcp`

### Available Tools

1. **web_search_tool**
   - Search the web for information
   - Parameters: `query`, `max_results`

2. **prior_art_search_tool**
   - Search for prior art patents
   - Parameters: `query`, `max_results`, `context`, `conversation_history`

3. **claim_drafting_tool**
   - Draft patent claims
   - Parameters: `user_query`, `conversation_context`, `document_reference`

4. **claim_analysis_tool**
   - Analyze patent claims
   - Parameters: `claims`, `analysis_type`, `focus_areas`

## API Usage

### Initialize Connection
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "test-client",
      "version": "1.0.0"
    }
  }
}
```

### List Tools
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

### Execute Tool
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "web_search_tool",
    "arguments": {
      "query": "patent search",
      "max_results": 5
    }
  }
}
```

## Development

### Project Structure
```
app/
├── core/           # Configuration and core utilities
├── mcp_tools/      # MCP tool implementations
├── services/       # External service integrations
├── utils/          # Utility functions
├── prompts/        # LLM prompt templates
└── main.py         # Main FastAPI application
```

### Adding New Tools

1. Create a new tool class in `app/mcp_tools/`
2. Inherit from `BaseMCPTool`
3. Implement the `execute` method
4. Add the tool to the tools dictionary in `main.py`

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.




