# COMPASS (Landmark) 定向井设计软件基础

> 来源: Landmark EDT COMPASS 帮助文档 + 实际施工方案
> 整理: Windows Codex CLI (DeepSeek-v4-flash)
> 更新时间: 2026-08-09

## 概述
COMPASS 是 Landmark 套件中的定向井设计与分析软件。
三大核心模块: Survey(测斜), Planning(轨迹设计), Anticollision(防碰扫描)。
支持扭矩/摩阻优化、绘图与报告生成。

## Survey 测斜模块
- 井眼轨迹计算，支持多种行业标准方法
- 数据手动输入/导入，支持惯性测斜和仅井斜数据
- 工具间隔编辑器拼接多段测斜为最佳路径
- Project Ahead: 从测斜点预测至目标
- 数据质量校验: Input Validation + Varying Curvature
- 多基准面坐标参考，多种格式导出

## Planning 轨迹设计模块
- 交互式轨迹设计工作簿，分段构建
- 剖面类型: 2D (Slant/S-Shaped), 3D (Dogleg-Toolface/Build-Turn)
- 实时图形更新，灵活插入/删除/修改分段
- Wellbore Optimizer: 集成扭矩/摩阻分析，自动搜索最优轨迹参数
- 优化目标: 最低成本/防碰最优/最小摩阻
- 检测: 碰撞/超限/屈曲等不可钻设计

## Anticollision 防碰扫描模块
- Spider Plot(蜘蛛网图), Ladder Plot(阶梯图)
- Traveling Cylinder Plot(行进圆柱图)
- Separation Factor(分离系数)定量评估碰撞风险
- Error Ellipse(误差椭圆)考虑测斜不确定度
- 3D Proximity View 三维可视化
- 支持交互式防碰扫描，实时联动规划修改

## 设计概念 (Design Concept)
- Actual Design: 实钻轨迹(由测斜数据构成，每井眼仅一个)
- Prototype Design: 方案设计(拟钻井眼轨迹，可多个)
- Planned Design: 批准设计(标记为批准施工，每井眼仅一个)
- Lookahead: 以当前最深测斜点为起点的延伸预测

## 常用工作流
1. 建立项目 → 设置坐标系/基准面/磁偏角
2. 输入靶点(Target) → 定义地质目标坐标/深度
3. 设计轨迹 → Planning Editor 分段设计剖面
4. 导入测斜 → Survey Editor 导入/输入实钻数据
5. 防碰分析 → 加载邻井数据，运行防碰扫描
6. 优化与验证 → Wellbore Optimizer 检查可钻性
7. 出图出报告 → 生成轨迹图/防碰图/施工报表

## 与 Landmark 套件集成
- WellPlan: 钻柱摩阻/扭矩/屈曲详细分析
- WELLCAT: 井筒热力学/套管应力分析
- StressCheck: 井壁稳定性分析
- EDM: 数据管理与归档
- OpenWells: 钻井日报/井数据管理
- AutoSync: 现场-办公室数据同步