# 使用OpenManus功能抓取下周投资热点和建议报告

> **创建时间**: 2026-01-11  
> **状态**: ✅ 已实现

---

## 📋 功能说明

使用OpenManus功能（WorkflowEnhancer、FinancialCollector）抓取下周投资热点和建议，并生成HTML报告。

### 使用的OpenManus功能

1. **WorkflowEnhancer** (`core/workflow/openmanus_integration.py`)
   - `enhance_r1_market_trend`: R1市场趋势分析增强（使用MarketTrendAnalyzer - 多周期共振+HMM）
   - `enhance_r2_mainline`: R2主线轮动研究增强（热点主题识别）

2. **FinancialCollector** (`core/data_collection/financial_collector.py`)
   - `fetch_news`: 获取财经新闻（东方财富）

### 报告内容

1. **市场趋势分析**
   - 趋势标签（bullish/bearish/neutral）
   - 共振阶段
   - HMM状态
   - 综合评分

2. **投资热点主题**
   - 热点主题列表（Top5）
   - 热度得分
   - 出现次数

3. **相关财经新闻**
   - 财经新闻列表（Top15）
   - 新闻标题、链接
   - 来源和时间

4. **下周投资建议**
   - 基于市场趋势和热点主题的建议
   - 投资策略建议
   - 风险提示

---

## 🚀 使用方式

### 方式1: 运行脚本（推荐）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/generate_investment_hotspot_report.py
```

### 方式2: 在Python代码中使用

```python
import asyncio
from scripts.generate_investment_hotspot_report import collect_investment_hotspots, generate_html_report
from pathlib import Path

async def main():
    # 收集投资热点信息
    results = await collect_investment_hotspots()
    
    # 生成HTML报告
    output_file = Path("reports/investment_hotspot_report.html")
    html_file = generate_html_report(results, output_file)
    
    print(f"报告已生成: {html_file}")

