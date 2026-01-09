# -*- coding: utf-8 -*-
"""
聚宽策略代码生成器
================
将V4.0投资推荐系统的预测信号转换为聚宽格式的策略代码

功能：
1. 生成标准的 initialize(), handle_data(), run_daily() 函数
2. 集成多因子计算逻辑
3. 集成交易策略（入场、出场、风控）
4. 支持BulletTrade和聚宽平台
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .trading_strategy import TradeSignal, TradingConfig

logger = logging.getLogger(__name__)


class JoinQuantStrategyGenerator:
    """聚宽策略代码生成器"""
    
    def __init__(self):
        """初始化生成器"""
        pass
    
    def generate_strategy_code(
        self,
        strategy_name: str = "V4.0多因子预测策略",
        v4_config: Dict[str, Any] = None,
        trading_config: TradingConfig = None,
        market_trend: Any = None,
        signals_by_date: Dict[str, List[TradeSignal]] = None
    ) -> str:
        """
        生成聚宽格式策略代码
        
        Args:
            strategy_name: 策略名称
            v4_config: V4.0系统配置
            trading_config: 交易配置
            market_trend: 市场趋势分析结果
            signals_by_date: 按日期分组的预测信号 {date: [TradeSignal, ...]}
        
        Returns:
            聚宽格式的策略代码字符串
        """
        v4_config = v4_config or {}
        trading_config = trading_config or TradingConfig()
        
        # 生成代码各部分
        header = self._generate_header(strategy_name, v4_config)
        initialize_code = self._generate_initialize(trading_config, market_trend)
        before_trading_code = self._generate_before_trading_start(signals_by_date)
        handle_data_code = self._generate_handle_data(trading_config)
        after_trading_code = self._generate_after_trading_end()
        helper_functions = self._generate_helper_functions(trading_config)
        
        # 组合完整代码
        full_code = f"""{header}

{initialize_code}

{before_trading_code}

{handle_data_code}

{after_trading_code}

{helper_functions}
"""
        return full_code
    
    def _generate_header(self, strategy_name: str, v4_config: Dict) -> str:
        """生成文件头部注释"""
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'''# -*- coding: utf-8 -*-
"""
{strategy_name}
=====================================

生成时间: {create_time}
平台: 聚宽(JoinQuant) / BulletTrade

策略说明:
---------
基于TRQuant Investment Advisor V4.0系统生成
- 使用XGBoost模型预测高收益股票
- 多因子综合评分
- 动态仓位管理和风险控制

