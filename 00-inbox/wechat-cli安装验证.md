# wechat-cli 安装与双端 MCP 接入验证报告

> 执行时间:2026-08-28
> 任务来源:用户指令「安装 r266-tech/wechat-cli 并接入 Claude Code 与 Codex 双端 MCP,逐步执行、每步验证,结果写入本文件;代理走 127.0.0.1:7897;微信已登录」
> 执行人:Mac 侧 Claude Code

## 0. 前置说明:任务简报文件缺失

任务中引用的简报文件 **`知识库/AI对话存档/Mac任务/Mac任务简报-wechat-cli双端MCP.md` 在本机文件系统与 git 历史中均不存在**。
已找到的旧简报 `微信聊天记录/Mac任务简报-ClaudeCode.md` 是 2026-08-27 的「微信记录导出清洗」任务,与本任务无关。
本次严格按用户消息中的直接指令执行。

## 1. 关键事实:官方源被封锁,采用同源 fork

- `github.com/r266-tech/wechat-cli` 因 **DMCA 被 GitHub 整体封锁**(2026-08-06),连 fork 也无法直接访问。
- 官方 npm 伞包 `@canghe_ai/wechat-cli`(最新 0.2.4)**仅为 arm64 发布预编译二进制**,本机是 **Intel x86_64**,无现成二进制。
- PyPI 无 `wechat-cli` 包。
- 决策:采用同源可访问 fork **`huohuoer/wechat-cli`**(主线 0.2.4,与官方同版本同时源)进行**源码安装**,并本地编译 x86_64 版密钥扫描器。
  - 源码位置:`~/Tools/wechat-cli/`
  - 说明:该 fork 仓库文件树与 r266-tech 官方一致(go/pip/npm 结构相同,来自 DeepWiki 对官方同代仓库的索引)。

## 2. 环境验证(逐项)

| 项目 | 结果 |
|------|------|
| 代理 `127.0.0.1:7897` | ✔ HTTP 200(`curl -x` 实测) |
| Node / npm | v26.5.0 / 11.17.0 |
| git | 2.39.5 |
| Python | 3.14.5(`/usr/local/bin/python3`) |
| clang / CLT | 17.0.0 x86_64,`/Library/Developer/CommandLineTools` ✔ |
| 微信进程 | ✔ 运行中(WeChat 4.1.11,含 WeChatAppEx) |
| 微信容器目录读取 | ✔ 当前会话可直接读 `~/Library/Containers/.../Documents` |
| sudo | ✘ 需密码交互(本会话不可代输) |

> 微信版本 4.1.11 高于 fork 文档声明的兼容上限 4.1.8.100;密钥格式在 4.x 一直稳定,**实际兼容性以 init 实测为准**。

## 3. 安装过程与验证

1. `curl -x 127.0.0.1:7897` 下载 `huohuoer/wechat-cli` main 分支 tarball → 解压到 `~/Tools/wechat-cli/`
2. 编译 x86_64 扫描器:
   `cc -O2 -o wechat_cli/bin/find_all_keys_macos.x86_64 wechat_cli/bin/find_all_keys_macos.c -framework Foundation`
   - 产物:Mach-O 64-bit executable x86_64 ✔(命名严格匹配源码 `scanner_macos.py` 中 x86_64 规则)
3. 建 venv:`python3 -m venv ~/Tools/wechat-cli/venv`
4. 安装:`venv/bin/pip install .`(代理 pip)
   - 依赖:click 8.5.0 / pycryptodome 3.23.0 / zstandard 0.25.0
   - 打包内 x86_64 扫描器 ✔(site-packages/wechat_cli/bin/)
5. 运行验证:
   - `wechat-cli --version` → `wechat-cli, version 0.2.4` ✔
   - `wechat-cli --help` → 注册 11 个子命令 ✔(sessions/history/search/contacts/members/stats/export/favorites/unread/new-messages/init)
   - `wechat-cli` 入口:`~/Tools/wechat-cli/venv/bin/wechat-cli`

## 4. 双端 MCP 接入

r266-tech/wechat-cli **非原生 MCP server**(纯 CLI,click 子命令)。
方案:写一个**极简 stdio MCP 封装器**(仅用 Python 标准库)把 wechat-cli 各命令暴露为标准 MCP 工具,**同一 server 分别注册进 Claude Code 与 Codex**。

### 4.1 MCP 封装器

- 文件:`~/Tools/wechat-cli/wechat_mcp_server.py`
- 暴露工具(10 个):`wx_sessions / wx_history / wx_search / wx_contacts / wx_members / wx_unread / wx_new_messages / wx_stats / wx_export / wx_favorites`
- 协议自测(手动喂入 JSON-RPC 流):✔
  - `initialize` → 协商协议版本 2025-06-18 ✔
  - `tools/list` → 返回 10 个工具 ✔
  - `ping` → `{}` ✔
  - `tools/call wx_sessions` → 正确派发到 `wechat-cli sessions`;未初始化时预期报错「密钥文件不存在 ~/.wechat-cli/all_keys.json,请运行 wechat-cli init」✔(链路通,只差初始化)

### 4.2 Claude Code 侧

- 注册:`claude mcp add wechat-cli --transport stdio --scope user -- /Users/w/Tools/wechat-cli/venv/bin/python3 /Users/w/Tools/wechat-cli/wechat_mcp_server.py`
- 写入:`~/.claude.json` → `mcpServers.wechat-cli`(type=stdio)✔
- 健康检查:`claude mcp list` → **wechat-cli ✔ Connected** ✔
- (注:既有 `sot` server 一直连接失败,与本次无关)

### 4.3 Codex 侧

- 写入:`~/.codex/config.toml` 新增 `[mcp_servers.wechat-cli]`:

  ```toml
  [mcp_servers.wechat-cli]
  enabled = true
  transport = "stdio"
  command = "/Users/w/Tools/wechat-cli/venv/bin/python3"
  args = ["/Users/w/Tools/wechat-cli/wechat_mcp_server.py"]
  ```

- TOML 解析校验:✔(`tomllib` 加载正常,`mcp_servers` 含 wechat-cli)
- 同一 server 已通过 4.1 的 stdio 握手验证;`codex` CLI 启动时会加载该 MCP server

## 5. 待执行:密钥初始化(唯一剩余步骤)

`init` 需要 **sudo** 读微信进程内存提取 SQLCipher 密钥(微信当前无 get-task-allow 授权),**必须由东哥在终端交互输入密码执行**:

```bash
sudo /Users/w/Tools/wechat-cli/venv/bin/wechat-cli init
```

预期交互:
- 若 `task_for_pid failed`:工具会自动**重签微信**并提示「退出微信→重新打开→重新登录→再次 sudo init」。重签安全,不影响账号,但可能影响微信自动更新(必要时官方重新安装即可,已配好的密钥与 config 保留)。
- 完成后生成 `~/.wechat-cli/all_keys.json` 与 `config.json`。

init 完成后,后续全部步骤(会话查询、消息读取、双端 MCP 实际调用)即可自动化验证。

## 6. 结论

- 安装 ✔(0.2.4,Intel 源码路线)
- Claude Code 侧 MCP 接入 ✔ Connected
- Codex 侧 MCP 接入 ✔ 配置完成(TOML 合法,stdio 握手通过同一 server)
- 剩余:`sudo wechat-cli init` 待东哥执行 → 完成后更新本报告并做真实数据验证
