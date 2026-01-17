# QMT股票代码格式修复说明

> **修复时间**: 2026-01-09  
> **问题**: QMT回测时出现大量"无效股票代码"警告

---

## 🔍 问题分析

### 错误现象

```
[系统][WARNING][set_universe]无效股票代码:688599.XSHG 601088.XSHG 688396.XSHG ...
```

### 根本原因

**QMT使用的股票代码格式**:
- 上海股票: `600837.SH` ✅
- 深圳股票: `000001.SZ` ✅

**错误的转换逻辑**:
- 原代码将 `.SH` 转换为 `.XSHG` ❌
- 原代码将 `.SZ` 转换为 `.XSHE` ❌

**正确的转换逻辑**:
- JQData格式 (`.XSHG`) → QMT格式 (`.SH`) ✅
- JQData格式 (`.XSHE`) → QMT格式 (`.SZ`) ✅
- 纯数字格式 → 根据前缀判断并添加 `.SH` 或 `.SZ` ✅

---

## ✅ 修复方案

### 修复后的 `normalize_stock_code` 函数

```python
def normalize_stock_code(code):
    """
    Normalize stock code format for QMT
    QMT uses .SH (Shanghai) and .SZ (Shenzhen) format
    Convert various formats to QMT format: 000001.SH or 000001.SZ
    """
    if not code:
        return code
    
    # Remove any existing suffix
    code_clean = code.strip().upper()
    
    # Handle different input formats
    if code_clean.endswith('.XSHG'):
        # JQData format: convert to QMT format
        code_clean = code_clean.replace('.XSHG', '')
        return f"{code_clean}.SH"
    elif code_clean.endswith('.XSHE'):
        # JQData format: convert to QMT format
        code_clean = code_clean.replace('.XSHE', '')
        return f"{code_clean}.SZ"
    elif code_clean.endswith('.SH'):
        # Already in QMT format
        return code_clean
    elif code_clean.endswith('.SZ'):
        # Already in QMT format
        return code_clean
    elif '.' not in code_clean:
        # Pure number format: determine market by prefix
        if len(code_clean) == 6:
            # Shanghai stocks: 600xxx, 601xxx, 603xxx, 605xxx, 688xxx
            if code_clean.startswith(('600', '601', '603', '605', '688')):
                return f"{code_clean}.SH"
            # Shenzhen stocks: 000xxx, 001xxx, 002xxx, 003xxx, 300xxx
            elif code_clean.startswith(('000', '001', '002', '003', '300')):
                return f"{code_clean}.SZ"
            else:
                # Default to Shanghai if cannot determine
                return f"{code_clean}.SH"
        else:
            # Invalid format, return as is
            return code_clean
    else:
        # Unknown format, return as is
        return code_clean
```

---

## 📊 测试用例

| 输入格式 | 输出格式 | 说明 |
|---------|---------|------|
| `600837.SH` | `600837.SH` | 已经是QMT格式 |
| `000001.SZ` | `000001.SZ` | 已经是QMT格式 |
| `600837.XSHG` | `600837.SH` | JQData格式转QMT |
| `000001.XSHE` | `000001.SZ` | JQData格式转QMT |
| `600837` | `600837.SH` | 纯数字，上海 |
| `000001` | `000001.SZ` | 纯数字，深圳 |
| `688599` | `688599.SH` | 科创板，上海 |
| `300274` | `300274.SZ` | 创业板，深圳 |

---

## 🔧 修复的文件

1. **`core/advisor_v4/qmt_research_strategy_generator.py`**
   - 修复 `normalize_stock_code` 函数
   - 确保生成的策略代码使用正确的QMT格式

2. **`strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py`**
   - 修复 `normalize_stock_code` 函数
   - 直接修复已生成的策略文件

---

## 📝 QMT股票代码格式规则

### 上海市场 (`.SH`)
- 主板: `600xxx`, `601xxx`, `603xxx`, `605xxx`
- 科创板: `688xxx`

### 深圳市场 (`.SZ`)
- 主板: `000xxx`, `001xxx`, `002xxx`, `003xxx`
- 创业板: `300xxx`

### 格式要求
- **必须使用**: `代码.SH` 或 `代码.SZ` 格式
- **不能使用**: `.XSHG` 或 `.XSHE` 格式（这是JQData格式）

---

## ✅ 验证方法

1. **运行策略**: 在QMT研究环境中运行修复后的策略
2. **检查日志**: 确认不再出现"无效股票代码"警告
3. **验证数据**: 确认能够正常获取股票数据

---

## 🔗 相关文档

- `utils/a_share_tools.py` - A股代码解析器，包含 `to_qmt()` 方法
- `core/jqdata_to_qmt_converter.py` - JQData到QMT转换器
- `strategies/qmt/README_RESEARCH.md` - QMT研究环境使用说明

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
