# COMPASS 防碰扫描与报表完全指南

> 更新: 2026-08-10
> 来源: 实际软件分析 + EDM XML 反查 + 现场调试

## 一、防碰扫描核心概念

### 1.1 扫描原理
防碰扫描计算**设计井**与周围**已钻井（Offset Well）**之间的空间距离，评估碰撞风险。

关键指标：
- **分离系数 (Separation Factor, SF)**：设计井误差椭圆边界到老井的最小距离 ÷ 椭圆半长轴。SF > 1.5 安全，SF < 1.0 有碰撞风险
- **中心距离 (Center-to-Center Distance)**：两口井轨迹之间的直线距离
- **3D 分离距离 (3D Separation)**：考虑误差椭圆后的三维分离距离

### 1.2 COMPASS 中的防碰视图
- **Spider Plot（蜘蛛网图）**：俯视投影，显示各井相对位置
- **Ladder Plot（阶梯图）**：沿井深展开的分离距离曲线
- **Traveling Cylinder Plot（行进圆柱图）**：三维立体视图
- **Separation Factor View（分离系数图）**：SF 沿井深变化曲线
- **Error Ellipse View（误差椭圆图）**：显示误差椭圆大小和方向

## 二、Offset Well（老井）正确建法

### 2.1 常见错误
**错误做法**：把老井的测斜数据作为设计井的第二个 wellbore 挂进去。
→ 后果：Offset SMA（半长轴）= 0，分离系数算不出来。

**正确做法**：每口老井必须是独立的 Well 实体。

### 2.2 操作步骤

**Step 1 — 建新井**
`
File → New → Well
`
- Well Name: 老井名（如 ZY-545H1、ZY-547）
- Site: 选同一平台
- 在 Well Properties 里输入 slot_ew、slot_ns 坐标

**Step 2 — 输入测斜数据**
`
Survey → New → Survey Header
`
- Type 选 **Actual**（不是 Design）
- 输入 MD / Inclination / Azimuth
- 支持手动输入、粘贴、文件导入

**Step 3 — 配置测斜工具和误差模型（关键！）**
`
Survey → Survey Program
`
- 选测斜工具：**MWD std**
- 确认 Assign Error Model：**ISCWSA MWD**（error_model=3）
- ⚠️ 不配这一步 → SMA = 0 → SF 算不出来

**Step 4 — 执行防碰扫描**
`
Calculations → Anticollision
`
- Offset Wells 列表勾选对应老井
- 设扫描范围（MD from/to）
- 点 Scan 执行

### 2.3 误差模型类型
| 值 | 模型 | 说明 |
|----|------|------|
| 0 | 无误差模型 | 不推荐 |
| 1 | 通用模型 | 粗略估计 |
| 2 | 行业标准模型 | 较精确 |
| 3 | **ISCWSA MWD** | 行业标准，推荐 |

## 三、防碰报表语言问题

### 3.1 问题根因
COMPASS 界面语言 ≠ 报表模板语言。

- **界面汉化**：中文 DLL 覆盖 C:\Landmark\EDT\COMPASS\Bin\ → 菜单/对话框中文
- **报表模板**：.rpt 文件（Crystal Reports 编译二进制）→ 语言文字嵌入在专有格式中，与 DLL 汉化相互独立

### 3.2 关键文件位置
`
报表模板根目录:
C:\Landmark\EDT\EDM\Site Configuration Files\OutputReports\

Common/                              ← 公共子报表
├── CompassAnticollisionInfo.rpt     ← 防碰信息子报表
├── CompassACReportHeader.rpt        ← 防碰报表头
├── CompassEllipseSep.rpt            ← 椭圆分离
├── CompassEllipseSepSummary.rpt     ← 椭圆分离汇总
├── CompassHeader.rpt                ← 通用报表头
├── CompassStandardSurvey.rpt        ← 标准测斜报表
└── CompassConfigurableSurveyReport*.rpt  ← 可配测斜报表

Landmark/Design/
├── Compass Anticollision with Risk/ ← 主防碰报表
│   ├── CompassAnticollisionRisk.rpt
│   ├── CompassAnticollisionRiskConfig.xml
│   ├── CompassAnticollisionRiskFiltered.xsd
│   ├── CompassAnticollisionRiskTables.xml
│   ├── plot_1.wpc                   ← 防碰图
│   └── plot_2.wpc                   ← 分离系数图
├── Compass Ellipse Separation/      ← 椭圆分离报表
├── Compass Ellipse Separation Summary/
└── Compass Travelling Cylinder/     ← 行进圆柱图报表
`

