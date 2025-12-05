---
title: "附录：量化因子速查手册"
description: "A股量化因子公式、API参考和常用代码速查"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-quantitative"
updateDate: "2025-01-27"
---

# 📋 附录：量化因子速查手册

> **快速查阅量化因子公式、JQData API和常用代码模板**

## 📋 目录

<div class="section-overview">
  <div class="overview-item">
    <span class="item-icon">📊</span>
    <a href="#value-factors">价值因子公式</a>
    <span class="item-desc">PE、PB、PS、股息率</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">📈</span>
    <a href="#growth-factors">成长因子公式</a>
    <span class="item-desc">营收增速、利润增速、ROE变化</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">⭐</span>
    <a href="#quality-factors">质量因子公式</a>
    <span class="item-desc">ROE、毛利率、周转率、杠杆</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">🚀</span>
    <a href="#momentum-factors">动量因子公式</a>
    <span class="item-desc">价格动量、反转、成交量</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">💰</span>
    <a href="#flow-factors">资金流因子公式</a>
    <span class="item-desc">北向资金、主力资金、融资</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">🔧</span>
    <a href="#jqdata-api">JQData API参考</a>
    <span class="item-desc">常用数据接口</span>
  </div>
  <div class="overview-item">
    <span class="item-icon">📝</span>
    <a href="#code-templates">代码模板</a>
    <span class="item-desc">因子计算、回测框架</span>
  </div>
</div>

---

<h2 id="value-factors">📊 价值因子公式</h2>

### 估值指标

| 因子 | 公式 | 方向 | 说明 |
|------|------|------|------|
| **EP（盈利收益率）** | EP = 净利润TTM / 市值 | 越高越好 | PE的倒数，便于处理负值 |
| **BP（账面市值比）** | BP = 净资产 / 市值 | 越高越好 | PB的倒数 |
| **SP（营收收益率）** | SP = 营业收入TTM / 市值 | 越高越好 | PS的倒数 |
| **股息率** | DY = 每股股息 / 股价 | 越高越好 | 现金回报率 |
| **EVEBITDA** | EV/EBITDA = 企业价值 / EBITDA | 越低越好 | 考虑负债的估值 |

### 价值因子代码

```python
def calculate_value_factors(stocks, date):
    """计算价值因子"""
    # 获取估值数据
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.ps_ratio,
        valuation.market_cap
    ).filter(valuation.code.in_(stocks))
    
    df = get_fundamentals(q, date)
    
    # 计算因子（使用倒数，方向一致）
    df['EP'] = 1 / df['pe_ratio']  # 盈利收益率
    df['BP'] = 1 / df['pb_ratio']  # 账面市值比
    df['SP'] = 1 / df['ps_ratio']  # 营收收益率
    
    return df[['code', 'EP', 'BP', 'SP']]
```

---

<h2 id="growth-factors">📈 成长因子公式</h2>

### 成长指标

| 因子 | 公式 | 方向 | 说明 |
|------|------|------|------|
| **营收同比增速** | (营收_t - 营收_t-1) / 营收_t-1 | 越高越好 | 业务规模扩张 |
| **净利润同比增速** | (净利润_t - 净利润_t-1) / abs(净利润_t-1) | 越高越好 | 盈利增长 |
| **扣非净利润增速** | (扣非_t - 扣非_t-1) / abs(扣非_t-1) | 越高越好 | 主业盈利增长 |
| **ROE变化** | ROE_t - ROE_t-1 | 越高越好 | 盈利能力改善 |
| **分析师预期修正** | (预期_t - 预期_t-1) / abs(预期_t-1) | 越高越好 | 预期边际变化 |

### 成长因子代码

```python
def calculate_growth_factors(stocks, date):
    """计算成长因子"""
    q = query(
        indicator.code,
        indicator.inc_revenue_year_on_year,      # 营收同比
        indicator.inc_net_profit_year_on_year,   # 净利润同比
        indicator.roe                             # ROE
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date)
    
    # 异常值处理
    df['revenue_growth'] = df['inc_revenue_year_on_year'].clip(-100, 500)
    df['profit_growth'] = df['inc_net_profit_year_on_year'].clip(-100, 500)
    
    return df
```

---

<h2 id="quality-factors">⭐ 质量因子公式</h2>

### 质量指标

| 因子 | 公式 | 方向 | 说明 |
|------|------|------|------|
| **ROE** | 净利润 / 净资产 | 越高越好 | 股东回报率 |
| **ROA** | 净利润 / 总资产 | 越高越好 | 资产回报率 |
| **毛利率** | (营收 - 营业成本) / 营收 | 越高越好 | 产品竞争力 |
| **净利率** | 净利润 / 营收 | 越高越好 | 盈利能力 |
| **资产周转率** | 营收 / 总资产 | 越高越好 | 资产效率 |
| **资产负债率** | 总负债 / 总资产 | 越低越好 | 财务风险 |
| **现金流/净利润** | 经营现金流 / 净利润 | 越高越好 | 盈利质量 |

