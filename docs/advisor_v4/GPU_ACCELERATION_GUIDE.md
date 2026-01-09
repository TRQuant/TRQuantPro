# GPU加速优化指南

> **版本**: v1.0  
> **日期**: 2026-01-08  
> **目的**: 充分利用GPU加速技术指标计算，提升因子提取性能

---

## 1. GPU环境检测

### 1.1 硬件要求

- **GPU**: NVIDIA GPU with CUDA support（如 NVIDIA GeForce RTX 5070 Ti）
- **CUDA**: CUDA 12.8+（推荐）
- **显存**: 至少 8GB（推荐16GB+）

### 1.2 软件要求

- **PyTorch**: 2.9.1+ with CUDA support
- **CUDA Toolkit**: 12.8+

### 1.3 检测GPU

```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
```

**当前系统**:
- ✅ PyTorch: 2.9.1+cu128
- ✅ CUDA: 12.8
- ✅ GPU: NVIDIA GeForce RTX 5070 Ti
- ✅ GPU Memory: 16GB

---

## 2. GPU加速架构

### 2.1 设计原则

1. **批量处理**: 将所有股票的价格数据合并成批次，一次性计算
2. **向量化计算**: 使用PyTorch的向量化操作
3. **内存优化**: 使用float32减少显存占用
4. **异步计算**: 使用CUDA流实现异步计算（未来优化）

### 2.2 三阶段流程

```
阶段1: 并行提取价格数据（网络IO，CPU多线程）
    ↓
阶段2: 批量GPU计算技术指标（GPU加速，批量处理）
    ↓
阶段3: 并行提取其他因子并合并（网络IO，CPU多线程）
```

### 2.3 性能提升

| 优化项 | 原始耗时 | 优化后耗时 | 提升倍数 |
|--------|---------|-----------|---------|
| **单线程逐个计算** | ~30分钟 (1024案例) | - | - |
| **并行提取** | - | ~10分钟 | 3x |
| **GPU批量计算** | - | ~3-5分钟 | 2-3x |
| **总计提升** | 30分钟 | **3-5分钟** | **6-10x** |

---

## 3. GPU批量计算模块

### 3.1 核心类: `GPUTechnicalIndicatorCalculator`

**位置**: `core/advisor_v4/gpu_accelerator.py`

**功能**:
- 批量计算技术指标（动量、RSI、相对位置、量比）
- 自动处理不同长度的数据（填充和掩码）
- 自动降级到CPU（如果GPU不可用）

**使用示例**:

```python
from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator

# 创建计算器
calculator = GPUTechnicalIndicatorCalculator(
    batch_size=50,  # 批处理大小（可根据显存调整）
    use_gpu=True    # 启用GPU
)

# 批量计算
prices_list = [df1, df2, df3, ...]  # 价格数据列表
results = calculator.calculate_batch(prices_list)

# 结果格式: [{'momentum_5d': 5.2, 'rsi': 65.3, ...}, ...]
```

### 3.2 批量计算的技术指标

1. **动量指标**:
   - `momentum_5d`: 5日动量
   - `momentum_10d`: 10日动量
   - `momentum_20d`: 20日动量

2. **相对位置**: `rel_strength`（基于20日最高最低价）

3. **RSI**: 14日RSI指标

4. **量比**: `volume_ratio`（5日均量/20日均量）

### 3.3 批量处理优化

#### 数据准备
- **统一长度**: 所有股票数据填充到统一长度（取最大值）
- **NaN掩码**: 使用掩码标识有效数据位置
- **批量转换**: 一次性将所有数据转换为GPU张量

#### GPU计算
- **向量化操作**: 所有指标使用PyTorch向量化计算
- **并行计算**: 多个股票同时计算
- **内存优化**: 使用float32减少显存占用

#### 结果后处理
- **自动转换**: GPU结果自动转回CPU numpy数组
- **NaN处理**: 自动过滤无效值
- **格式转换**: 转换为标准字典格式

---

## 4. 并行提取器优化

### 4.1 优化后的 `ParallelPredictorFactorExtractor`

**位置**: `core/advisor_v4/predictor_factor_extractor_parallel.py`

**优化点**:
1. 集成GPU批量计算器
2. 三阶段流程（价格提取 → GPU计算 → 因子合并）
3. 自动降级到单线程模式（如果GPU不可用）

**使用示例**:

```python
from core.advisor_v4.predictor_factor_extractor_parallel import ParallelPredictorFactorExtractor

# 创建提取器（自动启用GPU批量加速）
extractor = ParallelPredictorFactorExtractor(
    num_workers=3,      # JQData并发连接数
    use_gpu=True,       # 启用GPU加速
    batch_size=50,      # GPU批处理大小
    verbose=True
)

# 提取预测因子（自动使用GPU批量计算）
predictive_df = extractor.extract_from_historical_cases(
    cases_file='results/high_return_cases_cleaned.csv',
    lookback_weeks=1,
    resume=True
)
```

---

## 5. 性能优化技巧

### 5.1 批处理大小调整

**原则**: 根据显存大小调整批处理大小

```python
# 小显存（8GB）
batch_size = 30

# 中等显存（16GB）
batch_size = 50  # 默认值

# 大显存（24GB+）
batch_size = 100
```

