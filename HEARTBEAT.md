# 🕐 Heartbeat 巡检任务

> 每次心跳触发时，执行以下巡检任务。
> 任务按优先级排列，做完即止。

---

## 1. 运行清洗脚本

执行归档清理脚本，将 `00_Inbox/` 中的新内容分类归档：

```bash
python3 /Users/w/Documents/知识库/_ai/scripts/heartbeat-cleanup.py
```

如果脚本未提交推送成功，手动补齐：

```bash
cd /Users/w/Documents/知识库
git add -A && git commit -m "heartbeat: manual sync $(date +%Y-%m-%d-%H%M)" && git push
```

## 2. 检查 Git 状态

确认最新变更已推送到 GitHub：

```bash
cd /Users/w/Documents/知识库 && git status --short
```

如果有未推送的 commit，手动 push。

## 3. 更新每日日记

检查 `memory/` 目录，如果当天（YYYY-MM-DD）没有日记文件，创建一个简要记录。

---

## 执行原则

- 每一步做完再走下一步
- 如果某步失败（如 git push 网络不通），跳过继续下一步
- 不做一般性问答，不闲聊
- 巡检完即止，不需要等东哥回复
