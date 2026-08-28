---
date: 2026-08-24
tags: [AI对话, Codex++, 系统调试, Windows, 故障排查]
source: "Hermes 会话 2026-08-24"
---

# Codex++ 任务栏图标修复与 helper runtime 绑定报错排错

## 问题描述

1. **任务栏图标异常**：任务栏上 Codex++ 的固定项显示为「批处理文件」默认图标，不是正常应用图标。
2. **Helper 绑定报错**：启动时报 `failed to bind helper runtime on 127.0.0.1:57321`，且 `codex-plus-plus.exe` / `codex.exe` 的 PID 反复变化（进程被反复拉起/退出）。

## 解决方案

### 问题 1：任务栏图标空白 → 批处理默认图标

**根因**：任务栏固定项 `codex-plus-launcher.lnk` 的 IconLocation 字段为空（`Icon: ,0`），Windows 解析不到图标就回退成批处理文件样式。对比开始菜单里的 `Codex++.lnk` 是正常的（`codex-plus-plus.exe,0`）。

**修复**：用 WScript.Shell 重写 lnk 图标字段：

```powershell
$wshell = New-Object -ComObject WScript.Shell
$lnkPath = "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\codex-plus-launcher.lnk"
$exePath = "$env:LOCALAPPDATA\Programs\Codex++\codex-plus-plus.exe"
$lnk = $wshell.CreateShortcut($lnkPath)
$lnk.IconLocation = "$exePath,0"
$lnk.Save()
```

验证：重读 `IconLocation` 应显示完整路径（`...\codex-plus-plus.exe,0`）。若任务栏仍显示旧图标，需**取消固定 → 重新固定**（explorer 图标缓存），顽固时清 IconCache：

```powershell
Stop-Process -Name explorer -Force
Remove-Item "$env:LOCALAPPDATA\IconCache.db" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache_*.db" -Force -ErrorAction SilentlyContinue
Start-Process explorer
```

### 问题 2：helper runtime 绑定失败（127.0.0.1:57321）

**根因**：Codex++ 存在**双重 watcher 启动项**，登录时两个入口同时拉起 `codex-plus-plus.exe`，新旧实例竞争 helper 端口 57321，新实例绑定失败报错后退出，旧实例随后也让位，导致 PID 反复变化：

- 注册表 `HKCU\...\CurrentVersion\Run` → `CodexPlusPlusWatcher`（`--debug-port 9229`）
- 启动文件夹 `Startup\CodexPlusPlusWatcher.lnk`（同样参数）

**修复**：二选一删除一份重复 watcher（保留其一即可）：

```powershell
# 方案 A：删注册表那份（保留 Startup lnk）
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "CodexPlusPlusWatcher" -ErrorAction SilentlyContinue

# 方案 B：删 Startup lnk（保留注册表那份）
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\CodexPlusPlusWatcher.lnk" -Force
```

**诊断工具**：

- 查端口占用：`netstat -ano | grep 57321`（比对 LISTENING 的 PID 是否与当前进程一致）
- 查进程：`tasklist | grep -i codex`
- 查 watcher 启动项：`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"` + 查看 Startup 文件夹

**坑**：验证 lnk 图标不要用 ASCII grep 查二进制（`.lnk` 内字符串是 UTF-16 编码，grep 匹配不到会误判"未写入"），要用 PowerShell `CreateShortcut().IconLocation` 读取。

## 关键命令/配置

- Codex++ 安装目录：`%LOCALAPPDATA%\Programs\Codex++\`（`codex-plus-plus.exe`、`codex-plus-plus-manager.exe`、`codex-plus-plus.ico`、还有 `.exe.backup` / `.exe.backup2` 备份）
- 任务栏固定项目录：`%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\`
- Codex++ 由 taskbar 固定项启动 `codex-plus-plus.exe` → 拉起底层 `codex.exe`（增强工具链）
- 端口：helper runtime 57321（127.0.0.1）；watcher 调试端口 9229

## 相关笔记

- [[mac-win-codex-relay]]
- [[2026-07-26-最终架构-codex-relay+relay-ai分工]]
- [[_ai/MEMORY.md]]（内网穿透 Tailscale 网络节、端口表）