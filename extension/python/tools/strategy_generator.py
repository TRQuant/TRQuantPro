# -*- coding: utf-8 -*-
"""
策略生成器
==========

支持生成PTrade和QMT两种平台的策略代码
"""

from datetime import datetime
from typing import Dict, List, Any


class StrategyGenerator:
    """策略代码生成器"""
    
    PLATFORMS = ['ptrade', 'qmt']
    STYLES = ['multi_factor', 'momentum_growth', 'value', 'market_neutral']
    
    def __init__(self):
        self.templates = {
            'ptrade': PTRADETemplate(),
            'qmt': QMTTemplate()
        }
    
    def generate(
        self,
        platform: str,
        style: str,
        factors: List[str],
        risk_params: Dict[str, Any],
        mainlines: List[str] = None
    ) -> Dict[str, Any]:
        """
        生成策略代码
        
        Args:
            platform: 平台 ('ptrade' 或 'qmt')
            style: 策略风格
            factors: 使用的因子列表
            risk_params: 风控参数
            mainlines: 投资主线（可选）
        
        Returns:
            包含代码和元信息的字典
        """
        if platform not in self.PLATFORMS:
            raise ValueError(f"不支持的平台: {platform}, 可选: {self.PLATFORMS}")
        
        if style not in self.STYLES:
            raise ValueError(f"不支持的风格: {style}, 可选: {self.STYLES}")
        
        template = self.templates[platform]
        
        code = template.generate(
            style=style,
            factors=factors,
            risk_params=risk_params,
            mainlines=mainlines
        )
        
        strategy_name = f"{style}_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            'code': code,
            'name': strategy_name,
            'platform': platform,
            'style': style,
            'factors': factors,
            'risk_params': risk_params,
            'description': self._generate_description(style, factors, platform)
        }
    
    def _generate_description(self, style: str, factors: List[str], platform: str) -> str:
        """生成策略描述"""
        style_names = {
            'multi_factor': '多因子选股',
            'momentum_growth': '动量成长',
            'value': '价值投资',
            'market_neutral': '市场中性'
        }
        return f"{style_names.get(style, style)}策略，使用{', '.join(factors)}等因子，适用于{platform.upper()}平台"


