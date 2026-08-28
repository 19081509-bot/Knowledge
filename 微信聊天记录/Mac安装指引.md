# Mac 安装与导出指引 · WeChatDataAnalysis

> 执行人：Mac Claude Code CLI。场景：微信聊天记录导出清洗（见 `00-说明.md` 与 `Mac任务简报-ClaudeCode.md`）。
> 边界：**只处理微信客户端 / WeChatDataAnalysis 的明文导出，严禁读取微信 SQLCipher 加密库。**

## 一、软件来源与安装

- **官方下载**（GitHub Release）：
  `https://github.com/LifeArchiveProject/WeChatDataAnalysis/releases`
- 在 Release 页下载最新 macOS 版 `.dmg`（本机已装 **v2.2.1**，确认在 `/Applications/WeChatDataAnalysis.app`）。
- 安装/首次打开若遇"无法验证开发者"，在「系统设置 → 隐私与安全性」底部点「仍要打开」。GUI 安装需东哥手动，Claude 不代点。

## 二、导出单个联系人/群的聊天记录

微信客户端自身没有批量导出 API，只能逐人导出（Windows/Mac 同法）：

1. 打开某联系人/群的聊天窗口 → 右上角 `...` → **导出聊天记录**
2. 选时间范围 → 导出（生成文件夹，含 `index.html` + 媒体占位符）
3. 若用 WeChatDataAnalysis 导出：在工具内选中该联系人/群 → 导出为 **JSON / TXT**
4. GUI 内的具体按钮位置以工具当前界面为准，此处只定落位规则（见三）

## 三、导出文件放哪（按联系人归档）

```
01-原始导出/<联系人名>/Mac-YYYYMMDD.json      ← 首选（工具导出的 JSON）
01-原始导出/<联系人名>/Mac-YYYYMMDD.html     ← 也可（客户端导出的 index.html）
```

- 一个联系人一个文件夹；同人多次导出文件名带不同日期即可（合并清洗阶段再做）。
- 示例：`01-原始导出/王东/Mac-20260828.json`

## 四、安全底线（清洗阶段严格执行）

- 严禁读取微信加密库（`db_storage/` 下 `*.db` 为 SQLCipher 加密，不逆向、不破解）
- 导出文件含他人隐私，清洗落库前必脱敏：手机号/身份证/银行卡/地址等 PII 打码（如 `138****1234`）
- 不修改任何微信原始数据，只产出 `02-清洗后/<联系人名>.md`

## 五、完成后回报

- 建好文件后回报：指引已写 + 目录确认
- 等东哥在 GUI 导出 `01-原始导出/<联系人名>/` 后，再执行清洗（阶段2）