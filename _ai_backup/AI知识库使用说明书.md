# 🤖 AI 知识库使用说明书

> 适用于：Codex CLI · OpenClaw · Claude Code · 任何能读写 Markdown 的 AI

---

## 一、系统架构

```
你（用户）
  ├── 💬 Codex CLI（当前对话） ←→ 硅基流动 API（DeepSeek）
  ├── 💬 OpenClaw ←→ 硅基流动 API（DeepSeek）+ Claude Code
  ├── 💬 Claude Code ←→ Anthropic API
  └── 📓 Obsidian Vault ← 所有 AI 共享的记忆库
         ├── _ai/            ← AI 共享知识
         ├── 00_Inbox/       ← 剪藏/草稿入口，AI 自动归档
         ├── Templates/      ← 笔记模板
         └── GitHub 自动同步 ← crontab 每小时推送
```

## 二、你的 AI 工具栈

| 工具 | 用途 | 模型 |
|------|------|------|
| **Codex CLI** | 日常对话、代码、本文编辑 | DeepSeek V4 Pro / V4 Flash |
| **OpenClaw** | AI 编排、多模型路由、Obsidian 集成 | DeepSeek V4 Pro + Qwen VL |
| **Claude Code** | 配置修复、yaml/toml 调试、代码审查 | Claude Opus / Sonnet |

## 三、Obsidian 知识库结构

```
/Users/w/Documents/知识库/
│
├── _ai/                          ← ★ AI 共享知识（所有 AI 自动读取）
│   ├── README.md                 ← 本仓库说明
│   ├── MEMORY.md                 ← ★ 全局约束记忆（所有 AI 必须遵守）
│   ├── AI知识库使用说明书.md      ← 本文档
│   ├── env-setup/                ← 环境配置方案
│   │   ├── clash-verge-config.md
│   │   ├── ssh-keys-setup.md
│   │   └── codex-relay-setup.md
│   ├── workflows/                ← 工作流方案
│   │   └── mac-win-codex-relay.md
│   └── decisions/                ← 技术决策记录
│       └── openclaw-obsidian-auto-report.md
│
├── 00_Inbox/                     ← ★ 剪藏入口，AI 从此处读取新内容
│                                    AI 自动分类归档到对应文件夹
│
├── Templates/                    ← 笔记模板
│   └── AI对话模板.md
│
├── _archive/                     ← 过期内容
│
├── 欢迎.md                       ← Obsidian 默认
├── .obsidian/                    ← Obsidian 配置（插件等）
└── .gitignore
```

## 四、全局规则（定义在 MEMORY.md，所有 AI 必须遵守）

### 网络规则
1. Clash Verge 永久关闭 TUN 模式，用系统代理（127.0.0.1:7897）
2. 运行 codex-relay 时必须退出 Clash Verge（端口冲突）
3. 局域网 IP（192.168.x.x/10.x.x.x）直连，不走代理

### 模型规则
1. 纯文本对话 → DeepSeek V4 Pro / V4 Flash
2. 视觉/截图/OCR → Qwen3-VL-32B-Instruct
3. 配置修复/yaml/toml 调试 → Claude Code
4. **禁止在同一次对话中切换文本↔视觉模型**（会导致 stream disconnected）
5. 切换模型方案：重启 relay / 新建对话

### 笔记规则
1. 所有 AI 对话存档必须套用 `Templates/AI对话模板.md`
2. 剪藏/草稿统一放入 `00_Inbox/`，由 AI 自动分类
3. 标签体系：#codex-relay #ClashVerge #OpenClaw #Mac #Windows #排错

### 同步规则
1. Git 自动同步由 crontab 每小时整点触发
2. 图片托管在 GitHub 图床（obsidian-img 仓库）

## 五、各 AI 如何读写知识库

### Codex CLI（我）
- ✅ **直接读取任何文件**：`cat /Users/w/Documents/知识库/_ai/MEMORY.md`
- ✅ **直接写入任何文件**：创建/修改 Markdown 文件
- ✅ **搜索内容**：`grep -r "关键词" /Users/w/Documents/知识库/`
- ⚠️ 每次新对话需要你提示，我会自动读取 `_ai/` 目录

### OpenClaw
- ✅ **已配置 workspace** 指向 Obsidian Vault
- ✅ **可通过对话命令写入**：`openclaw agent --agent main --message "写入笔记..." --deliver`
- ✅ **可运行记忆索引**：`openclaw memory index --force`（索引后能语义搜索全库）
- ⚠️ 需要手动触发写入/索引操作

### Claude Code
- ✅ **可直接读写文件**：`claude /Users/w/Documents/知识库/_ai/MEMORY.md`
- ✅ **可通过 OpenClaw 调用**（OpenClaw 配置了 Claude Code 作为代码专家）
- ⚠️ 需要显式指定文件路径

## 六、OpenClaw 集成指南

### 启动 OpenClaw Gateway
```bash
openclaw gateway restart
# Dashboard: http://192.168.2.67:18789/
```

### OpenClaw 常用命令
```bash
# 查看状态
openclaw status

# 查看模型列表
openclaw models status

# 运行一次对话（写入 Obsidian）
openclaw agent --agent main --message "你的指令" --deliver

# 索引 vault（让 OpenClaw 能搜索全库）
openclaw memory index --force

# 查看已安装插件
openclaw plugins list
```

### Obsidian Local REST API
- 地址：`https://127.0.0.1:27124/`
- 插件：obsidian-local-rest-api v4.1.7
- 用途：允许 OpenClaw 通过 API 读写 Obsidian

## 七、自动化机制

| 机制 | 触发方式 | 说明 |
|------|---------|------|
| Git 自动同步 | crontab `0 * * * *` | 每小时整点自动 commit + push 到 GitHub |
| OpenClaw 文件监听 | 需手动触发 | 通过 `openclaw agent` 指令驱动 |
| MEMORY.md 自动加载 | 每次 AI 读取 | 所有 AI 读取此文件了解规则 |
| 模板自动套用 | 手动调用 Templater | Obsidian 内 Ctrl+P → Templater: Insert Template |

## 八、快速上手

### 作为用户
1. 打开 Obsidian，浏览 `_ai/` 目录看已有知识
2. 有新对话/方案 → 告诉任意 AI "写到 Obsidian"
3. 需要查历史 → 告诉 AI "搜一下 Obsidian 里关于 xxx 的笔记"

### 作为 AI（读到本文档的 AI）
1. 首先读取 `_ai/MEMORY.md` 了解全局规则
2. 读取 `_ai/env-setup/` 了解环境配置
3. 读取 `Templates/AI对话模板.md` 了解笔记格式
4. 写入笔记时：套用模板 → 放 `00_Inbox/` → 打标签

---

*最后更新：2026-07-19*
*由 Codex CLI 生成，供所有 AI 工具共享使用*
