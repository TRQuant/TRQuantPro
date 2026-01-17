# Notebook缓存功能更新说明

## 更新日期
2026-01-04 (最后更新: 2026-01-04 23:30)

## 更新文件
- `notebooks/research/01_市场趋势判断回测验证.ipynb`
- `core/signal_backtest.py`

## 最新更新 (2026-01-04 23:30)

### MongoDB 保存验证增强

在 notebook 中添加了明确的 MongoDB 保存验证功能，确保用户能够清楚地看到回测结果是否已成功保存到数据库。

**新增功能：**
1. MongoDB 连接状态检查
2. 保存前后的结果数量对比
3. 显示最新保存的结果 ID
4. Phase 2 缓存完整性检查（信号数>0）

**输出示例：**
```
✅ MongoDB已连接

💾 新结果已保存到MongoDB数据库
   数据库中Phase 1结果数: 1 → 2
   最新结果ID: 695ae896cf1ec34386c0bc3d
```

## 更新内容

### 1. 核心数据类扩展

为 `EnhancedSignalRecord` 和 `EnhancedBacktestResult` 添加了 `from_dict()` 类方法，支持从字典完整恢复对象：

```python
# EnhancedSignalRecord.from_dict()
- 自动转换枚举类型（SignalType, MarketStateCategory）
- 保持所有字段完整性

# EnhancedBacktestResult.from_dict()
- 恢复 BacktestConfig 对象
- 恢复所有 EnhancedSignalRecord 对象
- 支持从MongoDB或文件加载
```

### 2. Notebook 缓存支持

#### Phase 1 回测 (Cell 16)
- 添加 `USE_CACHE` 参数控制
- 自动检查数据库中是否有缓存结果
- 如果有缓存：使用 `storage.load_backtest_result()` 加载（<1秒）
- 如果无缓存：运行新回测并自动保存

#### Phase 2 回测 (Cell 20)
- 同 Phase 1，支持完整的缓存机制
- 对于10年回测，缓存可节省8-12分钟

#### 可视化 (Cells 23-25)
- 自动检测 `phase2_result` 是否存在
- 如果不存在，自动从数据库加载最新结果
- 无需手动管理内存中的对象

## 使用方法

### 基本用法

```python
# Phase 1 回测（使用缓存）
USE_CACHE = True  # 默认True
phase1_result = run_phase1_backtest(sample_interval=10)
# 如果缓存存在，几秒内返回；否则运行新回测

# Phase 1 回测（强制重新运行）
USE_CACHE = False
phase1_result = run_phase1_backtest(sample_interval=10)
# 忽略缓存，运行新回测
```

### 可视化自动加载

```python
# 即使 phase2_result 不在内存中，可视化也能正常工作
# Notebook 会自动从数据库加载最新结果
fig = viz.create_accuracy_heatmap()
fig.show()
```

## 优势

1. **避免重复计算**
   - 相同配置的回测只运行一次
   - 后续使用直接从缓存加载
   - Phase 2 回测可节省 8-12 分钟

2. **跨会话持久化**
   - 关闭notebook后结果仍保存在数据库
   - 新会话可直接使用历史结果
   - 支持多人协作（共享数据库）

3. **版本管理**
   - 每个结果包含算法版本信息
   - 可以比较不同版本的结果
   - 支持查询特定版本的历史结果

4. **透明的缓存机制**
   - 用户无需手动管理缓存
   - 自动处理文件路径和反序列化
   - 缓存失效时自动运行新回测

## 技术细节

### 缓存查找逻辑

```python
# 1. 计算配置哈希
config_hash = md5(json.dumps(config, sort_keys=True))

# 2. 查找匹配的缓存
cached = storage.find_cached_backtest(config_dict, backtest_type='signal_phase1')

# 3. 加载完整结果
if cached:
    result = storage.load_backtest_result(str(cached['_id']))
    # 自动处理：
    # - 从MongoDB或文件加载
    # - pickle反序列化
    # - 对象重建
```

### 存储结构

- **MongoDB**: 存储元数据和小结果（<10MB）
- **文件系统**: 存储大结果（>10MB），MongoDB存储文件路径
- **索引**: `backtest_type + algorithm_version + config_hash` 复合索引

## 注意事项

1. **Phase 2 迁移结果**
   - 从旧JSON文件迁移的Phase 2结果信号数为0（原文件不完整）
   - 建议重新运行Phase 2回测获取完整数据

2. **配置变化**
   - 配置参数变化会导致缓存失效
   - 例如：修改 `sample_interval` 会运行新回测

3. **算法版本**
   - 算法代码变化会生成新版本
   - 新版本不会使用旧版本的缓存
   - 支持版本间结果比较

## 数据库状态查询

```python
from core.market_trend_storage import MarketTrendStorage

storage = MarketTrendStorage()

# 查询所有Phase 1结果
results = storage.query_backtest_results(
    backtest_type='signal_phase1',
    limit=10,
    sort_by='created_at',
    sort_order=-1  # 最新的在前
)

# 查看结果信息
for r in results:
    print(f"ID: {r['_id']}")
    print(f"创建时间: {r['created_at']}")
    print(f"算法版本: {r['algorithm_version']}")
    print(f"总信号数: {r['summary']['total_signals']}")
```

## 下一步

1. 运行新的 Phase 2 回测以获取完整数据
2. 使用缓存功能加速后续分析
3. 比较不同版本的结果（如果修改算法）

## 相关文档

- `docs/BACKTEST_RESULT_STORAGE.md`: 完整的存储系统文档
- `notebooks/lib/backtest_utils.py`: Notebook辅助工具
- `core/market_trend_storage.py`: 存储管理器实现
