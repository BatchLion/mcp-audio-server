#!/usr/bin/env python3
"""
Test script for MCP Audio Server
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from audio_server import AudioPlayer

async def test_audio_player():
    """Test the AudioPlayer functionality"""
    print("Testing MCP Audio Server...")
    
    # Initialize audio player
    player = AudioPlayer()
    
    # Test 1: Get audio status
    print("\n1. Testing audio status...")
    status_result = player.get_audio_status()
    print(f"Status result: {json.dumps(status_result, indent=2)}")
    
    # Test 2: Text-to-speech
    print("\n2. Testing text-to-speech...")
    tts_result = player.speak_text("Hello! This is a test of the MCP Audio Server.")
    print(f"TTS result: {json.dumps(tts_result, indent=2)}")
    
    # Test 3: Test with custom parameters
    print("\n3. Testing TTS with custom parameters...")
    tts_custom_result = player.speak_text(
        "This is a slower, quieter test message.", 
        rate=100, 
        volume=0.5
    )
    print(f"Custom TTS result: {json.dumps(tts_custom_result, indent=2)}")
    
    # Test 4: Stop audio
    print("\n4. Testing stop audio...")
    stop_result = player.stop_audio()
    print(f"Stop result: {json.dumps(stop_result, indent=2)}")
    
    # Test 5: Test audio file playback (if file exists)
    print("\n5. Testing audio file playback...")
    test_audio_path = "test_audio.mp3"  # You can replace with an actual audio file path
    file_result = player.play_audio_file(test_audio_path)
    print(f"File playback result: {json.dumps(file_result, indent=2)}")
    
    print("\nAll tests completed!")

def test_sync():
    """Synchronous test function"""
    print("Running synchronous tests...")
    
    player = AudioPlayer()
    
    # Test basic functionality
    print("Testing basic TTS...")
    result = player.speak_text("MCP Audio Server is working correctly!")
    print(f"Result: {result}")

if __name__ == "__main__":
    print("MCP Audio Server Test Suite")
    print("=" * 40)
    
    # Run synchronous tests
    test_sync()
    
    # Run async tests
    print("\nRunning async tests...")
    asyncio.run(test_audio_player())
