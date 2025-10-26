#!/bin/bash

# FastMCP Server Startup Script
# This script helps you quickly start the FastMCP server

set -e

echo "======================================================================"
echo "  Novitai Patent MCP Server - FastMCP Edition Startup"
echo "======================================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "📝 Please create .env file from env.example"
    echo ""
    echo "   cp env.example .env"
    echo "   # Then edit .env with your API keys"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if FastMCP is installed
if ! python -c "import fastmcp" 2>/dev/null; then
    echo "📦 Installing FastMCP dependencies..."
    pip install -r requirements.txt
    pip install -r requirements-fastmcp.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Display configuration
echo "⚙️  Configuration:"
echo "   - Transport: SSE (Server-Sent Events)"
echo "   - Host: 0.0.0.0"
echo "   - Port: 8003"
echo ""

# Start the server
echo "🚀 Starting FastMCP server..."
echo ""
python fastmcp_server.py

