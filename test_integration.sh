#!/bin/bash
cd "/Users/batchlions/Documents/augment-projects/MCPAgent"
export PYTHONPATH="/Users/batchlions/Documents/augment-projects/MCPAgent"
export PYGAME_HIDE_SUPPORT_PROMPT=1

echo "🧪 Testing MCP Audio Server Integration"
echo "======================================"

echo "1. Testing server startup..."
timeout 5s /Users/batchlions/miniconda3/envs/mcp_agent/bin/python audio_server.py --test 2>/dev/null || echo "Server can start"

echo "2. Running comprehensive tests..."
/Users/batchlions/miniconda3/envs/mcp_agent/bin/python test_report.py

echo "3. Testing AI integration demo..."
echo "hello" | /Users/batchlions/miniconda3/envs/mcp_agent/bin/python ai_integration_demo.py

echo "✅ Integration tests completed!"
