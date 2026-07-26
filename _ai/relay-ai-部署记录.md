# relay-ai 统一网关 — 部署记录

> 最后更新：2026-07-23
> 适用：Codex Desktop / Claude Code / Claudian

---

## 一、架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    relay-ai server                           │
│                    port 17645 (固定)                         │
│                                                             │
│   /anthropic ── SDK proxy ── SiliconFlow (chat/completions)  │
│   /openai/v1 ── SDK proxy ── SiliconFlow (chat/completions)  │
│                                                             │
│   Codex Desktop 不走直连，走 relay-ai codex-app 临时代理       │
│   临时代理 (随机端口) ── responses→chat 转换 ── relay-ai     │
└─────────────────────────────────────────────────────────────┘
        ▲              ▲              ▲              ▲
        │              │              │              │
   Codex Desktop  Claude Code    Claudian      OpenClaw
   (codex-app)   (messages)    (chat)       (保持直连)
```

## 二、协议映射（核心）

| 客户端 | 发送协议 | relay-ai 接收端 | relay-ai 转成 | 最终到达上游 |
|--------|----------|----------------|---------------|-------------|
| Codex Desktop | `/v1/responses` | 临时代理 (codex-app) | `chat/completions` | SiliconFlow |
| Claude Code | `/v1/messages` (Anthropic) | `/anthropic/v1/messages` | `chat/completions` | SiliconFlow |
| Claudian | `/v1/chat/completions` | `/openai/v1/chat/completions` | `chat/completions` | SiliconFlow |
| OpenClaw | 自有的 Gateway 协议 | 不经过 relay-ai | — | SiliconFlow 直连 |

**关键限制：**
- relay-ai v0.6.2 **不支持** `--enable-codex-responses` 参数
- Codex Desktop 新版强制 POST `/v1/responses`，普通 OpenAI 兼容网关只处理 `chat/completions`
- 解决方式：用 `relay-ai codex-app` 启动 Codex，它自动创建临时代理做协议转换

## 三、工具配置详情

### relay-ai server（端口 17645）

**Provider 注册信息：**
- ID: `custom-siliconflow2`
- 类型: `custom-openai`（OpenAI-compatible）
- Base URL: `https://api.siliconflow.cn/v1`
- API Key: macOS Keychain（`keyring:provider:custom-siliconflow2`）

**启动命令：**
```bash
export SILICONFLOW_API_KEY=sk-iybgixsjrstotytjuwwlmwuannkgjaexqrnlijrhvkfnogqy
relay-ai server --listen local --providers custom-siliconflow2
```

**端点：**
```
Anthropic:  http://127.0.0.1:17645/anthropic
OpenAI:     http://127.0.0.1:17645/openai/v1
API key:    any non-empty value
```

**加载模型：** 91 个（来自 SiliconFlow）

### Codex Desktop

**启动方式（必须通过 relay-ai 启动器，不能直连）：**
```bash
relay-ai codex-app --provider custom-siliconflow2 --model deepseek-ai/DeepSeek-V4-Flash
```

启动后：
1. relay-ai 创建临时代理（随机端口，如 60370/60492）
2. 自动修改 `~/.codex/config.toml` 指向临时代理
3. 临时代理处理 `responses → chat/completions` 转换
4. 用完 `Ctrl+C` → 选 Yes 恢复原配置

**遗留的 `~/.codex/config.toml` 静态配置（仅作 fallback，不影响 codex-app 启动）：**
```toml
[model_providers.custom]
name = "relay-ai-gateway"
base_url = "http://127.0.0.1:17645/openai/v1"
wire_api = "responses"
requires_openai_auth = true
api_key = "anything"
request_timeout_sec = 360
stream_keepalive_ms = 10000
```

> ⚠️ 新版 ChatGPT Desktop（Codex 模式）会读顶层 `openai_base_url` 和 `model_provider = "openai"`，`[model_providers.custom]` 段已废弃。但 codex-app 启动器会自动切换，无需手动管理。

### Claude Code

