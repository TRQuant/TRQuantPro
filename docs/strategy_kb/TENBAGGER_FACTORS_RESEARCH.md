# A股十倍股因子研究报告

> **研究时间**: 2025-12-20  
> **数据来源**: 东吴证券《A股十倍股群像》、网络调研  
> **研究目的**: 设计可执行的十倍股识别因子组合

---

## 一、研究背景

### 1.1 十倍股定义

**十倍股（Tenbagger）**：股价在一定时期内上涨10倍以上的超级赢家。

**关键统计**（来自东吴证券A股样本）：
- 起步市值均值：约17亿元
- 30亿以下占比：78%
- 起步PE：约47倍
- 净利润年化增速：约23%
- 毛利率：约30%
- ROE：约13%
- 创十倍平均用时：约8年

### 1.2 行业分布

| 行业 | 数量 | 占比 |
|------|------|------|
| 医药生物 | 26 | 26% |
| 食品饮料 | 10 | 10% |
| 电子 | 10 | 10% |
| 计算机 | 9 | 9% |
| 国防军工 | 7 | 7% |
| 房地产 | 7 | 7% |
| 汽车 | 6 | 6% |
| 其他 | 25 | 25% |

---

## 二、十倍股核心因子

### 2.1 财务因子（40%权重）

| 因子 | 字段 | 阈值 | 权重 | JQData字段 |
|------|------|------|------|------------|
| 营收增速 | revenue_growth | >15% | 10% | `inc_revenue_year_on_year` |
| 利润增速 | profit_growth | >20% | 10% | `inc_net_profit_year_on_year` |
| 毛利率 | gross_margin | >25% | 8% | `gross_profit_margin` |
| ROE | roe | >10% | 7% | `roe` |
| 净利率 | net_margin | >5% | 5% | `net_profit_margin` |

### 2.2 估值因子（20%权重）

| 因子 | 字段 | 阈值 | 权重 | JQData字段 |
|------|------|------|------|------------|
| PE | pe_ratio | <100 | 8% | `valuation.pe_ratio` |
| PEG | peg | <2 | 7% | 计算: PE / profit_growth |
| 市值 | market_cap | 20-300亿 | 5% | `valuation.market_cap` |

### 2.3 成长动量因子（25%权重）

| 因子 | 字段 | 阈值 | 权重 | 计算方法 |
|------|------|------|------|----------|
| 营收加速度 | rev_accel | >0 | 10% | 本期增速-上期增速 |
| 利润加速度 | profit_accel | >0 | 10% | 本期增速-上期增速 |
| 连续改善 | consecutive | ≥2季度 | 5% | 连续季度环比改善 |

### 2.4 技术因子（15%权重）

| 因子 | 字段 | 阈值 | 权重 | 计算方法 |
|------|------|------|------|----------|
| 均线多头 | ma_bullish | True | 5% | MA5>MA20>MA60 |
| 相对强度 | rs | >60 | 5% | 近20日涨幅排名 |
| 成交量趋势 | vol_trend | 放大 | 5% | 5日量/20日量 |

---

## 三、JQData实现方案

### 3.1 数据获取

```python
from jqdatasdk import *

# 1. 获取财务指标（indicator表）
def get_financial_factors(symbol: str, date: str) -> dict:
    """获取财务因子"""
    q = query(
        indicator.roe,                        # ROE
        indicator.gross_profit_margin,        # 毛利率
        indicator.net_profit_margin,          # 净利率
        indicator.inc_revenue_year_on_year,   # 营收同比增速
        indicator.inc_net_profit_year_on_year,# 净利润同比增速
        indicator.eps                         # 每股收益
    ).filter(
        indicator.code == symbol
    )
    df = get_fundamentals(q, statDate=date)
    return df.to_dict('records')[0] if len(df) > 0 else {}

# 2. 获取估值数据（valuation表）
def get_valuation_factors(symbol: str, date: str) -> dict:
    """获取估值因子"""
    q = query(
        valuation.pe_ratio,                   # PE
        valuation.pb_ratio,                   # PB
        valuation.ps_ratio,                   # PS
        valuation.market_cap,                 # 总市值（亿）
        valuation.circulating_market_cap,     # 流通市值
        valuation.turnover_ratio              # 换手率
    ).filter(
        valuation.code == symbol
    )
    df = get_fundamentals(q, date=date)
    return df.to_dict('records')[0] if len(df) > 0 else {}

# 3. 获取价格数据
def get_price_factors(symbol: str, end_date: str, days: int = 60) -> dict:
    """获取技术因子"""
    from datetime import datetime, timedelta
    
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - 
                  timedelta(days=days)).strftime('%Y-%m-%d')
    
    prices = get_price(
        symbol,
        start_date=start_date,
        end_date=end_date,
        frequency='daily',
        fields=['close', 'volume', 'high', 'low']
    )
    
    if prices is None or len(prices) < 20:
        return {}
    
    # 计算技术因子
    close = prices['close']
    volume = prices['volume']
    
    # 均线
    ma5 = close.tail(5).mean()
    ma20 = close.tail(20).mean()
    ma60 = close.tail(60).mean() if len(close) >= 60 else ma20
    
    # 均线多头
    ma_bullish = close.iloc[-1] > ma5 > ma20
    
    # 成交量比率
    vol_5 = volume.tail(5).mean()
    vol_20 = volume.tail(20).mean()
    vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
    
    # 相对强度
    if len(close) >= 20:
        change_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100
        rs = min(100, max(0, 50 + change_20d))
    else:
        rs = 50
    
    return {
        'ma_bullish': ma_bullish,
        'vol_ratio': vol_ratio,
        'relative_strength': rs,
        'latest_close': close.iloc[-1]
    }
```

