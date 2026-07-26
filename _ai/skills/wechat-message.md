# wechat-message — 微信消息发送技能

> 通过 macOS GUI 自动化发送微信消息/文件给指定联系人。
> 脚本位置: `~/scripts/send_wechat_v4.py` / `~/scripts/send_wechat_file.py`

## 快速命令

```bash
# 发文字消息
python3 ~/scripts/send_wechat_v4.py <拼音> '<消息>'

# 发文件+附言
python3 ~/scripts/send_wechat_file.py <拼音> '<文件路径>' '[附言]'
```

## 已知联系人

| 联系人 | 拼音 |
|--------|------|
| 王东 | wangdong |
| 辉癫癫 | huidiandian |
| 张先明 | zhangxianming |

完整拼音表: `~/.openclaw/workspace/contacts_pinyin.json`

## 核心原理

通过 pyautogui + AppleScript 操控 macOS 微信桌面版:
1. 激活微信窗口 (AppleScript)
2. 切换英文输入法
3. 搜索联系人 (按窗口比例算坐标 + AppleScript keystroke 输入拼音)
4. pbcopy + AppleScript Cmd+V 粘贴中文消息（绕过输入法拦截）
5. Enter 发送
6. 关闭微信窗口，保留 Dock 进程

## 依赖

- gui-automation skill
- Python 3 + pyautogui + pygetwindow
- macOS 微信桌面版
- 终端需要辅助功能权限

## 完整文档

- SKILL.md: `~/.openclaw/workspace/skills/wechat-message/SKILL.md`
- WEIXIN_GUI.md: `~/.openclaw/workspace/WEIXIN_GUI.md`