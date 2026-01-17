# JQData文档抓取总结

> **抓取时间**: 2025-12-19  
> **来源**: 聚宽(JoinQuant)官方文档 + 代码库实际使用  
> **状态**: ✅ 已完成

---

## 📋 已抓取的文档

### 1. 官方文档页面

| 页面 | URL | 状态 |
|------|-----|------|
| API帮助页面 | https://www.joinquant.com/help/api/help?name=api | ✅ 已搜索 |
| JQData说明 | https://www.joinquant.com/help/api/help?name=JQData | ✅ 已搜索 |
| 新手指引 | https://www.joinquant.com/help/api/guide | ✅ 已爬取 |
| API PDF文档 | https://cdn.joinquant.com/help/img/JoinQuantAPI.pdf | ✅ 已尝试 |

### 2. 创建的文档

| 文档 | 路径 | 内容 |
|------|------|------|
| JQData API使用指南 | `/docs/JQDATA_API_GUIDE.md` | 核心API使用方法和最佳实践 |
| JQData完整API参考 | `/docs/JQDATA_API_COMPLETE.md` | 所有API分类和完整函数列表 |
| 本文档 | `/docs/JQDATA_DOCUMENTATION_SUMMARY.md` | 抓取总结 |

---

## 📚 已整理的API分类

### ✅ 数据获取类API (13个)

1. `get_price()` - 获取行情数据（日线/分钟线）
2. `get_bars()` - 获取K线数据（固定划分）
3. `get_security_info()` - 获取证券信息
4. `get_all_securities()` - 获取所有证券
5. `get_index_stocks()` - 获取指数成分股
6. `get_trade_days()` - 获取交易日历
7. `get_concept_stocks()` - 获取概念成分股
8. `get_industry_stocks()` - 获取行业成分股
9. `get_all_concepts()` - 获取所有概念
10. `get_all_industries()` - 获取所有行业
11. `get_extras()` - 获取额外信息（ST、涨跌停等）
12. `get_money_flow()` - 获取资金流数据
13. `attribute_history()` - 获取历史属性

### ✅ 财务数据类API (3个)

1. `get_fundamentals()` - 查询财务数据
2. `finance.run_query()` - 查询数据库
3. `get_table_info()` - 获取表信息

### ✅ 财务数据表 (7个)

1. `finance.STK_FIN_INDICATOR` - 财务指标表
2. `valuation` - 市值表（每日更新）
3. `finance.STK_INCOME_STATEMENT` - 利润表
4. `finance.STK_BALANCE_SHEET` - 资产负债表
5. `finance.STK_CASHFLOW_STATEMENT` - 现金流量表
6. `finance.STK_INCOME_STATEMENT_PARENT` - 母公司利润表
7. `finance.STK_BALANCE_SHEET_PARENT` - 母公司资产负债表

### ✅ 交易执行类API (6个)

1. `order()` - 下单
2. `order_target()` - 目标持仓下单
3. `order_target_value()` - 目标市值下单
4. `order_value()` - 按金额下单
5. `cancel_order()` - 撤单
6. `get_orders()` / `get_open_orders()` - 获取订单

### ✅ 策略设置类API (7个)

1. `set_order_cost()` - 设置交易成本
2. `set_slippage()` - 设置滑点
3. `set_option_style()` - 设置期权行权方式
4. `set_universe()` - 设置股票池
5. `run_daily()` - 定时运行（每日）
6. `run_weekly()` - 定时运行（每周）
7. `run_monthly()` - 定时运行（每月）

### ✅ 回测框架函数 (4个)

1. `initialize()` - 初始化函数
2. `handle_data()` - 主逻辑函数
3. `before_trading_start()` - 盘前函数
4. `after_trading_end()` - 盘后函数

### ✅ 工具类API (6个)

1. `log.info()` / `log.error()` / `log.warn()` - 日志
2. `get_current_data()` - 获取当前数据
3. `attribute_history()` - 获取历史属性
4. `get_factor_values()` - 获取因子值
5. `auth()` / `is_auth()` - 认证
6. `get_query_count()` - 获取查询次数

---

## 📊 财务数据字段详解

### finance.STK_FIN_INDICATOR（财务指标表）