### 3.2 因子计算

```python
def calculate_tenbagger_score(symbol: str, date: str) -> dict:
    """计算十倍股潜力得分"""
    
    # 获取数据
    financial = get_financial_factors(symbol, date)
    valuation = get_valuation_factors(symbol, date)
    technical = get_price_factors(symbol, date)
    
    score = 0
    details = {}
    
    # === 财务因子（40%） ===
    
    # 营收增速（10%）
    rev_growth = financial.get('inc_revenue_year_on_year', 0)
    if rev_growth >= 30:
        score += 10
    elif rev_growth >= 15:
        score += 7
    elif rev_growth >= 0:
        score += 3
    details['revenue_growth'] = rev_growth
    
    # 利润增速（10%）
    profit_growth = financial.get('inc_net_profit_year_on_year', 0)
    if profit_growth >= 50:
        score += 10
    elif profit_growth >= 20:
        score += 7
    elif profit_growth >= 0:
        score += 3
    details['profit_growth'] = profit_growth
    
    # 毛利率（8%）
    gross_margin = financial.get('gross_profit_margin', 0)
    if gross_margin >= 40:
        score += 8
    elif gross_margin >= 25:
        score += 5
    elif gross_margin >= 15:
        score += 2
    details['gross_margin'] = gross_margin
    
    # ROE（7%）
    roe = financial.get('roe', 0)
    if roe >= 15:
        score += 7
    elif roe >= 10:
        score += 5
    elif roe >= 5:
        score += 3
    details['roe'] = roe
    
    # 净利率（5%）
    net_margin = financial.get('net_profit_margin', 0)
    if net_margin >= 15:
        score += 5
    elif net_margin >= 5:
        score += 3
    details['net_margin'] = net_margin
    
    # === 估值因子（20%） ===
    
    # PE（8%）
    pe = valuation.get('pe_ratio', 0)
    if 0 < pe <= 30:
        score += 8
    elif 30 < pe <= 50:
        score += 6
    elif 50 < pe <= 100:
        score += 3
    details['pe'] = pe
    
    # PEG（7%）
    if profit_growth > 0 and pe > 0:
        peg = pe / profit_growth
        if peg <= 1:
            score += 7
        elif peg <= 2:
            score += 5
        elif peg <= 3:
            score += 2
        details['peg'] = peg
    
    # 市值（5%）
    market_cap = valuation.get('market_cap', 0)
    if 20 <= market_cap <= 100:
        score += 5
    elif 100 < market_cap <= 300:
        score += 3
    elif market_cap < 20:
        score += 2  # 太小可能流动性差
    details['market_cap'] = market_cap
    
    # === 技术因子（15%） ===
    
    # 均线多头（5%）
    if technical.get('ma_bullish', False):
        score += 5
    details['ma_bullish'] = technical.get('ma_bullish', False)
    
    # 相对强度（5%）
    rs = technical.get('relative_strength', 50)
    if rs >= 70:
        score += 5
    elif rs >= 60:
        score += 3
    details['relative_strength'] = rs
    
    # 成交量趋势（5%）
    vol_ratio = technical.get('vol_ratio', 1)
    if vol_ratio >= 1.5:
        score += 5
    elif vol_ratio >= 1.2:
        score += 3
    details['vol_ratio'] = vol_ratio
    
    # === 成长动量（25%）待实现 ===
    # 需要获取多期数据计算加速度
    
    return {
        'symbol': symbol,
        'score': score,
        'max_score': 100,
        'details': details,
        'level': get_level(score)
    }

def get_level(score: float) -> str:
    """根据分数确定等级"""
    if score >= 80:
        return 'S+'
    elif score >= 70:
        return 'S'
    elif score >= 60:
        return 'A'
    elif score >= 50:
        return 'B'
    elif score >= 40:
        return 'C'
    else:
        return 'D'
```