V4.0配置:
---------
{self._format_config(v4_config)}
"""
'''
    
    def _format_config(self, config: Dict) -> str:
        """格式化配置为字符串"""
        if not config:
            return "  (使用默认配置)"
        lines = []
        for key, value in config.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines) if lines else "  (使用默认配置)"
    
    def _generate_initialize(self, trading_config: TradingConfig, market_trend: Any = None) -> str:
        """生成initialize函数"""
        benchmark = "000300.XSHG"  # 沪深300
        slippage = 0.002  # 0.2%滑点
        
        # 市场趋势判断（如果有）
        market_phase = "neutral"
        position_multiplier = 1.0
        if market_trend:
            market_phase = getattr(market_trend, 'market_phase', 'neutral')
            position_multiplier = getattr(market_trend, 'position_multiplier', 1.0)
        
        return f'''def initialize(context):
    """
    策略初始化
    """
    # 设置基准
    set_benchmark('{benchmark}')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage({slippage}))
    
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
    g.v4_config = {{
        'min_probability': {trading_config.min_probability},
        'min_score': {trading_config.min_score},
        'target_return': {trading_config.target_return},
        'stop_loss': {trading_config.stop_loss},
        'trailing_stop': {trading_config.trailing_stop},
        'max_holding_days': {trading_config.max_holding_days},
        'position_size': {trading_config.position_size},
        'max_positions': {trading_config.max_positions},
        'max_industry_exposure': {trading_config.max_industry_exposure},
    }}
    
    # 市场环境
    g.market_phase = '{market_phase}'
    g.position_multiplier = {position_multiplier}
    
    # 持仓管理
    g.positions = {{}}  # {{code: {{'entry_date': str, 'entry_price': float, 'target_price': float, 'stop_loss_price': float}}}}
    g.last_rebalance_date = None
    g.rebalance_days = 5  # 每5个交易日调仓一次
    
    # 定时任务
    run_daily(before_trading_start, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_trading_end, time='15:30')
'''
    
    def _generate_before_trading_start(self, signals_by_date: Dict[str, List[TradeSignal]] = None) -> str:
        """生成before_trading_start函数"""
        if signals_by_date:
            # 如果有预定义的信号，生成从字典读取的代码
            signals_dict_str = self._format_signals_dict(signals_by_date)
            return f'''def before_trading_start(context):
    """
    盘前准备 - 获取V4.0预测信号
    """
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    # V4.0预测信号（由系统预生成）
    # 格式: {{date: [{{'code': str, 'probability': float, 'score': float, 'entry_price': float, ...}}]}}
    g.v4_signals = {signals_dict_str}
    
    # 获取当日信号
    g.today_signals = g.v4_signals.get(current_date, [])
    
    if g.today_signals:
        log.info(f"{{current_date}} V4.0预测信号: {{len(g.today_signals)}} 个")
    else:
        log.info(f"{{current_date}} 无V4.0预测信号")
'''
        else:
            # 如果没有预定义信号，生成动态获取的代码（需要外部数据源）
            return '''def before_trading_start(context):
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
'''
    
    def _format_signals_dict(self, signals_by_date: Dict[str, List[TradeSignal]]) -> str:
        """格式化信号字典为Python代码字符串"""
        lines = ["{"]
        for date, signals in signals_by_date.items():
            signal_list = []
            for signal in signals:
                signal_dict = {
                    'code': signal.code,
                    'name': signal.name,
                    'probability': signal.probability,
                    'score': signal.score,
                    'entry_price': signal.entry_price,
                    'target_price': signal.target_price,
                    'stop_loss_price': signal.stop_loss_price,
                    'position_size': signal.position_size,
                }
                signal_list.append(signal_dict)
            lines.append(f"    '{date}': {signal_list},")
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_handle_data(self, trading_config: TradingConfig) -> str:
        """生成handle_data函数（盘中交易）"""
        return f'''def market_open(context):
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
'''
    
    def _generate_after_trading_end(self) -> str:
        """生成after_trading_end函数"""
        return '''def after_trading_end(context):
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
'''
    
    def _generate_helper_functions(self, trading_config: TradingConfig) -> str:
        """生成辅助函数"""
        return f'''# ==================== 辅助函数 ====================

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
            log.info(f"{{current_date}} 卖出 {{code}}: {{exit_reason}}, 收益率: {{return_pct:.2%}}")
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
        log.info(f"{{current_date}} 买入 {{code}}: {{target_value:.2f}}元, 预测概率: {{signal.get('probability', 0):.2%}}")
        
        # 记录持仓信息
        g.positions[code] = {{
            'entry_date': current_date,
            'entry_price': target_price,
            'target_price': signal.get('target_price', target_price * (1 + g.v4_config['target_return'])),
            'stop_loss_price': signal.get('stop_loss_price', target_price * (1 + g.v4_config['stop_loss'])),
            'highest_price': target_price,
        }}
        
        available_cash -= target_value
        
        # 检查持仓数量限制
        if len(context.portfolio.positions) >= g.v4_config['max_positions']:
            break
'''
    
    def export_to_file(self, code: str, output_path: str):
        """导出策略代码到文件"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(code, encoding='utf-8')
        logger.info(f"策略代码已导出: {output_path}")
    
    def generate_from_workflow(
        self,
        workflow,
        start_date: str,
        end_date: str,
        rebalance_freq: str = 'weekly'
    ) -> str:
        """
        从workflow生成策略代码
        
        这个方法会：
        1. 运行workflow获取预测信号
        2. 按日期组织信号
        3. 生成策略代码
        """
        # TODO: 实现从workflow获取信号的逻辑
        # 目前先返回基础模板
        return self.generate_strategy_code(
            strategy_name="V4.0多因子预测策略（从Workflow生成）",
            signals_by_date={}
        )
