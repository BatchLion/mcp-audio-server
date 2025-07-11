# MCP Audio Server 使用指南

## 🎯 项目概述

这是一个基于MCP (Model Context Protocol) 的音频服务器，允许AI模型通过系统音频播放器发出声音。服务器提供文本转语音和音频文件播放功能。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行演示

```bash
python demo_audio_server.py
```

### 3. 测试功能

```bash
python test_audio_server.py
```

## 🛠️ 可用工具

本服务器提供了一系列工具，可通过MCP调用。

### speak_text

将文本转换为语音并播放。此工具足够智能，可以自动检测中文并使用 `gTTS` 提供高质量的发音。对于其他语言，它使用系统的 `pyttsx3` 引擎。

**参数:**
- `text` (必需, `string`): 要转换为语音的文本。
- `rate` (可选, `integer`): 语速 (每分钟词数，默认: 150)。
- `volume` (可选, `float`): 音量 (0.0 到 1.0，默认: 0.8)。
- `voice_id` (可选, `string`): **仅用于非中文文本**。用于指定朗读语音的ID。使用 `list_voices` 工具获取可用ID。

**示例 (中文):**
```json
{
  "text": "你好，世界！",
  "volume": 0.9
}
```

**示例 (英文, 指定语音):**
```json
{
  "text": "Hello world!",
  "voice_id": "com.apple.speech.synthesis.voice.daniel"
}
```

### list_voices

列出系统上所有可用于 **非中文文本** 的TTS语音。

**参数:** 无

**返回示例:**
```json
{
  "success": true,
  "voices": [
    {
      "id": "com.apple.speech.synthesis.voice.daniel",
      "name": "Daniel",
      "lang": ["en_GB"],
      "gender": "male"
    },
    {
      "id": "com.apple.speech.synthesis.voice.samantha",
      "name": "Samantha",
      "lang": ["en_US"],
      "gender": "female"
    }
  ]
}
```

### play_audio_file

播放一个音频文件。

**参数:**
- `file_path` (必需, `string`): 要播放的音频文件的绝对路径。
- `volume` (可选, `float`): 音量 (0.0 到 1.0)。

### stop_audio

停止当前所有音频播放（包括TTS和文件播放）。

**参数:** 无

### get_audio_status

获取音频系统的当前状态。

**参数:** 无

## 🔧 使用方式

### 1. 独立模式
```bash
python audio_server.py --interactive
```

### 2. JSON-RPC模式 (用于MCP集成)
```bash
python audio_server.py
```

然后发送JSON-RPC请求到stdin:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "speak_text",
    "arguments": {
      "text": "Hello from AI!"
    }
  },
  "id": 1
}
```

### 3. MCP客户端配置

在MCP客户端配置文件中添加:
```json
{
  "mcpServers": {
    "audio-server": {
      "command": "python",
      "args": ["/path/to/audio_server.py"]
    }
  }
}
```

## 📁 项目文件

- `audio_server.py` - 主服务器文件
- `demo_audio_server.py` - 演示脚本
- `test_audio_server.py` - 测试脚本
- `test_json_rpc.py` - JSON-RPC接口测试
- `requirements.txt` - 依赖列表
- `config.json` - 配置文件
- `README.md` - 项目说明
- `setup.py` - 安装脚本

## 🎵 支持的音频格式

- MP3
- WAV
- OGG
- FLAC
- 其他pygame支持的格式

## 🔍 故障排除

### 常见问题

1. **TTS引擎初始化失败**
   - 确保系统有可用的TTS引擎
   - macOS: 内置语音合成
   - Windows: 需要SAPI
   - Linux: 需要espeak

2. **音频播放失败**
   - 检查音频文件是否存在
   - 确保文件格式受支持
   - 检查系统音频设备

3. **权限问题**
   - 确保Python有访问音频设备的权限

## 🧪 测试

运行所有测试:
```bash
python test_audio_server.py
python demo_audio_server.py
```

## 📝 开发

要添加新功能:
1. 在 `AudioPlayer` 类中添加新方法
2. 在 `MCPAudioServer.tools` 中注册新工具
3. 在 `call_tool` 方法中添加处理逻辑

## 📄 许可证

MIT License
