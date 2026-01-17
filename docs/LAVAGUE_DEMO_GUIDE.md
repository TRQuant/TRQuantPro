# LaVague 功能演示指南

> **创建时间**: 2026-01-17  
> **目的**: 提供LaVague在TRQuant系统中的完整功能演示

---

## 📋 演示文件说明

### 1. 完整演示 (`lavague_complete_demo.py`)

**文件位置**: `examples/lavague_complete_demo.py`

**功能**: 展示LaVague在TRQuant系统中的**6大应用场景**，包括：

1. **自动化数据收集**
   - 公告收集（巨潮资讯网）
   - 研报收集（东方财富网）
   - 财务数据收集（同花顺）

2. **自动化表单填写和登录**
   - 模拟登录流程
   - 自动化数据查询

3. **智能数据提取**
   - 从复杂页面提取股票数据
   - 提取动态渲染的内容

4. **自动化测试和验证**
   - 数据源可用性检测
   - 数据完整性验证

5. **自动化工作流**
   - 每日数据更新工作流
   - 多数据源数据同步

6. **智能信息检索**
   - 投资主线信息收集
   - 竞争对手分析

**运行方式**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python examples/lavague_complete_demo.py
```

**注意**: 
- 这是完整演示，会尝试访问真实网站
- 某些网站可能有反爬虫机制
- 需要正确安装LaVague和配置API密钥

---

### 2. 快速演示 (`lavague_quick_demo.py`)

**文件位置**: `examples/lavague_quick_demo.py`

**功能**: 提供**实际可运行的简化版本**，展示LaVague的核心功能：

1. **基础使用**
   - 网页导航
   - 执行自然语言指令
   - 智能数据提取

2. **股票数据收集**
   - 访问股票页面
   - 提取实时数据
   - 执行复杂指令

3. **工作流自动化**
   - 多步骤任务执行
   - 工作流编排

**运行方式**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python examples/lavague_quick_demo.py
```

**优势**:
- ✅ 更轻量，运行更快
- ✅ 实际可运行
- ✅ 适合快速测试

---

## 🚀 快速开始

### 前置条件

1. **安装LaVague**
   ```bash
   cd /home/taotao/.cursor/worktrees/TRQuant/ope
   ./venv/bin/python -m pip install lavague
   ```

2. **配置API密钥**
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # 或使用其他模型
   export GEMINI_API_KEY="your-gemini-key"
   ```

3. **验证安装**
   ```bash
   ./venv/bin/python -c "import lavague; print('✅ LaVague安装成功')"
   ```

### 运行演示

#### 方式1: 快速演示（推荐）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python examples/lavague_quick_demo.py
```

#### 方式2: 完整演示

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python examples/lavague_complete_demo.py
```

---

## 📊 演示输出说明

### 输出内容

演示会输出以下信息：

1. **场景标题**: 每个场景的名称和描述
2. **执行步骤**: 详细的执行步骤
3. **执行结果**: 
   - ✅ 成功：显示成功信息和结果摘要
   - ❌ 失败：显示错误信息
   - ⏭️  跳过：显示跳过原因

4. **结果文件**: 
   - `examples/lavague_demo_results.json` - 完整演示结果（JSON格式）

### 结果文件格式

```json
{
  "demo_time": "2026-01-17T...",
  "scenarios": {
    "1_automated_data_collection": {
      "announcements": {
        "success": true,
        "count": "...",
        "message": "..."
      },
      "research_reports": {...},
      "financial_data": {...}
    },
    "2_automated_form_filling": {...},
    ...
  }
}
```

---

## 💡 使用示例

### 示例1: 收集股票公告

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

# 创建爬虫实例
crawler = get_lavague_crawler(headless=True)

# 执行指令
instruction = """
访问巨潮资讯网，搜索股票代码000001，
提取最近30天的所有公告
"""
result = crawler.execute_instruction(instruction)

# 处理结果
if result.get("success"):
    print("✅ 公告收集成功")
    # 解析result.get("data")获取公告数据
else:
    print(f"❌ 失败: {result.get('error')}")

# 关闭
crawler.close()
```

### 示例2: 提取股票实时数据

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

crawler = get_lavague_crawler(headless=True)

# 导航到股票页面
crawler.navigate("https://quote.eastmoney.com/sz000001.html")

# 提取数据
description = """
提取以下信息：
- 当前价格
- 涨跌幅
- 成交量
- 资金流向
"""
result = crawler.extract_data(description)

if result.get("success"):
    data = result.get("data")
    print(f"提取的数据: {data}")

crawler.close()
```

### 示例3: 自动化工作流

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

crawler = get_lavague_crawler(headless=True)

# 多步骤工作流
workflow = [
    "访问数据源网站",
    "登录账户",
    "下载最新数据",
    "验证数据完整性"
]

for step in workflow:
    result = crawler.execute_instruction(step)
    if not result.get("success"):
        print(f"步骤失败: {step}")
        break

crawler.close()
```

---

## ⚠️ 注意事项

### 1. API成本

LaVague使用LLM API，会产生费用：
- 使用较小的模型（gpt-4o-mini）可以降低成本
- 使用TokenCounter估算成本
- 批量处理任务，减少API调用

### 2. 网站限制

某些网站可能有反爬虫机制：
- 访问频率限制
- IP封禁
- 验证码
- JavaScript渲染

**建议**:
- 使用合理的延迟
- 遵守robots.txt
- 使用headless模式
- 考虑使用代理

### 3. 性能优化

- ✅ 使用headless模式（更快）
- ✅ 缓存常用数据
- ✅ 批量处理任务
- ✅ 设置合理的超时时间

### 4. 错误处理

- ✅ 实现重试机制
- ✅ 记录详细日志
- ✅ 提供降级方案（传统爬虫）

---

## 🔗 相关文档

- `docs/LAVAGUE_IN_TRQUANT_COMPLETE_GUIDE.md` - 完整应用指南
- `docs/LAVAGUE_INSTALLATION_FIX.md` - 安装问题修复
- `mcp_servers/crawlers/lavague_crawler.py` - LaVague爬虫实现

---

## 📝 总结

### 演示文件对比

| 特性 | 完整演示 | 快速演示 |
|------|---------|---------|
| **场景数量** | 6个完整场景 | 3个核心场景 |
| **运行时间** | 较长（10-30分钟） | 较短（2-5分钟） |
| **适用场景** | 全面了解功能 | 快速测试和验证 |
| **网站访问** | 多个真实网站 | 示例网站为主 |
| **推荐使用** | 学习和演示 | 日常测试 |

### 推荐使用流程

1. **首次使用**: 运行快速演示，了解基础功能
2. **深入学习**: 查看完整演示，了解所有场景
3. **实际应用**: 根据需求修改示例代码
4. **集成系统**: 参考集成方案，集成到TRQuant系统

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
