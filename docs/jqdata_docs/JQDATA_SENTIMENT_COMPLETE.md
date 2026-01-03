# 聚宽JQData舆情信息服务完整说明

> **文档来源**: 聚宽官方文档 + 项目爬取文档  
> **更新时间**: 2025-12-26  
> **参考链接**: [聚宽API文档](https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9961)

---

## 📰 舆情信息服务概览

根据聚宽JQData官方文档，**舆情信息服务目前仅包含CCTV新闻联播文本数据**。

### 🔹 核心数据源

| 数据名称 | 数据表 | 时间范围 | 更新频率 |
|---------|--------|---------|---------|
| **CCTV新闻联播文本数据** | `finance.CCTV_NEWS` | 2009-06-26 至今 | 每日21:30前更新 |

---

## 📋 数据详情

### 1. CCTV新闻联播文本数据 (`finance.CCTV_NEWS`)

#### 数据来源
- **来源**: 央视新闻联播频道
- **数据性质**: 每日播报的新闻文本数据
- **历史范围**: 2009年6月26日至今

#### 数据字段结构

| 字段名 | 中文名称 | 数据类型 | 非空 | 说明 |
|--------|---------|---------|------|------|
| `day` | 日期 | date | ✅ | 新闻播报日期 |
| `title` | 标题 | varchar(200) | ✅ | 新闻标题（最多200字符） |
| `content` | 正文 | varchar(5000) | - | 新闻正文内容（最多5000字符） |

#### API使用方式

```python
from jqdatasdk import *

# 基础查询：获取指定日期的新闻
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10)
df = finance.run_query(q)

# 按标题关键词筛选
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%新春%%')  # 标题包含"新春"
).limit(10)
df = finance.run_query(q)

# 获取新闻正文内容
print(df.iloc[0]['content'])  # 获取第一条新闻的正文
```

#### 查询示例

```python
# 查询2019-02-19的新闻联播
from jqdatasdk import *

df = finance.run_query(query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10))

print(df)
```

**返回结果示例**:
```
      id         day                               title
0  77833  2019-02-19  【央视快评】推动深度融合 加快建设新型主流媒体
1  77828  2019-02-19  【领航新时代】安徽：树作风标杆 谋发展之变
2  77829  2019-02-19  中共中央 国务院关于坚持农业农村优先发展...
...
                                             content
0  本台今天刊播央视快评《推动深度融合 加快建设新型主流媒体》...
1  2014年3月9日，习近平总书记在参加十二届全国人大二次会议...
2  中共中央、国务院日前发出《关于坚持农业农村优先发展...
```

---

## ⚠️ 使用限制

1. **单次查询限制**: 最多返回5000行
2. **不支持连表查询**: 不能同时查询多张表的数据
3. **查询优化**: 建议使用日期字段进行filter以提高查询速度

---

## 💡 应用场景

### 1. 政策因子分析
- 提取政策相关新闻
- 分析政策对市场的影响
- 构建政策情绪指标

### 2. 市场情绪分析
- 对新闻标题和正文进行情绪分析
- 判断市场整体情绪倾向
- 识别市场热点和关注点

### 3. 主题挖掘
- 识别热点主题和关键词
- 跟踪特定行业/概念的新闻曝光度
- 构建主题投资策略

### 4. 事件追踪
- 跟踪特定事件在新闻联播中的报道
- 分析事件对市场的影响
- 构建事件驱动策略

---

## 🔗 项目中的集成

### 情绪分析器 (`core/sentiment_analyzer.py`)

项目中已实现市场情绪分析器，整合多渠道信息：

```python
class SentimentAnalyzer:
    """
    市场情绪分析器
    
    功能：
    1. 财经新闻情绪分析
    2. 社交媒体情绪监测
    3. 综合情绪评分
    4. 逆向指标提示
    """
```

**情绪来源**:
- AKShare财经新闻
- 百度指数（通过AKShare）
- 雪球热帖（模拟）
- 自定义观点输入

**注意**: 当前实现主要使用AKShare的财经新闻数据，JQData的CCTV新闻数据可以作为补充数据源。

---

## ✅ 权限说明

| 账号类型 | 权限 | 说明 |
|---------|------|------|
| **试用账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **正式账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **数据范围** | 2009-06-26 至今 | 无限制 |
| **更新频率** | 每日21:30前更新 | 实时更新 |

---

## 📊 数据统计

