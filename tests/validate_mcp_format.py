#!/usr/bin/env python3
"""
Validate MCP response format against specification
"""

import subprocess
import sys
import json

def validate_response_format(response, method_name):
    """Validate that response matches MCP specification"""
    print(f"🔍 Validating {method_name} response format...")
    
    # Check basic JSON-RPC structure
    if "jsonrpc" not in response:
        print(f"❌ Missing 'jsonrpc' field")
        return False
    
    if response["jsonrpc"] != "2.0":
        print(f"❌ Invalid jsonrpc version: {response['jsonrpc']}")
        return False
    
    if "id" not in response:
        print(f"❌ Missing 'id' field")
        return False
    
    if "result" not in response and "error" not in response:
        print(f"❌ Missing 'result' or 'error' field")
        return False
    
    # Method-specific validation
    if method_name == "initialize":
        result = response.get("result", {})
        required_fields = ["protocolVersion", "capabilities", "serverInfo"]
        for field in required_fields:
            if field not in result:
                print(f"❌ Missing required field '{field}' in initialize result")
                return False
        
        # Check capabilities structure
        capabilities = result.get("capabilities", {})
        if "tools" not in capabilities:
            print(f"❌ Missing 'tools' capability")
            return False
            
        tools_cap = capabilities["tools"]
        if not isinstance(tools_cap, dict):
            print(f"❌ 'tools' capability must be an object")
            return False
    
    elif method_name == "tools/list":
        result = response.get("result", {})
        if "tools" not in result:
            print(f"❌ Missing 'tools' field in tools/list result")
            return False
        
        tools = result["tools"]
        if not isinstance(tools, list):
            print(f"❌ 'tools' must be an array")
            return False
        
        # Validate each tool
        for i, tool in enumerate(tools):
            required_tool_fields = ["name", "description", "inputSchema"]
            for field in required_tool_fields:
                if field not in tool:
                    print(f"❌ Tool {i} missing required field '{field}'")
                    return False
    
    elif method_name == "tools/call":
        result = response.get("result", {})
        if "content" not in result:
            print(f"❌ Missing 'content' field in tools/call result")
            return False
        
        content = result["content"]
        if not isinstance(content, list):
            print(f"❌ 'content' must be an array")
            return False
        
        # Validate content items
        for i, item in enumerate(content):
            if "type" not in item:
                print(f"❌ Content item {i} missing 'type' field")
                return False
            
            if item["type"] == "text" and "text" not in item:
                print(f"❌ Text content item {i} missing 'text' field")
                return False
        
        # Check isError field
        if "isError" not in result:
            print(f"❌ Missing 'isError' field in tools/call result")
            return False
        
        if not isinstance(result["isError"], bool):
            print(f"❌ 'isError' must be a boolean")
            return False
    
    elif method_name in ["resources/list", "prompts/list"]:
        result = response.get("result", {})
        expected_field = method_name.split("/")[0]  # "resources" or "prompts"
        
        if expected_field not in result:
            print(f"❌ Missing '{expected_field}' field in {method_name} result")
            return False
        
        items = result[expected_field]
        if not isinstance(items, list):
            print(f"❌ '{expected_field}' must be an array")
            return False
    
    print(f"✅ {method_name} response format is valid")
    return True

def test_mcp_format_validation():
    """Test MCP format validation"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🧪 Testing MCP Format Validation...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Test methods
        test_cases = [
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
                }
            },
            {
                "name": "tools/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }
            },
            {
                "name": "resources/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "resources/list",
                    "params": {}
                }
            },
            {
                "name": "prompts/list",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "prompts/list",
                    "params": {}
                }
            },
            {
                "name": "tools/call",
                "request": {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "speak_text",
                        "arguments": {"text": "Test validation"}
                    }
                }
            }
        ]
        
        all_valid = True
        
        for test_case in test_cases:
            print(f"\n📤 Testing {test_case['name']}...")
            
            # Send request
            request_json = json.dumps(test_case["request"]) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            response = json.loads(response_line.strip())
            
            # Validate format
            if not validate_response_format(response, test_case["name"]):
                all_valid = False
            
            print(f"📥 Response: {json.dumps(response, indent=2)[:200]}...")
        
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        
        return all_valid
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        if 'process' in locals():
            try:
                process.kill()
            except:
                pass
        return False

def main():
    print("🎯 MCP Format Validation Test")
    print("=" * 40)
    
    if test_mcp_format_validation():
        print("\n🎉 All MCP response formats are valid!")
        print("The server should work correctly with Claude Desktop.")
        return 0
    else:
        print("\n❌ Some response formats are invalid!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
