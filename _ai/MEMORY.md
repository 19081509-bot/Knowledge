# 🧠 全局工具约束记忆

> 所有 AI 自动读取此文件。修改此处 = 修改所有 AI 的行为规则。

## 运行环境

- **设备**: Mac (192.168.2.67) + Windows (192.168.2.166)
- **AI 工具栈**: OpenClaw + Codex CLI + Claude Code
- **API 供应商**: 硅基流动（DeepSeek 文本/视觉、Qwen VL）
- **知识库**: Obsidian `~/ai-vault/`，GitHub 私有仓库同步

## 硬性规则

### 网络
1. Clash Verge 永久关闭 TUN 模式，用系统代理模式（127.0.0.1:7897）
2. 运行 codex-relay 时需退出 Clash Verge（端口栈冲突）
3. 局域网直连（192.168.x.x/10.x.x.x），不走代理

### 模型
1. 纯文本对话 → DeepSeek V4 Pro / V4 Flash
2. 视觉/截图/OCR → Qwen3-VL-32B-Instruct
3. 配置修复/yaml/toml 调试 → Claude Code
4. 禁止在同一次对话中切换文本↔视觉模型（会导致 stream disconnected）
5. 切换模型方案：重启 relay / 新建对话

### 知识库
1. 笔记模板统一用 `Templates/AI对话模板.md`
2. 剪藏草稿先放 `00_Inbox/`，由 AI 自动分类
3. 标签体系：#codex-relay #ClashVerge #OpenClaw #Mac #Windows #排错

### 同步
1. Git 自动同步由 crontab 触发
2. 图片统一托管在 GitHub 图床（obsidian-img 仓库）
