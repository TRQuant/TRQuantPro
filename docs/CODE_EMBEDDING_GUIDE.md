# 代码嵌入使用指南

## 📋 概述

使用Astro组件嵌入代码，实现代码与文档分离。代码更新后，文档自动显示最新版本，无需修改文档。

## 🎯 优势

1. **代码与文档分离**：代码存储在独立文件中，文档只引用
2. **自动更新**：代码更新后，文档自动显示最新版本
3. **版本管理**：代码可以独立版本管理
4. **避免重复**：修改代码时无需同步修改文档
5. **设计原理展示**：自动提取和显示设计原理说明

## 📁 代码文件结构

```
code_library/
├── 001_Chapter1_System_Overview/
│   └── 1.1/
│       └── code_1_1_1_example.py
├── 002_Chapter2_Data_Source/
│   └── 2.1/
│       └── code_2_1_1_data_source_manager.py
├── 003_Chapter3_Market_Analysis/
│   ├── 3.1/
│   │   └── code_3_1_1_trend_analyzer.py
│   └── 3.2/
│       ├── code_3_2_2_analyze_price_dimension.py
│       └── code_3_2_2_analyze_volume_dimension.py
└── ...
```

## 🔧 组件使用

### CodeBlockFromFile组件

**功能**：从文件路径直接读取代码并显示

**使用方式**：

```astro
---
import CodeBlockFromFile from '../../../components/CodeBlockFromFile.astro';
---

<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples={true}
  showLineNumbers={false}
/>
```

**参数说明**：

- `filePath`（必需）：代码文件路径，相对于项目根目录
- `language`（可选）：编程语言，默认 "python"
- `showDesignPrinciples`（可选）：是否显示设计原理，默认 true
- `showLineNumbers`（可选）：是否显示行号，默认 false

### CodeBlock组件（基于codeId）

**功能**：通过代码ID查找并显示代码（需要数据库支持）

**使用方式**：

```astro
---
import CodeBlock from '../../../components/CodeBlock.astro';
---

<CodeBlock 
  codeId="3.2.2.analyze_price_dimension"
  language="python"
  showDesignPrinciples={true}
  version="1.0.0"
/>
```

**参数说明**：

- `codeId`（必需）：代码ID，格式：章节.小节.函数名
- `language`（可选）：编程语言，默认 "python"
- `showDesignPrinciples`（可选）：是否显示设计原理，默认 true
- `showLineNumbers`（可选）：是否显示行号，默认 false
- `version`（可选）：指定版本号，默认最新版本

## 📝 代码文件格式

代码文件应包含：

1. **代码内容**：完整的函数或类定义
2. **设计原理说明**（可选）：在docstring或注释中

**示例**：

```python
def analyze_price_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析价格维度
    
    **设计原理**：
    - **多周期分析**：同时分析1日、5日、20日涨跌幅，提供不同时间尺度的价格变化
    - **相对位置**：计算价格在近期高低点之间的相对位置，反映价格水平
    
    **为什么这样设计**：
    1. **全面性**：多周期分析提供全面的价格变化信息
    2. **相对性**：相对位置比绝对价格更有意义，便于不同时期对比
    
    Args:
        data: 市场数据
    
    Returns:
        价格维度评分字典
    """
    # 设计原理：多周期涨跌幅计算
    # 原因：不同周期的涨跌幅反映不同时间尺度的价格变化
    price_change_1d = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]
    # ...
```

## 🔄 迁移流程

### 步骤1：提取代码到文件

```bash
# 使用代码管理工具提取代码
python scripts/code_manager.py \
    --action extract \
    --docs-dir extension/AShare-manual/src/pages/ashare-book6 \
    --code-lib-dir code_library \
    --db-config config/database_code_library.json
```

### 步骤2：更新文档使用组件

将文档中的代码块：

```markdown
```python
def analyze_price_dimension(data: pd.DataFrame) -> Dict[str, float]:
    # ...
```
```

替换为：

```astro
---
import CodeBlockFromFile from '../../../components/CodeBlockFromFile.astro';
---

<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples={true}
/>
```

### 步骤3：更新代码

直接修改代码文件：

```bash
# 编辑代码文件
vim code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py

# 文档会自动显示最新代码，无需修改文档
```

## 🎨 样式定制

组件支持通过CSS变量定制样式：

```css
:root {
  --code-bg: #f6f8fa;
  --principles-bg: #fff9e6;
  --border-color: #e1e4e8;
  --text-primary: #24292e;
  --text-secondary: #586069;
  --highlight-bg: #fff5b1;
}
```

## 📊 工作流程

```
1. 开发代码
   ↓
2. 保存到 code_library/
   ↓
3. 文档中使用组件引用
   ↓
4. 构建时自动读取最新代码
   ↓
5. 文档显示最新代码
```

## ✅ 最佳实践

1. **代码文件命名**：使用清晰的命名，如 `code_3_2_2_analyze_price_dimension.py`
2. **设计原理**：在代码注释中详细说明设计原理
3. **版本管理**：代码文件纳入Git版本管理
4. **文档备份**：保留原始代码作为注释备份（可选）
5. **测试验证**：更新代码后验证文档显示正常

## 🔍 故障排查

### 问题1：代码文件找不到

**错误**：`无法加载代码文件: xxx`

**解决**：
1. 检查文件路径是否正确
2. 确认文件是否存在
3. 检查文件权限

### 问题2：设计原理未显示

**原因**：代码文件中没有设计原理说明

**解决**：在代码的docstring或注释中添加设计原理说明

### 问题3：代码高亮不工作

**原因**：需要配置代码高亮库（如Prism.js）

**解决**：在Layout.astro中添加代码高亮库

