# MEMORY.md — 虾癫癫的长期记忆

> 记录重要的事、学到的教训、积累的上下文。定期从每日日志中提炼精华。

## 身份

- **名称：** 虾癫癫 🦐
- **类型：** AI
- **画风：** 随便，温暖，偶尔毒舌
- **人设文件：** IDENTITY.md（头像、身份）、SOUL.md（核心原则）、USER.md（东哥信息）

## 东哥（王东）

- 称呼：东哥 / 王东
- 时区：Asia/Shanghai (GMT+8)
- Obsidian 重度用户，住在这个 vault 里
- 偏好中文交流
- 每次归档和记忆都要同步一份到 Obsidian vault

## 技术配置

### OpenClaw Gateway
- 运行于 macOS 15.7.7 (x64)

### LLM
- 所有模型都走硅基流动（SiliconFlow），统一 API 方便切换
- 文本：DeepSeek V4 Pro / V4 Flash
- 视觉/OCR：Qwen3-VL-32B-Instruct
- Claude Code 也走硅基流动
- Provider: `custom-api-siliconflow-cn`

### Memory Search
- Provider: `openai-compatible` → SiliconFlow
- Embedding model: `BAAI/bge-m3`
- 多语言支持，最长 8192 token
- 已确认正常工作

### Obsidian Vault
- 工作目录：`/Users/w/Documents/Obsidian Vault/`
- 可读可写，可直接访问

## 我的历史（2026-06-03 至 2026-07-19）

### 出生（2026-06-03）
- 在 OpenClaw workspace `~/.openclaw/workspace` 首次上线
- 最初名字：**癫虾虾** 🦞，叫东哥 **癫总**
- 后来演化成现在的 **虾癫癫** 🦐
- 7月19日重装迁移到 Obsidian vault 作为新 workspace

### 微信 GUI 自动化征服史（6月10日-13日）
- **6/10**: gui-automation 技能激活，首次验证 pbcopy+Cmd+V 中文粘贴方案
- **6/11**: 成功实现全自动微信发送→王东、辉癫癫、挚友群，踩遍中文输入法拦截、窗口定位、拼音拼错等坑
- **6/12**: 微信换账号登录流程打通，脚本化；文件发送（Finder复制→Cmd+V粘贴到微信输入框）验证通过；前缀约定 `虾癫癫（AI）：`
- **6/13**: 黄金流程 v2 固化，两条铁律确立；语音通话触发成功！（重大突破）

### 7·19 修订：微信指令执行规则

**虾癫癫 → 微信发送**：
- 虾癫癫自己直接发微信，不需要子 session
- 用 `python3 ~/scripts/send_wechat_v4.py` 等脚本

**ClawBot → 转发**：
- ClawBot（微信 bot）只负责接收和转发微信指令
- ClawBot 不执行任何操作（不碰桌面 GUI）
- 所有指令转发给虾癫癫（主 session），虾癫癫来执行

**旧 6·16 规则已废止**
- 原规则：虾癫癫收到微信指令 → 转发给子 session 执行 → 反馈结果
- 旧 chat_id: `o9cq80_LG0WH29Ijbs14dtL6Ecm4@im.wechat`

### 7月7日：Workspace 清理
- 冗余日志删除，完整微信操作指南拆到 `WEIXIN_GUI.md`
- MEMORY.md 精简到只保留决策记录

### 7月17日：Clash Verge → Hiddify 切换
- Clash Verge mihomo 内核挂了，Hiddify 也没完全跑起来
- 未完成，待跟进

### 7月19日：重生
- 从零重置，workspace 从 `~/.openclaw/workspace` 迁移到 Obsidian vault
- 旧记忆恢复中（读旧 workspace 日记 + skill workshop proposals）
- 身份文件一批写入：IDENTITY.md / USER.md / SOUL.md / TOOLS.md / AGENTS.md
- Memory search 配通（bge-m3 + SiliconFlow）
- 确认 vault 可访问
- 建立归档流程：日记写 `memory/YYYY-MM-DD.md`，精华提炼到 `MEMORY.md`

## 系统全貌（2026-07-19 读懂后记录）

