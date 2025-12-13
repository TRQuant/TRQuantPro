# 代码嵌入示例

## 📋 使用示例

### 示例1：基本使用

在文档的frontmatter中导入组件：

```astro
---
import CodeBlockFromFile from '../../../components/CodeBlockFromFile.astro';

title: "3.2 市场状态"
---
```

在文档中使用组件：

```astro
<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples={true}
/>
```

### 示例2：不显示设计原理

```astro
<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples={false}
/>
```

### 示例3：显示行号

```astro
<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples={true}
  showLineNumbers={true}
/>
```

## 🔄 工作流程

### 1. 创建代码文件

```bash
# 创建代码文件
vim code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py

# 编写代码（包含设计原理说明）
```

### 2. 在文档中使用组件

```astro
<CodeBlockFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
/>
```

### 3. 更新代码

```bash
# 直接修改代码文件
vim code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py

# 文档会自动显示最新代码，无需修改文档
```

## ✅ 优势

1. **代码与文档分离**：代码存储在独立文件中
2. **自动更新**：代码更新后文档自动显示最新版本
3. **避免重复**：修改代码时无需同步修改文档
4. **版本管理**：代码文件可以独立版本管理
5. **设计原理展示**：自动提取和显示设计原理说明

