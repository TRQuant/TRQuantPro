# PTrade API文档侧栏页面完整爬取报告

**日期**: 2026-01-09  
**方法**: 使用Playwright + MCP工具（kb.add）  
**脚本**: `scripts/crawl_ptrade_sidebar_pages.py`

---

## 📊 爬取统计

### 链接统计
- **总锚点链接**: 216 个
- **总页面链接**: 12 个
- **已生成内容块**: 185 个
- **已生成页面文件**: 60 个
- **主页面文件**: ✅ 已保存
- **总内容大小**: ~0.5 MB

### 关键页面状态
- ✅ **快速入门** - 已爬取
- ✅ **新建策略** - 已爬取
- ✅ **新建回测** - 已爬取
- ✅ **新建交易** - 已爬取
- ✅ **开始写策略** - 已爬取
- ✅ **实用的策略** - 已爬取
- ✅ **必看-快速了解Ptrade** - 已爬取
- ✅ **视频教程** - 已爬取

---

## 📋 爬取内容分类

### 1. 入门指南
- 快速入门
- 必看-快速了解Ptrade
- 视频教程
- 开始写策略
- 简单但是完整的策略
- 添加一些交易
- 实用的策略

### 2. 策略开发
- 新建策略
- 新建回测
- 新建交易
- 策略运行周期
- 策略运行时间
- 交易策略委托下单时间
- 策略引擎简介
- 业务流程框架

### 3. 核心函数
- initialize(必选)
- before_trading_start(可选)
- handle_data(必选)
- after_trading_end(可选)
- tick_data(可选)
- on_order_response - 委托主推(可选)
- on_trade_response - 交易主推(可选)

### 4. API接口
- 设置函数（set_universe, set_benchmark, set_commission等）
- 定时周期性函数（run_daily, run_interval）
- 获取信息函数（get_trading_day, get_history, get_price等）
- 交易相关函数（order, order_target, order_value等）
- 融资融券专用函数
- 期货专用函数
- 计算函数（get_MACD, get_KDJ, get_RSI, get_CCI等）

---

## 💾 知识库状态

- ✅ **已存入**: 使用`kb.add` MCP工具
- ✅ **分类**: PTrade_API
- ✅ **标签**: PTrade, API文档, 量化交易, 策略开发, 回测, 交易, 数据, API接口, 快速入门等

---

## 📁 文件结构

```
docs/ptrade_crawled/mcp_crawl/
├── main_page.json                    # 主页面HTML
├── sidebar_links.json                # 侧栏链接列表
├── content_hashes.json               # 内容哈希（去重）
├── section_*.json                    # 内容块文件（185个）
├── anchor_page_*.json                # 锚点页面文件（60个）
├── sidebar_crawl.log                 # 爬取日志
└── SIDEBAR_CRAWL_REPORT.md          # 本报告
```

---

## 🔍 验证方法

### 1. 检查本地文件
```bash
# 统计内容块文件
ls -lh docs/ptrade_crawled/mcp_crawl/section_*.json | wc -l

# 查看关键页面
ls -lh docs/ptrade_crawled/mcp_crawl/section_*快速入门*.json
ls -lh docs/ptrade_crawled/mcp_crawl/section_*新建策略*.json
```

### 2. 检查知识库
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='kb.search',
    arguments={
        'query': 'PTrade 快速入门',
        'limit': 5
    }
)
```

---

## 📝 注意事项

1. **去重机制**: 使用MD5哈希去重，避免重复内容
2. **内容长度限制**: 单个内容块限制50,000字符
3. **代码块提取**: 最多提取10个代码块
4. **文件名安全**: 锚点ID中的特殊字符会被替换为下划线
5. **MCP工具回退**: 如果`kb.add` MCP工具失败，自动回退到直接函数调用
6. **跳过已爬取**: 自动检测已存在的文件，跳过重复爬取

---

## 🚀 后续优化

1. **并行处理**: 可以并行爬取多个锚点页面，提高效率
2. **增量更新**: 基于内容哈希实现增量更新
3. **内容验证**: 验证存入知识库的内容完整性
4. **错误重试**: 添加失败重试机制
5. **页面链接**: 爬取非锚点的页面链接（如stra.html, trade.html等）

---

**生成时间**: 2026-01-09  
**脚本版本**: v1.0
