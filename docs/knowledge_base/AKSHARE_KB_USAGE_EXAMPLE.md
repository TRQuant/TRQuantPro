# AKShare知识库使用示例

> **创建时间**: 2026-01-12  
> **目的**: 展示AKShare知识库的构建过程和使用方法

---

## 📋 完整示例：从爬取到策略开发

### 1. 爬取的页面

**页面URL**: `https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt`

这是AKShare股票数据文档的Markdown源文件，包含：
- 所有API接口定义
- 函数参数说明
- 代码示例
- 使用说明

**为什么选择源文件而不是HTML？**
- ✅ 结构更清晰，易于解析
- ✅ 包含完整的API文档
- ✅ 文件更小，处理更快
- ✅ 不需要解析复杂的HTML结构

---

### 2. 爬取的内容示例

#### 2.1 原始Markdown内容片段

```markdown
# 行情报价

## 沪深京 A 股

接口: stock_zh_a_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#hs_a_board

描述: 东方财富网-沪深京 A 股-实时行情数据

限量: 单次返回所有沪深京 A 股上市公司的实时行情数据

输入参数

| 名称   | 类型 | 必选 | 描述   |
| :----- | :--- | :--- | :----- |
| -      | -    | -    | -      |

输出参数

| 名称          | 类型 | 描述           |
| :------------ | :--- | :------------- |
| 代码          | str  | 股票代码       |
| 名称          | str  | 股票名称       |
| 最新价        | str  | 最新价         |
| 涨跌幅        | str  | 涨跌幅         |
| 涨跌额        | str  | 涨跌额         |
| 成交量        | str  | 成交量         |
| 成交额        | str  | 成交额         |
| 振幅          | str  | 振幅           |
| 最高          | str  | 最高价         |
| 最低          | str  | 最低价         |
| 今开          | str  | 今开价         |
| 昨收          | str  | 昨收价         |
| 量比          | str  | 量比           |
| 换手率        | str  | 换手率         |
| 市盈率-动态   | str  | 市盈率-动态    |
| 市净率        | str  | 市净率         |
| 总市值        | str  | 总市值         |
| 流通市值      | str  | 流通市值       |
| 涨速          | str  | 涨速           |
| 5分钟涨跌     | str  | 5分钟涨跌      |
| 60日涨跌幅    | str  | 60日涨跌幅     |
| 年初至今涨跌幅 | str  | 年初至今涨跌幅 |

接口示例

```python
import akshare as ak

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
print(stock_zh_a_spot_em_df)
```

数据示例

```
        代码    名称      最新价   涨跌幅   涨跌额   成交量        成交额      振幅   最高   最低   今开   昨收   量比   换手率  市盈率-动态  市净率   总市值        流通市值     涨速   5分钟涨跌  60日涨跌幅  年初至今涨跌幅
0  000001.SZ  平安银行  12.34   0.81%   0.10   12345678   152345678   2.34   12.45  12.10  12.20  12.24  1.23   0.45   8.90    0.95   1234567890  1234567890  0.12   0.05     15.23     12.34
...
```
```

#### 2.2 解析后的知识库条目

脚本会将上述Markdown内容解析为以下知识库条目：

```json
{
  "id": "kb_20260112_150316",
  "title": "AKShare股票数据: 沪深京 A 股",
  "type": "reference",
  "tags": ["AKShare", "股票数据", "API文档", "API接口", "行情数据"],
  "content": "接口: stock_zh_a_spot_em\n\n目标地址: http://quote.eastmoney.com/center/gridlist.html#hs_a_board\n\n描述: 东方财富网-沪深京 A 股-实时行情数据\n\n限量: 单次返回所有沪深京 A 股上市公司的实时行情数据\n\n输入参数: 无\n\n输出参数:\n- 代码: 股票代码\n- 名称: 股票名称\n- 最新价: 最新价\n- 涨跌幅: 涨跌幅\n...\n\n## 代码示例\n\n```python\nimport akshare as ak\n\nstock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()\nprint(stock_zh_a_spot_em_df)\n```\n\n---\n**来源**: https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt\n**锚点**: 沪深京-a股",
  "source": "https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt",
  "created": "2026-01-12T15:03:16",
  "updated": "2026-01-12T15:03:16"
}
```

---

### 3. 知识库构建过程

#### 3.1 脚本执行流程

