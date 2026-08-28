# Mac AI 架构与链路(2026-08 实测)

> 记录 Mac 上各 AI 工具的模型链路、中转指向、共用配置,供所有 agent(Mac 端 Claude Code / Codex / 未来 Hermes)自查。
> 写这份文档的原因:排查"codex-cli 走哪个中转"时发现 CLI 与桌面版共用配置、且顶层 model 缺失会落回 OpenAI 默认模型导致 20012。

## 一、链路全景(实测确认)

```
┌─ Codex(CLI + 桌面版共用)────────────────────────────┐
│  ~/.codex/config.toml                                │
│  model_provider = "custom"                           │
│  model = "deepseek-ai/DeepSeek-V4-Flash"  (顶层!)    │
│  base_url = http://127.0.0.1:4446/v1                 │
└──────────────┬───────────────────────────────────────┘
               ▼
        codex-relay (本机 :4446)
        --upstream https://api.siliconflow.cn/v1
               ▼
        硅基流动 SiliconFlow API
               ▼
        DeepSeek-V4-Flash
```

```
┌─ Claude Code ────────────────────────────────────────┐
│  ~/.claude/settings.json 自带 env(零配置,SSH 免配)    │
│  ANTHROPIC_BASE_URL = http://127.0.0.1:17645/anthropic │
└──────────────┬───────────────────────────────────────┘
               ▼
        relay-ai (本机 :17645)
               ▼
        硅基流动 SiliconFlow API(同一上游)
               ▼
        DeepSeek-V4-Flash
```

**共同点**:两个中转(codex-relay 4446 / relay-ai 17645)是**独立进程,但上游都是硅基流动,最终模型都是 DeepSeek-V4-Flash**。

## 二、关键事实(2026-08-25 实测)

| 项 | 结论 | 证据 |
|---|---|---|
| Codex CLI 与桌面版是否共用配置 | **共用 `~/.codex/config.toml`**(还有 `~/.codex/auth.json` 存登录凭证) | Codex CLI 本人确认:桌面版(ChatGPT.app / Codex.app 内置)的 app.asar 直接引用 `.codex/config.toml` |
| Codex 走哪个中转 | 本地 `codex-relay`,127.0.0.1:4446 | `grep base_url ~/.codex/config.toml` |
| codex-relay 上游 | `https://api.siliconflow.cn/v1`(硅基流动,实测 200) | `ps` 命令行 `--upstream https://api.siliconflow.cn/v1` |
| Claude Code 走哪个中转 | 本地 `relay-ai`,127.0.0.1:17645 | `~/.claude/settings.json` env |
| 模型 | DeepSeek-V4-Flash(全部走硅基流动) | config.toml + relay 命令行 |

## 三、坑(persistent lessons)

1. **顶层 model 必须写**(在第一个 `[` 段头之前):
   - 正确: `model_provider = "custom"` + `model = "deepseek-ai/DeepSeek-V4-Flash"` 都在文件顶部
   - 缺失时的症状:Codex 落回内置默认 OpenAI 模型(`gpt-5.6-sol`),relay 不认识 → `20012 Model does not exist` → 5 次重连失败
   - 陷阱:provider 块内 `[model_providers.custom]` 里**也有**一个 `model =`,但它只是该 provider 的默认值,**不是**顶层选择;grep `^model` 会误判(块内行也匹配),必须按"第一个 `[` 之前"判断
   - 修法(已执行):顶层 `model_provider` 行下补 `model = "deepseek-ai/DeepSeek-V4-Flash"`,改前已备份 `config.toml.bak-*`

2. **SSH 远程启动 Codex 要补 PATH**:
   - 非交互 shell 不加载 `~/.zshrc`,`codex` 是 node 程序会在 `~/.zshrc` 的 PATH 里(`CODEX_HOME/bin` + `/usr/local/bin`)
   - 必须显式: `export PATH=/usr/local/bin:$PATH`(node 在 `/usr/local/bin/node`)
   - 还要 `--skip-git-repo-check`(不在 git 仓库/非信目录时)和 `< /dev/null`(避免等 stdin)

3. **Codex CLI 与桌面版同配置 → 改一处两边都生效**(所以修顶层 model 同时修好了桌面版)。

## 四、远程启动姿势(Windows 遥控 Mac)

```bash
# Claude Code(零配置)
ssh w@100.83.233.122 'cd ~ && claude -p "任务"'

# Codex(补 PATH + 跳 git 检查)
ssh w@100.83.233.122 'export PATH=/usr/local/bin:$PATH && cd ~ && codex exec --skip-git-repo-check "任务" < /dev/null'
```

## 五、调度机制:Windows Hermes 派活给 Mac CLI(已定方案)

> 分工执行时的硬性规范,由 Windows 侧 Hermes(本会话)作为调度者执行。

