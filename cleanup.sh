#!/bin/bash
# Cleanup script for Novitai Patent MCP Server
# Removes obsolete files after FastMCP migration

echo "🧹 Starting cleanup of obsolete files..."

# Create archive directory for documentation
mkdir -p archive/migration-docs

# Move documentation files to archive
echo "📁 Archiving migration documentation..."
mv MIGRATION-GUIDE.md archive/migration-docs/
mv FASTMCP-SUMMARY.md archive/migration-docs/
mv QUICK-START-FASTMCP.md archive/migration-docs/
mv TESTING-SUMMARY.md archive/migration-docs/
mv COMPREHENSIVE-REVIEW.md archive/migration-docs/

# Remove obsolete requirements files
echo "🗑️ Removing obsolete requirements files..."
rm -f requirements.txt
rm -f requirements-fastmcp.txt

# Remove old Docker files
echo "🐳 Removing old Docker files..."
rm -f Dockerfile
rm -f Dockerfile.fastmcp
rm -f docker-compose.yml

# Remove debug and test files
echo "🧪 Removing debug and test files..."
rm -f debug_test.py
rm -f simple_debug.py
rm -f comprehensive_test.py
rm -f validate_fastmcp.py
rm -f test_mcp_server.py

# Remove old implementation files
echo "⚙️ Removing old implementation files..."
rm -f fastmcp_proxy.py
rm -f run-fastmcp.sh

# Remove miscellaneous files
echo "📄 Removing miscellaneous files..."
rm -f gitrelated

# Remove old virtual environment
echo "🐍 Removing old Python 3.9 virtual environment..."
rm -rf venv/

# Clean up Python cache
echo "🧽 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Cleanup completed!"
echo ""
echo "📊 Summary:"
echo "  - Archived migration documentation to archive/migration-docs/"
echo "  - Removed obsolete requirements files"
echo "  - Removed old Docker configurations"
echo "  - Removed debug and test files"
echo "  - Removed old virtual environment"
echo "  - Cleaned Python cache"
echo ""
echo "🎯 Current active files:"
echo "  - fastmcp_server.py (main FastMCP server)"
echo "  - requirements-fixed.txt (working dependencies)"
echo "  - Dockerfile.fastmcp-simple (working Docker setup)"
echo "  - docker-compose-fastmcp.yml (Docker Compose)"
echo "  - app/ (core application code)"
echo ""
echo "📁 Archived files available in archive/migration-docs/ for reference"
