# EDM XML 数据库结构分析（实战案例）

> 更新: 2026-08-10
> 来源: 中联煤煤层气.edm.xml + 长城钻探.edm.xml + 纯梁采油厂.edm.xml

## 一、中联煤煤层气项目

### 1.1 基本信息
- **数据库版本**: EDM 5000.17.1 (17.01.00.000)
- **坐标系统**: Gauss-Kruger (Pulkovo 1942) GK Zone 19
- **椭球体**: Krassovsky 1940
- **客户**: 中联煤煤层气
- **创建时间**: 2025-10 至 2025-12
- **最近更新**: 2026-08-10

### 1.2 平台（Site）分布
| Site ID | 名称 | 井数 |
|---------|------|------|
| Q4r6BEy4CF | ZY-547H1 平台 | 约 15 口 |
| 36yPxcTHRK | ZY-567 平台 | 约 10 口 |
| rulwyXooko | ZY-558 平台 | 约 5 口 |

### 1.3 井列表（共约 28 口）
ZY-545H1, ZY-545H2, ZY-545H3, ZY-545H4, ZY-547, ZY-547H1,
ZY-540, ZY-541, ZY-546, ZY-558, ZY-558H1, ZY-558H2, ZY-558H4,
ZY-560, ZY-561, ZY-564, ZY-565, ZY-568, ZY-168, ZY-169,
TS-008, TS-520, TS-521, TS-522, TS-548, TS-555,
SY-558H3, SY-567H1, SY-567H2

### 1.4 发现的问题

**1) ZY-545H1 重复**
`
well_id= CSSrZ48h6l ⇒ slot 坐标 (slot_ew=-1444, slot_ns=-1981)
well_id=JLKxMJlvfU ⇒ 独立坐标 (slot_ew=0, slot_ns=0)
`
两个不同 well_id 都叫 ZY-545H1，数据冗余。

**2) 井名前后有空格**
- TS-522: slot_name= TS-522（前面多空格）
- ZY-169: well_common_name= ZY-169（前面多空格）
- 545H4 (well_id=pYE817Yb2b): wellbore_name=545H4 缺 ZY- 前缀

**3) 没有 Offset Well**
全文件搜索不到 <CD_OFFSET_WELL> 标签。
所有井都是设计井，没有作为老井引用的独立 Well 实体。

### 1.5 数据结构特征
- 每口 Well 对应一个 Wellbore
- 测斜数据：设计轨迹存为 survey_type=100 (Plan/Design)
- 测斜工具：MWD std + ISCWSA 误差模型
- 防碰规则：Level 1 (SF=1.0), Level 2 (SF=1.25), Level 3 (SF=1.5)

## 二、长城钻探项目（已分析的旧文件）

### 2.1 主要问题
- **数据库结构错误**：只有一口井（辽河275CH），缺少独立的老井实体
- 老井的测斜数据直接挂在该井的第二个 wellbore 下
- 后果：防碰扫描时 Offset Well 无独立误差模型 → SMA=0

### 2.2 教训
老井必须作为独立 Well 存在，不能和设计井混在同一个 Well 下。

## 三、纯梁采油厂 LC53 井

### 3.1 基本信息
- 数据库版本较旧：EDM 5000.1.9
- 坐标系统：Gauss-Kruger (Pulkovo 1942) GK Zone 20
- 单井设计，结构相对简单

### 3.2 结构分析
- Well → Wellbore → Survey 结构完整
- 版本过旧，无法直接在新版 COMPASS 5000.17 中打开（需 EDM 升级）

## 四、XML 字段速查表

### CD_WELL_ALL (井)
| 属性 | 类型 | 说明 |
|------|------|------|
| well_id | string | 唯一标识 |
| well_common_name | string | 井名 |
| site_id | string | 所属平台 |
| coord_type | int | 0=槽口, 1=经纬度, 2=地图投影 |
| slot_ew | double | 槽口东西偏移 (m) |
| slot_ns | double | 槽口南北偏移 (m) |
| slot_radial_error | double | 槽口径向误差 |
| water_depth | double | 水深 (m) |
| convergence | double | 子午线收敛角 |
| is_subsea | Y/N | 是否水下 |
| scale_factor | double | 比例因子 |

### CD_WELLBORE (井眼)
| 属性 | 说明 |
|------|------|
| wellbore_name | 井眼名（通常与井名一致） |
| ko_md | 造斜点 MD |
| ko_tvd | 造斜点 TVD |
| bh_md / bh_tvd | 井底 MD/TVD |
| is_deviated | Y=定向井, N=直井 |

### CD_SURVEY_HEADER (测斜段)
| 属性 | 说明 |
|------|------|
| survey_type | 0=Actual, 100=Design, 200=Lookahead |
| phase | PLAN / PROTOTYPE |
| survey_name | 测斜段名称 |
| survey_tool_id | 测斜工具 |
| md_min / md_max | MD 范围 |
| tie_on_type | 0=地表, 1=上一段 |
| tie_on_depth | 连接深度 |

### CD_SURVEY_STATION (测斜点)
| 属性 | 说明 |
|------|------|
| md | 测量深度 |
| inclination | 井斜角 (°) |
| azimuth | 方位角 (°) |
| tvd | 垂深 |
| offset_east / offset_north | 东西/南北偏移 |
| dogleg_severity | 狗腿度 (°/30m) |
| build_rate / turn_rate | 造斜率/转向率 |
| sequence_no | 序号 |
| station_type | 0=测点 |
