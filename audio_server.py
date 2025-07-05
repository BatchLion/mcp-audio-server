#!/usr/bin/env python3
"""
MCP Audio Server - Provides audio playback capabilities for AI models
"""

import json
import logging
import os
import sys
from typing import Any, Dict, Optional

# Suppress pygame welcome message to avoid interfering with MCP JSON communication
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pyttsx3
import pygame

# Configure logging to stderr to avoid interfering with MCP JSON communication on stdout
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioPlayer:
    """Handles audio playback operations"""

    def __init__(self):
        self.tts_engine = None
        self.pygame_initialized = False
        self.current_sound = None
        self._init_tts()
        self._init_pygame()

    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            # Set default properties
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")

    def _init_pygame(self):
        """Initialize pygame mixer for audio file playback"""
        try:
            # Suppress pygame welcome message
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
            pygame.mixer.init()
            self.pygame_initialized = True
            logger.info("Pygame mixer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")

    def speak_text(self, text: str, rate: Optional[int] = None, volume: Optional[float] = None) -> Dict[str, Any]:
        """Convert text to speech and play it"""
        if not self.tts_engine:
            return {"success": False, "error": "TTS engine not available"}

        try:
            # Set custom rate and volume if provided
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
            if volume is not None:
                self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))

            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

            return {
                "success": True,
                "message": f"Successfully spoke text: '{text[:50]}{'...' if len(text) > 50 else ''}'"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to speak text: {str(e)}"}

    def play_audio_file(self, file_path: str, volume: Optional[float] = None) -> Dict[str, Any]:
        """Play an audio file"""
        if not self.pygame_initialized:
            return {"success": False, "error": "Audio system not initialized"}

        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {"success": False, "error": f"Audio file not found: {file_path}"}

            # Load and play the audio file
            pygame.mixer.music.load(file_path)

            # Set volume if provided
            if volume is not None:
                pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

            pygame.mixer.music.play()

            return {
                "success": True,
                "message": f"Successfully started playing: {os.path.basename(file_path)}"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to play audio file: {str(e)}"}

    def stop_audio(self) -> Dict[str, Any]:
        """Stop current audio playback"""
        try:
            if self.pygame_initialized:
                pygame.mixer.music.stop()

            if self.tts_engine:
                self.tts_engine.stop()

            return {"success": True, "message": "Audio playback stopped"}
        except Exception as e:
            return {"success": False, "error": f"Failed to stop audio: {str(e)}"}

    def get_audio_status(self) -> Dict[str, Any]:
        """Get current audio playback status"""
        try:
            status = {
                "tts_available": self.tts_engine is not None,
                "pygame_available": self.pygame_initialized,
                "music_playing": False
            }

            if self.pygame_initialized:
                status["music_playing"] = pygame.mixer.music.get_busy()

            return {"success": True, "status": status}
        except Exception as e:
            return {"success": False, "error": f"Failed to get audio status: {str(e)}"}

class MCPAudioServer:
    """Simple MCP-compatible Audio Server"""

    def __init__(self):
        self.audio_player = AudioPlayer()
        self.tools = {
            "speak_text": {
                "name": "speak_text",
                "description": "Convert text to speech and play it through the system audio",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to convert to speech and play"
                        },
                        "rate": {
                            "type": "integer",
                            "description": "Speech rate (words per minute, default: 150)",
                            "minimum": 50,
                            "maximum": 300
                        },
                        "volume": {
                            "type": "number",
                            "description": "Volume level (0.0 to 1.0, default: 0.8)",
                            "minimum": 0.0,
                            "maximum": 1.0
                        }
                    },
                    "required": ["text"]
                }
            },
            "play_audio_file": {
                "name": "play_audio_file",
                "description": "Play an audio file through the system audio",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the audio file to play"
                        },
                        "volume": {
                            "type": "number",
                            "description": "Volume level (0.0 to 1.0)",
                            "minimum": 0.0,
                            "maximum": 1.0
                        }
                    },
                    "required": ["file_path"]
                }
            },
            "stop_audio": {
                "name": "stop_audio",
                "description": "Stop current audio playback",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "get_audio_status": {
                "name": "get_audio_status",
                "description": "Get current audio system status and playback information",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        return {
            "tools": list(self.tools.values())
        }

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with given arguments"""
        try:
            if name == "speak_text":
                text = arguments.get("text", "")
                rate = arguments.get("rate")
                volume = arguments.get("volume")

                if not text:
                    return {
                        "content": [{"type": "text", "text": "Error: No text provided"}],
                        "isError": True
                    }

                result = self.audio_player.speak_text(text, rate, volume)
                if result.get("success"):
                    return {
                        "content": [{"type": "text", "text": result.get("message", "Speech completed successfully")}],
                        "isError": False
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error', 'Unknown error')}"}],
                        "isError": True
                    }

            elif name == "play_audio_file":
                file_path = arguments.get("file_path", "")
                volume = arguments.get("volume")

                if not file_path:
                    return {
                        "content": [{"type": "text", "text": "Error: No file path provided"}],
                        "isError": True
                    }

                result = self.audio_player.play_audio_file(file_path, volume)
                if result.get("success"):
                    return {
                        "content": [{"type": "text", "text": result.get("message", "Audio file played successfully")}],
                        "isError": False
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error', 'Unknown error')}"}],
                        "isError": True
                    }

            elif name == "stop_audio":
                result = self.audio_player.stop_audio()
                if result.get("success"):
                    return {
                        "content": [{"type": "text", "text": result.get("message", "Audio stopped successfully")}],
                        "isError": False
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error', 'Unknown error')}"}],
                        "isError": True
                    }

            elif name == "get_audio_status":
                result = self.audio_player.get_audio_status()
                if result.get("success"):
                    status = result.get("status", {})
                    status_text = f"Audio Status:\n- TTS Available: {status.get('tts_available', False)}\n- Pygame Available: {status.get('pygame_available', False)}\n- Music Playing: {status.get('music_playing', False)}"
                    return {
                        "content": [{"type": "text", "text": status_text}],
                        "isError": False
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error', 'Unknown error')}"}],
                        "isError": True
                    }

            else:
                return {
                    "content": [{"type": "text", "text": f"Error: Unknown tool '{name}'"}],
                    "isError": True
                }

        except Exception as e:
            logger.error(f"Error calling tool '{name}': {e}")
            return {
                "content": [{"type": "text", "text": f"Tool execution error: {str(e)}"}],
                "isError": True
            }

def handle_json_rpc_request(request_data: str) -> str:
    """Handle JSON-RPC requests"""
    try:
        request = json.loads(request_data)
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        # Handle notifications (no response expected)
        if method and method.startswith("notifications/"):
            logger.info(f"Received notification: {method}")
            return ""  # No response for notifications

        # Ensure request_id is never None for responses
        if request_id is None:
            request_id = 0

        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "audio-server",
                    "version": "1.0.0"
                }
            }
        elif method == "tools/list":
            result = server.list_tools()
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            tool_result = server.call_tool(tool_name, arguments)

            # Return the tool result directly (it's already in MCP format)
            result = tool_result
        elif method == "resources/list":
            # Return empty resources list - this server doesn't provide resources
            result = {"resources": []}
        elif method == "prompts/list":
            # Return empty prompts list - this server doesn't provide prompts
            result = {"prompts": []}
        else:
            result = {"success": False, "error": f"Unknown method: {method}"}

        # For tools/call, the result is already in the correct format
        if method == "tools/call":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        return json.dumps(response)

    except Exception as e:
        logger.error(f"JSON-RPC error: {e}")
        try:
            request_id = request.get("id") if 'request' in locals() else 0
        except:
            request_id = 0

        # Ensure request_id is never None
        if request_id is None:
            request_id = 0

        error_response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            }
        }
        return json.dumps(error_response)

def interactive_mode():
    """Run in interactive mode for testing"""
    print("MCP Audio Server - Interactive Mode", file=sys.stderr)
    print("Available commands:", file=sys.stderr)
    print("  list - List available tools", file=sys.stderr)
    print("  speak <text> - Speak text", file=sys.stderr)
    print("  play <file_path> - Play audio file", file=sys.stderr)
    print("  stop - Stop audio playback", file=sys.stderr)
    print("  status - Get audio status", file=sys.stderr)
    print("  quit - Exit", file=sys.stderr)
    print(file=sys.stderr)

    while True:
        try:
            command = input("audio> ").strip()

            if command == "quit":
                break
            elif command == "list":
                result = server.list_tools()
                print(json.dumps(result, indent=2), file=sys.stderr)
            elif command.startswith("speak "):
                text = command[6:]
                result = server.call_tool("speak_text", {"text": text})
                print(json.dumps(result, indent=2), file=sys.stderr)
            elif command.startswith("play "):
                file_path = command[5:]
                result = server.call_tool("play_audio_file", {"file_path": file_path})
                print(json.dumps(result, indent=2), file=sys.stderr)
            elif command == "stop":
                result = server.call_tool("stop_audio", {})
                print(json.dumps(result, indent=2), file=sys.stderr)
            elif command == "status":
                result = server.call_tool("get_audio_status", {})
                print(json.dumps(result, indent=2), file=sys.stderr)
            elif command == "":
                continue
            else:
                print(f"Unknown command: {command}", file=sys.stderr)

        except KeyboardInterrupt:
            print("\nExiting...", file=sys.stderr)
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        # JSON-RPC mode for MCP integration
        logger.info("Starting MCP Audio Server in JSON-RPC mode...")
        logger.info("Send JSON-RPC requests to stdin")

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break

                response = handle_json_rpc_request(line.strip())
                if response:  # Only print non-empty responses
                    print(response)
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

# Initialize server
server = MCPAudioServer()

if __name__ == "__main__":
    main()
