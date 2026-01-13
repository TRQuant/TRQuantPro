# AKShare知识库构建总结

> **创建时间**: 2026-01-12  
> **状态**: ✅ 已完成标准流程和工具开发

---

## 📋 已完成工作

### 1. ✅ 标准知识库构建流程定义

创建了标准化的知识库构建流程文档：
- **位置**: `docs/knowledge_base/STANDARD_KB_BUILD_PROCESS.md`
- **内容**: 4个核心步骤的详细说明
  1. 使用MCP工具下载/智能爬取
  2. 构建完整的RAG知识库
  3. 测试并完善
  4. 工具和流程进化

### 2. ✅ AKShare知识库构建脚本

创建了完整的构建脚本：
- **位置**: `scripts/kb/build_kb_akshare.py`
- **功能**:
  - 智能选择爬虫工具（MCP工具优先，支持回退）
  - 内容解析（针对Sphinx文档结构）
  - 智能分类和标签
  - 去重和验证
  - 存入知识库（优先MCP工具，支持回退）

### 3. ✅ 测试脚本

创建了测试脚本用于验证工具可用性：
- **位置**: `scripts/kb/test_kb_build.py`
- **测试内容**:
  - MCP工具可用性
  - 直接函数可用性
  - 爬虫工具测试
  - 知识库添加功能测试

---

## 🚀 使用方法

### 步骤1: 测试工具可用性

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/kb/test_kb_build.py
```

### 步骤2: 开始构建知识库

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/kb/build_kb_akshare.py
```

**注意**: 
- 脚本支持断点续传（会保存已访问的URL和内容哈希）
- 如需重新开始，删除 `docs/akshare_crawled/visited_urls.json` 和 `content_hashes.json`

### 步骤3: 监控进度

脚本会实时显示：
- 爬取页面数
- 找到内容块数
- 成功保存数
- 保存失败数
- 跳过重复数

### 步骤4: 查看统计信息

脚本结束后会显示完整的统计信息。

---

## 🔧 工具特性

### 智能爬虫选择

脚本会按以下顺序尝试：
1. **Playwright** (直接调用Python库) ⭐ 推荐
   - 最快、最可靠
   - 支持JavaScript渲染
   - 自动等待页面加载
2. **OpenManus** (通过MCP工具)
   - 智能浏览器工具
   - 支持复杂交互
3. MCP工具 - 基础爬虫 (`crawler.fetch`)
4. MCP工具 - Selenium (`crawler.selenium.fetch`)
5. 直接函数 - 基础爬虫
6. 直接函数 - Selenium

### 内容解析策略

针对Sphinx文档结构，使用三层解析策略：
1. **方法1**: 查找所有有ID的元素（最通用）
2. **方法2**: 提取主要内容区域，按标题分割
3. **方法3**: 将整个页面作为一个条目（兜底）

### 智能分类和标签

- **分类**: 根据内容自动判断（lesson/practice/reference）
- **标签**: 基于关键词自动生成（股票数据、期货数据、API接口等）

### 去重机制

- 使用内容哈希（MD5）去重
- 支持断点续传
- 自动保存状态

---

## 📊 测试结果

### 工具测试结果

```
✅ MCP工具可用
✅ 直接函数可用
✅ 爬虫工具成功
✅ 知识库添加功能成功
```

所有测试通过，可以开始构建知识库。

---

## 📁 文件结构

```
scripts/kb/
├── build_kb_akshare.py          # AKShare知识库构建脚本
├── test_kb_build.py             # 测试脚本
└── utils/                        # 工具函数（待扩展）

docs/knowledge_base/
├── STANDARD_KB_BUILD_PROCESS.md  # 标准流程文档
└── AKSHARE_KB_BUILD_SUMMARY.md   # 本文档

docs/akshare_crawled/
├── visited_urls.json             # 已访问URL（断点续传）
├── content_hashes.json           # 内容哈希（去重）
└── [其他输出文件]
```

---

## 🔄 下一步工作

### 1. 实际运行构建

运行脚本开始构建AKShare知识库：
```bash
./venv/bin/python scripts/kb/build_kb_akshare.py
```

### 2. 监控和优化

- 观察爬取效果
- 根据实际情况调整解析逻辑
- 优化分类和标签规则

### 3. 验证知识库

构建完成后，使用搜索功能验证：
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='knowledge.search',
    arguments={
        'query': 'AKShare 股票数据',
        'limit': 10
    }
)
```

### 4. 流程进化

根据实际使用情况：
- 记录问题和改进建议
- 更新工具和流程
- 文档化最佳实践

---

## 📝 注意事项

1. **网络请求**: 脚本会进行大量网络请求，请确保网络连接稳定
2. **请求频率**: 脚本已设置延迟（每页1秒），避免请求过快
3. **断点续传**: 支持中断后继续，无需重新开始
4. **资源占用**: 爬取过程可能占用较多内存和CPU

---

## 🔗 相关文档

- [标准知识库构建流程](./STANDARD_KB_BUILD_PROCESS.md)
- [MCP工具调用方式](../CLAUDE.md#mcp工具使用)
- [爬虫工具总结](../ptrade_crawled/CRAWLER_TOOLS_SUMMARY.md)

---

**最后更新**: 2026-01-12  
**维护者**: TRQuant Team
