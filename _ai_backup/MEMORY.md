# 🧠 全局工具约束记忆

> 所有 AI 自动读取此文件。修改此处 = 修改所有 AI 的行为规则。
> 最后更新: 2026-07-19（心跳 4h + Web Clipper 配置已写入）

## 运行环境

- **设备**: Mac (192.168.2.67) + Windows (192.168.2.166)
- **AI 工具栈**: Codex CLI + OpenClaw + Claude Code
- **Obsidian 侧边 AI**: Claudian（非 OpenClaw）
- **API 供应商**: 硅基流动（DeepSeek 文本）
- **知识库**: Obsidian `/Users/w/Documents/知识库/`，GitHub `19081509-bot/Knowledge`

## 硬性运行规范

### 网络
1. Clash Verge **永久关闭 TUN 模式**，用系统代理（127.0.0.1:7897）
2. 运行 codex-relay 时必须完全退出 Clash Verge
3. 局域网 IP（192.168.x.x/10.x.x.x）直连，不走代理

### 端口
| 端口 | 服务 | 说明 |
|------|------|------|
| 4446 | codex-relay | DeepSeek 中转 |
| 7897 | Clash Verge | HTTP 代理 |
| 36677 | PicGo | 图床上传 |
| 27124 | Obsidian REST API | HTTPS |
| 18789 | OpenClaw Gateway | WebSocket |

### 模型（当前仅纯文本，视觉已禁用）
1. 纯文本对话 → DeepSeek V4 Pro / V4 Flash
2. ❌ **视觉/OCR/截图已禁用**（余额不足）
3. 配置修复/YAML/TOML → Claude Code
4. **禁止在同一次对话中切换文本↔视觉模型**

### 会话清洗规则（归档对话时执行）

#### 1. 冗余过滤
- 删除所有重复提问、重复报错、重复日志
- 剔除流式断开提示、余额不足报错、工具加载等待文本
- 去除网页剪藏自带广告、登录弹窗、无关文字
- 精简重复铺垫上下文，只保留核心提问和可执行方案

#### 2. 分层排版（固定顺序）
```
## 用户原始提问
## AI标准化解决方案（提取可复制命令/配置）
## 故障踩坑总结 & 永久规避方案
## 关联工具双链 [[工具名]]
```

#### 3. 自动标签
- codex-relay 故障 → `#codex-relay [[故障]]`
- Clash 代理配置 → `#ClashVerge [[代理排错]]`
- OpenClaw 报错 → `#OpenClaw [[自动化故障]]`
- PicGo 图床 → `#PicGo [[图床]]`
- Mac 调试 → `#Mac`

#### 4. 分类目录
- codex-relay 对话 → `AI对话存档/codex-relay踩坑/`
- Clash 配置 → `AI对话存档/Clash Verge配置排错/`
- OpenClaw/系统调试 → `AI对话存档/系统调试日志/`
- 通用技术 → `AI对话存档/通用技术记录/`

### 笔记归档规则
1. 所有 AI 对话必须套用 `Templates/AI对话模板.md`
2. 剪藏草稿先放 `00_Inbox/`，由 AI 清洗后归档
3. 少于 3 轮无技术价值的对话不归档

### 同步规则
1. Obsidian Git 插件每 5 分钟自动提交推送
2. crontab 每小时整点兜底执行 `/Users/w/obsidian-git-sync.sh`
3. 截图不存入知识库仓库（通过 PicGo 传 GitHub 图床）

### OpenClaw 心跳 & 压缩配置（2026-07-19 更新）

#### 心跳（heartbeat）
| 参数 | 值 | 说明 |
|------|-----|------|
| `every` | `240m` | 4 小时触发一次，闲置日仅 6 次心跳 |
| `lightContext` | `true` | 极简上下文，不加载完整 MEMORY/会话历史 |
| `isolatedSession` | `true` | 独立隔离会话，不污染主对话上下文 |
| `skipWhenBusy` | `true` | 繁忙时自动跳过，避免抢 Token |

#### 压缩（compaction）
| 参数 | 值 | 说明 |
|------|-----|------|
| `reserveTokensFloor` | `35000` | 预留 3.5 万 Token 缓冲，防止压缩失败 |
| `recentTurnsPreserve` | `5` | 保留最近 5 轮对话原文 |
| `mode` | `default` | 基线模式，不额外消耗 |
| `maxHistoryShare` | `0.6` | 保留历史上限 60%，留足生成空间 |

#### 效果
- 🟢 完全闲置时心跳 Token 消耗降低 **~83%**（对比默认 30 分钟）
- 🟢 会话接近 Token 上限才触发压缩，不闲置巡检
- 🟢 配置已生效，网关无需重启

### Obsidian Web Clipper 配置（2026-07-19）

| 配置项 | 值 |
|--------|------|
| 插件版本 | v1.7 |
| 目标库（Vault） | `Obsidian Vault` |
| 笔记位置 | `00_Inbox/` |
| 触发器 | Google 域名（豆包剪藏） |
| 自动打开 | ❌ 关闭 |

