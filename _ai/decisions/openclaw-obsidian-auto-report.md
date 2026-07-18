# 📋 OpenClaw + Obsidian 自动化方案 — 可行性评估报告

**评估日期**: 2026-07-18
**评估对象**: 你提供的那份配置方案
**实际环境**: OpenClaw 2026.7.1 / Claude Code 2.1.212 / codex-relay 待确认

---

## 一、整体结论

| 项目 | 结论 |
|------|------|
| **总体可实现度** | ⚠️ 约 **60%** 可直接落地，**40%** 需要适配或替代方案 |
| **能直接用的** | OpenClaw + 多模型路由 + Claude Code 集成 + 硅基 API |
| **不能照搬的** | 配置格式、插件名称、部分命令与实际不符 |
| **风险评估** | 配置 JSON 格式不同，直接覆盖会导致 OpenClaw 启动失败 |

---

## 二、逐个条款核对

### ✅ 前置校验 — 基本可行

| 条目 | 状态 | 说明 |
|------|------|------|
| 权限补齐 | ✅ | 确实需要给 OpenClaw 完全磁盘访问权限 |
| claude --version | ✅ | 已安装 v2.1.212 |
| openclaw --version | ✅ | 已安装 v2026.7.1 |
| codex-relay 端口 | ⚠️ | 文件写 4446，我们之前用的是 57321，需确认 relay 当前端口 |
| `openclaw onboard --reset` | ✅ | 命令存在 |

### ❌ 配置文件 — 不能直接覆盖

**文件给出的 JSON 格式与实际的 OpenClaw 配置格式完全不同：**

| 项目 | 文件中的写法 | 实际 OpenClaw 格式 |
|------|-------------|-------------------|
| agents 结构 | 有 `memoryFile`、`autoLoadVaultMemory` | 实际没有这些字段 |
| models.providers | 用 `claude-code`/`codex-relay` 做 provider ID | 实际 provider ID 是 `custom-api-siliconflow-cn` 这种格式 |
| skills | `file-watcher`、`obsidian-write`、`ai-router`、`vault-sync` | 实际 skills 机制不同，这些 skill 不存在 |
| gateway.port | 38080 | 实际是 18789 |
| `clawhub` 命令 | `clawhub install ...` | 实际命令是 `openclaw plugins install clawhub:...` |

⚠️ **风险**: 直接把文件中的 JSON 覆盖到 `~/.openclaw/openclaw.json` 会导致 OpenClaw 解析失败无法启动。

### ❌ 插件/技能 — 名称不匹配

| 文件中的命令 | 实际状态 |
|-------------|---------|
| `clawhub install file-watcher` | ❌ `clawhub` 命令不存在 |
| `openclaw vault new` | ❌ `vault` 子命令不存在 |
| `openclaw daemon install` | ❌ 不存在，用 `openclaw gateway run --daemon` |
| Obsidian 插件 "Claudian" | ⚠️ 需确认 Obsidian 社区是否有此插件 |

### ⚠️ MEMORY.md — 概念可行但机制不同

文件中说 OpenClaw 会自动加载 `MEMORY.md`，但实际 OpenClaw 没有内置这个功能。不过可以通过 **custom skill** 或 **agent 配置** 实现类似效果。

---

## 三、真实可行的替代方案

### 替代 1：用 OpenClaw 原生能力实现多模型路由

OpenClaw 实际已支持多 provider（硅基已配好），只需在 `agents.defaults.models` 里配置不同模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "custom-api-siliconflow-cn/deepseek-ai/DeepSeek-V4-Pro"
      },
      "models": {
        "custom-api-siliconflow-cn/deepseek-ai/DeepSeek-V4-Flash": {},
        "custom-api-siliconflow-cn/deepseek-ai/DeepSeek-V4-Pro": {},
        "custom-api-siliconflow-cn/Qwen/Qwen3-235B-A22B-Thinking-2507": {}
      }
    }
  }
}
```

### 替代 2：用 OpenClaw skills 代替 "file-watcher"

OpenClaw 有 skills 机制，可以写自定义 skill 来监听文件变化并处理。不需要依赖不存在的插件。

### 替代 3：用 `launchctl` / `crontab` 代替 "daemon install"

```bash
# OpenClaw gateway 后台运行
openclaw gateway run --daemon

# 或者用 launchctl 配开机自启
```

### 替代 4：MEMORY.md 用 OpenClaw 的 workspace 机制

把 MEMORY.md 放到 workspace 目录，在 agent prompt 中引用即可。

---

## 四、推荐的实际落地步骤

### 阶段一：基础配置（今天可做）

1. **给 OpenClaw 开权限**：系统设置 → 隐私 → 完全磁盘访问 → 添加 OpenClaw
2. **配置 OpenClaw 的多模型**：
   ```bash
   openclaw configure --section model
   ```
3. **启动 gateway**：
   ```bash
   openclaw gateway run --daemon
   ```

### 阶段二：Obsidian 集成（需确认插件）

1. Obsidian 安装 **Local REST API** 插件（确认存在）
2. 配置 OpenClaw 通过 REST API 读写 Obsidian
3. 写一个 OpenClaw skill 实现「剪藏到 Inbox → 自动分类」

### 阶段三：自动化工作流

1. 用 crontab 或 launchd 做定时 Git 同步（已有 crontab）
2. 写 OpenClaw custom skill 实现文件监听
3. 配置多模型自动路由

---

## 五、需要你确认的信息

1. **Obsidian 库路径** — 是 `~/ai-vault` 还是别的？
2. **codex-relay 当前端口** — 是 57321 还是 4446？
3. **是否需要同时用 Claude Code** — Claude Code 有独立的 API key，你有吗？
4. **Obsidian 插件** — 你的 Obsidian 里已经装了哪些插件？

---

## 六、总结

| | 文件中的方案 | 实际可行方案 |
|--|------------|------------|
| 复杂度 | 中高 | 中 |
| 直接可用度 | ~60% 概念正确 | 需适配实际命令和格式 |
| 风险 | 配置覆盖会 crash | 逐步配置，安全 |
| 自动化程度 | 全自动 | 可达到 80% 以上 |

**建议**：不直接照搬文件 JSON，而是基于 OpenClaw 实际的能力和格式来重新配置。我可以帮你逐条落地。
