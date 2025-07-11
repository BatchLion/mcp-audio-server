#!/usr/bin/env python3
"""
Test all MCP methods to ensure Claude Desktop compatibility
"""

import subprocess
import sys
import json

def test_all_mcp_methods():
    """Test all MCP methods that Claude Desktop expects"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🧪 Testing All MCP Methods...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Test methods that Claude Desktop calls
        test_methods = [
            {
                "name": "initialize",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"}
                    }
                },
                "expected_key": "protocolVersion"
            },
            {
                "name": "tools/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                },
                "expected_key": "tools"
            },
            {
                "name": "resources/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "resources/list",
                    "params": {}
                },
                "expected_key": "resources"
            },
            {
                "name": "prompts/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "prompts/list",
                    "params": {}
                },
                "expected_key": "prompts"
            },
            {
                "name": "tools/call (speak_text)",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "speak_text",
                        "arguments": {"text": "Test message"}
                    }
                },
                "expected_key": "content"
            },
            {
                "name": "tools/call (list_voices)",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "tools/call",
                    "params": {
                        "name": "list_voices",
                        "arguments": {}
                    }
                },
                "expected_key": "content"
            }
        ]
        
        all_passed = True
        
        for test in test_methods:
            print(f"📤 Testing {test['name']}...")
            
            # Send request
            request_json = json.dumps(test["request"]) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            response = json.loads(response_line.strip())
            
            # Check response
            result = response.get("result", {})
            if test["expected_key"] in result:
                print(f"✅ {test['name']} successful")
                
                # Special handling for different response types
                if test["name"] == "tools/list":
                    tools = result.get("tools", [])
                    print(f"   Found {len(tools)} tools")
                    if len(tools) != 5:
                        print(f"   ❌ Expected 5 tools, but found {len(tools)}")
                        all_passed = False
                elif test["name"] == "resources/list":
                    resources = result.get("resources", [])
                    print(f"   Found {len(resources)} resources")
                elif test["name"] == "prompts/list":
                    prompts = result.get("prompts", [])
                    print(f"   Found {len(prompts)} prompts")
                elif test["name"].startswith("tools/call"):
                    content = result.get("content", [])
                    if content and not result.get("isError", False):
                        print(f"   Response: {content[0].get('text', '')[:100]}...")
                    
            else:
                print(f"❌ {test['name']} failed: {response}")
                all_passed = False
        
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        if 'process' in locals():
            try:
                process.kill()
            except:
                pass
        return False

def main():
    print("🎯 Complete MCP Method Test")
    print("=" * 40)
    
    if test_all_mcp_methods():
        print("\n🎉 All MCP methods work correctly!")
        print("\n📋 Now restart Claude Desktop:")
        print("1. Completely quit Claude Desktop (Cmd+Q)")
        print("2. Wait 10 seconds")
        print("3. Restart Claude Desktop")
        print("4. The error messages should be gone!")
        return 0
    else:
        print("\n❌ Some MCP methods failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
