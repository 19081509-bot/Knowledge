## 2026-08-23 codex-relay 健康检查与 launchd 托管确认

### 事件背景
本机 Codex 报 `502 Bad Gateway: Unknown error, url: http://127.0.0.1:4446/v1/responses`。经排查确认为瞬时上游传输中断，链路本身健康。

### 结论
1. **codex-relay 健康**：PID 738 连续运行 15 天，CPU 0.0% / 内存 284K，91 模型正常加载，08-13 之后无新错误。
2. **502 根因**：`upstream request failed: error sending request` / `SSE parse error: error decoding response body` — 上游 SiliconFlow 流式传输瞬时断开，属抖动，非配置错误。
3. **Tailscale 不占 4446**：Tailscale 用 WireGuard UDP（utun 网卡，100.x 网段），无 TCP 监听端口，与 127.0.0.1:4446 零冲突。装 Tailscale 后出现的 502 是巧合。
4. **与 relay-ai 无关**：codex-relay 直连 SiliconFlow（--upstream 参数），不经过 relay-ai(17645)。两条链路完全独立。
5. **launchd 两个服务互不拉扯**：com.codex-relay(4446) 与 com.relay-ai.server(17645) 端口/进程/日志/配置全分离。

### 踩坑总结 & 永久规避方案
- **不要手动跑 `codex-relay --port 4446`**！launchd 已 KeepAlive 托管，手动实例会和 launchd 抢端口，产生刷屏的 `Address already in use (os error 48)`（日志里曾积累 19 条）。
- 排查 codex-relay 状态：`tail -20 ~/.codex-relay.log`（正常）和 `tail -20 ~/.codex-relay-error.log`（错误）。
- 502 瞬时抖动无需处理，重试即可；若频繁出现长流中断，可先完全退出 Clash Verge 再验证。

### 关键命令 / 排障步骤
```bash
# 进程 & 端口
ps aux | grep codex-relay | grep -v grep
lsof -nP -i :4446
# 启动参数确认直连
ps aux | grep codex-relay | grep -v grep | tr ' ' '\n' | grep '^--'
# 上游连通性（401=通，没带 key）
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 15 https://api.siliconflow.cn/v1/models
# 最小请求穿透链路验证
curl -s -H "Content-Type: application/json" \
  -d '{"model":"deepseek-ai/DeepSeek-V4-Flash","input":"ping","max_output_tokens":1}' \
  http://127.0.0.1:4446/v1/responses
# launchd 服务状态
launchctl list | grep -iE "codex-relay|relay-ai"
```

### 关联
- [[relay-ai-部署记录]]
- [[跨Agent记忆持久化规则]]
- [[codex-relay踩坑]]

#codex-relay #故障 #launchd #排障