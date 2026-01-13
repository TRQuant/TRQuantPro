# 追涨策略递归迭代优化实施总结

> **生成时间**: 2026-01-10  
> **状态**: 代码框架已完成，需要运行测试

---

## 已完成的工作

### Phase 1: 信号有效性分析

**脚本**: `scripts/analyze_chase_rise_signals.py`

**功能**:
- 训练集信号统计分析（频率、收益率、胜率）
- 信号评分与收益率的相关性分析

**使用方法**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/analyze_chase_rise_signals.py
```

**输出**:
- `output/chase_rise_analysis/signals_*.csv` - 信号数据
- `output/chase_rise_analysis/statistics_*.json` - 统计结果

---

### Phase 1.2: 信号参数敏感性测试

**脚本**: `scripts/test_signal_sensitivity.py`

**功能**:
- 测试关键参数的敏感性
- 找出最优参数范围

**使用方法**:
```bash
./venv/bin/python scripts/test_signal_sensitivity.py
```

**输出**:
- `output/chase_rise_analysis/sensitivity_results_*.csv` - 敏感性测试结果
- `output/chase_rise_analysis/sensitivity_analysis_*.json` - 敏感性分析结果

---

### Phase 2: 选股规则迭代优化

**脚本**: `scripts/iterate_chase_rise_strategy.py`

**功能**:
- 递归迭代优化框架
- 使用训练集/验证集进行参数网格搜索
- 防止过拟合

**使用方法**:
```bash
./venv/bin/python scripts/iterate_chase_rise_strategy.py
```

**输出**:
- `output/chase_rise_optimization/best_params_*.json` - 最优参数
- `output/chase_rise_optimization/optimization_history_*.csv` - 优化历史

---

### Phase 3: 最优策略确定

**脚本**: `scripts/evaluate_chase_rise_strategy.py`

**功能**:
- 使用最优参数在测试集上进行最终回测
- 对比训练集/验证集/测试集结果
- 过拟合分析

**使用方法**:
```bash
./venv/bin/python scripts/evaluate_chase_rise_strategy.py
```

**输出**:
- `output/chase_rise_evaluation/evaluation_results_*.json` - 评估结果
- `output/chase_rise_evaluation/evaluation_report_*.md` - 评估报告

---

### Phase 3.2: 策略文档化

**脚本**: `scripts/generate_chase_rise_strategy_doc.py`

**功能**:
- 生成策略详细文档
- 包含最优参数、信号规则、风控规则、回测结果分析

**使用方法**:
```bash
./venv/bin/python scripts/generate_chase_rise_strategy_doc.py
```

**输出**:
- `docs/research/CHASE_RISE_STRATEGY_OPTIMIZED.md` - 策略文档

---

### Phase 4: QMT代码转换

**核心模块**: `core/qmt/chase_rise_strategy_generator.py`

**脚本**: `scripts/generate_qmt_chase_rise_code.py`

**功能**:
- 从最优参数生成QMT回测代码
- 从最优参数生成QMT实盘代码（集成passorder）

**使用方法**:
```bash
./venv/bin/python scripts/generate_qmt_chase_rise_code.py
```

**输出**:
- `strategies/qmt/TRQuant_ChaseRise_V1_*.py` - QMT回测代码
- `strategies/qmt/TRQuant_ChaseRise_V1_Live_*.py` - QMT实盘代码
- `strategies/qmt/TRQuant_ChaseRise_V1_params_*.json` - 参数配置

---

## 执行顺序

1. **Phase 1.1**: 运行 `analyze_chase_rise_signals.py` 进行信号统计分析
2. **Phase 1.2**: 运行 `test_signal_sensitivity.py` 进行参数敏感性测试（可选）
3. **Phase 2**: 运行 `iterate_chase_rise_strategy.py` 进行参数优化
4. **Phase 3.1**: 运行 `evaluate_chase_rise_strategy.py` 进行测试集评估
5. **Phase 3.2**: 运行 `generate_chase_rise_strategy_doc.py` 生成策略文档
6. **Phase 4**: 运行 `generate_qmt_chase_rise_code.py` 生成QMT代码

---

## 注意事项

### 代码生成器问题

**问题**: `core/qmt/chase_rise_strategy_generator.py` 中的 `generate_backtest_code()` 方法生成的代码有结构问题：
- `rebalance` 函数在 `handlebar` 函数之后定义，但在 `handlebar` 中被调用
- 在Python中，函数定义必须在调用之前

**影响**: 生成的QMT代码可能无法直接运行，需要手动调整函数定义顺序

**建议修复**:
1. 将 `rebalance` 和 `check_stop_loss_take_profit` 函数移到 `handlebar` 函数之前
2. 或者在 `handlebar` 函数中内联调用逻辑

---

## 下一步操作

1. **运行Phase 1脚本**，验证信号统计分析是否正常工作
2. **修复代码生成器**，确保生成的QMT代码结构正确
3. **运行完整流程**，从Phase 1到Phase 4
4. **测试生成的QMT代码**，在QMT平台上验证

---

**文档版本**: V1.0  
**最后更新**: 2026-01-10  
**维护者**: TRQuant Team
