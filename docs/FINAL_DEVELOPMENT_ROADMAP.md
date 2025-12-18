# TRQuant 最终版后续开发方案

> **创建时间**: 2024-12-17  
> **版本**: v1.0 Final  
> **状态**: 正式规划

---

## 📋 一、系统现状总览

### 1.1 核心定位

**TRQuant = 9步投资工作流系统 + AI辅助量化平台**

```
┌─────────────────────────────────────────────────────────────┐
│                    TRQuant 系统定位                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  9步投资工作流（核心）                               │   │
│  │  1.信息获取 → 2.市场趋势 → 3.投资主线 → 4.候选池    │   │
│  │  → 5.因子构建 → 6.策略生成 → 7.回测验证             │   │
│  │  → 8.策略优化 → 9.报告生成                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│           ┌───────────────┴───────────────┐                 │
│           ▼                               ▼                  │
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │ Cursor扩展      │          │ PyQt6桌面       │          │
│  │ (主要工作界面)  │          │ (辅助/监控)     │          │
│  │ • 策略研究      │          │ • 回测执行      │          │
│  │ • 工作流执行    │          │ • 结果分析      │          │
│  │ • AI对话        │          │ • 运营监控      │          │
│  └─────────────────┘          └─────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 完成度评估

| 模块 | 完成度 | 状态 | 关键缺失 |
|-----|-------|------|---------|
| **MCP服务器** | 85% | ✅ 可用 | 需整合，减少数量 |
| **9步工作流** | 80% | ✅ 可用 | 缓存、状态持久化 |
| **Cursor扩展** | 90% | ✅ 可用 | 运营监控、结果管理 |
| **PyQt6 GUI** | 85% | ✅ 可用 | 策略优化面板 |
| **数据库架构** | 30% | ⚠️ 基础 | PostgreSQL、ClickHouse |
| **测试体系** | 20% | ⚠️ 基础 | 单元测试、集成测试 |

### 1.3 代码规模

```
TRQuant项目统计：
├── MCP服务器: 35个文件, ~15000行代码
├── Cursor扩展: 58个TypeScript文件, ~8000行代码
├── PyQt6 GUI: 15个面板, ~5000行代码
├── 核心库: ~10000行代码
└── 文档: 200+个文件
```

---

## 🎯 二、开发原则（不可违背）

### 2.1 核心原则

1. **9步工作流不可更改**
   - 步骤顺序、命名、ID保持固定
   - 所有优化围绕这9步展开

2. **Cursor扩展为主工作界面**
   - 策略研究、工作流执行在Cursor中完成
   - PyQt6作为辅助和监控工具

3. **优化而非重构**
   - 不改变整体架构
   - 增量添加功能
   - 保持向后兼容

4. **实用优先**
   - 每个功能必须有明确使用场景
   - 避免过度工程化

### 2.2 技术约束

| 约束 | 说明 |
|-----|------|
| Python环境 | 统一使用 `/home/taotao/dev/QuantTest/TRQuant/venv` |
| MCP服务器 | 控制在6个以内 |
| 数据源 | 优先JQData，备选AKShare |
| 回测引擎 | 快速回测优先，BulletTrade备选 |

---

## 📊 三、后续开发路线图

### 总体规划（8周）

```
┌─────────────────────────────────────────────────────────────┐
│                    开发路线图 (8周)                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 1-2: 基础设施强化                                      │
│  ├── MCP服务器整合 (8→6)                                     │
│  ├── 缓存层实施 (Redis)                                      │
│  └── 工作流状态持久化                                        │
│                                                              │
│  Week 3-4: Cursor扩展完善                                    │
│  ├── 运营监控面板                                            │
│  ├── 结果管理中心                                            │
│  └── 回测历史TreeView                                        │
│                                                              │
│  Week 5-6: 数据库架构                                        │
│  ├── PostgreSQL部署                                          │
│  ├── 数据迁移                                                │
│  └── Chroma向量库集成                                        │
│                                                              │
│  Week 7-8: 质量保障与文档                                    │
│  ├── 单元测试覆盖                                            │
│  ├── 集成测试                                                │
│  └── 用户文档完善                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 四、Phase 1: 基础设施强化（Week 1-2）

### 4.1 MCP服务器整合