### 质量因子代码

```python
def calculate_quality_factors(stocks, date):
    """计算质量因子"""
    q = query(
        indicator.code,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_margin
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date)
    
    # 获取资产负债率
    balance_q = query(
        balance.code,
        balance.total_liability,
        balance.total_assets
    ).filter(balance.code.in_(stocks))
    balance_df = get_fundamentals(balance_q, date)
    
    df['leverage'] = balance_df['total_liability'] / balance_df['total_assets']
    
    return df
```

---

<h2 id="momentum-factors">🚀 动量因子公式</h2>

### 动量指标

| 因子 | 公式 | 方向 | 说明 |
|------|------|------|------|
| **N月动量** | (P_t - P_t-N) / P_t-N | A股：中期正向 | 价格趋势 |
| **1周反转** | -(P_t - P_t-5) / P_t-5 | A股：负向有效 | 短期反转 |
| **相对强弱** | 股票收益 - 基准收益 | 越高越好 | 相对表现 |
| **行业动量** | 行业指数N月收益 | 中期正向 | 行业趋势 |
| **成交量比** | 近N日成交量 / 过去M日均量 | 放量为正 | 量价配合 |

### 动量因子代码

```python
def calculate_momentum_factors(stocks, date, lookback=120):
    """计算动量因子"""
    # 获取历史价格
    price_df = get_price(
        stocks, 
        end_date=date, 
        count=lookback + 1, 
        fields=['close'],
        panel=False
    )
    
    # 计算收益率
    momentum = price_df.groupby('code').apply(
        lambda x: x['close'].iloc[-1] / x['close'].iloc[0] - 1
    )
    
    # 1周反转（负向）
    price_1w = get_price(stocks, end_date=date, count=6, fields=['close'], panel=False)
    reversal_1w = -price_1w.groupby('code').apply(
        lambda x: x['close'].iloc[-1] / x['close'].iloc[0] - 1
    )
    
    return pd.DataFrame({'momentum_6m': momentum, 'reversal_1w': reversal_1w})
```

---

<h2 id="flow-factors">💰 资金流因子公式</h2>

### 资金流指标

| 因子 | 公式 | 方向 | 说明 |
|------|------|------|------|
| **北向资金净买入** | 北向买入 - 北向卖出 | 越高越好 | 外资动向 |
| **北向持股比例变化** | 持股比例_t - 持股比例_t-N | 越高越好 | 外资增持 |
| **主力资金净流入** | 大单买入 - 大单卖出 | 越高越好 | 主力动向 |
| **融资余额变化** | (融资_t - 融资_t-N) / 融资_t-N | 越高越好 | 杠杆资金 |
| **机构持仓变化** | 机构持仓_t - 机构持仓_t-1 | 越高越好 | 机构动向 |

### 资金流因子代码

```python
def calculate_flow_factors(stocks, date):
    """计算资金流因子"""
    # 获取北向资金数据
    q = query(
        finance.STK_ML_QUOTA.day,
        finance.STK_ML_QUOTA.quota
    ).filter(
        finance.STK_ML_QUOTA.link_id == 310001,  # 沪股通
        finance.STK_ML_QUOTA.day <= date
    ).order_by(finance.STK_ML_QUOTA.day.desc()).limit(20)
    
    northbound = finance.run_query(q)
    
    # 获取融资融券数据
    margin_q = query(
        finance.STK_MT_TOTAL.sec_code,
        finance.STK_MT_TOTAL.fin_balance
    ).filter(
        finance.STK_MT_TOTAL.sec_code.in_(stocks),
        finance.STK_MT_TOTAL.date == date
    )
    margin = finance.run_query(margin_q)
    
    return margin
```

---

<h2 id="jqdata-api">🔧 JQData API参考</h2>

### 常用数据接口

| 函数 | 用途 | 示例 |
|------|------|------|
| `get_price()` | 获取行情数据 | `get_price('000001.XSHE', count=10)` |
| `get_fundamentals()` | 获取财务数据 | `get_fundamentals(query(...), date)` |
| `get_valuation()` | 获取估值数据 | `get_valuation(stocks, date)` |
| `get_index_stocks()` | 获取指数成分股 | `get_index_stocks('000300.XSHG')` |
| `get_industry()` | 获取行业分类 | `get_industry(stocks, date, 'sw_l1')` |
| `get_all_securities()` | 获取所有证券 | `get_all_securities('stock')` |
| `get_trade_days()` | 获取交易日 | `get_trade_days(start, end)` |

### 查询示例

