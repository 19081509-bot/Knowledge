---
date: 2026-07-26
tags: [AI对话, 待分类]
---

## Windows Codex++ 端口占用故障

### 现象
Codex++ 升级后启动报：`failed to bind helper runtime on 127.0.0.1:57321`

### 根因
端口 57321 被系统服务（svchost.exe, PID 7936）占用，Codex++ Helper Runtime 绑定失败。

### 解决方案
不纠结占端口的进程，直接**换端口**：

```powershell
# 1. Codex++ 设置里把端口从 57321 改成 57322

# 2. 防火墙放行新端口
netsh advfirewall firewall add rule name="Codex++ 57322" dir=in action=allow protocol=TCP localport=57322

# 3. 改配置文件中的端口
(Get-Content "$env:USERPROFILE\.codex-session-delete\settings.json") `
  -replace ':57321', ':57322' `
  | Set-Content "$env:USERPROFILE\.codex-session-delete\settings.json"

# 4. 重启 Codex++
```

### Windows Codex++ 配置文件关键字段
```toml
[model_providers.custom]
name = "custom"
wire_api = "responses"
requires_openai_auth = true
base_url = "http://127.0.0.1:57322/v1"
```

### 关联
- [[2026-07-26-最终架构-codex-relay+relay-ai分工]]