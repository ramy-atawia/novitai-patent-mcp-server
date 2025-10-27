# Complete MCP Server URLs

## 🐳 Local Docker Server

### Health Check
```
http://localhost:8003/health
```

### MCP Endpoint
```
http://localhost:8003/mcp
```

### For Clients Inside Docker Containers
```
http://host.docker.internal:8003/mcp
```

---

## 📡 Connection Details

### MCP Protocol
- **Transport**: HTTP (StreamableHTTP)
- **Protocol**: JSON-RPC 2.0
- **Method**: POST

### Required Headers
```json
{
  "Content-Type": "application/json",
  "Accept": "application/json, text/event-stream"
}
```

### Session Management
1. **First Request**: Send without `mcp-session-id` header
2. **Extract Session**: Get `mcp-session-id` from response headers
3. **Subsequent Requests**: Include `mcp-session-id` in all requests

---

## 🔧 Example Usage

### Initialize (First Request)
```bash
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "my-client", "version": "1.0"}
    },
    "id": 1
  }'
```

**Response Header:**
```
mcp-session-id: abc123...
```

### List Tools (With Session)
```bash
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: abc123..." \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'
```

---

## 📊 Container Status

```bash
# Check container status
docker ps | grep novitai-mcp-docker

# View logs
docker logs novitai-mcp-docker -f

# Stop container
docker stop novitai-mcp-docker

# Start container
docker start novitai-mcp-docker

# Restart container
docker restart novitai-mcp-docker
```

---

## 🌐 Available Endpoints

| Endpoint | URL | Method | Description |
|----------|-----|--------|-------------|
| MCP | `http://localhost:8003/mcp` | POST | Main MCP protocol endpoint |
| Health | `http://localhost:8003/health` | GET | Health check (Note: Not implemented yet) |

---

## ✅ Server Status

**Container**: novitai-mcp-docker  
**Status**: ✅ Running and Healthy  
**Port**: 8003:8003  
**Image**: novitai-mcp-server:local

**URL to use in MCP clients:**
```
http://localhost:8003/mcp
```

