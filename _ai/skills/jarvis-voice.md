---
name: jarvis-voice
description: 语音交互技能 — 语音输入（Whisper）+ 语音输出（macOS say/Piper TTS）
---

## 概述

提供语音交互能力。使用户可以通过语音与 AI 对话，AI 通过语音回复。

## 语音输入（STT）

使用 whisper.cpp 将麦克风录制音频转为文本：

```bash
# 录制 5 秒并转写
python3 ~/scripts/jarvis-stt.py 5

# 或直接调用 whisper.cpp
~/whisper.cpp/main -m ~/whisper.cpp/models/ggml-tiny.bin \
  -f /tmp/recording.wav --language zh --no-timestamps
```

## 语音输出（TTS）

使用 macOS 内置语音合成：

```bash
# 中文语音朗读
python3 ~/scripts/jarvis-tts.py "你好，我是虾癫癫" "Eddy"

# 或直接使用 say 命令
say -v 'Ting-Ting' "你好，我是你的贾维斯助手"
```

## 唤醒词

使用 Porcupine 监听唤醒词：

```bash
# 启动唤醒词监听
python3 ~/scripts/jarvis-wake.py
```

检测到唤醒词后：
1. 触发录音（默认 10 秒）
2. 语音转文本
3. 文本传给 OpenClaw 处理
4. OpenClaw 回复通过 TTS 朗读

## 使用场景

- 📝 **语音提问**："贾维斯，今天天气怎么样？"
- 🎛️ **语音控制**："贾维斯，打开浏览器搜索..."
- 💬 **连续对话**：唤醒一次后可连续对话（等待 3 秒静默结束）
- 🔊 **语音播报**：让 AI 朗读新闻、日记、长文本

## 依赖

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| whisper.cpp | 语音→文本 | `~/whisper.cpp/` 编译 |
| ffmpeg | 音频录制 | `brew install ffmpeg` |
| macOS `say` | 文本→语音 | 系统内置 |
| Porcupine | 唤醒词检测 | `pip install pvporcupine` |
| Piper TTS（可选） | 高质量中文TTS | `brew install piper` |

## 脚本

- `~/scripts/jarvis-stt.py` — 语音→文本
- `~/scripts/jarvis-tts.py` — 文本→语音
- `~/scripts/jarvis-wake.py` — 唤醒词监听
