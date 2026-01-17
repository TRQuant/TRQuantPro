# Advisor V4.0 数据验证与优化指南

> **版本**: v1.0  
> **日期**: 2026-01-08  
> **目的**: 确保训练数据质量，优化提取性能，防止过拟合

---

## 1. 数据验证和清洗

### 1.1 设计原则

1. **数据可靠性优先**: 确保训练数据质量，避免"垃圾进垃圾出"
2. **常识性检查**: 收益率、市值、估值等指标应在合理范围
3. **可追溯性**: 记录所有清洗操作，便于审计和调试

### 1.2 验证规则

#### 收益率范围检查
- **最小收益率**: 5.0%（低于此值不应作为高收益案例）
- **最大收益率**: 100.0%（超过此值需要特别验证）
- **异常处理**: 超出范围的数据将被移除

#### 市值范围检查
- **最小市值**: 1.0亿元（避免异常小市值）
- **最大市值**: 50000.0亿元（避免数据错误）
- **异常处理**: 超出范围的数据将被移除

#### PE/PB范围检查
- **PE范围**: -100.0 ~ 1000.0（允许亏损公司，但避免极端值）
- **PB范围**: 0.1 ~ 50.0（避免极端估值）
- **异常处理**: 超出范围的值将被标记为NaN

#### 缺失值检查
- **最大缺失比例**: 30%（超过此比例的列将被标记）
- **处理方式**: 使用中位数填充数值型缺失值

#### 重复数据检查
- **检查字段**: `code` + `date` 组合
- **处理方式**: 保留第一条，移除重复记录

#### 异常值检测（IQR方法）
- **方法**: 使用3倍IQR（四分位距）检测异常值
- **阈值**: 异常值比例<10%才标记（避免误删正常数据）

#### 格式检查
- **日期格式**: 必须可解析为日期
- **股票代码格式**: 必须符合 `XXXXXX.X(SHE|SHG)` 格式

### 1.3 使用示例

```python
from core.advisor_v4.data_validator import DataValidator, DataQualityConfig, validate_high_return_cases

# 方式1: 使用函数接口
result = validate_high_return_cases(
    cases_file='results/high_return_cases_full_train.csv',
    output_file='results/high_return_cases_cleaned.csv',
    config=DataQualityConfig()
)

# 方式2: 使用类接口
validator = DataValidator(config=DataQualityConfig(), verbose=True)
result = validator.validate_and_clean(df)

if result.is_valid:
    cleaned_df = result.cleaned_data
    print(f"数据保留率: {result.valid_records/result.total_records:.1%}")
else:
    print("数据验证未通过，请检查问题")
```

---

## 2. 并行提取与GPU加速

### 2.1 性能优化策略

1. **多进程并行**: 利用JQData的3个并发连接，分段并行提取
2. **批量处理**: 批量获取数据，减少API调用次数
3. **GPU加速**: 对技术指标计算（RSI、动量、移动平均等）使用GPU
4. **向量化计算**: 使用numpy/pandas向量化操作

### 2.2 性能提升

| 优化项 | 原始耗时 | 优化后耗时 | 提升倍数 |
|--------|---------|-----------|---------|
| **单线程提取** | ~30分钟 (1024案例) | - | - |
| **并行提取** | - | ~10分钟 | 3x |
| **GPU加速** | - | ~3-5分钟 | 2-3x |
| **总计提升** | 30分钟 | **3-5分钟** | **6-10x** |

### 2.3 使用示例

```python
from core.advisor_v4.predictor_factor_extractor_parallel import ParallelPredictorFactorExtractor

# 创建并行提取器
extractor = ParallelPredictorFactorExtractor(
    num_workers=3,    # JQData最多3个并发连接
    use_gpu=True,      # 启用GPU加速（如果可用）
    verbose=True
)

# 提取预测因子
predictive_df = extractor.extract_from_historical_cases(
    cases_file='results/high_return_cases_cleaned.csv',
    lookback_weeks=1,  # 周频：提前1周
    lookback_days=5,   # 兼容参数
    resume=True        # 支持断点续传
)
```

### 2.4 GPU加速要求

- **硬件**: NVIDIA GPU with CUDA support
- **软件**: PyTorch with CUDA
- **自动检测**: 如果GPU不可用，自动降级到CPU

---

## 3. 算法验证与过拟合检测

### 3.1 验证机制

#### Walk-Forward验证
- **方法**: 滚动窗口验证，模拟真实交易环境
- **训练窗口**: 3个月
- **测试窗口**: 1个月
- **步长**: 1个月

#### 过拟合检测指标
1. **AUC差距**: 训练AUC - 验证AUC > 0.1 视为过拟合
2. **精确率差距**: 训练精确率 - 验证精确率 > 0.15 视为过拟合
3. **特征重要性集中度**: Top3特征占比 > 70% 视为过度依赖
4. **验证集AUC过低**: 验证AUC < 0.5 视为模型无效

