# FastMCP Quick Start - 5 Minutes

## ⚡ Get FastMCP Running in 3 Commands

```bash
# 1. Install FastMCP (30 seconds)
pip install -r requirements-fastmcp.txt

# 2. Start server (instantly)
python fastmcp_server.py

# 3. Test it (30 seconds)
# In another terminal:
python test_fastmcp_server.py
```

## 🎯 What You Get

- ✅ Same 4 tools as original server
- ✅ Better code (61% less)
- ✅ SSE transport (better streaming)
- ✅ Port 8003 (original on 8001)
- ✅ Zero changes to original code

## 📍 Server Locations

| Server | Port | Command |
|--------|------|---------|
| **Original** | 8001 | `python -m uvicorn app.main:app --port 8001` |
| **FastMCP** | 8003 | `python fastmcp_server.py` |

## 🛠️ Available Tools (Same 4 Tools)

1. **web_search** - Google web search
2. **prior_art_search** - Patent search
3. **claim_drafting** - AI claim generation
4. **claim_analysis** - Claim evaluation

## 📞 Quick Test

```bash
# Test web search
curl -X POST http://localhost:8003/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "web_search",
      "arguments": {"query": "patent search", "max_results": 3}
    }
  }'
```

## 🐳 Docker (One Command)

```bash
docker-compose -f docker-compose-fastmcp.yml up --build
```

This runs both servers:
- Original: http://localhost:8001
- FastMCP: http://localhost:8003

## 📚 Full Documentation

- `README-FASTMCP.md` - Complete guide
- `MIGRATION-GUIDE.md` - Architecture & comparison
- `FASTMCP-SUMMARY.md` - Implementation details

## 🚀 That's It!

Your FastMCP server is running on port 8003 with all 4 tools ready to use!

