#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
补充BulletTrade知识
===================

将BulletTrade相关文章和文档添加到知识库
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


def supplement_bullettrade_knowledge():
    """补充BulletTrade知识"""
    
    print("=" * 70)
    print("📚 补充BulletTrade知识")
    print("=" * 70)
    print()
    
    bullettrade_knowledge = [
        {
            "title": "BulletTrade - 聚宽策略本地实盘解决方案",
            "content": """## BulletTrade - 聚宽策略本地实盘解决方案

### 项目简介
BulletTrade 是一个兼容聚宽 API 的本地量化框架，让聚宽策略代码几乎不改就能在本地回测、实盘。

### 核心特点
- **聚宽API兼容**: `from jqdata import *` 在本地也能跑
- **策略代码无需修改**: 聚宽策略直接迁移
- **多数据源支持**: JQData、MiniQMT、TuShare
- **本地运行**: 完全本地化，不依赖外部平台
- **实盘接入**: 支持QMT实盘交易

### 安装
```bash
pip install bullet-trade
```

### 核心功能

#### 1. 聚宽策略无缝迁移
在聚宽写的策略，可以直接使用：
```python
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    g.security = '510300.XSHG'
    run_daily(trade, 'every_bar')

def trade(context):
    if g.security not in context.portfolio.positions:
        order_value(g.security, context.portfolio.available_cash)
```

#### 2. 多数据源支持
切换数据源只需改一行配置：
```bash
# .env 配置文件
DEFAULT_DATA_PROVIDER=jqdata    # 聚宽数据（需要账号）
# DEFAULT_DATA_PROVIDER=miniqmt # MiniQMT 数据
# DEFAULT_DATA_PROVIDER=tushare # TuShare 数据
```

支持的数据源：
- **MiniQMT**: QMT客户端自带，开通券商账户即可免费使用
- **TuShare**: 注册即可用，部分高级数据需要积分
- **JQData**: 聚宽官方数据，质量好但需要付费
- **本地缓存**: 自动缓存历史数据，重复回测更快

#### 3. 回测引擎
```bash
bullet-trade backtest your_strategy.py --start 2024-01-01 --end 2024-12-01
```

回测引擎特点：
- 真实价格撮合：用开盘价/收盘价成交
- 分红送股处理：自动处理除权除息
- 支持分钟/日线：`--frequency minute` 或 `--frequency day`
- HTML报告一键生成：收益曲线、回撤、交易记录

#### 4. 参数优化
```bash
bullet-trade optimize your_strategy.py \\
    --params '{"ma_period": [5, 10, 20], "threshold": [0.01, 0.02, 0.03]}' \\
    --start 2020-01-01 --end 2023-12-31
```

自动遍历所有参数组合，输出最优解。

#### 5. Tick实时行情（打板利器）
支持tick级别的实时行情订阅：
```python
def initialize(context):
    g.watch_list = ['000001.XSHE', '000002.XSHE']
    g.limit_up = {}  # 缓存涨停价
    
    # 订阅 tick 数据
    subscribe(g.watch_list, 'tick')

def before_trading_start(context):
    # 开盘前获取涨停价
    for code in g.watch_list:
        data = get_current_data()[code]
        g.limit_up[code] = data.high_limit  # 涨停价

def handle_tick(context, tick):
    # 实时处理每一笔 tick
    code = tick['sid']
    price = tick['last_price']
    bid1_vol = tick.get('bid1_volume', 0)  # 买一量（封单量）
    
    # 判断涨停 + 封单量
    limit_up = g.limit_up.get(code)
    if limit_up and price >= limit_up and bid1_vol > 100000:
        print(f"{code} 涨停封单！封单量: {bid1_vol}")
```

Tick功能特点：
- ⚡ 毫秒级延迟：基于QMT的xtdata实时推送
- 📊 盘口深度：买一卖一价格和挂单量
- 🌐 全市场订阅：`subscribe(['SH', 'SZ'], 'tick')` 扫描全市场
- 打板场景：实时监控封单量变化，判断涨停板强度

#### 6. 实盘接入

**方案一：独立实盘（完全本地运行）**

本地QMT（Windows）：
```bash
bullet-trade live your_strategy.py --broker qmt
```

远程QMT Server（Mac/Linux也能用）：
```bash
# Windows机器上运行QMT Server
bullet-trade server --listen 0.0.0.0 --port 58620 --token your_secret

# Mac/Linux上运行策略
bullet-trade live your_strategy.py --broker qmt-remote
```

**方案二：聚宽模拟盘 + 远程QMT Server**

混合方案：策略在聚宽模拟盘实时运行，产生交易信号后调用QMT Server执行真实下单。

使用步骤：
1. 在Windows机器上启动QMT Server：
```bash
bullet-trade server --listen 0.0.0.0 --port 58620 --token your_secret
```

2. 把`bullet_trade_jq_remote_helper.py`上传到聚宽研究根目录

3. 在聚宽模拟盘策略中调用远程下单：
```python
import bullet_trade_jq_remote_helper as bt

def initialize(context):
    # 配置远程QMT Server
    bt.configure(
        host='你的服务器IP',
        port=58620,
        token='your_secret'
    )

def handle_data(context, data):
    if should_buy:
        # 聚宽模拟盘下单（可选，用于记录）
        order('510300.XSHG', 100)
        # 同时调用远程QMT真实下单
        bt.order('510300.XSHG', 100)
    
    # 查询真实账户信息
    real_portfolio = bt.get_portfolio()
    print(f"真实账户可用资金: {real_portfolio['available_cash']}")
```

### 快速上手

**Step 1: 安装**
```bash
pip install bullet-trade
```

**Step 2: 配置数据源**
创建`.env`文件：
```bash
# 方式一：MiniQMT（推荐，开通QMT后免费使用）
DEFAULT_DATA_PROVIDER=qmt

# 方式二：TuShare（需要注册，部分数据免费）
# DEFAULT_DATA_PROVIDER=tushare
# TUSHARE_TOKEN=你的token

# 方式三：JQData（聚宽数据，需要申请账号）
# DEFAULT_DATA_PROVIDER=jqdata
# JQDATA_USER=你的账号
# JQDATA_PASSWORD=你的密码
```

**Step 3: 运行**
```bash
# 回测
bullet-trade backtest your_strategy.py --start 2024-01-01 --end 2024-06-01

# 或者启动研究环境（JupyterLab）
bullet-trade lab
```

### 与聚宽的关系
BulletTrade不是聚宽官方项目，是个人开发的开源工具。

定位：
- 聚宽的补充，不是替代
- 让聚宽用户的策略能本地化运行
- 提供从回测到实盘的完整链路

使用建议：
- 只需要研究和回测 → 聚宽研究环境足够了
- 想要本地运行、实盘接入 → BulletTrade是个选择
- 两者可以配合使用：在聚宽上研究调试，确认没问题后用BulletTrade本地实盘

### 项目现状
**已支持**：
- ✅ 聚宽API兼容（大部分常用API）
- ✅ 多数据源（JQData、MiniQMT、TuShare）
- ✅ 日线/分钟级回测
- ✅ 参数优化
- ✅ 本地/远程QMT实盘
- ✅ CLI工具链

**规划中**：
- 🔲 Web UI监控面板
- 🔲 更多数据源支持
- 🔲 策略模板库

### 资源链接
- GitHub: https://github.com/BulletTrade/bullet-trade
- 文档站点: https://bullettrade.cn/
- 问题反馈: GitHub Issue

### 适用场景
- 聚宽策略想本地实盘
- 不想依赖聚宽官方实盘服务
- 需要完全本地化运行
- Mac/Linux用户想用QMT实盘
- 需要tick级别实时行情（打板场景）

### 注意事项
- BulletTrade是开源项目，非聚宽官方
- 需要QMT客户端才能实盘交易
- 数据源需要单独配置和申请
- 适合有一定Python基础的量化交易者""",
            "type": "reference",
            "tags": ["BulletTrade", "聚宽", "实盘交易", "QMT", "本地量化", "策略迁移", "API兼容"],
            "source": "BulletTrade官方文档和社区文章"
        },
        {
            "title": "BulletTrade实盘接入方案对比",
            "content": """## BulletTrade实盘接入方案对比

### 方案一：独立实盘（完全本地运行）

**特点**：
- 策略代码、数据、下单全部在本地完成
- 不依赖任何外部平台
- 完全自主控制

**适用场景**：
- 想要完全本地化运行
- 不想依赖任何外部服务
- 需要完全控制策略执行

**实现方式**：
1. **本地QMT（Windows）**：
   ```bash
   bullet-trade live your_strategy.py --broker qmt
   ```
   - 需要Windows系统
   - 需要安装QMT客户端
   - 策略直接跑在本地

2. **远程QMT Server（Mac/Linux）**：
   ```bash
   # Windows机器上运行QMT Server
   bullet-trade server --listen 0.0.0.0 --port 58620 --token your_secret
   
   # Mac/Linux上运行策略
   bullet-trade live your_strategy.py --broker qmt-remote
   ```
   - Mac/Linux用户也能实盘
   - 策略可以跑在云服务器上
   - 策略代码不用上传到任何平台

**优势**：
- ✅ 完全本地化，数据安全
- ✅ 不依赖外部服务
- ✅ 可以跑在云服务器上
- ✅ Mac/Linux用户也能用

**劣势**：
- ❌ 需要自己维护服务器
- ❌ 需要Windows机器运行QMT（或远程QMT Server）

---

### 方案二：聚宽模拟盘 + 远程QMT Server

**特点**：
- 策略在聚宽模拟盘实时运行
- 产生交易信号后调用QMT Server执行真实下单
- 信号和执行分离

**适用场景**：
- 策略已经在聚宽模拟盘跑了很久，验证过了
- 想用聚宽的数据和策略托管，但实盘用自己的券商
- 聚宽官方实盘太贵或有限制，想接自己的账户

**工作原理**：
```
┌─────────────────┐          ┌──────────────────┐
│   聚宽模拟盘      │  ──────▶ │  远程 QMT Server │
│  (策略实时运行 )  │   HTTP   │  (Windows + QMT) │
│  产生交易信号     │          │   执行真实下单     │
└─────────────────┘          └──────────────────┘
                                     │
                                     ▼
                              ┌─────────────────┐
                              │   券商真实账户    │
                              └─────────────────┘
```

**使用步骤**：
1. 在Windows机器上启动QMT Server
2. 把`bullet_trade_jq_remote_helper.py`上传到聚宽研究根目录
3. 在聚宽模拟盘策略中调用远程下单

**优势**：
- ✅ 策略托管在聚宽：7x24小时运行，不用自己维护服务器
- ✅ 下单走自己券商：佣金更低，资金在自己账户
- ✅ 信号和执行分离：聚宽产生信号，QMT执行交易
- ✅ 双重记录：聚宽模拟盘记录一份，真实账户执行一份

**劣势**：
- ❌ 依赖聚宽服务
- ❌ 需要网络连接
- ❌ 需要Windows机器运行QMT Server

---

### 方案对比总结

| 特性 | 独立实盘 | 聚宽模拟盘+QMT |
|------|---------|---------------|
| **策略运行位置** | 本地 | 聚宽服务器 |
| **数据来源** | 本地数据源 | 聚宽数据 |
| **下单通道** | QMT | QMT |
| **服务器维护** | 需要 | 不需要（聚宽托管） |
| **网络依赖** | 可选（远程QMT） | 必须 |
| **适用系统** | Windows/Mac/Linux | 任意（策略在聚宽） |
| **数据安全** | 完全本地 | 依赖聚宽 |
| **成本** | 免费（除数据源） | 聚宽模拟盘免费 |

### 选择建议

**选择独立实盘，如果**：
- 想要完全本地化运行
- 不想依赖任何外部服务
- 需要完全控制策略执行
- 有Windows机器或可以部署远程QMT Server

**选择聚宽模拟盘+QMT，如果**：
- 策略已经在聚宽模拟盘验证过
- 想用聚宽的数据和策略托管
- 不想自己维护服务器
- 聚宽官方实盘太贵或有限制""",
            "type": "reference",
            "tags": ["BulletTrade", "实盘交易", "QMT", "聚宽", "方案对比", "策略执行"],
            "source": "BulletTrade官方文档"
        },
        {
            "title": "BulletTrade数据源配置指南",
            "content": """## BulletTrade数据源配置指南

### 支持的数据源

#### 1. MiniQMT（推荐）
**特点**：
- QMT客户端自带
- 开通券商账户即可免费使用
- 数据质量好
- 支持实时行情

**配置**：
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=qmt
```

**适用场景**：
- 已有QMT券商账户
- 需要实时行情
- 想要免费数据源

---

#### 2. TuShare
**特点**：
- 注册即可用
- 部分高级数据需要积分
- 数据更新及时

**配置**：
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=tushare
TUSHARE_TOKEN=你的token
```

**获取Token**：
1. 访问 https://tushare.pro/
2. 注册账号
3. 获取token

**适用场景**：
- 没有QMT账户
- 需要免费数据源
- 不需要实时行情

---

#### 3. JQData（聚宽数据）
**特点**：
- 聚宽官方数据
- 数据质量最好
- 需要付费账号

**配置**：
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=jqdata
JQDATA_USER=你的账号
JQDATA_PASSWORD=你的密码
```

**适用场景**：
- 已有聚宽账号
- 需要高质量数据
- 愿意付费

---

#### 4. 模拟数据（Simulator）
**特点**：
- 用于测试和体验
- 不需要真实数据源
- 数据是模拟生成的

**配置**：
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=simulator
```

**适用场景**：
- 初次体验BulletTrade
- 测试策略框架
- 不需要真实数据

---

### 数据源对比

| 数据源 | 费用 | 数据质量 | 实时行情 | 适用场景 |
|--------|------|---------|---------|---------|
| **MiniQMT** | 免费 | 高 | ✅ 支持 | 推荐，已有QMT账户 |
| **TuShare** | 免费/积分 | 中 | ❌ 不支持 | 没有QMT账户 |
| **JQData** | 付费 | 最高 | ✅ 支持 | 需要高质量数据 |
| **Simulator** | 免费 | 模拟 | ❌ 不支持 | 测试体验 |

### 配置示例

**完整.env配置**：
```bash
# 数据源选择
DEFAULT_DATA_PROVIDER=qmt

# TuShare配置（如果使用TuShare）
# TUSHARE_TOKEN=your_token_here

# JQData配置（如果使用JQData）
# JQDATA_USER=your_username
# JQDATA_PASSWORD=your_password

# 其他配置
CACHE_DIR=./cache
LOG_LEVEL=INFO
```

### 数据缓存
BulletTrade自动缓存历史数据，重复回测更快：
- 缓存目录：`./cache`（可配置）
- 自动更新：数据过期自动更新
- 手动清理：删除缓存目录即可

### 切换数据源
切换数据源只需修改`.env`文件中的`DEFAULT_DATA_PROVIDER`，无需修改策略代码。

### 注意事项
- 不同数据源的数据格式可能略有差异
- 建议先用模拟数据测试策略框架
- 实盘前务必验证数据源的准确性
- 数据源需要单独申请和配置""",
            "type": "reference",
            "tags": ["BulletTrade", "数据源", "配置", "MiniQMT", "TuShare", "JQData"],
            "source": "BulletTrade官方文档"
        },
        {
            "title": "BulletTrade Tick实时行情使用指南",
            "content": """## BulletTrade Tick实时行情使用指南

### 功能简介
BulletTrade支持tick级别的实时行情订阅，特别适合打板、抢涨停等需要实时行情的场景。

### 核心特点
- ⚡ **毫秒级延迟**：基于QMT的xtdata实时推送
- 📊 **盘口深度**：买一卖一价格和挂单量
- 🌐 **全市场订阅**：`subscribe(['SH', 'SZ'], 'tick')` 扫描全市场
- 🎯 **打板场景**：实时监控封单量变化，判断涨停板强度

### 基本使用

#### 1. 订阅Tick数据
```python
def initialize(context):
    g.watch_list = ['000001.XSHE', '000002.XSHE']
    g.limit_up = {}  # 缓存涨停价
    
    # 订阅 tick 数据
    subscribe(g.watch_list, 'tick')
```

#### 2. 获取涨停价
```python
def before_trading_start(context):
    # 开盘前获取涨停价，写入全局变量
    for code in g.watch_list:
        data = get_current_data()[code]
        g.limit_up[code] = data.high_limit  # 涨停价
```

#### 3. 处理Tick数据
```python
def handle_tick(context, tick):
    # 实时处理每一笔 tick
    code = tick['sid']
    price = tick['last_price']
    bid1_vol = tick.get('bid1_volume', 0)  # 买一量（封单量）
    
    # 判断涨停 + 封单量
    limit_up = g.limit_up.get(code)
    if limit_up and price >= limit_up and bid1_vol > 100000:
        print(f"{code} 涨停封单！封单量: {bid1_vol}")
```

### Tick数据结构

**tick对象包含的字段**：
- `sid`: 股票代码
- `last_price`: 最新价
- `bid1_price`: 买一价
- `bid1_volume`: 买一量（封单量）
- `ask1_price`: 卖一价
- `ask1_volume`: 卖一量
- `volume`: 成交量
- `amount`: 成交额
- `time`: 时间戳

### 打板场景应用

#### 场景1：监控涨停封单量
```python
def handle_tick(context, tick):
    code = tick['sid']
    price = tick['last_price']
    bid1_vol = tick.get('bid1_volume', 0)
    limit_up = g.limit_up.get(code)
    
    # 涨停且封单量>100万
    if limit_up and price >= limit_up and bid1_vol > 100000:
        print(f"{code} 涨停封单！封单量: {bid1_vol}")
        # 可以在这里执行买入逻辑
```

#### 场景2：监控涨停打开
```python
def handle_tick(context, tick):
    code = tick['sid']
    price = tick['last_price']
    bid1_vol = tick.get('bid1_volume', 0)
    limit_up = g.limit_up.get(code)
    
    # 之前涨停，现在打开
    if limit_up and price < limit_up and bid1_vol < 50000:
        print(f"{code} 涨停打开！当前价: {price}, 封单量: {bid1_vol}")
        # 可以在这里执行卖出逻辑
```

#### 场景3：全市场扫描涨停
```python
def initialize(context):
    # 订阅全市场
    subscribe(['SH', 'SZ'], 'tick')
    g.limit_up_stocks = {}  # 记录涨停股票

def handle_tick(context, tick):
    code = tick['sid']
    price = tick['last_price']
    bid1_vol = tick.get('bid1_volume', 0)
    
    # 获取涨停价（需要提前获取）
    data = get_current_data()[code]
    limit_up = data.high_limit
    
    # 涨停判断
    if limit_up and price >= limit_up and bid1_vol > 100000:
        if code not in g.limit_up_stocks:
            g.limit_up_stocks[code] = {
                'time': tick['time'],
                'bid1_vol': bid1_vol
            }
            print(f"发现涨停: {code}, 封单量: {bid1_vol}")
```

### 注意事项
- Tick数据需要QMT数据源支持
- 全市场订阅可能产生大量数据，注意性能
- 封单量判断需要结合市场状态
- 打板策略风险较高，需要严格风控

### 适用场景
- ✅ 打板策略：实时监控涨停封单量
- ✅ 抢涨停：抓住涨停打开瞬间
- ✅ 盘口分析：分析买卖盘强度
- ✅ 高频策略：需要实时行情的高频交易

### 性能优化
- 只订阅需要的股票，不要全市场订阅
- 使用缓存减少重复计算
- 合理设置处理逻辑，避免阻塞""",
            "type": "reference",
            "tags": ["BulletTrade", "Tick行情", "实时行情", "打板", "QMT", "盘口数据"],
            "source": "BulletTrade官方文档"
        }
    ]
    
    print(f"📝 准备添加 {len(bullettrade_knowledge)} 条BulletTrade知识...")
    print()
    
    success_count = 0
    for i, kb_item in enumerate(bullettrade_knowledge, 1):
        print(f"[{i}/{len(bullettrade_knowledge)}] 添加: {kb_item['title']}")
        try:
            result = knowledge_add(
                title=kb_item['title'],
                content=kb_item['content'],
                type=kb_item['type'],
                tags=kb_item['tags'],
                source=kb_item.get('source', 'BulletTrade知识补充')
            )
            
            if result.get('success') or result.get('knowledge_id'):
                print(f"    ✅ 成功 (ID: {result.get('knowledge_id', 'N/A')})")
                success_count += 1
            else:
                print(f"    ❌ 失败: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
        print()
    
    print("=" * 70)
    print(f"📊 补充完成: {success_count}/{len(bullettrade_knowledge)} 条成功")
    print("=" * 70)
    
    return success_count


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 补充BulletTrade知识")
    print("=" * 70)
    print()
    
    success_count = supplement_bullettrade_knowledge()
    
    print()
    print("=" * 70)
    if success_count > 0:
        print(f"✅ BulletTrade知识补充成功！")
        print(f"   成功添加 {success_count} 条知识")
        print()
        print("📋 知识内容:")
        print("   - BulletTrade项目简介和核心功能")
        print("   - 实盘接入方案对比")
        print("   - 数据源配置指南")
        print("   - Tick实时行情使用指南")
    else:
        print("❌ BulletTrade知识补充失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
