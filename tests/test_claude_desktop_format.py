#!/usr/bin/env python3
"""
Test exact format that Claude Desktop expects
"""

import subprocess
import sys
import json

def test_claude_desktop_format():
    """Test the exact format Claude Desktop expects"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🧪 Testing Claude Desktop Format...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Test the exact sequence Claude Desktop uses
        test_cases = [
            {
                "name": "initialize",
                "request": {
                    "jsonrpc": "2.0",
                    "id": "1",  # Claude Desktop might use string IDs
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "experimental": {},
                            "sampling": {}
                        },
                        "clientInfo": {
                            "name": "Claude Desktop",
                            "version": "0.9.3"
                        }
                    }
                }
            },
            {
                "name": "initialized_notification",
                "request": {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                    "params": {}
                }
            },
            {
                "name": "tools/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": "2",
                    "method": "tools/list",
                    "params": {}
                }
            },
            {
                "name": "tools/call",
                "request": {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "tools/call",
                    "params": {
                        "name": "speak_text",
                        "arguments": {
                            "text": "Hello from Claude Desktop test"
                        }
                    }
                }
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📤 Testing {test_case['name']}...")
            
            # Send request
            request_json = json.dumps(test_case["request"]) + "\n"
            print(f"📤 Sending: {request_json.strip()}")
            
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response (skip notifications)
            if "notification" not in test_case["name"]:
                response_line = process.stdout.readline()
                print(f"📥 Received: {response_line.strip()}")
                
                try:
                    response = json.loads(response_line.strip())
                    
                    # Validate response structure
                    if "error" in response:
                        print(f"❌ Error response: {response['error']}")
                        return False
                    elif "result" in response:
                        print(f"✅ Success response")
                        
                        # Check specific fields for tools/call
                        if test_case["name"] == "tools/call":
                            result = response["result"]
                            if "content" not in result:
                                print(f"❌ Missing 'content' in tools/call result")
                                return False
                            if "isError" not in result:
                                print(f"❌ Missing 'isError' in tools/call result")
                                return False
                            if not isinstance(result["content"], list):
                                print(f"❌ 'content' must be an array")
                                return False
                            if not isinstance(result["isError"], bool):
                                print(f"❌ 'isError' must be a boolean")
                                return False
                    else:
                        print(f"❌ Response missing 'result' or 'error'")
                        return False
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON response: {e}")
                    return False
            else:
                print(f"✅ Notification sent (no response expected)")
        
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
    print("🎯 Claude Desktop Format Test")
    print("=" * 40)
    
    if test_claude_desktop_format():
        print("\n🎉 All Claude Desktop format tests passed!")
        print("The server should work correctly with Claude Desktop.")
        return 0
    else:
        print("\n❌ Some Claude Desktop format tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
