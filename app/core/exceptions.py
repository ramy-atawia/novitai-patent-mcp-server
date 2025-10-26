"""
Custom exceptions for the Novitai Patent MCP Server.
"""


class MCPError(Exception):
    """Base exception for MCP-related errors."""
    pass


class ToolNotFoundError(MCPError):
    """Raised when a requested tool is not found."""
    pass


class ValidationError(MCPError):
    """Raised when input validation fails."""
    pass


class ToolExecutionError(MCPError):
    """Raised when tool execution fails."""
    pass


class ExternalMCPServerError(MCPError):
    """Raised when external MCP server operations fail."""
    pass


class LLMError(MCPError):
    """Raised when LLM operations fail."""
    pass


class APIConnectionError(MCPError):
    """Raised when external API connections fail."""
    pass


class ConfigurationError(MCPError):
    """Raised when configuration is invalid or missing."""
    pass




