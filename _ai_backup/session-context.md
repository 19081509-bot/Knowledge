# 🧠 Session Context — 对话上下文持久化

> 使命: 对话崩溃后自动恢复上下文，有 Obsidian 时同步到 Mac
> 最后更新: 2026-08-11 09:30
> 当前模型: DeepSeek V4 (纯文本，无沙箱限制)

## 当前项目
- **任务**: 定向井 COMPASS 5000.17 防碰报表汉化 + EDM 数据库分析
- **工作目录**: C:\Users\Administrator\Documents\Codex\2026-08-10\ni-2
- **相关知识库**: C:\Users\Administrator\知识库\

## 本次会话笔记
8月10-11日完成：
1. 防碰报表英文根因确认（.rpt为Crystal Reports编译格式，DLL汉化不覆盖报表模板）
2. 中联煤煤层气.edm.xml分析（28口井，3平台，缺Offset Well，ZY-545H1重复）
3. 防碰+EDM知识写入Mac Obsidian知识库
4. 本机记忆持久化体系建立

## 关键知识点
### COMPASS
- 报表语言由.rpt模板独立控制，与DLL无关
- Offset Well必须是独立Well实体+MWD ISCWSA误差模型
- 导出可用Word/TXT后处理

### EDM XML
- 层次: Company→Project→Site→Well→Wellbore→Scenario→Survey
- survey_type: 0=Actual, 100=Design, 200=Lookahead
- coord_type: 0=槽口坐标, 1=经纬度, 2=地图投影

### Mac连接
- SSH: ssh -o StrictHostKeyChecking=no w@192.168.1.10
- 知识库: /Users/w/Documents/知识库/

## 待办
- [ ] 找中文.rpt模板替换（待同事/网上）
- [ ] 中联煤项目建Offset Well做防碰扫描
- [ ] 防碰导出Word格式替代方案

---

*保存: session-save.ps1/bat | 恢复: session-restore.ps1/bat*
*有Mac时运行sync同步到Obsidian*
