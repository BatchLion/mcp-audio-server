# MCP Audio Server

一个基于MCP (Model Context Protocol) 的音频服务器，允许AI模型通过系统音频播放器发出声音。

## 功能特性

- **文本转语音 (TTS)**: 将文本转换为语音并播放
- **音频文件播放**: 播放各种格式的音频文件
- **音量控制**: 调整播放音量
- **播放控制**: 停止当前播放
- **状态查询**: 获取音频系统状态

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 启动服务器

```bash
python audio_server.py
```

### 可用工具

#### 1. speak_text
将文本转换为语音并播放

**参数:**
- `text` (必需): 要转换为语音的文本
- `rate` (可选): 语音速度 (50-300 词/分钟，默认: 150)
- `volume` (可选): 音量级别 (0.0-1.0，默认: 0.8)

**示例:**
```json
{
  "text": "Hello, this is a test message",
  "rate": 150,
  "volume": 0.8
}
```

#### 2. play_audio_file
播放音频文件

**参数:**
- `file_path` (必需): 音频文件路径
- `volume` (可选): 音量级别 (0.0-1.0)

**示例:**
```json
{
  "file_path": "/path/to/audio/file.mp3",
  "volume": 0.7
}
```

#### 3. stop_audio
停止当前音频播放

**参数:** 无

#### 4. get_audio_status
获取音频系统状态

**参数:** 无

**返回示例:**
```json
{
  "success": true,
  "status": {
    "tts_available": true,
    "pygame_available": true,
    "music_playing": false
  }
}
```

## 支持的音频格式

- MP3
- WAV
- OGG
- FLAC
- 其他pygame支持的格式

## 系统要求

- Python 3.8+
- 系统音频设备
- 支持的操作系统: Windows, macOS, Linux

## 配置MCP客户端

要在MCP客户端中使用此服务器，请在配置文件中添加：

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

## 故障排除

### 常见问题

1. **TTS引擎初始化失败**
   - 确保系统有可用的TTS引擎
   - 在Windows上可能需要安装SAPI
   - 在Linux上可能需要安装espeak

2. **音频播放失败**
   - 检查音频文件是否存在
   - 确保音频文件格式受支持
   - 检查系统音频设备是否正常工作

3. **权限问题**
   - 确保Python有访问音频设备的权限
   - 在某些系统上可能需要管理员权限

## 开发

### 添加新功能

要添加新的音频功能，请：

1. 在 `AudioPlayer` 类中添加新方法
2. 在 `handle_list_tools()` 中注册新工具
3. 在 `handle_call_tool()` 中添加处理逻辑

### 测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行测试
pytest tests/
```

## 许可证

MIT License
