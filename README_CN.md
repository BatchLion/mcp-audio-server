# MCP 音频服务器 🔊

*[English](README.md) | [中文](README_CN.md)*

一个强大的模型上下文协议 (MCP) 服务器，为 Claude Desktop 和其他 MCP 客户端提供文本转语音和音频播放功能。

## ✨ 功能特性

- **🗣️ 高品质文本转语音 (TTS)**:
  - **智能语言检测**: 自动为中文使用谷歌 TTS 以获得高品质语音，其他语言则使用系统自带 TTS。
  - **语音选择**: 对于非中文文本，可以列出并选择系统上安装的多种语音。
  - **自定义语音**: 可调节语速和音量，获得定制化的听觉体验。
- **🎵 音频文件播放**: 支持播放各种音频格式 (WAV, MP3, OGG 等)。
- **⏹️ 音频控制**: 停止播放并获取实时音频状态。
- **🔌 MCP 兼容**: 完全兼容 Claude Desktop 及 MCP 规范 2024-11-05。
- **🛡️ 错误处理**: 稳健的错误处理和验证机制。
- **📊 状态监控**: 实时监控音频系统状态和播放信息。

## 🚀 快速入门

### 先决条件

- Python 3.8+
- Claude Desktop (用于 MCP 集成)
- 可用的系统音频功能

### 安装

1.  **克隆仓库:**
    ```bash
    git clone https://github.com/yourusername/mcp-audio-server.git
    cd mcp-audio-server
    ```

2.  **安装依赖:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置 Claude Desktop:**
    在您的 `claude_desktop_config.json` 文件中添加:
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

4.  **重启 Claude Desktop** 即可开始使用音频功能！

## 🛠️ 可用工具

| 工具 | 描述 | 参数 |
|---|---|---|
| `speak_text` | 将文本转换为语音。自动为中文使用谷歌TTS。 | `text` (必需), `rate` (可选), `volume` (可选), `voice_id` (可选, 用于非中文) |
| `list_voices` | 列出可用于非中文语言的TTS语音。 | 无 |
| `play_audio_file` | 播放一个音频文件。 | `file_path` (必需), `volume` (可选) |
| `stop_audio` | 停止当前音频播放。 | 无 |
| `get_audio_status` | 获取音频系统状态。 | 无 |

## 📖 使用示例

### 文本转语音 (中文)
```
"请用语音说出 '你好，世界'"
```
*这会自动使用谷歌TTS以获得自然流畅的发音。*

### 文本转语音 (英文, 使用特定语音)
1.  **首先, 列出可用语音:**
    ```
    "列出所有可用的语音"
    ```
2.  **然后, 使用列表中的一个语音ID:**
    ```
    "使用ID为 'com.apple.speech.synthesis.voice.daniel' 的语音说 'Hello, this is a test.'"
    ```

### 播放音频文件
```
"播放位于 /path/to/music.mp3 的音频文件"
```

### 停止音频
```
"停止当前音频播放"
```

### 查询状态
```
"当前的音频状态是什么？"
```

## 🧪 测试

运行全面的测试套件:
```bash
# 测试所有 MCP 方法
python test_all_mcp_methods.py

# 测试 Claude Desktop 格式兼容性
python test_claude_desktop_format.py

# 测试音频功能
python test_audio_server.py

# 交互式测试模式
python audio_server.py --interactive
```

## 🔧 配置

### Claude Desktop 配置

本服务器可与 Claude Desktop 无缝集成。请确保您的配置文件设置正确。

**位置:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**配置示例:**
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

## 🐛 问题排查

### 常见问题

1.  **音频无法播放**: 检查系统音频设置和权限。
2.  **TTS 不工作**: 确保 `pyttsx3` 和 `gTTS` 已正确安装。对于中文TTS，请检查网络连接。
3.  **MCP 连接问题**: 验证 Claude Desktop 配置文件中的路径是否正确。
4.  **权限错误**: 检查音频文件的读取权限。

### 调试模式

运行交互模式以进行调试:
```bash
python audio_server.py --interactive
```

## 🙏 致谢

- 基于模型上下文协议 (MCP) 构建
- 使用 `pyttsx3` 和 `gTTS` 进行文本转语音
- 使用 `pygame` 进行音频播放
- 兼容 Claude Desktop

---

**为 MCP 社区 ❤️ 制作**