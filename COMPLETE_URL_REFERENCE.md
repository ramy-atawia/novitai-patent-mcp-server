# Complete URL Reference - Novitai Patent MCP Server

## 🐳 Running Server

**Container:** `novitai-mcp-docker`  
**Status:** ✅ Running and Healthy  
**Port:** `8003:8003`  
**Image:** `novitai-mcp-server:local`

---

## 📡 Complete MCP URLs

### Primary Endpoint (Use This)
```
http://localhost:8003/mcp
```

**Protocol:** HTTP (JSON-RPC 2.0)  
**Method:** POST  
**Transport:** StreamableHTTP

---

## 🔧 Required Headers

```json
{
  "Content-Type": "application/json",
  "Accept": "application/json, text/event-stream"
}
```

---

## ✅ Example Usage

### 1. Initialize Connection
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
      "clientInfo": {"name": "test-client", "version": "1.0"}
    },
    "id": 1
  }'
```

**Important:** Extract `mcp-session-id` from response headers!

### 2. List Tools (With Session)
```bash
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'
```

### 3. Execute Tool
```bash
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "web_search",
      "arguments": {
        "query": "5G patents",
        "max_results": 5
      }
    },
    "id": 3
  }'
```

---

## 🎯 For Different Clients

### Cursor IDE
```
http://localhost:8003/mcp
```
*(Configured in ~/.cursor/mcp.json)*

### Docker Containers
```
http://host.docker.internal:8003/mcp
```

### Local Python Clients
```
http://localhost:8003/mcp
```

### Azure Deployment
```
https://your-app.azurecontainerapps.io/mcp
```

---

## 📊 Server Configuration

### mcp_server.py
```python
mcp.run(
    transport="http",
    host="0.0.0.0",
    port=8003
)
```

### Available Tools
1. **web_search** - Web search via Google API
2. **prior_art_search** - Patent search via PatentsView API
3. **claim_drafting** - AI-powered claim generation
4. **claim_analysis** - AI-powered claim evaluation

---

## 🔍 Health Check

**Note:** `/health` endpoint is not implemented.  
**Use:** Initialize connection to `/mcp` instead.

```bash
# Test if server is responding
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"health","version":"1.0"}},"id":1}'
```

---

## ✅ Status Summary

- ✅ Server running on port 8003
- ✅ Container healthy
- ✅ 4 tools available
- ✅ URLs configured correctly
- ✅ Ready for client connections

**Use this URL in your MCP client:**
```
http://localhost:8003/mcp
```

