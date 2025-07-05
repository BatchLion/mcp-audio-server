#!/usr/bin/env python3
"""
Demo: AI Model Integration with MCP Audio Server
This demonstrates how an AI model would interact with the audio server
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

class AIModelSimulator:
    """Simulates an AI model using the MCP Audio Server"""
    
    def __init__(self):
        self.audio_server = MCPAudioServer()
        self.conversation_history = []
    
    def speak(self, text, **kwargs):
        """Make the AI speak text"""
        print(f"🤖 AI: {text}")
        
        # Use the audio server to speak
        result = self.audio_server.call_tool("speak_text", {
            "text": text,
            **kwargs
        })
        
        if result.get("success"):
            print("   🔊 Audio played successfully")
        else:
            print(f"   ❌ Audio failed: {result.get('error')}")
        
        return result
    
    def think_and_respond(self, user_input):
        """Simulate AI thinking and responding"""
        self.conversation_history.append(f"User: {user_input}")
        
        # Simulate different types of responses
        if "hello" in user_input.lower():
            response = "Hello! I'm an AI assistant with audio capabilities. I can speak to you using text-to-speech!"
            self.speak(response, volume=0.8, rate=150)
            
        elif "slow" in user_input.lower():
            response = "I'll speak more slowly now. This demonstrates the rate parameter control."
            self.speak(response, volume=0.7, rate=100)
            
        elif "fast" in user_input.lower():
            response = "Now I'm speaking faster! This shows how we can adjust speech parameters dynamically."
            self.speak(response, volume=0.8, rate=200)
            
        elif "quiet" in user_input.lower():
            response = "I'm speaking quietly now. This demonstrates volume control."
            self.speak(response, volume=0.3, rate=150)
            
        elif "loud" in user_input.lower():
            response = "NOW I'M SPEAKING LOUDLY! Maximum volume demonstration."
            self.speak(response, volume=1.0, rate=150)
            
        elif "status" in user_input.lower():
            status = self.audio_server.call_tool("get_audio_status", {})
            if status.get("success"):
                audio_status = status["status"]
                response = f"Audio system status: TTS is {'available' if audio_status['tts_available'] else 'unavailable'}, Audio system is {'ready' if audio_status['pygame_available'] else 'not ready'}."
            else:
                response = "I couldn't check the audio system status."
            self.speak(response)
            
        elif "stop" in user_input.lower():
            self.audio_server.call_tool("stop_audio", {})
            response = "I've stopped any current audio playback."
            print(f"🤖 AI: {response}")
            
        elif "goodbye" in user_input.lower() or "bye" in user_input.lower():
            response = "Goodbye! It was nice talking with you. This MCP Audio Server integration works great!"
            self.speak(response, volume=0.8, rate=140)
            return False  # End conversation
            
        else:
            response = "I understand you, and I can respond with speech! Try saying 'slow', 'fast', 'quiet', 'loud', 'status', or 'goodbye'."
            self.speak(response)
        
        self.conversation_history.append(f"AI: {response}")
        return True

def demo_ai_integration():
    """Demonstrate AI integration with audio capabilities"""
    print("🎭 AI Model Integration Demo")
    print("=" * 50)
    print("This demo shows how an AI model would use the MCP Audio Server")
    print("to provide audio responses to user input.")
    print()
    
    ai = AIModelSimulator()
    
    # Check if audio system is ready
    status = ai.audio_server.call_tool("get_audio_status", {})
    if not status.get("success") or not status["status"]["tts_available"]:
        print("❌ Audio system not available. Demo cannot continue.")
        return
    
    print("✅ Audio system ready!")
    print()
    print("Available commands:")
    print("  • 'hello' - Greeting")
    print("  • 'slow' - Slow speech")
    print("  • 'fast' - Fast speech") 
    print("  • 'quiet' - Quiet speech")
    print("  • 'loud' - Loud speech")
    print("  • 'status' - Check audio status")
    print("  • 'stop' - Stop current audio")
    print("  • 'goodbye' - End demo")
    print()
    
    # Automated demo sequence
    demo_inputs = [
        "hello",
        "Can you speak slowly?",
        "Now speak fast please",
        "Please speak quietly",
        "Can you speak loudly?",
        "What's your status?",
        "goodbye"
    ]
    
    print("🎬 Running automated demo sequence...")
    print()
    
    for i, user_input in enumerate(demo_inputs, 1):
        print(f"👤 User ({i}/{len(demo_inputs)}): {user_input}")
        
        continue_demo = ai.think_and_respond(user_input)
        
        if not continue_demo:
            break
        
        # Small pause between interactions
        time.sleep(1)
        print()
    
    print("\n🎉 Demo completed!")
    print("\n📊 Conversation Summary:")
    for entry in ai.conversation_history:
        print(f"   {entry}")

def interactive_demo():
    """Interactive demo where user can type commands"""
    print("\n🎮 Interactive Mode")
    print("=" * 30)
    print("Type your messages and the AI will respond with audio!")
    print("Type 'quit' to exit.")
    print()
    
    ai = AIModelSimulator()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            continue_demo = ai.think_and_respond(user_input)
            
            if not continue_demo:
                break
                
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        demo_ai_integration()
        
        # Ask if user wants interactive mode
        print("\n🤔 Would you like to try interactive mode? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice in ['y', 'yes']:
            interactive_demo()
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
