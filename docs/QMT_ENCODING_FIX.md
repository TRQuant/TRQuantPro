# QMT编码问题修复指南

> **更新时间**: 2026-01-09  
> **问题**: QMT读取Python策略文件时出现UTF-8编码错误

---

## 🔍 问题分析

### 错误信息

```
SyntaxError:(unicode error) 'utf-8' codec can't decode byte 0xbf in position 160: invalid start byte
```

### 根本原因

1. **QMT在Windows上默认使用GBK编码**读取Python文件
2. **文件包含非ASCII字符**（如中文注释）
3. **编码不匹配**导致读取失败

---

## ✅ 解决方案

### 方案1: 使用纯ASCII版本（推荐）

**已修复**: `TRQuant_V4_QMT_Backtest_3Months.py` 现在是纯ASCII版本

**特点**:
- ✅ 所有注释都是英文
- ✅ 没有任何中文字符
- ✅ UTF-8编码，纯ASCII内容

**使用方法**:
1. 直接使用 `TRQuant_V4_QMT_Backtest_3Months.py`
2. 如果QMT仍然报错，尝试方案2

---

### 方案2: 转换为GBK编码

**脚本**: `scripts/convert_qmt_strategy_encoding.py`

**使用方法**:
```bash
python scripts/convert_qmt_strategy_encoding.py strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py
```

**输出**: `TRQuant_V4_QMT_Backtest_3Months_GBK.py` (GBK编码版本)

**特点**:
- ✅ GBK编码（Windows QMT兼容）
- ✅ 纯ASCII内容
- ✅ 可以直接在QMT中使用

---

### 方案3: 在QMT中设置编码

如果QMT支持设置文件编码：

1. 打开QMT策略编辑器
2. 设置文件编码为 **UTF-8**
3. 重新加载策略文件

---

## 📋 文件对比

| 文件 | 编码 | 内容 | 适用场景 |
|------|------|------|----------|
| `TRQuant_V4_QMT_Backtest_3Months.py` | UTF-8 | 纯ASCII | 通用（推荐） |
| `TRQuant_V4_QMT_Backtest_3Months_GBK.py` | GBK | 纯ASCII | Windows QMT |

---

## 🔧 验证方法

### 检查文件编码

```bash
# Linux/Mac
file strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py

# Python
python3 -c "
with open('strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py', 'rb') as f:
    data = f.read()
    try:
        text = data.decode('utf-8')
        is_ascii = all(ord(c) < 128 for c in text)
        print(f'UTF-8: ✅, Pure ASCII: {is_ascii}')
    except:
        print('UTF-8: ❌')
"
```

---

## ⚠️ 注意事项

### 1. 文件编码声明

文件头部应该包含：
```python
# -*- coding: ascii -*-
```

或者：
```python
# -*- coding: utf-8 -*-
```

### 2. 避免非ASCII字符

- ❌ 不要使用中文注释
- ❌ 不要使用中文变量名
- ❌ 不要使用中文字符串（除非必要）
- ✅ 使用英文注释
- ✅ 使用ASCII字符

### 3. 行尾符

- Windows使用 `\r\n` (CRLF)
- Linux/Mac使用 `\n` (LF)
- 建议统一使用 `\n` (LF)

---

## 🔗 相关文件

- `strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py` - UTF-8版本（纯ASCII）
- `strategies/qmt/TRQuant_V4_QMT_Backtest_3Months_GBK.py` - GBK版本（如果生成）
- `scripts/convert_qmt_strategy_encoding.py` - 编码转换脚本

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
