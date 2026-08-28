# Mac 安装 Hermes 完成记录(2026-08-26 实测)

> Windows 侧指挥安装的最终交付确认:Mac 端 Hermes CLI 已装好并跑通模型链路。
> 本文是 `mac-hermes-install.md`(方案)的**完成确认篇**——方案还写了"待执行",这篇标记结果。

## 一、安装结果(实测确认)

| 项 | 状态 | 实测证据 |
|---|---|---|
| Hermes 版本 | ✅ v0.20.5 | `hermes-mac --version` → `Hermes Agent v0.20.5 (2026.8.19) · upstream 76e306c4` |
| 安装位置 | ✅ `~/.hermes/hermes-agent/` | 代码 + venv 都在此 |
| 可执行命令 | ⚠️ **`hermes-mac`(不是 `hermes`)** | 符号链接 `/usr/local/bin/hermes-mac → ~/.hermes/hermes-agent/.venv/bin/hermes`;PATH 上没有 `hermes` 这个名字 |
| 模型配置 | ✅ 硅基流动 + DeepSeek-V4-Flash | `~/.hermes/config.yaml`:`model.default=deepseek-ai/DeepSeek-V4-Flash`, `provider: siliconflow`, `base_url: https://api.siliconflow.cn/v1`(与 Windows 侧配置一致) |
| 模型链路 | ✅ **实测跑通** | 真实对话完成:会话 `20260826_001558_987112`,2 条消息,1m14s,正常响应 |

## 二、硬性注意(其它 agent 远程调用它时必读)

**命令名是 `hermes-mac`,不是 `hermes`**:

```bash
# ✅ 正确(Windows 侧 SSH 远程调 Mac 的 Hermes)
ssh w@100.83.233.122 'export PATH=/usr/local/bin:$PATH && hermes-mac chat -q "任务"'

# ❌ 不要用 hermes(会 command not found;PATH 上只有 hermes-mac)
```

> 安装者(Windows 侧 Hermes)最初用 `hermes` 测试失败,查符号链接才发现真名是 `hermes-mac`。这个坑已踩过,别再踩。

## 三、配置要点(与 Windows 完全一致)

```yaml
# ~/.hermes/config.yaml(Mac 侧)
model:
  default: deepseek-ai/DeepSeek-V4-Flash
  provider: siliconflow
  base_url: https://api.siliconflow.cn/v1
providers:
  siliconflow:
    base_url: https://api.siliconflow.cn/v1
    key_env: SILICONFLOW_API_KEY   # key 从环境变量读(Mac 的 ~/.zshrc 已有)
```

## 四、与方案文档的关系

- `mac-hermes-install.md`——**方案**(怎么装:降 cryptography 48.0.1、清华 PyPI 镜像、Python 3.13、绕 crates.io)
- `mac-ai-architecture.md`——**链路**(codex/Claude Code/Hermes 各自走哪个中转)
- **本文**——**完成确认**(装好、命令名、实测通)

## 五、联动现状(三链路全部实测通)

```
Windows(出差/办公室) ──SSH──▶ Mac
  ├─ Claude Code   ✅ claude -p "任务"
  ├─ Codex         ✅ codex exec --skip-git-repo-check "任务"(已修顶层 model)
  └─ Hermes        ✅ hermes-mac chat -q "任务"(本次确认)
```

## 相关笔记

- [[mac-hermes-install]]——安装方案
- [[mac-ai-architecture]]——模型链路
- [[_ai/MEMORY.md]]——全局规则 / Tailscale 网络节