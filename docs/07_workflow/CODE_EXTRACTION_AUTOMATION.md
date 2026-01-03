# 代码提取和迁移自动化方案

## 🎯 方案概述

实现了自动化代码提取和迁移系统，可以：
1. **自动提取**：从Markdown文件中提取Python代码块
2. **自动保存**：将代码保存为独立文件到 `code_library` 目录
3. **自动更新**：更新Markdown文件，将代码块替换为 `<CodeFromFile>` 标签
4. **自动增强**：添加必要的导入和设计原理说明
5. **自动同步**：代码文件修改后，网页自动更新（通过Vite插件）

## 📁 文件结构

```
TRQuant/
├── scripts/
│   ├── extract_code_to_files.py      # 单个文件处理脚本
│   ├── batch_extract_code.py          # 批量处理脚本
│   └── README_CODE_EXTRACTION.md      # 详细使用说明
├── code_library/                      # 代码库目录
│   └── 003_Chapter3_Market_Analysis/
│       ├── 3.1/
│       │   ├── code_3_1_1_calculate_sma.py
│       │   └── ...
│       └── 3.2/
│           └── ...
└── extension/AShare-manual/
    └── src/
        └── plugins/
            └── vite-code-library-watcher-working.mjs  # 自动更新插件
```

## 🚀 快速开始

### 1. 单个文件处理

```bash
# 预览模式（推荐先预览）
python scripts/extract_code_to_files.py \
  extension/AShare-manual/src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md \
  --dry-run

# 实际执行
python scripts/extract_code_to_files.py \
  extension/AShare-manual/src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md
```

### 2. 批量处理

```bash
# 批量处理所有文件（预览）
python scripts/batch_extract_code.py --dry-run

# 只处理第3章
python scripts/batch_extract_code.py --chapter 003

# 实际执行批量处理
python scripts/batch_extract_code.py
```

## 🔄 完整工作流程

### 步骤1：提取代码

```bash
# 处理单个文件
python scripts/extract_code_to_files.py <markdown_file>
```

**结果**：
- ✅ 代码文件保存到 `code_library/`
- ✅ Markdown文件更新，代码块替换为 `<CodeFromFile>` 标签
- ✅ 原文件备份为 `.backup`

### 步骤2：验证结果

1. 检查代码文件是否正确生成
2. 检查Markdown文件是否正确更新
3. 启动开发服务器验证显示

### 步骤3：自动更新验证

1. 修改代码文件
2. 保存文件
3. 观察网页是否自动更新

## 📋 功能特性

### 1. 智能提取

- ✅ 自动识别Python代码块
- ✅ 提取函数名/类名作为文件名
- ✅ 从文件路径提取章节信息
- ✅ 生成规范的代码文件路径

### 2. 代码增强

- ✅ 自动添加必要的导入（pandas, numpy, typing等）
- ✅ 检查并添加设计原理说明（如果缺失）
- ✅ 保持代码格式和注释

### 3. Markdown更新

- ✅ 将代码块替换为 `<CodeFromFile>` 标签
- ✅ 保留原始代码作为注释（备份）
- ✅ 自动生成正确的相对路径

### 4. 自动同步

- ✅ Vite插件监控代码库目录
- ✅ 文件修改后自动触发HMR更新
- ✅ 网页自动刷新，无需手动操作

## 🎯 使用场景

### 场景1：新章节代码迁移

```bash
# 处理新章节的Markdown文件
python scripts/extract_code_to_files.py \
  extension/AShare-manual/src/pages/ashare-book6/004_Chapter4/4.1_xxx_CN.md
```

### 场景2：批量迁移所有章节

```bash
# 批量处理所有章节
python scripts/batch_extract_code.py
```

### 场景3：只处理特定章节

```bash
# 只处理第3章
python scripts/batch_extract_code.py --chapter 003
```

## ⚙️ 配置说明

### 路径规则