class PTRADETemplate:
    """PTrade策略模板"""
    
    def generate(
        self,
        style: str,
        factors: List[str],
        risk_params: Dict[str, Any],
        mainlines: List[str] = None
    ) -> str:
        """生成PTrade策略代码"""
        
        max_position = risk_params.get('max_position', 0.1)
        stop_loss = risk_params.get('stop_loss', 0.08)
        take_profit = risk_params.get('take_profit', 0.2)
        
        header = self._generate_header(style, factors, risk_params)
        initialize = self._generate_initialize(max_position, stop_loss, take_profit, factors)
        
        if style == 'multi_factor':
            handle_data = self._generate_multi_factor_logic(factors)
        elif style == 'momentum_growth':
            handle_data = self._generate_momentum_logic(factors)
        elif style == 'value':
            handle_data = self._generate_value_logic(factors)
        elif style == 'market_neutral':
            handle_data = self._generate_neutral_logic(factors)
        else:
            handle_data = self._generate_multi_factor_logic(factors)
        
        helper_functions = self._generate_helper_functions()
        
        return f"{header}\n\n{initialize}\n\n{handle_data}\n\n{helper_functions}"
    
    def _generate_header(self, style: str, factors: List[str], risk_params: Dict) -> str:
        return f'''# -*- coding: utf-8 -*-
"""
TRQuant自动生成策略 - PTrade版本
================================

策略风格: {style}
使用因子: {', '.join(factors)}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

风控参数:
- 单票最大仓位: {risk_params.get('max_position', 0.1)*100:.0f}%
- 止损线: {risk_params.get('stop_loss', 0.08)*100:.0f}%
- 止盈线: {risk_params.get('take_profit', 0.2)*100:.0f}%
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta'''

    def _generate_initialize(self, max_position: float, stop_loss: float, take_profit: float, factors: List[str]) -> str:
        return f'''
def initialize(context):
    """
    策略初始化
    设置参数、股票池、调仓频率
    """
    # 风控参数
    context.max_position = {max_position}      # 单票最大仓位
    context.stop_loss = {stop_loss}            # 止损线
    context.take_profit = {take_profit}        # 止盈线
    context.max_stocks = 10                    # 最大持仓数
    
    # 因子列表
    context.factors = {factors}
    
    # 股票池（沪深300成分股）
    context.universe = get_index_stocks('000300.XSHG')
    
    # 设置调仓时间
    run_daily(before_trading, time='09:00')
    run_daily(rebalance, time='09:35')
    run_daily(risk_control, time='14:50')
    
    # 初始化缓存
    context._cost_prices = {{}}  # 成本价记录
    context._holding_days = {{}}  # 持有天数
    
    log.info(f"策略初始化完成，股票池数量: {{len(context.universe)}}")


def before_trading(context):
    """
    每日开盘前运行
    更新股票池，剔除ST和停牌
    """
    # 获取最新成分股
    context.universe = get_index_stocks('000300.XSHG')
    
    # 剔除ST股票
    st_stocks = get_st_stocks()
    context.universe = [s for s in context.universe if s not in st_stocks]
    
    # 剔除停牌股票
    suspended = get_suspended_stocks(context.universe)
    context.universe = [s for s in context.universe if s not in suspended]
    
    log.info(f"今日可交易股票数: {{len(context.universe)}}")'''

    def _generate_multi_factor_logic(self, factors: List[str]) -> str:
        factor_code = ', '.join([f"'{f}'" for f in factors])
        return f'''
def rebalance(context):
    """
    调仓逻辑 - 多因子选股
    """
    # 获取因子数据
    factor_data = get_factor_values(
        context.universe,
        [{factor_code}],
        end_date=context.current_dt.strftime('%Y-%m-%d'),
        count=1
    )
    
    if factor_data is None or len(factor_data) == 0:
        log.warning("获取因子数据失败")
        return
    
    # 因子标准化
    scores = pd.DataFrame(index=context.universe)
    for factor in context.factors:
        if factor in factor_data:
            values = factor_data[factor].iloc[-1]
            # Z-score标准化
            scores[factor] = (values - values.mean()) / values.std()
    
    # 计算综合得分（等权）
    scores['composite'] = scores.mean(axis=1)
    
    # 排序选股
    scores = scores.dropna()
    selected = scores.nlargest(context.max_stocks, 'composite').index.tolist()
    
    log.info(f"本次选出股票: {{selected}}")
    
    # 执行调仓
    execute_rebalance(context, selected)


def execute_rebalance(context, selected):
    """
    执行调仓
    """
    current_holdings = list(context.portfolio.positions.keys())
    
    # 卖出不在选股列表中的股票
    for stock in current_holdings:
        if stock not in selected:
            order_target_percent(stock, 0)
            log.info(f"卖出: {{stock}}")
            if stock in context._cost_prices:
                del context._cost_prices[stock]
    
    # 买入新选出的股票
    if len(selected) > 0:
        target_weight = min(context.max_position, 1.0 / len(selected))
        for stock in selected:
            if stock not in current_holdings:
                order_target_percent(stock, target_weight)
                context._cost_prices[stock] = get_current_price(stock)
                log.info(f"买入: {{stock}}, 目标仓位: {{target_weight*100:.1f}}%")
            else:
                # 调整仓位
                order_target_percent(stock, target_weight)'''

    def _generate_momentum_logic(self, factors: List[str]) -> str:
        return f'''
def rebalance(context):
    """
    调仓逻辑 - 动量成长策略
    """
    # 获取价格数据计算动量
    prices = get_price(
        context.universe,
        end_date=context.current_dt,
        frequency='daily',
        fields=['close'],
        count=20
    )
    
    if prices is None:
        return
    
    # 计算20日动量
    momentum = (prices['close'].iloc[-1] / prices['close'].iloc[0] - 1)
    
    # 获取成长因子
    fundamentals = get_fundamentals(
        query(
            valuation.code,
            income.inc_revenue_year_on_year,
            income.inc_net_profit_year_on_year
        ).filter(
            valuation.code.in_(context.universe)
        )
    )
    
    # 计算综合得分
    scores = pd.DataFrame(index=context.universe)
    scores['momentum'] = momentum
    
    if fundamentals is not None:
        scores = scores.merge(
            fundamentals.set_index('code'),
            left_index=True, right_index=True, how='left'
        )
        scores['growth'] = (
            scores['inc_revenue_year_on_year'].fillna(0) * 0.5 +
            scores['inc_net_profit_year_on_year'].fillna(0) * 0.5
        )
    else:
        scores['growth'] = 0
    
    # 标准化并合成
    for col in ['momentum', 'growth']:
        if col in scores.columns:
            scores[col] = (scores[col] - scores[col].mean()) / scores[col].std()
    
    scores['composite'] = scores[['momentum', 'growth']].mean(axis=1)
    
    # 选股
    selected = scores.nlargest(context.max_stocks, 'composite').index.tolist()
    
    execute_rebalance(context, selected)'''

    def _generate_value_logic(self, factors: List[str]) -> str:
        return f'''
def rebalance(context):
    """
    调仓逻辑 - 价值投资策略
    """
    # 获取估值数据
    fundamentals = get_fundamentals(
        query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.inc_return  # 股息率
        ).filter(
            valuation.code.in_(context.universe),
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 50,  # 剔除高PE
            valuation.pb_ratio > 0,
            valuation.pb_ratio < 10   # 剔除高PB
        )
    )
    
    if fundamentals is None or len(fundamentals) == 0:
        log.warning("获取基本面数据失败")
        return
    
    scores = fundamentals.set_index('code')
    
    # 价值因子：低PE、低PB为好
    scores['pe_score'] = -scores['pe_ratio']
    scores['pb_score'] = -scores['pb_ratio']
    
    # 质量因子：高ROE为好
    scores['roe_score'] = scores['roe'].fillna(0)
    
    # 股息因子
    scores['dividend_score'] = scores['inc_return'].fillna(0)
    
    # 标准化
    for col in ['pe_score', 'pb_score', 'roe_score', 'dividend_score']:
        scores[col] = (scores[col] - scores[col].mean()) / scores[col].std()
    
    # 综合得分
    scores['composite'] = (
        scores['pe_score'] * 0.25 +
        scores['pb_score'] * 0.25 +
        scores['roe_score'] * 0.30 +
        scores['dividend_score'] * 0.20
    )
    
    selected = scores.nlargest(context.max_stocks, 'composite').index.tolist()
    
    execute_rebalance(context, selected)'''

    def _generate_neutral_logic(self, factors: List[str]) -> str:
        return f'''
def rebalance(context):
    """
    调仓逻辑 - 市场中性策略
    注意：需要融券支持
    """
    # 获取因子数据
    factor_data = get_factor_values(
        context.universe,
        {factors},
        end_date=context.current_dt.strftime('%Y-%m-%d'),
        count=1
    )
    
    if factor_data is None:
        return
    
    # 计算综合得分
    scores = pd.DataFrame(index=context.universe)
    for factor in context.factors:
        if factor in factor_data:
            values = factor_data[factor].iloc[-1]
            scores[factor] = (values - values.mean()) / values.std()
    
    scores['composite'] = scores.mean(axis=1)
    scores = scores.dropna()
    
    # 多头：得分最高的股票
    long_stocks = scores.nlargest(context.max_stocks // 2, 'composite').index.tolist()
    
    # 空头：得分最低的股票（需要融券）
    short_stocks = scores.nsmallest(context.max_stocks // 2, 'composite').index.tolist()
    
    log.info(f"多头: {{long_stocks}}")
    log.info(f"空头: {{short_stocks}}")
    
    # 执行多头
    long_weight = 0.5 / len(long_stocks) if long_stocks else 0
    for stock in long_stocks:
        order_target_percent(stock, long_weight)
    
    # 空头需要券商支持融券
    # 这里仅记录，实际执行需要配置融券账户
    log.info("空头部分需要融券支持")'''

    def _generate_helper_functions(self) -> str:
        return '''
def risk_control(context):
    """
    风控检查
    每日收盘前执行止损止盈
    """
    for stock, position in context.portfolio.positions.items():
        if stock not in context._cost_prices:
            context._cost_prices[stock] = position.avg_cost
        
        cost = context._cost_prices[stock]
        current = position.price
        pnl = (current - cost) / cost
        
        # 止损
        if pnl < -context.stop_loss:
            order_target_percent(stock, 0)
            log.warning(f"止损卖出 {stock}, 亏损: {pnl*100:.2f}%")
            del context._cost_prices[stock]
        
        # 止盈
        elif pnl > context.take_profit:
            order_target_percent(stock, 0)
            log.info(f"止盈卖出 {stock}, 盈利: {pnl*100:.2f}%")
            del context._cost_prices[stock]


def get_st_stocks():
    """获取ST股票列表"""
    try:
        df = get_extras('is_st', context.universe, count=1)
        return df.columns[df.iloc[0] == True].tolist()
    except:
        return []


def get_suspended_stocks(stocks):
    """获取停牌股票"""
    try:
        df = get_price(stocks, count=1, fields=['paused'])
        return df['paused'].columns[df['paused'].iloc[0] == True].tolist()
    except:
        return []


def get_current_price(stock):
    """获取当前价格"""
    try:
        return get_price(stock, count=1, fields=['close'])['close'].iloc[-1]
    except:
        return 0'''


