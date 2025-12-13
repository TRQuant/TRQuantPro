# 数据收集工具安装指南

## 📦 安装依赖

### 方法1: 使用extension虚拟环境（推荐）

```bash
# 激活extension虚拟环境
source extension/venv/bin/activate  # Linux/macOS
# 或
extension\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r tools/data_collector/requirements-collector.txt

# 安装Playwright浏览器（可选，用于JavaScript渲染）
playwright install chromium
```

### 方法2: 使用安装脚本

```bash
# 运行安装脚本
bash scripts/install_data_collector.sh
```

### 方法3: 手动安装

```bash
# 核心依赖
pip install scrapy beautifulsoup4 requests requests-html

# 浏览器自动化（可选）
pip install playwright selenium
playwright install chromium

# 学术论文下载
pip install arxiv feedparser

# PDF处理
pip install pypdf2 pdfplumber pymupdf

# 文本处理
pip install markdown html2text

# 工具
pip install tqdm python-dotenv pyyaml
```

## 🔧 配置MCP服务器

### 1. 添加到 .cursor/mcp.json

将以下配置添加到 `.cursor/mcp.json` 的 `mcpServers` 部分：

```json
{
  "mcpServers": {
    "data-collector": {
      "command": "python3",
      "args": [
        "mcp_servers/data_collector_server.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
```

### 2. 重启Cursor

配置完成后，重启Cursor IDE以使MCP服务器生效。

## 🧪 测试安装

### 测试工具

```bash
# 运行示例代码
python tools/data_collector/examples/example_usage.py
```

### 测试MCP服务器

在Cursor中，可以通过MCP工具调用：
- `data_collector.crawl_web` - 爬取网页
- `data_collector.download_pdf` - 下载PDF
- `data_collector.collect_academic` - 收集学术论文
- `data_collector.recommend_sources` - 推荐信息源

## 📝 使用示例

### Python代码中使用

```python
from tools.data_collector import WebCrawler, AcademicScraper

# 爬取网页
crawler = WebCrawler(output_dir="data/collected")
files = crawler.collect("https://example.com", max_depth=2)

# 下载arXiv论文
scraper = AcademicScraper(output_dir="data/papers")
files = scraper.collect("arxiv", "quantitative+trading", max_results=10)
```

### MCP工具调用

在Cursor中，可以直接调用MCP工具：
- 右键点击 → "Call MCP Tool" → 选择 `data_collector.crawl_web`
- 或在对话中直接使用

## ⚠️ 注意事项

1. **遵守法律法规**
   - 遵守网站使用条款
   - 尊重版权
   - 不要过度爬取

2. **反爬虫策略**
   - 使用合理的请求间隔
   - 使用代理池（如需要）
   - 优先使用官方API

3. **网络环境**
   - 某些网站可能需要代理访问
   - 学术数据库可能需要机构订阅

## 🐛 故障排除

### 问题1: 导入错误

```
ModuleNotFoundError: No module named 'tools'
```

**解决方案**: 确保在项目根目录运行，或设置PYTHONPATH：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题2: Playwright浏览器未安装

```
playwright._impl._api_types.Error: Executable doesn't exist
```

**解决方案**: 安装Playwright浏览器：
```bash
playwright install chromium
```

### 问题3: MCP服务器无法启动

**解决方案**: 
1. 检查Python路径是否正确
2. 检查文件权限
3. 查看错误日志

---

*最后更新: 2025-12-11*