```python
# scripts/kb/build_kb_akshare_from_source.py

1. 抓取Markdown源文件
   ↓
2. 解析Markdown内容
   - 识别标题（# ## ###）
   - 提取API接口定义
   - 提取参数说明
   - 提取代码示例
   ↓
3. 生成知识库条目
   - 标题: "AKShare股票数据: {section_title}"
   - 内容: 完整的API文档
   - 标签: 自动推断（AKShare, 股票数据, API接口等）
   ↓
4. 存入知识库
   - 使用MCP工具 knowledge.add
   - 或直接函数调用 knowledge_add()
   ↓
5. 验证知识库
   - 搜索测试
   - 统计信息
```

#### 3.2 内容去重机制

```python
# 使用MD5哈希避免重复存储
content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
if content_hash in content_hashes:
    # 跳过重复内容
    return False
```

#### 3.3 统计信息

```
找到内容块: 447个
成功保存: 447个
保存失败: 0个
跳过重复: 0个
```

---

### 4. 在策略开发中使用知识库

#### 4.1 场景：开发一个基于实时行情的选股策略

**需求**: 获取所有A股实时行情，筛选出涨跌幅>5%且成交量放大的股票

#### 4.2 步骤1：搜索相关知识

```python
from core.mcp.client import MCPClient

client = MCPClient()

# 搜索AKShare实时行情API
result = client.call(
    tool_name='knowledge.search',
    arguments={
        'query': 'AKShare 实时行情 A股',
        'limit': 5
    },
    timeout=30.0
)

if result.success:
    data = result.data
    if isinstance(data, str):
        import json
        data = json.loads(data)
    
    items = data.get('items', []) or data.get('results', [])
    for item in items:
        print(f"标题: {item['title']}")
        print(f"内容: {item['content'][:200]}...")
        print("---")
```

**搜索结果示例**:
```
标题: AKShare股票数据: 沪深京 A 股
内容: 接口: stock_zh_a_spot_em
目标地址: http://quote.eastmoney.com/center/gridlist.html#hs_a_board
描述: 东方财富网-沪深京 A 股-实时行情数据
...
代码示例:
import akshare as ak
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
```

#### 4.3 步骤2：基于知识库内容生成策略代码

```python
# 策略代码生成（基于知识库内容）

import akshare as ak
import pandas as pd
from datetime import datetime

def select_stocks_by_momentum():
    """
    基于实时行情选股策略
    
    筛选条件:
    1. 涨跌幅 > 5%
    2. 成交量放大（量比 > 1.5）
    3. 换手率 > 2%
    """
    # 从知识库获取的API接口
    # 接口: stock_zh_a_spot_em
    # 描述: 获取所有沪深京 A 股实时行情数据
    
    # 获取实时行情数据
    df = ak.stock_zh_a_spot_em()
    
    # 数据清洗
    # 从知识库知道输出字段包括: 代码, 名称, 涨跌幅, 量比, 换手率等
    df['涨跌幅_数值'] = df['涨跌幅'].str.replace('%', '').astype(float)
    df['量比_数值'] = df['量比'].astype(float)
    df['换手率_数值'] = df['换手率'].str.replace('%', '').astype(float)
    
    # 筛选条件
    selected = df[
        (df['涨跌幅_数值'] > 5.0) &      # 涨跌幅 > 5%
        (df['量比_数值'] > 1.5) &         # 量比 > 1.5
        (df['换手率_数值'] > 2.0)         # 换手率 > 2%
    ]
    
    # 按涨跌幅排序
    selected = selected.sort_values('涨跌幅_数值', ascending=False)
    
    return selected[['代码', '名称', '最新价', '涨跌幅', '量比', '换手率', '成交量', '成交额']]

# 执行策略
if __name__ == '__main__':
    result = select_stocks_by_momentum()
    print(f"筛选出 {len(result)} 只股票:")
    print(result.head(20))
```

#### 4.4 步骤3：在Notebook中使用

```python
# notebooks/research/strategy_momentum_selection.ipynb

# Cell 1: 环境初始化
import sys
from pathlib import Path
project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')
sys.path.insert(0, str(project_root))

from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)

# Cell 2: 搜索知识库
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='knowledge.search',
    arguments={'query': 'AKShare 实时行情', 'limit': 3},
    timeout=30.0
)

# 显示搜索结果
if result.success:
    data = json.loads(result.data) if isinstance(result.data, str) else result.data
    for item in data.get('items', [])[:3]:
        print(f"📚 {item['title']}")
        print(f"   {item['content'][:150]}...")
        print()

# Cell 3: 使用知识库中的API
import akshare as ak

# 根据知识库，使用 stock_zh_a_spot_em 获取实时行情
df = ak.stock_zh_a_spot_em()
print(f"获取到 {len(df)} 只股票的实时行情")

# Cell 4: 策略实现
# ... (使用上面生成的策略代码)
```