### 5.1 消除"弹窗"(从源头,不靠监管)
headless 远程执行**没有 GUI 弹窗**,只有进程等 stdin(yes/no)→ 表现为卡死。
- **Codex**:必须 `--full-auto`(否则每步写文件/执行都等确认卡死)。配合 config `sandbox_mode = "danger-full-access"`。
- **Claude Code**:靠 `settings.json` 的 `permissions.allow: ["Bash(*)"]` 预授权(已配),基本不弹;远程跑加 `< /dev/null`。

### 5.2 远程启动标准姿势(无人值守)
```bash
# Claude Code(零配置 + 免确认)
ssh w@100.83.233.122 'cd ~ && claude -p "任务" < /dev/null'

# Codex(⚠️ codex exec 无 --full-auto 参数! 用 --approve-for-me 免确认)
#   实测: 带 --full-auto 会直接报错退出(这就是"读完了没执行就结束"的根因之一)
ssh w@100.83.233.122 'export PATH=/usr/local/bin:$PATH && cd ~ && codex exec --approve-for-me --skip-git-repo-check "任务" < /dev/null'
```
> 注意: config.toml 已设 `sandbox_mode = "danger-full-access"`,所以即使不加 `--approve-for-me` 多数情况也能自动执行;但**显式加 `--approve-for-me` 更稳**,且避免个别确认卡住。

### 5.2b Codex 空跑监管(必做)
Codex 存在"读完任务、列计划、但静默结束啥也没干"的失效模式。监管三招:
1. **任务必须带可验证产物**(创建文件/改代码/输出标记),跑完**检查产物是否存在**——缺失即判空跑。
2. **带 `timeout`**(如 `timeout 300`)+ 抓退出码;Codex 报错退出(如参数错误)≠ 成功。
3. 产物缺失/超时 → 重新派活或上报用户,**不要假装完成**。

### 5.3 调度者监管(防卡死)
- 每次派活**带 `timeout`**(如 `timeout 300`),超时就判"卡在确认/挂起"→ 自动杀 + 上报用户。
- 输出落日志(`2>&1 | tee /tmp/xxx.log`),调度者可回看卡点。
- 高危任务**拆细 + 分步确认**,不一股脑 `--full-auto` 乱跑。
- **桌面版 Codex 渲染进程死循环监控**(CLI 版不受影响):桌面 Codex(ChatGPT.app 内 Codex Framework 渲染器)可能陷 JS 死循环,表现为单渲染进程 CPU 持续 100%+ 且累计时间长。监控法:定期 `ps` 查 `Codex (Renderer)` 的 PID/CPU/时间,超阈值即 `kill` 该渲染 PID 并告警;**codex-relay(4446)与 codex++ 管理器不受影响,勿误杀**。实测案例:PID 13814 占 109% 跑 27 分, kill 后桌面版自愈。

### 5.4 分工定位
- **Windows Hermes = 私人助理 / 总调度**:派活 + 收结果,不自己干重活;任务粗粒度拆解(不过细)。
- **一般任务 → Codex 执行**(施工队);**Claude Code = 参谋长**:出方案 + 审 + 验收。
- **Mac Hermes = 常驻副脑**(打通 Claude + Codex),主用硅基流动免费 `Qwen/Qwen2.5-7B-Instruct`,断网 fallback 本地 Ollama `qwen2.5:7b`。
- **OpenClaw = 洗知识库 + 巡检**(Obsidian 新结构出来前暂定角色)。
- **yes/no 已预授权**:Claude `Bash(*)` + Codex `--approve-for-me`,派活不中断确认。
- **Mac 电源**:`SleepDisabled=1` 系统不眠;`caffeinate -s`(非 `-d`)保系统不睡、允许显示器 10min 熄屏 → 假休眠; `womp=1` 远程唤醒开。
- **Codex 桌面版 vs CLI 版分工(2026-08-26 东哥定)**:桌面版 codex-desktop 插件多 → 日常交互用;**大文件处理直接用 CLI 版 `codex exec`**(无渲染器死循环风险,见 5.3 监控)。桌面版死循环仅影响交互界面,不碍 CLI/中继。

### 5.5 写入 Obsidian 规则(不变)
**子任务每执行完一个,就写入知识库**,遵循用户既定铁律:
1. 先同步写 Windows Hermes 长期记忆;
2. 再写 Obsidian(双边:Windows `C:\Users\Administrator\知识库\` + Mac `/Users/w/Documents/知识库\`);
3. 只记解决实际问题的案例,纯问答不入库。

## 六、相关笔记

- [[mac-hermes-install]]——Mac 装 Hermes 方案(同目录)
- [[mac-hermes-installation-complete]]——装机完成确认(命令名 hermes-mac)
- [[mac-win-codex-relay]]——Mac↔Windows Codex 中转工作流(方向相反:Mac 通过 Windows Codex++ 中转)
- [[_ai/MEMORY.md]] 网络节——Tailscale 地址/SSH