根据官方文档：
- **数据起始时间**: 2009年6月26日
- **数据更新**: 每日21:30前更新
- **数据量**: 每日约10-20条新闻（根据新闻联播实际播报情况）

---

## 🔍 特色数据说明

根据`docs/jqdata_crawled/003_JQData试用及购买.txt`文档：

> **特色数据**（需要单独申请）:
> - 需要联系微信号JQData02
> - 需要提交公司名片
> - 不在基础数据范围内

**注意**: 如果聚宽提供其他舆情相关的特色数据服务，需要单独联系申请，不在基础数据范围内。

---

## 📝 使用建议

### 1. 日期筛选
```python
# 精确查询特定日期
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
)
```

### 2. 关键词搜索
```python
# 模糊匹配标题
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%政策%%')
)
```

### 3. 批量处理
```python
# 如需大量数据，考虑分批查询
for date in date_range:
    q = query(finance.CCTV_NEWS).filter(
        finance.CCTV_NEWS.day == date
    )
    df = finance.run_query(q)
    # 处理数据...
```

### 4. 文本分析
```python
# 结合NLP技术对content字段进行深度分析
import jieba
from collections import Counter

# 提取关键词
text = df.iloc[0]['content']
keywords = jieba.analyse.extract_tags(text, topK=10)
```

---

## 📁 相关文档位置

```
docs/jqdata_crawled/021_舆情数据.txt          # 完整舆情数据文档
docs/jqdata_crawled/032_JQData数据范围及接口更新时间.txt  # 更新时间表
docs/jqdata_crawled/003_JQData试用及购买.txt  # 特色数据说明
core/sentiment_analyzer.py                   # 项目中的情绪分析器
```

---

## 🎯 总结

**聚宽JQData舆情信息服务目前仅包含CCTV新闻联播文本数据**，这是官方公开提供的基础舆情数据。

如果需要其他类型的舆情数据（如：
- 财经新闻数据
- 社交媒体数据
- 网络舆情数据
- 其他媒体文本数据

），需要：
1. 联系聚宽官方（微信号JQData02）
2. 提交公司名片申请特色数据
3. 或使用其他数据源（如AKShare、Tushare等）

---

*文档版本: 1.0 | 创建时间: 2025-12-26 | 最后更新: 2025-12-26*




> **文档来源**: 聚宽官方文档 + 项目爬取文档  
> **更新时间**: 2025-12-26  
> **参考链接**: [聚宽API文档](https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9961)

---

## 📰 舆情信息服务概览

根据聚宽JQData官方文档，**舆情信息服务目前仅包含CCTV新闻联播文本数据**。

### 🔹 核心数据源

| 数据名称 | 数据表 | 时间范围 | 更新频率 |
|---------|--------|---------|---------|
| **CCTV新闻联播文本数据** | `finance.CCTV_NEWS` | 2009-06-26 至今 | 每日21:30前更新 |

---

## 📋 数据详情

### 1. CCTV新闻联播文本数据 (`finance.CCTV_NEWS`)

#### 数据来源
- **来源**: 央视新闻联播频道
- **数据性质**: 每日播报的新闻文本数据
- **历史范围**: 2009年6月26日至今

#### 数据字段结构

| 字段名 | 中文名称 | 数据类型 | 非空 | 说明 |
|--------|---------|---------|------|------|
| `day` | 日期 | date | ✅ | 新闻播报日期 |
| `title` | 标题 | varchar(200) | ✅ | 新闻标题（最多200字符） |
| `content` | 正文 | varchar(5000) | - | 新闻正文内容（最多5000字符） |

#### API使用方式

```python
from jqdatasdk import *

# 基础查询：获取指定日期的新闻
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10)
df = finance.run_query(q)

# 按标题关键词筛选
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%新春%%')  # 标题包含"新春"
).limit(10)
df = finance.run_query(q)

# 获取新闻正文内容
print(df.iloc[0]['content'])  # 获取第一条新闻的正文
```

#### 查询示例

```python
# 查询2019-02-19的新闻联播
from jqdatasdk import *

df = finance.run_query(query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10))

print(df)
```

**返回结果示例**:
```
      id         day                               title
0  77833  2019-02-19  【央视快评】推动深度融合 加快建设新型主流媒体
1  77828  2019-02-19  【领航新时代】安徽：树作风标杆 谋发展之变
2  77829  2019-02-19  中共中央 国务院关于坚持农业农村优先发展...
...
                                             content
0  本台今天刊播央视快评《推动深度融合 加快建设新型主流媒体》...
1  2014年3月9日，习近平总书记在参加十二届全国人大二次会议...
2  中共中央、国务院日前发出《关于坚持农业农村优先发展...
```

