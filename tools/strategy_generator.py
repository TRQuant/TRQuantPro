# -*- coding: utf-8 -*-
"""
策略代码生成器
==============
支持多平台的策略代码生成

支持的平台:
- ptrade: PTrade交易终端
- jqdata: 聚宽研究平台
- bullettrade: BulletTrade本地回测
- qmt: QMT量化交易
"""

from typing import Dict, List, Optional
from datetime import datetime


class StrategyGenerator:
    """策略代码生成器"""
    
    # 平台特定的代码模板
    PLATFORM_TEMPLATES = {
        'ptrade': {
            'header': '''# -*- coding: utf-8 -*-
"""
{strategy_name} - PTrade策略
由TRQuant自动生成 @ {timestamp}

策略风格: {style}
使用因子: {factors}
"""

''',
            'imports': '',  # PTrade API是内置的
            'set_slippage': 'set_slippage(FixedSlippage({slippage}))',
            'set_commission': 'set_commission(PerTrade(buy_cost={commission}, sell_cost={sell_cost}, min_cost={min_commission}))',
            'get_history': "get_history({count}, '1d', {stocks}, ['close'], skip_paused=False, fq='pre')",
            'get_snapshot': 'get_snapshot({stocks})',
            'price_access': "prices['close']",
            'snapshot_price': 'snap.last_px',
            'snapshot_open': 'snap.open',
            'snapshot_high_limit': 'snap.up_limit',
            'snapshot_low_limit': 'snap.down_limit',
        },
        
        'jqdata': {
            'header': '''# -*- coding: utf-8 -*-
"""
{strategy_name} - 聚宽策略
由TRQuant自动生成 @ {timestamp}

策略风格: {style}
使用因子: {factors}
"""

from jqdata import *

''',
            'imports': 'from jqdata import *',
            'set_slippage': 'set_slippage(FixedSlippage({slippage}))',
            'set_commission': 'set_commission(PerTrade(buy_cost={commission}, sell_cost={sell_cost}, min_cost={min_commission}))',
            'get_history': "get_price({stocks}, end_date=context.current_dt.strftime('%Y-%m-%d'), frequency='daily', fields=['close'], count={count}, panel=False)",
            'get_snapshot': 'get_current_data()',
            'price_access': "prices.pivot(index='time', columns='code', values='close')",
            'snapshot_price': 'data.last_price',
            'snapshot_open': 'data.day_open',
            'snapshot_high_limit': 'data.high_limit',
            'snapshot_low_limit': 'data.low_limit',
        },
        
        'bullettrade': {
            'header': '''# -*- coding: utf-8 -*-
"""
{strategy_name} - BulletTrade策略
由TRQuant自动生成 @ {timestamp}

策略风格: {style}
使用因子: {factors}
"""

from jqdata import *
import pandas as pd

''',
            'imports': 'from jqdata import *\nimport pandas as pd',
            'set_slippage': 'set_slippage(FixedSlippage({slippage}))',
            'set_commission': 'set_commission(PerTrade(buy_cost={commission}, sell_cost={sell_cost}, min_cost={min_commission}))',
            'get_history': "get_price({stocks}, end_date=context.current_dt.strftime('%Y-%m-%d'), frequency='daily', fields=['close'], count={count}, panel=False)",
            'get_snapshot': 'get_current_data()',
            'price_access': "prices.pivot(index='time', columns='code', values='close') if 'time' in prices.columns else prices",
            'snapshot_price': 'data.last_price',
            'snapshot_open': "getattr(data, 'open', data.day_open if hasattr(data, 'day_open') else None)",
            'snapshot_high_limit': 'data.high_limit',
            'snapshot_low_limit': 'data.low_limit',
        },
        
        'qmt': {
            'header': '''# -*- coding: utf-8 -*-
"""
{strategy_name} - QMT策略
由TRQuant自动生成 @ {timestamp}

策略风格: {style}
使用因子: {factors}
"""

from xtquant import xtdata

''',
            'imports': 'from xtquant import xtdata',
            'set_slippage': '# QMT滑点在账户设置中配置',
            'set_commission': '# QMT佣金在账户设置中配置',
            'get_history': "xtdata.get_market_data(['close'], {stocks}, period='1d', count={count})",
            'get_snapshot': "xtdata.get_full_tick({stocks})",
            'price_access': "prices['close']",
            'snapshot_price': 'tick.lastPrice',
            'snapshot_open': 'tick.open',
            'snapshot_high_limit': 'tick.upperLimit',
            'snapshot_low_limit': 'tick.lowerLimit',
        },
    }
    
    # 策略风格模板
    STYLE_CONFIGS = {
        'multi_factor': {
            'name': '多因子',
            'description': '基于多因子加权的选股策略',
            'momentum_weight': 0.3,
            'value_weight': 0.3,
            'quality_weight': 0.4,
        },
        'momentum_growth': {
            'name': '动量成长',
            'description': '基于价格动量的追涨策略',
            'momentum_weight': 0.7,
            'value_weight': 0.1,
            'quality_weight': 0.2,
        },
        'value': {
            'name': '价值',
            'description': '基于估值指标的价值投资策略',
            'momentum_weight': 0.2,
            'value_weight': 0.6,
            'quality_weight': 0.2,
        },
        'market_neutral': {
            'name': '市场中性',
            'description': '对冲市场风险的中性策略',
            'momentum_weight': 0.33,
            'value_weight': 0.33,
            'quality_weight': 0.34,
        },
    }
    
    def __init__(self):
        self.template_cache = {}
    
    def generate(
        self,
        platform: str = 'ptrade',
        style: str = 'multi_factor',
        factors: List[str] = None,
        risk_params: Dict = None,
        strategy_name: str = None,
    ) -> Dict:
        """
        生成策略代码
        
        Args:
            platform: 目标平台 (ptrade/jqdata/bullettrade/qmt)
            style: 策略风格 (multi_factor/momentum_growth/value/market_neutral)
            factors: 使用的因子列表
            risk_params: 风险参数
            strategy_name: 策略名称
            
        Returns:
            生成结果字典
        """
        if platform not in self.PLATFORM_TEMPLATES:
            return {
                'success': False,
                'error': f'不支持的平台: {platform}，支持的平台: {list(self.PLATFORM_TEMPLATES.keys())}'
            }
        
        if style not in self.STYLE_CONFIGS:
            style = 'multi_factor'
        
        factors = factors or ['momentum_20d', 'ROE_ttm']
        risk_params = risk_params or {}
        
        if not strategy_name:
            strategy_name = f"TRQuant_{style}_{platform}"
        
        # 获取平台模板
        tmpl = self.PLATFORM_TEMPLATES[platform]
        style_cfg = self.STYLE_CONFIGS[style]
        
        # 生成策略代码
        code = self._generate_code(
            platform=platform,
            tmpl=tmpl,
            style=style,
            style_cfg=style_cfg,
            factors=factors,
            risk_params=risk_params,
            strategy_name=strategy_name,
        )
        
        return {
            'success': True,
            'code': code,
            'platform': platform,
            'style': style,
            'factors': factors,
            'strategy_name': strategy_name,
            'generated_at': datetime.now().isoformat(),
        }
    
    def _generate_code(
        self,
        platform: str,
        tmpl: Dict,
        style: str,
        style_cfg: Dict,
        factors: List[str],
        risk_params: Dict,
        strategy_name: str,
    ) -> str:
        """生成策略代码"""
        
        # 风险参数
        max_position = risk_params.get('max_position', 0.1)
        stop_loss = risk_params.get('stop_loss', 0.08)
        take_profit = risk_params.get('take_profit', 0.20)
        max_stocks = risk_params.get('max_stocks', 5)
        slippage = risk_params.get('slippage', 0.001)
        commission = risk_params.get('commission', 0.0003)
        min_commission = risk_params.get('min_commission', 5)
        
        # 头部
        header = tmpl['header'].format(
            strategy_name=strategy_name,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            style=style_cfg['name'],
            factors=', '.join(factors),
        )
        
        # 策略参数部分
        params_section = f'''
# ==================== 策略参数 ====================
MAX_STOCKS = {max_stocks}              # 最大持股数量
SINGLE_POSITION = {max_position}       # 单票最大仓位
MIN_CASH_RATIO = 0.10                  # 最低现金保留

REBALANCE_DAYS = 5                     # 调仓周期
MOMENTUM_SHORT = 5                     # 短期动量
MOMENTUM_LONG = 20                     # 长期动量

STOP_LOSS = -{stop_loss}               # 止损线
TAKE_PROFIT = {take_profit}            # 止盈线

BENCHMARK = '000300.XSHG'              # 基准指数
FACTORS = {factors}                    # 使用因子

'''
        
        # 初始化函数
        # sell_cost = 佣金 + 印花税(0.001)
        sell_cost = commission + 0.001
        init_section = self._generate_initialize(platform, tmpl, slippage, commission, sell_cost, min_commission)
        
        # 核心函数
        core_section = self._generate_core_functions(platform, tmpl, style_cfg)
        
        # 辅助函数
        helper_section = self._generate_helper_functions(platform, tmpl)
        
        return header + params_section + init_section + core_section + helper_section
    
    def _generate_initialize(self, platform: str, tmpl: Dict, slippage: float, commission: float, sell_cost: float, min_commission: int) -> str:
        """生成初始化函数"""
        
        slippage_code = tmpl['set_slippage'].format(slippage=slippage)
        # 对于PTrade和BulletTrade，sell_cost包含佣金+印花税
        commission_code = tmpl['set_commission'].format(
            commission=commission, 
            sell_cost=sell_cost,
            min_commission=min_commission
        )
        
        return f'''
# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    set_benchmark(BENCHMARK)
    {slippage_code}
    {commission_code}
    
    g.trade_count = 0
    g.stock_pool = []
    g.cost_prices = {{}}
    g.highest_prices = {{}}
    
    run_daily(before_market_open, '09:00')
    run_daily(market_open, '09:35')
    run_daily(check_risk, '14:50')
    run_daily(after_market_close, '15:30')
    
    log.info('=' * 50)
    log.info(f'策略初始化: {{BENCHMARK}}')
    log.info(f'持股: {{MAX_STOCKS}}只 | 仓位: {{SINGLE_POSITION*100:.0f}}%')
    log.info('=' * 50)

'''
    
    def _generate_core_functions(self, platform: str, tmpl: Dict, style_cfg: Dict) -> str:
        """生成核心交易函数"""
        
        # 根据平台选择正确的数据获取代码
        get_history_code = tmpl['get_history'].replace('{count}', 'MOMENTUM_LONG + 5').replace('{stocks}', 'test_stocks')
        price_access = tmpl['price_access']
        
        return f'''
def before_market_open(context):
    """盘前准备"""
    g.trade_count += 1
    
    if g.trade_count % 20 == 1:
        try:
            g.stock_pool = get_index_stocks(BENCHMARK)
            log.info(f'[盘前] 股票池更新: {{len(g.stock_pool)}}只')
        except Exception as e:
            log.error(f'[盘前] 获取指数成分股失败: {{e}}')
            try:
                all_stocks = list(get_all_securities('stock').index)
                g.stock_pool = all_stocks[:300]
            except:
                g.stock_pool = []


def market_open(context):
    """开盘交易"""
    if g.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{{g.trade_count}}个交易日')
    
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warn('[调仓] 未选出股票')
        return
    
    log.info(f'[调仓] 目标股票: {{target_stocks}}')
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑"""
    stocks = g.stock_pool
    if not stocks:
        return []
    
    log.info(f'[选股] 开始选股，股票池: {{len(stocks)}}只')
    
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {{len(stocks)}}只')
    
    if len(stocks) == 0:
        return fallback_select(context)
    
    try:
        test_stocks = stocks[:30] if len(stocks) > 30 else stocks
        
        prices = {get_history_code}
        
        if prices is None:
            return fallback_select(context)
        
        close_df = {price_access}
        
        if close_df is None or close_df.empty:
            return fallback_select(context)
        
        # 计算动量
        mom_short = close_df.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = close_df.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 三级选股
        valid_strict = (mom_short > 0) & (mom_long > 0)
        score_strict = (mom_short * 0.5 + mom_long * 0.5).where(valid_strict).dropna()
        
        valid_loose = (mom_short > 0) | (mom_long > 0)
        score_loose = (mom_short * 0.5 + mom_long * 0.5).where(valid_loose).dropna()
        
        score_all = (mom_short * 0.5 + mom_long * 0.5).dropna()
        
        if len(score_strict) >= MAX_STOCKS:
            score = score_strict
        elif len(score_loose) >= MAX_STOCKS:
            score = score_loose
        elif len(score_all) > 0:
            score = score_all
        else:
            return fallback_select(context)
        
        selected = score.nlargest(MAX_STOCKS).index.tolist()
        log.info(f'[选股] 选股成功: {{len(selected)}}只')
        return selected
        
    except Exception as e:
        log.error(f'[选股] 异常: {{e}}')
        return fallback_select(context)


def fallback_select(context):
    """兜底选股"""
    stocks = g.stock_pool
    if not stocks:
        return []
    
    filtered = filter_stocks(context, stocks[:50])
    selected = filtered[:MAX_STOCKS]
    
    if selected:
        log.info(f'[选股] 兜底: {{selected}}')
    
    return selected


def rebalance(context, target_stocks):
    """调仓"""
    if not target_stocks:
        return
    
    current_stocks = set(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    # 卖出
    for stock in current_stocks - target_set:
        try:
            order_target_value(stock, 0)
            log.info(f'[卖出] {{stock}}')
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[卖出失败] {{stock}}: {{e}}')
    
    # 买入
    for stock in target_stocks:
        try:
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {{stock}} 目标:{{target_value:.0f}}')
        except Exception as e:
            log.warn(f'[买入失败] {{stock}}: {{e}}')


def check_risk(context):
    """风控检查"""
    for stock in list(context.portfolio.positions.keys()):
        try:
            pos = context.portfolio.positions[stock]
            if pos.total_amount == 0:
                continue
            
            current_price = pos.price
            cost = g.cost_prices.get(stock, pos.avg_cost)
            highest = g.highest_prices.get(stock, cost)
            
            if cost <= 0:
                continue
            
            profit = (current_price - cost) / cost
            g.highest_prices[stock] = max(highest, current_price)
            
            if profit < STOP_LOSS:
                order_target_value(stock, 0)
                log.warn(f'[止损] {{stock}} {{profit*100:.1f}}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            elif profit > TAKE_PROFIT:
                order_target_value(stock, 0)
                log.info(f'[止盈] {{stock}} {{profit*100:.1f}}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            elif profit > 0.15:
                dd = (g.highest_prices[stock] - current_price) / g.highest_prices[stock]
                if dd > 0.10:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {{stock}}')
                    g.cost_prices.pop(stock, None)
                    g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[风控异常] {{stock}}: {{e}}')


def after_market_close(context):
    """收盘统计"""
    pos_count = len([p for p in context.portfolio.positions.values() if p.total_amount > 0])
    total = context.portfolio.total_value
    ret = context.portfolio.returns
    log.info(f'[收盘] 持仓:{{pos_count}}只 资产:{{total:.0f}} 收益:{{ret*100:.2f}}%')

'''
    
    def _generate_helper_functions(self, platform: str, tmpl: Dict) -> str:
        """生成辅助函数"""
        
        snapshot_code = tmpl['get_snapshot'].replace('{stocks}', 'stocks[:100]')
        
        return f'''
def filter_stocks(context, stocks):
    """过滤股票"""
    filtered = []
    
    try:
        snapshots = {snapshot_code}
    except:
        snapshots = {{}}
    
    for stock in stocks:
        try:
            # 排除ST
            try:
                info = get_instrument(stock) if 'ptrade' in '{platform}' else get_security_info(stock)
                if info and hasattr(info, 'name'):
                    if 'ST' in info.name or '*ST' in info.name:
                        continue
            except:
                pass
            
            filtered.append(stock)
        except:
            continue
    
    return filtered
'''


