# 代码提取和迁移脚本使用指南

## 📋 功能说明

这些脚本用于自动化代码迁移过程：

1. **提取代码块**：从Markdown文件中提取Python代码块
2. **保存独立文件**：将代码保存到 `code_library` 目录
3. **更新Markdown**：将代码块替换为 `<CodeFromFile>` 标签
4. **自动增强**：添加必要的导入和设计原理说明

## 🚀 使用方法

### 1. 单个文件处理

```bash
# 处理单个Markdown文件
python scripts/extract_code_to_files.py extension/AShare-manual/src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md

# 预览模式（不实际修改文件）
python scripts/extract_code_to_files.py extension/AShare-manual/src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md --dry-run
```

### 2. 批量处理

```bash
# 批量处理所有Markdown文件
python scripts/batch_extract_code.py

# 只处理第3章
python scripts/batch_extract_code.py --chapter 003

# 预览模式
python scripts/batch_extract_code.py --dry-run
```

## 📁 输出结构

代码文件会保存到以下结构：

```
code_library/
  └── 003_Chapter3_Market_Analysis/
      ├── 3.1/
      │   ├── code_3_1_1_calculate_sma.py
      │   ├── code_3_1_1_calculate_ema.py
      │   └── ...
      └── 3.2/
          ├── code_3_2_2_analyze_price_dimension.py
          └── ...
```

## 🔧 功能特性

### 1. 自动提取

- 自动识别Python代码块
- 提取函数名或类名作为文件名
- 从文件路径提取章节信息

### 2. 代码增强

- 自动添加必要的导入（pandas, numpy, typing等）
- 检查并添加设计原理说明（如果缺失）
- 保持代码格式和注释

### 3. Markdown更新

- 将代码块替换为 `<CodeFromFile>` 标签
- 保留原始代码作为注释（备份）
- 自动生成相对路径

### 4. 安全机制

- 预览模式：可以先预览，不实际修改
- 自动备份：更新前自动备份原文件
- 错误处理：处理失败不影响其他文件

## 📝 示例

### 输入（Markdown文件）

```markdown
### 简单移动平均线

```python
def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """计算简单移动平均线"""
    return data['close'].rolling(window=period).mean()
```
```

### 输出1（代码文件）

`code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py`

```python
import pandas as pd
from typing import Dict, List, Optional

def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    calculate_sma函数
    
    **设计原理**：
    - **核心功能**：计算简单移动平均线
    - **设计思路**：通过滚动窗口计算平均值
    - **性能考虑**：使用pandas向量化计算提高效率
    
    **为什么这样设计**：
    1. **平滑价格波动**：移动平均能平滑价格波动，识别趋势
    2. **参数可配置**：周期参数可配置，适应不同需求
    3. **高效计算**：使用pandas的rolling方法，性能好
    
    **使用场景**：
    - 趋势识别：通过移动平均线判断趋势方向
    - 支撑阻力：移动平均线可作为动态支撑阻力位
    
    Args:
        data: 价格数据
        period: 周期
    
    Returns:
        SMA序列
    """
    return data['close'].rolling(window=period).mean()
```

### 输出2（更新后的Markdown）

```markdown
### 简单移动平均线

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def calculate_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
    """计算简单移动平均线"""
    return data['close'].rolling(window=period).mean()
```
-->
```

## ⚙️ 配置选项

### extract_code_to_files.py

- `markdown_file`: Markdown文件路径（必需）
- `--output-dir`: 代码输出目录（默认：code_library）
- `--dry-run`: 预览模式，不实际修改文件

### batch_extract_code.py

- `--dry-run`: 预览模式
- `--chapter`: 章节过滤（如 `003` 只处理第3章）

## 🔍 注意事项

1. **备份文件**：脚本会自动创建 `.backup` 备份文件
2. **路径识别**：脚本从文件路径自动识别章节信息
3. **代码增强**：自动添加导入和设计原理，但可能需要手动调整
4. **重复运行**：可以安全地重复运行，已存在的代码文件会被覆盖

## 🐛 故障排查

### 问题1：找不到代码块

**原因**：代码块格式不正确或不是Python代码

**解决**：检查Markdown文件中的代码块格式：
```markdown
```python
# 代码
```
```

### 问题2：路径错误

**原因**：无法从文件路径提取章节信息

**解决**：确保文件路径包含章节信息（如 `3.1_Trend_Analysis_CN.md`）

### 问题3：导入缺失

**原因**：代码中使用了未导入的模块

**解决**：脚本会自动添加常见导入，但特殊导入需要手动添加

## 📊 处理流程

```
1. 读取Markdown文件
   ↓
2. 提取所有Python代码块
   ↓
3. 为每个代码块生成文件路径
   ↓
4. 增强代码（添加导入和设计原理）
   ↓
5. 保存代码文件到code_library
   ↓
6. 更新Markdown文件（替换为CodeFromFile标签）
   ↓
7. 创建备份文件
   ↓
8. 完成 ✅
```

## 🎯 最佳实践

1. **先预览**：使用 `--dry-run` 先预览结果
2. **分批处理**：使用 `--chapter` 参数分批处理
3. **检查结果**：处理完成后检查代码文件和Markdown文件
4. **手动调整**：根据需要手动调整设计原理说明
5. **测试更新**：修改代码文件，验证自动更新功能

---

**更新时间**: 2025-12-13  
**版本**: v1.0.0

