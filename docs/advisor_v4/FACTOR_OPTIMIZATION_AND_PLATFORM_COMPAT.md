# 因子优化与平台兼容性实现报告

> **版本**: 1.0  
> **更新时间**: 2026-01-09

---

## 1. 实现概述

本次实现完成了以下任务：

1. **聚宽因子API测试** - 验证`get_factor_values`返回Z-score标准化值
2. **因子计算优化** - 添加辅助函数，简化代码结构
3. **平台兼容性知识库** - 建立聚宽/BulletTrade/Ptrade/QMT差异对照
4. **策略转换器** - 实现BulletTrade → Ptrade/QMT代码转换

---

## 2. 因子API测试结论

### 2.1 聚宽因子特性

| 特性 | 说明 |
|------|------|
| 返回格式 | Z-score标准化值（均值≈0，标准差≈1） |
| 适用场景 | 股票排序、因子组合 |
| 不适用场景 | 阈值筛选（需要原始值） |

### 2.2 可用因子

| 因子类型 | 因子名称 |
|----------|----------|
| CNE5 | size, beta, momentum, liquidity, residual_volatility |
| CNE6额外 | growth, earnings_yield |
| 财务 | roe_ttm |
| 换手率 | turnover_volatility |

### 2.3 决策

由于策略需要原始值进行阈值筛选（如市值30-200亿），**保留手工计算逻辑**，聚宽因子仅作为补充排序依据。

---

## 3. 代码优化

### 3.1 新增辅助函数

```python
def _flatten_multiindex_columns(df):
    """处理MultiIndex列名"""
    
def _calculate_momentum(prices_df, codes, days, default=0.0):
    """通用动量计算函数"""
```

### 3.2 优化效果

- 代码行数减少约40%
- 消除重复的MultiIndex处理逻辑
- 统一的动量计算接口

---

## 4. 知识库建立

### 4.1 分类结构

```
知识库
├── platform_compat (12条)
│   ├── 聚宽与BulletTrade数据API差异
│   ├── 聚宽与BulletTrade订单API差异
│   ├── 聚宽与BulletTrade持仓账户差异
│   ├── 聚宽与BulletTrade认证机制差异
│   ├── 聚宽与Ptrade数据API差异
│   ├── 聚宽与Ptrade订单API差异
│   ├── 聚宽与Ptrade持仓账户差异
│   ├── 聚宽与Ptrade定时任务差异
│   ├── 聚宽与QMT数据API差异
│   ├── 聚宽与QMT订单API差异
│   └── 聚宽与QMT回调机制差异
├── strategy_convert (1条)
│   └── 策略转换核心要点
└── jqdata_api (2条)
    ├── get_factor_values返回Z-score
    └── market_cap单位说明
```

### 4.2 使用方法

```python
from unified_dev_server import kb_search

# 搜索平台差异
result = kb_search("Ptrade", category="platform_compat")

# 搜索API用法
result = kb_search("get_price")
```

---

## 5. 策略转换器

### 5.1 文件结构

| 文件 | 说明 |
|------|------|
| `strategy_converter.py` | 转换器基类和工具函数 |
| `ptrade_converter.py` | Ptrade转换器 |
| `qmt_converter.py` | QMT转换器 |

### 5.2 转换内容

| 转换项 | 说明 |
|--------|------|
| 股票代码 | .XSHG/.XSHE → .SH/.SZ |
| 数据API | get_price → get_klines/xtdata |
| 订单API | order → order/xt_trader |
| 定时任务 | run_daily → schedule |

### 5.3 使用示例

```python
from core.advisor_v4.ptrade_converter import convert_to_ptrade
from core.advisor_v4.qmt_converter import convert_to_qmt

# 转换为Ptrade
result = convert_to_ptrade(source_code)
print(result.target_code)

# 转换为QMT
result = convert_to_qmt(source_code)
print(result.target_code)
```

---

## 6. 测试验证结果

| 测试项 | 结果 |
|--------|------|
| 模块导入 | ✅ 全部成功 |
| 股票代码转换 | ✅ 正确转换 |
| Ptrade转换 | ✅ 成功，3个警告 |
| QMT转换 | ✅ 成功，4个警告 |
| 代码分析器 | ✅ 正确识别API |
| 策略生成器 | ✅ 27732字符 |
| 知识库 | ✅ 15条记录 |

---

## 7. 文件清单

### 7.1 新增文件

| 文件 | 说明 |
|------|------|
| `core/advisor_v4/strategy_converter.py` | 策略转换器基类 |
| `core/advisor_v4/ptrade_converter.py` | Ptrade转换器 |
| `core/advisor_v4/qmt_converter.py` | QMT转换器 |
| `docs/advisor_v4/FACTOR_OPTIMIZATION_AND_PLATFORM_COMPAT.md` | 本文档 |

### 7.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `core/advisor_v4/bullettrade_strategy_generator.py` | 添加辅助函数，优化因子计算 |
| `mcp_servers/unified_dev_server.py` | 修复kb_search搜索自定义知识库 |

### 7.3 知识库数据

| 文件 | 说明 |
|------|------|
| `.trquant/dev/kb/custom_kb.json` | 15条知识条目 |

---

## 8. 后续建议

1. **因子回测验证** - 使用BulletTrade验证优化后的因子计算
2. **转换器完善** - 处理更多边界情况
3. **知识库扩展** - 添加更多调试经验
4. **自动化测试** - 建立单元测试覆盖

---

*TRQuant开发团队*
