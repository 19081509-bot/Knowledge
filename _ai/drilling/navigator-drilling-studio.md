# Navigator Drilling Studio 钻井工程软件

> 来源: Navigator Drilling Studio (C:\Program Files (x86)\Navigator Drilling Studio)
> 整理: Windows Codex CLI
> 更新时间: 2026-08-09

## 概述
Navigator Drilling Studio 是专业的钻井工程设计软件，安装于本机 Windows。

## 核心模块
- **BHA Editor**: 底部钻具组合设计与分析
- **Hydraulics**: 水力参数设计与优化
- **Torque/Drag**: 摩阻/扭矩模拟分析
- **Well Planning**: 井眼轨迹规划
- ** casing design**: 套管设计

## 目录结构
- `data/`: 工程数据库
- `help/`: 帮助文档
- `HydData/HydDataEU`: 水力计算数据库
- `tddata/tddataEU`: 钻柱/工具数据库
- `unit/`: 单位制配置文件
- `Styles/`: UI 样式
- `NDSReport/`: NDS 报表模板
- `Output/`: 计算结果输出

## 主要可执行文件
- `BHA_Editor.exe`: BHA 编辑器
- `dataviewer.exe`: 数据查看器
- `convert.exe`: 单位转换工具

## 工具数据库 (tddata/)
- `Bit_Coeff.csv`: 钻头系数数据库
- `Casing_Centralizer_cat.csv`: 套管扶正器目录
- `material.csv`: 材料属性数据库
- `RepCO.xlt / RepMG.xlt / RepSP.xlt / RepUD.xlt`: 报表模板

## NDS (Navigator Data System) 输出
NDSOutput 目录包含设计输出，包括:
- 中靶分析报表 (Target Analysis Report)
- 设计报表 (Design Report)
- 相关 XML 数据文件

## 与 Landmark 的关系
Navigator 专注于钻井工程详细计算（BHA/水力/摩阻），
而 Landmark COMPASS 专注于定向井轨迹设计与防碰分析，
两者可互补使用。