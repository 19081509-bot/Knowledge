# ⚠️ OpenClaw Auto-compaction 压缩失败修复方案

## 报错含义

OpenClaw 会话上下文缓存超限，自动压缩机制无法清理冗余历史，会话占用 Token 溢出。

## 临时解决（不用改配置）

在 OpenClaw / Claudian 对话中输入：

```
/new
```

新建干净会话，立即恢复，不会丢已有记忆。

## 永久根治

### compaction 已配置的内容

`~/.openclaw/openclaw.json` 中 `agents.defaults` 已包含：

```json
"compaction": {
  "reserveTokensFloor": 35000
}
```

**注意**：OpenClaw 不支持 `autoCompactThreshold` 和 `compactRetainRecent`，加进去会导致配置报错，只需保留 `reserveTokensFloor` 即可。

### 验证方法

```bash
openclaw config validate
# 返回 Config valid 即正常
```

## 预防措施

1. 对话过长时，及时输入 `/new` 开新会话
2. 在 Claudian 中点击「保存为笔记」归档后重建对话
3. `MEMORY.md` 保持精简，不要写入超长文本
4. 单次不要同时 @ 引用 5 条以上笔记

## Claudian 设置建议

Obsidian → Claudian 设置：
- 关闭「加载全部历史对话上下文」
- 上下文缓存长度限制设为 15
- 对话归档后自动清空当前缓存

---

*记录于 2026-07-19*
