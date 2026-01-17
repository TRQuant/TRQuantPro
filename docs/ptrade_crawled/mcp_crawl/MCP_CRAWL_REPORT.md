# PTrade API文档 - MCP工具爬取报告

**日期**: 2026-01-09  
**方法**: 使用MCP工具（Playwright + kb.add）完整爬取PTrade API文档  
**脚本**: `scripts/crawl_ptrade_with_mcp_tools.py`

---

## 📋 爬取方法

### 1. 工具选择
- **主工具**: Playwright（直接调用，非MCP工具）
- **知识库工具**: `kb.add` MCP工具（优先） + `knowledge_add` 直接调用（回退）
- **原因**: Selenium MCP工具返回数据为空，改用Playwright直接调用

### 2. 爬取流程
1. 使用Playwright访问主页面 `https://ptradeapi.com/`
2. 等待页面完全加载（networkidle + 5秒额外等待）
3. 提取HTML内容
4. 使用BeautifulSoup解析HTML，提取所有有ID的元素作为锚点内容块
5. 对每个内容块：
   - 提取标题、内容、代码块
   - 计算内容哈希（去重）
   - 分类和标签
   - 存入RAG知识库（优先使用`kb.add` MCP工具）
   - 保存到本地JSON文件（备份）

---

## 📊 爬取结果

### 文件统计
- **主页面**: `main_page.json` (1.1MB) ✅
- **内容块文件**: `section_*.json` (124个) ✅
- **总内容大小**: 0.22 MB
- **内容哈希**: `content_hashes.json` (124个去重记录) ✅

### 知识库统计
- **存入知识库**: 使用`kb.add` MCP工具 ✅
- **调用次数**: 从日志看，每个内容块都成功调用了`kb.add`
- **分类**: PTrade_API
- **标签**: PTrade, API文档, 量化交易, API接口, 交易, 数据, 策略开发, 回测等

### 内容块示例
1. Ptrade API文档
2. after_trading_end（可选）
3. after_trading_order - 盘后固定价委托(股票)
4. before_trading_start（可选）
5. buy_close - 空平
... (共124个内容块)

---

## 🔍 验证方法

### 1. 检查知识库
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='kb.search',
    arguments={
        'query': 'PTrade API',
        'limit': 10
    }
)
```

### 2. 检查本地文件
```bash
ls -lh docs/ptrade_crawled/mcp_crawl/*.json
```

### 3. 查看爬取日志
```bash
tail -f docs/ptrade_crawled/mcp_crawl/crawl.log
```

---

## 📝 注意事项

1. **去重机制**: 使用MD5哈希去重，避免重复内容
2. **内容长度限制**: 单个内容块限制50,000字符
3. **代码块提取**: 最多提取10个代码块
4. **文件名安全**: 锚点ID中的特殊字符会被替换为下划线
5. **MCP工具回退**: 如果`kb.add` MCP工具失败，自动回退到直接函数调用

---

## 🚀 后续优化

1. **并行处理**: 可以并行提取多个锚点内容
2. **增量更新**: 基于内容哈希实现增量更新
3. **内容验证**: 验证存入知识库的内容完整性
4. **错误重试**: 添加失败重试机制

---

**生成时间**: 2026-01-09  
**脚本版本**: v1.0
