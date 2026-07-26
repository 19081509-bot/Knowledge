---
date: 2026-07-26
tags: [AI对话, 待分类]
---

## 最终架构定稿：codex-relay + relay-ai 分工

### 结论

**不用 relay-ai 统一所有工具。** relay-ai v0.6.3 不支持 `/v1/responses` 协议，Codex Desktop 必须走 codex-relay。

### 最终分工

| 工具 | 网关 | 端口 | 运行方式 |
|------|------|------|---------|
| Codex Desktop | codex-relay | 4446 | launchd 后台（com.codex-relay） |
| Claude Code | relay-ai | 17645/anthropic | launchd 后台（com.relay-ai.server） |
| Claudian (Obsidian) | relay-ai | 17645/openai/v1 | Obsidian 插件设置 |
| OpenClaw | 直连硅基 | — | 不变 |

### 协议映射

| 客户端 | 协议 | 网关处理 |
|--------|------|---------|
| Codex Desktop | POST /v1/responses | codex-relay → chat/completions → SiliconFlow |
| Claude Code | POST /v1/messages (Anthropic) | relay-ai SDK proxy → chat/completions → SiliconFlow |
| Claudian | POST /v1/chat/completions | relay-ai → chat/completions → SiliconFlow |

### 关键命令

**codex-relay launchd 安装：**
```xml
<!-- ~/Library/LaunchAgents/com.codex-relay.plist -->
<key>ProgramArguments</key>
<array>
    <string>/Library/Frameworks/Python.framework/Versions/3.14/bin/codex-relay</string>
    <string>--upstream</string>
    <string>https://api.siliconflow.cn/v1</string>
    <string>--api-key</string>
    <string>sk-iybgixsjrstotytjuwwlmwuannkgjaexqrnlijrhvkfnogqy</string>
    <string>--port</string>
    <string>4446</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<true/>
```

**加载命令：**
```bash
launchctl load ~/Library/LaunchAgents/com.codex-relay.plist
```

**relay-ai server：**
```bash
export SILICONFLOW_API_KEY=sk-iyb...
relay-ai server --listen local --providers custom-siliconflow2
```

**Codex Desktop 配置（~/.codex/config.toml）：**
```toml
model_provider = "custom"
[model_providers.custom]
name = "codex-relay"
base_url = "http://127.0.0.1:4446/v1"
wire_api = "responses"
requires_openai_auth = false
api_key = "dummy"
```

**Claude Code 配置（~/.claude/settings.json）：**
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:17645/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "anything"
  }
}
```

### 注意事项
1. codex-relay 和 relay-ai 是独立的两个 launchd 服务，互不干扰
2. Windows 上的 Codex++ 直连硅基，不经过 Mac 的网关
3. codex-relay 升级后如果报 `20012 Model does not exist`，通常是上游波动，重试即可

### 关联
- [[relay-ai-部署记录]] relay-ai 部署失败的教训
- [[codex-troubleshooting]] Codex 数据库崩溃修复
- [[relay-ai-codex-troubleshooting]] responses 404 排查