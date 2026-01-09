# Investment Advisor V4.0 端到端测试指南

## 概述

本文档描述了Investment Advisor V4.0系统的端到端测试流程，包括从数据准备到最终推荐报告的完整验证。

## 测试脚本

**主脚本**: `scripts/test_advisor_v4_e2e.py`

## 测试模式

### 快速测试模式（默认）

适用于快速验证系统功能，约15-20分钟：

```bash
python scripts/test_advisor_v4_e2e.py
```

**特点**:
- 数据量：100个案例
- 因子优化：1次迭代，仅权重优化
- 回测：Fast层
- 推荐：Top 3

### 完整测试模式

适用于完整验证，约2-3小时：

```bash
python scripts/test_advisor_v4_e2e.py --full
```

**特点**:
- 数据量：全部案例
- 因子优化：完整递归优化
- 回测：Fast + Standard层
- 推荐：Top 5

## 命令行参数

```bash
python scripts/test_advisor_v4_e2e.py [选项]

选项:
  --full                完整测试模式（默认：快速模式）
  --skip-training       跳过模型训练
  --skip-optimization   跳过因子优化
  --skip-backtest       跳过回测验证
  --skip-recommendation 跳过推荐生成
```

## 测试阶段

### 阶段1: 环境检查

**检查项**:
- ✅ JQData连接和权限
- ✅ GPU可用性（CUDA、PyTorch）
- ⚠️  MongoDB连接（可选）
- ✅ 必需数据文件是否存在
- ✅ Python环境和依赖包

**输出**: 环境检查报告

### 阶段2: 数据验证和清洗

**功能**: 验证和清洗高收益案例数据

**模块**: `core/advisor_v4/data_validator.py`

**检查项**:
- 数据完整性（必需列是否存在）
- 数据合理性（收益率、市值、PE/PB范围）
- 异常值检测（IQR方法）
- 数据保留率（应>90%）

**输出**:
- 清洗后的数据文件: `output/advisor_v4/data/high_return_cases_cleaned.csv`
- 验证报告: `output/advisor_v4/data/high_return_cases_cleaned_validation_report.txt`

### 阶段3: 模型训练（GPU加速）

**功能**: 使用GPU批量加速提取因子并训练模型

**模块**:
- `core/advisor_v4/predictor_factor_extractor_parallel.py`
- `core/advisor_v4/gpu_accelerator.py`
- `core/advisor_v4/advisor_v4_workflow.py`

**流程**:
1. 并行提取价格数据（3线程）
2. GPU批量计算技术指标（批处理大小50）
3. 合并因子数据
4. 构建训练数据集（正负样本）
5. 特征工程流水线
6. Walk-Forward交叉验证
7. XGBoost模型训练（正则化+早停）
8. 过拟合检测

**性能指标**:
- 因子提取速度：> 300个/秒（GPU批量）
- 训练时间：< 5分钟（1024案例）
- 模型AUC：> 0.55（验证集）

**输出**:
- 预测因子文件: `output/advisor_v4/data/predictive_features.csv`
- 训练数据: `output/advisor_v4/data/training_data.csv`
- 模型文件: `output/advisor_v4/models/xgboost_model.json`
- 特征流水线: `output/advisor_v4/models/feature_pipeline.pkl`

### 阶段4: 因子优化（递归优化）

**功能**: 递归优化因子选择和权重

**模块**: `core/advisor_v4/factor_optimizer.py`

**流程**:
1. 初始化优化配置（Walk-Forward验证，多目标优化）
2. 因子选择优化（从已验证因子池中选择最优组合）
3. 因子权重优化（网格搜索最优权重）
4. 融合权重优化（已验证因子 vs 聚宽因子的权重）
5. 生成优化报告

**性能指标**:
- 优化后Sharpe Ratio提升：> 10%
- 优化后命中率提升：> 5%
- 过拟合检测：无严重过拟合

**输出**:
- 优化结果: `output/advisor_v4/optimization/factor_optimization_result.json`
- 优化报告HTML: `output/advisor_v4/reports/factor_optimization_report.html`

### 阶段5: 回测验证

**功能**: 使用训练好的模型进行历史回测

**模块**: `core/advisor_v4/advisor_v4_workflow.py`

**回测层级**:
1. Fast层（<5秒）：向量化快速验证
2. Standard层（<30秒）：事件驱动标准回测
3. Precise层（可选）：BulletTrade精确回测

**指标**:
- 总收益率
- 夏普比率
- 最大回撤
- 10%+命中率
- 胜率

**输出**:
- 回测结果: `output/advisor_v4/backtest/backtest_result.json`
- 回测报告: `output/advisor_v4/reports/backtest_report.html`

### 阶段6: 推荐生成

**功能**: 生成本周投资推荐

**模块**: `core/advisor_v4/advisor_v4_workflow.py`

**流程**:
1. 加载训练好的模型
2. 获取当前周锚点日期
3. 计算全市场股票因子
4. 模型预测
5. 规则引擎过滤
6. 生成推荐列表（Top 5）

