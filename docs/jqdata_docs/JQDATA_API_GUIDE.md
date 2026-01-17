# JQData API 使用指南

> **来源**: 聚宽(JoinQuant)官方文档  
> **更新时间**: 2025-12-19  
> **用途**: 十倍股识别系统数据获取、回测数据准备

---

## 📚 目录

1. [安装与认证](#安装与认证)
2. [核心API](#核心api)
3. [行情数据](#行情数据)
4. [财务数据](#财务数据)
5. [指数与成分股](#指数与成分股)
6. [回测数据准备](#回测数据准备)
7. [最佳实践](#最佳实践)

---

## 安装与认证

### 安装

```bash
pip install jqdatasdk
```

### 认证

```python
from jqdatasdk import *

# 方式1: 直接认证
auth('your_username', 'your_password')

# 方式2: 检查认证状态
if not is_auth():
    auth('your_username', 'your_password')

# 方式3: 使用配置文件
from config.config_manager import get_config_manager
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
auth(jq_config['username'], jq_config['password'])
```

### 数据权限范围

- **试用账号**: 前15个月 ~ 前3个月
- **正式账号**: 不限制历史范围

---

## 核心API

### 1. get_price() - 获取行情数据

**功能**: 获取历史行情数据（K线数据）

**语法**:
```python
get_price(
    security,                    # 证券代码或代码列表
    start_date=None,            # 开始日期
    end_date=None,              # 结束日期
    frequency='daily',          # 频率: 'daily', '1d', '1m', '5m', '15m', '30m', '60m'
    fields=None,                # 字段: ['open', 'close', 'high', 'low', 'volume', 'money']
    skip_paused=False,          # 是否跳过停牌日
    fq='pre',                   # 复权: 'pre'(前复权), 'post'(后复权), None(不复权)
    count=None                  # 获取最近N条数据
)
```

**示例**:
```python
# 获取单只股票日线数据
df = get_price('000001.XSHE', 
                start_date='2023-01-01', 
                end_date='2023-12-31',
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume'])

# 获取多只股票
df = get_price(['000001.XSHE', '600519.XSHG'],
                start_date='2023-01-01',
                end_date='2023-12-31')

# 获取最近100条数据
df = get_price('000001.XSHE', count=100, frequency='daily')

# 获取分钟线数据（用于回测）
df = get_price('000001.XSHE',
                start_date='2023-01-01',
                end_date='2023-01-31',
                frequency='1m')  # 1分钟K线
```

**返回**: pandas.DataFrame，索引为datetime，列为fields指定的字段

**注意事项**:
- `get_price`使用移动窗口，更符合统计学划分
- 每个交易日按指定unit，从开盘时间开始划分到收盘
- 最多返回10000行数据

---

### 2. get_fundamentals() - 获取财务数据

**功能**: 查询财务数据（基本面数据）

**语法**:
```python
get_fundamentals(
    query_object,              # query查询对象
    date=None,                 # 指定交易日（收盘后能看到的最新数据）
    statDate=None              # 指定报告期（如'2023Q3', '2023'）
)
```

**query对象构建**:
```python
from jqdatasdk import query, finance

# 查询单表
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code == '600519.XSHG'
)

# 查询指定字段
q = query(
    finance.STK_FIN_INDICATOR.code,
    finance.STK_FIN_INDICATOR.roe,
    finance.STK_FIN_INDICATOR.net_profit_margin
).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE'])
)

# 查询多只股票
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE'])
)
```

**示例**:
```python
# 获取指定日期的财务数据
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code == '600519.XSHG'
)
df = get_fundamentals(q, date='2023-12-31')

# 获取指定报告期的财务数据
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code == '600519.XSHG'
)
df = get_fundamentals(q, statDate='2023Q3')  # 2023年第三季度

# 获取年度数据
df = get_fundamentals(q, statDate='2023')  # 2023年度（返回Q4数据）

# 查询多只股票
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE', '300750.XSHE'])
)
df = get_fundamentals(q, date='2023-12-31')
```

**常用财务表**:
- `finance.STK_FIN_INDICATOR` - 财务指标表（ROE、毛利率、净利率等）
- `finance.STK_INCOME_STATEMENT` - 利润表
- `finance.STK_BALANCE_SHEET` - 资产负债表
- `finance.STK_CASHFLOW_STATEMENT` - 现金流量表
- `valuation` - 市值表（每日更新）

**注意事项**:
- `date`和`statDate`参数只能传入一个
- 传入`date`时，查询指定日期收盘后能看到的最新数据
- 传入`statDate`时，查询指定报告期的数据
- 单季度财务数据使用`get_fundamentals`，年度数据使用`finance.run_query`
- 最多返回10000行数据
- 不支持连表查询

---

### 3. get_security_info() - 获取证券信息

**功能**: 获取单只证券的基本信息

**示例**:
```python
info = get_security_info('000001.XSHE')
print(info.display_name)  # 中文名称
print(info.name)           # 缩写简称
print(info.start_date)     # 上市日期
print(info.end_date)       # 退市日期（如果已退市）
```

---

### 4. get_all_securities() - 获取所有证券

**功能**: 获取所有证券列表

**示例**:
```python
# 获取所有股票
stocks = get_all_securities(types=['stock'], date='2023-12-31')
print(stocks.head())

# 获取所有指数
indices = get_all_securities(types=['index'], date='2023-12-31')
```

**返回**: pandas.DataFrame，索引为证券代码，包含display_name、start_date等字段

---

### 5. get_index_stocks() - 获取指数成分股

**功能**: 获取指定指数的成分股列表

**示例**:
```python
# 获取沪深300成分股
hs300 = get_index_stocks('000300.XSHG', date='2023-12-31')

# 获取创业板指成分股
cyb = get_index_stocks('399006.XSHE', date='2023-12-31')

# 获取中证500成分股
zz500 = get_index_stocks('000905.XSHG', date='2023-12-31')
```

**返回**: List[str]，证券代码列表

---

### 6. get_trade_days() - 获取交易日历

**功能**: 获取指定日期范围内的所有交易日

**示例**:
```python
# 获取2023年的所有交易日
trade_days = get_trade_days(start_date='2023-01-01', end_date='2023-12-31')

# 获取最近30个交易日
trade_days = get_trade_days(end_date='2023-12-31', count=30)
```

**返回**: List[datetime.date]

---

### 7. get_concept_stocks() - 获取概念板块成分股

**功能**: 获取指定概念板块的成分股

**示例**:
```python
# 获取"人工智能"概念成分股
ai_stocks = get_concept_stocks('GN001', date='2023-12-31')
```

**注意**: 需要先获取概念代码，可通过`get_all_concepts()`获取

---

### 8. get_industry_stocks() - 获取行业成分股

**功能**: 获取指定行业的成分股

**示例**:
```python
# 获取"银行"行业成分股
bank_stocks = get_industry_stocks('801780', date='2023-12-31')
```

---

## 行情数据

### 获取历史K线数据

```python
# 日线数据
daily = get_price('000001.XSHE',
                   start_date='2023-01-01',
                   end_date='2023-12-31',
                   frequency='daily')

# 分钟线数据（用于回测）
minute = get_price('000001.XSHE',
                    start_date='2023-01-01',
                    end_date='2023-01-31',
                    frequency='1m')  # 1分钟
```

### 获取复权数据

```python
# 前复权
df_pre = get_price('000001.XSHE',
                   start_date='2023-01-01',
                   end_date='2023-12-31',
                   fq='pre')

# 后复权
df_post = get_price('000001.XSHE',
                    start_date='2023-01-01',
                    end_date='2023-12-31',
                    fq='post')

# 不复权
df_none = get_price('000001.XSHE',
                    start_date='2023-01-01',
                    end_date='2023-12-31',
                    fq=None)
```

---

## 财务数据

### 常用财务指标

```python
from jqdatasdk import query, finance

# 查询财务指标
q = query(
    finance.STK_FIN_INDICATOR.code,
    finance.STK_FIN_INDICATOR.roe,                    # ROE
    finance.STK_FIN_INDICATOR.net_profit_margin,      # 净利率
    finance.STK_FIN_INDICATOR.gross_profit_margin,    # 毛利率
    finance.STK_FIN_INDICATOR.inc_revenue_year_on_year,  # 营收同比增长
    finance.STK_FIN_INDICATOR.inc_net_profit_year_on_year,  # 净利润同比增长
    finance.STK_FIN_INDICATOR.asset_liability_ratio,  # 资产负债率
    finance.STK_FIN_INDICATOR.current_ratio,          # 流动比率
    finance.STK_FIN_INDICATOR.quick_ratio              # 速动比率
).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE'])
)

df = get_fundamentals(q, date='2023-12-31')
```

### 查询市值数据

```python
from jqdatasdk import query, valuation

# 市值表每天更新
q = query(valuation).filter(
    valuation.code == '600519.XSHG'
)
df = get_fundamentals(q, date='2023-12-31')

# 获取多只股票的市值
q = query(valuation).filter(
    valuation.code.in_(['600519.XSHG', '000001.XSHE'])
)
df = get_fundamentals(q, date='2023-12-31')
```

### 查询利润表

```python
q = query(finance.STK_INCOME_STATEMENT).filter(
    finance.STK_INCOME_STATEMENT.code == '600519.XSHG'
)
df = get_fundamentals(q, statDate='2023Q3')
```

---

## 指数与成分股

### 获取指数成分股

```python
# 沪深300
hs300 = get_index_stocks('000300.XSHG')

# 中证500
zz500 = get_index_stocks('000905.XSHG')

# 创业板指
cyb = get_index_stocks('399006.XSHE')

# 中证1000
zz1000 = get_index_stocks('000852.XSHG')
```

### 获取所有概念列表

```python
concepts = get_all_concepts()
print(concepts.head())
```

### 获取所有行业列表

```python
industries = get_all_industries()
print(industries.head())
```

---

## 回测数据准备

### 准备历史行情数据

```python
from datetime import datetime, timedelta

# 准备回测期间的数据
start_date = '2023-01-01'
end_date = '2023-12-31'

# 获取候选股票池
candidate_stocks = get_index_stocks('000300.XSHG')

# 获取所有股票的行情数据
price_data = {}
for stock in candidate_stocks:
    try:
        df = get_price(stock,
                      start_date=start_date,
                      end_date=end_date,
                      frequency='daily',
                      fq='pre')
        price_data[stock] = df
    except Exception as e:
        print(f"获取{stock}数据失败: {e}")
```

### 准备财务数据

```python
# 获取季度财务数据
from jqdatasdk import query, finance

# 获取2023年各季度的财务数据
quarters = ['2023Q1', '2023Q2', '2023Q3', '2023Q4']
financial_data = {}

for quarter in quarters:
    q = query(finance.STK_FIN_INDICATOR).filter(
        finance.STK_FIN_INDICATOR.code.in_(candidate_stocks)
    )
    df = get_fundamentals(q, statDate=quarter)
    financial_data[quarter] = df
```

### 准备交易日历

```python
# 获取回测期间的交易日
trade_days = get_trade_days(start_date=start_date, end_date=end_date)

# 用于回测循环
for trade_day in trade_days:
    # 回测逻辑
    pass
```

---

## 最佳实践

### 1. 认证管理

```python
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

class JQDataManager:
    def __init__(self):
        self.client = JQDataClient()
        self._ensure_auth()
    
    def _ensure_auth(self):
        if not self.client.is_authenticated():
            cm = get_config_manager()
            jq_config = cm.get_jqdata_config()
            self.client.authenticate(jq_config['username'], jq_config['password'])
    
    def get_price(self, *args, **kwargs):
        self._ensure_auth()
        return self.client.get_price(*args, **kwargs)
```

### 2. 批量获取数据

```python
def batch_get_price(stocks, start_date, end_date, **kwargs):
    """批量获取行情数据"""
    results = {}
    for stock in stocks:
        try:
            df = get_price(stock, start_date=start_date, end_date=end_date, **kwargs)
            results[stock] = df
        except Exception as e:
            print(f"获取{stock}失败: {e}")
    return results
```

### 3. 数据缓存

```python
import pickle
from datetime import datetime

def get_price_cached(stock, start_date, end_date, cache_dir='./cache'):
    """带缓存的获取价格数据"""
    cache_file = f"{cache_dir}/{stock}_{start_date}_{end_date}.pkl"
    
    # 检查缓存
    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if (datetime.now().timestamp() - mtime) < 3600:  # 1小时内
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
    
    # 获取数据
    df = get_price(stock, start_date=start_date, end_date=end_date)
    
    # 保存缓存
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(df, f)
    
    return df
```

### 4. 错误处理

```python
def safe_get_price(stock, start_date, end_date, retry=3):
    """安全获取价格数据，带重试"""
    for i in range(retry):
        try:
            return get_price(stock, start_date=start_date, end_date=end_date)
        except Exception as e:
            if i == retry - 1:
                raise
            time.sleep(1)
    return None
```

### 5. 数据验证

```python
def validate_price_data(df):
    """验证价格数据"""
    if df is None or len(df) == 0:
        return False
    
    # 检查必要字段
    required_fields = ['open', 'close', 'high', 'low', 'volume']
    if not all(field in df.columns for field in required_fields):
        return False
    
    # 检查数据合理性
    if (df['high'] < df['low']).any():
        return False
    
    if (df['close'] > df['high']).any() or (df['close'] < df['low']).any():
        return False
    
    return True
```

---

## 常见问题

### Q1: 如何获取连续多个季度的财务数据？

```python
quarters = ['2023Q1', '2023Q2', '2023Q3', '2023Q4']
all_data = []

for quarter in quarters:
    q = query(finance.STK_FIN_INDICATOR).filter(
        finance.STK_FIN_INDICATOR.code == '600519.XSHG'
    )
    df = get_fundamentals(q, statDate=quarter)
    df['quarter'] = quarter
    all_data.append(df)

result = pd.concat(all_data, ignore_index=True)
```

### Q2: 如何获取所有A股的最新财务数据？

```python
# 获取所有股票
all_stocks = get_all_securities(types=['stock']).index.tolist()

# 分批获取（避免数据量过大）
batch_size = 100
all_financial = []

for i in range(0, len(all_stocks), batch_size):
    batch = all_stocks[i:i+batch_size]
    q = query(finance.STK_FIN_INDICATOR).filter(
        finance.STK_FIN_INDICATOR.code.in_(batch)
    )
    df = get_fundamentals(q, date='2023-12-31')
    all_financial.append(df)

result = pd.concat(all_financial, ignore_index=True)
```

### Q3: 如何计算技术指标？

```python
# 获取价格数据
df = get_price('000001.XSHE', count=60, frequency='daily')

# 计算移动平均
df['ma5'] = df['close'].rolling(5).mean()
df['ma20'] = df['close'].rolling(20).mean()
df['ma60'] = df['close'].rolling(60).mean()

# 计算RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['rsi'] = calculate_rsi(df['close'])
```

---

## 参考资料

- [JQData官方文档](https://www.joinquant.com/help/api/help?name=JQData)
- [聚宽API文档](https://www.joinquant.com/help/api/help?name=api)
- [jqdatasdk PyPI](https://pypi.org/project/jqdatasdk/)

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

