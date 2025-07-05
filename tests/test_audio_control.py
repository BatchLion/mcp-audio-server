#!/usr/bin/env python3
"""
Test audio control and error handling for MCP Audio Server
"""

import json
import sys
import os
import time

# Suppress pygame messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_server import MCPAudioServer

def test_audio_control():
    """Test audio playback control"""
    print("🎮 Testing Audio Control Functions")
    print("=" * 40)
    
    server = MCPAudioServer()
    
    # Test 1: Start speaking and then stop
    print("\n1️⃣ Testing speak and stop sequence...")
    
    # Start speaking (this should be non-blocking in a real scenario)
    print("   Starting speech...")
    result = server.call_tool("speak_text", {
        "text": "This is a longer message that we will interrupt with the stop command. It should demonstrate the stop functionality.",
        "rate": 100  # Slower speech to give time to stop
    })
    print(f"   Speech started: {result.get('success', False)}")
    
    # Immediately try to stop
    print("   Stopping audio...")
    stop_result = server.call_tool("stop_audio", {})
    print(f"   Stop result: {stop_result.get('success', False)}")
    
    # Test 2: Check status during playback
    print("\n2️⃣ Testing status during playback...")
    
    # Start another speech
    print("   Starting new speech...")
    server.call_tool("speak_text", {
        "text": "Testing status check during playback",
        "rate": 80
    })
    
    # Check status
    status = server.call_tool("get_audio_status", {})
    print(f"   Status check: {status.get('success', False)}")
    if status.get('success'):
        print(f"   TTS Available: {status['status']['tts_available']}")
        print(f"   Audio System: {status['status']['pygame_available']}")
        print(f"   Music Playing: {status['status']['music_playing']}")
    
    print("\n✅ Audio control tests completed!")

def test_error_handling():
    """Test error handling scenarios"""
    print("\n🚨 Testing Error Handling")
    print("=" * 40)
    
    server = MCPAudioServer()
    
    # Test 1: Empty text
    print("\n1️⃣ Testing empty text...")
    result = server.call_tool("speak_text", {"text": ""})
    print(f"   Success: {result.get('success', False)}")
    print(f"   Error: {result.get('error', 'No error')}")
    
    # Test 2: Invalid audio file
    print("\n2️⃣ Testing invalid audio file...")
    result = server.call_tool("play_audio_file", {"file_path": "/nonexistent/file.mp3"})
    print(f"   Success: {result.get('success', False)}")
    print(f"   Error: {result.get('error', 'No error')}")
    
    # Test 3: Invalid parameters
    print("\n3️⃣ Testing invalid parameters...")
    result = server.call_tool("speak_text", {
        "text": "Test",
        "rate": 1000,  # Too high
        "volume": 2.0  # Too high
    })
    print(f"   Success: {result.get('success', False)}")
    # Should still work as we clamp values
    
    # Test 4: Unknown tool
    print("\n4️⃣ Testing unknown tool...")
    result = server.call_tool("unknown_tool", {})
    print(f"   Success: {result.get('success', False)}")
    print(f"   Error: {result.get('error', 'No error')}")
    
    # Test 5: Missing required parameters
    print("\n5️⃣ Testing missing parameters...")
    result = server.call_tool("speak_text", {})  # Missing text
    print(f"   Success: {result.get('success', False)}")
    print(f"   Error: {result.get('error', 'No error')}")
    
    result = server.call_tool("play_audio_file", {})  # Missing file_path
    print(f"   Success: {result.get('success', False)}")
    print(f"   Error: {result.get('error', 'No error')}")
    
    print("\n✅ Error handling tests completed!")

def test_parameter_validation():
    """Test parameter validation"""
    print("\n🔧 Testing Parameter Validation")
    print("=" * 40)
    
    server = MCPAudioServer()
    
    # Test 1: Rate boundaries
    print("\n1️⃣ Testing rate boundaries...")
    
    # Very low rate
    result = server.call_tool("speak_text", {"text": "Low rate test", "rate": 10})
    print(f"   Low rate (10): {result.get('success', False)}")
    
    # Very high rate  
    result = server.call_tool("speak_text", {"text": "High rate test", "rate": 500})
    print(f"   High rate (500): {result.get('success', False)}")
    
    # Test 2: Volume boundaries
    print("\n2️⃣ Testing volume boundaries...")
    
    # Negative volume
    result = server.call_tool("speak_text", {"text": "Negative volume", "volume": -0.5})
    print(f"   Negative volume: {result.get('success', False)}")
    
    # Volume > 1.0
    result = server.call_tool("speak_text", {"text": "High volume", "volume": 1.5})
    print(f"   High volume: {result.get('success', False)}")
    
    print("\n✅ Parameter validation tests completed!")

if __name__ == "__main__":
    try:
        test_audio_control()
        test_error_handling()
        test_parameter_validation()
        print("\n🎉 All audio control and error handling tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
