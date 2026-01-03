# 聚宽API知识库使用示例

> **目的**: 展示如何在实际开发中使用知识库查找和使用聚宽API

---

## 📖 场景1: 开发数据获取功能

### 需求
需要获取股票的历史价格数据，但不确定API的具体用法。

### 步骤1: 搜索知识库

```python
import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')
from mcp_servers.unified_dev_server import knowledge_search

# 搜索get_price API
result = knowledge_search("get_price")
print(f"找到 {result['total']} 个相关条目")

# 查看最相关的结果
if result['results']:
    best_match = result['results'][0]
    print(f"\n标题: {best_match['title']}")
    print(f"内容预览: {best_match['content'][:200]}...")
```

### 步骤2: 从知识库获取完整信息

```python
# 获取完整的API文档
api_doc = result['results'][0]['content']
print(api_doc)
```

**输出示例**:
```
# get_price

**函数签名**: `get_price(security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)`

## 参数
- **security**: 一只str格式的股票代码或期货代码，或者一个list格式的股票或者期货列表
- **start_date**: 开始日期
- **end_date**: 结束日期
...
```

### 步骤3: 在实际代码中使用

```python
from jqdata.client import JQDataClient

# 初始化客户端
jq_client = JQDataClient()

# 根据知识库中的信息，使用get_price API
price_data = jq_client.get_price(
    security='000001.XSHE',  # 平安银行
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency='daily',
    fields=['open', 'close', 'high', 'low', 'volume']
)

print(price_data.head())
```

---

## 📖 场景2: 开发策略初始化功能

### 需求
需要了解如何在策略中初始化，设置基准等。

### 步骤1: 搜索策略设置相关API

```python
from mcp_servers.unified_dev_server import knowledge_search

# 搜索initialize和策略设置
result1 = knowledge_search("initialize")
result2 = knowledge_search("策略设置")

print("=== initialize API ===")
for item in result1['results'][:2]:
    print(f"- {item['title']} (分数: {item['_score']})")

print("\n=== 策略设置分类 ===")
for item in result2['results'][:2]:
    print(f"- {item['title']} (分数: {item['_score']})")
```

### 步骤2: 查看完整文档

```python
# 获取initialize的详细文档
init_doc = result1['results'][0]['content']
print(init_doc)
```

### 步骤3: 编写策略代码

```python
# 根据知识库信息编写策略
def initialize(context):
    """
    策略初始化函数
    根据知识库文档编写
    """
    # 设置基准
    set_benchmark('000300.XSHG')  # 沪深300
    
    # 设置股票池
    g.security = '000001.XSHE'
    
    # 设置手续费
    set_option('order_cost', {
        'type': 'stock',
        'cost': 0.0003  # 万三
    })

def handle_data(context, data):
    """
    主逻辑函数
    """
    # 获取当前价格
    current_price = data[g.security].close
    
    # 策略逻辑...
    pass
```

---

## 📖 场景3: 查询财务数据

### 需求
需要查询股票的财务指标，如ROE、净利润增长率等。

### 步骤1: 搜索财务数据API

```python
from mcp_servers.unified_dev_server import knowledge_search

# 搜索财务数据相关API
result = knowledge_search("get_fundamentals")
print(f"找到 {result['total']} 个相关条目")

# 查看最相关的结果
if result['results']:
    doc = result['results'][0]
    print(f"\n标题: {doc['title']}")
    print(f"标签: {doc['tags']}")
```

### 步骤2: 查看参数说明

```python
# 从知识库内容中提取参数信息
content = result['results'][0]['content']
# 查找参数部分
if "## 参数" in content:
    params_section = content.split("## 参数")[1].split("##")[0]
    print("参数说明:")
    print(params_section)
```

### 步骤3: 编写查询代码

```python
from jqdata.client import JQDataClient
from jqdatasdk import query, finance

jq_client = JQDataClient()

# 根据知识库信息，构建查询
q = query(
    finance.STK_M_FINANCE_INDICATOR.code,
    finance.STK_M_FINANCE_INDICATOR.roe,
    finance.STK_M_FINANCE_INDICATOR.inc_net_profit_year_on_year
).filter(
    finance.STK_M_FINANCE_INDICATOR.code == '000001.XSHE'
)

# 执行查询
df = jq_client.get_fundamentals(q, statDate='2024-09-30')
print(df)
```