```python
from jqdata import *

# 获取沪深300成分股
stocks = get_index_stocks('000300.XSHG')

# 获取估值数据
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(
    valuation.code.in_(stocks),
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 100
)
df = get_fundamentals(q, '2024-01-01')

# 获取财务指标
q = query(
    indicator.code,
    indicator.roe,
    indicator.inc_net_profit_year_on_year
).filter(indicator.code.in_(stocks))
fundamentals = get_fundamentals(q, '2024-01-01')
```

---

<h2 id="code-templates">📝 代码模板</h2>

### 因子计算模板

```python
import pandas as pd
import numpy as np
from jqdata import *

def calculate_factor(stocks, date, factor_name):
    """
    通用因子计算模板
    
    参数:
        stocks: 股票列表
        date: 计算日期
        factor_name: 因子名称
    
    返回:
        因子值Series
    """
    # 1. 获取原始数据
    raw_data = get_raw_data(stocks, date)
    
    # 2. 计算因子值
    factor = compute_factor(raw_data)
    
    # 3. 异常值处理（MAD法）
    factor = winsorize_mad(factor)
    
    # 4. 标准化
    factor = (factor - factor.mean()) / factor.std()
    
    # 5. 行业中性化（可选）
    factor = industry_neutralize(factor, stocks, date)
    
    return factor


def winsorize_mad(series, n=5):
    """MAD法去极值"""
    median = series.median()
    mad = (series - median).abs().median()
    upper = median + n * 1.4826 * mad
    lower = median - n * 1.4826 * mad
    return series.clip(lower, upper)


def industry_neutralize(factor, stocks, date):
    """行业中性化"""
    industries = get_industry(stocks, date, 'sw_l1')
    industry_map = {s: ind['sw_l1']['industry_name'] for s, ind in industries.items()}
    
    df = pd.DataFrame({'factor': factor, 'industry': factor.index.map(industry_map)})
    df['factor_neutral'] = df.groupby('industry')['factor'].transform(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
    )
    return df['factor_neutral']
```

### 回测框架模板

```python
def backtest_factor(stocks, start_date, end_date, factor_func, top_n=30):
    """
    因子回测框架
    
    参数:
        stocks: 股票池
        start_date: 开始日期
        end_date: 结束日期
        factor_func: 因子计算函数
        top_n: 选股数量
    
    返回:
        回测结果DataFrame
    """
    trade_days = get_trade_days(start_date, end_date)
    monthly_days = [d for i, d in enumerate(trade_days) if i % 20 == 0]
    
    portfolio_returns = []
    
    for i, date in enumerate(monthly_days[:-1]):
        # 计算因子
        factor = factor_func(stocks, date)
        
        # 选股
        top_stocks = factor.nlargest(top_n).index.tolist()
        
        # 计算下月收益
        next_date = monthly_days[i + 1]
        returns = calculate_returns(top_stocks, date, next_date)
        portfolio_returns.append(returns.mean())
    
    # 计算绩效指标
    returns_series = pd.Series(portfolio_returns)
    annual_return = (1 + returns_series).prod() ** (12 / len(returns_series)) - 1
    sharpe = returns_series.mean() / returns_series.std() * np.sqrt(12)
    max_drawdown = calculate_max_drawdown(returns_series)
    
    return {
        'annual_return': annual_return,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown
    }
```

### PTrade策略模板

```python
def initialize(context):
    """初始化"""
    context.stock_pool = '000905.XSHG'  # 中证500
    context.hold_num = 30
    run_monthly(rebalance, 1, time='open')

def rebalance(context):
    """月度调仓"""
    # 获取股票池
    stocks = get_index_stocks(context.stock_pool)
    
    # 计算因子
    factor = calculate_composite_factor(stocks, context.current_dt)
    
    # 选股
    target_stocks = factor.nlargest(context.hold_num).index.tolist()
    
    # 调仓
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)
    
    weight = 1.0 / len(target_stocks)
    for stock in target_stocks:
        order_target_value(stock, context.portfolio.total_value * weight)
```

---

## 📊 因子有效性参考

### A股主要因子IC统计（2015-2024）

| 因子类别 | 代表因子 | IC均值 | IC_IR | 年化多空收益 |
|----------|----------|--------|-------|--------------|
| **价值** | EP | 0.032 | 0.45 | 7.3% |
| **成长** | 净利润增速 | 0.035 | 0.48 | 8.5% |
| **质量** | ROE | 0.038 | 0.52 | 9.2% |
| **动量** | 1周反转 | 0.042 | 0.65 | 10.5% |
| **资金流** | 北向资金 | 0.045 | 0.72 | 12.0% |

---

<div class="summary-outlook">
  <h3>返回目录</h3>
  <p>本附录提供了量化因子的快速参考，更详细的内容请参阅各章节。</p>
  
  <a href="/ashare-book4/000_Preface_CN" class="next-section">
    返回：第四册目录 →
  </a>
</div>
