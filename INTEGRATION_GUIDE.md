# 🎵 MCP Audio Server 集成指南

## 🎉 集成完成！

你的MCP Audio Server已经成功集成并可以使用了！以下是完整的使用指南。

## 📋 集成状态

✅ **服务器已安装并配置完成**
✅ **所有依赖项已安装**
✅ **Claude Desktop配置已创建**
✅ **通用MCP配置已生成**
✅ **所有测试通过 (7/7)**

## 🚀 如何使用

### 1. Claude Desktop 集成

如果你使用Claude Desktop：

1. **重启Claude Desktop应用**
2. **音频服务器将自动可用，名称为 'audio-server'**
3. **配置文件位置**: `/Users/batchlions/Library/Application Support/Claude/claude_desktop_config.json`

在Claude Desktop中，你可以这样使用：
```
请使用音频功能说"Hello World"
```

### 2. 其他MCP客户端

对于其他MCP客户端，使用以下配置：

**配置文件**: `/Users/batchlions/Documents/augment-projects/MCPAgent/mcp_server_config.json`

```json
{
  "mcpServers": {
    "audio-server": {
      "command": "/Users/batchlions/miniconda3/envs/mcp_agent/bin/python",
      "args": ["/Users/batchlions/Documents/augment-projects/MCPAgent/audio_server.py"],
      "env": {
        "PYTHONPATH": "/Users/batchlions/Documents/augment-projects/MCPAgent",
        "PYGAME_HIDE_SUPPORT_PROMPT": "1"
      }
    }
  }
}
```

### 3. 手动测试

#### 启动服务器
```bash
cd /Users/batchlions/Documents/augment-projects/MCPAgent
./start_audio_server.sh
```

#### 交互模式测试
```bash
/Users/batchlions/miniconda3/envs/mcp_agent/bin/python audio_server.py --interactive
```

#### 运行集成测试
```bash
./test_integration.sh
```

## 🛠️ 可用工具

### 1. speak_text
将文本转换为语音并播放

**参数:**
- `text` (必需): 要转换的文本
- `rate` (可选): 语音速度 (50-300 词/分钟，默认: 150)
- `volume` (可选): 音量 (0.0-1.0，默认: 0.8)

**示例使用:**
```
请用慢速语音说"这是一个测试"
请用大声音量说"重要通知"
```

### 2. play_audio_file
播放音频文件

**参数:**
- `file_path` (必需): 音频文件路径
- `volume` (可选): 音量 (0.0-1.0)

**示例使用:**
```
请播放文件 /path/to/music.mp3
```

### 3. stop_audio
停止当前音频播放

**示例使用:**
```
请停止当前的音频播放
```

### 4. get_audio_status
获取音频系统状态

**示例使用:**
```
请检查音频系统状态
```

## 🎯 AI模型使用示例

以下是AI模型如何使用音频功能的示例：

### 基础语音输出
```
AI: 我现在可以通过语音与你交流了！
[使用 speak_text 工具播放语音]
```

### 动态语音参数
```
用户: 请说得慢一点
AI: 好的，我会说得更慢一些。
[使用 speak_text 工具，rate=100]
```

### 音量控制
```
用户: 请说得大声一点
AI: 现在我会大声说话！
[使用 speak_text 工具，volume=1.0]
```

### 状态查询
```
用户: 音频系统工作正常吗？
AI: 让我检查一下音频系统状态...
[使用 get_audio_status 工具]
AI: 音频系统工作正常，TTS可用，音频系统就绪。
```

## 📁 文件结构

```
MCPAgent/
├── audio_server.py              # 主服务器文件
├── claude_desktop_config.json   # Claude Desktop配置
├── mcp_server_config.json       # 通用MCP配置
├── start_audio_server.sh        # 启动脚本
├── test_integration.sh          # 集成测试脚本
├── install_and_setup.sh         # 安装设置脚本
├── demo_audio_server.py         # 演示脚本
├── ai_integration_demo.py       # AI集成演示
├── test_report.py               # 测试报告
├── requirements.txt             # 依赖列表
├── README.md                    # 项目说明
├── USAGE_GUIDE.md              # 使用指南
└── INTEGRATION_GUIDE.md        # 本集成指南
```

## 🔧 故障排除

### 常见问题

1. **Claude Desktop中看不到音频工具**
   - 确保重启了Claude Desktop
   - 检查配置文件是否正确创建
   - 路径: `/Users/batchlions/Library/Application Support/Claude/claude_desktop_config.json`

2. **TTS不工作**
   - 确保系统音频设备正常
   - 检查音量设置
   - 运行测试: `python test_report.py`

3. **权限问题**
   - 确保Python有访问音频设备的权限
   - 检查conda环境是否激活

4. **依赖问题**
   - 重新运行: `./install_and_setup.sh`
   - 手动安装: `pip install -r requirements.txt`

### 调试命令

```bash
# 检查服务器状态
python test_report.py

# 测试基础功能
python demo_audio_server.py

# 完整集成测试
./test_integration.sh

# 交互式测试
python audio_server.py --interactive
```

## 🎊 成功！

你的MCP Audio Server现在已经完全集成并可以使用了！

### 下一步
1. 在Claude Desktop中尝试使用音频功能
2. 探索不同的语音参数和设置
3. 根据需要自定义音频功能

### 支持的功能
- ✅ 文本转语音
- ✅ 音频文件播放
- ✅ 音量和语速控制
- ✅ 播放控制
- ✅ 状态查询
- ✅ 错误处理
- ✅ 参数验证

**🎵 享受你的AI音频助手吧！**
