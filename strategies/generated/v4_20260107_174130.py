# -*- coding: utf-8 -*-
"""
V4.0测试策略
=====================================

生成时间: 2026-01-07 17:41:30
平台: 聚宽(JoinQuant) / BulletTrade

策略说明:
---------
基于TRQuant Investment Advisor V4.0系统生成
- 使用XGBoost模型预测高收益股票
- 多因子综合评分
- 动态仓位管理和风险控制

V4.0配置:
---------
  model_path: models/xgb_high_return_v4.pkl
  lookback_days: 5
"""


def initialize(context):
    """
    策略初始化
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_order_cost(
        OrderCost(
            open_tax=0,              # 买入印花税（A股不收）
            close_tax=0.001,         # 卖出印花税0.1%
            open_commission=0.0003,  # 买入佣金0.03%
            close_commission=0.0003, # 卖出佣金0.03%
            min_commission=5         # 最小佣金5元
        ),
        type='stock'
    )
    
    # 真实价格模式
    set_option('use_real_price', True)
    
    # V4.0策略参数
    g.v4_config = {
        'min_probability': 0.5,
        'min_score': 60.0,
        'target_return': 0.1,
        'stop_loss': -0.05,
        'trailing_stop': 0.03,
        'max_holding_days': 5,
        'position_size': 0.1,
        'max_positions': 10,
        'max_industry_exposure': 0.3,
    }
    
    # 市场环境
    g.market_phase = 'neutral'
    g.position_multiplier = 1.0
    
    # 持仓管理
    g.positions = {}  # {code: {'entry_date': str, 'entry_price': float, 'target_price': float, 'stop_loss_price': float}}
    g.last_rebalance_date = None
    g.rebalance_days = 5  # 每5个交易日调仓一次
    
    # 定时任务
    run_daily(before_trading_start, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_trading_end, time='15:30')


def before_trading_start(context):
    """
    盘前准备 - 获取V4.0预测信号
    
    注意：这里需要从外部数据源获取V4.0系统的预测信号
    可以通过以下方式：
    1. 从文件读取（推荐）
    2. 从API获取
    3. 从数据库读取
    """
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # TODO: 从外部数据源加载V4.0预测信号
    # 示例：从文件读取
    # import json
    # with open('v4_signals.json', 'r') as f:
    #     all_signals = json.load(f)
    # g.today_signals = all_signals.get(current_date, [])
    
    g.today_signals = []  # 默认空信号
    
    if g.today_signals:
        log.info(f"{current_date} V4.0预测信号: {len(g.today_signals)} 个")


def market_open(context):
    """
    盘中交易 - 根据V4.0预测信号执行交易
    """
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # 检查是否调仓日
    if g.last_rebalance_date is None:
        should_rebalance = True
    else:
        last_date = pd.to_datetime(g.last_rebalance_date)
        days_diff = (context.current_dt - last_date).days
        should_rebalance = (days_diff >= g.rebalance_days)
    
    if not should_rebalance:
        return
    
    # 更新持仓价格和检查出场条件
    update_positions(context)
    
    # 检查出场条件
    check_exit_conditions(context)
    
    # 执行新信号（买入）
    if g.today_signals:
        execute_entry_signals(context, g.today_signals)
    
    g.last_rebalance_date = current_date


def after_trading_end(context):
    """
    盘后处理 - 记录日志和更新状态
    """
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # 计算组合价值
    total_value = context.portfolio.total_value
    cash = context.portfolio.available_cash
    positions_value = total_value - cash
    
    # 记录日志
    log.info(f"{current_date} 组合价值: {total_value:.2f}, 持仓: {positions_value:.2f}, 现金: {cash:.2f}")
    log.info(f"{current_date} 持仓数量: {len(context.portfolio.positions)}")
    
    # 更新市场环境（可选）
    # g.market_phase = update_market_phase(context)


# ==================== 辅助函数 ====================

def update_positions(context):
    """更新持仓信息"""
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    for code, pos_info in g.positions.items():
        if code in context.portfolio.positions:
            pos = context.portfolio.positions[code]
            current_price = get_current_data()[code].last_price
            
            # 更新最高价（用于移动止盈）
            if 'highest_price' not in pos_info:
                pos_info['highest_price'] = current_price
            else:
                pos_info['highest_price'] = max(pos_info['highest_price'], current_price)
            
            pos_info['current_price'] = current_price
            pos_info['holding_days'] = (pd.to_datetime(current_date) - pd.to_datetime(pos_info['entry_date'])).days


def check_exit_conditions(context):
    """检查出场条件"""
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    for code in list(g.positions.keys()):
        if code not in context.portfolio.positions:
            # 已平仓，移除记录
            del g.positions[code]
            continue
        
        pos_info = g.positions[code]
        current_price = pos_info.get('current_price', 0)
        entry_price = pos_info['entry_price']
        target_price = pos_info['target_price']
        stop_loss_price = pos_info['stop_loss_price']
        highest_price = pos_info.get('highest_price', entry_price)
        holding_days = pos_info.get('holding_days', 0)
        
        # 计算收益率
        return_pct = (current_price / entry_price - 1) if entry_price > 0 else 0
        
        # 计算移动止盈价格
        trailing_stop_price = highest_price * (1 - g.v4_config['trailing_stop'])
        
        # 检查出场条件
        should_exit = False
        exit_reason = ""
        
        # 1. 目标止盈
        if current_price >= target_price:
            should_exit = True
            exit_reason = "目标止盈"
        
        # 2. 移动止盈（回撤）
        elif current_price <= trailing_stop_price and return_pct > 0:
            should_exit = True
            exit_reason = "移动止盈"
        
        # 3. 固定止损
        elif current_price <= stop_loss_price:
            should_exit = True
            exit_reason = "固定止损"
        
        # 4. 时间止损
        elif holding_days >= g.v4_config['max_holding_days']:
            should_exit = True
            exit_reason = "时间止损"
        
        if should_exit:
            order_target(code, 0)
            log.info(f"{current_date} 卖出 {code}: {exit_reason}, 收益率: {return_pct:.2%}")
            del g.positions[code]


def execute_entry_signals(context, signals: List[Dict]):
    """执行买入信号"""
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # 过滤信号
    valid_signals = []
    for signal in signals:
        code = signal['code']
        probability = signal.get('probability', 0)
        score = signal.get('score', 0)
        
        # 检查基本条件
        if probability < g.v4_config['min_probability']:
            continue
        if score < g.v4_config['min_score']:
            continue
        
        # 检查是否已持仓
        if code in context.portfolio.positions:
            continue
        
        # 检查持仓数量限制
        if len(context.portfolio.positions) >= g.v4_config['max_positions']:
            break
        
        valid_signals.append(signal)
    
    # 按概率排序
    valid_signals.sort(key=lambda x: x.get('probability', 0), reverse=True)
    
    # 计算总仓位（考虑市场环境）
    total_value = context.portfolio.total_value
    available_cash = context.portfolio.available_cash
    max_position_value = total_value * g.position_multiplier * g.v4_config['position_size']
    
    # 执行买入
    for signal in valid_signals:
        code = signal['code']
        target_price = signal.get('entry_price', 0)
        position_size = signal.get('position_size', g.v4_config['position_size'])
        
        if target_price <= 0:
            continue
        
        # 计算目标持仓金额
        target_value = total_value * position_size * g.position_multiplier
        
        # 检查可用资金
        if target_value > available_cash:
            target_value = available_cash * 0.95  # 保留5%现金
        
        if target_value < 1000:  # 最小买入金额
            continue
        
        # 下单
        order_target_value(code, target_value)
        log.info(f"{current_date} 买入 {code}: {target_value:.2f}元, 预测概率: {signal.get('probability', 0):.2%}")
        
        # 记录持仓信息
        g.positions[code] = {
            'entry_date': current_date,
            'entry_price': target_price,
            'target_price': signal.get('target_price', target_price * (1 + g.v4_config['target_return'])),
            'stop_loss_price': signal.get('stop_loss_price', target_price * (1 + g.v4_config['stop_loss'])),
            'highest_price': target_price,
        }
        
        available_cash -= target_value
        
        # 检查持仓数量限制
        if len(context.portfolio.positions) >= g.v4_config['max_positions']:
            break

