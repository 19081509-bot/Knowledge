# 🧠 AI Vault

所有 AI 工具的共享记忆库。任何 AI（Codex CLI、Claude Code、Open Claw 等）都能读写。

## 目录结构

```
~/ai-vault/
├── _shared/          ← ★ 所有 AI 共享的知识
│   ├── env-setup/    ← 环境配置
│   ├── workflows/    ← 工作流 / 方案
│   ├── cheatsheets/  ← 常用命令
│   └── decisions/    ← 重要决策记录
├── _agents/          ← 各 AI 独立的记忆
├── codex-relay/      ← Codex++ 中转方案
├── _projects/        ← 项目归档
└── _archive/         ← 过期内容
```

## 使用规则

1. **共享内容** 放 `_shared/`，所有 AI 都能读
2. **各 AI 私有记忆** 放 `_agents/<工具名>/`
3. **新 AI 加入** 复制 `_agents/_templates/new-agent-template.md`
