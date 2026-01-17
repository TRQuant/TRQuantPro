# 集成模型验证执行指南

**执行时间**: 2026-01-12  
**状态**: 进行中

---

## 📋 执行步骤概览

### ✅ 步骤1: 启动模型验证（已完成）

**状态**: ✅ 已启动（PID: 372861）

**命令**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
nohup /home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python scripts/validate_individual_models.py > logs/validation/validate_individual_models.log 2>&1 &
```

**预计耗时**: 2-4小时

**输出位置**:
- 日志文件: `logs/validation/validate_individual_models.log`
- 验证报告: `output/model_validation/individual_models_validation_*.md`

---

### ⏳ 步骤2: 监控验证进度（进行中）

**监控命令**:
```bash
# 方式1: 使用监控脚本
bash scripts/monitor_validation_progress.sh

# 方式2: 实时查看日志
tail -f logs/validation/validate_individual_models.log

# 方式3: 检查进程状态
ps aux | grep validate_individual_models.py
```

**检查点**:
- ✅ 进程是否运行
- ✅ 日志是否有错误
- ✅ 报告文件是否生成

---

### ⏳ 步骤3: 更新模型权重（等待验证完成）

**执行时机**: 验证报告生成后

**命令**:
```bash
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python scripts/update_ensemble_weights.py
```

**功能**:
- 自动从验证报告中提取各模型准确率
- 更新`core/ensemble_market_trend.py`中的`model_accuracies`
- 自动重新计算权重

**预期输出**:
```
📄 使用最新报告: individual_models_validation_20260112_*.md
📊 提取的准确率:
   HMM: 58.3%
   Technical: 65.0%
   Breadth: 60.0%
   Sentiment: 55.0%
✅ 更新 HMM 准确率: 58.3%
✅ 更新 Technical 准确率: 65.0%
✅ 更新 Breadth 准确率: 60.0%
✅ 更新 Sentiment 准确率: 55.0%
✅ 已更新 core/ensemble_market_trend.py
✅ 权重更新完成！
```

---

### ⏳ 步骤4: 回测验证集成模型（等待权重更新后）

**执行时机**: 权重更新完成后

**命令**:
```bash
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python scripts/backtest_ensemble_model.py
```

**预计耗时**: 30-60分钟

**输出位置**:
- 回测报告: `output/ensemble_backtest/ensemble_backtest_*.md`

**预期输出**:
- 集成模型的综合准确率
- 分市场状态的准确率（牛市/熊市/震荡市）
- 与各独立模型的对比

---

## 📊 验证标准

### 各模型准确率要求

| 模型 | 最低要求 | 目标 | 当前状态 |
|------|---------|------|---------|
| HMM | >=55% | >=60% | 58.3% ✅ |
| Technical | >=55% | >=65% | 待验证 |
| Breadth | >=55% | >=60% | 待验证 |
| Sentiment | >=55% | >=60% | 待验证 |

### 集成模型准确率要求

| 指标 | 最低要求 | 目标 | 用途 |
|------|---------|------|------|
| 综合准确率 | >=55% | >=65% | 模拟交易/实盘 |
| 牛市准确率 | >=60% | >=70% | 牛市策略切换 |
| 熊市准确率 | >=50% | >=60% | 熊市风险控制 |
| 震荡市准确率 | >=50% | >=60% | 震荡市策略调整 |

---

## 🔍 故障排查

### 问题1: 验证进程停止

**检查**:
```bash
# 检查进程
ps aux | grep validate_individual_models.py

# 检查日志错误
tail -50 logs/validation/validate_individual_models.log | grep -i error
```

**解决**:
- 如果是JQData连接问题，检查网络和认证
- 如果是内存不足，减少验证期间数量
- 重新启动验证进程

### 问题2: 报告文件未生成

**检查**:
```bash
ls -la output/model_validation/
```

**解决**:
- 检查日志文件，查看是否有错误
- 确认输出目录权限
- 手动运行验证脚本查看详细错误

### 问题3: 权重更新失败

**检查**:
```bash
# 手动查看报告文件
cat output/model_validation/individual_models_validation_*.md | grep -i "准确率"
```

**解决**:
- 手动从报告中提取准确率
- 手动更新`core/ensemble_market_trend.py`中的`model_accuracies`

---

## 📝 执行记录

### 2026-01-12 14:XX

- ✅ 启动模型验证进程（PID: 372861）
- ⏳ 等待验证完成（预计2-4小时）

### 下一步

- [ ] 监控验证进度
- [ ] 验证完成后更新权重
- [ ] 运行回测验证
- [ ] 生成最终报告

---

## 🔗 相关文档

- [集成模型开发文档](ENSEMBLE_MODEL_DEVELOPMENT.md)
- [下一步建议](NEXT_STEPS_RECOMMENDATION.md)
- [情绪模型优化](SENTIMENT_MODEL_OPTIMIZATION.md)

---

**最后更新**: 2026-01-12  
**维护**: TRQuant Team
