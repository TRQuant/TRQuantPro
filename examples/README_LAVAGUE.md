# LaVague 使用示例

> **更新**: 2026-01-17  
> **目的**: 提供LaVague在TRQuant系统中的实际使用示例

---

## 📋 示例文件列表

### 1. 完整功能演示

- **`lavague_complete_demo.py`** - 展示6大应用场景的完整演示
- **`lavague_quick_demo.py`** - 快速演示（实际可运行）

### 2. 实际应用示例

- **`lavague_cninfo_603986.py`** - 从巨潮资讯网提取股票603986的公告

---

## 🚀 快速使用

### 提取股票公告（实际示例）

```bash
# 提取股票603986最近90天的公告
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python examples/lavague_cninfo_603986.py
```

**功能**:
- ✅ 访问巨潮资讯网
- ✅ 搜索指定股票代码
- ✅ 提取最近N天的所有公告
- ✅ 保存结果到JSON文件

**输出文件**:
- `examples/announcements_603986_90days.json` - 执行结果
- `examples/announcements_603986_extracted.json` - 提取的结构化数据

---

## 💡 自定义使用

### 修改股票代码和时间范围

编辑 `lavague_cninfo_603986.py`，修改以下变量：

```python
stock_code = "603986"  # 改为目标股票代码
days = 90              # 改为需要提取的天数
```

### 使用MCP工具（在Cursor Chat中）

```
使用crawler.lavague.execute工具，执行以下指令：
访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告
```

---

## 📝 注意事项

1. **API密钥**: 需要配置 `OPENAI_API_KEY` 环境变量
2. **网络访问**: 确保可以访问巨潮资讯网
3. **反爬虫**: 某些网站可能有访问限制
4. **执行时间**: LaVague需要调用LLM API，可能需要较长时间

---

## 🔗 相关文档

- `docs/LAVAGUE_IN_TRQUANT_COMPLETE_GUIDE.md` - 完整应用指南
- `docs/LAVAGUE_DEMO_GUIDE.md` - 演示指南
- `docs/LAVAGUE_INSTALLATION_FIX.md` - 安装问题修复
