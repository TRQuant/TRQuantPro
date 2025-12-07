# Requirements 文件更新说明

## 📋 更新日期
2025-12-07

## 🎯 更新内容

### 新增 PDF 处理库
为了支持 PDF 读取和代码提取功能，已在所有 requirements 文件中添加：

```
pdfplumber>=0.10.0
PyPDF2>=3.0.0
pdfminer.six>=20221105
```

### 更新的文件

1. **`requirements.txt`** (根目录)
   - ✅ 清理了 4434 行重复内容 → 93 行
   - ✅ 添加 PDF 处理库
   - ✅ 添加跨平台兼容性说明

2. **`extension/requirements.txt`**
   - ✅ 添加 PDF 处理库
   - ✅ 保持原有结构

3. **`extension/python/requirements.txt`**
   - ✅ 添加 PDF 处理库
   - ✅ 保持分层设计

---

## 🌍 跨平台兼容性

### 支持的平台
- ✅ **Linux** (Ubuntu/Debian/CentOS/Fedora)
- ✅ **macOS** (Intel/Apple Silicon)
- ✅ **Windows** (10/11)

### 版本要求
- Python >= 3.8
- 所有库均使用 `>=` 版本约束，确保兼容性

---

## 📦 安装方式

### 方式1：完整安装（推荐）
```bash
# 根目录
pip install -r requirements.txt

# Extension目录
cd extension
pip install -r requirements.txt
```

### 方式2：仅安装 PDF 库
```bash
pip install pdfplumber>=0.10.0 PyPDF2>=3.0.0 pdfminer.six>=20221105
```

### 方式3：使用虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

---

## ⚠️ 系统依赖（可选）

### PDF 处理库的系统依赖

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev

# CentOS/RHEL
sudo yum install libjpeg-devel zlib-devel
```

#### macOS
```bash
brew install jpeg zlib
```

#### Windows
- 通常已包含在 Python 安装中
- 如遇问题，安装 Visual C++ Redistributable

---

## 🔍 验证安装

```bash
# 验证 PDF 库安装
python -c "import pdfplumber; import PyPDF2; from pdfminer.high_level import extract_text; print('✅ 所有PDF库安装成功！')"
```

---

## 📝 使用示例

```python
# 使用 PDF 读取工具
from utils.pdf_reader import PDFReader, extract_code_from_pdf

# 提取代码
code_blocks = extract_code_from_pdf("document.pdf")

# 提取文本
reader = PDFReader("document.pdf")
text = reader.extract_text()
```

---

## 🔄 版本历史

### v1.0.0 (2025-12-07)
- 添加 PDF 处理库支持
- 清理根目录 requirements.txt 重复内容
- 统一所有 requirements 文件格式
- 添加跨平台兼容性说明

---

## 📚 相关文档

- [PDF 读取指南](./PDF_READING_GUIDE.md)
- [PDF 代码提取指南](./PDF_CODE_EXTRACTION.md)
- [GUI 整合指南](./GUI_INTEGRATION_GUIDE.md)


