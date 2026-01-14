# 北向资金数据获取整合方案

> **更新日期**: 2026-01-13  
> **目的**: 整合聚宽(JQData)、AKShare和知识库，提供完整的北向资金数据获取方案

---

## 📊 数据源对比

| 数据源 | 接口 | 数据范围 | 更新频率 | 适用场景 | 限制 |
|--------|------|---------|---------|---------|------|
| **聚宽(JQData)** | `finance.STK_ML_QUOTA` | 2014-11-17 ~ 2024-08-16 | 每日收盘后 | 历史回测 | ⚠️ 2024-08-18后不再披露买卖分项 |
| **AKShare汇总** | `stock_hsgt_fund_flow_summary_em` | 当日数据 | 实时 | 实时监控 | ✅ 推荐 |
| **AKShare分时** | `stock_hsgt_fund_min_em` | 当日分时 | 盘中实时 | 盘中监控 | ⚠️ 盘后/盘前为空 |
| **AKShare历史** | `stock_hsgt_hist_em` | 2014-11-17 ~ 2024-08-16 | 延迟 | 历史分析 | ⚠️ 最新数据停在2024-08-16 |

---

## 🎯 推荐策略（按优先级）

### 1. 实时监控（推荐）

**使用**: `ak.stock_hsgt_fund_flow_summary_em()`

**优点**:
- ✅ 数据更新及时
- ✅ 包含沪股通、深股通分项
- ✅ 免费使用

**代码示例**:
```python
import akshare as ak

df = ak.stock_hsgt_fund_flow_summary_em()
north_df = df[df['资金方向'] == '北向']

# 计算合计
total_net = north_df['成交净买额'].sum()
sh_net = north_df[north_df['板块'] == '沪股通']['成交净买额'].iloc[0]
sz_net = north_df[north_df['板块'] == '深股通']['成交净买额'].iloc[0]

print(f"北向资金净买入: {total_net:.2f}亿元")
print(f"沪股通: {sh_net:.2f}亿元, 深股通: {sz_net:.2f}亿元")
```

---

### 2. 盘中实时监控

**使用**: `ak.stock_hsgt_fund_min_em()`

**优点**:
- ✅ 交易时间内实时更新
- ✅ 分时数据，可监控盘中变化

**代码示例**:
```python
df_min = ak.stock_hsgt_fund_min_em()
df_valid = df_min[df_min['北向资金'].notna()]

if not df_valid.empty:
    latest = df_valid.iloc[-1]
    print(f"时间: {latest['时间']}, 北向资金: {latest['北向资金']:.2f}亿")
```

---

### 3. 历史回测（2014-11 ~ 2024-08-16）

**使用**: 聚宽 `finance.STK_ML_QUOTA`

**优点**:
- ✅ 数据完整，包含买卖分项
- ✅ 适合历史回测

**代码示例**:
```python
import jqdatasdk as jq
from jqdatasdk import finance, query

q = query(
    finance.STK_ML_QUOTA.day,
    finance.STK_ML_QUOTA.link_id,
    finance.STK_ML_QUOTA.link_name,
    finance.STK_ML_QUOTA.buy_amount,
    finance.STK_ML_QUOTA.sell_amount,
    finance.STK_ML_QUOTA.sum_amount
).filter(
    finance.STK_ML_QUOTA.day >= '2024-08-10',
    finance.STK_ML_QUOTA.day <= '2024-08-16',
    finance.STK_ML_QUOTA.link_id.in_([310001, 310002])  # 沪股通、深股通
).order_by(
    finance.STK_ML_QUOTA.day.desc()
)

df = finance.run_query(q)
df['net_buy'] = df['buy_amount'] - df['sell_amount']
```

---

## 🔄 整合方案（降级策略）

### 完整的数据获取函数