**调整方法**:

```python
# 在创建提取器时指定
extractor = ParallelPredictorFactorExtractor(
    batch_size=100,  # 根据显存调整
    use_gpu=True
)
```

### 5.2 显存管理

**自动清理**: GPU计算后自动调用 `torch.cuda.empty_cache()`

**手动清理**（如需要）:

```python
import torch

# 清理GPU缓存
torch.cuda.empty_cache()

# 检查显存使用
print(f"显存使用: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
print(f"显存缓存: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
```

### 5.3 数据类型优化

**使用float32**: 减少显存占用，速度更快

```python
# 自动设置为float32（在gpu_accelerator.py中）
torch.set_default_dtype(torch.float32)
```

---

## 6. 故障排查

### 6.1 GPU不可用

**问题**: GPU加速未启用

**检查步骤**:
1. 检查CUDA是否安装: `nvidia-smi`
2. 检查PyTorch CUDA支持: `torch.cuda.is_available()`
3. 检查CUDA版本兼容性: `torch.version.cuda`

**解决方案**:
- 如果GPU不可用，系统会自动降级到CPU
- 确保PyTorch与CUDA版本匹配

### 6.2 显存溢出（OOM）

**问题**: GPU显存不足

**解决方案**:
1. 减小批处理大小: `batch_size=30`
2. 分批处理: 自动分批（已实现）
3. 清理显存: `torch.cuda.empty_cache()`

### 6.3 多进程CUDA问题

**问题**: 在子进程中无法使用CUDA

**解决方案**:
- 使用线程池而非进程池（已实现）
- GPU计算在主线程中进行
- 价格数据提取在子线程中进行（网络IO）

---

## 7. 性能测试

### 7.1 基准测试

```python
from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator
import pandas as pd
import numpy as np
import time

# 创建测试数据
test_data = [
    pd.DataFrame({
        'close': np.random.randn(60).cumsum() + 100,
        'high': np.random.randn(60).cumsum() + 102,
        'low': np.random.randn(60).cumsum() + 98,
        'volume': np.random.randint(1000000, 10000000, 60)
    })
    for _ in range(100)
]

# CPU测试
start = time.time()
calc_cpu = GPUTechnicalIndicatorCalculator(use_gpu=False)
results_cpu = calc_cpu.calculate_batch(test_data)
cpu_time = time.time() - start

# GPU测试
start = time.time()
calc_gpu = GPUTechnicalIndicatorCalculator(use_gpu=True)
results_gpu = calc_gpu.calculate_batch(test_data)
gpu_time = time.time() - start

print(f"CPU耗时: {cpu_time:.2f}秒")
print(f"GPU耗时: {gpu_time:.2f}秒")
print(f"加速比: {cpu_time/gpu_time:.1f}x")
```

### 7.2 实际场景测试

**测试条件**:
- 1024个历史案例
- 每个案例60天价格数据
- GPU: NVIDIA GeForce RTX 5070 Ti
- 批处理大小: 50

**预期结果**:
- CPU耗时: ~10分钟
- GPU耗时: ~3-5分钟
- 加速比: 2-3x

---

## 8. 最佳实践

### 8.1 使用建议

1. **优先使用GPU批量加速**: 始终使用`ParallelPredictorFactorExtractor`，它会自动选择最优方式
2. **调整批处理大小**: 根据显存大小调整`batch_size`参数
3. **监控显存使用**: 定期检查显存使用情况，避免OOM

### 8.2 代码示例

```python
from core.advisor_v4.predictor_factor_extractor_parallel import ParallelPredictorFactorExtractor

# 创建提取器（自动启用GPU批量加速）
extractor = ParallelPredictorFactorExtractor(
    num_workers=3,      # JQData并发连接数
    use_gpu=True,       # 启用GPU加速
    batch_size=50,      # GPU批处理大小（根据显存调整）
    verbose=True
)

# 提取预测因子
predictive_df = extractor.extract_from_historical_cases(
    cases_file='results/high_return_cases_cleaned.csv',
    lookback_weeks=1,
    resume=True  # 支持断点续传
)

print(f"✅ 提取完成: {len(predictive_df)} 条预测特征")
```

---

## 9. 未来优化方向

### 9.1 异步计算

- 使用CUDA流实现异步计算
- 重叠数据传输和计算

### 9.2 多GPU支持

- 支持多GPU并行计算
- 数据分片到不同GPU

### 9.3 混合精度计算

- 使用float16进一步减少显存占用
- 加速计算（如果GPU支持）

### 9.4 更多技术指标

- MACD、KDJ、BOLL等
- 批量计算更多指标

---

## 10. 相关文件

| 文件 | 说明 |
|------|------|
| `core/advisor_v4/gpu_accelerator.py` | GPU批量计算模块 |
| `core/advisor_v4/predictor_factor_extractor_parallel.py` | 并行提取器（集成GPU加速） |
| `scripts/train_advisor_v4.py` | 训练脚本（自动使用GPU加速） |

---

## 11. 参考资料

- [PyTorch CUDA Documentation](https://pytorch.org/docs/stable/cuda.html)
- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [GPU Acceleration for Financial Computing](https://developer.nvidia.com/financial-computing)
