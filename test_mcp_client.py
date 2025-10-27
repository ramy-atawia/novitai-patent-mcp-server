#!/usr/bin/env python3
"""
FastMCP Client Test Script

This script demonstrates how to properly connect to the FastMCP server.
Use this as a reference for your other client implementation.
"""

import requests
import json

# Server URL
SERVER_URL = "http://localhost:8003/mcp"

def test_fastmcp_connection():
    """Test connection to FastMCP server with proper session handling"""
    
    # Step 1: Initialize without session ID
    print("Step 1: Sending initialize request...")
    init_payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0"
            }
        },
        "id": 1
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    try:
        response = requests.post(SERVER_URL, headers=headers, json=init_payload, stream=True)
        
        # Check if we got a session ID in the headers
        session_id = response.headers.get("mcp-session-id")
        
        if session_id:
            print(f"✅ Session ID received: {session_id}")
            
            # Step 2: List tools with session ID
            print("\nStep 2: Requesting tools list with session ID...")
            tools_payload = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 2
            }
            
            headers_with_session = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": session_id
            }
            
            response2 = requests.post(SERVER_URL, headers=headers_with_session, json=tools_payload, stream=True)
            
            if response2.status_code == 200:
                print("✅ Tools list request successful!")
                # Try to read the SSE response
                for line in response2.iter_lines():
                    if line:
                        print(f"Response: {line.decode('utf-8')}")
                        if 'tools' in line.decode('utf-8').lower():
                            break
            else:
                print(f"❌ Tools list failed: {response2.status_code}")
                print(response2.text)
        else:
            print(f"❌ No session ID received. Status: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_fastmcp_connection()

