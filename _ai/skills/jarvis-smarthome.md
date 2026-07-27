---
name: jarvis-smarthome
description: 智能家居控制 — 通过 Home Assistant MCP 控制灯光、传感器、场景
---

## 概述

通过 Home Assistant MCP 协议连接和控制智能家居设备。

## 前提条件

- 需要运行 Home Assistant 实例（本机或局域网）
- 需要长期访问令牌

## 能力范围

- 💡 **灯光控制**：开关、调光、色温、颜色
- 🌡️ **环境监测**：温度、湿度、空气质量
- 🚪 **门窗传感器**：开关状态检测
- 🔌 **插座/开关**：电源控制
- 📋 **场景自动化**：一键执行场景模式
- 📺 **媒体设备**：电视、音响控制

## 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json5
{
  "tools": {
    "mcpServers": {
      "homeassistant": {
        "command": "npx",
        "args": ["-y", "@home-assistant/mcp"],
        "env": {
          "HA_URL": "http://192.168.2.67:8123",
          "HA_TOKEN": "你的长期访问令牌"
        }
      }
    }
  }
}
```

## 使用示例

```
用户: "贾维斯，打开客厅的灯"
AI: → 调用 homeassistant 的 light.turn_on 服务 → 确认执行 → TTS 反馈

用户: "贾维斯，现在室温多少？"
AI: → 读取传感器数据 → TTS 播报 "当前室温 26°C，湿度 60%"
```

## 注意事项

- ⚠️ 首次配置需要获取 HA 长期访问令牌（Profile → 长期访问令牌）
- ⚠️ 确保 HA 实例与 OpenClaw 在同一网络
- ⚠️ 敏感操作（如门锁）建议加入二次确认