---

## ⚠️ 使用限制

1. **单次查询限制**: 最多返回5000行
2. **不支持连表查询**: 不能同时查询多张表的数据
3. **查询优化**: 建议使用日期字段进行filter以提高查询速度

---

## 💡 应用场景

### 1. 政策因子分析
- 提取政策相关新闻
- 分析政策对市场的影响
- 构建政策情绪指标

### 2. 市场情绪分析
- 对新闻标题和正文进行情绪分析
- 判断市场整体情绪倾向
- 识别市场热点和关注点

### 3. 主题挖掘
- 识别热点主题和关键词
- 跟踪特定行业/概念的新闻曝光度
- 构建主题投资策略

### 4. 事件追踪
- 跟踪特定事件在新闻联播中的报道
- 分析事件对市场的影响
- 构建事件驱动策略

---

## 🔗 项目中的集成

### 情绪分析器 (`core/sentiment_analyzer.py`)

项目中已实现市场情绪分析器，整合多渠道信息：

```python
class SentimentAnalyzer:
    """
    市场情绪分析器
    
    功能：
    1. 财经新闻情绪分析
    2. 社交媒体情绪监测
    3. 综合情绪评分
    4. 逆向指标提示
    """
```

**情绪来源**:
- AKShare财经新闻
- 百度指数（通过AKShare）
- 雪球热帖（模拟）
- 自定义观点输入

**注意**: 当前实现主要使用AKShare的财经新闻数据，JQData的CCTV新闻数据可以作为补充数据源。

---

## ✅ 权限说明

| 账号类型 | 权限 | 说明 |
|---------|------|------|
| **试用账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **正式账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **数据范围** | 2009-06-26 至今 | 无限制 |
| **更新频率** | 每日21:30前更新 | 实时更新 |

---

## 📊 数据统计

根据官方文档：
- **数据起始时间**: 2009年6月26日
- **数据更新**: 每日21:30前更新
- **数据量**: 每日约10-20条新闻（根据新闻联播实际播报情况）

---

## 🔍 特色数据说明

根据`docs/jqdata_crawled/003_JQData试用及购买.txt`文档：

> **特色数据**（需要单独申请）:
> - 需要联系微信号JQData02
> - 需要提交公司名片
> - 不在基础数据范围内

**注意**: 如果聚宽提供其他舆情相关的特色数据服务，需要单独联系申请，不在基础数据范围内。

---

## 📝 使用建议

### 1. 日期筛选
```python
# 精确查询特定日期
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
)
```

### 2. 关键词搜索
```python
# 模糊匹配标题
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%政策%%')
)
```

### 3. 批量处理
```python
# 如需大量数据，考虑分批查询
for date in date_range:
    q = query(finance.CCTV_NEWS).filter(
        finance.CCTV_NEWS.day == date
    )
    df = finance.run_query(q)
    # 处理数据...
```

### 4. 文本分析
```python
# 结合NLP技术对content字段进行深度分析
import jieba
from collections import Counter

# 提取关键词
text = df.iloc[0]['content']
keywords = jieba.analyse.extract_tags(text, topK=10)
```

---

## 📁 相关文档位置

```
docs/jqdata_crawled/021_舆情数据.txt          # 完整舆情数据文档
docs/jqdata_crawled/032_JQData数据范围及接口更新时间.txt  # 更新时间表
docs/jqdata_crawled/003_JQData试用及购买.txt  # 特色数据说明
core/sentiment_analyzer.py                   # 项目中的情绪分析器
```

---

## 🎯 总结

**聚宽JQData舆情信息服务目前仅包含CCTV新闻联播文本数据**，这是官方公开提供的基础舆情数据。

如果需要其他类型的舆情数据（如：
- 财经新闻数据
- 社交媒体数据
- 网络舆情数据
- 其他媒体文本数据

），需要：
1. 联系聚宽官方（微信号JQData02）
2. 提交公司名片申请特色数据
3. 或使用其他数据源（如AKShare、Tushare等）

---

*文档版本: 1.0 | 创建时间: 2025-12-26 | 最后更新: 2025-12-26*