**目标**: 从30+个服务器整合到6个核心服务器

#### 最终服务器架构

| # | 服务器名称 | 工具数 | 职责 |
|---|-----------|-------|------|
| 1 | `filesystem` | 15 | 文件操作（官方） |
| 2 | `trquant-core` | 35 | 数据+市场+因子+策略+回测+优化 |
| 3 | `trquant-workflow` | 6 | 9步工作流编排 |
| 4 | `trquant-project` | 17 | 项目+任务+日志管理 |
| 5 | `trquant-trading` | 5 | 交易执行（预留） |
| 6 | `trquant-dev` | 15 | 代码+测试+文档 |

#### 实施步骤

```bash
# Step 1: 验证trquant_core_server.py完整性
python -c "import sys; sys.path.insert(0, 'mcp_servers'); from trquant_core_server import *; print('OK')"

# Step 2: 更新mcp.json配置
# 只保留6个服务器

# Step 3: 删除冗余服务器文件
# 保留: trquant_core_server.py, workflow_9steps_server.py, 
#       project_manager_server.py, trading_server.py, dev_server.py

# Step 4: 重启Cursor，测试MCP连接
```

#### 任务清单

- [ ] 验证`trquant_core_server.py`包含35个工具
- [ ] 更新`.cursor/mcp.json`为6服务器配置
- [ ] 创建`dev_server.py`合并开发工具
- [ ] 删除冗余服务器文件
- [ ] 测试所有MCP工具调用

### 4.2 缓存层实施

**目标**: 实现工作流上下文缓存，避免重复计算

#### 缓存架构

```python
# 缓存配置
CACHE_CONFIG = {
    # 市场状态 - 5分钟有效
    "market.status": {"ttl": 300},
    
    # 投资主线 - 30分钟有效
    "market.mainlines": {"ttl": 1800},
    
    # 因子推荐 - 1小时有效
    "factor.recommend": {"ttl": 3600},
    
    # 候选池 - 1天有效
    "data.candidate_pool": {"ttl": 86400},
    
    # 回测结果 - 永久（按hash）
    "backtest.result": {"ttl": -1}
}
```

#### 实施方案

**方案A: 文件缓存（简单，推荐先用）**
```python
# mcp_servers/utils/cache.py
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path(__file__).parent.parent.parent / ".cache"

class FileCache:
    def __init__(self, namespace: str, ttl: int = 300):
        self.namespace = namespace
        self.ttl = ttl
        self.cache_dir = CACHE_DIR / namespace
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str) -> dict | None:
        cache_file = self._get_cache_file(key)
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # 检查过期
            if self.ttl > 0:
                cached_at = datetime.fromisoformat(data['cached_at'])
                if datetime.now() - cached_at > timedelta(seconds=self.ttl):
                    cache_file.unlink()
                    return None
            
            return data['value']
        except:
            return None
    
    def set(self, key: str, value: dict) -> None:
        cache_file = self._get_cache_file(key)
        with open(cache_file, 'w') as f:
            json.dump({
                'cached_at': datetime.now().isoformat(),
                'value': value
            }, f)
    
    def _get_cache_file(self, key: str) -> Path:
        key_hash = hashlib.md5(key.encode()).hexdigest()[:16]
        return self.cache_dir / f"{key_hash}.json"
```

**方案B: Redis缓存（生产环境）**
```python
# 待Phase 5数据库架构时实施
```

#### 任务清单

- [ ] 创建`mcp_servers/utils/cache.py`
- [ ] 在`workflow_9steps_server.py`中集成缓存
- [ ] 在每个步骤执行前检查缓存
- [ ] 测试缓存命中和过期机制

### 4.3 工作流状态持久化

**目标**: 工作流执行状态可保存和恢复

#### 状态存储结构

```python
# .trquant/workflows/{workflow_id}.json
{
    "workflow_id": "wf_abc123",
    "name": "我的工作流",
    "created_at": "2024-12-17T10:00:00",
    "updated_at": "2024-12-17T10:30:00",
    "status": "in_progress",  # created/in_progress/completed/failed
    "current_step": 5,
    "context": {
        "market_status": {...},
        "mainlines": [...],
        "candidate_pool": [...],
        "factors": [...]
    },
    "steps": [
        {"id": "data_source", "status": "completed", "result": {...}},
        {"id": "market_trend", "status": "completed", "result": {...}},
        ...
    ]
}
```

