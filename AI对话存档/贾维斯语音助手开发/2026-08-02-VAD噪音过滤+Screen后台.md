---
created: 2026-08-02
tags:
  - jarvis
  - voice-assistant
  - development-log
  - vad
  - noise-filter
  - screen
  - background
---

# 🦞 贾维斯 v3 — VAD 噪音过滤 + Screen 后台运行

> 日期: 2026-08-02

---

## ✅ 当前状态

| 功能 | 状态 |
|------|------|
| 🎤 流式 VAD 唤醒（30ms帧级） | ✅ 工作 |
| 🧠 DeepSeek V4 Pro 问答 | ✅ 工作 |
| 🌐 联网搜索 / 天气查询 | ✅ 工作 |
| 🔊 Edge TTS (云健男声) + 科幻混响 | ✅ 工作 |
| 💬 连续对话（10s超时退下） | ✅ 工作 |
| 🔇 后台运行（Screen） | ✅ 工作 |
| 🚀 开机自启（登录项） | ⚠️ 脚本已创建，待用户配置 |

---

## 🐛 修复的问题

### 1. launchd 找不到 ffmpeg

**症状**：`FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**原因**：launchd 的 PATH 环境变量不含 `/usr/local/bin`（Homebrew 目录）。

**修复**：将代码中的 `'ffmpeg'` 改为全路径 `'/usr/local/bin/ffmpeg'`。

涉及文件：
- `jarvis-wake.py` — AudioStream 类
- `jarvis-tts.py` — 混响处理（Codex 已改全路径）

### 2. launchd 无麦克风权限

**症状**：进程启动正常，但 VAD 永不触发（30 分钟 0 次 STT 调用）。

**原因**：macOS 的麦克风权限按应用授予。Terminal.app 有权限，launchd 直接启动的 python3 没有权限。ffmpeg 能运行但输出静音数据。

**解决方案**：放弃 launchd，改用 `screen`：

```bash
screen -dmS jarvis python3 ~/scripts/jarvis-wake.py
```

Screen 运行在伪终端中，继承终端的麦克风权限。

### 3. 环境噪音占用 STT 限流

**症状**：VAD 被环境噪音持续触发，录音 8 秒撞上限 → 调 STT API → 吃满 4次/分钟限流 → 用户真说话时 `stt_blocked`。

**修复**：`record_utterance()` 返回两个值 `(pcm_data, hit_max)`。`hit_max=True` 表示录音因为撞到 `MAX_RECORD_MS` 上限（8秒）而结束，说明是持续噪音而非人声。`standby_loop` 遇到 `hit_max=True` 直接跳过 STT 调用，不消耗限流。

```python
# record_utterance 新版返回值
pcm, hit_max = record_utterance(stream, vad)
if hit_max:
    continue  # 噪音 → 跳过 STT，不消耗限流
```

---

## 🔧 当前配置

| 参数 | 值 | 说明 |
|------|-----|------|
| `VAD_RATIO` | 4.0 | 能量阈值倍率 |
| `VAD_MIN_TH` | 1200 | 最低阈值 |
| `MIN_SPEECH_MS` | 400 | 最短语音 |
| `MAX_RECORD_MS` | 8000 | 最长录音（撞上限视为噪音） |
| `SILENCE_TIMEOUT_MS` | 10000 | 沉默超时退下 |
| `SILENCE_PAUSE_MS` | 1200 | 句尾停顿判定 |
| `_stt_tm` 限流 | 4次/分钟 | SenseVoice STT |
| `_llm_tm` 限流 | 6次/分钟 | DeepSeek V4 |

---

## 📁 文件清单

| 路径 | 用途 |
|------|------|
| `~/scripts/jarvis-wake.py` | 主循环（VAD + API + 联网） |
| `~/scripts/jarvis-tts.py` | TTS（Edge TTS 云健男声 + 混响） |
| `~/scripts/jarvis-stt.py` | STT 单测（独立脚本） |
| `~/scripts/jarvis-start.sh` | 开机自启脚本（screen 方式） |
| `~/Library/LaunchAgents/com.jarvis.wake.plist` | ⚠️ launchd plist（麦克风问题，未使用） |
| `~/scripts/jarvis.log` | 运行日志 |
| `~/scripts/jarvis.pid` | PID 记录 |

---

## 📋 待办

- [ ] `active_loop` 的 `hit_max` 处理（当前只有 `standby_loop` 有）
- [ ] macOS 登录项配置（让 `jarvis-start.sh` 开机自启）
- [ ] VAD 阈值进一步调试（根据使用环境微调）
- [ ] App 操控（AppleScript）
- [ ] 屏幕交互
- [ ] 智能家居（Home Assistant）