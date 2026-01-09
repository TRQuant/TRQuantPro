---
name: "TRQuant编码规范"
description: "TRQuant项目的Python编码规范和最佳实践"
type: "always"
tags: ["coding", "python", "trquant"]
---

# TRQuant编码规范

## Python代码规范

### 命名规范
- **模块名**: `snake_case` (如 `market_trend_analyzer.py`)
- **类名**: `PascalCase` (如 `MarketTrendAnalyzer`)
- **函数名**: `snake_case` (如 `analyze_market_trend`)
- **变量名**: `snake_case` (如 `trend_score`)
- **常量**: `UPPER_CASE` (如 `MAX_POSITION_SIZE`)

### 导入规范
```python
# 标准库导入
import sys
from pathlib import Path
from datetime import datetime

# 第三方库导入
import pandas as pd
import numpy as np

# 本地模块导入
from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer
```

**原则**:
- 使用绝对导入: `from core.xxx import Xxx`
- Notebook中必须设置 `sys.path`
- 避免循环导入

### 文档规范
- 所有公共函数必须有docstring
- 使用Google风格docstring
- 包含参数说明、返回值说明、示例

```python
def analyze_market_trend(index_code: str, date: str) -> MarketTrendSignal:
    """
    分析市场趋势
    
    Args:
        index_code: 指数代码，如 "000300.XSHG"
        date: 分析日期，格式 "YYYY-MM-DD"
    
    Returns:
        MarketTrendSignal: 市场趋势信号对象
    
    Example:
        >>> analyzer = MarketTrendAnalyzer(config)
        >>> result = analyzer.analyze("000300.XSHG", "2025-01-05")
    """
    pass
```

## 代码质量

### 类型提示
- 所有函数参数和返回值必须有类型提示
- 使用 `typing` 模块的类型（如 `List`, `Dict`, `Optional`）

### 错误处理
- 使用具体的异常类型
- 提供有意义的错误消息
- 记录错误日志

```python
try:
    result = analyzer.analyze(...)
except ValueError as e:
    logger.error(f"分析失败: {e}")
    raise
```

## 测试规范
- 单元测试文件: `tests/test_xxx.py`
- 测试函数名: `test_xxx`
- 使用pytest框架
