#!/usr/bin/env python3
"""
Comprehensive diagnostic script for MCP Audio Server setup
"""

import subprocess
import sys
import time
import json
import os

def test_python_environment():
    """Test if the Python environment is working"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    
    print("🐍 Testing Python environment...")
    try:
        result = subprocess.run([python_path, "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Python version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Python test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Python environment error: {e}")
        return False

def test_audio_dependencies():
    """Test if audio dependencies are available"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    
    print("📦 Testing audio dependencies...")
    test_script = """
try:
    import pygame
    print("✅ pygame imported successfully")
except ImportError as e:
    print(f"❌ pygame import failed: {e}")
    exit(1)

try:
    import pyttsx3
    print("✅ pyttsx3 imported successfully")
except ImportError as e:
    print(f"❌ pyttsx3 import failed: {e}")
    exit(1)

try:
    import mcp
    print("✅ mcp imported successfully")
except ImportError as e:
    print(f"❌ mcp import failed: {e}")
    exit(1)

print("✅ All dependencies available")
"""
    
    try:
        result = subprocess.run([python_path, "-c", test_script], 
                              capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Dependency test failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Dependency test error: {e}")
        return False

def test_config_file():
    """Test if the config file is valid"""
    config_path = "/Users/batchlions/Library/Application Support/Claude/claude_desktop_config.json"
    
    print("📄 Testing configuration file...")
    try:
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            return False
            
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        print("✅ Config file is valid JSON")
        
        # Check structure
        if 'mcpServers' not in config:
            print("❌ Missing 'mcpServers' in config")
            return False
            
        servers = config['mcpServers']
        if not servers:
            print("❌ No servers configured")
            return False
            
        # Find any audio-related server
        audio_server = None
        for name, server_config in servers.items():
            if 'audio' in name.lower() or 'speech' in name.lower():
                audio_server = (name, server_config)
                break
        
        if not audio_server:
            print("❌ No audio/speech server found in config")
            return False
            
        name, server_config = audio_server
        print(f"✅ Found audio server: {name}")
        
        if 'command' not in server_config or 'args' not in server_config:
            print("❌ Missing 'command' or 'args' in server config")
            return False
            
        print("✅ Config file structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Config file error: {e}")
        return False

def test_audio_server_syntax():
    """Test if the audio server has valid Python syntax"""
    python_path = "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python"
    server_path = "/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"
    
    print("🔍 Testing audio server syntax...")
    try:
        result = subprocess.run([python_path, "-m", "py_compile", server_path], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Audio server syntax is valid")
            return True
        else:
            print(f"❌ Syntax error in audio server: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Syntax test error: {e}")
        return False

def main():
    print("🧪 MCP Audio Server Diagnostic Suite")
    print("=" * 50)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Audio Dependencies", test_audio_dependencies),
        ("Configuration File", test_config_file),
        ("Audio Server Syntax", test_audio_server_syntax),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print("-" * 50)
    
    print("\n📊 Diagnostic Results:")
    print("=" * 50)
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All diagnostics passed!")
        print("\n📋 The setup looks correct. If Claude Desktop still shows errors:")
        print("1. Completely quit Claude Desktop (Cmd+Q)")
        print("2. Wait 10 seconds")
        print("3. Restart Claude Desktop")
        print("4. Wait for MCP servers to initialize (15-30 seconds)")
        print("5. Check Claude Desktop Console (Help > Developer Tools)")
        print("6. Test with: 'Please use speech to say Hello World'")
    else:
        print("❌ Some diagnostics failed.")
        print("Please fix the issues above before proceeding.")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
