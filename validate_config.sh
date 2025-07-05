#!/bin/bash

# Validate Claude Desktop Configuration Script

CONFIG_PATH="/Users/batchlions/Library/Application Support/Claude/claude_desktop_config.json"
BACKUP_PATH="/Users/batchlions/Documents/augment-projects/MCPAgent/claude_desktop_config_clean.json"

echo "🔍 Validating Claude Desktop Configuration..."

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Configuration file not found: $CONFIG_PATH"
    echo "📋 Creating new configuration file..."
    cp "$BACKUP_PATH" "$CONFIG_PATH"
    echo "✅ Configuration file created"
fi

# Validate JSON syntax
if python -m json.tool "$CONFIG_PATH" > /dev/null 2>&1; then
    echo "✅ JSON syntax is valid"
    
    # Check if audio-server is configured
    if python -c "import json; data=json.load(open('$CONFIG_PATH')); print('audio-server' in data.get('mcpServers', {}))" 2>/dev/null | grep -q "True"; then
        echo "✅ Audio server is properly configured"
        echo ""
        echo "📋 Configuration Summary:"
        echo "   • File: $CONFIG_PATH"
        echo "   • Server: audio-server"
        echo "   • Command: $(python -c "import json; data=json.load(open('$CONFIG_PATH')); print(data['mcpServers']['audio-server']['command'])" 2>/dev/null)"
        echo "   • Script: $(python -c "import json; data=json.load(open('$CONFIG_PATH')); print(data['mcpServers']['audio-server']['args'][0])" 2>/dev/null)"
        echo ""
        echo "🚀 Ready to use! Restart Claude Desktop to activate the audio server."
    else
        echo "❌ Audio server not found in configuration"
        echo "📋 Restoring configuration..."
        cp "$BACKUP_PATH" "$CONFIG_PATH"
        echo "✅ Configuration restored"
    fi
else
    echo "❌ JSON syntax error detected"
    echo "📋 Restoring clean configuration..."
    cp "$BACKUP_PATH" "$CONFIG_PATH"
    
    if python -m json.tool "$CONFIG_PATH" > /dev/null 2>&1; then
        echo "✅ Configuration restored and validated"
    else
        echo "❌ Failed to restore configuration"
        exit 1
    fi
fi

echo ""
echo "💡 If you still see errors:"
echo "   1. Restart Claude Desktop completely"
echo "   2. Check that the audio server script exists"
echo "   3. Run: ./validate_config.sh"
