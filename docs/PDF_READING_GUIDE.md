# PDF读取和大模型集成指南

## 📚 问题解答

### 1. pdfplumber 是否最好？

**答案：对于大多数场景，pdfplumber 是最佳选择之一，但建议组合使用。**

#### pdfplumber 的优势
- ✅ **表格提取准确**：能准确识别表格结构
- ✅ **文本结构保持好**：保留段落和布局信息
- ✅ **API简洁易用**：代码清晰，易于维护
- ✅ **页面级操作**：支持按页提取，内存友好

#### 推荐的工具组合
| 用途 | 首选工具 | 备选工具 |
|------|---------|---------|
| 文本提取 | pdfplumber | pdfminer |
| 表格提取 | pdfplumber | tabula-py, camelot |
| 元数据 | PyPDF2 | - |
| 图片提取 | pdf2image | - |

### 2. 大模型能否直接读取PDF？

**答案：部分API支持，但代码中通常需要先提取文本。**

#### 直接支持PDF的API
- ✅ **Claude 3.5 Sonnet**：支持直接上传PDF文件
- ✅ **GPT-4 Vision**：可以处理PDF（作为图片）
- ⚠️ **大多数API**：需要先转换为文本

#### 推荐方案
```python
from utils.pdf_reader import PDFReader, read_pdf_for_llm

# 方法1：快速使用
text = read_pdf_for_llm("document.pdf", max_length=50000)
# 直接传给大模型
response = llm_api.chat(messages=[
    {"role": "user", "content": f"请分析以下PDF内容：\n\n{text}"}
])

# 方法2：完整控制
reader = PDFReader("document.pdf")
reader.extract_metadata()
reader.extract_text()
reader.extract_tables()

# 转换为LLM格式
llm_text = reader.to_llm_format(
    include_metadata=True,
    include_tables=True,
    max_length=50000
)
```

---

## 🚀 使用示例

### 基础使用

```python
from utils.pdf_reader import PDFReader

# 创建读取器
reader = PDFReader("投资报告.pdf")

# 提取元数据
metadata = reader.extract_metadata()
print(f"标题: {metadata['title']}")
print(f"页数: {metadata['total_pages']}")

# 提取文本
text = reader.extract_text()
print(f"文本长度: {len(text)} 字符")

# 提取表格
tables = reader.extract_tables()
print(f"找到 {len(tables)} 个表格")
```

### 大模型集成

```python
from utils.pdf_reader import read_pdf_for_llm
from core.ai_assistant import AIAssistant

# 读取PDF并转换为LLM格式
pdf_content = read_pdf_for_llm(
    "策略报告.pdf",
    max_length=50000,  # 限制长度避免超出token限制
    include_tables=True  # 包含表格数据
)

# 使用AI助手分析
assistant = AIAssistant()
response = assistant.ask(
    f"请分析以下投资报告，提取关键信息：\n\n{pdf_content}"
)
print(response)
```

### 批量处理

```python
from pathlib import Path
from utils.pdf_reader import PDFReader

pdf_dir = Path("docs/reports")
output_dir = Path("extracted_content")

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"处理: {pdf_file.name}")
    
    reader = PDFReader(str(pdf_file))
    
    # 保存提取的内容
    saved_files = reader.save_extracted_content(
        str(output_dir / pdf_file.stem),
        include_tables=True
    )
    
    print(f"已保存到: {saved_files}")
```

### 与工作流集成

```python
# 在8步工作流中使用PDF读取
from utils.pdf_reader import PDFReader

def process_research_document(pdf_path: str):
    """处理研究报告PDF"""
    reader = PDFReader(pdf_path)
    
    # 提取关键信息
    metadata = reader.extract_metadata()
    text = reader.extract_text()
    tables = reader.extract_tables()
    
    # 转换为结构化数据
    llm_text = reader.to_llm_format(
        include_metadata=True,
        include_tables=True
    )
    
    # 传给AI分析
    # ... 后续处理
```

---

## 📊 性能对比

### 不同工具的提取质量

| 工具 | 文本质量 | 表格质量 | 速度 | 内存占用 |
|------|---------|---------|------|---------|
| pdfplumber | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| pdfminer | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| PyPDF2 | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| tabula-py | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### 推荐策略

1. **默认使用 pdfplumber**：平衡了质量和性能
2. **复杂表格用 tabula-py**：作为备选
3. **大文件分页处理**：避免内存溢出
4. **组合使用**：根据需求选择工具

---

## 🔧 安装依赖

```bash
# 核心依赖
pip install pdfplumber PyPDF2 pdfminer.six

# 可选依赖（用于表格和图片）
pip install tabula-py camelot-py[cv] pdf2image Pillow

# 完整安装（包含所有功能）
pip install pdfplumber PyPDF2 pdfminer.six tabula-py camelot-py[cv] pdf2image Pillow opencv-python
```

---

## ⚠️ 注意事项

### 1. 大文件处理
- 超过100页的PDF建议分页处理
- 使用 `page_range` 参数限制范围
- 设置 `max_length` 避免超出token限制

### 2. 内存管理
- pdfplumber 按页加载，内存友好
- 处理完及时释放资源（使用 `with` 语句）

### 3. 编码问题
- 确保PDF文件编码正确
- 输出文本使用UTF-8编码

### 4. 表格提取
- 复杂表格可能需要手动调整
- 可以尝试多种工具组合

---

## 📝 最佳实践

### 1. 统一使用工具类
```python
# ✅ 推荐：使用统一的工具类
from utils.pdf_reader import PDFReader

# ❌ 不推荐：直接使用多个库
import pdfplumber
import PyPDF2
```

### 2. 错误处理
```python
try:
    reader = PDFReader("document.pdf")
    text = reader.extract_text()
except FileNotFoundError:
    print("PDF文件不存在")
except ImportError as e:
    print(f"缺少依赖: {e}")
except Exception as e:
    print(f"提取失败: {e}")
```

### 3. 缓存结果
```python
# 避免重复提取
if not reader._extracted_text:
    reader.extract_text()
```

### 4. 长度控制
```python
# 控制输出长度，避免超出API限制
llm_text = reader.to_llm_format(max_length=50000)
```

---

## 🔗 相关资源

- [pdfplumber文档](https://github.com/jsvine/pdfplumber)
- [PyPDF2文档](https://pypdf2.readthedocs.io/)
- [pdfminer文档](https://pdfminersix.readthedocs.io/)
- [项目PDF处理脚本](../extension/AShare-manual/scripts/comprehensive-pdf-extractor.ps1)



