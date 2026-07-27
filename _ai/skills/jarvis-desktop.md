---
name: jarvis-desktop
description: 桌面控制技能 — 浏览器自动化、文件操作、系统命令
---

## 概述

提供桌面控制能力，让 AI 可以操作浏览器、管理文件、执行系统命令。

## 浏览器控制

通过 Playwright MCP 控制浏览器：

```bash
# 使用 npx 直接调用 Playwright MCP
npx -y @anthropic/mcp-server-playwright
```

### 能力范围
- 🌐 打开/关闭网页标签
- 🔍 搜索信息、读取页面内容
- 📷 网页截图
- 🖱️ 点击按钮、填写表单
- 📥 下载文件

### 使用示例
```
用户: "贾维斯，帮我在百度搜索今天的新闻"
AI: 调用 browser 打开 baidu.com → 输入关键词 → 读取搜索结果 → TTS 播报
```

## 文件操作

通过 filesystem MCP 管理系统文件：

```bash
npx -y @modelprotocol/server-filesystem \
  /Users/w/Documents/知识库 \
  /Users/w/scripts \
  /Users/w/Downloads
```

### 能力范围
- 📂 读取/创建/编辑文件
- 🔍 搜索文件内容
- 📋 复制/移动/删除文件
- 📊 读取 CSV/JSON/Markdown

## 系统命令

通过 system MCP 执行终端命令：

```bash
npx -y @anthropic/mcp-server-system
```

### 能力范围
- 💻 执行 shell 命令
- ⚙️ 管理系统进程
- 📈 查看系统资源
- 🔧 运行脚本

## 使用限制

- ⚠️ 执行可能影响系统的命令前需用户确认
- ⚠️ 浏览器操作受页面加载速度影响
- ⚠️ 文件删除操作需二次确认

## 配置

MCP 服务器需在 `~/.openclaw/openclaw.json` 中配置：

```json5
{
  "tools": {
    "mcpServers": {
      "browser": {
        "command": "npx",
        "args": ["-y", "@anthropic/mcp-server-playwright"]
      },
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelprotocol/server-filesystem",
          "/Users/w/Documents/知识库",
          "/Users/w/scripts",
          "/Users/w/Downloads"]
      }
    }
  }
}
```