---

## 四、因子权重体系

### 4.1 基础权重

| 因子类别 | 权重 | 说明 |
|----------|------|------|
| 财务因子 | 40% | 业绩是底层燃料 |
| 成长动量 | 25% | 加速度和连续性 |
| 估值因子 | 20% | 空间和安全边际 |
| 技术因子 | 15% | 趋势确认 |

### 4.2 动态调整

```python
# 根据市场环境动态调整权重
def get_dynamic_weights(market_trend: str) -> dict:
    """
    market_trend: 'bull' / 'bear' / 'neutral'
    """
    if market_trend == 'bull':
        return {
            'financial': 0.35,
            'growth': 0.30,  # 牛市更重成长
            'valuation': 0.15,
            'technical': 0.20
        }
    elif market_trend == 'bear':
        return {
            'financial': 0.45,  # 熊市更重质量
            'growth': 0.20,
            'valuation': 0.25,  # 更重估值安全
            'technical': 0.10
        }
    else:
        return {
            'financial': 0.40,
            'growth': 0.25,
            'valuation': 0.20,
            'technical': 0.15
        }
```

---

## 五、三层漏斗筛选

### 5.1 L0 - 基础过滤

```python
L0_CRITERIA = {
    # 排除条件
    'exclude_st': True,
    'exclude_delisting_risk': True,
    'min_trading_days_ratio': 0.9,
    
    # 市值范围
    'market_cap_min': 20,   # 亿
    'market_cap_max': 500,  # 亿
    
    # 流动性
    'min_turnover': 0.005,  # 0.5%
}
```

### 5.2 L1 - 早期信号

```python
L1_CRITERIA = {
    # 成长性
    'revenue_growth_min': 15,
    'profit_growth_min': 20,
    
    # 盈利能力
    'gross_margin_min': 20,
    'roe_min': 5,
    
    # 阈值
    'score_threshold': 40,
}
```

### 5.3 L2 - 精选推荐

```python
L2_CRITERIA = {
    # 更高标准
    'revenue_growth_min': 25,
    'profit_growth_min': 30,
    'gross_margin_min': 30,
    'roe_min': 10,
    
    # 技术确认
    'ma_bullish': True,
    'relative_strength_min': 60,
    
    # 阈值
    'score_threshold': 60,
    
    # 通过率控制
    'target_pass_rate': (0.05, 0.20),  # 5%-20%
}
```

---

## 六、阶段判定标准

### 6.1 S0 - 观察期（排除）

- 无明显增长信号
- 业绩平稳或下滑
- 市场关注度低
- **行动**: 排除或观察

### 6.2 S1 - 验证期（关注）

- 营收增速>15%
- 利润增速>20%
- 成交量从底部回升
- **行动**: 重点关注，小仓试探

### 6.3 S2 - 导入期（最佳买入）⭐

- 营收增速>25%
- 利润增速>30%
- 增速加速（环比提升）
- 放量突破关键位
- **行动**: ★ 最佳买入点

### 6.4 S3 - 放量期（持有）

- 营收增速>40%
- 利润增速>50%
- 高成交量
- **行动**: 持有，设置止盈

---

## 七、与现有系统集成

### 7.1 更新 scoring_engine_v2.py

将上述因子体系集成到现有评分引擎。

### 7.2 更新 candidate_funnel.py

将L0/L1/L2标准更新到漏斗筛选。

### 7.3 更新 tri_axis_stage.py

将阶段判定标准更新到三轴状态机。

---

## 八、总结

### 8.1 核心发现

1. **小市值是基础**: 78%十倍股起步市值<30亿
2. **高增速是驱动**: 净利润CAGR约23%
3. **高毛利是护城河**: 毛利率约30%
4. **ROE是质量标尺**: 约13%
5. **PE不必太低**: 起步PE约47倍，靠业绩消化

### 8.2 关键纪律

1. **7%-8%止损**: 无条件执行
2. **识别高潮顶**: 加速上冲后分批卖出
3. **分批止盈**: 涨幅过大先锁1/3利润
4. **降低仓位**: 市场分配日增多时

### 8.3 下一步

1. 实现因子计算代码
2. 集成到V2系统
3. 回测验证
4. 优化参数

---

*研究报告 | 创建时间: 2025-12-20 | 版本: v1.0*