**输出**:
- 推荐信号: List[TradeSignal]
- 推荐数据: `output/advisor_v4/recommendations/recommendations_YYYYMMDD.json`

### 阶段7: 报告生成

**功能**: 生成多Tab HTML报告

**模块**: `core/advisor_v4/weekly_report_generator.py`

**报告内容**:
- 首页Tab：本周推荐和交易策略
- 模型性能Tab：训练指标、过拟合检测
- 因子分析Tab：因子重要性、优化结果
- 回测结果Tab：历史回测表现
- 推荐详情Tab：每只股票的详细分析

**输出**:
- HTML报告: `output/advisor_v4/reports/weekly_layout_report_YYYYMMDD.html`

### 阶段8: 结果汇总

**功能**: 汇总所有阶段的测试结果

**输出**:
- 测试总结报告: `output/advisor_v4/reports/e2e_test_summary_YYYYMMDD_HHMMSS.json`
- 测试日志: `output/advisor_v4/reports/e2e_test.log`

## 验收标准

1. **数据验证**: 数据保留率 > 90%，无严重错误
2. **模型训练**: 验证集AUC > 0.55，无严重过拟合
3. **因子优化**: 优化后性能提升 > 5%（如果执行）
4. **回测验证**: 总收益率 > 0，10%+命中率 > 10%（如果执行）
5. **推荐生成**: 成功生成Top N推荐（如果执行）
6. **报告生成**: HTML报告完整且可访问

## 常见问题

### 1. JQData连接失败

**症状**: 环境检查阶段JQData连接失败

**解决方案**:
- 检查 `config/jqdata_config.json` 配置
- 确认用户名和密码正确
- 检查网络连接
- 确认JQData账户权限

### 2. GPU不可用

**症状**: GPU检查失败，将使用CPU

**解决方案**:
- GPU不可用不影响功能，但会降低速度
- 如需使用GPU，检查CUDA安装和PyTorch版本
- 确认NVIDIA驱动正确安装

### 3. 数据文件不存在

**症状**: 高收益案例数据文件不存在

**解决方案**:
- 检查 `output/advisor_v4/data/high_return_cases_full_train.csv`
- 或检查 `results/high_return_cases_full_train.csv`
- 如需生成数据，先运行数据提取脚本

### 4. 模型训练失败

**症状**: 模型训练阶段报错

**可能原因**:
- 预测因子文件不存在（快速模式）
- 数据量不足
- 特征列不匹配

**解决方案**:
- 确保执行因子提取（不要跳过）
- 检查训练数据量是否足够（>50条）
- 检查特征列是否一致

### 5. 特征数量不匹配

**症状**: `X has N features, but StandardScaler is expecting M features`

**原因**: 训练和推荐时使用的特征列不一致

**解决方案**:
- 确保特征流水线正确保存和加载
- 检查 `FEATURE_COLUMNS` 定义是否一致
- 确保推荐时使用的因子计算器与训练时一致

### 6. 过拟合警告

**症状**: 训练完成后显示过拟合警告

**说明**:
- 轻微的过拟合警告是正常的
- 如果严重过拟合（AUC差距>0.2），建议：
  - 增加正则化强度
  - 减少模型复杂度
  - 增加训练数据量
  - 使用类别权重平衡

## 性能优化建议

### 1. 使用GPU加速

确保GPU可用，可以显著加速：
- 因子提取：6-10倍加速
- 技术指标计算：批量GPU处理

### 2. 并行处理

- 价格数据提取：3线程并行
- GPU批量计算：批处理大小50

### 3. 缓存机制

- 因子计算结果缓存
- 回测结果缓存（MongoDB）

## 输出文件说明

### 数据文件

- `high_return_cases_cleaned.csv`: 清洗后的高收益案例
- `predictive_features.csv`: 提取的预测因子
- `training_data.csv`: 训练数据集（正负样本）

### 模型文件

- `xgb_high_return_v4.pkl`: XGBoost模型
- `feature_pipeline.pkl`: 特征工程流水线

### 报告文件

- `factor_optimization_report.html`: 因子优化报告
- `backtest_report.html`: 回测报告
- `weekly_layout_report_YYYYMMDD.html`: 周度布局报告
- `e2e_test_summary_YYYYMMDD_HHMMSS.json`: 测试汇总报告

## 后续步骤

1. **查看测试报告**: 打开 `e2e_test_summary_*.json` 查看详细结果
2. **检查日志**: 查看 `e2e_test.log` 了解详细信息
3. **查看HTML报告**: 打开生成的HTML报告查看可视化结果
4. **分析问题**: 根据测试结果分析并改进系统

## 相关文档

- [因子架构文档](FACTOR_ARCHITECTURE.md)
- [因子选择理论](FACTOR_SELECTION_THEORY.md)
- [GPU加速指南](GPU_ACCELERATION_GUIDE.md)
- [数据验证指南](DATA_VALIDATION_AND_OPTIMIZATION.md)