> **文档来源**: 聚宽官方文档 + 项目爬取文档  
> **更新时间**: 2025-12-26  
> **参考链接**: [聚宽API文档](https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9961)

---

## 📰 舆情信息服务概览

根据聚宽JQData官方文档，**舆情信息服务目前仅包含CCTV新闻联播文本数据**。

### 🔹 核心数据源

| 数据名称 | 数据表 | 时间范围 | 更新频率 |
|---------|--------|---------|---------|
| **CCTV新闻联播文本数据** | `finance.CCTV_NEWS` | 2009-06-26 至今 | 每日21:30前更新 |

---

## 📋 数据详情

### 1. CCTV新闻联播文本数据 (`finance.CCTV_NEWS`)

#### 数据来源
- **来源**: 央视新闻联播频道
- **数据性质**: 每日播报的新闻文本数据
- **历史范围**: 2009年6月26日至今

#### 数据字段结构

| 字段名 | 中文名称 | 数据类型 | 非空 | 说明 |
|--------|---------|---------|------|------|
| `day` | 日期 | date | ✅ | 新闻播报日期 |
| `title` | 标题 | varchar(200) | ✅ | 新闻标题（最多200字符） |
| `content` | 正文 | varchar(5000) | - | 新闻正文内容（最多5000字符） |

#### API使用方式

```python
from jqdatasdk import *

# 基础查询：获取指定日期的新闻
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10)
df = finance.run_query(q)

# 按标题关键词筛选
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%新春%%')  # 标题包含"新春"
).limit(10)
df = finance.run_query(q)

# 获取新闻正文内容
print(df.iloc[0]['content'])  # 获取第一条新闻的正文
```

#### 查询示例

```python
# 查询2019-02-19的新闻联播
from jqdatasdk import *

df = finance.run_query(query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10))

print(df)
```

**返回结果示例**:
```
      id         day                               title
0  77833  2019-02-19  【央视快评】推动深度融合 加快建设新型主流媒体
1  77828  2019-02-19  【领航新时代】安徽：树作风标杆 谋发展之变
2  77829  2019-02-19  中共中央 国务院关于坚持农业农村优先发展...
...
                                             content
0  本台今天刊播央视快评《推动深度融合 加快建设新型主流媒体》...
1  2014年3月9日，习近平总书记在参加十二届全国人大二次会议...
2  中共中央、国务院日前发出《关于坚持农业农村优先发展...
```

---

## ⚠️ 使用限制

1. **单次查询限制**: 最多返回5000行
2. **不支持连表查询**: 不能同时查询多张表的数据
3. **查询优化**: 建议使用日期字段进行filter以提高查询速度

---

## 💡 应用场景

### 1. 政策因子分析
- 提取政策相关新闻
- 分析政策对市场的影响
- 构建政策情绪指标

### 2. 市场情绪分析
- 对新闻标题和正文进行情绪分析
- 判断市场整体情绪倾向
- 识别市场热点和关注点

### 3. 主题挖掘
- 识别热点主题和关键词
- 跟踪特定行业/概念的新闻曝光度
- 构建主题投资策略

### 4. 事件追踪
- 跟踪特定事件在新闻联播中的报道
- 分析事件对市场的影响
- 构建事件驱动策略

---

## 🔗 项目中的集成

### 情绪分析器 (`core/sentiment_analyzer.py`)

项目中已实现市场情绪分析器，整合多渠道信息：

```python
class SentimentAnalyzer:
    """
    市场情绪分析器
    
    功能：
    1. 财经新闻情绪分析
    2. 社交媒体情绪监测
    3. 综合情绪评分
    4. 逆向指标提示
    """
```

**情绪来源**:
- AKShare财经新闻
- 百度指数（通过AKShare）
- 雪球热帖（模拟）
- 自定义观点输入

**注意**: 当前实现主要使用AKShare的财经新闻数据，JQData的CCTV新闻数据可以作为补充数据源。

---

## ✅ 权限说明

| 账号类型 | 权限 | 说明 |
|---------|------|------|
| **试用账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **正式账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **数据范围** | 2009-06-26 至今 | 无限制 |
| **更新频率** | 每日21:30前更新 | 实时更新 |

---

## 📊 数据统计

根据官方文档：
- **数据起始时间**: 2009年6月26日
- **数据更新**: 每日21:30前更新
- **数据量**: 每日约10-20条新闻（根据新闻联播实际播报情况）

---

