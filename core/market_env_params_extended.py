"""
市场环境扩展参数
==================

基于 market_env_identifier_v3.py 的结果，提供完整的下游操作参数。

核心设计：
1. 12种市场状态 → 12套完整参数
2. 包含仓位、风险、止盈止损、调仓、买卖条件等
3. 与v3核心模块配合使用

使用方法：
    from core.market_env_params_extended import get_extended_params
    from core.market_env_identifier_v3 import identify_market_env_v3
    
    result = identify_market_env_v3()
    params = get_extended_params(result.combined_environment)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# 导入市场环境枚举
try:
    from core.market_env_identifier_v3 import MarketEnvironment, MarketEnvResultV3
except ImportError:
    # 备用定义
    class MarketEnvironment(Enum):
        STRONG_BULL = "强势牛市"
        BULL = "牛市"
        WEAK_BULL = "弱势牛市"
        STRONG_BEAR = "强势熊市"
        BEAR = "熊市"
        WEAK_BEAR = "弱势熊市"
        HIGH_RANGE = "高位震荡"
        MID_RANGE = "中位震荡"
        LOW_RANGE = "低位震荡"
        RECOVERY = "复苏"
        DISTRIBUTION = "派发"
        NEUTRAL = "中性"


@dataclass
class EntryConditions:
    """买入条件"""
    ma_condition: str           # 均线条件
    momentum_condition: str     # 动量条件
    volume_condition: str       # 成交量条件
    rsi_range: tuple            # RSI范围
    macd_condition: str         # MACD条件
    description: str            # 条件说明
    
    def to_dict(self) -> dict:
        return {
            'ma_condition': self.ma_condition,
            'momentum_condition': self.momentum_condition,
            'volume_condition': self.volume_condition,
            'rsi_range': self.rsi_range,
            'macd_condition': self.macd_condition,
            'description': self.description
        }


@dataclass
class ExitConditions:
    """卖出条件"""
    stop_loss_type: str         # 止损类型：fixed/trailing/atr
    take_profit_type: str       # 止盈类型：fixed/trailing/target
    ma_break_condition: str     # 均线破位条件
    momentum_reversal: str      # 动量反转条件
    volume_divergence: str      # 量价背离条件
    description: str            # 条件说明
    
    def to_dict(self) -> dict:
        return {
            'stop_loss_type': self.stop_loss_type,
            'take_profit_type': self.take_profit_type,
            'ma_break_condition': self.ma_break_condition,
            'momentum_reversal': self.momentum_reversal,
            'volume_divergence': self.volume_divergence,
            'description': self.description
        }


@dataclass 
class ExtendedParams:
    """扩展参数"""
    # 基础信息
    environment: MarketEnvironment
    environment_name: str
    category: str               # bull/bear/range/turning
    
    # 仓位管理
    position_min: float         # 最低仓位
    position_max: float         # 最高仓位
    suggested_position: float   # 建议仓位
    single_stock_max: float     # 单股最大仓位
    
    # 风险控制
    risk_level: str             # low/medium/high
    stop_loss_pct: float        # 止损线
    take_profit_pct: float      # 止盈线
    trailing_stop_pct: float    # 移动止损
    drawdown_limit: float       # 最大回撤限制
    
    # 调仓设置
    rebalance_frequency: str    # daily/weekly/monthly/quarterly
    rebalance_threshold: float  # 触发调仓的偏离阈值
    
    # 选股标准
    max_holdings: int           # 最大持仓数量
    min_market_cap: float       # 最小市值（亿）
    liquidity_requirement: str  # 流动性要求
    
    # 买卖条件
    entry_conditions: EntryConditions
    exit_conditions: ExitConditions
    
    # 行业配置
    industry_preference: List[str]   # 偏好行业
    industry_avoid: List[str]        # 回避行业
    
    # 操作建议
    operation_advice: str       # 操作建议文字
    key_indicators: List[str]   # 关键关注指标
    
    def to_dict(self) -> dict:
        return {
            'environment': self.environment.name,
            'environment_name': self.environment_name,
            'category': self.category,
            'position': {
                'min': self.position_min,
                'max': self.position_max,
                'suggested': self.suggested_position,
                'single_stock_max': self.single_stock_max
            },
            'risk': {
                'level': self.risk_level,
                'stop_loss_pct': self.stop_loss_pct,
                'take_profit_pct': self.take_profit_pct,
                'trailing_stop_pct': self.trailing_stop_pct,
                'drawdown_limit': self.drawdown_limit
            },
            'rebalance': {
                'frequency': self.rebalance_frequency,
                'threshold': self.rebalance_threshold
            },
            'selection': {
                'max_holdings': self.max_holdings,
                'min_market_cap': self.min_market_cap,
                'liquidity_requirement': self.liquidity_requirement
            },
            'entry_conditions': self.entry_conditions.to_dict(),
            'exit_conditions': self.exit_conditions.to_dict(),
            'industry': {
                'preference': self.industry_preference,
                'avoid': self.industry_avoid
            },
            'operation_advice': self.operation_advice,
            'key_indicators': self.key_indicators
        }


# ============================================================================
# 12种市场状态的完整参数定义
# ============================================================================

EXTENDED_PARAMS_MAP: Dict[MarketEnvironment, ExtendedParams] = {
    
    # ------------------------------------------------------------------------
    # 牛市系列
    # ------------------------------------------------------------------------
    
    MarketEnvironment.STRONG_BULL: ExtendedParams(
        environment=MarketEnvironment.STRONG_BULL,
        environment_name="强势牛市",
        category="bull",
        # 仓位：积极
        position_min=0.8,
        position_max=1.0,
        suggested_position=0.9,
        single_stock_max=0.15,
        # 风险：低
        risk_level="low",
        stop_loss_pct=0.12,
        take_profit_pct=0.40,
        trailing_stop_pct=0.08,
        drawdown_limit=0.20,
        # 调仓：低频
        rebalance_frequency="weekly",
        rebalance_threshold=0.10,
        # 选股
        max_holdings=10,
        min_market_cap=100,
        liquidity_requirement="medium",
        # 买入条件
        entry_conditions=EntryConditions(
            ma_condition="价格站上MA20，MA5>MA10>MA20",
            momentum_condition="20日动量>5%",
            volume_condition="成交量>20日均量",
            rsi_range=(40, 80),
            macd_condition="MACD金叉或DIF>0",
            description="趋势确认后追涨，优先选择主线龙头"
        ),
        # 卖出条件
        exit_conditions=ExitConditions(
            stop_loss_type="trailing",
            take_profit_type="trailing",
            ma_break_condition="收盘跌破MA20",
            momentum_reversal="MACD死叉且DIF<0",
            volume_divergence="价涨量缩连续3天",
            description="移动止盈为主，让利润奔跑"
        ),
        # 行业
        industry_preference=["科技", "新能源", "医药", "消费"],
        industry_avoid=["钢铁", "煤炭"],
        # 建议
        operation_advice="强势牛市，积极做多。重仓持有主线龙头，适度追涨。注意控制单票仓位，分散风险。",
        key_indicators=["MA趋势", "成交量", "板块轮动", "龙头股表现"]
    ),
    
    MarketEnvironment.BULL: ExtendedParams(
        environment=MarketEnvironment.BULL,
        environment_name="牛市",
        category="bull",
        position_min=0.6,
        position_max=0.8,
        suggested_position=0.7,
        single_stock_max=0.12,
        risk_level="low",
        stop_loss_pct=0.10,
        take_profit_pct=0.30,
        trailing_stop_pct=0.06,
        drawdown_limit=0.15,
        rebalance_frequency="weekly",
        rebalance_threshold=0.08,
        max_holdings=10,
        min_market_cap=100,
        liquidity_requirement="medium",
        entry_conditions=EntryConditions(
            ma_condition="价格>MA20，MA20向上",
            momentum_condition="20日动量>3%",
            volume_condition="成交量放大",
            rsi_range=(35, 75),
            macd_condition="MACD>0或金叉",
            description="顺势而为，回调买入"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="trailing",
            take_profit_type="target",
            ma_break_condition="跌破MA20且MA20拐头",
            momentum_reversal="RSI>80后回落",
            volume_divergence="量价背离",
            description="目标止盈+移动止损结合"
        ),
        industry_preference=["科技", "消费", "金融"],
        industry_avoid=["周期弱势行业"],
        operation_advice="牛市阶段，保持较高仓位。顺势操作，回调加仓。关注领涨板块和龙头个股。",
        key_indicators=["MA20趋势", "板块强度", "资金流向", "北向资金"]
    ),
    
    MarketEnvironment.WEAK_BULL: ExtendedParams(
        environment=MarketEnvironment.WEAK_BULL,
        environment_name="弱势牛市",
        category="bull",
        position_min=0.4,
        position_max=0.6,
        suggested_position=0.5,
        single_stock_max=0.10,
        risk_level="medium",
        stop_loss_pct=0.08,
        take_profit_pct=0.20,
        trailing_stop_pct=0.05,
        drawdown_limit=0.12,
        rebalance_frequency="weekly",
        rebalance_threshold=0.06,
        max_holdings=8,
        min_market_cap=150,
        liquidity_requirement="high",
        entry_conditions=EntryConditions(
            ma_condition="价格>MA60，MA20走平或向上",
            momentum_condition="20日动量>0%",
            volume_condition="温和放量",
            rsi_range=(30, 65),
            macd_condition="MACD柱缩短或金叉",
            description="谨慎乐观，等待确认信号"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="target",
            ma_break_condition="跌破MA60",
            momentum_reversal="动量转负",
            volume_divergence="放量下跌",
            description="固定止损，分批止盈"
        ),
        industry_preference=["防御性消费", "医药", "公用事业"],
        industry_avoid=["高波动行业"],
        operation_advice="弱势牛市，保持谨慎乐观。中等仓位操作，注意风险控制。优选确定性高的标的。",
        key_indicators=["MA60支撑", "成交量变化", "市场情绪", "VIX指数"]
    ),
    
    # ------------------------------------------------------------------------
    # 熊市系列
    # ------------------------------------------------------------------------
    
    MarketEnvironment.STRONG_BEAR: ExtendedParams(
        environment=MarketEnvironment.STRONG_BEAR,
        environment_name="强势熊市",
        category="bear",
        position_min=0.0,
        position_max=0.2,
        suggested_position=0.1,
        single_stock_max=0.05,
        risk_level="high",
        stop_loss_pct=0.05,
        take_profit_pct=0.10,
        trailing_stop_pct=0.03,
        drawdown_limit=0.05,
        rebalance_frequency="daily",
        rebalance_threshold=0.03,
        max_holdings=3,
        min_market_cap=500,
        liquidity_requirement="very_high",
        entry_conditions=EntryConditions(
            ma_condition="不主动买入",
            momentum_condition="等待超卖反弹",
            volume_condition="地量出现",
            rsi_range=(10, 30),
            macd_condition="底背离",
            description="空仓或极低仓位，仅做超跌反弹"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="fixed",
            ma_break_condition="任何反弹到MA5即考虑减仓",
            momentum_reversal="反弹无量",
            volume_divergence="反弹量能不足",
            description="快进快出，严格止损"
        ),
        industry_preference=["现金", "国债逆回购"],
        industry_avoid=["所有权益类"],
        operation_advice="强势熊市，首要任务是保护本金！空仓观望或仅保留极少仓位做超跌反弹。不抄底！",
        key_indicators=["下跌速度", "恐慌指数", "融资余额", "破净股数量"]
    ),
    
    MarketEnvironment.BEAR: ExtendedParams(
        environment=MarketEnvironment.BEAR,
        environment_name="熊市",
        category="bear",
        position_min=0.1,
        position_max=0.3,
        suggested_position=0.2,
        single_stock_max=0.08,
        risk_level="high",
        stop_loss_pct=0.06,
        take_profit_pct=0.12,
        trailing_stop_pct=0.04,
        drawdown_limit=0.08,
        rebalance_frequency="weekly",
        rebalance_threshold=0.05,
        max_holdings=5,
        min_market_cap=300,
        liquidity_requirement="very_high",
        entry_conditions=EntryConditions(
            ma_condition="谨慎操作，等待企稳信号",
            momentum_condition="超卖后反弹",
            volume_condition="缩量企稳",
            rsi_range=(20, 40),
            macd_condition="底部抬高",
            description="防守为主，仅参与超跌反弹"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="fixed",
            ma_break_condition="反弹到压力位",
            momentum_reversal="反弹力度减弱",
            volume_divergence="量价背离",
            description="严格止损，快速止盈"
        ),
        industry_preference=["公用事业", "消费必需品"],
        industry_avoid=["周期股", "高估值成长"],
        operation_advice="熊市阶段，严格控制仓位。以防守为主，仅参与确定性较高的超跌反弹。",
        key_indicators=["支撑位", "成交量", "政策信号", "估值水平"]
    ),
    
    MarketEnvironment.WEAK_BEAR: ExtendedParams(
        environment=MarketEnvironment.WEAK_BEAR,
        environment_name="弱势熊市",
        category="bear",
        position_min=0.2,
        position_max=0.4,
        suggested_position=0.3,
        single_stock_max=0.08,
        risk_level="medium",
        stop_loss_pct=0.07,
        take_profit_pct=0.15,
        trailing_stop_pct=0.05,
        drawdown_limit=0.10,
        rebalance_frequency="weekly",
        rebalance_threshold=0.05,
        max_holdings=6,
        min_market_cap=200,
        liquidity_requirement="high",
        entry_conditions=EntryConditions(
            ma_condition="接近MA60支撑",
            momentum_condition="动量收敛",
            volume_condition="缩量企稳",
            rsi_range=(25, 45),
            macd_condition="底部形态",
            description="逢低布局，分批建仓"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="target",
            ma_break_condition="跌破前低",
            momentum_reversal="反弹受阻",
            volume_divergence="无量反弹",
            description="控制风险，适度止盈"
        ),
        industry_preference=["高股息", "防御性板块"],
        industry_avoid=["高弹性品种"],
        operation_advice="弱势熊市，可能是底部区域。轻仓参与，分批布局优质标的。关注转折信号。",
        key_indicators=["估值分位", "政策动向", "资金流向", "筑底形态"]
    ),
    
    # ------------------------------------------------------------------------
    # 震荡系列
    # ------------------------------------------------------------------------
    
    MarketEnvironment.HIGH_RANGE: ExtendedParams(
        environment=MarketEnvironment.HIGH_RANGE,
        environment_name="高位震荡",
        category="range",
        position_min=0.4,
        position_max=0.6,
        suggested_position=0.5,
        single_stock_max=0.10,
        risk_level="medium",
        stop_loss_pct=0.08,
        take_profit_pct=0.15,
        trailing_stop_pct=0.05,
        drawdown_limit=0.12,
        rebalance_frequency="weekly",
        rebalance_threshold=0.06,
        max_holdings=8,
        min_market_cap=200,
        liquidity_requirement="high",
        entry_conditions=EntryConditions(
            ma_condition="回踩MA20买入",
            momentum_condition="超卖区域",
            volume_condition="缩量回调",
            rsi_range=(30, 50),
            macd_condition="接近零轴",
            description="高抛低吸，区间操作"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="target",
            ma_break_condition="突破区间上沿卖出",
            momentum_reversal="超买区域",
            volume_divergence="冲高无量",
            description="逢高减仓，控制仓位"
        ),
        industry_preference=["轮动热点", "景气行业"],
        industry_avoid=["滞涨板块"],
        operation_advice="高位震荡，风险收益比下降。适度减仓，高抛低吸。警惕向下突破风险。",
        key_indicators=["区间上下沿", "成交量", "板块轮动", "北向资金"]
    ),
    
    MarketEnvironment.MID_RANGE: ExtendedParams(
        environment=MarketEnvironment.MID_RANGE,
        environment_name="中位震荡",
        category="range",
        position_min=0.3,
        position_max=0.5,
        suggested_position=0.4,
        single_stock_max=0.10,
        risk_level="medium",
        stop_loss_pct=0.07,
        take_profit_pct=0.12,
        trailing_stop_pct=0.05,
        drawdown_limit=0.10,
        rebalance_frequency="weekly",
        rebalance_threshold=0.05,
        max_holdings=8,
        min_market_cap=150,
        liquidity_requirement="medium",
        entry_conditions=EntryConditions(
            ma_condition="回踩支撑位",
            momentum_condition="超卖反弹",
            volume_condition="缩量企稳",
            rsi_range=(30, 50),
            macd_condition="底部金叉",
            description="等待方向选择，轻仓试探"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="target",
            ma_break_condition="触及压力位",
            momentum_reversal="冲高回落",
            volume_divergence="量价背离",
            description="区间操作，灵活应对"
        ),
        industry_preference=["均衡配置"],
        industry_avoid=["极端波动品种"],
        operation_advice="中位震荡，等待方向选择。轻仓参与，关注突破信号。做好两手准备。",
        key_indicators=["箱体上下沿", "突破信号", "量能变化", "市场情绪"]
    ),
    
    MarketEnvironment.LOW_RANGE: ExtendedParams(
        environment=MarketEnvironment.LOW_RANGE,
        environment_name="低位震荡",
        category="range",
        position_min=0.4,
        position_max=0.6,
        suggested_position=0.5,
        single_stock_max=0.10,
        risk_level="medium",
        stop_loss_pct=0.08,
        take_profit_pct=0.20,
        trailing_stop_pct=0.06,
        drawdown_limit=0.12,
        rebalance_frequency="weekly",
        rebalance_threshold=0.06,
        max_holdings=8,
        min_market_cap=150,
        liquidity_requirement="medium",
        entry_conditions=EntryConditions(
            ma_condition="底部企稳，MA20走平",
            momentum_condition="动量由负转正",
            volume_condition="底部放量",
            rsi_range=(25, 50),
            macd_condition="底部金叉，柱体翻红",
            description="底部区域，逢低布局"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="trailing",
            ma_break_condition="跌破前低止损",
            momentum_reversal="突破后跟进",
            volume_divergence="突破需放量确认",
            description="止损要严，止盈要宽"
        ),
        industry_preference=["超跌反弹", "估值修复"],
        industry_avoid=["基本面恶化行业"],
        operation_advice="低位震荡，可能是筑底阶段。分批建仓优质标的，等待向上突破信号。",
        key_indicators=["底部形态", "成交量变化", "政策信号", "估值底"]
    ),
    
    # ------------------------------------------------------------------------
    # 转折系列
    # ------------------------------------------------------------------------
    
    MarketEnvironment.RECOVERY: ExtendedParams(
        environment=MarketEnvironment.RECOVERY,
        environment_name="复苏",
        category="turning",
        position_min=0.5,
        position_max=0.7,
        suggested_position=0.6,
        single_stock_max=0.12,
        risk_level="medium",
        stop_loss_pct=0.08,
        take_profit_pct=0.25,
        trailing_stop_pct=0.06,
        drawdown_limit=0.12,
        rebalance_frequency="weekly",
        rebalance_threshold=0.06,
        max_holdings=8,
        min_market_cap=150,
        liquidity_requirement="medium",
        entry_conditions=EntryConditions(
            ma_condition="突破MA60，均线多头排列形成",
            momentum_condition="动量持续为正",
            volume_condition="放量突破",
            rsi_range=(40, 70),
            macd_condition="MACD金叉，柱体持续放大",
            description="确认转势，加仓布局"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="trailing",
            take_profit_type="trailing",
            ma_break_condition="回踩MA20不破可持有",
            momentum_reversal="动量持续减弱",
            volume_divergence="价涨量缩需警惕",
            description="跟随趋势，移动止盈"
        ),
        industry_preference=["景气反转行业", "政策受益板块", "超跌优质股"],
        industry_avoid=["夕阳行业"],
        operation_advice="复苏阶段，趋势可能反转。积极布局，跟随趋势。关注领涨板块和龙头个股。",
        key_indicators=["突破信号", "量能配合", "板块轮动", "资金流向"]
    ),
    
    MarketEnvironment.DISTRIBUTION: ExtendedParams(
        environment=MarketEnvironment.DISTRIBUTION,
        environment_name="派发",
        category="turning",
        position_min=0.2,
        position_max=0.4,
        suggested_position=0.3,
        single_stock_max=0.08,
        risk_level="high",
        stop_loss_pct=0.06,
        take_profit_pct=0.10,
        trailing_stop_pct=0.04,
        drawdown_limit=0.08,
        rebalance_frequency="daily",
        rebalance_threshold=0.04,
        max_holdings=5,
        min_market_cap=300,
        liquidity_requirement="very_high",
        entry_conditions=EntryConditions(
            ma_condition="不建议新开仓",
            momentum_condition="仅超跌反弹",
            volume_condition="缩量观望",
            rsi_range=(20, 40),
            macd_condition="死叉后的反弹",
            description="防守为主，逐步减仓"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="fixed",
            ma_break_condition="跌破MA60清仓",
            momentum_reversal="反弹无力",
            volume_divergence="高位放量下跌",
            description="严格止损，快速减仓"
        ),
        industry_preference=["现金为王"],
        industry_avoid=["前期涨幅大的板块"],
        operation_advice="派发阶段，风险加大。逐步减仓，锁定利润。现金为王，等待机会。",
        key_indicators=["分配日数量", "龙头股表现", "量价关系", "融资余额"]
    ),
    
    MarketEnvironment.NEUTRAL: ExtendedParams(
        environment=MarketEnvironment.NEUTRAL,
        environment_name="中性",
        category="neutral",
        position_min=0.3,
        position_max=0.5,
        suggested_position=0.4,
        single_stock_max=0.10,
        risk_level="medium",
        stop_loss_pct=0.07,
        take_profit_pct=0.15,
        trailing_stop_pct=0.05,
        drawdown_limit=0.10,
        rebalance_frequency="weekly",
        rebalance_threshold=0.05,
        max_holdings=8,
        min_market_cap=150,
        liquidity_requirement="medium",
        entry_conditions=EntryConditions(
            ma_condition="等待明确信号",
            momentum_condition="动量企稳",
            volume_condition="观察量能",
            rsi_range=(30, 60),
            macd_condition="等待方向",
            description="观望为主，等待方向确认"
        ),
        exit_conditions=ExitConditions(
            stop_loss_type="fixed",
            take_profit_type="target",
            ma_break_condition="根据方向调整",
            momentum_reversal="信号不明",
            volume_divergence="持续观察",
            description="灵活应对，等待信号"
        ),
        industry_preference=["均衡配置", "防御性板块"],
        industry_avoid=["高波动品种"],
        operation_advice="中性市场，方向不明。保持中性仓位，等待趋势明确。做好双向准备。",
        key_indicators=["趋势信号", "政策动向", "资金流向", "市场情绪"]
    ),
}


# ============================================================================
# 便捷函数
# ============================================================================

def get_extended_params(env: MarketEnvironment) -> ExtendedParams:
    """
    获取扩展参数
    
    Args:
        env: 市场环境枚举
        
    Returns:
        ExtendedParams
    """
    return EXTENDED_PARAMS_MAP.get(env, EXTENDED_PARAMS_MAP[MarketEnvironment.NEUTRAL])


def get_params_from_result(result: 'MarketEnvResultV3') -> ExtendedParams:
    """
    从v3结果获取扩展参数
    
    Args:
        result: MarketEnvResultV3实例
        
    Returns:
        ExtendedParams
    """
    return get_extended_params(result.combined_environment)


def get_params_dict(env: MarketEnvironment) -> Dict:
    """
    获取扩展参数字典
    
    Args:
        env: 市场环境枚举
        
    Returns:
        参数字典
    """
    params = get_extended_params(env)
    return params.to_dict()


def format_params_summary(params: ExtendedParams) -> str:
    """
    格式化参数摘要
    
    Args:
        params: ExtendedParams
        
    Returns:
        格式化的字符串
    """
    lines = []
    lines.append("=" * 60)
    lines.append(f"市场环境: {params.environment_name} ({params.category})")
    lines.append("=" * 60)
    
    lines.append(f"\n【仓位管理】")
    lines.append(f"  建议仓位: {params.suggested_position:.0%} ({params.position_min:.0%} ~ {params.position_max:.0%})")
    lines.append(f"  单股上限: {params.single_stock_max:.0%}")
    lines.append(f"  最大持仓: {params.max_holdings}只")
    
    lines.append(f"\n【风险控制】")
    lines.append(f"  风险等级: {params.risk_level}")
    lines.append(f"  止损线: {params.stop_loss_pct:.0%}")
    lines.append(f"  止盈线: {params.take_profit_pct:.0%}")
    lines.append(f"  移动止损: {params.trailing_stop_pct:.0%}")
    lines.append(f"  最大回撤: {params.drawdown_limit:.0%}")
    
    lines.append(f"\n【调仓设置】")
    lines.append(f"  调仓频率: {params.rebalance_frequency}")
    lines.append(f"  触发阈值: {params.rebalance_threshold:.0%}")
    
    lines.append(f"\n【买入条件】")
    lines.append(f"  {params.entry_conditions.description}")
    lines.append(f"  - 均线: {params.entry_conditions.ma_condition}")
    lines.append(f"  - RSI: {params.entry_conditions.rsi_range}")
    
    lines.append(f"\n【卖出条件】")
    lines.append(f"  {params.exit_conditions.description}")
    lines.append(f"  - 止损类型: {params.exit_conditions.stop_loss_type}")
    lines.append(f"  - 止盈类型: {params.exit_conditions.take_profit_type}")
    
    lines.append(f"\n【行业配置】")
    lines.append(f"  偏好: {', '.join(params.industry_preference)}")
    lines.append(f"  回避: {', '.join(params.industry_avoid)}")
    
    lines.append(f"\n【操作建议】")
    lines.append(f"  {params.operation_advice}")
    
    lines.append(f"\n【关注指标】")
    lines.append(f"  {', '.join(params.key_indicators)}")
    
    return "\n".join(lines)


# ============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    # 测试
    for env in MarketEnvironment:
        params = get_extended_params(env)
        print(f"\n{env.value}: 仓位{params.suggested_position:.0%}, 止损{params.stop_loss_pct:.0%}, 止盈{params.take_profit_pct:.0%}")
    
    # 打印强势牛市的完整参数
    print("\n" + "=" * 60)
    strong_bull_params = get_extended_params(MarketEnvironment.STRONG_BULL)
    print(format_params_summary(strong_bull_params))

