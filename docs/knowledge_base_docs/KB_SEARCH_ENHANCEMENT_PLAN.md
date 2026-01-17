# 知识库搜索增强方案 - 量化研究和策略生成

> 创建时间: 2026-01-01
> 目标: 优化知识库搜索，更好地支持量化研究和策略生成

---

## 🎯 需求分析

### 量化研究需要

1. **API函数搜索**
   - 精确匹配函数名（如`get_price`, `get_fundamentals`）
   - 查找函数用法示例
   - 查找函数参数说明

2. **因子搜索**
   - Alpha101/191因子
   - CNE5/CNE6风格因子
   - 自定义因子

3. **策略模板搜索**
   - 策略代码示例
   - 回测框架
   - 优化方法

4. **数据源搜索**
   - 数据获取方法
   - 数据字段说明
   - 数据范围限制

---

## ✅ 已实现的增强功能

### 1. 精确匹配优先级 ✅

**功能**: API函数名、因子名精确匹配获得更高分数

**实现**:
- `exact_match_boost`: 精确匹配权重（默认10.0）
- 函数名匹配：`code_match_boost * 2`
- 因子名匹配：`code_match_boost * 1.5`

**效果**:
- API函数搜索结果更准确
- 因子搜索结果更相关

---

### 2. 代码块提取和搜索 ✅

**功能**: 从内容中提取代码块，支持代码搜索

**实现**:
- 提取Markdown代码块（```python...```）
- 提取行内代码（`code`）
- 代码块匹配获得更高分数（`code_match_boost`）

**效果**:
- 可以搜索代码示例
- 代码相关结果优先级更高

---

### 3. API函数提取 ✅

**功能**: 自动提取内容中的API函数名

**实现**:
- 正则匹配函数调用模式（`function_name(`）
- 匹配方法调用（`.method_name(`）
- 匹配导入语句（`from module import`, `import module`）

**效果**:
- 识别内容中包含的API函数
- API函数匹配获得更高分数

---

### 4. 因子名提取 ✅

**功能**: 自动提取内容中的因子名称

**实现**:
- 匹配Alpha因子（Alpha101, Alpha191）
- 匹配CNE因子（CNE5, CNE6）
- 匹配通用因子名（ROE, ROA, PE等）

**效果**:
- 识别内容中包含的因子
- 因子匹配获得更高分数

---

### 5. 标签优先匹配 ✅

**功能**: 标签匹配获得较高分数

**实现**:
- 标签完全匹配：`tag_match_boost`
- 标签部分匹配：`tag_match_boost * 0.5`

**效果**:
- 标签相关的搜索结果更靠前

---

### 6. 相关性评分增强 ✅

**功能**: 多维度评分系统

**评分项**:
- 精确匹配：10.0x
- 代码匹配：8.0x
- API函数匹配：16.0x（8.0 * 2）
- 因子匹配：12.0x（8.0 * 1.5）
- 标签匹配：5.0x
- 标题匹配：3.0x
- 内容匹配：1.0x（出现在前500字符则2.0x）
- URL匹配：2.0x（API相关）

**效果**:
- 搜索结果更相关
- 重要内容更靠前

---

### 7. 分类型搜索 ✅

**功能**: 按类别搜索（API/因子/策略/数据）

**类别**:
- `api`: API函数文档、交易函数、数据获取
- `factor`: 因子构建、Alpha因子、因子库、CNE因子
- `strategy`: 策略生成、回测、优化
- `data`: 数据获取、行情数据、财务数据、宏观数据

**使用**:
```python
result = search_by_category(query="Alpha", category="factor")
```

---

### 8. 专用搜索函数 ✅

**功能**: 针对特定用途的搜索函数

**函数**:
- `search_api_function(func_name)`: API函数搜索
- `search_factor(factor_name)`: 因子搜索

**特点**:
- 更高的精确匹配权重
- 针对性的评分策略

---

## 📊 使用示例

### 示例1: 搜索API函数

```python
from scripts.enhance_knowledge_search import search_api_function

# 搜索get_price函数
result = search_api_function("get_price", limit=5)

if result.get('success'):
    for item in result['results']:
        print(f"标题: {item['title']}")
        print(f"评分: {item['_score']}")
        print(f"API函数: {item['_match_details']['api_functions']}")
```

### 示例2: 搜索因子

```python
from scripts.enhance_knowledge_search import search_factor

# 搜索Alpha101因子
result = search_factor("Alpha101", limit=5)

if result.get('success'):
    for item in result['results']:
        print(f"标题: {item['title']}")
        print(f"评分: {item['_score']}")
        print(f"因子: {item['_match_details']['factors']}")
```

### 示例3: 增强搜索

```python
from scripts.enhance_knowledge_search import enhanced_search

# 通用增强搜索
result = enhanced_search(
    query="get_price",
    limit=10,
    exact_match_boost=20.0,  # 提高精确匹配权重
    code_match_boost=15.0,   # 提高代码匹配权重
)

if result.get('success'):
    for item in result['results']:
        print(f"标题: {item['title']}")
        print(f"评分: {item['_score']}")
        print(f"匹配详情: {item['_match_details']}")
```

### 示例4: 分类搜索

```python
from scripts.enhance_knowledge_search import search_by_category

# 搜索因子相关
result = search_by_category(query="Alpha", category="factor", limit=10)

if result.get('success'):
    for item in result['results']:
        print(f"标题: {item['title']}")
        print(f"标签: {item['tags']}")
```

---

## 🔄 集成到MCP服务器

### 方案1: 替换现有函数

修改 `mcp_servers/unified_dev_server.py` 中的 `knowledge_search` 函数，使用增强搜索逻辑。

### 方案2: 新增增强搜索工具

在MCP服务器中新增 `knowledge.enhanced_search` 工具，保留原有 `knowledge.search` 工具。

**推荐**: 方案2（向后兼容）

---

## 📈 性能对比

### 搜索"get_price"

**原始搜索**:
- 结果：按字符串匹配排序
- 相关性：一般

**增强搜索**:
- 结果：API函数匹配优先
- 相关性：高
- 评分：包含代码块的结果评分更高

### 搜索"Alpha101"

**原始搜索**:
- 结果：所有包含"Alpha101"的内容
- 相关性：一般

**增强搜索**:
- 结果：因子相关的优先
- 相关性：高
- 评分：包含因子定义和使用示例的评分更高

---

## 🚀 后续优化建议

### 1. 向量搜索（语义搜索）

- 使用embedding模型（如sentence-transformers）
- 支持语义相似度搜索
- 适合查找概念相关但关键词不完全匹配的内容

### 2. 全文索引

- 使用Elasticsearch或类似工具
- 支持更复杂的查询语法
- 支持模糊匹配、通配符等

### 3. 查询扩展

- 同义词扩展（如"因子" -> "factor", "指标"）
- 关联词扩展（如"Alpha101" -> "Alpha因子", "因子库"）

### 4. 结果聚类

- 将相似结果聚类
- 避免结果重复
- 提供更好的浏览体验

---

## ✅ 验证清单

- [x] 精确匹配优先级
- [x] 代码块提取和搜索
- [x] API函数提取
- [x] 因子名提取
- [x] 标签优先匹配
- [x] 相关性评分增强
- [x] 分类型搜索
- [x] 专用搜索函数
- [ ] 集成到MCP服务器（待实现）
- [ ] 性能测试（待进行）

---

*增强方案文档生成时间: 2026-01-01*

