# 综合PDF内容提取工具

这是一个功能强大的PDF内容提取工具，能够提取PDF中的文字、图表、图片等所有内容，并分类保存到不同文件夹中，便于后续分析和引用。

## 🚀 功能特性

### 📝 文本提取
- **多引擎支持**：使用`pdfplumber`、`PyPDF2`、`pdfminer`多种引擎
- **结构化输出**：提供完整文本、分页文本、结构化JSON格式
- **高精度**：保持原文档的文本结构和格式

### 🖼️ 图片提取
- **全页转换**：将每页转换为高清PNG图片（300 DPI）
- **嵌入图片**：提取PDF中嵌入的原始图片
- **多格式支持**：输出PNG格式，便于后续处理

### 📊 表格提取
- **多工具集成**：使用`tabula-py`、`camelot`、`pdfplumber`三种工具
- **多格式输出**：CSV、Excel格式，便于数据分析
- **可视化**：生成表格结构可视化图片

### 📈 图表检测
- **智能识别**：使用OpenCV进行图表区域检测
- **自动提取**：提取检测到的图表区域
- **标记显示**：在原页面上标记图表位置

### 📋 报告生成
- **HTML报告**：生成美观的可视化报告
- **JSON数据**：提供结构化的提取结果数据
- **使用指南**：自动生成使用说明

## 📦 安装依赖

### 方法1：自动安装（推荐）
```powershell
.\install-dependencies.ps1
```

### 方法2：手动安装
```bash
pip install PyPDF2 pdfplumber pdf2image Pillow pandas tabula-py camelot-py[cv] pdfminer.six matplotlib opencv-python numpy openpyxl
```

### 系统依赖
- **Python 3.7+**
- **Java**（用于tabula-py）
- **poppler-utils**（用于pdf2image）

#### Windows安装poppler
1. 下载：https://github.com/oschwartz10612/poppler-windows/releases
2. 解压到任意目录（如：`C:\poppler`）
3. 将`bin`目录添加到PATH环境变量

## 🎯 使用方法

### 方法1：批处理文件（最简单）
将PDF文件拖拽到`extract-pdf.bat`文件上即可

### 方法2：PowerShell脚本
```powershell
# 基本使用
.\comprehensive-pdf-extractor.ps1 -PdfPath "document.pdf"

# 指定输出目录
.\comprehensive-pdf-extractor.ps1 -PdfPath "document.pdf" -OutputDir "my_output"

# 只提取文本和图片
.\comprehensive-pdf-extractor.ps1 -PdfPath "document.pdf" -ExtractTables:$false
```

### 方法3：简化调用
```powershell
.\extract-pdf.ps1 -PdfFile "document.pdf"
```

### 方法4：Python直接调用
```bash
python pdf_extractor.py document.pdf --output-dir extracted_content
```

## 📁 输出结构

```
extracted_content_20250103_143022/
├── text/                          # 文本内容
│   ├── full_text.txt             # 完整文本
│   ├── structured_text.json      # 结构化文本
│   ├── detailed_text.txt         # 详细文本
│   └── page_001.txt              # 分页文本
├── images/                        # 图片内容
│   ├── page_001_full.png         # 完整页面
│   └── page_001_img_1.png        # 嵌入图片
├── tables/                        # 表格数据
│   ├── tabula_table_001.csv      # CSV格式
│   ├── tabula_table_001.xlsx     # Excel格式
│   └── camelot_table_001_visual.png # 表格可视化
├── charts/                        # 图表内容
│   ├── page_001_chart_1.png      # 检测的图表
│   └── page_001_marked.png       # 标记页面
├── metadata/                      # 元数据
│   └── extraction_metadata.json  # 提取元数据
├── reports/                       # 分析报告
│   ├── extraction_report.html    # HTML报告
│   └── extraction_report.json    # JSON报告
├── pdf_extractor.py              # 生成的Python脚本
└── 使用指南.md                    # 使用说明
```

## 🔧 参数说明

### PowerShell参数
- `-PdfPath`：PDF文件路径（必需）
- `-OutputDir`：输出目录名称（默认：pdf_extracted_content）
- `-ExtractText`：是否提取文本（默认：true）
- `-ExtractImages`：是否提取图片（默认：true）
- `-ExtractTables`：是否提取表格（默认：true）
- `-GenerateReport`：是否生成报告（默认：true）

### Python参数
- `pdf_path`：PDF文件路径（必需）
- `--output-dir`：输出目录
- `--no-text`：不提取文本
- `--no-images`：不提取图片
- `--no-tables`：不提取表格
- `--no-charts`：不检测图表

## 📊 使用示例

### 投资文档分析
```powershell
# 提取投资报告内容
.\extract-pdf.ps1 -PdfFile "AVGO_Analysis_Report.pdf"

# 查看HTML报告了解提取概况
# 使用text/full_text.txt进行关键词搜索
# 使用tables/目录中的数据进行财务分析
# 使用charts/目录中的图表进行趋势分析
```

### 学术论文处理
```powershell
# 提取学术论文
.\extract-pdf.ps1 -PdfFile "research_paper.pdf"

# 分析文本内容进行文献综述
# 提取表格数据进行统计分析
# 保存图表用于演示文稿
```

## 🛠️ 故障排除

### 常见问题

#### 1. "poppler not found" 错误
**解决方案**：
- Windows：安装poppler-utils并添加到PATH
- Mac：`brew install poppler`
- Linux：`sudo apt-get install poppler-utils`

#### 2. Java相关错误（tabula）
**解决方案**：
- 安装Java运行环境
- 或使用`--no-tables`参数跳过表格提取

#### 3. OpenCV安装失败
**解决方案**：
```bash
pip install opencv-python-headless
```

#### 4. 内存不足
**解决方案**：
- 处理大文件时分页处理
- 减少DPI设置（修改Python脚本中的dpi参数）

### 性能优化

#### 大文件处理
- 对于超过100页的PDF，建议分批处理
- 可以修改脚本中的DPI设置以减少内存使用

#### 提取质量调整
- 图片DPI：修改`convert_from_path(dpi=300)`中的数值
- 图表检测敏感度：调整`cv2.Canny`参数
- 表格检测精度：调整各表格提取工具的参数

## 📈 后续处理建议

### 文本分析
- 使用文本分析工具进行关键词提取
- 进行情感分析或主题建模
- 构建知识图谱

### 数据分析
- 将表格数据导入Excel/Python进行统计分析
- 使用可视化工具创建图表
- 进行时间序列分析

### 内容管理
- 整合到文档管理系统
- 建立搜索索引
- 创建内容标签体系

## 🔄 更新日志

### v1.0.0 (2025-01-03)
- 初始版本发布
- 支持文本、图片、表格、图表提取
- 生成HTML和JSON报告
- 多平台支持

## 📞 技术支持

如遇到问题，请检查：
1. Python环境是否正确安装
2. 所有依赖库是否安装成功
3. 系统依赖（Java、poppler）是否可用
4. PDF文件是否损坏或加密

## 📄 许可证

本工具仅供学习和研究使用，请遵守相关PDF文档的版权规定。 