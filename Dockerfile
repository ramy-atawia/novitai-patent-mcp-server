# Multi-stage Dockerfile for FastMCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements-fixed.txt requirements-fastmcp-fixed.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-fixed.txt -r requirements-fastmcp-fixed.txt

# Copy application files
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/mcp || exit 1

# Run the FastMCP server
CMD ["python", "fastmcp_server.py"]
