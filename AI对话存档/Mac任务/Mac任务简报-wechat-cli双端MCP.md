# Mac 任务简报 · 安装 wechat-cli 并接入 Claude Code + Codex 双端 MCP

> 派发: Windows Hermes(总调度) → Mac Claude Code(参谋长/执行)
> 日期: 2026-08-28
> 目标: 在 Intel Mac 上装 r266-tech/wechat-cli,注册为 Claude Code 与 Codex 的 MCP server,使 agent 能直接查询微信聊天记录。后期换 M 芯片 Mac,此配置随用户目录迁移无缝。

## 环境事实(已侦察)
- Mac = Intel, hostname hymacbook-pro, 用户 w
- Clash Verge 仅监听 **7897**(混合端口)。**直连 GitHub 不通(HTTP 000)**,必须走代理:
  `export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897 ALL_PROXY=socks5://127.0.0.1:7897`
- Go **未装**(brew 装过但 PATH 未刷新,需 `export PATH=$PATH:/usr/local/go/bin` 或 `eval $(brew shellenv)`)
- Python 3.14.5 已有;brew 6.0.12 已有
- 微信**已登录运行**(进程在)
- Claude Code v2.1.250, Codex v0.149.1,均 `/usr/local/bin`
- Claude 现有 MCP: sot(连超时,无关);Codex 现有: computer-use(关)、node_repl、brave_search(开)、sot

## 执行步骤(逐步,每步验证)

### 1. 设代理 + 装 Go
```
source ~/.zshrc 2>/dev/null; eval $(brew shellenv)
export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897 ALL_PROXY=socks5://127.0.0.1:7897
brew install go
export PATH=$PATH:$(go env GOPATH)/bin:/usr/local/go/bin
go version   # 确认可用
```

### 2. 获取 wechat-cli 二进制(优先预编译,其次 go install)
```
REL=$(curl -sL -m 20 "https://api.github.com/repos/r266-tech/wechat-cli/releases?per_page=1" | python3 -c "import sys,json;print(json.load(sys.stdin)[0]['tag_name'])")
ASSET=$(curl -sL -m 20 "https://api.github.com/repos/r266-tech/wechat-cli/releases/tags/$REL" | python3 -c "import sys,json;[print(a['browser_download_url']) for a in json.load(sys.stdin)['assets'] if 'darwin' in a['name'].lower() and ('amd64' in a['name'].lower() or 'x86_64' in a['name'].lower())]" | head -1)
mkdir -p ~/bin
if [ -n "$ASSET" ]; then curl -sL -m 180 -o ~/bin/wechat-cli "$ASSET" && chmod +x ~/bin/wechat-cli
else go install github.com/r266-tech/wechat-cli@latest; fi
~/bin/wechat-cli --help   # 记录真实 MCP 子命令名(如 mcp / serve / mcp-serve)
```

### 3. 提取微信 key(微信须登录运行)
- 查 wechat-cli 的 key 提取子命令(一般 `wechat-cli key` 或 `extract-key`),按 --help 输出执行
- 输出 key 文件路径记下(如 ~/wechat-key.txt 或项目目录)

### 4. 注册 MCP 到双端
- **Claude Code**:
  `claude mcp add wechat --scope user -- ~/bin/wechat-cli <MCP子命令>`
  (若需 env 传 key 路径,用 `-e WECHAT_KEY_FILE=...`)
- **Codex**:
  在 `~/.codex/config.toml` 加:
  ```
  [mcp_servers.wechat]
  command = "/Users/w/bin/wechat-cli"
  args = ["<MCP子命令>"]
  transport = "stdio"
  enabled = true
  ```

### 5. 重启 + 验证
- 重启 Claude Code / Codex 使 MCP 加载
- 验证:`claude mcp list` 显示 wechat 已连接;`wechat_search_messages` 或对应工具能返回你的聊天
- 写入验证结果到 `知识库/00-inbox/wechat-cli安装验证.md`

## 安全底线(严格遵守)
- 仅处理**本人**微信数据,不碰他人隐私、不批量爬群友
- 不修改任何微信消息
- key 文件仅本地,不传入任何远程/agent 上下文以外的地方
- 装包全部走本地代理,不对外上传聊天内容

## 完成标准
`claude mcp list` 与 `codex mcp list` 均显示 wechat 已连接且可查询;验证文件已写。完成后在 `00-inbox/` 留一句话结果即可。
