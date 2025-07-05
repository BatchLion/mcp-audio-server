#!/usr/bin/env python3
"""
Test JSON-RPC interface for MCP Audio Server
"""

import json
import subprocess
import sys
import time

def test_json_rpc():
    """Test the JSON-RPC interface"""
    print("🧪 Testing MCP Audio Server JSON-RPC Interface")
    print("=" * 50)
    
    # Start the audio server process
    print("🚀 Starting audio server...")
    process = subprocess.Popen(
        [sys.executable, "audio_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    def send_request(method, params=None, request_id=1):
        """Send a JSON-RPC request"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": request_id
        }
        if params:
            request["params"] = params
        
        request_json = json.dumps(request)
        print(f"📤 Sending: {request_json}")
        
        process.stdin.write(request_json + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            print(f"📥 Response: {response_line.strip()}")
            try:
                response = json.loads(response_line)
                return response
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return None
        else:
            print("❌ No response received")
            return None
    
    try:
        # Test 1: List tools
        print("\n1️⃣ Testing tools/list...")
        response = send_request("tools/list")
        
        # Test 2: Call speak_text tool
        print("\n2️⃣ Testing speak_text tool...")
        response = send_request("tools/call", {
            "name": "speak_text",
            "arguments": {
                "text": "Hello from JSON-RPC interface!",
                "volume": 0.7
            }
        })
        
        # Test 3: Get audio status
        print("\n3️⃣ Testing get_audio_status tool...")
        response = send_request("tools/call", {
            "name": "get_audio_status",
            "arguments": {}
        })
        
        # Test 4: Stop audio
        print("\n4️⃣ Testing stop_audio tool...")
        response = send_request("tools/call", {
            "name": "stop_audio",
            "arguments": {}
        })
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_json_rpc()