# 便捷函数
def generate_strategy(
    platform: str = 'ptrade',
    style: str = 'multi_factor',
    factors: List[str] = None,
    risk_params: Dict = None,
    strategy_name: str = None,
    output_path: str = None,
) -> Dict:
    """
    生成策略代码
    
    Args:
        platform: 目标平台
        style: 策略风格
        factors: 因子列表
        risk_params: 风险参数
        strategy_name: 策略名称
        output_path: 输出文件路径（可选）
        
    Returns:
        生成结果
    """
    generator = StrategyGenerator()
    result = generator.generate(
        platform=platform,
        style=style,
        factors=factors,
        risk_params=risk_params,
        strategy_name=strategy_name,
    )
    
    if result['success'] and output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['code'])
        result['output_file'] = output_path
    
    return result


if __name__ == '__main__':
    import sys
    
    platform = sys.argv[1] if len(sys.argv) > 1 else 'ptrade'
    style = sys.argv[2] if len(sys.argv) > 2 else 'momentum_growth'
    
    result = generate_strategy(
        platform=platform,
        style=style,
        factors=['momentum_20d', 'ROE_ttm'],
        risk_params={'max_stocks': 5, 'stop_loss': 0.08},
    )
    
    if result['success']:
        print(result['code'])
    else:
        print(f"Error: {result['error']}")
