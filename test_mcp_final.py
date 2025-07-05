#!/usr/bin/env python3
"""
Final test for MCP Audio Server
"""

import subprocess
import sys
import json
import time

def test_mcp_protocol():
    """Test MCP protocol communication"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🧪 Testing MCP Protocol Communication...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Test 1: Initialize
        print("📤 Testing initialize...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        response = json.loads(response_line.strip())
        
        if response.get("result", {}).get("protocolVersion") == "2024-11-05":
            print("✅ Initialize successful")
        else:
            print(f"❌ Initialize failed: {response}")
            return False
        
        # Test 2: List tools
        print("📤 Testing tools/list...")
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(list_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        response = json.loads(response_line.strip())
        
        tools = response.get("result", {}).get("tools", [])
        if len(tools) > 0:
            print(f"✅ Found {len(tools)} tools")
            for tool in tools:
                print(f"   - {tool.get('name')}: {tool.get('description')}")
        else:
            print("❌ No tools found")
            return False
        
        # Test 3: Call speak_text tool
        print("📤 Testing tools/call (speak_text)...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "speak_text",
                "arguments": {
                    "text": "Hello from MCP Audio Server test!"
                }
            }
        }
        
        process.stdin.write(json.dumps(call_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        response = json.loads(response_line.strip())

        result = response.get("result", {})
        # Check for new MCP format with content array
        if "content" in result:
            if not result.get("isError", False):
                print("✅ speak_text tool executed successfully")
                content = result.get("content", [])
                if content and len(content) > 0:
                    print(f"   Response: {content[0].get('text', '')}")
            else:
                print(f"❌ speak_text tool failed: {result}")
                return False
        # Check for old format with success field
        elif result.get("success"):
            print("✅ speak_text tool executed successfully")
        else:
            print(f"❌ speak_text tool failed: {response}")
            return False
        
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

        return True

    except Exception as e:
        print(f"❌ Test error: {e}")
        if 'process' in locals():
            try:
                process.kill()
            except:
                pass
        return False

def main():
    print("🎯 MCP Audio Server Final Test")
    print("=" * 40)
    
    if test_mcp_protocol():
        print("\n🎉 All MCP protocol tests passed!")
        print("\n📋 The audio server is ready for Claude Desktop:")
        print("1. Completely quit Claude Desktop (Cmd+Q)")
        print("2. Wait 10 seconds")
        print("3. Restart Claude Desktop")
        print("4. Wait for MCP servers to initialize")
        print("5. Test with: 'Please use speech to say Hello World'")
        return 0
    else:
        print("\n❌ MCP protocol tests failed!")
        print("Please check the server implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