## 🔍 特色数据说明

根据`docs/jqdata_crawled/003_JQData试用及购买.txt`文档：

> **特色数据**（需要单独申请）:
> - 需要联系微信号JQData02
> - 需要提交公司名片
> - 不在基础数据范围内

**注意**: 如果聚宽提供其他舆情相关的特色数据服务，需要单独联系申请，不在基础数据范围内。

---

## 📝 使用建议

### 1. 日期筛选
```python
# 精确查询特定日期
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
)
```

### 2. 关键词搜索
```python
# 模糊匹配标题
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%政策%%')
)
```

### 3. 批量处理
```python
# 如需大量数据，考虑分批查询
for date in date_range:
    q = query(finance.CCTV_NEWS).filter(
        finance.CCTV_NEWS.day == date
    )
    df = finance.run_query(q)
    # 处理数据...
```

### 4. 文本分析
```python
# 结合NLP技术对content字段进行深度分析
import jieba
from collections import Counter

# 提取关键词
text = df.iloc[0]['content']
keywords = jieba.analyse.extract_tags(text, topK=10)
```

---

## 📁 相关文档位置

```
docs/jqdata_crawled/021_舆情数据.txt          # 完整舆情数据文档
docs/jqdata_crawled/032_JQData数据范围及接口更新时间.txt  # 更新时间表
docs/jqdata_crawled/003_JQData试用及购买.txt  # 特色数据说明
core/sentiment_analyzer.py                   # 项目中的情绪分析器
```

---

## 🎯 总结

**聚宽JQData舆情信息服务目前仅包含CCTV新闻联播文本数据**，这是官方公开提供的基础舆情数据。

如果需要其他类型的舆情数据（如：
- 财经新闻数据
- 社交媒体数据
- 网络舆情数据
- 其他媒体文本数据

），需要：
1. 联系聚宽官方（微信号JQData02）
2. 提交公司名片申请特色数据
3. 或使用其他数据源（如AKShare、Tushare等）

---

*文档版本: 1.0 | 创建时间: 2025-12-26 | 最后更新: 2025-12-26*




> **文档来源**: 聚宽官方文档 + 项目爬取文档  
> **更新时间**: 2025-12-26  
> **参考链接**: [聚宽API文档](https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9961)

---

## 📰 舆情信息服务概览

根据聚宽JQData官方文档，**舆情信息服务目前仅包含CCTV新闻联播文本数据**。

### 🔹 核心数据源

| 数据名称 | 数据表 | 时间范围 | 更新频率 |
|---------|--------|---------|---------|
| **CCTV新闻联播文本数据** | `finance.CCTV_NEWS` | 2009-06-26 至今 | 每日21:30前更新 |

---

## 📋 数据详情

### 1. CCTV新闻联播文本数据 (`finance.CCTV_NEWS`)

#### 数据来源
- **来源**: 央视新闻联播频道
- **数据性质**: 每日播报的新闻文本数据
- **历史范围**: 2009年6月26日至今

#### 数据字段结构

| 字段名 | 中文名称 | 数据类型 | 非空 | 说明 |
|--------|---------|---------|------|------|
| `day` | 日期 | date | ✅ | 新闻播报日期 |
| `title` | 标题 | varchar(200) | ✅ | 新闻标题（最多200字符） |
| `content` | 正文 | varchar(5000) | - | 新闻正文内容（最多5000字符） |

#### API使用方式

```python
from jqdatasdk import *

# 基础查询：获取指定日期的新闻
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10)
df = finance.run_query(q)

# 按标题关键词筛选
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%新春%%')  # 标题包含"新春"
).limit(10)
df = finance.run_query(q)

# 获取新闻正文内容
print(df.iloc[0]['content'])  # 获取第一条新闻的正文
```

#### 查询示例

```python
# 查询2019-02-19的新闻联播
from jqdatasdk import *

df = finance.run_query(query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
).limit(10))

print(df)
```

**返回结果示例**:
```
      id         day                               title
0  77833  2019-02-19  【央视快评】推动深度融合 加快建设新型主流媒体
1  77828  2019-02-19  【领航新时代】安徽：树作风标杆 谋发展之变
2  77829  2019-02-19  中共中央 国务院关于坚持农业农村优先发展...
...
                                             content
0  本台今天刊播央视快评《推动深度融合 加快建设新型主流媒体》...
1  2014年3月9日，习近平总书记在参加十二届全国人大二次会议...
2  中共中央、国务院日前发出《关于坚持农业农村优先发展...
```