```python
def get_northbound_flow(date=None, use_jqdata=True):
    """
    获取北向资金流向数据（整合方案）
    
    策略:
    1. 优先使用AKShare汇总数据（实时）
    2. 如果失败，尝试分时数据
    3. 如果是历史日期且需要买卖分项，使用JQData
    4. 如果JQData失败，使用AKShare历史数据
    
    Args:
        date: 目标日期（None表示当日）
        use_jqdata: 是否使用JQData（需要付费权限）
    
    Returns:
        dict: {
            'date': 日期,
            'total_net': 合计净买入(亿),
            'sh_net': 沪股通净买入(亿),
            'sz_net': 深股通净买入(亿),
            'source': 数据源
        }
    """
    import akshare as ak
    from datetime import datetime
    
    result = {
        'date': date or datetime.now().strftime('%Y-%m-%d'),
        'total_net': 0,
        'sh_net': 0,
        'sz_net': 0,
        'source': None
    }
    
    # 方案1: AKShare汇总数据（实时）
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is not None and not df.empty:
            north_df = df[df['资金方向'] == '北向']
            if not north_df.empty:
                sh_row = north_df[north_df['板块'] == '沪股通']
                sz_row = north_df[north_df['板块'] == '深股通']
                
                if not sh_row.empty and not sz_row.empty:
                    result['sh_net'] = float(sh_row['成交净买额'].iloc[0])
                    result['sz_net'] = float(sz_row['成交净买额'].iloc[0])
                    result['total_net'] = result['sh_net'] + result['sz_net']
                    result['source'] = 'AKShare汇总'
                    return result
    except Exception as e:
        print(f"AKShare汇总数据获取失败: {e}")
    
    # 方案2: AKShare分时数据
    try:
        df_min = ak.stock_hsgt_fund_min_em()
        if df_min is not None and not df_min.empty:
            df_valid = df_min[df_min['北向资金'].notna()]
            if not df_valid.empty:
                latest = df_valid.iloc[-1]
                result['total_net'] = float(latest['北向资金'])
                result['sh_net'] = float(latest['沪股通'])
                result['sz_net'] = float(latest['深股通'])
                result['source'] = 'AKShare分时'
                return result
    except Exception as e:
        print(f"AKShare分时数据获取失败: {e}")
    
    # 方案3: JQData（历史数据，需要付费）
    if use_jqdata and date:
        try:
            import jqdatasdk as jq
            from jqdatasdk import finance, query
            
            # 检查是否在披露范围内
            target_dt = datetime.strptime(date, '%Y-%m-%d')
            cutoff_dt = datetime.strptime('2024-08-16', '%Y-%m-%d')
            
            if target_dt <= cutoff_dt:
                q = query(
                    finance.STK_ML_QUOTA.day,
                    finance.STK_ML_QUOTA.link_id,
                    finance.STK_ML_QUOTA.buy_amount,
                    finance.STK_ML_QUOTA.sell_amount
                ).filter(
                    finance.STK_ML_QUOTA.day == date,
                    finance.STK_ML_QUOTA.link_id.in_([310001, 310002])
                )
                
                df = finance.run_query(q)
                if df is not None and not df.empty:
                    df['net_buy'] = df['buy_amount'] - df['sell_amount']
                    sh_net = df[df['link_id'] == 310001]['net_buy'].sum()
                    sz_net = df[df['link_id'] == 310002]['net_buy'].sum()
                    
                    result['sh_net'] = float(sh_net) / 1e8
                    result['sz_net'] = float(sz_net) / 1e8
                    result['total_net'] = result['sh_net'] + result['sz_net']
                    result['source'] = 'JQData'
                    return result
        except Exception as e:
            print(f"JQData获取失败: {e}")
    
    # 方案4: AKShare历史数据
    try:
        df_hist = ak.stock_hsgt_hist_em(symbol="北向资金")
        if df_hist is not None and not df_hist.empty:
            df_valid = df_hist[df_hist['当日成交净买额'].notna()]
            if not df_valid.empty:
                df_sorted = df_valid.sort_values('日期', ascending=False)
                latest = df_sorted.iloc[0]
                result['total_net'] = float(latest['当日成交净买额'])
                result['date'] = str(latest['日期'])
                result['source'] = 'AKShare历史'
                return result
    except Exception as e:
        print(f"AKShare历史数据获取失败: {e}")
    
    return result
```

---

## 📝 重要说明

### 1. 数据披露限制

- **聚宽(JQData)**: 2024-08-18之后不再披露买卖分项，只有成交总额
- **AKShare历史**: 最新数据可能停在2024-08-16
- **AKShare汇总**: 数据更新及时，但可能不包含买卖分项

### 2. 数据验证

建议对比多个数据源，确保数据准确性：
- 实时数据：对比 `stock_hsgt_fund_flow_summary_em` 和 `stock_hsgt_fund_min_em`
- 历史数据：对比 JQData 和 AKShare历史数据

### 3. 使用建议

- **实时监控**: 使用 `stock_hsgt_fund_flow_summary_em`（推荐）
- **盘中监控**: 使用 `stock_hsgt_fund_min_em`
- **历史回测**: 使用 JQData（2014-11 ~ 2024-08-16）+ AKShare（2024-08-16之后）
- **降级策略**: 主数据源失败时，自动切换到备选数据源

---

## 🔗 相关资源

- **知识库**: `.trquant/dev/knowledge/knowledge_base.json` - 北向资金行为映射
- **代码实现**: `core/astock_indicators.py` - `NorthFundAnalyzer`
- **代码实现**: `core/capital_flow.py` - `CapitalFlowAnalyzer.get_northbound_flow()`

---

**最后更新**: 2026-01-13