asyncio.run(main())
```

---

## 📊 报告示例

### 市场趋势分析

- **趋势标签**: neutral (中性)
- **共振阶段**: 周期分歧
- **HMM状态**: 震荡
- **综合评分**: 25.41

### 投资热点主题

1. **科技** (热度: 100.0, 出现次数: 2)
2. **半导体** (热度: 50.0, 出现次数: 1)

### 相关财经新闻

- 十大机构论市：牛市行情或将继续推进...
- 本周沪指上涨3.82%，深证成指上涨4.40%...
- 1月11日晚间沪深上市公司重大事项公告最新快递...

### 下周投资建议

1. 市场处于震荡状态，建议精选个股，关注热点主题轮动机会
2. 重点关注热点主题: 科技, 半导体
3. 建议关注市场热点轮动，把握结构性机会
4. 严格控制风险，设置止损位

---

## 📁 输出文件

### HTML报告

**位置**: `reports/investment_hotspot_report_YYYYMMDD.html`

**内容**:
- 市场趋势分析
- 投资热点主题
- 相关财经新闻
- 下周投资建议
- 风险提示

**格式**: 专业的HTML报告，包含CSS样式

### JSON数据

**位置**: `reports/investment_hotspot_data_YYYYMMDD.json`

**内容**:
- 市场趋势分析数据
- 热点主题数据
- 财经新闻数据
- 收集时间

**格式**: JSON格式，可用于进一步分析

---

## 🔧 脚本功能

### 1. 收集投资热点信息

```python
async def collect_investment_hotspots():
    """收集投资热点信息"""
    results = {
        "market_trend": None,
        "hot_topics": None,
        "news_list": None,
        "collect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 使用WorkflowEnhancer获取市场趋势和热点主题
    async with WorkflowEnhancer(headless=True) as enhancer:
        # R1市场趋势分析
        r1_result = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
        
        # R2主线轮动研究
        r2_result = await enhancer.enhance_r2_mainline()
    
    # 使用FinancialCollector获取财经新闻
    async with FinancialCollector(headless=True) as collector:
        news_result = await collector.fetch_news("eastmoney", limit=20)
    
    return results
```

### 2. 生成HTML报告

```python
def generate_html_report(results: Dict[str, Any], output_file: Path):
    """生成HTML报告"""
    # 生成HTML内容
    html_content = """
    <!DOCTYPE html>
    <html>
    ...
    </html>
    """
    
    # 保存HTML文件
    output_file.write_text(html_content, encoding='utf-8')
    
    return output_file
```

---

## 📊 报告结构

### HTML报告结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>下周投资热点和建议报告</title>
    <style>...</style>
</head>
<body>
    <div class="header">
        <h1>📈 下周投资热点和建议报告</h1>
        <div class="subtitle">时间范围、生成时间</div>
    </div>
    
    <div class="section">
        <h2>📊 市场趋势分析</h2>
        <!-- 市场趋势数据 -->
    </div>
    
    <div class="section">
        <h2>🔥 投资热点主题</h2>
        <!-- 热点主题列表 -->
    </div>
    
    <div class="section">
        <h2>📰 相关财经新闻</h2>
        <!-- 财经新闻列表 -->
    </div>
    
    <div class="section">
        <h2>💡 下周投资建议</h2>
        <!-- 投资建议 -->
    </div>
    
    <div class="section">
        <h2>⚠️ 风险提示</h2>
        <!-- 风险提示 -->
    </div>
</body>
</html>
```

---

## 💡 使用建议

### 1. 定期运行

建议每周运行一次，获取最新的投资热点和建议：

```bash
# 每周一运行，获取下周投资热点
./venv/bin/python scripts/generate_investment_hotspot_report.py
```

### 2. 自定义参数

可以修改脚本中的参数：

```python
# 修改热点关键词列表
hot_keywords = ["AI", "新能源", "半导体", "消费", "医药", "金融", "科技", ...]

# 修改新闻数量
news_result = await collector.fetch_news("eastmoney", limit=30)  # 改为30条

# 修改指数代码
r1_result = await enhancer.enhance_r1_market_trend(index_code="000001.XSHG")  # 上证指数
```

### 3. 集成到工作流

可以集成到9步工作流中：

```python
from core.workflow import WorkflowEnhancer

async with WorkflowEnhancer() as enhancer:
    # R0数据源检测
    r0 = await enhancer.enhance_r0_data_source()
    
    # R1市场趋势分析
    r1 = await enhancer.enhance_r1_market_trend()
    
    # R2主线轮动研究
    r2 = await enhancer.enhance_r2_mainline()
    
    # 生成报告
    results = {
        "market_trend": r1.data,
        "hot_topics": r2.data
    }
    generate_html_report(results, output_file)
```

---

## 🔍 报告预览

### 市场趋势分析示例

- **趋势标签**: NEUTRAL (中性趋势)
- **共振阶段**: 周期分歧
- **HMM状态**: 震荡
- **综合评分**: 25.41

### 投资热点主题示例

1. **科技** (热度: 100.0, 出现次数: 2)
2. **半导体** (热度: 50.0, 出现次数: 1)

### 财经新闻示例

- 十大机构论市：牛市行情或将继续推进...
- 本周沪指上涨3.82%，深证成指上涨4.40%...
- 1月11日晚间沪深上市公司重大事项公告最新快递...

### 投资建议示例

1. 市场处于震荡状态，建议精选个股，关注热点主题轮动机会
2. 重点关注热点主题: 科技, 半导体
3. 建议关注市场热点轮动，把握结构性机会
4. 严格控制风险，设置止损位

---

## 📚 相关文档

- **脚本位置**: `scripts/generate_investment_hotspot_report.py`
- **WorkflowEnhancer**: `core/workflow/openmanus_integration.py`
- **FinancialCollector**: `core/data_collection/financial_collector.py`
- **报告输出**: `reports/investment_hotspot_report_YYYYMMDD.html`
- **数据输出**: `reports/investment_hotspot_data_YYYYMMDD.json`

---

## ✅ 验证结果

### 报告生成

- ✅ HTML报告已生成（12KB）
- ✅ JSON数据已保存（18KB）
- ✅ 报告包含市场趋势分析、投资热点主题、财经新闻和投资建议

### 数据质量

- ✅ 市场趋势分析完成（使用MarketTrendAnalyzer - 多周期共振+HMM）
- ✅ 主线轮动研究完成（2个热点主题）
- ✅ 财经新闻获取完成（20条新闻）

---

**脚本已创建**: 2026-01-11  
**维护者**: TRQuant Team
