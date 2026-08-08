---
date: 2026-08-09
tags: [AI对话, 待分类]
---

# Windows Codex Desktop 配置流程

> 最后更新: 2026-07-31

## 基本信息

| 项目 | 值 |
|:----|:----|
| 主机 | Wd (192.168.2.38) |
| 用户 | Administrator |
| 安装方式 | 微软商店 AppX (OpenAI.Codex) |
| 版本 | 26.721.11231.0 |
| 主程序 | `C:\Program Files\WindowsApps\OpenAI.Codex_26.721.11231.0_x64__2p2nqsd0c76g0\app\ChatGPT.exe` |
| 配置文件 | `C:\Users\Administrator\.codex\config.toml` |
| SSH 连接 | `ssh administrator@192.168.2.38` |

## API 后端架构

```
Codex Desktop (ChatGPT.exe)
    ↓ config.toml → base_url = "http://127.0.0.1:57321/v1"
    ↓
codex-plus-plus.exe  (:57321)
    ↓ 代理转发
硅基流动 API (api.siliconflow.cn)
    ↓
DeepSeek-V4-Flash / V4-Pro
```

| 组件 | 端口 | 路径 |
|:----|:----:|:-----|
| codex-plus-plus.exe | **57321** | `C:\Users\Administrator\AppData\Local\Programs\Codex++\codex-plus-plus.exe` |
| codex-plus-plus-manager.exe | 动态 | 同目录 |

## 502 Bad Gateway 解决方案

**症状：** Codex Desktop 报 `502 Bad Gateway: http://127.0.0.1:57321/v1/responses`

**原因：** codex-plus-plus.exe 进程异常或未运行（manager.exe 不会自动拉起它）

**最快修复：** 关闭当前 Codex 对话 → 新建对话 → 正常。如果不行：

```powershell
# 管理员 PowerShell
# 1. 检查进程
Get-Process codex-plus-plus -ErrorAction SilentlyContinue

# 2. 如果不在运行，手动启动
Start-Process "C:\Users\Administrator\AppData\Local\Programs\Codex++\codex-plus-plus.exe" -WindowStyle Hidden

# 3. 确认监听
netstat -ano | Select-String :57321

# 4. 验证 API 响应（看能不能拉到模型列表）
Invoke-WebRequest -Uri https://api.siliconflow.cn/v1/models -Method GET `
  -Headers @{Authorization="Bearer 你的KEY"} -UseBasicParsing
```

## 任务栏图标修复

**现象：** 图标显示为文本文档

```powershell
# 管理员 PowerShell
Stop-Process -Name explorer -Force

Remove-Item "$env:LOCALAPPDATA\IconCache.db" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache_*.db" -Force -ErrorAction SilentlyContinue

Get-AppxPackage *codex* | Add-AppxPackage -RegisterDisposition None -ForceApplicationShutdown

Start-Process explorer
```

如果还不行：任务栏取消固定 → 重新固定。

## 开机自启

已部署计划任务 `CodexppServer`，登录时自动启动 codex-plus-plus：

```powershell
schtasks /CREATE /SC ONLOGON /TN CodexppServer /TR "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Users\Administrator\start-codexpp.ps1" /RL HIGHEST /F
```

自动启动脚本 `C:\Users\Administrator\start-codexpp.ps1`：
```powershell
$pp = "C:\Users\Administrator\AppData\Local\Programs\Codex++\codex-plus-plus.exe"
if (-not (Get-Process codex-plus-plus -ErrorAction SilentlyContinue)) {
    Start-Process $pp -WindowStyle Hidden
}
```

## Git 同步（知识库写到 GitHub）

```powershell
# 配置代理（Windows 需要 Clash Verge 才能出国）
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

# 克隆知识库（已完成）
git clone https://19081509-bot:TOKEN@github.com/19081509-bot/Knowledge.git C:\Users\Administrator\知识库\

# 日常同步
cd C:\Users\Administrator\知识库\
git add -A
git commit -m "auto sync"
git pull --rebase
git push
```

## 跨 Agent 规则

Windows Codex 的 AGENTS.md：`C:\Users\Administrator\.codex\AGENTS.md`

### 启动时必读（按顺序）
1. `C:\Users\Administrator\知识库根文件\AGENTS.md` — 规则指南
2. `C:\Users\Administrator\知识库根文件\IDENTITY.md` — 身份
3. `C:\Users\Administrator\知识库根文件\USER.md` — 用户信息
4. `C:\Users\Administrator\知识库根文件\SOUL.md` — 核心原则
5. `C:\Users\Administrator\知识库根文件\MEMORY.md` — 长期记忆
6. `C:\Users\Administrator\_ai\MEMORY.md` — 全局规则（必读）
7. `C:\Users\Administrator\_ai\README.md` — 知识库结构

### 写入规则
- 有价值的技术方案/配置/决策 → 立即写 `C:\Users\Administrator\知识库\00_Inbox\`
- 一般问答 → **不记**
- 写完后 `git push`

### 跨 Agent 协作
| Agent | 角色 | 连接 |
|:------|:-----|:-----|
| 🦐 虾癫癫 (Mac Codex) | 主力生产力 | codex-relay :4446 |
| Claude Code (Mac) | 代码开发 | relay-ai :17645 |
| 🐉 OpenClaw (Mac) | 巡检/心跳/清洗 | :18789 |
| 🪟 Windows Codex | 辅助生产力 | :57321 → 硅基流动 |

## 关联文件
- [[../../_ai/MEMORY.md]]
- [[../../_ai/README.md]]
- [[../../AGENTS.md]]