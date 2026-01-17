# 聚宽情绪因子完整使用指南

**来源URL**: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10439  
**爬取时间**: 2026-01-12  
**文档类型**: JQData API文档 - 情绪类因子

---

## 一、情绪因子概述

### 1.1 什么是情绪因子

情绪因子（Emotion Factors）是量化交易中用于衡量市场情绪和投资者心理状态的指标。聚宽因子库中的情绪类因子包括：

- **PSY**: 心理线（Psychological Line），衡量市场超买超卖状态
- **AR**: 人气指标（Arising），反映市场买卖气势
- **BR**: 意愿指标（Bearing），反映市场买卖意愿
- **ARBR**: AR/BR组合指标
- **VR**: 成交量变异率（Volume Ratio），衡量成交量变化
- **WVAD**: 威廉变异离散量（Williams Variable Accumulation Distribution）

### 1.2 情绪因子的作用

- **市场情绪判断**: 识别市场恐慌、贪婪、中性等情绪状态
- **买卖时机**: 辅助判断超买超卖区域
- **风险控制**: 识别极端情绪，避免追涨杀跌
- **策略优化**: 作为多因子模型的重要组成部分

---

## 二、聚宽情绪因子API使用

### 2.1 获取情绪因子历史表现 - `get_factor_kanban_values`

**API函数**:
```python
from jqdatasdk import get_factor_kanban_values

df = get_factor_kanban_values(
    universe='hs300',                    # 股票池
    bt_cycle='month_3',                  # 测试周期
    model='long_only',                   # 组合模型
    category=['emotion'],                # 因子分类：情绪类
    skip_paused=False,                   # 是否过滤停牌
    commision_slippage=0                 # 手续费及滑点
)
```

**参数说明**:

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `universe` | 股票池 | `'hs300'`, `'zz500'`, `'zz800'`, `'zz1000'`, `'zzqz'` |
| `bt_cycle` | 测试周期 | `'month_3'`, `'year_1'`, `'year_3'`, `'year_10'` |
| `model` | 组合构建模型 | `'long_only'`（纯多头）, `'long_short'`（多空组合） |
| `category` | 因子分类 | `['emotion']` 表示情绪类因子 |
| `skip_paused` | 过滤停牌 | `False`（否）, `True`（是） |
| `commision_slippage` | 手续费及滑点 | `0`（无）, `1`（3‱佣金+1‰印花税）, `2`（+1‰滑点） |

**返回值** (long_only模式):

| 字段 | 说明 |
|------|------|
| `date` | 数据更新日期（T+2日凌晨3点后可用） |
| `category` | 因子分类（'emotion'） |
| `code` | 因子代码（如 'PSY', 'AR', 'BR', 'VR', 'WVAD'） |
| `ic_mean` | IC均值（因子与收益的相关性） |
| `ir` | IR值（信息比率） |
| `good_ic` | IC绝对值>0.02的比率 |
| `compound_return_1q` | 一分位数累积收益 |
| `compound_return_5q` | 五分位数累积收益 |
| `annualized_return_1q` | 一分位数年化收益率 |
| `annualized_return_5q` | 五分位数年化收益率 |
| `max_drawdown_1q` | 一分位数最大回撤 |
| `max_drawdown_5q` | 五分位数最大回撤 |
| `sharpe_1q` | 一分位数夏普比率 |
| `sharpe_5q` | 五分位数夏普比率 |
| `turnover_ratio_1q` | 一分位数换手率 |
| `turnover_ratio_5q` | 五分位数换手率 |

**使用示例**:
```python
from jqdatasdk import *

# 获取情绪因子看板数据
df = get_factor_kanban_values(
    universe='hs300',
    bt_cycle='month_3',
    model='long_only',
    category=['emotion'],
    skip_paused=False,
    commision_slippage=0
)

# 查看情绪因子列表
emotion_factors = df['code'].unique()
print(f"情绪因子列表: {emotion_factors}")

# 筛选表现好的情绪因子（IC>0.02）
good_factors = df[df['ic_mean'] > 0.02]['code'].unique()
print(f"有效情绪因子: {good_factors}")

# 查看PSY因子表现
psy_data = df[df['code'] == 'PSY']
print(psy_data[['date', 'ic_mean', 'ir', 'good_ic', 'sharpe_1q']])
```

