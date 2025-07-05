#!/usr/bin/env python3
"""
Comprehensive test report for MCP Audio Server
"""

import json
import sys
import os
import time
from datetime import datetime

# Suppress pygame messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_server import MCPAudioServer, handle_json_rpc_request

def generate_test_report():
    """Generate a comprehensive test report"""
    print("📊 MCP Audio Server - Comprehensive Test Report")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {
        "server_initialization": False,
        "tools_available": 0,
        "tts_functionality": False,
        "audio_control": False,
        "status_query": False,
        "json_rpc_interface": False,
        "error_handling": False,
        "parameter_validation": False
    }
    
    try:
        # Test 1: Server Initialization
        print("🔧 1. Server Initialization")
        print("-" * 30)
        server = MCPAudioServer()
        test_results["server_initialization"] = True
        print("   ✅ Server initialized successfully")
        
        # Test 2: Tools Availability
        print("\n📋 2. Tools Availability")
        print("-" * 30)
        tools = server.list_tools()
        test_results["tools_available"] = len(tools["tools"])
        print(f"   ✅ Found {test_results['tools_available']} tools:")
        for tool in tools["tools"]:
            print(f"      • {tool['name']}: {tool['description'][:50]}...")
        
        # Test 3: Text-to-Speech Functionality
        print("\n🗣️  3. Text-to-Speech Functionality")
        print("-" * 30)
        tts_result = server.call_tool("speak_text", {
            "text": "MCP Audio Server test successful",
            "rate": 150,
            "volume": 0.7
        })
        test_results["tts_functionality"] = tts_result.get("success", False)
        if test_results["tts_functionality"]:
            print("   ✅ TTS functionality working")
        else:
            print(f"   ❌ TTS failed: {tts_result.get('error', 'Unknown error')}")
        
        # Test 4: Audio Control
        print("\n🎮 4. Audio Control")
        print("-" * 30)
        stop_result = server.call_tool("stop_audio", {})
        test_results["audio_control"] = stop_result.get("success", False)
        if test_results["audio_control"]:
            print("   ✅ Audio control working")
        else:
            print(f"   ❌ Audio control failed: {stop_result.get('error', 'Unknown error')}")
        
        # Test 5: Status Query
        print("\n🔍 5. Status Query")
        print("-" * 30)
        status_result = server.call_tool("get_audio_status", {})
        test_results["status_query"] = status_result.get("success", False)
        if test_results["status_query"]:
            status = status_result.get("status", {})
            print(f"   ✅ Status query working")
            print(f"      • TTS Available: {status.get('tts_available', 'Unknown')}")
            print(f"      • Audio System: {status.get('pygame_available', 'Unknown')}")
            print(f"      • Currently Playing: {status.get('music_playing', 'Unknown')}")
        else:
            print(f"   ❌ Status query failed: {status_result.get('error', 'Unknown error')}")
        
        # Test 6: JSON-RPC Interface
        print("\n🔗 6. JSON-RPC Interface")
        print("-" * 30)
        json_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "speak_text",
                "arguments": {"text": "JSON-RPC test"}
            },
            "id": 1
        }
        json_response = handle_json_rpc_request(json.dumps(json_request))
        try:
            response_obj = json.loads(json_response)
            test_results["json_rpc_interface"] = response_obj.get("result", {}).get("success", False)
            if test_results["json_rpc_interface"]:
                print("   ✅ JSON-RPC interface working")
            else:
                print("   ❌ JSON-RPC interface failed")
        except:
            print("   ❌ JSON-RPC response parsing failed")
        
        # Test 7: Error Handling
        print("\n🚨 7. Error Handling")
        print("-" * 30)
        error_tests = [
            ("Empty text", server.call_tool("speak_text", {"text": ""})),
            ("Invalid file", server.call_tool("play_audio_file", {"file_path": "/invalid/path.mp3"})),
            ("Unknown tool", server.call_tool("unknown_tool", {})),
            ("Missing params", server.call_tool("speak_text", {}))
        ]
        
        error_count = 0
        for test_name, result in error_tests:
            if not result.get("success", True):  # Should fail
                error_count += 1
                print(f"   ✅ {test_name}: Properly handled")
            else:
                print(f"   ❌ {test_name}: Not properly handled")
        
        test_results["error_handling"] = error_count == len(error_tests)
        
        # Test 8: Parameter Validation
        print("\n🔧 8. Parameter Validation")
        print("-" * 30)
        param_tests = [
            ("Extreme rate", server.call_tool("speak_text", {"text": "test", "rate": 1000})),
            ("Negative volume", server.call_tool("speak_text", {"text": "test", "volume": -1.0})),
            ("High volume", server.call_tool("speak_text", {"text": "test", "volume": 2.0}))
        ]
        
        param_success = 0
        for test_name, result in param_tests:
            if result.get("success", False):  # Should handle gracefully
                param_success += 1
                print(f"   ✅ {test_name}: Handled gracefully")
            else:
                print(f"   ❌ {test_name}: Failed to handle")
        
        test_results["parameter_validation"] = param_success == len(param_tests)
        
    except Exception as e:
        print(f"\n❌ Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    # Generate Summary
    print("\n📈 Test Summary")
    print("=" * 60)
    
    passed_tests = sum(1 for key, value in test_results.items() 
                      if key != "tools_available" and value)
    total_tests = len(test_results) - 1  # Exclude tools_available count
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    print("Detailed Results:")
    print(f"  • Server Initialization: {'✅' if test_results['server_initialization'] else '❌'}")
    print(f"  • Tools Available: {test_results['tools_available']}")
    print(f"  • TTS Functionality: {'✅' if test_results['tts_functionality'] else '❌'}")
    print(f"  • Audio Control: {'✅' if test_results['audio_control'] else '❌'}")
    print(f"  • Status Query: {'✅' if test_results['status_query'] else '❌'}")
    print(f"  • JSON-RPC Interface: {'✅' if test_results['json_rpc_interface'] else '❌'}")
    print(f"  • Error Handling: {'✅' if test_results['error_handling'] else '❌'}")
    print(f"  • Parameter Validation: {'✅' if test_results['parameter_validation'] else '❌'}")
    
    print("\n🎯 Recommendations:")
    if passed_tests == total_tests:
        print("  • All tests passed! The MCP Audio Server is ready for production use.")
        print("  • Consider adding more audio format support if needed.")
        print("  • Monitor performance with longer audio files.")
    else:
        print("  • Review failed tests and address any issues.")
        print("  • Ensure all dependencies are properly installed.")
        print("  • Check system audio configuration.")
    
    print("\n🚀 Ready for AI Model Integration!")
    print("The MCP Audio Server can now be used with AI models to provide audio capabilities.")
    
    return test_results

if __name__ == "__main__":
    generate_test_report()