### 3.2 常识性检查

#### 因子合理性检查
- **动量因子**: 不应超过±50%（极端值需要验证）
- **相对位置**: 应在0-100%范围内
- **估值因子**: PE/PB应在合理范围（见数据验证规则）

#### 预测结果合理性检查
- **预测收益率**: 不应超过±30%（单周）
- **预测概率**: 应在0-1范围内
- **特征重要性**: 不应过度集中在单一因子

### 3.3 使用示例

```python
from core.advisor_v4.cross_validator import WalkForwardValidator, OverfittingDetector

# Walk-Forward验证
validator = WalkForwardValidator(
    train_months=3,
    test_months=1,
    step_months=1,
    verbose=True
)

cv_result = validator.validate(
    df=training_df,
    train_func=lambda df: train_model(df),
    eval_func=lambda model, df: evaluate_model(model, df)
)

# 过拟合检测
detector = OverfittingDetector(
    auc_gap_threshold=0.1,
    precision_gap_threshold=0.15
)

overfitting_report = detector.detect(
    train_metrics=train_metrics,
    val_metrics=val_metrics,
    feature_importance=feature_importance
)

if overfitting_report['is_overfitting']:
    print(f"⚠️ 检测到过拟合: {overfitting_report['warnings']}")
    print(f"建议: {overfitting_report['recommendation']}")
```

---

## 4. 完整训练流程

### 4.1 标准流程

```
1. 数据验证和清洗
   ├─ 检查数据完整性
   ├─ 常识性检查（收益率、市值、估值）
   ├─ 异常值检测
   └─ 生成清洗后数据

2. 并行提取预测因子（GPU加速）
   ├─ 使用清洗后的数据
   ├─ 并行提取（3个进程）
   ├─ GPU加速技术指标计算
   └─ 支持断点续传

3. 构建训练数据集
   ├─ 正样本：历史高收益案例
   ├─ 负样本：随机采样
   └─ 特征工程

4. 模型训练
   ├─ 特征选择
   ├─ 交叉验证（Walk-Forward）
   └─ 过拟合检测

5. 模型验证
   ├─ 算法合理性检查
   ├─ 常识性验证
   └─ 性能评估
```

### 4.2 训练脚本

```bash
# 使用优化后的训练脚本
python scripts/train_advisor_v4.py
```

脚本会自动：
1. ✅ 验证和清洗数据
2. ✅ 使用并行+GPU加速提取
3. ✅ 进行Walk-Forward验证
4. ✅ 检测过拟合
5. ✅ 生成验证报告

---

## 5. 最佳实践

### 5.1 数据质量

1. **定期验证**: 每次训练前必须验证数据质量
2. **保存清洗记录**: 记录所有清洗操作，便于追溯
3. **异常值审查**: 对标记的异常值进行人工审查

### 5.2 性能优化

1. **使用并行提取**: 始终使用`ParallelPredictorFactorExtractor`
2. **启用GPU加速**: 如果硬件支持，启用GPU加速
3. **断点续传**: 长时间提取任务使用断点续传

### 5.3 算法验证

1. **Walk-Forward验证**: 必须使用Walk-Forward验证，而非简单train/test split
2. **过拟合检测**: 训练后必须进行过拟合检测
3. **常识性检查**: 验证预测结果是否符合常识

---

## 6. 故障排查

### 6.1 数据验证失败

**问题**: 数据验证未通过

**解决方案**:
1. 检查验证报告，找出具体问题
2. 修复数据源问题
3. 调整验证配置（如果规则过于严格）

### 6.2 GPU加速未启用

**问题**: GPU加速未启用

**解决方案**:
1. 检查CUDA是否安装: `nvidia-smi`
2. 检查PyTorch CUDA支持: `torch.cuda.is_available()`
3. 如果GPU不可用，系统会自动降级到CPU

### 6.3 过拟合检测

**问题**: 检测到过拟合

**解决方案**:
1. 增加正则化强度
2. 减少模型复杂度
3. 增加训练数据
4. 使用特征选择减少特征数量

---

## 7. 相关文件

| 文件 | 说明 |
|------|------|
| `core/advisor_v4/data_validator.py` | 数据验证和清洗模块 |
| `core/advisor_v4/predictor_factor_extractor_parallel.py` | 并行+GPU加速提取器 |
| `core/advisor_v4/cross_validator.py` | 交叉验证和过拟合检测 |
| `scripts/train_advisor_v4.py` | 优化后的训练脚本 |

---

## 8. 参考资料

- [HIGH_RETURN_FACTOR_RESEARCH.md](../HIGH_RETURN_FACTOR_RESEARCH.md) - 高收益因子研究
- [V4_METHOD_VALIDATION_REPORT.md](../V4_METHOD_VALIDATION_REPORT.md) - V4.0方法验证报告
- [FACTOR_ARCHITECTURE.md](./FACTOR_ARCHITECTURE.md) - 因子架构设计