**重要说明**:
- `get_factor_kanban_values` 返回的是**因子的历史表现数据**（IC、IR、收益等），**不是当前因子值**
- 数据更新时间：T日收盘后的因子收益需要T+1的收盘价才能得出，数据在T+2日凌晨3点计算后可用
- 该API主要用于**因子筛选和评估**，不能用于获取实时因子值

---

### 2.2 为什么不能直接使用 `get_factor_values`？

**API限制**:
```python
from jqdatasdk import get_factor_values

# ❌ 不支持情绪因子
values = get_factor_values(
    securities=['000001.XSHG'],
    factors=['PSY', 'ARBR', 'VR'],  # 这些因子不支持
    count=1,
    end_date='2024-01-12'
)
# 会报错或返回空值
```

**原因**:
- `get_factor_values` 主要支持 **CNE5/CNE6风格因子**（如 `size`, `beta`, `momentum`）
- 支持 **Alpha101/191因子**（如 `alpha_001`, `alpha_002`）
- **不支持情绪因子**（PSY、ARBR、VR、WVAD等）

**支持的因子类型**:
- ✅ CNE5风格因子: `size`, `beta`, `momentum`, `reversal`, `volatility`
- ✅ CNE6风格因子: `size`, `beta`, `momentum`, `reversal`, `volatility`, `growth`, `earnings_yield`
- ✅ Alpha101/191因子: `alpha_001` ~ `alpha_191`
- ❌ 情绪因子: `PSY`, `AR`, `BR`, `ARBR`, `VR`, `WVAD` 等

---

## 三、手动计算情绪因子值

由于聚宽不提供情绪因子的实时值API，需要手动计算。以下是常用情绪因子的计算方法：

### 3.1 PSY - 心理线

**计算公式**:
```
PSY = (N日内上涨天数 / N) × 100
```

**Python实现**:
```python
import jqdatasdk as jq
import pandas as pd
import numpy as np

def calculate_psy(security, end_date, period=12):
    """
    计算PSY心理线
    
    Args:
        security: 股票代码
        end_date: 结束日期
        period: 周期（默认12日）
    
    Returns:
        float: PSY值（0-100）
    """
    # 获取价格数据
    df = jq.get_price(
        security,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['close']
    )
    
    # 计算涨跌
    returns = df['close'].pct_change()
    up_days = (returns > 0).rolling(period).sum()
    psy = (up_days / period * 100).iloc[-1]
    
    return psy
```

### 3.2 ARBR - 人气意愿指标

**计算公式**:
```
AR = (N日内(H-O)之和 / N日内(O-L)之和) × 100
BR = (N日内(H-YC)之和 / N日内(YC-L)之和) × 100
其中：H=最高价, O=开盘价, L=最低价, YC=前收盘价
```

**Python实现**:
```python
def calculate_arbr(security, end_date, period=26):
    """
    计算AR/BR指标
    
    Args:
        security: 股票代码
        end_date: 结束日期
        period: 周期（默认26日）
    
    Returns:
        tuple: (AR值, BR值)
    """
    # 获取价格数据
    df = jq.get_price(
        security,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['open', 'high', 'low', 'close', 'pre_close']
    )
    
    # 计算AR
    h_o = (df['high'] - df['open']).rolling(period).sum()
    o_l = (df['open'] - df['low']).rolling(period).sum()
    ar = (h_o / o_l * 100).iloc[-1]
    
    # 计算BR
    h_yc = (df['high'] - df['pre_close']).rolling(period).sum()
    yc_l = (df['pre_close'] - df['low']).rolling(period).sum()
    br = (h_yc / yc_l * 100).iloc[-1]
    
    return ar, br
```

