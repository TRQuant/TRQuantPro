# PTrade API文档锚点页面爬取报告

**日期**: 2026-01-09  
**目标URL**: `https://ptradeapi.com/#PtradeAPI%E6%96%87%E6%A1%A3`  
**方法**: 使用Playwright + MCP工具（kb.add）

---

## 📋 爬取结果

### 文件生成
- ✅ `anchor_page_PtradeAPI文档.json` (1.1MB) - 完整页面HTML
- ✅ `section_PtradeAPI文档.json` (352B) - 初始提取内容
- ✅ `section_PtradeAPI文档_完整.json` (674B) - 完整锚点内容
- ✅ `section_PtradeAPI文档_完整提取.json` (1KB) - 完整提取内容

### 内容摘要
- **标题**: Ptrade API文档
- **内容长度**: 344 字符
- **关键信息**:
  - ✅ 包含试用账号信息
  - ✅ 包含支持的券商列表
  - ✅ 包含代码加密功能说明
  - ✅ 包含回测功能说明

---

## 📄 内容详情

### 主要信息
1. **权限开通**: 关注公众号并后台留言 "ptrade开通" 或 "ptrade试用"
2. **支持券商**: 国盛证券、国金证券、东莞证券、湘财证券、长江证券、国泰君安-海通等
3. **试用账号**: 55010687，密码：259800
4. **代码加密**: 支持代码加密下载与上传功能，保证源代码不泄密
5. **回测功能**: 券商实盘版无法盘中回测，可盘后回测；部分券商实盘版不支持回测

---

## 💾 知识库状态

- ✅ **已存入**: 使用`kb.add` MCP工具
- ✅ **分类**: PTrade_API
- ✅ **标签**: PTrade, API文档, 量化交易, 完整文档

---

## 🔍 验证方法

### 1. 检查本地文件
```bash
ls -lh docs/ptrade_crawled/mcp_crawl/*PtradeAPI*
```

### 2. 检查知识库
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='kb.search',
    arguments={
        'query': 'PTrade API文档 完整内容',
        'limit': 5
    }
)
```

---

**生成时间**: 2026-01-09  
**脚本**: `scripts/crawl_ptrade_with_mcp_tools.py` (修改版)