---

## 📖 场景4: 批量查找多个API

### 需求
需要同时了解多个相关API的用法。

### 步骤1: 按分类搜索

```python
from mcp_servers.unified_dev_server import knowledge_search

# 搜索"数据获取"分类下的所有API
result = knowledge_search("数据获取")
print(f"找到 {result['total']} 个数据获取相关的条目")

# 列出所有相关API
for item in result['results']:
    print(f"- {item['title']}")
```

### 步骤2: 获取分类下的API列表

```python
# 从分类条目中提取API列表
category_doc = result['results'][0]['content']
# 解析文档，提取API名称
import re
api_names = re.findall(r'## (\w+)', category_doc)
print("数据获取分类下的API:")
for api in api_names[:10]:
    print(f"  - {api}")
```

### 步骤3: 逐个查询详细文档

```python
# 对感兴趣的API查询详细文档
apis_to_check = ['get_price', 'get_index_stocks', 'get_trade_days']

for api_name in apis_to_check:
    result = knowledge_search(api_name)
    if result['results']:
        print(f"\n=== {api_name} ===")
        print(result['results'][0]['content'][:300] + "...")
```

---

## 📖 场景5: 在回测系统中使用

### 需求
开发回测系统，需要了解如何获取历史数据和执行交易。

### 完整示例代码

```python
"""
回测策略示例
基于知识库中的API文档编写
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')
from mcp_servers.unified_dev_server import knowledge_search
from jqdata.client import JQDataClient

# 1. 从知识库获取API信息
def get_api_info(api_name):
    """从知识库获取API信息"""
    result = knowledge_search(api_name)
    if result['results']:
        return result['results'][0]['content']
    return None

# 2. 查看get_price的用法
price_info = get_api_info("get_price")
print("get_price API信息:")
print(price_info[:500] if price_info else "未找到")

# 3. 查看order的用法
order_info = get_api_info("order")
print("\norder API信息:")
print(order_info[:500] if order_info else "未找到")

# 4. 实际使用
jq_client = JQDataClient()

# 获取历史价格
price_data = jq_client.get_price(
    security='000001.XSHE',
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency='daily'
)

# 计算移动平均
price_data['ma20'] = price_data['close'].rolling(20).mean()

# 策略逻辑（示例）
# 如果当前价格高于20日均线，买入
# 如果当前价格低于20日均线，卖出
# （实际交易需要order API，这里只是示例）
```

---

## 🔍 搜索技巧

### 1. 精确搜索API名称
```python
# ✅ 推荐：直接搜索API名称
result = knowledge_search("get_price")
```

### 2. 按分类搜索
```python
# ✅ 推荐：搜索分类名称
result = knowledge_search("数据获取")
result = knowledge_search("交易执行")
```

### 3. 组合搜索
```python
# ✅ 可以搜索多个关键词
result = knowledge_search("聚宽API get_fundamentals 参数")
```

### 4. 查看搜索结果
```python
result = knowledge_search("get_price")

# 查看所有结果
for item in result['results']:
    print(f"标题: {item['title']}")
    print(f"分数: {item['_score']}")
    print(f"标签: {item['tags']}")
    print()
```

---

## 📝 最佳实践

1. **先搜索，再编码**: 在编写代码前，先搜索知识库了解API用法
2. **查看完整文档**: 不要只看标题，查看完整的content获取参数说明
3. **检查标签**: 查看tags了解API的分类和用途
4. **验证参数**: 根据知识库中的参数说明，确保参数正确
5. **参考示例**: 知识库中的示例代码可以直接参考使用

---

## 🎯 快速参考

### 常用API搜索关键词

| API类别 | 搜索关键词 | 预期结果 |
|---------|-----------|---------|
| 价格数据 | `get_price` | 获取行情数据 |
| 财务数据 | `get_fundamentals` | 查询财务数据 |
| 指数成分 | `get_index_stocks` | 获取指数成分股 |
| 交易日历 | `get_trade_days` | 获取交易日历 |
| 下单 | `order` | 按数量下单 |
| 初始化 | `initialize` | 策略初始化 |
| 主逻辑 | `handle_data` | 策略主逻辑 |

---

*示例文档版本: 1.0 | 更新时间: 2025-12-19*