### 3.3 VR - 成交量变异率

**计算公式**:
```
VR = (N日内上涨日成交量之和 / N日内下跌日成交量之和) × 100
```

**Python实现**:
```python
def calculate_vr(security, end_date, period=26):
    """
    计算VR成交量变异率
    
    Args:
        security: 股票代码
        end_date: 结束日期
        period: 周期（默认26日）
    
    Returns:
        float: VR值
    """
    # 获取价格和成交量数据
    df = jq.get_price(
        security,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['close', 'volume']
    )
    
    # 计算涨跌
    returns = df['close'].pct_change()
    up_volume = df[returns > 0]['volume'].rolling(period).sum()
    down_volume = df[returns < 0]['volume'].rolling(period).sum()
    vr = (up_volume / down_volume * 100).iloc[-1]
    
    return vr
```

### 3.4 WVAD - 威廉变异离散量

**计算公式**:
```
WVAD = N日内((C-O)/(H-L) × V)之和
其中：C=收盘价, O=开盘价, H=最高价, L=最低价, V=成交量
```

**Python实现**:
```python
def calculate_wvad(security, end_date, period=24):
    """
    计算WVAD威廉变异离散量
    
    Args:
        security: 股票代码
        end_date: 结束日期
        period: 周期（默认24日）
    
    Returns:
        float: WVAD值
    """
    # 获取价格和成交量数据
    df = jq.get_price(
        security,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['open', 'high', 'low', 'close', 'volume']
    )
    
    # 计算WVAD
    wvad = ((df['close'] - df['open']) / (df['high'] - df['low']) * df['volume']).rolling(period).sum().iloc[-1]
    
    return wvad
```

---

## 四、实际应用示例

### 4.1 使用因子看板筛选有效情绪因子

```python
from jqdatasdk import *

# 获取情绪因子看板数据
df = get_factor_kanban_values(
    universe='hs300',
    bt_cycle='year_1',  # 近1年
    model='long_only',
    category=['emotion']
)

# 筛选IC>0.02且IR>0的有效因子
good_factors = df[
    (df['ic_mean'] > 0.02) & 
    (df['ir'] > 0) &
    (df['sharpe_1q'] > 0)
].sort_values('ic_mean', ascending=False)

print("有效情绪因子:")
print(good_factors[['code', 'ic_mean', 'ir', 'sharpe_1q', 'annualized_return_1q']])
```

### 4.2 计算当前情绪因子值并判断市场情绪

```python
import jqdatasdk as jq
from datetime import datetime

# 计算当前情绪因子
index_code = '000300.XSHG'  # 沪深300
end_date = datetime.now().strftime('%Y-%m-%d')

# 计算PSY
psy = calculate_psy(index_code, end_date, period=12)
print(f"PSY: {psy:.2f}")

# 计算AR/BR
ar, br = calculate_arbr(index_code, end_date, period=26)
print(f"AR: {ar:.2f}, BR: {br:.2f}")

# 判断市场情绪
if psy > 75:
    sentiment = "极度贪婪"
elif psy > 60:
    sentiment = "贪婪"
elif psy < 25:
    sentiment = "极度恐慌"
elif psy < 40:
    sentiment = "恐慌"
else:
    sentiment = "中性"

print(f"市场情绪: {sentiment}")
```

### 4.3 集成到多因子模型

