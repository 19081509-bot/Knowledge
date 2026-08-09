# COMPASS (Landmark) 定向井设计软件详细教程

> 来源: Landmark EDM COMPASS教程.doc + 实际施工方案
> 更新: 2026-08-09 补充完整教程

## 一、软件概述

Landmark钻井设计软件覆盖油田开发全过程，主要模块包括：
- **COMPASS**: 定向井设计(轨迹/测斜/防碰)
- **WellPlan**: 钻柱摩阻/扭矩/屈曲分析
- **CasingSeat**: 套管下深设计
- **StressCheck**: 套管柱设计
- **WellCat**: 高温高压井管柱分析
- **EDM**: 工程数据模块(通用数据库)

## 二、EDM数据库系统

### 2.1 登录
- 所有EDM钻井软件需要事先登录数据库
- 选择数据库+输入用户名密码
- 可通过EDM Administration更改密码
- 启动方式: 开始菜单→Landmark EDM→COMPASS, 或桌面快捷方式

### 2.2 数据结构层次
EDM采用层次对象数据结构:
公司(Company) → 项目(Project) → 位置(Location) → 井(Well) → 井眼(Wellbore) → 设计(Design) → 实例(Instance)

### 2.3 通用数据模块
- 单位系统(Units System)
- 管材目录(Pipe Catalog)
- 接头目录(Connections Catalog)
- 孔隙压力/破裂压力梯度
- 地温梯度
- 测斜数据

### 2.4 数据锁定
- 各级别可设定密码锁定(只读)
- 锁定后只能Save as或Export
- 被锁定项图标一角显示小锁

## 三、单位系统设置

Tools菜单→Units/Units System
- Active Viewing Unit System: 选择使用的单位系统
- 用户可自定义单位系统保存到数据库
- 关键单位: 深度(m/ft), 角度(°), 压力(MPa/psi), 长度(mm/in)

## 四、COMPASS三大核心模块

### 4.1 Survey(测斜模块)
- 井眼轨迹计算(支持多种行业标准方法)
  - **最小曲率法(Minimum Curvature)** ★★★★★ 行业标准
  - 半径曲率法/平衡正切法/平均角法/切线段法
- 数据手动输入或导入
- 支持惯性测斜和仅井斜数据
- Tool Interval Editor: 拼接多段测斜为最佳路径
- Project Ahead: 从测斜点预测至目标
- 数据质量校验: Input Validation + Varying Curvature
- 多基准面坐标参考

### 4.2 Planning(轨迹设计模块)
- 交互式轨迹设计工作簿, 分段构建
- 剖面类型:
  - **2D**: Slant(直斜)/S-Shaped(五段式)/J-Shaped(J型)
  - **3D**: Dogleg-Toolface / Build-Turn
- 实时图形更新
- Wellbore Optimizer: 集成扭矩/摩阻分析
  - 优化目标: 最低成本/防碰最优/最小摩阻
- 检测功能: 碰撞/超限/屈曲等不可钻设计

### 4.3 Anticollision(防碰扫描模块)
- Spider Plot(蜘蛛网图)
- Ladder Plot(阶梯图)
- Traveling Cylinder Plot(行进圆柱图)
- Separation Factor(分离系数)定量评估
- Error Ellipse(误差椭圆)考虑测斜不确定度
- 3D Proximity View三维可视化
- 交互式防碰扫描, 实时联动规划修改

## 五、设计概念

| 概念 | 说明 |
|------|------|
| Actual Design | 实钻轨迹(由测斜数据构成, 每井眼仅一个) |
| Prototype Design | 方案设计(拟钻井眼轨迹, 可多个) |
| Planned Design | 批准设计(标记为批准施工, 每井眼仅一个) |
| Lookahead | 以当前最深测斜点为起点的延伸预测 |

## 六、详细操作流程

### 6.1 新建项目
1. 登录EDM数据库
2. File→New Project
3. 设置项目名称/坐标系/基准面
4. 设置磁偏角(输入当地磁偏角+日期)

