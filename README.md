# MCP Audio Server 🔊

*[English](README.md) | [中文](README_CN.md)*

A powerful Model Context Protocol (MCP) server that provides text-to-speech and audio playback capabilities for Claude Desktop and other MCP clients.

## ✨ Features

- **🗣️ High-Quality TTS**: 
  - **Smart Language Detection**: Automatically uses Google's TTS for high-quality Chinese speech and falls back to the system's TTS for other languages.
  - **Voice Selection**: For non-Chinese text, list and select from various system-installed voices.
  - **Customizable Speech**: Adjust rate and volume for a tailored listening experience.
- **🎵 Audio File Playback**: Play various audio formats (WAV, MP3, OGG, etc.).
- **⏹️ Audio Control**: Stop playback and get real-time audio status.
- **🔌 MCP Compliant**: Fully compatible with Claude Desktop and MCP specification 2024-11-05.
- **🛡️ Error Handling**: Robust error handling and validation.
- **📊 Status Monitoring**: Real-time audio system status and playback information.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Claude Desktop (for MCP integration)
- System audio capabilities

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/mcp-audio-server.git
cd mcp-audio-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure Claude Desktop:**
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "audio-server": {
      "command": "/path/to/your/python",
      "args": ["/path/to/mcp-audio-server/audio_server.py"]
    }
  }
}
```

4. **Restart Claude Desktop** and start using audio features!

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `speak_text` | Convert text to speech. Automatically uses Google TTS for Chinese. | `text` (required), `rate` (optional), `volume` (optional), `voice_id` (optional, for non-Chinese) |
| `list_voices` | List available TTS voices for non-Chinese languages. | None |
| `play_audio_file` | Play an audio file. | `file_path` (required), `volume` (optional) |
| `stop_audio` | Stop current audio playback. | None |
| `get_audio_status` | Get audio system status. | None |

## 📖 Usage Examples

### Text-to-Speech (Chinese)
```
"请用语音说出 '你好，世界'"
```
*This will automatically use Google TTS for a natural-sounding voice.*

### Text-to-Speech (English, with a specific voice)
1.  **First, list available voices:**
    ```
    "List all available voices"
    ```
2.  **Then, use a specific voice ID from the list:**
    ```
    "Use the voice with ID 'com.apple.speech.synthesis.voice.daniel' to say 'Hello, this is a test.'"
    ```

### Play Audio File
```
"Play the audio file at /path/to/music.mp3"
```

### Stop Audio
```
"Stop the current audio playback"
```

### Check Status
```
"What's the current audio status?"
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Test all MCP methods
python test_all_mcp_methods.py

# Test Claude Desktop format compatibility
python test_claude_desktop_format.py

# Test audio functionality
python test_audio_server.py

# Interactive testing mode
python audio_server.py --interactive
```

## 📁 Project Structure

```
mcp-audio-server/
├── audio_server.py              # Main MCP server
├── requirements.txt             # Python dependencies
├── README.md                   # English documentation (default)
├── README_CN.md                # Chinese documentation
├── .gitignore                  # Git ignore rules
├── tests/                      # Test files
│   ├── test_*.py               # Various tests
│   └── validate_*.py           # Validation scripts
├── examples/                   # Configuration examples
│   ├── claude_desktop_config.json
│   └── other config files
├── scripts/                    # Utility scripts
│   ├── install_and_setup.sh
│   └── other shell scripts
└── docs/                       # Additional documentation
    ├── INTEGRATION_GUIDE.md    # Integration guide
    ├── USAGE_GUIDE.md          # Usage guide
    └── FINAL_INTEGRATION_REPORT.md
```

## 🔧 Configuration

### Claude Desktop Configuration

The server integrates seamlessly with Claude Desktop. Make sure your configuration file is properly set up:

**Location:** 
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Example configuration:**
```json
{
  "mcpServers": {
    "audio-server": {
      "command": "/Users/yourusername/miniconda3/envs/mcp_agent/bin/python",
      "args": ["/path/to/mcp-audio-server/audio_server.py"]
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Audio not playing**: Check system audio settings and permissions
2. **TTS not working**: Ensure pyttsx3 is properly installed
3. **MCP connection issues**: Verify Claude Desktop configuration path
4. **Permission errors**: Check file permissions for audio files

### Debug Mode

Run in interactive mode for debugging:
```bash
python audio_server.py --interactive
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with the Model Context Protocol (MCP)
- Uses pyttsx3 for text-to-speech
- Uses pygame for audio playback
- Compatible with Claude Desktop

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the integration guide
3. Open an issue on GitHub
4. Check Claude Desktop documentation

---

**Made with ❤️ for the MCP community**
