#!/usr/bin/env python3
"""
Simple test for MCP Audio Server
"""

import json
import sys
import os

# Suppress pygame messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_server import MCPAudioServer, handle_json_rpc_request

def test_direct_calls():
    """Test direct function calls"""
    print("🧪 Testing MCP Audio Server - Direct Calls")
    print("=" * 50)
    
    # Initialize server
    server = MCPAudioServer()
    print("✅ Server initialized")
    
    # Test 1: List tools
    print("\n1️⃣ Testing list_tools()...")
    tools = server.list_tools()
    print(f"   Found {len(tools['tools'])} tools:")
    for tool in tools['tools']:
        print(f"   • {tool['name']}")
    
    # Test 2: Get audio status
    print("\n2️⃣ Testing get_audio_status...")
    status = server.call_tool("get_audio_status", {})
    print(f"   TTS Available: {status.get('status', {}).get('tts_available', 'Unknown')}")
    print(f"   Audio System: {status.get('status', {}).get('pygame_available', 'Unknown')}")
    
    # Test 3: Text-to-speech
    print("\n3️⃣ Testing speak_text...")
    result = server.call_tool("speak_text", {
        "text": "Testing MCP Audio Server functionality",
        "volume": 0.6
    })
    print(f"   Result: {result.get('success', False)}")
    if result.get('success'):
        print(f"   Message: {result.get('message', '')}")
    else:
        print(f"   Error: {result.get('error', '')}")
    
    # Test 4: Stop audio
    print("\n4️⃣ Testing stop_audio...")
    result = server.call_tool("stop_audio", {})
    print(f"   Result: {result.get('success', False)}")
    
    print("\n✅ Direct call tests completed!")

def test_json_rpc_requests():
    """Test JSON-RPC request handling"""
    print("\n🔗 Testing JSON-RPC Request Handling")
    print("=" * 50)
    
    # Test 1: List tools request
    print("\n1️⃣ Testing tools/list request...")
    request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
    response = handle_json_rpc_request(json.dumps(request))
    print("   Request sent successfully")
    try:
        response_obj = json.loads(response)
        print(f"   Response ID: {response_obj.get('id')}")
        print(f"   Tools count: {len(response_obj.get('result', {}).get('tools', []))}")
    except:
        print("   Response parsing failed")
    
    # Test 2: Speak text request
    print("\n2️⃣ Testing speak_text request...")
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "speak_text",
            "arguments": {
                "text": "Hello from JSON-RPC!",
                "rate": 120
            }
        },
        "id": 2
    }
    response = handle_json_rpc_request(json.dumps(request))
    print("   Request sent successfully")
    try:
        response_obj = json.loads(response)
        print(f"   Response ID: {response_obj.get('id')}")
        print(f"   Success: {response_obj.get('result', {}).get('success', False)}")
    except:
        print("   Response parsing failed")
    
    # Test 3: Invalid method request
    print("\n3️⃣ Testing invalid method...")
    request = {
        "jsonrpc": "2.0",
        "method": "invalid/method",
        "id": 3
    }
    response = handle_json_rpc_request(json.dumps(request))
    print("   Request sent successfully")
    try:
        response_obj = json.loads(response)
        print(f"   Response ID: {response_obj.get('id')}")
        print(f"   Success: {response_obj.get('result', {}).get('success', False)}")
        if not response_obj.get('result', {}).get('success', True):
            print(f"   Error (expected): {response_obj.get('result', {}).get('error', '')}")
    except:
        print("   Response parsing failed")
    
    print("\n✅ JSON-RPC tests completed!")

if __name__ == "__main__":
    try:
        test_direct_calls()
        test_json_rpc_requests()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