**配置文件 `~/.claude/settings.json`：**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "anything",
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:17645/anthropic",
    "ANTHROPIC_MODEL": "deepseek-ai/DeepSeek-V4-Flash",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-ai/DeepSeek-V4-Flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-ai/DeepSeek-V4-Flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-ai/DeepSeek-V4-Flash",
    "ANTHROPIC_REASONING_MODEL": "deepseek-ai/DeepSeek-V4-Flash"
  }
}
```

### Claudian（Obsidian 插件）

**设置路径：** Obsidian → 左侧 Claudian 图标 → 设置 → Codex 标签

```
API 地址：http://127.0.0.1:17645/openai/v1
模型：deepseek-ai/DeepSeek-V4-Flash
```

### OpenClaw

保持原有配置，直连 SiliconFlow，不受 relay-ai 影响。

---

## 四、启动顺序

```
1. relay-ai server（前台窗口，不能关）
   export SILICONFLOW_API_KEY=sk-iyb...
   relay-ai server --listen local --providers custom-siliconflow2

2. Claude Code（可直接用，settings.json 已配好）
   claude -p "你好"

3. Codex Desktop（通过 relay-ai 启动器）
   relay-ai codex-app --provider custom-siliconflow2 --model deepseek-ai/DeepSeek-V4-Flash

4. Claudian（Obsidian 打开自动加载）
```

---

## 五、端口对照

| 端口 | 服务 | 说明 |
|------|------|------|
| **17645** | relay-ai server | 统一网关（固定端口） |
| 随机端口 | relay-ai codex-app 临时代理 | 每次启动随机分配 |
| 18789 | OpenClaw Gateway | 不受影响 |
| 7897 | Clash Verge | 系统代理 |
| 36677 | PicGo | 图床上传 |
| 27124 | Obsidian Local REST API | Obsidian API |

---

## 六、退役组件

| 退役 | 替代 |
|------|------|
| codex-relay (port 4446, Python) | relay-ai server (port 17645) |
| ccswitch 协议转换层 | relay-ai SDK proxy 内置 |
| `[model_providers.custom]` 段 | 顶层 `openai_base_url`（新版 Codex 格式） |

> 注意：codex-relay 的 launchd（`com.codex-relay`）已停用，plist 已备份到 `/Library/LaunchAgents/com.codex-relay.plist.bak`

---

## 七、排查

| 现象 | 原因 | 修复 |
|------|------|------|
| Codex 返回 404 `/v1/responses` | 直连 relay-ai，但 relay-ai 不支持 responses | 改用 `relay-ai codex-app` 启动 |
| relay-ai server 报 "No providers configured" | providers.json 格式不对或 env 变量未设 | 设 `SILICONFLOW_API_KEY`，或 `relay-ai providers add` 重加 |
| relay-ai server 报 "No models to expose" | provider ID 和 --providers 参数不匹配 | 用 `relay-ai providers list` 确认 ID |
| relay-ai codex-app 报 "another session may be running" | 上次代理进程残留 | `relay-ai codex-app --restore` 清理 |
| Claude Code 连不上 | ANTHROPIC_BASE_URL 指向错误 | 确认是 `http://127.0.0.1:17645/anthropic` |
| Claudian 连不上 | API 地址格式错误 | 确保是 `http://127.0.0.1:17645/openai/v1`（不要漏 `/v1`） |

---

## 八、回退

如需恢复到旧的 codex-relay：

```bash
# 停 relay-ai
# Ctrl+C 关闭前台窗口

# 重启 codex-relay
launchctl bootstrap gui/$(id -u) /Library/LaunchAgents/com.codex-relay.plist.bak

# 恢复 Claude Code 配置
# ~/.claude/settings.json → ANTHROPIC_BASE_URL 改回 https://api.siliconflow.cn

# Codex Desktop 直接打开即可（config.toml 恢复后指向 4446）
```

---

## 九、注意事项

1. **relay-ai server 窗口不能关**，关了所有工具断连
2. **API Key 只填在 relay-ai 内部**，所有客户端用 `anything` 占位
3. **换 Provider 只需改 relay-ai 的 provider 注册**，各工具配置不动
4. **Clash Verge 与 relay-ai 端口不冲突**（17645 vs 7897），无需退出 Clash
5. **codex-relay 的 launchd plist 已备份**，如需恢复可手动拉起