#### 任务清单

- [ ] 创建`mcp_servers/utils/workflow_storage.py`
- [ ] 实现工作流保存/加载接口
- [ ] 在`workflow_9steps_server.py`中集成
- [ ] 添加工作流恢复命令到Cursor扩展

---

## 🖥️ 五、Phase 2: Cursor扩展完善（Week 3-4）

### 5.1 运营监控面板

**目标**: 实时监控回测任务状态

#### 文件创建

```typescript
// extension/src/views/monitoringPanel.ts

export class MonitoringPanel {
    // 任务状态监控
    // 系统健康检查
    // 批量任务管理
}
```

#### UI设计

```
┌─────────────────────────────────────────────────┐
│  📊 运营监控中心                                 │
├─────────────────────────────────────────────────┤
│  系统状态: ✅ 正常                               │
│  ├── MCP服务器: ✅ 6/6 在线                      │
│  ├── 数据源: ✅ JQData 连接正常                  │
│  └── 回测引擎: ✅ 就绪                           │
├─────────────────────────────────────────────────┤
│  运行中任务 (2)                                  │
│  ┌─────────────────────────────────────────┐    │
│  │ 策略A回测  [████████░░] 80%  预计2分钟   │    │
│  │ 策略B优化  [██░░░░░░░░] 20%  预计5分钟   │    │
│  └─────────────────────────────────────────┘    │
├─────────────────────────────────────────────────┤
│  最近完成 (5)                                    │
│  • 策略C回测 ✅ 完成 收益率: 25.3%              │
│  • 策略D回测 ❌ 失败 错误: 数据不足             │
└─────────────────────────────────────────────────┘
```

#### 任务清单

- [ ] 创建`monitoringPanel.ts`
- [ ] 实现系统状态检查API
- [ ] 实现任务进度轮询机制
- [ ] 注册命令`trquant.openMonitoring`

### 5.2 结果管理中心

**目标**: 管理历史回测结果，支持对比分析

#### 文件创建

```typescript
// extension/src/views/resultManagerPanel.ts

export class ResultManagerPanel {
    // 结果列表
    // 筛选搜索
    // 对比分析
    // 导出功能
}
```

#### UI设计

```
┌─────────────────────────────────────────────────┐
│  📋 回测结果管理                                 │
├─────────────────────────────────────────────────┤
│  [🔍 搜索] [📅 日期筛选] [📊 排序] [📥 导出]    │
├─────────────────────────────────────────────────┤
│  ☑ 策略名称        日期         收益率  夏普   │
│  ──────────────────────────────────────────────│
│  ☐ 动量策略v1.0   12-17 10:30   25.3%   1.8   │
│  ☑ 多因子v2.1     12-16 15:20   18.7%   1.5   │
│  ☐ 价值成长v1.2   12-15 09:00   22.1%   1.6   │
├─────────────────────────────────────────────────┤
│  [📊 对比选中] [🗑️ 删除] [📄 查看详情]          │
└─────────────────────────────────────────────────┘
```

#### 任务清单

- [ ] 创建`resultManagerPanel.ts`
- [ ] 实现结果存储（VS Code Memento + 文件系统）
- [ ] 实现结果筛选和搜索
- [ ] 实现多结果对比图表
- [ ] 注册命令`trquant.openResultManager`

### 5.3 回测历史TreeView

**目标**: 在侧边栏显示回测历史

#### 实现

```typescript
// extension/src/views/backtestHistoryTreeView.ts

export class BacktestHistoryTreeProvider implements vscode.TreeDataProvider<BacktestHistoryItem> {
    // 按策略分组
    // 显示关键指标
    // 双击打开详情
}
```

#### 任务清单

- [ ] 创建`backtestHistoryTreeView.ts`
- [ ] 在`package.json`中注册TreeView
- [ ] 实现右键菜单（查看、对比、删除）

### 5.4 命令注册