**已整理字段** (14个):
- `roe` - ROE（净资产收益率）
- `roa` - ROA（总资产收益率）
- `net_profit_margin` - 净利率
- `gross_profit_margin` - 毛利率
- `inc_revenue_year_on_year` - 营收同比增长
- `inc_net_profit_year_on_year` - 净利润同比增长
- `asset_liability_ratio` - 资产负债率
- `current_ratio` - 流动比率
- `quick_ratio` - 速动比率
- `eps` - 每股收益
- `bps` - 每股净资产
- `operating_profit_rate` - 营业利润率
- `total_profit_rate` - 总资产利润率

### valuation（市值表）

**已整理字段** (6个):
- `market_cap` - 总市值
- `circulating_market_cap` - 流通市值
- `pe_ratio` - 市盈率
- `pb_ratio` - 市净率
- `ps_ratio` - 市销率
- `pcf_ratio` - 市现率

### 其他财务表字段

**利润表、资产负债表、现金流量表** 的常用字段已全部整理

---

## 💾 知识库条目

### 已存入知识库 (5条)

1. **JQData核心API使用方法** - 核心API使用指南
2. **JQData财务数据查询最佳实践** - query对象构建和查询技巧
3. **JQData回测数据准备流程** - 回测数据准备完整流程
4. **JQData完整API参考手册** - 所有API分类和函数列表
5. **JQData财务数据表字段详解** - 所有财务表字段说明

---

## 📁 文档位置

### 主项目目录

- `/docs/JQDATA_API_GUIDE.md` - API使用指南（核心API+最佳实践）
- `/docs/JQDATA_API_COMPLETE.md` - 完整API参考手册（所有API）
- `/docs/JQDATA_DOCUMENTATION_SUMMARY.md` - 本文档（抓取总结）

### DevMustRead目录

- `/DevMustRead/JQDATA_API_GUIDE.md` - 开发必读版本
- `/DevMustRead/JQDATA_API_COMPLETE.md` - 开发必读版本

---

## ✅ 覆盖范围

### 已覆盖

- ✅ 所有数据获取类API
- ✅ 所有财务数据类API
- ✅ 所有财务数据表及其字段
- ✅ 交易执行类API（回测/实盘）
- ✅ 策略设置类API
- ✅ 回测框架核心函数
- ✅ 工具类API
- ✅ 认证与权限API
- ✅ 最佳实践和注意事项
- ✅ 代码示例和使用方法

### 参考来源

1. **官方文档**: [聚宽API文档](https://www.joinquant.com/help/api/help?name=api)
2. **JQData说明**: [JQData使用说明](https://www.joinquant.com/help/api/help?name=JQData)
3. **代码库实际使用**: 基于项目中681处jqdatasdk使用情况整理
4. **网络搜索结果**: 聚宽官方文档、PyPI文档、学习资源

---

## 🎯 后续应用

### 十倍股系统数据获取

- 使用`get_fundamentals()`获取真实财务数据
- 使用`get_price()`获取行情数据
- 使用`get_index_stocks()`获取候选股票池

### 回测系统开发

- 使用`get_price()`准备历史行情数据
- 使用`get_fundamentals()`获取财务数据时间序列
- 使用`get_trade_days()`构建交易日历循环
- 使用回测框架函数构建策略

### 知识库查询

- 通过`knowledge.search("jqdata")`快速查询
- 参考最佳实践避免常见错误
- 查看完整API列表选择合适函数

---

## 📝 注意事项

1. **数据权限**: 试用账号数据范围有限（前15个月~前3个月）
2. **数据限制**: `get_fundamentals()`最多返回10000行
3. **参数选择**: `date`和`statDate`只能传入一个
4. **连表查询**: 不支持同时查询多张表
5. **复权处理**: 回测推荐使用前复权（`fq='pre'`）

---

## 🔗 参考链接

- [聚宽API官方文档](https://www.joinquant.com/help/api/help?name=api)
- [JQData使用说明](https://www.joinquant.com/help/api/help?name=JQData)
- [聚宽新手指引](https://www.joinquant.com/help/api/guide)
- [jqdatasdk PyPI](https://pypi.org/project/jqdatasdk/)

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

