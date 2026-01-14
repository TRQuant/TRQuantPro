# Notebook结果管理系统

> **创建时间**: 2026-01-14  
> **版本**: v1.0  
> **状态**: 已实施

## 概述

Notebook结果管理系统提供了自动化的notebook运行结果保存和管理功能，支持：
- ✅ **自动保存到带时间戳的文件夹**：每次运行都会创建独立的文件夹，不会覆盖历史结果
- ✅ **MongoDB统一管理**：所有结果保存到数据库，方便查询和引用
- ✅ **完整数据保存**：包括结果数据、输出文本、图表、元数据等
- ✅ **版本管理**：支持历史追踪和对比
- ✅ **便捷引用**：其他notebook可以通过运行ID或日期查询历史结果

## 目录结构

```
notebooks/research/results/
├── chen_xiaoqun_strategy/
│   ├── 01_market_environment_judgment/
│   │   ├── 20260114_133000/          # 运行ID（时间戳）
│   │   │   ├── result.json           # 结果数据
│   │   │   ├── metadata.json         # 元数据
│   │   │   ├── outputs/               # 输出文本
│   │   │   │   └── output_1.txt
│   │   │   ├── charts/               # 图表文件
│   │   │   │   └── chart_1.png
│   │   │   ├── data/                 # 数据文件（CSV等）
│   │   │   │   └── candidates.csv
│   │   │   └── 01_market_environment_judgment.ipynb  # Notebook副本
│   │   ├── 20260114_140000/          # 另一次运行
│   │   └── ...
│   └── 02_stock_selection/
│       ├── 20260114_133500/
│       └── ...
└── other_strategy/
    └── ...
```

## 使用方法

### 1. 在Notebook中自动保存

系统已经在以下notebook中集成了自动保存功能：
- `01_market_environment_judgment.ipynb` - 市场环境判断
- `02_stock_selection.ipynb` - 股票筛选

**运行notebook后，最后一个cell会自动保存结果**，无需手动操作。

### 2. 手动保存（如果需要）

```python
from core.notebook_result_manager import NotebookResultManager

# 创建管理器
manager = NotebookResultManager(
    strategy_name="chen_xiaoqun_strategy",
    notebook_name="01_market_environment_judgment"
)

# 保存结果
save_info = manager.save_result(
    result={
        'cycle': '启动期',
        'position': '10%',
        'strategy': '首板卡位术',
        'limit_up_count': 50,
        'max_height': 5,
        'zhaban_rate': 15.5
    },
    description="市场环境判断结果",
    tags=["市场环境", "情绪周期"],
    save_notebook_copy=True
)

print(f"保存成功！运行ID: {save_info['run_id']}")
```

### 3. 查询历史结果

```python
from core.notebook_result_manager import NotebookResultManager

# 创建管理器
manager = NotebookResultManager(
    strategy_name="chen_xiaoqun_strategy",
    notebook_name="01_market_environment_judgment"
)

# 列出最近10次运行
results = manager.list_results(limit=10)
for r in results:
    print(f"{r['run_id']}: {r['run_date']} {r['run_time']} - {r['result_summary']}")

# 获取最新结果
latest = manager.get_latest_result()
if latest:
    print(f"最新运行: {latest['run_id']}")

# 加载指定运行ID的结果
result = manager.load_result('20260114_133000')
if result:
    print(f"情绪周期: {result.get('cycle')}")
```

### 4. 在其他Notebook中引用

```python
from core.notebook_result_manager import NotebookResultManager

# 从第一步notebook读取结果
manager = NotebookResultManager(
    strategy_name="chen_xiaoqun_strategy",
    notebook_name="01_market_environment_judgment"
)

# 方法1: 获取最新结果
latest = manager.get_latest_result()
if latest:
    run_id = latest['run_id']
    result = manager.load_result(run_id)
    emotion_cycle = result.get('cycle')
    position = result.get('position')
    strategy = result.get('strategy')

# 方法2: 指定运行ID
result = manager.load_result('20260114_133000')
emotion_cycle = result.get('cycle')

# 方法3: 按日期查询
from datetime import datetime, timedelta
today = datetime.now().strftime('%Y-%m-%d')
results = manager.list_results(start_date=today, limit=1)
if results:
    result = manager.load_result(results[0]['run_id'])
```

## MongoDB数据结构

### 集合：`jqquant.notebook_results`

```python
{
    "_id": ObjectId("..."),
    "notebook_name": "01_market_environment_judgment",
    "strategy_name": "chen_xiaoqun_strategy",
    "run_id": "20260114_133000",              # 运行ID（时间戳）
    "run_date": "2026-01-14",                 # 运行日期
    "run_time": "13:30:00",                   # 运行时间
    "result_summary": {                        # 结果摘要
        "cycle": "启动期",
        "position": "10%",
        "strategy": "首板卡位术",
        "limit_up_count": 50,
        "max_height": 5,
        "zhaban_rate": 15.5
    },
    "parameters": {                            # 运行参数
        "notebook": "01_market_environment_judgment",
        "strategy": "chen_xiaoqun_strategy"
    },
    "tags": ["市场环境", "情绪周期", "陈小群战法"],
    "description": "市场环境判断结果（情绪周期分析）",
    "version": "1.0.0",
    "file_path": "chen_xiaoqun_strategy/01_market_environment_judgment/20260114_133000",
    "file_size": 10240,                        # 文件大小（字节）
    "output_count": 0,                        # 输出数量
    "chart_count": 0,                         # 图表数量
    "created_at": "2026-01-14T13:30:00",      # 创建时间（ISO格式）
    "result_data": {                          # 完整结果数据（小结果）或None（大结果）
        "cycle": "启动期",
        "position": "10%",
        ...
    }
}
```

