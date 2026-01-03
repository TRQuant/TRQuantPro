# JQData API 完整参考手册

> **来源**: 聚宽(JoinQuant)官方文档 + 代码库实际使用  
> **更新时间**: 2025-12-19  
> **参考链接**: [聚宽API文档](https://www.joinquant.com/help/api/help?name=api)

---

## 📚 目录

1. [认证与权限](#认证与权限)
2. [数据获取类API](#数据获取类api)
3. [财务数据类API](#财务数据类api)
4. [交易执行类API](#交易执行类api)
5. [策略设置类API](#策略设置类api)
6. [工具类API](#工具类api)
7. [完整API列表](#完整api列表)

---

## 认证与权限

### auth() - 用户认证

```python
from jqdatasdk import auth

auth('username', 'password')
```

### is_auth() - 检查认证状态

```python
from jqdatasdk import is_auth

if not is_auth():
    auth('username', 'password')
```

### get_query_count() - 获取查询次数

```python
from jqdatasdk import get_query_count

count = get_query_count()
print(f"剩余查询次数: {count.get('spare', 'N/A')}")
```

---

## 数据获取类API

### 1. get_price() - 获取行情数据

**功能**: 获取历史K线数据

**完整参数**:
```python
get_price(
    security,                    # 证券代码或代码列表
    start_date=None,            # 开始日期 'YYYY-MM-DD'
    end_date=None,              # 结束日期 'YYYY-MM-DD'
    frequency='daily',          # 频率: 'daily', '1d', '1m', '5m', '15m', '30m', '60m', 'week', 'month'
    fields=None,                # 字段: ['open', 'close', 'high', 'low', 'volume', 'money']
    skip_paused=False,          # 是否跳过停牌日
    fq='pre',                   # 复权: 'pre'(前复权), 'post'(后复权), None(不复权)
    count=None,                 # 获取最近N条数据
    panel=False                 # 是否返回Panel格式
)
```

**示例**:
```python
# 日线数据
df = get_price('000001.XSHE', 
                start_date='2023-01-01', 
                end_date='2023-12-31',
                frequency='daily')

# 分钟线数据
df = get_price('000001.XSHE',
                start_date='2023-01-01',
                end_date='2023-01-31',
                frequency='1m')

# 多只股票
df = get_price(['000001.XSHE', '600519.XSHG'],
                start_date='2023-01-01',
                end_date='2023-12-31')

# 最近100条
df = get_price('000001.XSHE', count=100, frequency='daily')
```

---

### 2. get_bars() - 获取K线数据（固定划分）

**功能**: 每个交易日按指定unit，固定从开盘时间开始划分到收盘

**参数**:
```python
get_bars(
    security,                   # 证券代码
    count,                      # 数量
    unit,                       # 单位: '1m', '5m', '15m', '30m', '60m', '1d', '1w', '1M'
    fields=['date', 'open', 'high', 'low', 'close', 'volume'],
    include_now=False,          # 是否包含当前未完成的K线
    end_dt=None,                # 结束时间
    fq_ref_date=None            # 复权基准日期
)
```

**与get_price的区别**:
- `get_price`: 移动窗口，更符合统计学划分
- `get_bars`: 固定划分，与主流行情软件相同

---

### 3. get_security_info() - 获取证券信息

```python
info = get_security_info('000001.XSHE')
print(info.display_name)  # 中文名称
print(info.name)           # 缩写简称
print(info.start_date)     # 上市日期
print(info.end_date)       # 退市日期
```

---

### 4. get_all_securities() - 获取所有证券

```python
# 获取所有股票
stocks = get_all_securities(types=['stock'], date='2023-12-31')

# 获取所有指数
indices = get_all_securities(types=['index'], date='2023-12-31')

# 获取所有基金
funds = get_all_securities(types=['fund'], date='2023-12-31')
```

**返回**: pandas.DataFrame，索引为证券代码

---

### 5. get_index_stocks() - 获取指数成分股

```python
# 沪深300
hs300 = get_index_stocks('000300.XSHG', date='2023-12-31')

# 中证500
zz500 = get_index_stocks('000905.XSHG', date='2023-12-31')

# 创业板指
cyb = get_index_stocks('399006.XSHE', date='2023-12-31')

# 中证1000
zz1000 = get_index_stocks('000852.XSHG', date='2023-12-31')
```

**返回**: List[str]，证券代码列表

---

### 6. get_trade_days() - 获取交易日历

```python
# 获取日期范围
trade_days = get_trade_days(start_date='2023-01-01', end_date='2023-12-31')

# 获取最近N个交易日
trade_days = get_trade_days(end_date='2023-12-31', count=30)
```

**返回**: List[datetime.date]

---

### 7. get_concept_stocks() - 获取概念板块成分股

```python
# 先获取概念列表
concepts = get_all_concepts()

# 获取概念成分股
ai_stocks = get_concept_stocks('GN001', date='2023-12-31')
```

---

### 8. get_industry_stocks() - 获取行业成分股

```python
# 先获取行业列表
industries = get_all_industries()

# 获取行业成分股
bank_stocks = get_industry_stocks('801780', date='2023-12-31')
```

---

### 9. get_all_concepts() - 获取所有概念

```python
concepts = get_all_concepts()
print(concepts.head())
```

---

### 10. get_all_industries() - 获取所有行业

```python
industries = get_all_industries(date='2023-12-31')
print(industries.head())
```

---

### 11. get_extras() - 获取额外信息

```python
# 获取是否ST
is_st = get_extras('is_st', ['000001.XSHE', '600519.XSHG'], 
                   start_date='2023-01-01', end_date='2023-12-31')

# 获取涨跌停
limit_info = get_extras('is_st', ['000001.XSHE'], 
                        start_date='2023-01-01', end_date='2023-12-31')
```

---

### 12. get_money_flow() - 获取资金流数据

```python
# 获取主力资金净流入
money_flow = get_money_flow(['000001.XSHE'],
                            start_date='2023-01-01',
                            end_date='2023-12-31')
```

---

## 财务数据类API

### 1. get_fundamentals() - 获取财务数据

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

# 单表查询
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code == '600519.XSHG'
)

# 多只股票
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE'])
)

# 指定字段
q = query(
    finance.STK_FIN_INDICATOR.code,
    finance.STK_FIN_INDICATOR.roe,
    finance.STK_FIN_INDICATOR.net_profit_margin
).filter(
    finance.STK_FIN_INDICATOR.code.in_(['600519.XSHG', '000001.XSHE'])
)
```

**常用财务表**:

| 表名 | 说明 | 更新频率 |
|------|------|----------|
| `finance.STK_FIN_INDICATOR` | 财务指标表 | 季度 |
| `finance.STK_INCOME_STATEMENT` | 利润表 | 季度 |
| `finance.STK_BALANCE_SHEET` | 资产负债表 | 季度 |
| `finance.STK_CASHFLOW_STATEMENT` | 现金流量表 | 季度 |
| `valuation` | 市值表 | 每日 |
| `finance.STK_INCOME_STATEMENT_PARENT` | 母公司利润表 | 季度 |
| `finance.STK_BALANCE_SHEET_PARENT` | 母公司资产负债表 | 季度 |

**常用财务指标字段**:

| 字段 | 说明 |
|------|------|
| `roe` | ROE（净资产收益率） |
| `net_profit_margin` | 净利率 |
| `gross_profit_margin` | 毛利率 |
| `inc_revenue_year_on_year` | 营收同比增长 |
| `inc_net_profit_year_on_year` | 净利润同比增长 |
| `asset_liability_ratio` | 资产负债率 |
| `current_ratio` | 流动比率 |
| `quick_ratio` | 速动比率 |
| `eps` | 每股收益 |
| `bps` | 每股净资产 |

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

# 查询市值数据（每天更新）
q = query(valuation).filter(
    valuation.code == '600519.XSHG'
)
df = get_fundamentals(q, date='2023-12-31')
```

---

### 2. finance.run_query() - 查询数据库

**功能**: 查询数据库中的数据（用于年度数据、历史数据）

**语法**:
```python
finance.run_query(query_object)
```

**示例**:
```python
# 查询年度财务数据
q = query(finance.STK_FIN_INDICATOR).filter(
    finance.STK_FIN_INDICATOR.code == '600519.XSHG',
    finance.STK_FIN_INDICATOR.statDate == '2023'
)
df = finance.run_query(q)
```

**注意事项**:
- 最多返回5000行
- 不支持连表查询

---

### 3. get_table_info() - 获取表信息

```python
# 获取表的字段信息
info = get_table_info(finance.STK_FIN_INDICATOR)
print(info)
```

---

## 交易执行类API（回测/实盘）

### 1. order() - 下单

```python
# 按股数下单
order('000001.XSHE', 100)  # 买入100股

# 按金额下单
order_value('000001.XSHE', 10000)  # 买入10000元

# 按目标持仓下单
order_target('000001.XSHE', 1000)  # 调整持仓至1000股

# 按目标市值下单
order_target_value('000001.XSHE', 100000)  # 调整市值至100000元
```

---

### 2. order_target() - 目标持仓下单

```python
# 调整持仓至目标数量
order_target('000001.XSHE', 1000)
```

---

### 3. order_target_value() - 目标市值下单

```python
# 调整持仓至目标市值
order_target_value('000001.XSHE', 100000)
```

---

### 4. order_value() - 按金额下单

```python
# 买入指定金额
order_value('000001.XSHE', 10000)
```

---

### 5. cancel_order() - 撤单

```python
# 撤销指定订单
cancel_order(order_id)
```

---

### 6. get_orders() - 获取订单

```python
# 获取所有订单
orders = get_orders()

# 获取指定订单
order = get_orders(order_id)
```

---

### 7. get_open_orders() - 获取未完成订单

```python
open_orders = get_open_orders()
```

---

## 策略设置类API

### 1. set_order_cost() - 设置交易成本

```python
from jqdatasdk import OrderCost

# 设置股票交易成本
set_order_cost(
    OrderCost(
        open_tax=0,              # 买入印花税
        close_tax=0.001,         # 卖出印花税
        open_commission=0.0003,  # 买入佣金
        close_commission=0.0003, # 卖出佣金
        min_commission=5         # 最低佣金
    ),
    type='stock'
)
```

---

### 2. set_slippage() - 设置滑点

```python
from jqdatasdk import FixedSlippage, PriceRelatedSlippage

# 固定滑点
set_slippage(FixedSlippage(0.001))  # 0.1%

# 价格相关滑点
set_slippage(PriceRelatedSlippage(0.002))  # 0.2%
```

---

### 3. set_option_style() - 设置期权行权方式

```python
from jqdatasdk import OPTION_STYLE_EUROPEAN, OPTION_STYLE_AMERICAN

set_option_style(OPTION_STYLE_EUROPEAN)  # 欧式期权
```

---

### 4. set_universe() - 设置股票池

```python
# 设置股票池
set_universe(['000001.XSHE', '600519.XSHG'])
```

---

### 5. run_daily() - 定时运行

```python
# 每天运行
run_daily(func, time='09:30')

# 每周运行
run_weekly(func, weekday=1, time='09:30')  # 周一

# 每月运行
run_monthly(func, monthday=1, time='09:30')  # 每月1号
```

---

### 6. run_weekly() - 每周运行

```python
run_weekly(func, weekday=1, time='09:30')
```

---

### 7. run_monthly() - 每月运行

```python
run_monthly(func, monthday=1, time='09:30')
```

---

## 工具类API

### 1. log.info() / log.error() / log.warn() - 日志

```python
log.info('信息')
log.error('错误')
log.warn('警告')
```

---

### 2. get_current_data() - 获取当前数据

```python
# 获取当前行情数据
current_data = get_current_data()
for stock in current_data:
    print(f"{stock}: {current_data[stock].last_price}")
```

---

### 3. attribute_history() - 获取历史属性

```python
# 获取历史收盘价
hist = attribute_history('000001.XSHE', 20, '1d', ['close'])
```

---

### 4. get_factor_values() - 获取因子值

```python
# 获取因子值
factor_values = get_factor_values(
    securities=['000001.XSHE'],
    factors=['pe_ratio', 'pb_ratio'],
    start_date='2023-01-01',
    end_date='2023-12-31'
)
```

---

## 完整API列表

### 数据获取类（Data）

| API | 功能 | 返回类型 |
|-----|------|----------|
| `get_price()` | 获取行情数据 | DataFrame |
| `get_bars()` | 获取K线数据（固定划分） | List |
| `get_security_info()` | 获取证券信息 | SecurityInfo |
| `get_all_securities()` | 获取所有证券 | DataFrame |
| `get_index_stocks()` | 获取指数成分股 | List[str] |
| `get_trade_days()` | 获取交易日历 | List[date] |
| `get_concept_stocks()` | 获取概念成分股 | List[str] |
| `get_industry_stocks()` | 获取行业成分股 | List[str] |
| `get_all_concepts()` | 获取所有概念 | DataFrame |
| `get_all_industries()` | 获取所有行业 | DataFrame |
| `get_extras()` | 获取额外信息 | DataFrame |
| `get_money_flow()` | 获取资金流数据 | DataFrame |
| `get_fundamentals()` | 获取财务数据 | DataFrame |
| `finance.run_query()` | 查询数据库 | DataFrame |
| `get_table_info()` | 获取表信息 | Dict |

### 交易执行类（Trading）

| API | 功能 | 返回类型 |
|-----|------|----------|
| `order()` | 下单 | Order |
| `order_target()` | 目标持仓下单 | Order |
| `order_target_value()` | 目标市值下单 | Order |
| `order_value()` | 按金额下单 | Order |
| `cancel_order()` | 撤单 | None |
| `get_orders()` | 获取订单 | List[Order] |
| `get_open_orders()` | 获取未完成订单 | List[Order] |

### 策略设置类（Strategy）

| API | 功能 | 返回类型 |
|-----|------|----------|
| `set_order_cost()` | 设置交易成本 | None |
| `set_slippage()` | 设置滑点 | None |
| `set_option_style()` | 设置期权行权方式 | None |
| `set_universe()` | 设置股票池 | None |
| `run_daily()` | 定时运行（每日） | None |
| `run_weekly()` | 定时运行（每周） | None |
| `run_monthly()` | 定时运行（每月） | None |

### 工具类（Utils）

| API | 功能 | 返回类型 |
|-----|------|----------|
| `log.info()` | 信息日志 | None |
| `log.error()` | 错误日志 | None |
| `log.warn()` | 警告日志 | None |
| `get_current_data()` | 获取当前数据 | Dict |
| `attribute_history()` | 获取历史属性 | DataFrame |
| `get_factor_values()` | 获取因子值 | DataFrame |

### 认证类（Auth）

| API | 功能 | 返回类型 |
|-----|------|----------|
| `auth()` | 用户认证 | None |
| `is_auth()` | 检查认证状态 | bool |
| `get_query_count()` | 获取查询次数 | Dict |

---

## 财务数据表详细说明

### finance.STK_FIN_INDICATOR - 财务指标表

**常用字段**:
- `code`: 股票代码
- `statDate`: 报告期
- `roe`: ROE（净资产收益率）
- `roa`: ROA（总资产收益率）
- `net_profit_margin`: 净利率
- `gross_profit_margin`: 毛利率
- `inc_revenue_year_on_year`: 营收同比增长
- `inc_net_profit_year_on_year`: 净利润同比增长
- `asset_liability_ratio`: 资产负债率
- `current_ratio`: 流动比率
- `quick_ratio`: 速动比率
- `eps`: 每股收益
- `bps`: 每股净资产
- `operating_profit_rate`: 营业利润率
- `total_profit_rate`: 总资产利润率

### valuation - 市值表

**常用字段**:
- `code`: 股票代码
- `day`: 日期
- `market_cap`: 总市值
- `circulating_market_cap`: 流通市值
- `pe_ratio`: 市盈率
- `pb_ratio`: 市净率
- `ps_ratio`: 市销率
- `pcf_ratio`: 市现率

### finance.STK_INCOME_STATEMENT - 利润表

**常用字段**:
- `code`: 股票代码
- `statDate`: 报告期
- `operating_revenue`: 营业收入
- `operating_cost`: 营业成本
- `operating_profit`: 营业利润
- `total_profit`: 利润总额
- `net_profit`: 净利润
- `net_profit_after_nrgal`: 扣非净利润

### finance.STK_BALANCE_SHEET - 资产负债表

**常用字段**:
- `code`: 股票代码
- `statDate`: 报告期
- `total_assets`: 总资产
- `total_liability`: 总负债
- `total_equity`: 股东权益
- `current_assets`: 流动资产
- `current_liability`: 流动负债
- `fixed_assets`: 固定资产

### finance.STK_CASHFLOW_STATEMENT - 现金流量表

**常用字段**:
- `code`: 股票代码
- `statDate`: 报告期
- `operating_cash_flow`: 经营活动现金流
- `investing_cash_flow`: 投资活动现金流
- `financing_cash_flow`: 筹资活动现金流
- `net_cash_flow`: 净现金流

---

## 回测框架核心函数

### initialize() - 初始化函数

```python
def initialize(context):
    # 设置股票池
    g.stocks = ['000001.XSHE', '600519.XSHG']
    
    # 设置交易成本
    set_order_cost(...)
    
    # 设置滑点
    set_slippage(...)
```

### handle_data() - 主逻辑函数

```python
def handle_data(context, data):
    # 每个交易日执行
    for stock in g.stocks:
        # 交易逻辑
        pass
```

### before_trading_start() - 盘前函数

```python
def before_trading_start(context):
    # 每个交易日开始前执行
    pass
```

### after_trading_end() - 盘后函数

```python
def after_trading_end(context):
    # 每个交易日结束后执行
    pass
```

---

## 常用数据表索引

### 财务数据表

| 表名 | 说明 | 查询方式 |
|------|------|----------|
| `finance.STK_FIN_INDICATOR` | 财务指标 | `get_fundamentals()` |
| `finance.STK_INCOME_STATEMENT` | 利润表 | `get_fundamentals()` |
| `finance.STK_BALANCE_SHEET` | 资产负债表 | `get_fundamentals()` |
| `finance.STK_CASHFLOW_STATEMENT` | 现金流量表 | `get_fundamentals()` |
| `finance.STK_INCOME_STATEMENT_PARENT` | 母公司利润表 | `get_fundamentals()` |
| `finance.STK_BALANCE_SHEET_PARENT` | 母公司资产负债表 | `get_fundamentals()` |
| `valuation` | 市值表 | `get_fundamentals()` |

### 行业概念表

| 表名 | 说明 | 查询方式 |
|------|------|----------|
| `finance.SW1` | 申万一级行业 | `get_industry_stocks()` |
| `finance.SW2` | 申万二级行业 | `get_industry_stocks()` |
| `finance.SW3` | 申万三级行业 | `get_industry_stocks()` |

---

## 注意事项

### 1. 数据权限

- **试用账号**: 前15个月 ~ 前3个月
- **正式账号**: 不限制历史范围

### 2. 数据限制

- `get_fundamentals()`: 最多返回10000行
- `finance.run_query()`: 最多返回5000行
- 不支持连表查询

### 3. 日期参数

- `date`: 指定交易日，获取收盘后能看到的最新数据
- `statDate`: 指定报告期，如'2023Q3'(季度)或'2023'(年度)
- `date`和`statDate`只能传入一个

### 4. 复权处理

- `fq='pre'`: 前复权（推荐用于回测）
- `fq='post'`: 后复权
- `fq=None`: 不复权

### 5. 频率参数

- `'daily'` 或 `'1d'`: 日线
- `'1m'`, `'5m'`, `'15m'`, `'30m'`, `'60m'`: 分钟线
- `'week'`: 周线
- `'month'`: 月线

---

## 参考资料

- [聚宽API官方文档](https://www.joinquant.com/help/api/help?name=api)
- [JQData使用说明](https://www.joinquant.com/help/api/help?name=JQData)
- [聚宽新手指引](https://www.joinquant.com/help/api/guide)
- [jqdatasdk PyPI](https://pypi.org/project/jqdatasdk/)

---

*文档版本: 2.0 | 创建时间: 2025-12-19 | 最后更新: 2025-12-19*

