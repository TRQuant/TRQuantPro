# 回测结果存储与缓存系统

> **创建时间**: 2026-01-03  
> **版本**: v1.0  
> **状态**: 已实施

## 概述

回测结果存储与缓存系统提供了系统级的回测结果管理和缓存功能，避免重复运行长时间回测，节省计算资源。

## 核心特性

1. **自动缓存**: 基于参数哈希的精确匹配缓存机制
2. **统一存储**: 使用MongoDB统一存储，与现有系统保持一致
3. **智能存储**: 小结果直接存储，大结果存储文件路径
4. **便捷查询**: 提供灵活的查询和管理接口

## 架构设计

### 存储方案

- **数据库**: MongoDB (`jqquant`)
- **集合**: `signal_backtest_results`
- **存储方式**: 
  - 小结果（<10MB）: 直接存储在MongoDB文档中
  - 大结果（>10MB）: 存储文件路径，实际数据存文件系统（`output/backtest_results/`）

### 缓存机制

- **缓存依据**: 基于回测参数（start_date, end_date, sample_interval, benchmark等）的MD5哈希值
- **精确匹配**: `backtest_type + config_hash` 完全匹配
- **自动检查**: 运行前自动检查缓存，存在则直接返回
- **自动保存**: 回测完成后自动保存结果

### 与现有系统的关系

本系统扩展了`MarketTrendStorage`类，与现有系统保持统一：

- **复用基础设施**: 使用相同的MongoDB配置（`jqquant`数据库，`mongodb://localhost:27017`）
- **遵循模式**: 参考`CacheManager`的缓存模式（参数查询、集合管理）
- **统一错误处理**: 使用相同的错误处理和连接管理方式

## API文档

### MarketTrendStorage类（扩展方法）

#### `save_backtest_result(result, config, backtest_type, use_cache=True)`

保存回测结果（增强版，支持缓存）。

**参数**:
- `result`: BacktestResult对象（需有to_dict方法）
- `config`: 配置字典（包含start_date, end_date, sample_interval等）
- `backtest_type`: 回测类型（如'signal_phase1', 'signal_phase2'）
- `use_cache`: 是否使用缓存（如果已存在相同配置的结果，则不重复保存）

**返回**: 结果ID（MongoDB _id的字符串形式），失败返回None

**示例**:
```python
from core.market_trend_storage import MarketTrendStorage

storage = MarketTrendStorage()
config = {
    'start_date': '2023-01-01',
    'end_date': '2024-08-16',
    'sample_interval': 5
}
result_id = storage.save_backtest_result(
    result=phase1_result,
    config=config,
    backtest_type='signal_phase1',
    use_cache=True
)
```

#### `find_cached_backtest(config, backtest_type)`

基于配置哈希查找缓存的结果。

**参数**:
- `config`: 配置字典
- `backtest_type`: 回测类型

**返回**: 缓存的文档（包含_id），未找到返回None

#### `load_backtest_result(result_id)`

加载完整的回测结果。

**参数**:
- `result_id`: 结果ID（MongoDB _id的字符串形式）

**返回**: EnhancedBacktestResult对象或字典，失败返回None

#### `query_backtest_results(**filters)`

灵活查询回测结果。

**参数**:
- `backtest_type`: 回测类型（可选）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `limit`: 返回结果数量限制（默认100）
- `sort_by`: 排序字段（默认'created_at'）
- `sort_order`: 排序顺序（DESCENDING或ASCENDING）

**返回**: 结果列表（只包含元数据和摘要，不包含完整结果数据）

#### `list_backtest_results(backtest_type, limit, sort_by)`

列出回测结果（便捷方法）。

**参数**:
- `backtest_type`: 回测类型（可选）
- `limit`: 返回结果数量（默认10）
- `sort_by`: 排序字段（默认'created_at'）

**返回**: 结果列表

#### `delete_backtest_result(result_id)`