### 索引

- `strategy_name + notebook_name`: 复合索引，加速查询
- `run_date`: 日期索引，支持日期范围查询
- `run_id`: 唯一索引，确保运行ID唯一
- `created_at`: 时间索引，支持时间排序

## API参考

### NotebookResultManager类

#### `__init__(strategy_name, notebook_name, base_output_dir=None, mongo_uri=None, db_name=None)`

初始化结果管理器。

**参数**:
- `strategy_name`: 策略名称（如：`chen_xiaoqun_strategy`）
- `notebook_name`: notebook名称（如：`01_market_environment_judgment`）
- `base_output_dir`: 基础输出目录（可选）
- `mongo_uri`: MongoDB连接URI（可选）
- `db_name`: 数据库名称（可选）

#### `save_result(result, outputs=None, charts=None, parameters=None, description="", tags=None, save_notebook_copy=True)`

保存notebook运行结果。

**参数**:
- `result`: 结果字典
- `outputs`: 输出列表（文本、数据等）
- `charts`: 图表列表（matplotlib/plotly图表对象）
- `parameters`: 运行参数
- `description`: 描述
- `tags`: 标签列表
- `save_notebook_copy`: 是否保存notebook副本

**返回**: 保存信息字典（包含run_id、文件路径等）

#### `list_results(limit=10, start_date=None, end_date=None)`

列出历史结果。

**参数**:
- `limit`: 返回数量限制
- `start_date`: 开始日期（YYYY-MM-DD）
- `end_date`: 结束日期（YYYY-MM-DD）

**返回**: 结果列表

#### `get_latest_result()`

获取最新结果。

**返回**: 最新结果字典或None

#### `load_result(run_id)`

加载指定运行ID的结果。

**参数**:
- `run_id`: 运行ID（格式：YYYYMMDD_HHMMSS）

**返回**: 结果字典或None

#### `get_result_path(run_id)`

获取结果路径。

**参数**:
- `run_id`: 运行ID

**返回**: 结果路径（Path对象）或None

## 最佳实践

### 1. 结果数据结构

建议将结果组织为清晰的字典结构：

```python
result = {
    # 核心结果
    'cycle': '启动期',
    'position': '10%',
    'strategy': '首板卡位术',
    
    # 原始数据
    'limit_up_count': 50,
    'max_height': 5,
    'zhaban_rate': 15.5,
    
    # 详细数据（DataFrame等）
    'candidates': candidates_df,  # 会自动保存为CSV
    
    # 元数据
    'confidence': 4.5,
    'data_source': 'AKShare + JQData'
}
```

### 2. 保存图表

```python
import plotly.graph_objects as go

# 创建图表
fig = go.Figure(...)

# 保存时包含图表
save_info = manager.save_result(
    result=result,
    charts=[fig]  # 图表会自动保存为PNG
)
```

### 3. 保存输出文本

```python
# 收集输出文本
outputs = []
outputs.append("市场环境判断结果：")
outputs.append(f"情绪周期: {emotion_cycle}")
outputs.append(f"建议仓位: {position}")

# 保存时包含输出
save_info = manager.save_result(
    result=result,
    outputs=outputs
)
```

### 4. 跨Notebook引用

在第二个notebook中引用第一个notebook的结果：

```python
# 在 02_stock_selection.ipynb 中
from core.notebook_result_manager import NotebookResultManager

# 读取第一步的结果
step1_manager = NotebookResultManager(
    strategy_name="chen_xiaoqun_strategy",
    notebook_name="01_market_environment_judgment"
)

latest = step1_manager.get_latest_result()
if latest:
    step1_result = step1_manager.load_result(latest['run_id'])
    emotion_cycle = step1_result.get('cycle')
    position = step1_result.get('position')
    strategy = step1_result.get('strategy')
    
    print(f"从第一步读取: {emotion_cycle}, {position}, {strategy}")
```

## 注意事项

1. **MongoDB连接**: 如果MongoDB不可用，系统会自动降级为仅文件系统保存
2. **大文件处理**: 超过10MB的结果不会完整保存到MongoDB，只保存摘要，完整数据从文件系统读取
3. **时间戳格式**: 运行ID使用`YYYYMMDD_HHMMSS`格式，确保唯一性和可排序性
4. **路径管理**: 所有路径使用相对路径，便于项目迁移
5. **数据格式**: DataFrame会自动保存为CSV，其他数据保存为JSON

## 故障排除

### MongoDB连接失败

如果看到"MongoDB连接失败"的警告，系统仍会保存到文件系统。检查：
1. MongoDB服务是否运行：`systemctl status mongod`
2. 连接URI是否正确：默认`mongodb://localhost:27017`

### 结果未保存

检查：
1. `result`变量是否存在
2. 是否有写入权限
3. 磁盘空间是否充足

### 查询不到历史结果

检查：
1. 运行ID格式是否正确（`YYYYMMDD_HHMMSS`）
2. 策略名称和notebook名称是否匹配
3. MongoDB索引是否创建成功

## 更新日志

### v1.0 (2026-01-14)
- ✅ 初始版本
- ✅ 支持文件系统和MongoDB双重保存
- ✅ 自动时间戳管理
- ✅ 图表和输出保存
- ✅ 历史查询功能