代码文件路径生成规则：
```
code_library/{chapter_dir}/{section}/code_{chapter}_{section}_{name}.py
```

示例：
- 输入：`3.1_Trend_Analysis_CN.md` 中的 `calculate_sma` 函数
- 输出：`code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py`

### 文件命名规则

1. **有函数名/类名**：使用函数名/类名
   - `def calculate_sma()` → `code_3_1_1_calculate_sma.py`

2. **无函数名**：使用索引
   - 第1个代码块 → `code_3_1_00.py`
   - 第2个代码块 → `code_3_1_01.py`

## 🔍 示例

### 输入（Markdown）

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
    ...
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

## 🛠️ 高级用法

### 自定义输出目录

```bash
python scripts/extract_code_to_files.py <markdown_file> \
  --output-dir custom_code_library
```

### 预览模式

```bash
# 预览，不实际修改文件
python scripts/extract_code_to_files.py <markdown_file> --dry-run
```

## 📊 处理统计

脚本会输出处理统计信息：

```
📄 处理文件: extension/AShare-manual/src/pages/.../3.1_Trend_Analysis_CN.md
📊 找到 15 个代码块

📝 处理代码块 1/15
   函数/类名: calculate_sma
   输出路径: code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py
✅ 已保存代码文件: code_library/.../code_3_1_1_calculate_sma.py

...

📊 处理完成:
   提取代码块: 15/15
   更新Markdown: 15/15
```

## 🔄 自动更新机制

### 工作原理

1. **Vite插件监控**：`vite-code-library-watcher-working.mjs` 监控 `code_library` 目录
2. **文件变化检测**：使用 `server.watcher.add()` 直接监控
3. **精确匹配**：查找包含该代码文件的Markdown文件
4. **HMR触发**：触发Vite的HMR更新机制
5. **自动刷新**：网页自动更新，显示最新代码

### 验证方法

1. 修改代码文件
2. 保存文件（Ctrl+S）
3. 观察控制台日志
4. 检查网页是否自动更新

## ⚠️ 注意事项

1. **备份文件**：脚本会自动创建 `.backup` 备份，可以安全恢复
2. **重复运行**：可以安全地重复运行，已存在的代码文件会被覆盖
3. **路径识别**：确保Markdown文件路径包含章节信息
4. **代码格式**：确保代码块使用正确的格式（```python ... ```）
5. **手动调整**：设计原理说明可能需要手动调整和完善

## 🐛 故障排查

### 问题1：找不到代码块

**检查**：
- 代码块格式是否正确（```python ... ```）
- 代码块是否在Markdown文件中

### 问题2：路径错误

**检查**：
- 文件路径是否包含章节信息（如 `3.1_Trend_Analysis_CN.md`）
- 章节编号格式是否正确

### 问题3：导入缺失

**解决**：
- 脚本会自动添加常见导入
- 特殊导入需要手动添加到代码文件

## 📈 效率提升

### 手动方式 vs 自动化方式

| 操作 | 手动方式 | 自动化方式 |
|------|---------|-----------|
| 提取代码 | 复制粘贴 | 自动提取 |
| 保存文件 | 手动创建 | 自动保存 |
| 更新Markdown | 手动替换 | 自动替换 |
| 添加导入 | 手动添加 | 自动添加 |
| 处理时间 | ~10分钟/文件 | ~10秒/文件 |

**效率提升：60倍+**

## 🎉 总结

通过自动化脚本，代码迁移工作变得简单高效：

1. ✅ **一键处理**：单个命令完成所有操作
2. ✅ **批量处理**：可以批量处理所有文件
3. ✅ **自动增强**：自动添加导入和设计原理
4. ✅ **自动同步**：代码修改后网页自动更新
5. ✅ **安全可靠**：自动备份，可恢复

---

**更新时间**: 2025-12-13  
**版本**: v1.0.0  
**状态**: ✅ 完整实现