删除回测结果。

**参数**:
- `result_id`: 结果ID

**返回**: 是否成功

### Notebook辅助工具（notebooks.lib.backtest_utils）

#### `list_backtest_results(backtest_type=None, limit=10, sort_by='created_at')`

列出回测结果。

**示例**:
```python
from notebooks.lib.backtest_utils import list_backtest_results

results = list_backtest_results(backtest_type='signal_phase1', limit=5)
for r in results:
    print(f"ID: {r['_id']}, 创建时间: {r['created_at']}")
```

#### `load_backtest_result(result_id)`

加载完整的回测结果。

**示例**:
```python
from notebooks.lib.backtest_utils import load_backtest_result

result = load_backtest_result('507f1f77bcf86cd799439011')
print(f"总信号数: {result.total_signals}")
```

#### `find_cached_result(config, backtest_type)`

查找缓存结果。

**示例**:
```python
from notebooks.lib.backtest_utils import find_cached_result

config = {
    'start_date': '2023-01-01',
    'end_date': '2024-08-16',
    'sample_interval': 5
}
cached = find_cached_result(config, 'signal_phase1')
if cached:
    result = load_backtest_result(cached['_id'])
```

#### `format_backtest_summary(result_dict)`

格式化回测结果摘要（用于显示）。

## 使用示例

### 基本使用（自动缓存）

```python
from core.signal_backtest import run_phase1_backtest

# 第一次运行：执行回测并保存结果
result1 = run_phase1_backtest(sample_interval=5, use_cache=True)

# 第二次运行相同配置：直接从缓存加载，节省时间
result2 = run_phase1_backtest(sample_interval=5, use_cache=True)
# 输出: ✅ 从缓存加载Phase 1回测结果: 507f1f77bcf86cd799439011
```

### 查询历史结果

```python
from notebooks.lib.backtest_utils import (
    list_backtest_results,
    load_backtest_result,
    format_backtest_summary
)

# 列出最近的Phase 1回测结果
results = list_backtest_results(backtest_type='signal_phase1', limit=5)

for r in results:
    print(format_backtest_summary(r))
    
# 加载指定结果
result_id = results[0]['_id']
result = load_backtest_result(result_id)
print(f"准确率: {result.accuracy_5d:.1f}%")
```

### 禁用缓存（强制重新运行）

```python
# 强制重新运行，不使用缓存
result = run_phase1_backtest(sample_interval=5, use_cache=False)
```

### 在Notebook中使用

在`01_市场趋势判断回测验证.ipynb`中，缓存机制已自动集成：

```python
# Cell 14: Phase 1回测
phase1_result = run_phase1_backtest(sample_interval=10, use_cache=True)

# Cell 17: Phase 2回测
phase2_result = run_phase2_backtest(sample_interval=10, use_cache=True)
```

系统会自动：
1. 检查是否存在相同配置的缓存结果
2. 如果存在，直接返回缓存结果
3. 如果不存在，执行回测并保存结果
4. 在结果对象上标记`_from_cache`属性

## 数据模型

### MongoDB文档结构

```python
{
    "_id": ObjectId("..."),
    "backtest_type": "signal_phase1",  # 回测类型
    "config_hash": "a1b2c3d4...",      # 配置哈希（MD5）
    "config": {                         # 完整配置对象
        "start_date": "2023-01-01",
        "end_date": "2024-08-16",
        "sample_interval": 5,
        "benchmark": "000001.XSHG",
        # ... 其他参数
    },
    "start_date": "2023-01-01",
    "end_date": "2024-08-16",
    "created_at": "2026-01-03T10:30:00",
    "duration_seconds": 120.5,
    "summary": {                        # 结果摘要（关键指标）
        "total_signals": 100,
        "accuracy_5d": 65.0,
        "accuracy_20d": 75.0,
        "accuracy_60d": 67.5,
        "duration_seconds": 120.5
    },
    "result_data": {                    # 完整结果数据（小结果）或None（大结果）
        # EnhancedBacktestResult.to_dict()的结果
    },
    "file_path": None,                  # 文件路径（大结果）或None（小结果）
    "file_size": 1024000,               # 文件大小（字节）
    "backtest_time": "2026-01-03 10:30:00"  # 回测时间（可选）
}
```

