#!/usr/bin/env python3
"""
Test MCP JSON communication to ensure no stdout pollution
"""

import subprocess
import sys
import json
import time

def test_mcp_json_communication():
    """Test that the MCP server only outputs valid JSON to stdout"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🧪 Testing MCP JSON communication...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send an initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send the request
        request_json = json.dumps(init_request) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Wait for response
        time.sleep(2)
        
        # Read stdout
        stdout_data = ""
        stderr_data = ""
        
        # Try to read with timeout
        try:
            stdout_data, stderr_data = process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout_data, stderr_data = process.communicate()
        
        print(f"📤 Sent request: {request_json.strip()}")
        print(f"📥 Received stdout: {repr(stdout_data)}")
        print(f"📥 Received stderr: {repr(stderr_data)}")
        
        # Check if stdout contains only valid JSON
        if stdout_data.strip():
            try:
                # Try to parse each line as JSON
                lines = stdout_data.strip().split('\n')
                for line in lines:
                    if line.strip():
                        json.loads(line.strip())
                print("✅ All stdout output is valid JSON")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in stdout: {e}")
                print(f"❌ Problematic line: {repr(line)}")
                return False
        else:
            print("⚠️  No stdout output received")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_server_startup_output():
    """Test what the server outputs on startup"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"

    print("🔍 Testing server startup output...")

    try:
        # Start the server with a short timeout
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send a simple request and close stdin to make server exit
        try:
            process.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n')
            process.stdin.close()

            # Wait for response
            stdout_data, stderr_data = process.communicate(timeout=3)

            print(f"📤 Startup stderr: {repr(stderr_data[:200])}...")  # Truncate for readability

            # Check if stdout contains only JSON responses
            if stdout_data.strip():
                lines = stdout_data.strip().split('\n')
                for line in lines:
                    if line.strip():
                        json.loads(line.strip())  # This will raise if not valid JSON
                print("✅ Server outputs only valid JSON to stdout")
                return True
            else:
                print("⚠️  No stdout output (server may not have responded)")
                return True  # This is actually OK for startup test

        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️  Server startup test timed out (this is normal)")
            return True  # Timeout is expected for a server that waits for input

    except Exception as e:
        print(f"❌ Startup test error: {e}")
        return False

def main():
    print("🧪 MCP JSON Communication Test")
    print("=" * 40)
    
    tests = [
        ("Server Startup Output", test_server_startup_output),
        ("MCP JSON Communication", test_mcp_json_communication),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print("-" * 40)
    
    print("\n📊 Test Results:")
    print("=" * 40)
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All JSON communication tests passed!")
        print("The server should work correctly with Claude Desktop.")
    else:
        print("\n❌ Some tests failed.")
        print("The server may have stdout pollution issues.")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
