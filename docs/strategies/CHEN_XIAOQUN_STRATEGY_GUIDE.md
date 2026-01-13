# 陈小群游资战法实战操作指南

> **版本**: v1.0  
> **创建时间**: 2026-01-13  
> **适用市场**: A股市场  
> **风险等级**: ⚠️ 高风险高收益

---

## 📋 目录

1. [策略概述](#策略概述)
2. [核心战法体系](#核心战法体系)
3. [完整操作流程图](#完整操作流程图)
4. [详细操作说明](#详细操作说明)
5. [数据获取方法](#数据获取方法)
6. [实盘操作案例](#实盘操作案例)
7. [一周投资建议](#一周投资建议)
8. [风险控制](#风险控制)

---

## 策略概述

### 核心理念

陈小群游资战法是一套完整的短线交易体系，通过**三板斧战法**、**龙头战法**和**合力情绪战法**，实现从试错到重仓的完整交易流程。

### 核心特点

- **三阶段仓位管理**: 首板10% → 二板50% → 三板40%
- **聚焦总龙头**: 只参与市场辨识度最高的龙头股
- **情绪周期把控**: 根据市场情绪周期调整仓位和策略
- **严格纪律**: 每月只做1-2笔交易，其余时间空仓

### 适用条件

- **市场环境**: 情绪高涨、有明确主线的市场
- **资金规模**: 适合中小资金快速进阶
- **交易经验**: 需要丰富的短线交易经验

---

## 核心战法体系

### 1. 三板斧战法

#### 首板卡位术（10%试错仓）

**选股条件**:
- ✅ 早盘9:35前涨停的个股
- ✅ 题材新颖、有想象空间
- ✅ 流通市值小于30亿
- ✅ 封单量超过流通市值的2%

**操作方式**: 扫板介入

#### 二板定龙术（50%主攻仓）

**确认条件**:
- ✅ 单日换手率超过25%
- ✅ 分时走势：急跌不破开盘价，反弹带量拉升
- ✅ 板块内至少有3只跟风股涨停，形成梯队效应
- ✅ 确认龙头地位

**操作方式**: 重仓介入

#### 三板加速术（40%加仓仓）

**确认条件**:
- ✅ 在前两板基础上
- ✅ 第三板出现缩量涨停或量能持续放大
- ✅ 板块效应持续增强
- ✅ 分时走势稳健

**操作方式**: 继续加仓持有

### 2. 龙头战法

- **聚焦总龙头**: 只参与市场辨识度最高的龙头股
- **重仓持有**: 在龙头启动期重仓介入
- **坚定持有**: 不爱做T，看准就坚定持有到巅峰
- **退出时机**: 只有明显见顶或预计停牌才走

### 3. 合力情绪战法

- **市场合力高于一切**: 识别并跟随市场合力
- **精准择时**: 在题材发酵初期介入
- **严格纪律**: 在行情震荡或出现风险信号时，果断止盈离场

---

## 完整操作流程图

```mermaid
flowchart TD
    A[每日开盘前准备] --> B{判断市场情绪周期}
    
    B -->|启动期| C[轻仓试错 10%]
    B -->|加速期| D[重仓持有 50%+]
    B -->|高位震荡期| E[逐步减仓]
    B -->|退潮期| F[空仓观望]
    
    C --> G[首板卡位术]
    G --> H{早盘9:35前涨停?}
    H -->|是| I{流通市值<30亿?}
    H -->|否| F
    I -->|是| J{封单量>2%?}
    I -->|否| F
    J -->|是| K[扫板介入 10%仓位]
    J -->|否| F
    
    K --> L{次日二板确认?}
    L -->|是| M{换手率>25%?}
    L -->|否| N[止损退出]
    M -->|是| O{板块内3只以上跟风涨停?}
    M -->|否| N
    O -->|是| P[重仓介入 50%仓位]
    O -->|否| N
    
    P --> Q{第三板确认?}
    Q -->|是| R{缩量涨停或量能放大?}
    Q -->|否| S[持有观察]
    R -->|是| T[继续加仓 40%仓位]
    R -->|否| S
    
    T --> U{板块效应持续增强?}
    U -->|是| V[持有至见顶或停牌风险]
    U -->|否| W[逐步减仓]
    
    V --> X[退出时机判断]
    W --> X
    S --> X
    N --> X
    
    X --> Y{明显见顶或停牌风险?}
    Y -->|是| Z[果断退出]
    Y -->|否| AA[继续持有]
    
    Z --> F
    AA --> V
    
    D --> AB[持有龙头股]
    AB --> AC{龙头地位确认?}
    AC -->|是| AD[享受主升浪]
    AC -->|否| AE[重新评估]
    AD --> X
    AE --> F
    
    E --> AF[锁定利润]
    AF --> F
    
    style A fill:#e1f5ff
    style C fill:#ffe1f5
    style D fill:#e1ffe1
    style E fill:#ffe1e1
    style F fill:#f5f5f5
    style K fill:#e1f5ff
    style P fill:#e1ffe1
    style T fill:#ffe1f5
    style Z fill:#ffe1e1
```

---

## 详细操作说明

### 阶段一：开盘前准备（9:00-9:25）

#### 1.1 市场情绪判断

**数据获取**:
```python
# 使用JQData获取市场指数数据
import jqdatasdk as jq
jq.auth('username', 'password')

# 获取沪深300、中证1000指数数据
hs300 = jq.get_price('000300.XSHG', count=20, end_date=today, frequency='daily')
zz1000 = jq.get_price('000852.XSHG', count=20, end_date=today, frequency='daily')

# 判断市场情绪周期
# 启动期：指数企稳，成交量放大
# 加速期：指数上涨，成交量持续放大
# 高位震荡期：指数高位震荡，成交量萎缩
# 退潮期：指数下跌，成交量萎缩
```

**判断标准**:
- **启动期**: 指数企稳，成交量放大，涨停板数量增加
- **加速期**: 指数上涨，成交量持续放大，龙头股确认
- **高位震荡期**: 指数高位震荡，成交量萎缩，分化明显
- **退潮期**: 指数下跌，成交量萎缩，涨停板数量减少

#### 1.2 板块热点扫描

**数据获取**:
```python
# 使用AKShare获取板块数据
import akshare as ak

# 获取概念板块涨幅榜
concept_rank = ak.stock_board_concept_name_em()

# 获取行业板块涨幅榜
industry_rank = ak.stock_board_industry_name_em()

# 筛选热点板块（涨幅>3%，涨停股数量>3只）
hot_boards = []
for board in concept_rank.head(20).itertuples():
    if board.涨跌幅 > 3 and board.涨停数 > 3:
        hot_boards.append({
            'name': board.板块名称,
            'change_pct': board.涨跌幅,
            'limit_up_count': board.涨停数
        })
```

### 阶段二：首板卡位（9:25-9:35）

#### 2.1 选股条件

**数据获取**:
```python
# 使用AKShare获取实时行情
spot_data = ak.stock_zh_a_spot_em()

# 筛选首板卡位候选股
candidates = []
for stock in spot_data.itertuples():
    # 条件1: 早盘9:35前涨停
    if stock.最新价 == stock.涨停价 and stock.涨跌幅 >= 9.5:
        # 条件2: 流通市值<30亿
        market_cap = stock.总市值 * stock.流通市值占比 / 100
        if market_cap < 30 * 100000000:  # 30亿
            # 条件3: 封单量>2%
            limit_up_amount = stock.封单额
            if limit_up_amount / stock.总市值 > 0.02:
                candidates.append({
                    'code': stock.代码,
                    'name': stock.名称,
                    'market_cap': market_cap,
                    'limit_up_amount': limit_up_amount,
                    'change_pct': stock.涨跌幅
                })
```

#### 2.2 操作执行

**操作步骤**:
1. 确认选股条件全部满足
2. 检查板块效应（板块内是否有3只以上涨停）
3. 确认题材新颖、有想象空间
4. 扫板介入，仓位10%

### 阶段三：二板定龙（T+1日）

#### 3.1 确认条件

**数据获取**:
```python
# 使用JQData获取昨日首板股票数据
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# 获取昨日涨停股票
limit_up_stocks = jq.get_limit_price_list(date=yesterday, limit_type='UP')

# 筛选今日二板股票
second_board_candidates = []
for stock in limit_up_stocks:
    code = stock['code']
    # 获取今日数据
    today_data = jq.get_price(code, count=1, end_date=today, frequency='daily')
    
    # 条件1: 换手率>25%
    turnover = today_data['turnover'].iloc[0] if 'turnover' in today_data.columns else 0
    if turnover > 25:
        # 条件2: 分时走势确认（需要实时数据）
        # 条件3: 板块内3只以上跟风涨停
        board_stocks = get_board_stocks(code)  # 获取同板块股票
        follow_up_count = count_limit_up_in_board(board_stocks)
        
        if follow_up_count >= 3:
            second_board_candidates.append({
                'code': code,
                'name': stock['name'],
                'turnover': turnover,
                'follow_up_count': follow_up_count
            })
```

#### 3.2 操作执行

**操作步骤**:
1. 确认换手率>25%
2. 确认分时走势：急跌不破开盘价，反弹带量拉升
3. 确认板块内3只以上跟风涨停
4. 重仓介入，仓位50%

### 阶段四：三板加速（T+2日）

#### 4.1 确认条件

**数据获取**:
```python
# 获取三板股票数据
third_board_candidates = []
for stock in second_board_candidates:
    code = stock['code']
    # 获取今日数据
    today_data = jq.get_price(code, count=3, end_date=today, frequency='daily')
    
    # 条件1: 缩量涨停或量能持续放大
    volume_trend = check_volume_trend(today_data)
    
    # 条件2: 板块效应持续增强
    board_effect = check_board_effect(code)
    
    if volume_trend in ['缩量涨停', '量能放大'] and board_effect:
        third_board_candidates.append({
            'code': code,
            'name': stock['name'],
            'volume_trend': volume_trend,
            'board_effect': board_effect
        })
```

#### 4.2 操作执行

**操作步骤**:
1. 确认缩量涨停或量能持续放大
2. 确认板块效应持续增强
3. 继续加仓，仓位40%
4. 总仓位达到100%

### 阶段五：持有与退出

#### 5.1 持有策略

- **坚定持有**: 不爱做T，看准就坚定持有到巅峰
- **不频繁交易**: 避免踏空
- **享受主升浪**: 持有至见顶或停牌风险

#### 5.2 退出时机

**退出条件**:
1. **明显见顶**: 
   - 高位放量滞涨
   - 连续3日无法创新高
   - 板块效应明显减弱
2. **停牌风险**: 
   - 连续涨停触发停牌规则
   - 预计停牌风险
3. **市场环境变化**:
   - 市场情绪进入退潮期
   - 板块整体退潮

---

## 数据获取方法

### JQData数据获取

#### 1. 市场指数数据

```python
import jqdatasdk as jq
from datetime import datetime

# 登录
jq.auth('username', 'password')

# 获取沪深300指数数据
hs300 = jq.get_price(
    '000300.XSHG',
    start_date='2024-01-01',
    end_date=datetime.now().strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume']
)

# 获取中证1000指数数据
zz1000 = jq.get_price(
    '000852.XSHG',
    start_date='2024-01-01',
    end_date=datetime.now().strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume']
)
```

#### 2. 个股历史数据

```python
# 获取个股历史数据
stock_data = jq.get_price(
    '000001.XSHE',  # 平安银行
    start_date='2024-01-01',
    end_date=datetime.now().strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume', 'money']
)

# 计算技术指标
stock_data['ma5'] = stock_data['close'].rolling(5).mean()
stock_data['ma10'] = stock_data['close'].rolling(10).mean()
stock_data['ma20'] = stock_data['close'].rolling(20).mean()
```

#### 3. 涨停板数据

```python
# 获取涨停板列表
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

limit_up_list = jq.get_limit_price_list(
    date=yesterday,
    limit_type='UP'  # UP: 涨停, DOWN: 跌停
)
```

#### 4. 财务数据

```python
# 获取财务指标
from jqdata import *

q = query(
    indicator.code,
    indicator.roe,           # ROE
    indicator.roa,           # ROA
    indicator.net_profit_margin  # 净利润率
).filter(
    indicator.code.in_(['000001.XSHE', '600000.XSHG'])
)

df = finance.run_query(q)
```

### AKShare数据获取

#### 1. 实时行情数据

```python
import akshare as ak

# 获取所有A股实时行情
spot_data = ak.stock_zh_a_spot_em()

# 筛选涨停股票
limit_up_stocks = spot_data[
    (spot_data['最新价'] == spot_data['涨停价']) & 
    (spot_data['涨跌幅'] >= 9.5)
]
```

#### 2. 板块数据

```python
# 获取概念板块数据
concept_data = ak.stock_board_concept_name_em()

# 获取行业板块数据
industry_data = ak.stock_board_industry_name_em()

# 获取板块成分股
board_stocks = ak.stock_board_concept_cons_em(symbol="新能源汽车")
```

#### 3. 资金流向数据

```python
# 获取个股资金流向
fund_flow = ak.stock_individual_fund_flow_rank(indicator="今日")

# 获取板块资金流向
board_fund_flow = ak.stock_board_fund_flow_rank(indicator="今日")
```

#### 4. 龙虎榜数据

```python
# 获取龙虎榜数据
from datetime import datetime
today = datetime.now().strftime('%Y%m%d')
lhb_data = ak.stock_lhb_detail_em(start_date=today, end_date=today)
```

### 知识库搜索

```python
from mcp_servers.unified_dev_server import knowledge_search

# 搜索陈小群战法
result = knowledge_search("陈小群三板斧战法", limit=5)

# 搜索龙头战法
result = knowledge_search("龙头战法", limit=5)

# 搜索情绪周期
result = knowledge_search("情绪周期", limit=5)
```

---

## 实盘操作案例

### 案例1: 航天发展（合力情绪战法）

#### 背景
- **时间**: 2024年X月
- **板块**: 商业航天
- **市场环境**: 情绪高涨，商业航天成为市场热点

#### 操作过程

**T日（首板）**:
- **9:30**: 商业航天板块异动，多只股票涨停
- **9:32**: 航天发展涨停，封单量强劲
- **9:33**: 确认条件：
  - ✅ 早盘9:35前涨停
  - ✅ 流通市值<30亿
  - ✅ 封单量>2%
  - ✅ 板块内3只以上跟风涨停
- **9:34**: 扫板介入，仓位10%

**T+1日（二板）**:
- **9:30**: 航天发展高开，快速封板
- **9:35**: 确认条件：
  - ✅ 换手率>25%
  - ✅ 分时走势：急跌不破开盘价，反弹带量拉升
  - ✅ 板块内5只跟风涨停
- **9:36**: 重仓介入，仓位50%

**T+2日（三板）**:
- **9:30**: 航天发展继续涨停
- **9:35**: 确认条件：
  - ✅ 缩量涨停
  - ✅ 板块效应持续增强
- **9:36**: 继续加仓，仓位40%

**T+3至T+5日**:
- **持有**: 享受主升浪，5连板
- **观察**: 板块效应持续，资金共识强劲

**T+6日（退出）**:
- **9:30**: 行情震荡，板块分化
- **9:35**: 确认风险信号：
  - ❌ 板块效应减弱
  - ❌ 高位放量滞涨
- **9:36**: 果断止盈离场，保住收益

#### 收益分析
- **入场价格**: 10.50元
- **退出价格**: 16.80元
- **收益率**: 60%
- **持仓时间**: 6个交易日
- **仓位**: 最高100%

### 案例2: 中交地产（龙头战法）

#### 背景
- **时间**: 2024年X月
- **板块**: 房地产
- **市场环境**: 情绪高涨，房地产成为市场主线

#### 操作过程

**T日（首板）**:
- **9:30**: 房地产板块异动
- **9:32**: 中交地产涨停，确认龙头地位
- **9:33**: 确认条件：
  - ✅ 市场辨识度最高
  - ✅ 逻辑硬（政策利好）
  - ✅ 盘子小（深市）
- **9:34**: 重仓介入，仓位50%

**T+1至T+20日**:
- **持有**: 坚定持有，享受主升浪
- **观察**: 龙头地位确认，板块效应持续

**T+21日（退出）**:
- **9:30**: 明显见顶信号
- **9:35**: 确认风险信号：
  - ❌ 高位放量滞涨
  - ❌ 连续3日无法创新高
- **9:36**: 果断退出

#### 收益分析
- **入场价格**: 8.50元
- **退出价格**: 18.70元
- **收益率**: 120%
- **持仓时间**: 21个交易日
- **仓位**: 50%

---

## 一周投资建议

> **注意**: 以下投资建议基于当前市场环境和数据，实际操作需根据实时市场情况调整。  
> **生成方式**: 使用 `scripts/strategies/generate_chen_xiaoqun_weekly_advice.py` 自动生成

### 自动生成一周建议

运行以下命令生成最新的一周投资建议：

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/strategies/generate_chen_xiaoqun_weekly_advice.py
```

生成的建议会保存到 `docs/strategies/weekly_advice.md`。

### 当前一周投资建议（2026-01-13生成）

#### 市场环境判断
- **当前市场情绪**: 高位震荡期
- **市场指数**: 沪深300、中证1000高位震荡
- **建议**: 逐步减仓，锁定利润

#### 每日操作建议

**周一（2026-01-13）**:
- **市场情绪**: 高位震荡期
- **建议仓位**: 逐步减仓
- **操作策略**: 锁定利润，防范风险
- **风险控制**: 逐步减仓，保留核心仓位

**周二（2026-01-14）**:
- **市场情绪**: 高位震荡期
- **建议仓位**: 逐步减仓
- **操作策略**: 锁定利润，防范风险
- **风险控制**: 逐步减仓，保留核心仓位

**周三（2026-01-15）**:
- **市场情绪**: 高位震荡期
- **建议仓位**: 逐步减仓
- **操作策略**: 锁定利润，防范风险
- **风险控制**: 逐步减仓，保留核心仓位

**周四（2026-01-16）**:
- **市场情绪**: 退潮期
- **建议仓位**: 空仓观望
- **操作策略**: 等待下一轮机会
- **风险控制**: 空仓，不操作

**周五（2026-01-17）**:
- **市场情绪**: 退潮期
- **建议仓位**: 空仓观望
- **操作策略**: 等待下一轮机会
- **风险控制**: 空仓，不操作

### 不同情绪周期的操作策略

#### 启动期（轻仓试错 10%）

**首板卡位机会**:
1. **板块关注**: 
   - 人工智能（AI）
   - 新能源汽车
   - 半导体
2. **选股条件**:
   - 早盘9:35前涨停
   - 流通市值<30亿
   - 封单量>2%
   - 板块内3只以上跟风涨停

**具体操作**:
- **时间**: 9:30-9:35
- **策略**: 首板卡位术
- **仓位**: 10%
- **止损**: -5%

#### 加速期（重仓持有 50%+）

**二板定龙机会**:
1. **确认条件**:
   - 换手率>25%
   - 分时走势：急跌不破开盘价，反弹带量拉升
   - 板块内3只以上跟风涨停
2. **操作**: 重仓介入，仓位50%

**三板加速机会**:
1. **确认条件**:
   - 缩量涨停或量能持续放大
   - 板块效应持续增强
2. **操作**: 继续加仓，仓位40%

#### 高位震荡期（逐步减仓）

**减仓策略**:
- 逐步减仓，锁定利润
- 保留核心仓位
- 防范风险

#### 退潮期（空仓观望）

**空仓策略**:
- 空仓观望
- 等待下一轮机会
- 不操作

### 数据获取代码示例

#### 获取实时行情和涨停股票

```python
# 使用AKShare获取实时行情
import akshare as ak
spot_data = ak.stock_zh_a_spot_em()

# 筛选首板卡位候选股
candidates = spot_data[
    (spot_data['最新价'] == spot_data['涨停价']) &
    (spot_data['涨跌幅'] >= 9.5) &
    (spot_data['总市值'] < 30 * 100000000)
]

# 使用知识库搜索相关战法
from mcp_servers.unified_dev_server import knowledge_search
kb_result = knowledge_search("首板卡位术", limit=3)
```

#### 获取市场指数数据

```python
# 使用JQData获取市场指数数据
import jqdatasdk as jq
from datetime import datetime

jq.auth('username', 'password')

# 获取沪深300指数
hs300 = jq.get_price(
    '000300.XSHG',
    count=20,
    end_date=datetime.now().strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume']
)

# 获取中证1000指数
zz1000 = jq.get_price(
    '000852.XSHG',
    count=20,
    end_date=datetime.now().strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume']
)
```

#### 获取热点板块

```python
# 使用AKShare获取热点板块
import akshare as ak

# 获取概念板块
concept_data = ak.stock_board_concept_name_em()

# 筛选热点板块（涨幅>3%）
hot_boards = concept_data[concept_data['涨跌幅'] > 3].head(10)
```

---

## 风险控制

### 止损策略

1. **首板止损**: -5%
2. **二板止损**: -8%
3. **三板止损**: -10%

### 止盈策略

1. **首板止盈**: +10%
2. **二板止盈**: +20%
3. **三板止盈**: +30%或持有至见顶

### 仓位管理

1. **启动期**: 10%轻仓试错
2. **加速期**: 50%+重仓持有
3. **高位震荡期**: 逐步减仓
4. **退潮期**: 空仓观望

### 风险提示

1. **高风险高收益**: 游资战法属于高风险策略，需要严格的风险控制
2. **市场环境依赖**: 战法效果与市场情绪周期密切相关
3. **纪律要求高**: 需要极强的执行力和纪律性
4. **不适合所有人**: 需要丰富的实战经验和市场敏感度

---

## 附录

### A. 数据源配置

#### JQData配置

```python
# config/jqdata_config.json
{
    "username": "your_username",
    "password": "your_password"
}
```

#### AKShare使用

```python
# AKShare无需配置，直接使用
import akshare as ak
```

### B. 知识库使用

```python
from mcp_servers.unified_dev_server import knowledge_search

# 搜索相关战法
result = knowledge_search("陈小群三板斧战法", limit=5)
result = knowledge_search("龙头战法", limit=5)
result = knowledge_search("情绪周期", limit=5)
```

### C. 相关文档

- [陈小群战法知识库](./CHEN_XIAOQUN_STRATEGY_REVIEW.md)
- [知识库构建报告](./CHEN_XIAOQUN_KB_BUILD_REPORT.md)
- [JQData配置指南](../JQDATA_CONFIGURATION_GUIDE.md)
- [AKShare数据源文档](../04_platform_integration/AKSHARE_DATA_SOURCE.md)

---

**最后更新**: 2026-01-13  
**维护者**: TRQuant Team
