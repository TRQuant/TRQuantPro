# 聚宽API知识库

> **构建时间**: 2025-12-19  
> **来源**: 聚宽官方文档（33个页面）  
> **状态**: ✅ 已构建完成

---

## 📊 知识库统计

| 指标 | 数值 |
|------|------|
| **总API函数** | 315个 |
| **知识库条目** | 27个 |
| **分类数量** | 10个 |
| **详细文档** | 17个 |

---

## 📚 API分类

### 1. 数据获取 (17个)

**核心API**:
- `get_price()` - 获取行情数据（日线/分钟线）
- `get_bars()` - 获取K线数据
- `history()` - 获取历史数据
- `attribute_history()` - 获取历史属性
- `get_index_stocks()` - 获取指数成分股
- `get_industry_stocks()` - 获取行业成分股
- `get_concept_stocks()` - 获取概念成分股
- `get_all_securities()` - 获取所有证券
- `get_trade_days()` - 获取交易日历
- `get_money_flow()` - 获取资金流数据

**知识库条目**: `聚宽API - 数据获取`

---

### 2. 财务数据 (8个)

**核心API**:
- `get_fundamentals()` - 查询财务数据
- `get_fundamentals_continuously()` - 查询多日财务数据
- `get_valuation()` - 获取市值表数据
- `get_history_fundamentals()` - 获取历史财务数据
- `finance.run_query()` - 查询数据库

**知识库条目**: `聚宽API - 财务数据`

---

### 3. 交易执行 (18个)

**核心API**:
- `order()` - 按数量下单
- `order_target()` - 目标数量下单
- `order_value()` - 按金额下单
- `order_target_value()` - 目标金额下单
- `cancel_order()` - 取消订单

**知识库条目**: `聚宽API - 交易执行`

---

### 4. 策略设置 (11个)

**核心API**:
- `initialize()` - 初始化函数
- `handle_data()` - 主逻辑函数
- `before_trading_start()` - 交易前运行
- `after_trading_end()` - 交易后运行
- `run_daily()` - 每日运行
- `set_benchmark()` - 设置基准
- `set_option()` - 设置选项

**知识库条目**: `聚宽API - 策略设置`

---

### 5. 因子分析 (5个)

**核心API**:
- `get_factor_values()` - 获取因子值
- `get_factor_kanban_values()` - 获取因子看板数据
- `alpha_001()` - Alpha 101因子
- `alpha_191()` - Alpha 191因子

**知识库条目**: `聚宽API - 因子分析`

---

### 6. 技术指标 (32个)

**核心API**:
- `GDX()` - 济安线
- `MA()` - 移动平均
- `MACD()` - MACD指标
- `RSI()` - 相对强弱指标

**知识库条目**: `聚宽API - 技术指标`

---

### 7. 融资融券 (8个)

**核心API**:
- `margincash_open()` - 融资买入
- `margincash_close()` - 卖券还款
- `marginsec_open()` - 融券卖出
- `marginsec_close()` - 买券还券
- `get_mtss()` - 获取融资融券信息
- `get_margincash_stocks()` - 获取融资标的
- `get_marginsec_stocks()` - 获取融券标的

**知识库条目**: `聚宽API - 融资融券`

---

### 8. 期货 (21个)

**核心API**:
- `get_dominant_future()` - 获取主力合约
- `get_future_contracts()` - 获取期货合约列表
- `futures_margin_rate()` - 设置保证金比例
- `order()` - 期货下单（支持多空）

**知识库条目**: `聚宽API - 期货`

---

### 9. Tick级 (6个)

**核心API**:
- `handle_tick()` - Tick事件处理
- `subscribe()` - 订阅Tick事件
- `unsubscribe()` - 取消订阅
- `get_call_auction()` - 获取集合竞价数据

**知识库条目**: `聚宽API - Tick级`

---

### 10. 其他 (221个)

包含各种辅助函数、工具函数等。

**知识库条目**: `聚宽API - 其他`

---

## 🔍 详细API文档

以下API已提取详细文档（参数、返回值、示例）：

1. ✅ `get_price` - 获取行情数据
2. ✅ `get_fundamentals` - 查询财务数据
3. ✅ `get_index_stocks` - 获取指数成分股
4. ✅ `get_industry_stocks` - 获取行业成分股
5. ✅ `get_concept_stocks` - 获取概念成分股
6. ✅ `get_all_securities` - 获取所有证券
7. ✅ `get_trade_days` - 获取交易日历
8. ✅ `get_money_flow` - 获取资金流数据
9. ✅ `order` - 按数量下单
10. ✅ `order_target` - 目标数量下单
11. ✅ `order_value` - 按金额下单
12. ✅ `initialize` - 初始化函数
13. ✅ `handle_data` - 主逻辑函数
14. ✅ `history` - 获取历史数据
15. ✅ `attribute_history` - 获取历史属性
16. ✅ `get_valuation` - 获取市值表数据
17. ✅ `get_fundamentals_continuously` - 查询多日财务数据

---

## 📖 如何使用知识库

### 1. 搜索API文档

```python
# 使用MCP工具搜索
mcp_xuanyuan_knowledge_search(query="聚宽API get_price")
```

### 2. 按分类查找

```python
# 搜索特定分类
mcp_xuanyuan_knowledge_search(query="聚宽API 数据获取")
mcp_xuanyuan_knowledge_search(query="聚宽API 交易执行")
```

### 3. 查找详细文档

```python
# 搜索特定API的详细文档
mcp_xuanyuan_knowledge_search(query="聚宽API get_fundamentals 参数")
```

---

## 📁 文件位置

### 1. API索引
- **路径**: `docs/joinquant_crawled/api_index.json`
- **内容**: 所有315个API的索引和分类

### 2. 原始文档
- **路径**: `docs/joinquant_crawled/texts_enhanced/`
- **内容**: 33个原始文本文件

### 3. 知识库条目
- **位置**: MCP知识库系统
- **数量**: 27个条目
- **标签**: `joinquant`, `api`, `reference`

---

## 🎯 使用示例

### 示例1: 获取股票价格

```python
# 搜索知识库
knowledge = mcp_xuanyuan_knowledge_search(query="聚宽API get_price 如何使用")

# 从知识库获取示例代码
# get_price(security, start_date=None, end_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None)
```

### 示例2: 查询财务数据

```python
# 搜索知识库
knowledge = mcp_xuanyuan_knowledge_search(query="聚宽API get_fundamentals 参数说明")

# 从知识库获取参数说明
# query_object: Query对象
# date: 查询日期
# statDate: 财报统计日期
```

---

## ✅ 知识库特性

1. **结构化存储**: 按分类组织，便于查找
2. **详细文档**: 17个核心API包含完整文档
3. **代码示例**: 包含实际使用示例
4. **参数说明**: 详细的参数和返回值说明
5. **可搜索**: 通过MCP工具快速搜索

---

## 🔄 更新计划

1. **定期更新**: 每月重新爬取和解析
2. **补充示例**: 添加更多实际使用示例
3. **扩展分类**: 根据使用情况调整分类
4. **优化搜索**: 改进搜索算法和标签

---

## 📝 注意事项

1. **API版本**: 文档基于当前聚宽平台版本
2. **数据权限**: 部分API需要特定数据权限
3. **回测环境**: 某些API仅在回测或研究环境可用
4. **参数格式**: 注意参数类型和格式要求

---

*知识库版本: 1.0 | 更新时间: 2025-12-19*