### 索引

- `config_hash`: 用于缓存查找
- `backtest_type + config_hash`: 复合索引，加速缓存查找
- `created_at`: 时间排序
- `start_date, end_date`: 日期范围查询
- `backtest_type`: 按类型查询

## 配置哈希计算

配置哈希基于关键参数计算，排除时间戳、随机种子等不相关参数：

**包含的参数**:
- `start_date`, `end_date`
- `sample_interval`
- `benchmark`
- `use_trend_analyzer`, `use_hmm`, `use_ibd` (算法开关)
- 其他影响结果的配置参数

**排除的参数**:
- 时间戳
- 随机种子（如果存在）
- 运行环境相关参数

## 存储策略

### 大小判断

- **阈值**: 10MB（MongoDB文档限制16MB，留出安全边际）
- **小结果（<10MB）**: 直接存储在MongoDB文档的`result_data`字段
- **大结果（>10MB）**: 保存为pickle文件（`output/backtest_results/{result_id}.pkl`），MongoDB中只存储文件路径

### 文件存储格式

- **主格式**: Pickle (`.pkl`) - 保持Python对象完整性
- **位置**: `output/backtest_results/`
- **命名**: `{result_id}.pkl`（使用MongoDB ObjectId）

## 最佳实践

1. **默认启用缓存**: 在Notebook中使用`use_cache=True`，避免重复计算
2. **定期清理**: 对于不再需要的历史结果，使用`delete_backtest_result()`删除
3. **查询优化**: 使用`query_backtest_results()`时指定`backtest_type`和日期范围，提高查询效率
4. **结果对比**: 可以加载多个历史结果进行对比分析
5. **参数变更**: 如果算法或参数阈值发生变化，系统会自动识别为不同的配置（不同的哈希），不会误用旧结果

## 故障处理

### MongoDB未连接

如果MongoDB未连接，系统会：
- 记录警告日志
- 回退到直接运行，不保存结果
- 不抛出异常，确保回测可以正常执行

### 缓存查找失败

如果缓存查找失败（如MongoDB连接问题），系统会：
- 记录警告日志
- 继续执行回测
- 尝试保存结果（如果MongoDB恢复连接）

### 结果加载失败

如果结果加载失败（如文件不存在），系统会：
- 记录错误日志
- 返回None
- 建议检查文件路径或重新运行回测

## 性能考虑

- **查询性能**: 使用MongoDB索引加速查询（特别是`config_hash`和`backtest_type`）
- **存储空间**: 大结果存储在文件系统中，避免MongoDB文档过大
- **内存使用**: 加载结果时，大结果从文件系统加载，避免占用过多内存

## 扩展性

系统设计支持未来扩展：

- **TTL机制**: 可以添加基于时间的缓存过期机制
- **结果压缩**: 对于大型结果，可以添加压缩支持
- **分布式存储**: 如果需要，可以迁移到分布式MongoDB集群
- **Web UI**: 可以基于查询接口开发Web管理界面

## 相关文档

- `core/market_trend_storage.py`: MarketTrendStorage类实现
- `core/signal_backtest.py`: 回测框架，集成缓存机制
- `core/cache_manager.py`: 参考的缓存模式
- `notebooks/lib/backtest_utils.py`: Notebook辅助工具

## 更新日志

### v1.0 (2026-01-03)

- 初始版本
- 扩展MarketTrendStorage类，添加回测结果管理方法
- 集成到signal_backtest.py
- 创建Notebook辅助工具
- 更新notebook使用说明

