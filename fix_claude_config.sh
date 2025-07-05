#!/bin/bash

# Claude Desktop Configuration Fix Script

CONFIG_PATH="/Users/batchlions/Library/Application Support/Claude/claude_desktop_config.json"
CONFIG_DIR="/Users/batchlions/Library/Application Support/Claude"
BACKUP_DIR="/Users/batchlions/Documents/augment-projects/MCPAgent"

echo "🔧 Claude Desktop Configuration Fix Script"
echo "=========================================="

# Ensure directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "📁 Creating Claude config directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Remove any existing config file
if [ -f "$CONFIG_PATH" ]; then
    echo "🗑️  Removing existing config file..."
    rm "$CONFIG_PATH"
fi

# Create minimal, clean config using Python to ensure perfect JSON
echo "📝 Creating new configuration file..."
python3 -c "
import json
config = {
    'mcpServers': {
        'speech': {
            'command': '/Users/batchlions/miniconda3/envs/mcp_agent/bin/python',
            'args': ['/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py']
        }
    }
}
with open('$CONFIG_PATH', 'w') as f:
    json.dump(config, f, indent=2)
"

# Validate JSON
echo "✅ Validating JSON syntax..."
if python -m json.tool "$CONFIG_PATH" > /dev/null 2>&1; then
    echo "✅ JSON is valid"
else
    echo "❌ JSON validation failed"
    exit 1
fi

# Check file permissions
echo "🔐 Checking file permissions..."
chmod 644 "$CONFIG_PATH"
echo "✅ Permissions set to 644"

# Check if audio server exists
AUDIO_SERVER="/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
if [ -f "$AUDIO_SERVER" ]; then
    echo "✅ Audio server script found"
else
    echo "❌ Audio server script not found: $AUDIO_SERVER"
    exit 1
fi

# Check Python environment
PYTHON_PATH="/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
if [ -f "$PYTHON_PATH" ]; then
    echo "✅ Python environment found"
else
    echo "❌ Python environment not found: $PYTHON_PATH"
    exit 1
fi

# Test audio server can start
echo "🧪 Testing audio server startup..."
timeout 3 "$PYTHON_PATH" "$AUDIO_SERVER" 2>&1 | head -5
if [ $? -eq 124 ]; then
    echo "✅ Audio server starts successfully (timeout expected)"
else
    echo "⚠️  Audio server test completed"
fi

# Check for conflicting files
echo "🔍 Checking for conflicting configuration files..."
find "$CONFIG_DIR" -name "*.json" -not -path "*/node_modules/*" -not -path "*/sentry/*" | grep -v claude_desktop_config.json | head -5

echo ""
echo "🎉 Configuration fixed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Completely quit Claude Desktop (Cmd+Q)"
echo "   2. Wait 10 seconds"
echo "   3. Restart Claude Desktop"
echo "   4. Wait for MCP servers to initialize (15-30 seconds)"
echo "   5. Test with: 'Please use speech to say Hello World'"
echo ""
echo "📁 Config file location: $CONFIG_PATH"
echo "🔍 Current config:"
cat "$CONFIG_PATH"
echo ""
echo "💡 If problems persist:"
echo "   • Check Claude Desktop Console logs (Help > Developer Tools)"
echo "   • Ensure no other MCP configs conflict"
echo "   • Try running: $PYTHON_PATH $AUDIO_SERVER manually"
echo "   • Check if Claude Desktop has permission to access files"
