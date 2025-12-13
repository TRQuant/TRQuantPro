# 代码文件头注释格式规范

## ✅ 统一格式

所有由脚本生成的代码文件都包含统一的文件头注释，格式如下：

```python
"""
文件名: code_3_3_score_macro_dimension.py
保存路径: code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py
绝对路径: /home/taotao/dev/QuantTest/TRQuant/code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.3_Five_Dimensional_Scoring_CN.md
提取时间: 2025-12-13 08:49:08
函数/类名: score_macro_dimension

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。

在Markdown中使用方式：
<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>
"""

from typing import Dict, List, Optional

def score_macro_dimension(...):
    ...
```

## 📋 注释内容说明

### 1. 文件信息
- **文件名**: 代码文件的名称
- **保存路径**: 相对于项目根目录的路径
- **绝对路径**: 完整的文件系统路径
- **来源文件**: 提取代码的Markdown文件路径
- **提取时间**: 代码提取的时间戳
- **函数/类名**: 代码中的主要函数或类名

### 2. 使用说明
- 说明文件来源和生成方式
- 说明如何修改和使用
- 提供Markdown引用示例

## 🔧 脚本实现

文件头注释由 `extract_code_to_files.py` 脚本的 `_generate_file_header()` 方法统一生成：

```python
def _generate_file_header(self, code_file_path: Path, code_block: Dict) -> str:
    """生成文件头注释（统一格式）"""
    # 计算路径信息
    relative_path = code_file_path.relative_to(PROJECT_ROOT)
    absolute_path = str(code_file_path.resolve())
    source_markdown = str(self.markdown_file.relative_to(PROJECT_ROOT))
    
    # 生成注释
    header = f'''"""
文件名: {code_file_path.name}
保存路径: {relative_path_str}
绝对路径: {absolute_path}
来源文件: {source_markdown}
提取时间: {extract_time}
函数/类名: {func_or_class_name}
...
"""
'''
    return header
```

## ✅ 验证方法

### 检查文件头

```bash
# 查看文件头
head -20 code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py

# 验证所有文件都有文件头
grep -l '^"""' code_library/003_Chapter3_Market_Analysis/3.3/*.py
```

### 验证格式

文件头注释应该：
1. ✅ 在文件最顶部（第1行开始）
2. ✅ 使用三引号 `"""` 包围
3. ✅ 包含所有必需信息
4. ✅ 格式统一规范

## 🎯 优势

1. **可追溯性**：清楚知道代码来源
2. **路径信息**：便于查找和引用
3. **使用说明**：提供使用示例
4. **统一格式**：所有文件格式一致

---

**更新时间**: 2025-12-13  
**版本**: v1.0.0  
**状态**: ✅ 已实现