#### 4.5 步骤4：在MCP工具中使用（自动化）

```python
# 在MCP工具中，AI助手可以自动搜索知识库并生成代码

# 用户请求: "帮我写一个获取A股实时行情的策略"

# AI助手内部流程:
1. 调用 knowledge.search("AKShare 实时行情 A股")
2. 获取API接口信息: stock_zh_a_spot_em
3. 获取参数说明和代码示例
4. 生成完整的策略代码
5. 返回给用户
```

---

### 5. 知识库搜索增强功能

#### 5.1 精确匹配API函数名

```python
# 搜索 "stock_zh_a_spot_em" 会精确匹配函数名
result = client.call(
    tool_name='knowledge.search',
    arguments={'query': 'stock_zh_a_spot_em', 'limit': 5}
)
# 函数名匹配会获得更高分数，排在结果最前面
```

#### 5.2 代码块搜索

```python
# 搜索代码示例
result = client.call(
    tool_name='knowledge.search',
    arguments={'query': 'ak.stock_zh_a_spot_em() 代码示例', 'limit': 5}
)
# 包含代码块的内容会优先返回
```

#### 5.3 标签过滤

```python
# 搜索特定标签的内容
result = client.call(
    tool_name='knowledge.search',
    arguments={
        'query': '实时行情',
        'type': 'reference',  # 只搜索参考文档类型
        'limit': 10
    }
)
```

---

### 6. 完整工作流示例

```
用户需求
  ↓
AI助手搜索知识库
  ↓
找到相关API文档
  ↓
提取API接口、参数、示例代码
  ↓
生成策略代码
  ↓
用户验证和优化
  ↓
策略回测
```

**实际对话示例**:

```
用户: "我想获取所有A股的实时行情数据，筛选出涨跌幅大于5%的股票"

AI助手:
1. 搜索知识库: "AKShare 实时行情 A股"
2. 找到条目: "AKShare股票数据: 沪深京 A 股"
3. 提取信息:
   - API: stock_zh_a_spot_em()
   - 输出字段: 代码, 名称, 涨跌幅, ...
4. 生成代码:
   ```python
   import akshare as ak
   df = ak.stock_zh_a_spot_em()
   df['涨跌幅_数值'] = df['涨跌幅'].str.replace('%', '').astype(float)
   selected = df[df['涨跌幅_数值'] > 5.0]
   print(selected[['代码', '名称', '涨跌幅']])
   ```
```

---

### 7. 知识库统计

**已构建的知识库条目**:
- **总数**: 447个条目
- **类型**: reference (API参考文档)
- **标签**: AKShare, 股票数据, API文档, API接口, 行情数据等
- **覆盖范围**: 
  - A股实时行情
  - 历史行情数据
  - 个股信息查询
  - 行业数据
  - 财务数据
  - 等等

**知识库文件位置**:
- JSON文件: `.trquant/dev/knowledge/knowledge_base.json`
- 源文件: `docs/akshare_crawled/stock_data/stock.md.txt`

---

### 8. 总结

✅ **爬取**: 直接从Markdown源文件爬取，结构清晰  
✅ **构建**: 自动解析、分类、去重，存入知识库  
✅ **使用**: 通过MCP工具搜索，AI助手自动生成策略代码  
✅ **验证**: 知识库搜索测试通过，可用于策略开发  

**优势**:
1. **准确性**: 直接从官方文档源文件提取，信息准确
2. **完整性**: 包含API接口、参数、示例代码
3. **易用性**: 通过MCP工具和AI助手，自动搜索和代码生成
4. **可扩展**: 可以继续爬取其他数据类型的文档

---

**相关文件**:
- 爬取脚本: `scripts/kb/build_kb_akshare_from_source.py`
- 知识库文件: `.trquant/dev/knowledge/knowledge_base.json`
- 源文件: `docs/akshare_crawled/stock_data/stock.md.txt`
- 使用文档: `docs/knowledge_base/AKSHARE_KB_USAGE_EXAMPLE.md` (本文档)