#### 剪藏流程
1. 在豆包对话页面 → 点击 Web Clipper 图标
2. 文件自动存入 `/Users/w/Documents/知识库/00_Inbox/`
3. OpenClaw 文件监听自动触发清洗归档
4. 清洗后移至 `AI对话存档/` 对应分类目录
5. Git 自动提交推送

#### 注意事项
- 库名是 `Obsidian Vault`（不是 TechVault）
- 默认文件夹在 Web Clipper 设置中通过「笔记位置」固定为 `00_Inbox`
- 不要使用插件默认的 `Clippings/` 文件夹
- 已删除 Clippings 目录，剪藏直接进 00_Inbox



---

## 实际运行端口映射（2026-07-25 核实）

| 服务 | 端口 | PID | 运行位置 | 上游 |
|------|------|-----|---------|------|
| **codex-relay** | 4446 | 612 | Mac 本机 | SiliconFlow |
| **relay-ai** | 17645 | 629 | Mac 本机 | SiliconFlow（91 模型） |
| **Codex++** | 57321 | 982 | Mac 本机 | SiliconFlow |
| **Codex++ 管理工具** | — | 957 | Mac 本机 | 管理界面 |

### AI 工具连接映射

| AI 工具 | 连接目标 | 协议 |
|---------|---------|------|
| **虾癫癫（Codex CLI / Desktop）** | codex-relay  |  |
| **Claude Code** | relay-ai  | Anthropic Messages |
| **Claudian（Obsidian）** | relay-ai  | OpenAI Chat |
| **Windows Codex Desktop（备用）** | 本机 Codex++ （或局域网） | OpenAI Chat |
---

## 🧠 跨 Agent 记忆持久化规则（2026-07-25 确立）

### 核心原则
所有 AI agent（虾癫癫·Codex CLI / OpenClaw / Claude Code / Windows Codex）统一遵守：

### 规则 1：每次新任务先读知识库
新会话启动后，先读取以下文件获取上下文：
- `_ai/MEMORY.md` — 全局规则
- `_ai/README.md` — 知识库说明
- `MEMORY.md` — 长期记忆
- `AGENTS.md` / `IDENTITY.md` / `USER.md` / `SOUL.md` — 身份和行为规范

### 规则 2：对话中边走边记，不等结束
当对话产生以下内容时，立即写入 `00_Inbox/`，不要等线程关闭：
- ✅ 技术方案 / 配置 / 命令
- ✅ 故障排查记录和根因
- ✅ 决策和理由
- ✅ 任何以后可能用得上的东西
- ❌ 一般性问答 / 闲聊不记

### 规则 3：写入格式
```
## 日期 / 话题
### 结论
### 关键命令 / 配置
### 关联
```

### 规则 4：OpenClaw heartbeat（每 4h）负责收尾
- 扫描 `00_Inbox/` → 清洗 → 分类归档
- 更新 `MEMORY.md` 提炼精华
- Git 自动提交推送

### 实现前提
- Codex CLI 线程之间不共享上下文，必须主动写文件来持久化
- OpenClaw 无法"调用" Codex CLI 线程，但可以执行 shell 命令和 Claude Code
- Windows Codex Desktop 可通过网络共享或 SSH 写入知识库

> **Heartbeat 自动归档 (2026-07-26 10:12)**：处理了 8 个文件
> - 2026-07-25-跨Agent记忆持久化规则确立.md
> - test-note.md
> - 豆包 1.md
> - 豆包 2.md
> - 豆包 3.md
> - 豆包 4.md
> - 豆包 5.md
> - 豆包.md

---

## 自动清洗流程（2026-07-26 投入使用）

### 触发方式
- OpenClaw Heartbeat 每 4 小时触发 → 读取 HEARTBEAT.md → 执行 `heartbeat-cleanup.py`

### 脚本位置
- `_ai/scripts/heartbeat-cleanup.py` — 扫描 `00_Inbox/` → 清洗 → 分类归档
- `_ai/scripts/heartbeat-cleanup.log` — 运行日志

### 分类规则
| 关键词 | 归档目录 |
|--------|---------|
| codex-relay / codex_relay / Codex++ | AI对话存档/codex-relay踩坑/ |
| Clash / clash / mihomo / 代理 / Verge | AI对话存档/Clash Verge配置排错/ |
| OpenClaw / openclaw / Gateway | AI对话存档/系统调试日志/ |
| 跨Agent / 记忆持久化 / 全局规则 | AI对话存档/系统调试日志/ |
| 豆包 / doubao（默认） | AI对话存档/通用技术记录/ |

### Git 同步
- 已配置 git 全局代理: `http://127.0.0.1:7897`（走 Clash Verge）
- 脚本自动 add → commit → pull --rebase → push

> **Heartbeat 自动归档 (2026-07-26 14:32)**：处理了 2 个文件
> - 2026-07-26-Windows Codex++ 端口占用解决.md
> - 2026-07-26-最终架构-codex-relay+relay-ai分工.md
