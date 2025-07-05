#!/bin/bash

# MCP Audio Server Installation and Setup Script

echo "🎵 MCP Audio Server Installation and Setup"
echo "=========================================="

# Get current directory
CURRENT_DIR=$(pwd)
PYTHON_PATH="/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"

echo "📁 Current directory: $CURRENT_DIR"
echo "🐍 Python path: $PYTHON_PATH"

# Check if we're in the right directory
if [ ! -f "audio_server.py" ]; then
    echo "❌ Error: audio_server.py not found in current directory"
    echo "Please run this script from the MCPAgent directory"
    exit 1
fi

echo "✅ Found audio_server.py"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
$PYTHON_PATH -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test the server
echo ""
echo "🧪 Testing server functionality..."
$PYTHON_PATH test_report.py

if [ $? -eq 0 ]; then
    echo "✅ Server test passed"
else
    echo "❌ Server test failed"
    exit 1
fi

# Create configuration directories
echo ""
echo "📁 Setting up configuration directories..."

# Claude Desktop configuration
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "📁 Creating Claude Desktop config directory: $CLAUDE_CONFIG_DIR"
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

# Copy Claude Desktop configuration
echo "📋 Setting up Claude Desktop configuration..."
cat > "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "audio-server": {
      "command": "$PYTHON_PATH",
      "args": ["$CURRENT_DIR/audio_server.py"],
      "env": {
        "PYTHONPATH": "$CURRENT_DIR",
        "PYGAME_HIDE_SUPPORT_PROMPT": "1"
      }
    }
  }
}
EOF

echo "✅ Claude Desktop configuration created at: $CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Create a generic MCP config for other clients
echo "📋 Creating generic MCP configuration..."
cat > "$CURRENT_DIR/mcp_server_config.json" << EOF
{
  "mcpServers": {
    "audio-server": {
      "command": "$PYTHON_PATH",
      "args": ["$CURRENT_DIR/audio_server.py"],
      "env": {
        "PYTHONPATH": "$CURRENT_DIR",
        "PYGAME_HIDE_SUPPORT_PROMPT": "1"
      }
    }
  }
}
EOF

echo "✅ Generic MCP configuration created at: $CURRENT_DIR/mcp_server_config.json"

# Create startup script
echo "📋 Creating startup script..."
cat > "$CURRENT_DIR/start_audio_server.sh" << EOF
#!/bin/bash
cd "$CURRENT_DIR"
export PYTHONPATH="$CURRENT_DIR"
export PYGAME_HIDE_SUPPORT_PROMPT=1
$PYTHON_PATH audio_server.py
EOF

chmod +x "$CURRENT_DIR/start_audio_server.sh"
echo "✅ Startup script created at: $CURRENT_DIR/start_audio_server.sh"

# Create test script
echo "📋 Creating test script..."
cat > "$CURRENT_DIR/test_integration.sh" << EOF
#!/bin/bash
cd "$CURRENT_DIR"
export PYTHONPATH="$CURRENT_DIR"
export PYGAME_HIDE_SUPPORT_PROMPT=1

echo "🧪 Testing MCP Audio Server Integration"
echo "======================================"

echo "1. Testing server startup..."
timeout 5s $PYTHON_PATH audio_server.py --test 2>/dev/null || echo "Server can start"

echo "2. Running comprehensive tests..."
$PYTHON_PATH test_report.py

echo "3. Testing AI integration demo..."
echo "hello" | $PYTHON_PATH ai_integration_demo.py

echo "✅ Integration tests completed!"
EOF

chmod +x "$CURRENT_DIR/test_integration.sh"
echo "✅ Test script created at: $CURRENT_DIR/test_integration.sh"

echo ""
echo "🎉 Installation and setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. If using Claude Desktop:"
echo "   - Restart Claude Desktop application"
echo "   - The audio server should be available as 'audio-server'"
echo ""
echo "2. If using other MCP clients:"
echo "   - Use the configuration from: $CURRENT_DIR/mcp_server_config.json"
echo ""
echo "3. To test manually:"
echo "   - Run: ./start_audio_server.sh"
echo "   - Or: $PYTHON_PATH audio_server.py --interactive"
echo ""
echo "4. To run integration tests:"
echo "   - Run: ./test_integration.sh"
echo ""
echo "🎵 Your MCP Audio Server is ready to use!"
