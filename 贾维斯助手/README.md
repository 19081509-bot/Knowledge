---
created: 2026-07-28
tags:
  - jarvis
  - index
  - project
aliases:
  - 贾维斯
  - Jarvis
  - 语音助手
---

# 🦞 贾维斯语音助手

> AI 语音助手，唤醒即用

---

## 📄 文档索引

| 文档 | 说明 |
|------|------|
| [[贾维斯部署方案.md]] | 完整项目架构与技术方案 |
| [[AI对话存档/贾维斯语音助手开发/2026-07-26-全链路搭建.md]] | 开发日志 |
| [[_ai/skills/jarvis-voice.md]] | OpenClaw 语音交互技能 |
| [[_ai/skills/jarvis-desktop.md]] | OpenClaw 桌面控制技能 |
| [[_ai/skills/jarvis-smarthome.md]] | OpenClaw 智能家居技能 |

## 📜 源代码

| 文件 | 说明 |
|------|------|
| `scripts/jarvis-stt.py` | 🎤 语音→文本 |
| `scripts/jarvis-tts.py` | 🔊 文本→语音 |
| `scripts/jarvis-wake.py` | 🔔 唤醒主循环 |

## 🔧 快速命令

```bash
# 启动唤醒
python3 ~/scripts/jarvis-wake.py

# 测试录音
python3 ~/scripts/jarvis-stt.py 5

# 测试朗读
python3 ~/scripts/jarvis-tts.py "你好，我是贾维斯"
```

## 🎯 技术栈

- **语音识别**: 达摩院 SenseVoiceSmall（硅基流动 API）
- **AI 大脑**: DeepSeek V4 Pro / Qwen 2.5（Ollama）
- **语音合成**: Edge TTS 微软晓晓
- **网关**: OpenClaw Gateway
- **TTS 降级**: macOS say (Tingting)
