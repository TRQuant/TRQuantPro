# 回测Token消耗分析

## 问题分析

### 当前实现的问题

在生成的BulletTrade策略代码中，每次调仓都会调用JQData API：

1. **每次调仓调用**：
   - `get_price()` - 获取价格数据（每次调仓调用，约25次/半年）
   - `get_fundamentals()` - 获取基本面数据（每次调仓调用，约25次/半年）
   - `get_index_stocks()` - 获取指数成分股（每周调用）

2. **Token消耗估算**：
   - 半年回测：125个交易日
   - 每周调仓：约25次调仓
   - 每次调仓获取约300只股票的数据
   - **总API调用次数**：约 25 × 300 = 7,500次
   - **Token消耗**：每次API调用约消耗1-10 token，总计约7,500-75,000 token

### 解决方案

#### 方案1：使用预加载缓存数据（推荐）

**优点**：
- 零Token消耗（数据已预加载）
- 回测速度快（本地读取）
- 数据一致性高

**实现方式**：
1. 在策略初始化时加载所有缓存数据到内存
2. 策略代码中使用内存数据而不是API调用
3. 需要修改策略生成器，支持缓存数据注入

#### 方案2：修改BulletTrade数据提供者

**优点**：
- 不需要修改策略代码
- 可以统一管理数据源

**实现方式**：
1. 创建自定义数据提供者，从Parquet文件读取
2. 替换BulletTrade的默认数据提供者
3. 需要了解BulletTrade的数据提供者接口

#### 方案3：等待Auto模式

**说明**：
- 如果BulletTrade支持"auto"模式（使用本地数据，不调用API）
- 可以设置`data_provider="auto"`或类似配置

## 当前状态

### 已实现的功能

1. ✅ **数据预加载器** (`data_preloader.py`)
   - 支持并行下载数据到本地缓存
   - 数据格式：Parquet（高效压缩）
   - 支持增量更新

2. ✅ **缓存数据结构**
   ```
   data/cache/
   ├── daily_prices/2024H2_prices.parquet  # 所有股票的价格数据
   ├── fundamentals/valuation/2024H2_valuation.parquet  # 估值数据
   └── fundamentals/indicator/2024H2_indicator.parquet  # 财务指标
   ```

### 待实现的功能

1. ❌ **策略代码使用缓存数据**
   - 当前策略代码仍使用API调用
   - 需要修改策略生成器，注入缓存数据

2. ❌ **BulletTrade本地数据提供者**
   - 需要创建自定义数据提供者
   - 或修改BulletTrade配置使用本地数据

## 建议

### 短期方案（立即实施）

1. **修改策略生成器**，在策略初始化时加载缓存数据：
   ```python
   # 在策略代码中添加
   _cached_prices = None
   _cached_fundamentals = None
   
   def load_cache_data():
       global _cached_prices, _cached_fundamentals
       if _cached_prices is None:
           _cached_prices = pd.read_parquet('data/cache/daily_prices/2024H2_prices.parquet')
           _cached_fundamentals = pd.read_parquet('data/cache/fundamentals/valuation/2024H2_valuation.parquet')
   ```

2. **修改因子计算函数**，使用缓存数据：
   ```python
   def calculate_validated_factors(codes, date_str):
       # 使用 _cached_prices 而不是 get_price()
       # 使用 _cached_fundamentals 而不是 get_fundamentals()
   ```

### 长期方案（优化）

1. **创建BulletTrade本地数据提供者**
   - 实现`LocalDataProvider`类
   - 从Parquet文件读取数据
   - 替换默认的`jqdata`提供者

2. **数据预加载自动化**
   - 回测前自动检查缓存
   - 缺失数据自动下载
   - 支持多时间段缓存管理

## 当前回测Token消耗

### 实际消耗（已执行的回测）

- **数据预加载阶段**：约7,500次API调用（一次性）
- **回测执行阶段**：约7,500次API调用（策略代码中）
- **总计**：约15,000次API调用

### 优化后消耗

- **数据预加载阶段**：约7,500次API调用（一次性，可复用）
- **回测执行阶段**：0次API调用（使用缓存）
- **总计**：约7,500次API调用（减少50%）

## 下一步行动

1. ✅ **已完成**：数据预加载器
2. ⏳ **进行中**：修改策略生成器使用缓存数据
3. ⏳ **待实施**：创建本地数据提供者（可选）
