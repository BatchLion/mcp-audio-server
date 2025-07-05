#!/usr/bin/env python3
"""
Demo script for MCP Audio Server
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from audio_server import MCPAudioServer
    
    def demo_interactive():
        """Interactive demo of the audio server"""
        print("🎵 MCP Audio Server Demo")
        print("=" * 40)
        
        # Initialize server
        server = MCPAudioServer()
        
        print("✅ Audio server initialized successfully!")
        print()
        
        # Test 1: List tools
        print("📋 Available tools:")
        tools = server.list_tools()
        for tool in tools["tools"]:
            print(f"  • {tool['name']}: {tool['description']}")
        print()
        
        # Test 2: Get audio status
        print("🔍 Audio system status:")
        status = server.call_tool("get_audio_status", {})
        if status["success"]:
            print(f"  • TTS Available: {status['status']['tts_available']}")
            print(f"  • Audio System: {status['status']['pygame_available']}")
            print(f"  • Currently Playing: {status['status']['music_playing']}")
        print()
        
        # Test 3: Text-to-speech demo
        print("🗣️  Testing text-to-speech...")
        demo_text = "Hello! This is the MCP Audio Server. I can convert text to speech and play audio files."
        result = server.call_tool("speak_text", {"text": demo_text})
        if result["success"]:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  ❌ Error: {result['error']}")
        print()
        
        # Test 4: Custom TTS parameters
        print("🎛️  Testing custom speech parameters...")
        custom_text = "This message is spoken more slowly and quietly."
        result = server.call_tool("speak_text", {
            "text": custom_text,
            "rate": 100,
            "volume": 0.5
        })
        if result["success"]:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  ❌ Error: {result['error']}")
        print()
        
        print("🎉 Demo completed successfully!")
        print()
        print("💡 To use this server with an AI model:")
        print("   1. Start the server: python audio_server.py")
        print("   2. Send JSON-RPC requests to stdin")
        print("   3. Example request:")
        print('   {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "speak_text", "arguments": {"text": "Hello World"}}, "id": 1}')
        
    if __name__ == "__main__":
        demo_interactive()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install pyttsx3 pygame pydantic")
except Exception as e:
    print(f"❌ Error: {e}")
