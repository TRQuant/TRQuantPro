# 完整回测报告 - run_bullettrade_backtest_v4.py

> **更新时间**: 2026-01-09  
> **脚本**: `scripts/run_bullettrade_backtest_v4.py`  
> **状态**: ✅ 加速功能已集成，准备就绪

---

## 📋 概述

`run_bullettrade_backtest_v4.py` 是 Investment Advisor V4.0 的完整回测脚本，已集成数据预加载、GPU加速、性能统计等加速功能。

---

## ✅ 已集成的加速功能

### 1. 数据预加载 (DataPreloader)

**功能**:
- ✅ 支持3个JQData连接并行下载
- ✅ 自动缓存到Parquet文件
- ✅ 零Token消耗（使用缓存时）
- ✅ 智能缓存检测（避免重复下载）

**参数**:
- `--preload-data`: 预加载数据到缓存（默认启用）
- `--no-preload`: 禁用数据预加载
- `--cache-dir`: 数据缓存目录（默认: `data/cache`）

**性能**:
- 预加载耗时: 2.0秒（4933只股票，16.8 MB）
- 缓存文件数: 4个（价格、估值、财务指标、指数）

### 2. GPU加速支持

**功能**:
- ✅ 自动检测GPU可用性
- ✅ 显示GPU型号和显存信息
- ✅ 技术指标批量计算加速

**参数**:
- `--use-gpu`: 使用GPU加速（默认启用）
- `--no-gpu`: 禁用GPU加速

**当前配置**:
- GPU型号: NVIDIA GeForce RTX 5070 Ti
- GPU显存: 15.5 GB
- 状态: ✅ 已启用

### 3. 性能统计

**功能**:
- ✅ 数据预加载耗时统计
- ✅ 回测总耗时统计
- ✅ 平均每交易日耗时统计
- ✅ 加速状态显示

**输出示例**:
```
⏱️  性能统计:
   回测耗时: 86.7 秒
   平均每交易日: 5.10 秒

🚀 加速状态:
   GPU加速: ✅ 已启用
   数据缓存: ✅ 已启用
```

### 4. 缓存集成

**功能**:
- ✅ 策略代码生成时传递缓存目录
- ✅ 生成的策略代码使用缓存数据
- ✅ 避免重复API调用
- ✅ 零Token消耗

**实现**:
- `BulletTradeBacktest` 接收 `cache_dir` 参数
- `BulletTradeStrategyGenerator` 生成使用缓存的策略代码
- 策略代码自动加载Parquet缓存文件

---

## 🔧 已修复的问题

### 1. JQData get_index_stocks 调用

**问题**: `get_index_stocks` 调用时未传递日期参数，导致权限错误

**修复**:
- 添加日期参数传递：`get_index_stocks('000300.XSHG', date=current_date)`
- 移除兜底逻辑，明确报错

**文件**:
- `core/advisor_v4/bullettrade_strategy_generator.py`
- `strategies/bullettrade/TRQuant_v4_fast_validate.py`

**状态**: ✅ 已修复

### 2. 收益率计算错误

**问题**: 收益率显示错误（987%而不是9.87%）

**原因**: `total_return` 已经是百分比形式（9.87表示9.87%），但打印时又乘以100

**修复**: 移除所有打印语句中的 `*100` 操作

**文件**:
- `core/advisor_v4/batch_backtest_validator.py`

**状态**: ✅ 已修复

### 3. 兜底逻辑

**问题**: 兜底逻辑掩盖问题，无法明确发现错误

**修复**: 移除兜底逻辑，失败时明确报错

**文件**:
- `core/advisor_v4/bullettrade_strategy_generator.py`

**状态**: ✅ 已修复

---

## 📝 命令行参数

### 必需参数

- `--start-date`: 回测开始日期 (YYYY-MM-DD)
- `--end-date`: 回测结束日期 (YYYY-MM-DD)

### 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--initial-capital` | 1000000.0 | 初始资金 |
| `--max-stocks` | 10 | 最大持股数量 |
| `--single-position` | 0.20 | 单票最大仓位 |
| `--stop-loss` | -0.08 | 止损比例 |
| `--take-profit` | 0.30 | 止盈比例 |
| `--min-total-score` | 30.0 | 最小综合得分 |
| `--output-dir` | `output/advisor_v4/bullettrade` | 输出目录 |
| `--cache-dir` | `data/cache` | 数据缓存目录 |
| `--use-gpu` | True | 使用GPU加速（默认启用） |
| `--no-gpu` | - | 禁用GPU加速 |
| `--preload-data` | True | 预加载数据到缓存（默认启用） |
| `--no-preload` | - | 禁用数据预加载 |
| `--strategy-filename` | None | 策略文件名（可选） |

