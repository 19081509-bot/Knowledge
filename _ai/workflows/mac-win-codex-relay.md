# Mac ↔ Windows Codex 中转工作流

## 启动顺序

1. Windows: 启动 Codex++（`codex-plus-plus-manager.exe`）
2. Windows: 确认 57321 端口监听（`netstat -ano | findstr 57321`）
3. Windows: 确保防火墙放行 + 端口转发（局域网访问）
4. Mac: 修改 `~/.codex/config.toml` 的 base_url 指向 Windows IP
5. Mac: 测试 `curl http://192.168.2.166:57321/v1/models`
6. Mac: 运行 `codex` 开始使用

## 关闭顺序

1. Mac: 将 config.toml 改回直连硅基（`https://api.siliconflow.cn/v1`）
2. Windows: 关闭 Codex++ 窗口
3. （可选）删除端口转发

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| Mac curl 不通 | Windows 防火墙拦截 | 执行放行命令 |
| 57321 无 LISTEN | Codex++ 未启动中转 | 点启动 |
| API 返回错误 | wire_api 不一致 | 两端统一为 chat |
| Mac 连接超时 | 不在同一局域网 | 检查 WiFi，关 VPN |