---

## ⚠️ 使用限制

1. **单次查询限制**: 最多返回5000行
2. **不支持连表查询**: 不能同时查询多张表的数据
3. **查询优化**: 建议使用日期字段进行filter以提高查询速度

---

## 💡 应用场景

### 1. 政策因子分析
- 提取政策相关新闻
- 分析政策对市场的影响
- 构建政策情绪指标

### 2. 市场情绪分析
- 对新闻标题和正文进行情绪分析
- 判断市场整体情绪倾向
- 识别市场热点和关注点

### 3. 主题挖掘
- 识别热点主题和关键词
- 跟踪特定行业/概念的新闻曝光度
- 构建主题投资策略

### 4. 事件追踪
- 跟踪特定事件在新闻联播中的报道
- 分析事件对市场的影响
- 构建事件驱动策略

---

## 🔗 项目中的集成

### 情绪分析器 (`core/sentiment_analyzer.py`)

项目中已实现市场情绪分析器，整合多渠道信息：

```python
class SentimentAnalyzer:
    """
    市场情绪分析器
    
    功能：
    1. 财经新闻情绪分析
    2. 社交媒体情绪监测
    3. 综合情绪评分
    4. 逆向指标提示
    """
```

**情绪来源**:
- AKShare财经新闻
- 百度指数（通过AKShare）
- 雪球热帖（模拟）
- 自定义观点输入

**注意**: 当前实现主要使用AKShare的财经新闻数据，JQData的CCTV新闻数据可以作为补充数据源。

---

## ✅ 权限说明

| 账号类型 | 权限 | 说明 |
|---------|------|------|
| **试用账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **正式账户** | ✅ 完全开放 | 可访问所有CCTV新闻数据 |
| **数据范围** | 2009-06-26 至今 | 无限制 |
| **更新频率** | 每日21:30前更新 | 实时更新 |

---

## 📊 数据统计

根据官方文档：
- **数据起始时间**: 2009年6月26日
- **数据更新**: 每日21:30前更新
- **数据量**: 每日约10-20条新闻（根据新闻联播实际播报情况）

---

## 🔍 特色数据说明

根据`docs/jqdata_crawled/003_JQData试用及购买.txt`文档：

> **特色数据**（需要单独申请）:
> - 需要联系微信号JQData02
> - 需要提交公司名片
> - 不在基础数据范围内

**注意**: 如果聚宽提供其他舆情相关的特色数据服务，需要单独联系申请，不在基础数据范围内。

---

## 📝 使用建议

### 1. 日期筛选
```python
# 精确查询特定日期
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.day == '2019-02-19'
)
```

### 2. 关键词搜索
```python
# 模糊匹配标题
q = query(finance.CCTV_NEWS).filter(
    finance.CCTV_NEWS.title.like('%%政策%%')
)
```

### 3. 批量处理
```python
# 如需大量数据，考虑分批查询
for date in date_range:
    q = query(finance.CCTV_NEWS).filter(
        finance.CCTV_NEWS.day == date
    )
    df = finance.run_query(q)
    # 处理数据...
```

### 4. 文本分析
```python
# 结合NLP技术对content字段进行深度分析
import jieba
from collections import Counter

# 提取关键词
text = df.iloc[0]['content']
keywords = jieba.analyse.extract_tags(text, topK=10)
```

---

## 📁 相关文档位置

```
docs/jqdata_crawled/021_舆情数据.txt          # 完整舆情数据文档
docs/jqdata_crawled/032_JQData数据范围及接口更新时间.txt  # 更新时间表
docs/jqdata_crawled/003_JQData试用及购买.txt  # 特色数据说明
core/sentiment_analyzer.py                   # 项目中的情绪分析器
```

---

## 🎯 总结

**聚宽JQData舆情信息服务目前仅包含CCTV新闻联播文本数据**，这是官方公开提供的基础舆情数据。

如果需要其他类型的舆情数据（如：
- 财经新闻数据
- 社交媒体数据
- 网络舆情数据
- 其他媒体文本数据

），需要：
1. 联系聚宽官方（微信号JQData02）
2. 提交公司名片申请特色数据
3. 或使用其他数据源（如AKShare、Tushare等）

---

*文档版本: 1.0 | 创建时间: 2025-12-26 | 最后更新: 2025-12-26*









































