#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
聚宽策略回测引擎知识库RAG构建脚本
================================
将聚宽策略回测API文档转换为RAG知识库条目，并构建向量索引
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

def create_joinquant_backtest_kb_items() -> List[Dict[str, Any]]:
    """
    创建聚宽策略回测引擎知识库条目
    
    基于已爬取的聚宽API文档和项目中的策略模板
    """
    kb_items = []
    
    # 1. 策略程序架构
    kb_items.append({
        "id": "jq_backtest_001",
        "title": "聚宽策略程序架构",
        "content": """聚宽策略程序架构

聚宽策略代码必须包含以下核心函数：

1. initialize(context) - 策略初始化函数
   - 在策略开始运行时调用一次
   - 用于设置策略参数、股票池、调仓频率等
   - 示例：
     def initialize(context):
         set_benchmark('000300.XSHG')
         set_slippage(PriceRelatedSlippage(0.002))
         set_order_cost(OrderCost(...))
         g.stock_pool = '000300.XSHG'
         g.hold_num = 30
         run_daily(before_trading_start, time='09:00')
         run_daily(handle_data, time='09:30')

2. before_trading_start(context) - 盘前准备函数
   - 每个交易日开盘前调用
   - 用于更新股票池、获取最新数据等

3. handle_data(context, data) - 盘中交易函数
   - 每个交易时间点调用（按分钟或按天）
   - 用于执行交易逻辑

4. after_trading_end(context) - 盘后处理函数
   - 每个交易日收盘后调用
   - 用于记录日志、更新状态等

全局变量对象：
- g: 全局变量对象，用于存储策略状态
- context: 策略上下文对象，包含账户信息、持仓信息等""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "策略架构", "initialize", "handle_data", "回测引擎", "API文档"],
        "source": "https://www.joinquant.com/help/api/help#api:策略程序架构♠",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 2. 策略设置函数
    kb_items.append({
        "id": "jq_backtest_002",
        "title": "聚宽策略设置函数 - initialize",
        "content": """聚宽策略设置函数 - initialize(context)

initialize(context) 是策略的初始化函数，在策略开始运行时调用一次。

核心设置函数：

1. set_benchmark(security) - 设置基准指数
   示例：set_benchmark('000300.XSHG')  # 沪深300

2. set_slippage(slippage) - 设置滑点
   示例：
   set_slippage(PriceRelatedSlippage(0.002))  # 价格相关滑点0.2%
   set_slippage(FixedSlippage(0.001))  # 固定滑点0.1%

3. set_order_cost(cost, type='stock') - 设置交易成本
   示例：
   set_order_cost(
       OrderCost(
           open_tax=0,              # 买入印花税
           close_tax=0.001,          # 卖出印花税0.1%
           open_commission=0.0003,   # 买入佣金0.03%
           close_commission=0.0003,  # 卖出佣金0.03%
           min_commission=5           # 最小佣金5元
       ),
       type='stock'
   )

4. set_option(name, value) - 设置策略选项
   常用选项：
   - set_option('use_real_price', True)  # 使用真实价格模式
   - set_option('order_volume_ratio', 0.25)  # 订单成交量比例

5. run_daily(func, time='09:30') - 设置定时运行函数
   示例：
   run_daily(before_trading_start, time='09:00')
   run_daily(handle_data, time='09:30')
   run_daily(after_trading_end, time='15:30')

全局变量初始化：
- g.params = {}  # 策略参数
- g.stock_pool = '000300.XSHG'  # 股票池
- g.hold_num = 30  # 持仓数量""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "initialize", "set_benchmark", "set_slippage", "set_order_cost", "run_daily", "策略设置"],
        "source": "https://www.joinquant.com/help/api/help#api:策略设置函数",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 3. 数据获取函数
    kb_items.append({
        "id": "jq_backtest_003",
        "title": "聚宽数据获取函数 - get_price, history, get_fundamentals",
        "content": """聚宽数据获取函数

1. get_price(security, start_date, end_date, frequency='daily', fields=[...])
   获取价格数据（移动窗口）
   示例：
   # 获取单只股票日线数据
   df = get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-12-31', 
                  frequency='daily', fields=['open', 'high', 'low', 'close', 'volume'])
   
   # 获取多只股票数据
   df = get_price(['000001.XSHE', '600519.XSHG'], count=60, 
                  frequency='daily', fields=['close'])
   
   参数说明：
   - security: 股票代码或代码列表
   - start_date/end_date: 开始/结束日期
   - count: 获取end_date之前N个周期的数据
   - frequency: 'daily'（日线）或'1m'（分钟线）
   - fields: ['open', 'high', 'low', 'close', 'volume', 'money']
   - fq: 'pre'（前复权，默认）/ 'post'（后复权）/ 'none'（不复权）

2. history(count, unit, field, security_list, df=True)
   获取历史数据（固定窗口）
   示例：
   # 获取过去20天的收盘价
   prices = history(20, '1d', 'close', g.stocks, df=True)
   
   # 计算20日收益率
   returns = (prices.iloc[-1] / prices.iloc[0] - 1)

3. get_fundamentals(query, date=None)
   获取财务数据
   示例：
   from jqlib.technical_analysis import *
   
   q = query(
       valuation.code,
       valuation.pe_ratio,
       valuation.pb_ratio,
       indicator.roe,
       indicator.gross_profit_margin
   ).filter(valuation.code.in_(g.stocks))
   
   df = get_fundamentals(q, date=context.current_dt.strftime('%Y-%m-%d'))

4. get_index_stocks(index_symbol)
   获取指数成分股
   示例：
   stocks = get_index_stocks('000300.XSHG')  # 沪深300成分股

5. get_current_data()
   获取当前时刻的实时数据
   示例：
   current_data = get_current_data()
   price = current_data['000001.XSHE'].last_price""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "get_price", "history", "get_fundamentals", "数据获取", "API"],
        "source": "https://www.joinquant.com/help/api/help#api:数据获取函数",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 4. 交易函数
    kb_items.append({
        "id": "jq_backtest_004",
        "title": "聚宽交易函数 - order_target, order_value, order_target_percent",
        "content": """聚宽交易函数

1. order_target(security, amount)
   目标持仓数量（股数）
   示例：
   order_target('000001.XSHE', 1000)  # 目标持仓1000股
   order_target('000001.XSHE', 0)  # 全部卖出

2. order_target_value(security, value)
   目标持仓金额（元）
   示例：
   order_target_value('000001.XSHE', 100000)  # 目标持仓10万元
   order_target_value('000001.XSHE', 0)  # 全部卖出

3. order_target_percent(security, percent)
   目标持仓百分比
   示例：
   order_target_percent('000001.XSHE', 0.1)  # 目标持仓10%
   order_target_percent('000001.XSHE', 0)  # 全部卖出

4. order_value(security, value)
   按金额买入
   示例：
   order_value('000001.XSHE', 50000)  # 买入5万元

5. order(security, amount)
   按股数买入/卖出
   示例：
   order('000001.XSHE', 100)  # 买入100股
   order('000001.XSHE', -100)  # 卖出100股

注意事项：
- 所有下单函数可以在 handle_data 和 run_daily 中使用
- 创建订单失败（返回None）的可能原因：
  * 股票停牌
  * 标的代码错误、已退市、未上市
  * 账户错误
  * 调整下单手数为0
  * 股票下空单等""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "order_target", "order_value", "order_target_percent", "交易函数", "下单"],
        "source": "https://www.joinquant.com/help/api/help#api:交易函数",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 5. 回测环境配置
    kb_items.append({
        "id": "jq_backtest_005",
        "title": "聚宽回测环境配置 - 滑点、手续费、真实价格",
        "content": """聚宽回测环境配置

1. 滑点设置
   set_slippage(PriceRelatedSlippage(0.002))  # 价格相关滑点0.2%
   set_slippage(FixedSlippage(0.001))  # 固定滑点0.1%

2. 手续费设置
   set_order_cost(
       OrderCost(
           open_tax=0,              # 买入印花税（A股买入不收）
           close_tax=0.001,          # 卖出印花税0.1%
           open_commission=0.0003,   # 买入佣金0.03%
           close_commission=0.0003,  # 卖出佣金0.03%
           min_commission=5          # 最小佣金5元
       ),
       type='stock'
   )

3. 真实价格模式
   set_option('use_real_price', True)  # 使用真实价格成交
   set_option('order_volume_ratio', 0.25)  # 订单成交量比例

4. 基准设置
   set_benchmark('000300.XSHG')  # 沪深300

5. 运行频率
   - 日级策略：使用 run_daily(func, time='09:30')
   - 分钟级策略：使用 handle_data(context, data)

注意事项：
- 每个交易日结束时自动撤销所有未完成订单（A股在17:00之后）
- 回测和模拟中，每日下单的最大数量为10000笔
- 所有价格单位是元
- 所有时间都是北京时间（UTC+8）""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "回测环境", "滑点", "手续费", "真实价格", "set_slippage", "set_order_cost"],
        "source": "https://www.joinquant.com/help/api/help#api:回测环境",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 6. 策略对象说明
    kb_items.append({
        "id": "jq_backtest_006",
        "title": "聚宽策略对象 - context, g, Portfolio, Position",
        "content": """聚宽策略对象说明

1. context对象（策略上下文）
   - context.current_dt: 当前时间（datetime对象）
   - context.portfolio: 账户组合对象
   - context.portfolio.total_value: 总资产
   - context.portfolio.available_cash: 可用现金
   - context.portfolio.positions: 持仓字典
   - context.portfolio.returns: 累计收益率

2. g对象（全局变量）
   - g.params: 策略参数字典
   - g.stock_pool: 股票池
   - g.hold_num: 持仓数量
   - g.trade_days: 交易日计数
   - g.cost_prices: 成本价字典
   - g.hold_days: 持仓天数字典

3. Portfolio对象（账户组合）
   - portfolio.total_value: 总资产
   - portfolio.available_cash: 可用现金
   - portfolio.positions: 持仓字典 {security: Position对象}
   - portfolio.returns: 累计收益率

4. Position对象（持仓）
   - position.total_amount: 总持仓数量
   - position.closeable_amount: 可卖出数量
   - position.value: 持仓市值
   - position.avg_cost: 平均成本

5. 获取持仓信息
   for stock in context.portfolio.positions:
       pos = context.portfolio.positions[stock]
       print(f"{stock}: {pos.total_amount}股, 市值: {pos.value}")

注意事项：
- Context, Portfolio, Position对象都是只读的，尝试修改会报错
- 使用g对象存储策略状态和自定义变量""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "context", "g对象", "Portfolio", "Position", "策略对象"],
        "source": "https://www.joinquant.com/help/api/help#api:对象♠",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 7. 完整策略模板
    kb_items.append({
        "id": "jq_backtest_007",
        "title": "聚宽多因子策略完整模板",
        "content": """聚宽多因子策略完整模板

# -*- coding: utf-8 -*-
\"\"\"
多因子量化策略 - 聚宽平台
\"\"\"

import pandas as pd
import numpy as np

def initialize(context):
    \"\"\"策略初始化\"\"\"
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点和手续费
    set_slippage(PriceRelatedSlippage(0.002))
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5
        ),
        type='stock'
    )
    
    # 真实价格模式
    set_option('use_real_price', True)
    
    # 策略参数
    g.stock_pool = '000300.XSHG'  # 股票池
    g.hold_num = 10  # 持仓数量
    g.rebalance_days = 20  # 调仓周期
    
    # 定时任务
    run_daily(before_trading_start, time='09:00')
    run_daily(market_open, time='09:30')

def before_trading_start(context):
    \"\"\"盘前准备\"\"\"
    # 获取股票池
    g.stocks = get_index_stocks(g.stock_pool)
    
    # 过滤ST和停牌股票
    g.paused_stocks = get_paused_stocks()
    g.st_stocks = get_st_stocks()

def market_open(context):
    \"\"\"盘中交易\"\"\"
    # 检查调仓日
    if context.current_dt.weekday() != 0:  # 只在周一调仓
        return
    
    # 多因子选股
    target_stocks = select_stocks(context)
    
    # 执行调仓
    rebalance(context, target_stocks)

def select_stocks(context):
    \"\"\"多因子选股\"\"\"
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # 获取财务数据
    q = query(
        valuation.code,
        valuation.pe_ratio,
        indicator.roe
    ).filter(valuation.code.in_(g.stocks))
    
    df = get_fundamentals(q, date=current_date)
    
    # 获取价格数据计算动量
    prices = history(20, '1d', 'close', g.stocks, df=True)
    returns = (prices.iloc[-1] / prices.iloc[0] - 1)
    
    # 计算综合得分
    df['momentum'] = returns
    df['score'] = df['roe'] * 0.5 - df['pe_ratio'] * 0.3 + df['momentum'] * 100 * 0.2
    
    # 选股
    target = df.nlargest(g.hold_num, 'score')['code'].tolist()
    return target

def rebalance(context, target_stocks):
    \"\"\"调仓\"\"\"
    # 卖出不在目标中的股票
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)
    
    # 等权重买入目标股票
    if target_stocks:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            if stock not in g.paused_stocks and stock not in g.st_stocks:
                order_target_percent(stock, weight)""",
        "type": "code_example",
        "tags": ["聚宽", "JoinQuant", "策略模板", "多因子策略", "完整示例", "代码模板"],
        "source": "extension/templates/strategies/multi_factor_template.py",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 8. 回测过程说明
    kb_items.append({
        "id": "jq_backtest_008",
        "title": "聚宽回测过程说明",
        "content": """聚宽回测过程说明

回测执行流程：

1. 初始化阶段
   - 执行 initialize(context) 函数
   - 设置基准、滑点、手续费等
   - 初始化全局变量

2. 每个交易日
   a) 盘前（09:00）
      - 执行 before_trading_start(context) 函数
      - 更新股票池、获取最新数据
   
   b) 盘中（09:30-15:00）
      - 执行 handle_data(context, data) 或 run_daily 注册的函数
      - 根据策略逻辑执行交易
   
   c) 盘后（15:30）
      - 执行 after_trading_end(context) 函数
      - 记录日志、更新状态

3. 订单处理
   - 系统自动处理订单成交
   - 考虑滑点、手续费
   - 检查停牌、涨跌停限制

4. 回测结果
   - 总收益率
   - 年化收益率
   - 最大回撤
   - 夏普比率
   - 胜率
   - 交易记录

注意事项：
- 回测使用历史数据，确保没有未来函数
- 注意数据更新时间（财务数据通常T+1更新）
- 考虑停牌、退市等特殊情况""",
        "type": "reference",
        "tags": ["聚宽", "JoinQuant", "回测过程", "回测流程", "回测说明"],
        "source": "https://www.joinquant.com/help/api/help#api:回测过程",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    # 9. V4.0系统集成说明
    kb_items.append({
        "id": "jq_backtest_009",
        "title": "V4.0系统生成聚宽策略代码指南",
        "content": """V4.0系统生成聚宽策略代码指南

V4.0投资推荐系统需要将预测信号转换为聚宽策略代码。

转换步骤：

1. 预测信号格式
   - 股票代码（聚宽格式：000001.XSHE）
   - 预测概率（XGBoost模型输出）
   - 目标买入价、止盈价、止损价

2. 生成initialize函数
   - 设置基准：set_benchmark('000300.XSHG')
   - 设置滑点：set_slippage(PriceRelatedSlippage(0.002))
   - 设置手续费：set_order_cost(...)
   - 初始化全局变量：g.predictions = {}

3. 生成before_trading_start函数
   - 从V4.0系统获取当日预测信号
   - 存储到g.predictions字典
   - 格式：g.predictions[stock_code] = {
       'proba': 0.85,
       'buy_price': 10.5,
       'target_profit': 11.55,
       'stop_loss': 9.98
   }

4. 生成handle_data函数
   - 检查调仓频率（如每周一次）
   - 遍历g.predictions，执行买入
   - 检查持仓，执行止盈止损

5. 生成风控函数
   - 移动止损逻辑
   - 最大持仓限制
   - 行业分散度控制

示例代码结构：
def initialize(context):
    # V4.0系统配置
    g.v4_config = {
        'prediction_threshold': 0.6,
        'max_positions': 10,
        'single_position_pct': 0.1
    }
    # ... 其他初始化

def before_trading_start(context):
    # 从V4.0系统获取预测（需要实现API调用或数据文件读取）
    g.predictions = load_v4_predictions(context.current_dt)

def market_open(context):
    # 执行交易逻辑
    execute_v4_signals(context)""",
        "type": "guide",
        "tags": ["V4.0", "聚宽", "策略生成", "代码转换", "系统集成", "TRQuant"],
        "source": "core/advisor_v4/joinquant_strategy_generator.py",
        "created_at": datetime.now().isoformat(),
        "useful_count": 0
    })
    
    return kb_items

def add_to_knowledge_base(kb_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """将知识库条目添加到RAG知识库"""
    try:
        from mcp_servers.unified_dev_server import knowledge_add
        
        results = {
            'success': 0,
            'failed': 0,
            'errors': [],
            'ids': []
        }
        
        for item in kb_items:
            try:
                result = knowledge_add(
                    title=item['title'],
                    content=item['content'],
                    type=item['type'],
                    tags=item['tags'],
                    source=item.get('source', '')
                )
                
                if result.get('success') or result.get('id') or result.get('knowledge_id'):
                    results['success'] += 1
                    results['ids'].append(result.get('id') or result.get('knowledge_id'))
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{item['title']}: {result.get('error', 'Unknown error')}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{item['title']}: {str(e)}")
        
        return results
        
    except ImportError as e:
        return {
            'success': False,
            'error': f'MCP工具不可用: {e}',
            'items': kb_items
        }

def build_vector_index(kb_items: List[Dict[str, Any]], force_rebuild: bool = False) -> Dict[str, Any]:
    """构建向量索引"""
    try:
        from mcp_servers.knowledge_vector_index import build_vector_index
        
        # 创建临时知识库JSON文件
        kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "joinquant_backtest_kb.json"
        kb_file.parent.mkdir(parents=True, exist_ok=True)
        
        kb_data = {
            "items": kb_items,
            "metadata": {
                "name": "聚宽策略回测引擎知识库",
                "description": "聚宽(JoinQuant)策略回测引擎API文档和最佳实践",
                "created_at": datetime.now().isoformat(),
                "source": "聚宽官方API文档 + V4.0系统集成"
            }
        }
        
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        
        # 构建向量索引
        result = build_vector_index(kb_file, force_rebuild=force_rebuild)
        return result
        
    except ImportError as e:
        return {
            'success': False,
            'error': f'向量索引模块不可用: {e}'
        }

def main():
    """主函数"""
    print("=" * 70)
    print("📚 聚宽策略回测引擎知识库RAG构建")
    print("=" * 70)
    
    # 1. 创建知识库条目
    print("\n📝 创建知识库条目...")
    kb_items = create_joinquant_backtest_kb_items()
    print(f"✅ 共创建 {len(kb_items)} 个知识库条目")
    
    # 2. 保存为JSON文件（备份）
    output_file = TRQUANT_ROOT / "docs" / "knowledge_base" / "joinquant_backtest_kb.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    kb_data = {
        "items": kb_items,
        "metadata": {
            "name": "聚宽策略回测引擎知识库",
            "description": "聚宽(JoinQuant)策略回测引擎API文档和最佳实践",
            "created_at": datetime.now().isoformat(),
            "source": "聚宽官方API文档 + V4.0系统集成",
            "total_items": len(kb_items)
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 知识库条目已保存: {output_file}")
    
    # 3. 添加到RAG知识库（使用MCP工具）
    print("\n💾 添加到RAG知识库...")
    add_result = add_to_knowledge_base(kb_items)
    if add_result.get('success') is not False:
        print(f"✅ 成功添加: {add_result.get('success', 0)} 个")
        if add_result.get('failed', 0) > 0:
            print(f"⚠️  失败: {add_result.get('failed', 0)} 个")
            for error in add_result.get('errors', [])[:5]:
                print(f"   - {error}")
    else:
        print(f"⚠️  MCP工具不可用，已保存JSON文件供手动导入")
    
    # 4. 构建向量索引
    print("\n🔍 构建向量索引...")
    index_result = build_vector_index(kb_items, force_rebuild=False)
    if index_result.get('success'):
        print(f"✅ 向量索引构建成功")
        print(f"   - 条目数: {index_result.get('items_count', 0)}")
        print(f"   - 模型: {index_result.get('model', '')}")
        print(f"   - 索引路径: {index_result.get('index_path', '')}")
    else:
        print(f"⚠️  向量索引构建失败: {index_result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 70)
    print("✅ 知识库构建完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