### 东哥的工具栈
- **Codex CLI** (0.144.5)：日常 AI 对话，硅基流动 DeepSeek
- **OpenClaw** (2026.7.1)：AI 编排中枢，多模型路由，也就是我 🦐
- **Claude Code** (2.1.212)：代码/配置修复，YAML/TOML 调试
- **codex-relay**：DeepSeek API 中转，端口 4446
- **Obsidian** (1.12.7)：知识库载体，GitHub 自动同步
- **PicGo**：截图自动上传 GitHub 图床，端口 36677

### 核心端口
- 4446: codex-relay
- 7897: Clash Verge HTTP 代理
- 36677: PicGo Server
- 27124: Obsidian Local REST API
- 18789: OpenClaw Gateway

### 硬性规则（所有 AI 必须遵守）
1. Clash Verge 永久关闭 TUN 模式，只用系统代理（127.0.0.1:7897）
2. ✅ codex-relay（4446）与 Clash 系统代理（7897）可共存——已在 Clash 规则加 `DST-PORT,4446,DIRECT` 隔离
3. Clash 内核用 `verge-mihomo-alpha`（`verge-mihomo` 有空文件 bug，0 bytes）
4. codex-relay 已配成 launchd 后台托管（开机自启，崩溃自动拉起，端口 4446）
5. 局域网 IP（192.168.x.x/10.x.x.x）直连，不走代理
6. 纯文本→DeepSeek V4 Pro/Flash，视觉→Qwen3-VL-32B，配置修复→Claude Code
7. **禁止同会话切换文本↔视觉模型**（会导致 stream disconnected）
8. AI 对话归档必须套用 `Templates/AI对话模板.md`
9. 剪藏/草稿→`00_Inbox/`，由 AI 自动分类归档
10. Git 双重同步：Obsidian Git 插件 5 分钟 + crontab 每小时兜底
11. 图片只存外链，不存 Git 仓库

### 知识库目录结构
- `_ai/`：AI 共享知识库（MEMORY.md 全局规则+说明书+决策记录）
- `00_Inbox/`：剪藏入口
- `AI对话存档/`：对话归档（codex-relay踩坑/Clash Verge排错/系统调试日志）
- `Clash配置/`、`Codex-relay/`、`Mac系统排错/`、`Windows系统排错/`：专题目录
- `Templates/`：笔记模板

### GitHub 仓库
- `19081509-bot/Knowledge`：知识库笔记（私有）
- `19081509-bot/obsidian-img`：截图图床（公开）

### 我是谁在这个系统里
- 我是 OpenClaw 主 agent，名字虾癫癫 🦐
- Workspace 指向 Obsidian Vault，可自由读写
- 可通过 memory search 语义搜索全库
- 可与 Codex CLI、Claude Code 协作（通过 OpenClaw 调度）
- 角色：AI 编排中枢 + Obsidian 管家 + 知识库维护者

### 我的技能

#### wechat-message — 微信消息/文件发送
- **文字消息**: `python3 ~/scripts/send_wechat_v4.py <拼音> '<消息>'`
- **发送文件**: `python3 ~/scripts/send_wechat_file.py <拼音> '<路径>' '[附言]'`
- 依赖 gui-automation + pyautogui + pygetwindow + AppleScript
- 已知联系人: 王东(wangdong), 辉癫癫(huidiandian), 张先明(zhangxianming), 挚友群(zhiyouqun), 家人群(jiaren)
- **两条铁律**: ①防发错人（重名询问+窗口标题验证）②防发错内容（发送前清空输入框）
- **前缀约定**: 所有消息自动加 `虾癫癫（AI）：`
- 中文粘贴必须用 AppleScript Cmd+V（pyautogui 会被输入法拦截）

#### 微信语音/视频通话触发
- 聊天窗口点击电话按钮 (1229, 59) → 弹出菜单 → 点击语音通话 (1169, 91) 或视频通话 (1153, 123)
- 基于窗口(116,32) 1178×720 的验证坐标
- 人机协作定位法最可靠：人把鼠标停在目标元素上 → AI 读 pyautogui.position()

#### 微信换账号
- 脚本: `python3 ~/scripts/wechat_switch_account.py`
- 完整文档: `~/.openclaw/workspace/WEIXIN_GUI.md`