### 3.3 报表字段映射
| 数据库字段 | 含义 | 中文名 |
|-----------|------|--------|
| ref_md | Reference MD | 参考井深 |
| off_md | Offset MD | 邻井井深 |
| sep_3d | 3D Separation | 三维分离距离 |
| sep_cc | Center-to-Center Distance | 中心距离 |
| sep_factor | Separation Factor | 分离系数 |
| off_ellipse_maj | Offset Semi-Major Axis | 邻井半长轴 |
| ref_ellipse_maj | Reference Semi-Major Axis | 参考井半长轴 |
| off_tvd / ref_tvd | TVD | 垂深 |

### 3.4 解决方案
1. **找到中文 .rpt 模板**（最佳）：从同事处拷贝后替换即可
2. **导出 TXT 后替换表头**：COMPASS 导出 TXT → 手动/脚本替换英文表头为中文
3. **使用 Crystal Reports 编辑**：有 Designer 软件可直接改 .rpt

## 四、EDM XML 结构分析

### 4.1 数据层次
`
Company → Project → Site → Well → Wellbore → Scenario → Survey
`

### 4.2 关键 XML 标签
| 标签 | 含义 | 关键属性 |
|------|------|----------|
| CD_SITE | 平台/井场 | site_name, coord_type, geo_latitude/longitude |
| CD_WELL_ALL | 井 | well_common_name, slot_ew/slot_ns, coord_type |
| CD_WELLBORE | 井眼 | wellbore_name, ko_md, bh_md/tvd |
| CD_SURVEY_HEADER | 测斜段 | survey_type(100=Design, 0=Actual), survey_name |
| CD_SURVEY_STATION | 测斜点 | md, inclination, azimuth, tvd, offset_east/north |
| CD_SURVEY_PROGRAM | 测斜程序 | survey_tool_id, md_base/md_top |
| CD_SCENARIO | 场景 | phase(PROTOTYPE/PLAN), name |
| CD_POLICY | 政策 | error_model(3=ISCWSA), scan_method, error_level |
| DP_TOOL_TERM | 误差模型项 | term_name, c_value, c_formula |
| DP_ACRULE | 防碰规则 | rule_name, ac_ratio |
| CD_OFFSET_WELL | 老井引用 | offset_well_id（注意: COMPASS 中为独立 CD_WELL_ALL） |

### 4.3 survey_type 值
| 值 | 含义 |
|----|------|
| 0 | Actual（实钻） |
| 100 | Plan/Design（设计） |
| 200 | Lookahead（延伸预测） |
| 300 | Definitive（终测） |

### 4.4 coord_type 值
| 值 | 含义 |
|----|------|
| 0 | Slot（槽口坐标） |
| 1 | Lat/Lon（经纬度） |
| 2 | Map（地图投影坐标） |

## 五、常见问题排查

### 5.1 防碰报告英文
- ✅ 界面是中文 → DLL 汉化已生效
- ❌ 报表是英文 → .rpt 模板未汉化（需单独处理）
- 验证方法：检查 OutputReports/Common/*.rpt 文件日期，对比原始安装包

### 5.2 Offset SMA = 0
- 原因：老井没有独立测斜工具和误差模型
- 解决：Survey Program 中选 MWD + ISCWSA

### 5.3 数据库结构问题
- ZY-545H1 重复出现两次 → 需清理冗余
- 井名前后有空格（TS-522、ZY-169）→ 影响匹配
- 缺少 <CD_OFFSET_WELL> 标签 → 需要建独立 Offset Well 实体