class QMTTemplate:
    """QMT策略模板"""
    
    def generate(
        self,
        style: str,
        factors: List[str],
        risk_params: Dict[str, Any],
        mainlines: List[str] = None
    ) -> str:
        """生成QMT策略代码"""
        
        max_position = risk_params.get('max_position', 0.1)
        stop_loss = risk_params.get('stop_loss', 0.08)
        take_profit = risk_params.get('take_profit', 0.2)
        
        return f'''# -*- coding: utf-8 -*-
"""
TRQuant自动生成策略 - QMT版本
================================

策略风格: {style}
使用因子: {', '.join(factors)}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

风控参数:
- 单票最大仓位: {max_position*100:.0f}%
- 止损线: {stop_loss*100:.0f}%
- 止盈线: {take_profit*100:.0f}%

注意: QMT策略需要在迅投QMT客户端中运行
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def init(ContextInfo):
    """
    策略初始化
    QMT入口函数
    """
    # 风控参数
    ContextInfo.max_position = {max_position}
    ContextInfo.stop_loss = {stop_loss}
    ContextInfo.take_profit = {take_profit}
    ContextInfo.max_stocks = 10
    
    # 因子列表
    ContextInfo.factors = {factors}
    
    # 股票池
    ContextInfo.universe = ContextInfo.get_stock_list_in_sector('沪深300')
    
    # 设置账号
    ContextInfo.accID = 'your_account_id'
    
    # 设置定时任务
    ContextInfo.run_time('rebalance', '09:35:00', 'SH')
    ContextInfo.run_time('risk_control', '14:50:00', 'SH')
    
    # 初始化缓存
    ContextInfo.cost_prices = {{}}
    
    print(f"[init] 策略初始化完成，股票池: {{len(ContextInfo.universe)}}只")


def handlebar(ContextInfo):
    """
    每个bar调用
    QMT主循环函数
    """
    # 获取当前时间
    current_time = ContextInfo.get_bar_timetag(ContextInfo.barpos)
    
    # 这里可以添加实时监控逻辑
    pass


def rebalance(ContextInfo):
    """
    调仓逻辑
    """
    print(f"[rebalance] 开始调仓...")
    
    # 更新股票池
    ContextInfo.universe = ContextInfo.get_stock_list_in_sector('沪深300')
    
    # 剔除ST和停牌
    ContextInfo.universe = [s for s in ContextInfo.universe 
                           if not is_st(ContextInfo, s) 
                           and not is_suspended(ContextInfo, s)]
    
    # 获取因子数据并计算得分
    scores = calculate_factor_scores(ContextInfo)
    
    if scores is None or len(scores) == 0:
        print("[rebalance] 获取因子数据失败")
        return
    
    # 选股
    selected = scores.nlargest(ContextInfo.max_stocks, 'composite').index.tolist()
    print(f"[rebalance] 选出股票: {{selected}}")
    
    # 执行调仓
    execute_trades(ContextInfo, selected)


def calculate_factor_scores(ContextInfo):
    """
    计算因子得分
    """
    scores = pd.DataFrame(index=ContextInfo.universe)
    
    for stock in ContextInfo.universe:
        try:
            # 获取因子数据（根据实际数据源调整）
            for factor in ContextInfo.factors:
                value = get_factor_value(ContextInfo, stock, factor)
                if stock not in scores.index:
                    scores.loc[stock] = {{}}
                scores.loc[stock, factor] = value
        except Exception as e:
            print(f"[error] 获取{{stock}}因子失败: {{e}}")
    
    # 标准化
    for factor in ContextInfo.factors:
        if factor in scores.columns:
            col = scores[factor].astype(float)
            scores[factor] = (col - col.mean()) / col.std()
    
    # 综合得分
    scores['composite'] = scores[ContextInfo.factors].mean(axis=1)
    
    return scores.dropna()


def get_factor_value(ContextInfo, stock, factor):
    """
    获取单个因子值
    需要根据实际数据源实现
    """
    # 示例：获取PE
    if factor == 'pe_ttm':
        return ContextInfo.get_financial_data(['pe_ttm'], stock)[0]
    # 示例：获取ROE
    elif factor == 'roe_ttm':
        return ContextInfo.get_financial_data(['roe'], stock)[0]
    # 动量
    elif factor == 'momentum_20d':
        prices = ContextInfo.get_market_data(['close'], stock, count=20)
        if len(prices) > 0:
            return (prices[-1] / prices[0]) - 1
        return 0
    else:
        return 0


def execute_trades(ContextInfo, selected):
    """
    执行交易
    """
    # 获取当前持仓
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    current_holdings = [p.m_strInstrumentID for p in positions] if positions else []
    
    # 卖出不在列表中的
    for stock in current_holdings:
        if stock not in selected:
            sell_stock(ContextInfo, stock, 0)
            print(f"[sell] 卖出 {{stock}}")
    
    # 买入新股票
    if len(selected) > 0:
        target_weight = min(ContextInfo.max_position, 1.0 / len(selected))
        total_value = ContextInfo.get_total_asset(ContextInfo.accID)
        
        for stock in selected:
            target_value = total_value * target_weight
            buy_stock(ContextInfo, stock, target_value)
            print(f"[buy] 买入 {{stock}}, 目标金额: {{target_value:.0f}}")


def risk_control(ContextInfo):
    """
    风控检查
    """
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
    
    if not positions:
        return
    
    for pos in positions:
        stock = pos.m_strInstrumentID
        cost = pos.m_dOpenPrice
        current = ContextInfo.get_last_price(stock)
        
        if cost <= 0:
            continue
        
        pnl = (current - cost) / cost
        
        # 止损
        if pnl < -ContextInfo.stop_loss:
            sell_stock(ContextInfo, stock, 0)
            print(f"[止损] {{stock}} 亏损 {{pnl*100:.2f}}%")
        
        # 止盈
        elif pnl > ContextInfo.take_profit:
            sell_stock(ContextInfo, stock, 0)
            print(f"[止盈] {{stock}} 盈利 {{pnl*100:.2f}}%")


def buy_stock(ContextInfo, stock, value):
    """买入股票"""
    price = ContextInfo.get_last_price(stock)
    if price > 0:
        volume = int(value / price / 100) * 100  # 整手
        if volume > 0:
            order_id = ContextInfo.order_stock(
                ContextInfo.accID, stock, 
                volume, price, 'LATEST_PRICE', 'buy'
            )
            return order_id
    return None


def sell_stock(ContextInfo, stock, volume):
    """卖出股票"""
    if volume == 0:
        # 全部卖出
        positions = ContextInfo.get_trade_detail_data(ContextInfo.accID, 'stock', 'position')
        for pos in positions:
            if pos.m_strInstrumentID == stock:
                volume = pos.m_nVolume
                break
    
    if volume > 0:
        price = ContextInfo.get_last_price(stock)
        order_id = ContextInfo.order_stock(
            ContextInfo.accID, stock,
            volume, price, 'LATEST_PRICE', 'sell'
        )
        return order_id
    return None


def is_st(ContextInfo, stock):
    """判断是否ST"""
    try:
        name = ContextInfo.get_stock_name(stock)
        return 'ST' in name or '*ST' in name
    except:
        return False


def is_suspended(ContextInfo, stock):
    """判断是否停牌"""
    try:
        status = ContextInfo.get_instrument_status(stock)
        return status != 'NORMAL'
    except:
        return False
'''


# 单例生成器
_generator = None

def get_strategy_generator() -> StrategyGenerator:
    """获取策略生成器单例"""
    global _generator
    if _generator is None:
        _generator = StrategyGenerator()
    return _generator