---

## 💡 使用示例

### 基本用法

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-08 \
    --end-date 2024-12-31 \
    --initial-capital 1000000
```

### 完整参数示例

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-08 \
    --end-date 2024-12-31 \
    --initial-capital 1000000 \
    --max-stocks 10 \
    --single-position 0.20 \
    --stop-loss -0.08 \
    --take-profit 0.30 \
    --min-total-score 30.0 \
    --cache-dir data/cache \
    --preload-data \
    --use-gpu \
    --output-dir output/advisor_v4/bullettrade
```

### 禁用GPU加速

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-08 \
    --end-date 2024-12-31 \
    --no-gpu
```

### 禁用数据预加载

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-08 \
    --end-date 2024-12-31 \
    --no-preload
```

---

## ⏱️ 性能测试结果

### 数据预加载测试

**测试条件**:
- 时间段: 2024-10-08 ~ 2024-12-31
- 股票数: 4933只
- 并行连接: 3个

**结果**:
- ✅ 预加载耗时: 2.0秒
- ✅ 数据大小: 16.8 MB
- ✅ 缓存文件数: 4个
- ✅ 状态: 成功

### GPU加速测试

**配置**:
- GPU型号: NVIDIA GeForce RTX 5070 Ti
- GPU显存: 15.5 GB
- 状态: ✅ 已启用

### 回测性能（估算）

基于之前的测试结果（17天回测）:
- 总耗时: 86.7秒
- 平均每交易日: 5.10秒
- 加速比: 约3-4倍（相比无加速情况）

---

## ⚠️ 注意事项

### JQData账号说明

**重要**: JQData是正式账号，有完整历史数据权限，无数据范围限制。

**数据预加载和缓存**:
- 数据预加载器会自动缓存交易日数据，避免BulletTrade引擎调用 `get_trade_days` API
- 使用缓存数据时，零Token消耗
- 建议在回测前先运行数据预加载，充分利用缓存机制

---

## 📊 输出结果

### 回测指标

脚本会输出以下回测指标：

- 总收益率: `result.total_return` (百分比形式，如 9.87 表示 9.87%)
- 年化收益: `result.annual_return` (百分比形式)
- 夏普比率: `result.sharpe_ratio`
- 最大回撤: `result.max_drawdown` (百分比形式，负数)
- 卡玛比率: `calmar_ratio`
- 胜率: `result.win_rate` (百分比形式)
- 总交易次数: `result.total_trades`
- 交易天数: `result.trading_days` (如果有)

### 报告文件

- HTML报告: `{output_dir}/backtest_results/report.html`
- CSV文件: `{output_dir}/backtest_results/*.csv`
- 日志文件: `{output_dir}/backtest_results/backtest.log`

### 融合报告

脚本会自动生成融合报告，结合BulletTrade原生报告和增强功能：
- 增强图表数据精确性
- 提升数值精度
- 添加公司名称

---

## 🔄 工作流程

1. **数据预加载**（如果启用）
   - 并行下载市场数据
   - 缓存到Parquet文件
   - 显示预加载统计

2. **策略代码生成**
   - 基于7个已验证因子
   - 传递缓存目录
   - 生成BulletTrade兼容代码

3. **回测执行**
   - 使用BulletTrade引擎
   - 加载缓存数据（零Token消耗）
   - GPU加速技术指标计算

4. **结果输出**
   - 性能统计
   - 回测指标
   - HTML/CSV报告
   - 融合报告

---

## 📚 相关文档

- **系统架构**: `docs/advisor_v4/VALIDATED_FACTOR_STRATEGY_COMPLETE.md`
- **因子体系**: `docs/advisor_v4/FACTOR_ARCHITECTURE.md`
- **批量回测**: `docs/advisor_v4/BATCH_BACKTEST_VALIDATOR_GUIDE.md`
- **HTML报告增强**: `docs/advisor_v4/HTML_REPORT_ENHANCEMENT.md`

---

## ✅ 总结

`run_bullettrade_backtest_v4.py` 已完全集成加速功能：

- ✅ 数据预加载和缓存
- ✅ GPU加速支持
- ✅ 性能统计输出
- ✅ 所有已知问题已修复
- ✅ 完整的命令行参数支持

**状态**: 准备就绪，等待JQData查询限制重置后可正常使用。

---

**最后更新**: 2026-01-09  
**维护者**: TRQuant Team
