# 个股筛选模块开发指南

> **本文档用于GPT深度研究，指导个股筛选模块的完整开发**

## 📋 目录

1. [模块概述](#模块概述)
2. [系统架构](#系统架构)
3. [数据流程](#数据流程)
4. [核心功能设计](#核心功能设计)
5. [数据源与API](#数据源与API)
6. [评分模型](#评分模型)
7. [实现步骤](#实现步骤)
8. [代码结构](#代码结构)
9. [测试与验证](#测试与验证)
10. [参考文档](#参考文档)

---

## 1. 模块概述

### 1.1 功能定位

个股筛选模块是"投资主线"工作流的第三步，位于"主线识别"和"热度评分"之后：

```
主线识别 → 热度评分 → **个股筛选** → 调研验证 → 回测验证
```

**核心功能**：
- 从高热度主线板块中筛选优质个股
- 多维打分：技术面 + 资金面 + 基本面
- 综合评分：主线热度权重 + 个股因子权重
- 生成股票池，供后续策略开发和回测使用

### 1.2 业务逻辑

```
1. 读取热度评分结果（latest_heatmap_scores.json）
   ↓
2. 筛选高热度主线（≥60分）
   ↓
3. 获取主线内的个股列表
   ↓
4. 获取个股多维度数据（技术/资金/基本面）
   ↓
5. 计算个股综合得分：
   综合得分 = 所属主线热度 × 15% + 个股因子 × 85%
   其中：个股因子 = 30%×技术分 + 30%×资金分 + 40%×基本面分
   ↓
6. 排序并展示Top N
   ↓
7. 支持导出股票池、生成策略、加入观察池
```

### 1.3 与前后模块的衔接

**前置依赖**：
- ✅ 主线识别模块：提供板块/概念列表
- ✅ 热度评分模块：提供主线热度分数（保存在 `~/.local/share/jqquant/reports/heatmap/latest_heatmap_scores.json`）

**后续输出**：
- 股票池JSON文件（供策略开发模块使用）
- 观察池列表（供实时监控模块使用）
- 策略代码生成（供回测验证模块使用）

---

## 2. 系统架构

### 2.1 模块结构

```
markets/ashare/mainline/
├── stock_selection_engine.py      # 核心评分引擎
├── stock_data_fetcher.py          # 个股数据获取器
└── stock_selection_report.py      # 报告生成器

gui/widgets/
└── stock_selection_panel.py        # GUI面板（已存在框架，需完善）

reports/
└── stock_selection/                # 报告目录
    ├── stock_pool_YYYYMMDD.json   # 股票池JSON
    └── selection_report_*.html     # HTML报告
```

### 2.2 核心类设计

#### 2.2.1 StockSelectionEngine（评分引擎）

```python
class StockSelectionEngine:
    """个股筛选评分引擎"""
    
    def __init__(self, data_source: str = "akshare"):
        """
        初始化引擎
        
        Args:
            data_source: 数据源类型 ("akshare", "jqdata", "wind")
        """
        self.data_source = data_source
        self.data_fetcher = StockDataFetcher(data_source)
        
    def calculate_tech_score(self, stock_code: str) -> float:
        """计算技术面得分（0-100）"""
        # 因子：均线系统、量价关系、技术形态、动量指标
        pass
    
    def calculate_fund_score(self, stock_code: str) -> float:
        """计算资金面得分（0-100）"""
        # 因子：资金流入、主力动向、北向资金、换手率
        pass
    
    def calculate_basic_score(self, stock_code: str) -> float:
        """计算基本面得分（0-100）"""
        # 因子：ROE、营收增速、净利润增速、估值水平
        pass
    
    def calculate_composite_score(
        self, 
        stock_code: str, 
        mainline_heat: float
    ) -> StockScore:
        """
        计算综合得分
        
        Args:
            stock_code: 股票代码
            mainline_heat: 所属主线热度（0-100）
        
        Returns:
            StockScore对象，包含各维度得分和综合得分
        """
        tech = self.calculate_tech_score(stock_code)
        fund = self.calculate_fund_score(stock_code)
        basic = self.calculate_basic_score(stock_code)
        
        # 个股因子得分
        stock_factor = 0.3 * tech + 0.3 * fund + 0.4 * basic
        
        # 综合得分（主线热度15% + 个股因子85%）
        composite = 0.15 * mainline_heat + 0.85 * stock_factor
        
        return StockScore(
            code=stock_code,
            tech_score=tech,
            fund_score=fund,
            basic_score=basic,
            stock_factor=stock_factor,
            mainline_heat=mainline_heat,
            composite_score=composite
        )
    
    def screen_stocks(
        self,
        sector_name: str,
        mainline_heat: float,
        filters: Dict[str, Any]
    ) -> List[StockScore]:
        """
        筛选个股
        
        Args:
            sector_name: 板块/概念名称
            mainline_heat: 主线热度
            filters: 筛选条件（市值范围、排除ST等）
        
        Returns:
            排序后的股票评分列表
        """
        # 1. 获取板块内个股列表
        stocks = self.data_fetcher.get_stocks_in_sector(sector_name)
        
        # 2. 应用基础筛选（市值、ST、停牌等）
        stocks = self._apply_filters(stocks, filters)
        
        # 3. 计算每只股票的得分
        scores = []
        for stock in stocks:
            score = self.calculate_composite_score(stock.code, mainline_heat)
            scores.append(score)
        
        # 4. 排序
        scores.sort(key=lambda x: x.composite_score, reverse=True)
        
        return scores
```

#### 2.2.2 StockDataFetcher（数据获取器）

```python
class StockDataFetcher:
    """个股数据获取器"""
    
    def __init__(self, data_source: str = "akshare"):
        self.data_source = data_source
        
    def get_stocks_in_sector(self, sector_name: str) -> List[StockInfo]:
        """
        获取板块/概念内的个股列表
        
        Args:
            sector_name: 板块或概念名称（如"新能源汽车"、"半导体"）
        
        Returns:
            股票信息列表
        """
        # AKShare API: ak.stock_board_concept_cons_em()
        # 或: ak.stock_board_industry_cons_em()
        pass
    
    def get_tech_data(self, stock_code: str) -> TechData:
        """
        获取技术面数据
        
        Returns:
            TechData: 均线、量价、技术指标等
        """
        # 数据项：
        # - 价格数据（开高低收）
        # - 成交量、成交额
        # - 均线系统（MA5/10/20/60）
        # - MACD、RSI、KDJ等
        pass
    
    def get_fund_data(self, stock_code: str) -> FundData:
        """
        获取资金面数据
        
        Returns:
            FundData: 资金流向、主力动向等
        """
        # 数据项：
        # - 主力资金净流入
        # - 北向资金持仓
        # - 换手率
        # - 龙虎榜数据
        pass
    
    def get_basic_data(self, stock_code: str) -> BasicData:
        """
        获取基本面数据
        
        Returns:
            BasicData: 财务指标、估值等
        """
        # 数据项：
        # - ROE、ROA
        # - 营收增速、净利润增速
        # - PE、PB、PS
        # - 市值
        pass
```

---

## 3. 数据流程

### 3.1 完整数据流

```
┌─────────────────────────────────────────────────────────────┐
│  1. 读取热度评分结果                                          │
│     ~/.local/share/jqquant/reports/heatmap/                  │
│     latest_heatmap_scores.json                               │
│     ↓                                                         │
│  2. 筛选高热度主线（≥60分）                                   │
│     ↓                                                         │
│  3. 用户选择主线 → 获取主线热度分数                           │
│     ↓                                                         │
│  4. 获取主线内个股列表                                        │
│     AKShare: ak.stock_board_concept_cons_em()                │
│     ↓                                                         │
│  5. 批量获取个股数据（异步）                                   │
│     - 技术面：价格、成交量、技术指标                          │
│     - 资金面：资金流向、主力动向                              │
│     - 基本面：财务指标、估值                                  │
│     ↓                                                         │
│  6. 计算个股得分                                              │
│     - 技术分（30%）                                           │
│     - 资金分（30%）                                           │
│     - 基本面分（40%）                                         │
│     - 综合分 = 主线热度×15% + 个股因子×85%                   │
│     ↓                                                         │
│  7. 排序并展示Top N                                           │
│     ↓                                                         │
│  8. 导出股票池JSON                                            │
│     ~/.local/share/jqquant/reports/stock_selection/          │
│     stock_pool_YYYYMMDD.json                                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 数据缓存策略

- **个股基础信息**：缓存到MongoDB（板块成分股列表）
- **技术面数据**：实时获取（价格、成交量）
- **资金面数据**：实时获取（资金流向）
- **基本面数据**：缓存到MongoDB（财务数据更新频率低）

---

## 4. 核心功能设计

### 4.1 筛选条件

**基础筛选**：
- ✅ 市值范围（最小-最大，单位：亿元）
- ✅ 排除ST/*ST股票
- ✅ 排除停牌股票
- ✅ 日均成交额 > 1000万

**高级筛选**（可选）：
- 技术面筛选：均线多头排列、突破关键位等
- 资金面筛选：主力净流入 > 0、北向资金增持等
- 基本面筛选：ROE > 15%、营收增速 > 20%等

### 4.2 评分维度

#### 4.2.1 技术面评分（30%权重）

**因子构成**：
1. **均线系统**（30%）
   - MA5 > MA10 > MA20：多头排列
   - 价格 > MA20：趋势向上
   - MA5斜率：短期动量

2. **量价关系**（25%）
   - 成交量放大：资金关注度高
   - 价涨量增：健康上涨
   - 换手率：流动性指标

3. **技术形态**（25%）
   - 突破关键位：阻力位突破
   - K线形态：看涨形态识别
   - 趋势强度：RSI、MACD等

4. **动量指标**（20%）
   - 短期涨幅：5日/10日涨幅
   - 相对强度：相对大盘表现
   - 动量持续性：连续上涨天数

**计算公式**：
```python
tech_score = (
    0.30 * ma_score +      # 均线系统
    0.25 * volume_score +  # 量价关系
    0.25 * pattern_score + # 技术形态
    0.20 * momentum_score   # 动量指标
)
```

#### 4.2.2 资金面评分（30%权重）

**因子构成**：
1. **主力资金**（40%）
   - 主力净流入：大单资金流向
   - 主力占比：主力成交占比
   - 资金持续性：连续流入天数

2. **北向资金**（30%）
   - 北向持仓：持仓市值
   - 北向增持：近期增持幅度
   - 北向占比：占流通盘比例

3. **龙虎榜**（20%）
   - 上榜次数：近期上榜频率
   - 净买入额：游资净买入
   - 机构席位：机构参与度

4. **换手率**（10%）
   - 换手率水平：活跃度指标
   - 换手率变化：关注度变化

**计算公式**：
```python
fund_score = (
    0.40 * main_fund_score +    # 主力资金
    0.30 * north_fund_score +    # 北向资金
    0.20 * lhb_score +           # 龙虎榜
    0.10 * turnover_score         # 换手率
)
```

#### 4.2.3 基本面评分（40%权重）

**因子构成**：
1. **盈利能力**（35%）
   - ROE：净资产收益率
   - ROA：总资产收益率
   - 净利润率：盈利质量

2. **成长性**（35%）
   - 营收增速：收入增长
   - 净利润增速：利润增长
   - 营收质量：营收稳定性

3. **估值水平**（20%）
   - PE：市盈率（相对合理）
   - PB：市净率
   - PEG：成长性估值

4. **财务健康**（10%）
   - 负债率：财务杠杆
   - 现金流：经营现金流
   - 资产质量：资产结构

**计算公式**：
```python
basic_score = (
    0.35 * profit_score +    # 盈利能力
    0.35 * growth_score +     # 成长性
    0.20 * valuation_score +  # 估值水平
    0.10 * health_score       # 财务健康
)
```

### 4.3 综合得分计算

```python
# 第一步：计算个股因子得分
stock_factor = (
    0.30 * tech_score +   # 技术面30%
    0.30 * fund_score +   # 资金面30%
    0.40 * basic_score    # 基本面40%
)

# 第二步：结合主线热度
composite_score = (
    0.15 * mainline_heat +  # 主线热度15%
    0.85 * stock_factor     # 个股因子85%
)
```

**设计理念**：
- 主线热度权重较低（15%），因为主线只是筛选范围，个股质量更重要
- 个股因子中基本面权重最高（40%），因为基本面决定长期价值
- 技术面和资金面各30%，反映短期市场表现

---

## 5. 数据源与API

### 5.1 AKShare数据源（当前使用）

#### 5.1.1 板块成分股

```python
import akshare as ak

# 概念板块成分股
df = ak.stock_board_concept_cons_em(symbol="新能源汽车")
# 返回：代码、名称、最新价、涨跌幅等

# 行业板块成分股
df = ak.stock_board_industry_cons_em(symbol="半导体")
```

#### 5.1.2 个股技术面数据

```python
# 历史K线数据
df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241201",
    adjust="qfq"  # 前复权
)
# 返回：日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率

# 实时行情
df = ak.stock_zh_a_spot_em()
# 返回：代码、名称、最新价、涨跌幅、成交量、成交额、换手率等
```

#### 5.1.3 个股资金面数据

```python
# 个股资金流向
df = ak.stock_individual_fund_flow_rank(indicator="今日")
# 返回：代码、名称、主力净流入、超大单、大单、中单、小单

# 北向资金持仓
df = ak.stock_hsgt_fund_flow_summary_em()
# 返回：日期、沪股通、深股通、合计

# 龙虎榜
df = ak.stock_lhb_detail_em(start_date="20241201", end_date="20241201")
# 返回：代码、名称、买入额、卖出额、净买入额
```

#### 5.1.4 个股基本面数据

```python
# 财务指标（需要TuShare Pro或聚宽）
# AKShare暂不支持，需要：
# 1. 使用聚宽JQData（推荐）
# 2. 使用TuShare Pro（需要积分）
# 3. 使用Wind（需要授权）
```

### 5.2 JQData数据源（推荐，需配置）

#### 5.2.1 财务数据

```python
from jqdata import *

# 查询财务指标
q = query(
    indicator.code,
    indicator.roe,           # ROE
    indicator.roa,          # ROA
    indicator.net_profit_margin,  # 净利润率
    indicator.inc_total_revenue_year_on_year,  # 营收增速
    indicator.inc_net_profit_year_on_year,     # 净利润增速
).filter(
    indicator.code.in_(['000001.XSHE', '600000.XSHG'])
)

df = finance.run_query(q)
```

#### 5.2.2 估值数据

```python
# 查询估值指标
q = query(
    valuation.code,
    valuation.pe_ratio,     # PE
    valuation.pb_ratio,      # PB
    valuation.market_cap,   # 总市值
).filter(
    valuation.code.in_(['000001.XSHE', '600000.XSHG'])
)

df = get_fundamentals(q, date='2024-12-01')
```

### 5.3 数据源选择策略

**当前阶段（AKShare）**：
- ✅ 技术面数据：完整可用
- ✅ 资金面数据：完整可用
- ⚠️ 基本面数据：部分可用（需要补充）

**下一阶段（JQData）**：
- ✅ 技术面数据：完整可用
- ✅ 资金面数据：完整可用
- ✅ 基本面数据：完整可用（推荐）

**未来（Wind）**：
- ✅ 所有数据：完整可用（机构级）

---

## 6. 评分模型

### 6.1 技术面评分详细算法

#### 6.1.1 均线系统得分（0-100）

```python
def calculate_ma_score(price_data):
    """
    计算均线系统得分
    
    规则：
    - MA5 > MA10 > MA20：多头排列（60分基础分）
    - 价格 > MA20：趋势向上（+20分）
    - MA5斜率 > 0：短期动量（+20分）
    - 均线间距：均线分散度（+0-20分）
    """
    ma5 = price_data['close'].rolling(5).mean()
    ma10 = price_data['close'].rolling(10).mean()
    ma20 = price_data['close'].rolling(20).mean()
    
    score = 0
    
    # 多头排列（60分）
    if ma5.iloc[-1] > ma10.iloc[-1] > ma20.iloc[-1]:
        score += 60
    
    # 趋势向上（20分）
    if price_data['close'].iloc[-1] > ma20.iloc[-1]:
        score += 20
    
    # 短期动量（20分）
    ma5_slope = (ma5.iloc[-1] - ma5.iloc[-5]) / ma5.iloc[-5]
    if ma5_slope > 0:
        score += 20
    
    return min(score, 100)
```

#### 6.1.2 量价关系得分（0-100）

```python
def calculate_volume_score(price_data, volume_data):
    """
    计算量价关系得分
    
    规则：
    - 价涨量增：健康上涨（40分）
    - 成交量放大：资金关注（30分）
    - 换手率：流动性（30分）
    """
    score = 0
    
    # 价涨量增（40分）
    price_change = price_data['close'].pct_change()
    volume_change = volume_data['volume'].pct_change()
    if price_change.iloc[-1] > 0 and volume_change.iloc[-1] > 0:
        score += 40
    
    # 成交量放大（30分）
    avg_volume = volume_data['volume'].rolling(20).mean()
    if volume_data['volume'].iloc[-1] > avg_volume.iloc[-1] * 1.2:
        score += 30
    
    # 换手率（30分）
    turnover = volume_data.get('turnover', 0)
    if turnover > 3:  # 换手率>3%
        score += 30
    elif turnover > 1:
        score += 15
    
    return min(score, 100)
```

### 6.2 资金面评分详细算法

#### 6.2.1 主力资金得分（0-100）

```python
def calculate_main_fund_score(fund_data):
    """
    计算主力资金得分
    
    规则：
    - 主力净流入 > 0：资金流入（50分）
    - 主力净流入金额：流入规模（30分）
    - 连续流入天数：持续性（20分）
    """
    score = 0
    
    # 资金流入（50分）
    net_inflow = fund_data.get('main_net_inflow', 0)
    if net_inflow > 0:
        score += 50
    
    # 流入规模（30分）
    if net_inflow > 100000000:  # >1亿
        score += 30
    elif net_inflow > 50000000:  # >5000万
        score += 20
    elif net_inflow > 10000000:  # >1000万
        score += 10
    
    # 持续性（20分）
    consecutive_days = fund_data.get('consecutive_inflow_days', 0)
    if consecutive_days >= 5:
        score += 20
    elif consecutive_days >= 3:
        score += 10
    
    return min(score, 100)
```

### 6.3 基本面评分详细算法

#### 6.3.1 盈利能力得分（0-100）

```python
def calculate_profit_score(financial_data):
    """
    计算盈利能力得分
    
    规则：
    - ROE > 20%：优秀（40分）
    - ROE > 15%：良好（30分）
    - ROE > 10%：一般（20分）
    - 净利润率：盈利质量（30分）
    """
    score = 0
    
    roe = financial_data.get('roe', 0)
    if roe > 20:
        score += 40
    elif roe > 15:
        score += 30
    elif roe > 10:
        score += 20
    
    net_margin = financial_data.get('net_profit_margin', 0)
    if net_margin > 20:
        score += 30
    elif net_margin > 15:
        score += 20
    elif net_margin > 10:
        score += 10
    
    return min(score, 100)
```

---

## 7. 实现步骤

### 阶段1：数据获取器开发（2-3天）

**任务清单**：
1. ✅ 创建 `stock_data_fetcher.py`
2. ✅ 实现 `get_stocks_in_sector()` - 获取板块成分股
3. ✅ 实现 `get_tech_data()` - 获取技术面数据
4. ✅ 实现 `get_fund_data()` - 获取资金面数据
5. ⚠️ 实现 `get_basic_data()` - 获取基本面数据（需要JQData或Wind）
6. ✅ 添加数据缓存（MongoDB）
7. ✅ 添加错误处理和降级策略

**验收标准**：
- 能够获取任意板块/概念的成分股列表
- 能够获取个股的技术面、资金面数据
- 数据获取失败时有降级策略（使用缓存或估算）

### 阶段2：评分引擎开发（3-4天）

**任务清单**：
1. ✅ 创建 `stock_selection_engine.py`
2. ✅ 实现技术面评分算法
3. ✅ 实现资金面评分算法
4. ⚠️ 实现基本面评分算法（需要财务数据）
5. ✅ 实现综合得分计算
6. ✅ 实现筛选逻辑（市值、ST、停牌等）
7. ✅ 添加评分结果数据类（StockScore）

**验收标准**：
- 能够计算每只股票的技术面、资金面、基本面得分
- 能够计算综合得分（含主线热度权重）
- 筛选逻辑正确（排除ST、停牌等）

### 阶段3：GUI面板完善（2-3天）

**任务清单**：
1. ✅ 完善 `mainline_panel.py` 中的 `_create_stock_selection_tab()`
2. ✅ 实现 `_screen_stocks()` - 筛选按钮逻辑
3. ✅ 实现数据获取进度显示（异步）
4. ✅ 实现结果表格展示
5. ✅ 实现"加入观察池"功能
6. ✅ 实现"生成策略"功能
7. ✅ 实现报告生成和导出

**验收标准**：
- UI界面完整，交互流畅
- 数据获取不阻塞UI（异步）
- 结果展示清晰（表格+图表）
- 支持导出股票池JSON

### 阶段4：报告生成（1-2天）

**任务清单**：
1. ✅ 创建 `stock_selection_report.py`
2. ✅ 实现HTML报告生成
3. ✅ 实现股票池JSON导出
4. ✅ 报告自动打开（浏览器+文件管理器）

**验收标准**：
- HTML报告美观、信息完整
- JSON格式规范，供后续模块使用
- 报告自动打开功能正常

### 阶段5：测试与优化（2-3天）

**任务清单**：
1. ✅ 单元测试（数据获取、评分算法）
2. ✅ 集成测试（完整流程）
3. ✅ 性能优化（批量数据获取、缓存）
4. ✅ 错误处理完善
5. ✅ 文档完善

**验收标准**：
- 所有测试通过
- 性能满足要求（100只股票筛选 < 30秒）
- 错误处理完善（网络失败、数据缺失等）

---

## 8. 代码结构

### 8.1 文件组织

```
markets/ashare/mainline/
├── stock_selection_engine.py      # 评分引擎（核心）
├── stock_data_fetcher.py           # 数据获取器
├── stock_selection_report.py       # 报告生成器
└── models.py                       # 数据模型（StockScore等）

gui/widgets/
└── stock_selection_panel.py        # GUI面板（完善现有代码）

reports/
└── stock_selection/
    ├── stock_pool_YYYYMMDD.json   # 股票池JSON
    └── selection_report_*.html     # HTML报告
```

### 8.2 核心类定义

#### 8.2.1 StockScore（数据模型）

```python
@dataclass
class StockScore:
    """股票评分结果"""
    code: str                    # 股票代码
    name: str                    # 股票名称
    sector: str                  # 所属板块
    mainline_heat: float         # 主线热度
    
    # 各维度得分
    tech_score: float            # 技术面得分（0-100）
    fund_score: float            # 资金面得分（0-100）
    basic_score: float           # 基本面得分（0-100）
    
    # 综合得分
    stock_factor: float          # 个股因子得分
    composite_score: float       # 综合得分
    
    # 附加信息
    market_cap: float           # 市值（亿元）
    price_change: float          # 涨跌幅（%）
    turnover: float             # 换手率（%）
    
    # 时间戳
    timestamp: datetime = field(default_factory=datetime.now)
```

#### 8.2.2 StockDataFetcher（数据获取器）

```python
class StockDataFetcher:
    """个股数据获取器"""
    
    def __init__(self, data_source: str = "akshare"):
        self.data_source = data_source
        self.cache = MongoDBCache()  # MongoDB缓存
        
    def get_stocks_in_sector(self, sector_name: str) -> List[StockInfo]:
        """获取板块成分股"""
        # 1. 先查缓存
        cached = self.cache.get_sector_stocks(sector_name)
        if cached:
            return cached
        
        # 2. 调用API
        if self.data_source == "akshare":
            df = ak.stock_board_concept_cons_em(symbol=sector_name)
            # 或: ak.stock_board_industry_cons_em(symbol=sector_name)
        
        # 3. 转换为StockInfo列表
        stocks = [StockInfo(code=row['代码'], name=row['名称']) 
                  for _, row in df.iterrows()]
        
        # 4. 缓存结果
        self.cache.save_sector_stocks(sector_name, stocks)
        
        return stocks
    
    def get_tech_data(self, stock_code: str) -> TechData:
        """获取技术面数据"""
        # 获取K线数据
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=(datetime.now() - timedelta(days=60)).strftime("%Y%m%d"),
            end_date=datetime.now().strftime("%Y%m%d"),
            adjust="qfq"
        )
        
        return TechData(
            close_prices=df['收盘'].tolist(),
            volumes=df['成交量'].tolist(),
            turnover=df['换手率'].iloc[-1] if '换手率' in df.columns else 0,
            # ... 其他技术指标
        )
    
    def get_fund_data(self, stock_code: str) -> FundData:
        """获取资金面数据"""
        # 获取资金流向
        df = ak.stock_individual_fund_flow_rank(indicator="今日")
        stock_data = df[df['代码'] == stock_code]
        
        return FundData(
            main_net_inflow=stock_data['主力净流入'].iloc[0] if not stock_data.empty else 0,
            # ... 其他资金数据
        )
    
    def get_basic_data(self, stock_code: str) -> BasicData:
        """获取基本面数据"""
        # 需要JQData或Wind
        if self.data_source == "jqdata":
            # 使用JQData查询财务数据
            pass
        elif self.data_source == "wind":
            # 使用Wind查询财务数据
            pass
        else:
            # AKShare暂不支持，返回估算值或提示
            return BasicData(roe=0, roa=0, ...)  # 默认值
```

---

## 9. 测试与验证

### 9.1 单元测试

```python
# tests/test_stock_selection_engine.py

def test_calculate_tech_score():
    """测试技术面评分"""
    engine = StockSelectionEngine()
    score = engine.calculate_tech_score("000001")
    assert 0 <= score <= 100

def test_calculate_composite_score():
    """测试综合得分计算"""
    engine = StockSelectionEngine()
    result = engine.calculate_composite_score("000001", mainline_heat=80)
    assert result.composite_score == 0.15 * 80 + 0.85 * result.stock_factor
```

### 9.2 集成测试

```python
def test_full_screening_flow():
    """测试完整筛选流程"""
    # 1. 读取热度评分
    heatmap_path = Path.home() / ".local/share/jqquant/reports/heatmap/latest_heatmap_scores.json"
    with open(heatmap_path) as f:
        heatmap_data = json.load(f)
    
    # 2. 选择高热度主线
    high_heat = [s for s in heatmap_data['scores'] if s['total_score'] >= 60]
    assert len(high_heat) > 0
    
    # 3. 筛选个股
    engine = StockSelectionEngine()
    results = engine.screen_stocks(
        sector_name=high_heat[0]['name'],
        mainline_heat=high_heat[0]['total_score'],
        filters={'exclude_st': True, 'market_cap_min': 0, 'market_cap_max': 1000}
    )
    
    # 4. 验证结果
    assert len(results) > 0
    assert all(r.composite_score >= 0 for r in results)
    assert results[0].composite_score >= results[-1].composite_score  # 已排序
```

---

## 10. 参考文档

### 10.1 项目内文档

- `docs/REVIEW_CHECKLIST.md` - 主线识别与热度评分检阅清单
- `docs/HEATMAP_SYSTEM_ARCHITECTURE.md` - 热度评分系统架构
- `docs/FIVE_DIMENSION_TASK_BREAKDOWN.md` - 五维评分系统任务分解
- `docs/DATA_SOURCE_INTEGRATION.md` - 数据源集成文档

### 10.2 外部参考

- AKShare文档：https://akshare.readthedocs.io/
- JQData文档：https://www.joinquant.com/help/api/help
- 聚宽研究平台：https://www.joinquant.com/research

### 10.3 设计原则

1. **数据源透明**：明确每个数据项的来源、API、可靠性
2. **降级策略**：数据获取失败时有备用方案
3. **异步处理**：数据获取不阻塞UI
4. **缓存机制**：减少API调用，提高性能
5. **错误处理**：完善的异常处理和用户提示

---

## 11. 开发注意事项

### 11.1 数据源优先级

1. **当前阶段**：AKShare（免费，技术面+资金面完整）
2. **下一阶段**：JQData（付费，基本面数据完整）
3. **未来**：Wind（机构级，所有数据完整）

### 11.2 性能优化

- **批量获取**：一次获取多只股票数据，减少API调用
- **缓存策略**：基本面数据缓存时间较长（季度更新）
- **异步处理**：使用QThread进行数据获取，不阻塞UI

### 11.3 错误处理

- **网络失败**：使用缓存数据或提示用户
- **数据缺失**：使用默认值或跳过该项评分
- **API变更**：版本检测和降级处理

---

## 12. 下一步行动

1. **立即开始**：创建 `stock_data_fetcher.py`，实现板块成分股获取
2. **本周完成**：完成数据获取器和评分引擎核心功能
3. **下周完成**：完善GUI面板和报告生成
4. **持续优化**：根据使用反馈优化评分算法和UI体验

---

*文档版本：v1.0*  
*最后更新：2024-11-29*  
*维护者：韬睿量化开发团队*