```python
class EmotionFactorAnalyzer:
    """情绪因子分析器"""
    
    def __init__(self):
        self.factors = ['PSY', 'AR', 'BR', 'VR', 'WVAD']
    
    def analyze(self, security, date):
        """分析情绪因子"""
        results = {}
        
        # 计算各情绪因子
        results['PSY'] = calculate_psy(security, date, period=12)
        ar, br = calculate_arbr(security, date, period=26)
        results['AR'] = ar
        results['BR'] = br
        results['VR'] = calculate_vr(security, date, period=26)
        results['WVAD'] = calculate_wvad(security, date, period=24)
        
        # 综合情绪得分
        composite_score = self._calculate_composite_score(results)
        
        return {
            'factors': results,
            'composite_score': composite_score,
            'sentiment': self._interpret_sentiment(composite_score)
        }
    
    def _calculate_composite_score(self, factors):
        """计算综合情绪得分"""
        # 标准化各因子值
        psy_score = (factors['PSY'] - 50) / 50  # -1 ~ +1
        ar_score = (factors['AR'] - 100) / 100  # 标准化
        br_score = (factors['BR'] - 100) / 100
        vr_score = (factors['VR'] - 100) / 100
        
        # 加权平均
        composite = (
            psy_score * 0.3 +
            ar_score * 0.25 +
            br_score * 0.25 +
            vr_score * 0.2
        )
        
        return composite * 100  # 转换为-100 ~ +100
    
    def _interpret_sentiment(self, score):
        """解释情绪得分"""
        if score > 70:
            return "极度贪婪"
        elif score > 40:
            return "贪婪"
        elif score < -70:
            return "极度恐慌"
        elif score < -40:
            return "恐慌"
        else:
            return "中性"
```

---

## 五、性能优化建议

### 5.1 使用缓存减少API调用

```python
from functools import lru_cache
import jqdatasdk as jq

class CachedEmotionFactorCalculator:
    """带缓存的情绪因子计算器"""
    
    def __init__(self):
        self._price_cache = {}
        self._cache_max_size = 50
    
    def _get_price_cached(self, security, start_date, end_date, fields):
        """获取价格数据（带缓存）"""
        cache_key = f"{security}_{start_date}_{end_date}_{'_'.join(fields)}"
        
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        df = jq.get_price(security, start_date=start_date, end_date=end_date, fields=fields)
        
        # 缓存数据
        if len(self._price_cache) >= self._cache_max_size:
            oldest_key = next(iter(self._price_cache))
            del self._price_cache[oldest_key]
        
        self._price_cache[cache_key] = df
        return df
```

### 5.2 批量计算多个股票

```python
def batch_calculate_emotion_factors(securities, date):
    """批量计算多个股票的情绪因子"""
    results = {}
    
    # 批量获取价格数据
    all_prices = jq.get_price(
        securities,
        start_date=(pd.to_datetime(date) - pd.Timedelta(days=60)).strftime('%Y-%m-%d'),
        end_date=date,
        fields=['open', 'high', 'low', 'close', 'volume', 'pre_close']
    )
    
    # 批量计算
    for security in securities:
        if security in all_prices.index.get_level_values('code'):
            df = all_prices.loc[security]
            # 计算各因子...
            results[security] = {
                'PSY': calculate_psy_from_df(df),
                'AR': calculate_ar_from_df(df),
                # ...
            }
    
    return results
```

---

## 六、总结

### 6.1 关键要点

1. **`get_factor_kanban_values`**: 用于获取情绪因子的历史表现数据（IC、IR、收益等），用于因子筛选和评估
2. **`get_factor_values`**: 不支持情绪因子，仅支持CNE5/CNE6风格因子和Alpha101/191因子
3. **手动计算**: 需要手动计算情绪因子的当前值，使用`get_price`获取价格数据后计算
4. **性能优化**: 使用缓存和批量处理可以显著提升性能

### 6.2 推荐工作流程

1. **因子筛选**: 使用`get_factor_kanban_values`筛选IC>0.02的有效情绪因子
2. **实时计算**: 使用手动计算方法获取当前情绪因子值
3. **情绪判断**: 基于情绪因子值判断市场情绪状态
4. **策略应用**: 将情绪因子集成到多因子模型中

### 6.3 注意事项

- 情绪因子数据有延迟：T+2日凌晨3点后可用
- 情绪因子需要结合其他因子使用，单独使用效果有限
- 不同市场环境下，情绪因子的有效性会发生变化
- 建议定期回测验证情绪因子的有效性

---

**参考文档**:
- 聚宽API文档: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10439
- 因子看板API: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10450
- 因子统计API: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10451
