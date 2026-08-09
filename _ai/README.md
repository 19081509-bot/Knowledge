# 🧠 AI 共享知识库

所有 AI 工具（OpenClaw / Codex CLI / Codex++ / Claude Code / Claudian / Windows Codex）统一读写此 vault。

## 实际目录结构

```
知识库/                           ← Obsidian Vault 根目录
├── _ai/                         ← AI 共享知识库
│   ├── MEMORY.md                ← 全局规则与分工
│   ├── README.md                ← 本文件
│   ├── drilling/                ← 钻井专业知识
│   ├── env-setup/               ← 环境配置说明
│   ├── workflows/               ← 工作流方案
│   ├── decisions/               ← 重要决策记录
│   ├── scripts/                 ← 自动化脚本
│   │   ├── heartbeat-cleanup.py
│   │   └── heartbeat-cleanup.log
│   └── skills/                  ← AI 技能说明
├── 00_Inbox/                    ← 剪藏入口（AI 自动清洗归档）
├── AI对话存档/                   ← 已归档对话
│   ├── codex-relay踩坑/
│   ├── Clash Verge配置排错/
│   ├── 系统调试日志/
│   └── 通用技术记录/
├── memory/                      ← 每日日记
├── Templates/                   ← 笔记模板
├── Clash配置/                    ← Clash 配置专题
├── Codex-relay/                 ← Codex 专题
├── Mac系统排错/
├── Windows系统排错/
├── AGENTS.md                    ← 各 AI 行为规范
├── IDENTITY.md                  ← 虾癫癫身份
├── USER.md                      ← 东哥信息
├── SOUL.md                      ← 虾癫癫灵魂
├── TOOLS.md                     ← 环境笔记
├── MEMORY.md                    ← 虾癫癫长期记忆
└── HEARTBEAT.md                 ← 巡检任务清单
```

## 使用规则

1. **新会话启动**：先读 `_ai/MEMORY.md`（全局规则）→ `_ai/README.md`（本文件）→ `MEMORY.md`（长期记忆）→ `AGENTS.md` / `IDENTITY.md` / `USER.md` / `SOUL.md`
2. **边走边记**：技术方案、配置、故障排查中途立即写入 `00_Inbox/`，不等对话结束
3. **虾癫癫 heartbeat（每 4h）**：扫描 `00_Inbox/` → 清洗 → 分类归档 → 提炼到 `MEMORY.md` → Git 提交推送
4. **专业知识（钻井/定向/工具/泥浆）** → 整理到 `_ai/drilling/`
5. **百科通识 / 豆包剪藏** → 归档到 `AI对话存档/通用技术记录/`

## AI 工具一览

| AI | 平台 | 连接 | 主要职责 |
|----|------|------|---------|
| 🦐 OpenClaw (虾癫癫) | Mac | 18789 | 编排中枢 + 管家 |
| 💻 Codex CLI | Mac | codex-relay:4446 | 专业知识（钻井/定向） |
| 🔧 Codex++ | Mac | 57321 | 专业知识辅助 |
| 🛠️ Claude Code | Mac | relay-ai:17645 | 配置修复 |
| 📝 Claudian | Mac (Obsidian内) | relay-ai:17645 | Obsidian 内嵌助手 |
| 🪟 Windows Codex | Windows | 本机 Codex++ | 专业知识跨平台补充 |
| 🫘 豆包 | Web | Web Clipper剪藏 | 百科知识入口 |