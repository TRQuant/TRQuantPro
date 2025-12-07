# PDF中代码提取指南

## 🎯 问题：PDF中有代码，应该用什么读取？

**答案：使用 `pdfplumber` + 专门的代码提取方法**

### 为什么选择 pdfplumber？

1. ✅ **保持格式**：可以保持代码的缩进、换行
2. ✅ **识别等宽字体**：代码通常使用等宽字体（Courier、Monaco等）
3. ✅ **布局分析**：可以分析字符位置，重建代码结构
4. ✅ **API简洁**：易于使用

---

## 🚀 使用方法

### 方法1：快速提取（推荐）

```python
from utils.pdf_reader import extract_code_from_pdf

# 提取所有代码块
code_blocks = extract_code_from_pdf(
    "strategy_guide.pdf",
    preserve_formatting=True,  # 保持格式
    detect_language=True       # 检测语言
)

# 遍历代码块
for block in code_blocks:
    print(f"第 {block['page']} 页")
    print(f"语言: {block['language']}")
    print(f"行数: {block['lines']}")
    print("代码:")
    print(block['code'])
    print("-" * 50)
```

### 方法2：完整控制

```python
from utils.pdf_reader import PDFReader

reader = PDFReader("document.pdf")

# 提取代码块
code_blocks = reader.extract_code_blocks(
    page_num=None,              # None=所有页，或指定页码
    preserve_formatting=True,   # 保持格式（推荐）
    detect_language=True        # 检测语言
)

# 按语言分组
python_blocks = [b for b in code_blocks if b['language'] == 'python']
js_blocks = [b for b in code_blocks if b['language'] == 'javascript']

# 保存代码
for i, block in enumerate(python_blocks, 1):
    filename = f"extracted_code_{i}.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(block['code'])
```

### 方法3：提取特定页的代码

```python
from utils.pdf_reader import PDFReader

reader = PDFReader("document.pdf")

# 只提取第5页的代码
code_blocks = reader.extract_code_blocks(page_num=5)

# 只提取第10-15页的代码
all_blocks = []
for page in range(10, 16):
    blocks = reader.extract_code_blocks(page_num=page)
    all_blocks.extend(blocks)
```

---

## 📊 代码检测原理

### 1. 等宽字体识别

代码通常使用等宽字体（Monospace），工具会：
- 识别等宽字体区域
- 提取该区域的文本
- 保持字符位置关系

### 2. 代码特征检测

工具会检测以下特征：
- ✅ **关键字**：`def`, `class`, `import`, `function`, `const` 等
- ✅ **符号**：`()`, `[]`, `{}`, `=>`, `->` 等
- ✅ **结构**：多行、缩进、平均行长短

### 3. 语言检测

支持检测的语言：
- Python（`def`, `import`, `print`）
- JavaScript/TypeScript（`function`, `const`, `=>`）
- Java（`public class`, `System.out`）
- C/C++（`#include`, `int main`）
- SQL（`SELECT`, `FROM`, `WHERE`）
- Shell/Bash（`#!/bin/`, `echo`）

---

## 💡 使用场景

### 场景1：提取策略代码

```python
from utils.pdf_reader import extract_code_from_pdf

# 从策略文档中提取代码
code_blocks = extract_code_from_pdf("strategy_guide.pdf")

# 只提取Python代码
python_code = [b['code'] for b in code_blocks if b['language'] == 'python']

# 保存到文件
for i, code in enumerate(python_code, 1):
    with open(f"strategy_{i}.py", 'w', encoding='utf-8') as f:
        f.write(code)
```

### 场景2：提取配置示例

```python
from utils.pdf_reader import PDFReader

reader = PDFReader("config_guide.pdf")

# 提取所有代码块
code_blocks = reader.extract_code_blocks()

# 查找包含配置的代码
config_blocks = [
    b for b in code_blocks
    if 'config' in b['code'].lower() or 'json' in b['code'].lower()
]

for block in config_blocks:
    print(f"配置代码（第{block['page']}页）:")
    print(block['code'])
```

### 场景3：批量处理多个PDF

```python
from pathlib import Path
from utils.pdf_reader import extract_code_from_pdf

pdf_dir = Path("docs")
output_dir = Path("extracted_code")
output_dir.mkdir(exist_ok=True)

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"处理: {pdf_file.name}")
    
    code_blocks = extract_code_from_pdf(str(pdf_file))
    
    # 按语言保存
    for block in code_blocks:
        lang = block['language'] or 'unknown'
        ext = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'sql': '.sql',
            'shell': '.sh'
        }.get(lang, '.txt')
        
        filename = output_dir / f"{pdf_file.stem}_page{block['page']}{ext}"
        filename.write_text(block['code'], encoding='utf-8')
```

---

## ⚠️ 注意事项

### 1. 格式保持

- ✅ **推荐**：`preserve_formatting=True`（使用layout模式）
- ⚠️ **注意**：某些PDF可能格式不完整

### 2. 代码截图

如果PDF中的代码是**截图/图片**：
- 需要先使用OCR工具（如Tesseract）
- 或使用 `pdf2image` + OCR

```python
# 如果代码是图片，需要OCR
from pdf2image import convert_from_path
import pytesseract

pages = convert_from_path("document.pdf", dpi=300)
for page in pages:
    code_text = pytesseract.image_to_string(page, lang='eng')
    # 处理提取的文本
```

### 3. 复杂布局

对于复杂布局的PDF：
- 可能需要手动调整参数
- 可以尝试不同的提取方法

---

## 🔧 高级用法

### 自定义代码检测

```python
from utils.pdf_reader import PDFReader

reader = PDFReader("document.pdf")

# 提取所有文本
text = reader.extract_text()

# 自定义代码块检测
import re

# 查找Python函数定义
python_functions = re.findall(r'def\s+\w+\s*\([^)]*\):.*?(?=\n\ndef|\nclass|\Z)', text, re.DOTALL)

for func in python_functions:
    print(func)
```

### 结合大模型分析

```python
from utils.pdf_reader import extract_code_from_pdf
from core.ai_assistant import AIAssistant

# 提取代码
code_blocks = extract_code_from_pdf("guide.pdf")

# 使用AI分析代码
assistant = AIAssistant()
for block in code_blocks:
    if block['language'] == 'python':
        response = assistant.ask(
            f"请分析以下Python代码的功能和用途：\n\n{block['code']}"
        )
        print(f"分析结果：{response}")
```

---

## 📝 最佳实践

1. **优先使用 `preserve_formatting=True`**
   - 保持代码格式对代码质量很重要

2. **检测语言后验证**
   - 自动检测可能不准确，建议人工验证

3. **保存原始代码块**
   - 保留页码信息，便于追溯

4. **处理大文件时分页**
   - 避免内存溢出

---

## 🔗 相关资源

- [pdfplumber文档](https://github.com/jsvine/pdfplumber)
- [PDF代码提取工具](../utils/pdf_reader.py)
- [OCR工具（用于图片代码）](https://github.com/tesseract-ocr/tesseract)