### 6.2 新建井/井眼
1. 在Well Explorer右键→New Well
2. 输入井名/坐标/海拔
3. 右键井→New Wellbore
4. 选择井眼类型(直井/定向井/水平井)
5. 如果是侧钻井: Sidetrack from an Existing Wellbore→选择老眼轨迹

### 6.3 磁偏角设置(Magnetics)
- 选择地磁模型和采样日期
- 磁偏角随时间变化, 需选定适当日期
- 自动计算: 磁偏角/地磁倾角/磁场强度
- 口诀: **东加西减**

### 6.4 新建设计(Design)
**General属性:**
- Detail: 设计名称和描述
- Prototype/Planned(principal): 最终设计(每井眼只能有一个)
- Depth Reference: 选择高度参考

**Tie-on Point(接点数据):**
- User Defined: 自定义(输入测深/井斜/方位/垂深/坐标)
- From Surface: 从井口开始(初始井斜)
- From Survey/Plan: 从已有测斜/设计选择起点
- Tortuosity: 弯曲指数DDI(Directional Difficulty Index)

**Survey Tool Program(测斜工具选择):**
- 定义各井段测量工具
- MD From/To: 起始/结束井深
- Survey Tool: 测量仪器类型

**Vert Section(水平位移投影方位):**
- 决定投影面显示轨迹
- 可分段定义投影方位
- Azimuth Type: 井底点/目标点/自定义
- Origin Type: 投影起点

### 6.5 定义靶点(Target)
1. 打开Target Editor
2. 输入靶点名称和参数
3. 选项卡:
   - Name & Location: 名称/垂深/中心坐标(Local/Map/Geographic/Polar/Lease)
   - Geometry: 靶区形状
   - Drilling Target: 钻井靶点

**靶区形状:**
| 形状 | 参数 |
|------|------|
| Point(点) | 无额外参数 |
| Circle(圆) | 靶半径 |
| Ellipse(椭圆) | 短半轴Minor/长半轴Major |
| Rectangle(矩形) | 靶宽Width/靶长Length |
| Polygon(多边形) | 各点位移或坐标 |

**高级参数:**
- Thickness: Up/Down 靶区上下厚度
- Offset from Target Centre: X/Y偏移
- Rotation About Centre: 旋转角度
- Formation Plane: 地层倾角Dip/方向Direction
- Start and End Angle: 圆弧起始角度

### 6.6 轨迹设计
1. Planning Editor中分段设计
2. 可选择剖面类型(2D/3D)
3. 插入/删除/修改分段
4. 实时图形显示更新
5. 可使用Wellbore Optimizer自动优化

### 6.7 导入测斜数据
1. Survey Editor→导入/输入实钻数据
2. 支持多种格式
3. 数据校验

### 6.8 防碰分析
1. 加载邻井数据
2. 运行防碰扫描
3. 查看蜘蛛网图/阶梯图/行进圆柱图
4. 检查分离系数(SF>1.5安全)

### 6.9 出图出报告
- 生成轨迹图/防碰图/施工报表
- 水平投影图+垂直剖面图
- 防碰间距曲线图

## 七、EDM数据管理

### 7.1 .EDM文件
- EDM文件(.edm.xml)是COMPASS项目的数据库文件
- 包含完整的井眼设计/测斜/防碰数据
- 可在不同电脑间传输和导入

### 7.2 数据导出/导入
- Save as: 另存为新设计
- Export/Import: 跨项目数据交换
- 支持多种测斜数据格式

## 八、与Landmark套件集成

| 软件 | 功能 | 与COMPASS关系 |
|------|------|--------------|
| WellPlan | 钻柱摩阻/扭矩/屈曲详细分析 | 共享EDM数据 |
| WELLCAT | 井筒热力学/套管应力分析 | 独立运行 |
| StressCheck | 井壁稳定性/套管强度 | 共享数据 |
| OpenWells | 钻井日报/井数据管理 | 数据互通 |
| AutoSync | 现场-办公室数据同步 | 实时同步 |