```json
// extension/package.json 新增

{
    "contributes": {
        "commands": [
            {
                "command": "trquant.openMonitoring",
                "title": "TRQuant: 打开运营监控",
                "icon": "$(dashboard)"
            },
            {
                "command": "trquant.openResultManager",
                "title": "TRQuant: 打开结果管理",
                "icon": "$(list-unordered)"
            },
            {
                "command": "trquant.compareResults",
                "title": "TRQuant: 对比回测结果"
            }
        ],
        "views": {
            "trquant-explorer": [
                {
                    "id": "trquant-backtest-history",
                    "name": "回测历史"
                }
            ]
        }
    }
}
```

---

## 🗄️ 六、Phase 3: 数据库架构（Week 5-6）

### 6.1 数据库选型（确认）

| 数据库 | 用途 | 部署方式 |
|-------|------|---------|
| **PostgreSQL** | 关系型主库（用户、策略、配置） | Docker |
| **SQLite** | 本地轻量存储（回测结果） | 内置 |
| **Chroma** | 向量库（RAG知识库） | 本地 |

### 6.2 PostgreSQL部署

```bash
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    container_name: trquant-postgres
    environment:
      POSTGRES_USER: trquant
      POSTGRES_PASSWORD: trquant123
      POSTGRES_DB: trquant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 6.3 数据模型

```sql
-- 策略表
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code TEXT,
    platform VARCHAR(20),  -- ptrade/qmt/local
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 回测结果表
CREATE TABLE backtest_results (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(id),
    start_date DATE,
    end_date DATE,
    initial_capital DECIMAL(15,2),
    total_return DECIMAL(10,4),
    annual_return DECIMAL(10,4),
    sharpe_ratio DECIMAL(6,3),
    max_drawdown DECIMAL(10,4),
    win_rate DECIMAL(6,4),
    trade_count INTEGER,
    equity_curve JSONB,
    trades JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 工作流记录表
CREATE TABLE workflow_runs (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    status VARCHAR(20),
    current_step INTEGER,
    context JSONB,
    steps JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.4 任务清单

- [ ] 创建`docker-compose.yml`
- [ ] 创建数据库Schema
- [ ] 创建`core/database/`模块
- [ ] 迁移现有数据到PostgreSQL
- [ ] 集成Chroma向量库

---

## ✅ 七、Phase 4: 质量保障（Week 7-8）

### 7.1 测试体系

#### 单元测试覆盖

```python
# tests/test_mcp_servers/test_core_server.py

import pytest
from mcp_servers.trquant_core_server import *

class TestDataTools:
    def test_health_check(self):
        result = _handle_health_check({})
        assert result["success"] == True
    
    def test_get_price(self):
        result = _handle_get_price({
            "securities": ["000001.XSHE"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        })
        assert "data" in result

class TestMarketTools:
    def test_market_status(self):
        result = _handle_market_status({"universe": "CN_EQ"})
        assert "regime" in result
```

#### 集成测试

```python
# tests/test_integration/test_workflow.py

class TestWorkflow9Steps:
    def test_full_workflow(self):
        """测试完整9步工作流"""
        workflow_id = create_workflow()
        
        # 执行每个步骤
        for step in WORKFLOW_9STEPS:
            result = execute_step(workflow_id, step["id"])
            assert result["success"] == True
        
        # 验证最终状态
        workflow = get_workflow(workflow_id)
        assert workflow["status"] == "completed"
```

### 7.2 测试覆盖目标

| 模块 | 目标覆盖率 |
|-----|-----------|
| MCP服务器 | 80% |
| 工作流引擎 | 90% |
| 数据库层 | 70% |
| Cursor扩展 | 50% |

### 7.3 任务清单

- [ ] 创建`tests/`目录结构
- [ ] 编写MCP服务器单元测试
- [ ] 编写工作流集成测试
- [ ] 配置CI/CD测试流程
- [ ] 生成测试覆盖率报告

---

## 📅 八、详细任务计划

### Week 1: MCP整合 + 缓存

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1 | 验证trquant_core_server.py | 服务器文件完整 |
| Day 2 | 更新mcp.json配置 | 6服务器配置 |
| Day 3 | 创建缓存模块 | cache.py |
| Day 4 | 集成缓存到工作流 | 缓存可用 |
| Day 5 | 测试和修复 | 全部通过 |

### Week 2: 状态持久化

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1 | 创建workflow_storage.py | 存储模块 |
| Day 2 | 集成到workflow_9steps_server | 持久化可用 |
| Day 3 | Cursor扩展工作流恢复 | 恢复功能 |
| Day 4 | 测试状态保存/恢复 | 功能完整 |
| Day 5 | 文档和优化 | 文档更新 |

### Week 3: 运营监控面板

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1 | 创建monitoringPanel.ts框架 | 基础面板 |
| Day 2 | 实现系统状态检查 | 状态显示 |
| Day 3 | 实现任务进度显示 | 进度条 |
| Day 4 | 实现任务列表 | 任务管理 |
| Day 5 | UI美化和测试 | 面板完成 |

### Week 4: 结果管理中心

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1 | 创建resultManagerPanel.ts | 基础面板 |
| Day 2 | 实现结果存储 | 存储可用 |
| Day 3 | 实现筛选搜索 | 搜索功能 |
| Day 4 | 实现对比分析 | 对比图表 |
| Day 5 | TreeView和集成 | 功能完整 |

### Week 5-6: 数据库

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1-2 | PostgreSQL部署 | 数据库运行 |
| Day 3-4 | Schema创建 | 表结构 |
| Day 5-6 | ORM模块开发 | database模块 |
| Day 7-8 | 数据迁移 | 数据迁移完成 |
| Day 9-10 | Chroma集成 | 向量库可用 |

### Week 7-8: 测试

| 日期 | 任务 | 产出 |
|-----|------|------|
| Day 1-3 | 单元测试编写 | 测试用例 |
| Day 4-5 | 集成测试编写 | 集成测试 |
| Day 6-7 | Bug修复 | 问题修复 |
| Day 8-10 | 文档完善 | 用户文档 |

---

## 🎯 九、关键里程碑

| 里程碑 | 日期 | 验收标准 |
|-------|------|---------|
| **M1: MCP整合完成** | Week 1结束 | 6服务器运行正常 |
| **M2: 缓存可用** | Week 2结束 | 缓存命中率>80% |
| **M3: 监控面板上线** | Week 3结束 | 可实时监控任务 |
| **M4: 结果管理可用** | Week 4结束 | 可管理历史结果 |
| **M5: 数据库就绪** | Week 6结束 | PostgreSQL+Chroma |
| **M6: 测试覆盖达标** | Week 8结束 | 覆盖率>70% |

---

## 📊 十、成功指标

### 10.1 性能指标

| 指标 | 目标值 |
|-----|-------|
| 工作流完整执行时间 | < 60秒 |
| 单步缓存命中率 | > 80% |
| MCP调用响应时间 | < 2秒 |
| 结果列表加载时间 | < 1秒 |

### 10.2 质量指标

| 指标 | 目标值 |
|-----|-------|
| 测试覆盖率 | > 70% |
| Bug密度 | < 1个/千行代码 |
| 文档完整度 | > 90% |

### 10.3 用户体验指标

| 指标 | 目标值 |
|-----|-------|
| 工作流成功率 | > 95% |
| 错误恢复率 | > 80% |
| 用户满意度 | > 4/5 |

---

## 📝 十一、执行检查清单

### 每日检查

- [ ] 代码提交到Git
- [ ] 测试通过
- [ ] 文档同步更新

### 每周检查

- [ ] 里程碑进度评估
- [ ] 风险识别和处理
- [ ] 任务计划调整

### 每阶段检查

- [ ] 功能验收
- [ ] 性能验收
- [ ] 用户体验验收

---

## 📚 十二、参考文档

| 文档 | 路径 |
|-----|------|
| 平台优化方案（修正版） | `docs/PLATFORM_OPTIMIZATION_PLAN_CORRECTED.md` |
| MCP服务器整合方案 | `docs/MCP_SERVER_CONSOLIDATION.md` |
| 前端架构计划 | `docs/FRONTEND_ARCHITECTURE_AND_PLAN.md` |
| 数据库架构背景 | `docs/DATABASE_ARCHITECTURE_AND_KB_BACKGROUND.md` |
| 监控集成方案 | `docs/CURSOR_EXTENSION_MONITORING_INTEGRATION.md` |

---

**文档维护**: TRQuant Dev Team  
**最后更新**: 2024-12-17  
**版本**: v1.0 Final

