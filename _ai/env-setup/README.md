# Codex++ 中转方案（Mac → Windows 局域网 relay）

## 架构

```
Mac Codex CLI → Windows Codex++ (57321) → 硅基流动 API → DeepSeek
```

## Windows 端（Codex++ 图形 UI）

### 安装
- 程序路径: `%USERPROFILE%\AppData\Local\Programs\Codex++\`
- 两个 exe:
  - `codex-plus-plus-manager.exe` — 管理窗口
  - `codex-plus-plus.exe` — 图形 UI（需 Codex Desktop 桌面版才能叠加）

### 配置目录
- `%USERPROFILE%\.codex-session-delete\settings.json`

### 关键配置项（configContents）
```toml
model = "deepseek-ai/DeepSeek-V4-Flash"
model_provider = "custom"

[model_providers.custom]
name = "custom"
wire_api = "chat"                    # ← 必须 chat，不能是 responses
requires_openai_auth = true
base_url = "http://127.0.0.1:57321/v1"
```

### 端口
- 中转监听: `127.0.0.1:57321`
- 局域网访问需加端口转发:
  ```powershell
  netsh interface portproxy add v4tov4 listenport=57321 listenaddress=0.0.0.0 connectport=57321 connectaddress=127.0.0.1
  netsh advfirewall firewall add rule name="Codex++ 57321" dir=in action=allow protocol=TCP localport=57321
  ```

## Mac 端（config.toml）

路径: `~/.codex/config.toml`

### 直连硅基流动（不走中转时）
```toml
model = "deepseek-ai/DeepSeek-V4-Flash"
sandbox_mode = "danger-full-access"
wire_api = "chat"

[model_providers.custom]
name = "siliconflow-relay"
base_url = "https://api.siliconflow.cn/v1"
wire_api = "chat"
requires_openai_auth = true
```

### 走 Windows 中转时
```toml
[model_providers.custom]
name = "siliconflow-relay"
base_url = "http://192.168.2.166:57321/v1"
wire_api = "chat"
requires_openai_auth = true
```

## 全链路校验

```bash
# Mac 测试 Windows 中转是否通
curl http://192.168.2.166:57321/v1/models

# Mac 测试调用 DeepSeek
curl http://192.168.2.166:57321/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxx" \
  -d '{"model":"deepseek-ai/DeepSeek-V4-Flash","messages":[{"role":"user","content":"hi"}]}'
```

## 注意事项

1. `wire_api` 必须统一为 `chat`（两端都要对）
2. Windows 防火墙必须放行 57321
3. Mac 和 Windows 必须在同一局域网
4. Codex++ 图形 UI 需要 Codex Desktop 桌面版（Electron），纯 CLI 版无法叠加
