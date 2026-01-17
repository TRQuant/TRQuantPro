#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接使用MCP工具添加BulletTrade知识库（最简洁方式）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 直接导入MCP工具
from mcp_servers.unified_dev_server import knowledge_add

# BulletTrade知识库条目
items = [
    {
        'title': 'BulletTrade 回测引擎概述',
        'content': '''BulletTrade 是兼容聚宽API的量化研究与交易框架，支持多数据源、多券商接入。

**核心特点**:
- ✅ **100%兼容聚宽API**: 聚宽策略可以在BulletTrade中无修改运行
- ✅ **多数据源支持**: JQData、MiniQMT、Tushare、本地缓存
- ✅ **多券商支持**: 本地QMT、远程QMT server、模拟券商
- ✅ **本地回测**: 无需联网，本地执行回测
- ✅ **实盘交易**: 支持实盘交易接口

**官方文档**: https://bullettrade.cn/docs/
**GitHub**: https://github.com/BulletTrade/bullet-trade

**与聚宽的关系**:
- BulletTrade完全兼容聚宽API
- 聚宽策略只需添加 `from jqdata import *` 即可在BulletTrade运行
- 无需任何代码转换

**适用场景**:
- 策略研究和开发
- 本地回测验证
- 实盘交易部署
- 多数据源测试''',
        'type': 'api_reference',
        'tags': ['BulletTrade', '回测引擎', '聚宽兼容', '量化框架', '回测系统'],
        'source': 'https://bullettrade.cn/docs/'
    },
    {
        'title': 'BulletTrade 安装和配置方法',
        'content': '''**安装方法**:
```bash
pip install bullet-trade
```

**环境配置 (.env)**:
```bash
DEFAULT_DATA_PROVIDER=jqdata
JQDATA_USERNAME=your_username
JQDATA_PASSWORD=your_password
DEFAULT_BROKER=simulator
```

**数据源配置**:
- jqdata: 聚宽数据（需要账号）
- miniqmt: 券商QMT免费行情
- tushare: Tushare数据（需要Token）
- mock: 模拟数据（用于测试）''',
        'type': 'tutorial',
        'tags': ['BulletTrade', '安装', '配置', '环境设置', '数据源'],
        'source': 'https://bullettrade.cn/docs/'
    },
    {
        'title': 'BulletTrade 回测使用指南',
        'content': '''**命令行回测**:
```bash
bullet-trade backtest strategies/bullettrade/my_strategy.py \\
  --start 2024-01-01 \\
  --end 2024-12-31 \\
  --cash 1000000 \\
  --benchmark 000300.XSHG \\
  --output backtest_results/my_backtest \\
  --auto-report
```

**回测参数说明**:
- --start: 回测开始日期
- --end: 回测结束日期
- --cash: 初始资金（默认100万）
- --benchmark: 基准指数
- --output: 输出目录
- --auto-report: 自动生成HTML报告

**策略文件要求**:
```python
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
```''',
        'type': 'guide',
        'tags': ['BulletTrade', '回测', '使用指南', '回测参数', '命令行'],
        'source': 'docs/07_workflow/BULLETTRADE_BACKTEST_GUIDE.md'
    },
    {
        'title': 'BulletTrade Python API 参考',
        'content': '''**Python API使用**:

```python
from core.bullettrade import BulletTradeEngine, BTConfig

config = BTConfig(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=1000000,
    data_provider="jqdata"
)

engine = BulletTradeEngine(config)
result = engine.run_backtest(strategy_path="strategies/bullettrade/my_strategy.py")

print(f"总收益率: {result.total_return:.2f}%")
print(f"夏普比率: {result.sharpe_ratio:.2f}")
```

**BTConfig 配置类**:
- start_date: 回测开始日期
- end_date: 回测结束日期
- initial_capital: 初始资金
- commission_rate: 佣金率
- data_provider: 数据源
- benchmark: 基准指数''',
        'type': 'api_reference',
        'tags': ['BulletTrade', 'Python API', 'BulletTradeEngine', 'BTConfig', 'BTResult'],
        'source': 'core/bullettrade/__init__.py'
    },
    {
        'title': 'BulletTrade 与聚宽 API 兼容性',
        'content': '''**核心结论**: BulletTrade和聚宽API **100%兼容**，无需转换！

**API对比**:
- from jqdata import *: ✅ 完全相同
- get_price(): ✅ 完全相同
- get_current_data(): ✅ 完全相同
- set_order_cost(): ✅ 完全相同
- order_target_value(): ✅ 完全相同

**转换关系**:
```
聚宽策略 → BulletTrade策略 ✅ 完全兼容，无需转换
BulletTrade策略 → PTrade策略 ⚠️ 需要转换
```

**使用示例**:
```python
# 聚宽策略（可直接在BulletTrade运行）
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
```''',
        'type': 'reference',
        'tags': ['BulletTrade', '聚宽', 'API兼容', '策略迁移', '无需转换'],
        'source': 'docs/07_workflow/BULLETTRADE_OFFICIAL_DOCS_ANALYSIS.md'
    },
    {
        'title': 'BulletTrade 在 TRQuant 项目中的集成',
        'content': '''**项目中的使用位置**:

1. **核心模块**: core/bullettrade/
   - engine.py - BulletTrade引擎封装
   - config.py - 配置类
   - result.py - 结果类

2. **MCP服务器集成**: mcp_servers/backtest_server_v2.py
   - backtest.bullettrade - BulletTrade回测工具

3. **工作流集成**: core/workflow_orchestrator.py
   - 步骤7（回测验证）自动使用BulletTrade

**使用示例**:
```python
from core.bullettrade import BulletTradeEngine, BTConfig

config = BTConfig(start_date="2024-01-01", end_date="2024-12-31")
engine = BulletTradeEngine(config)
result = engine.run_backtest(strategy_code)
```''',
        'type': 'integration',
        'tags': ['BulletTrade', 'TRQuant', '项目集成', 'MCP服务器', '工作流'],
        'source': 'core/bullettrade/'
    },
    {
        'title': 'BulletTrade 策略转换指南',
        'content': '''**转换关系**:

1. 聚宽 ↔ BulletTrade: ✅ 无需转换，完全兼容
2. BulletTrade/聚宽 → PTrade: ⚠️ 需要转换

**必须转换的差异**:
- 删除 from jqdata import *
- get_price() -> get_history()
- get_current_data() -> get_snapshot(stocks)
- set_order_cost() -> set_commission(PerTrade(...))

**转换器使用**:
```bash
python core/comprehensive_strategy_converter.py \\
    strategies/bullettrade/my_strategy.py \\
    strategies/ptrade/my_strategy_ptrade.py
```''',
        'type': 'guide',
        'tags': ['BulletTrade', '策略转换', 'PTrade', '聚宽', '转换器'],
        'source': 'docs/07_workflow/CORRECTED_CONVERSION_GUIDE.md'
    }
]

# 直接调用MCP工具添加
print("=" * 70)
print("使用MCP工具直接添加BulletTrade知识库")
print("=" * 70)

success = 0
failed = 0

for i, item in enumerate(items, 1):
    print(f"\n[{i}/{len(items)}] {item['title']}")
    try:
        result = knowledge_add(
            title=item['title'],
            content=item['content'],
            type=item['type'],
            tags=item['tags'],
            source=item.get('source', '')
        )
        if result.get('success') or result.get('knowledge_id'):
            success += 1
            kb_id = result.get('knowledge_id') or result.get('id', 'unknown')
            print(f"  ✅ 成功 (ID: {kb_id})")
        else:
            failed += 1
            print(f"  ❌ 失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        failed += 1
        print(f"  ❌ 异常: {e}")

print("\n" + "=" * 70)
print(f"✅ 成功: {success} 个")
print(f"❌ 失败: {failed} 个")
print("=" * 70)
