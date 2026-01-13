#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报策略 V6.0 - 完整策略引擎

整合所有改进模块:
1. MarketCharacterClassifierV6 - 改进的市场趋势识别 (动量加成)
2. EventDrivenEngineV6 - 事件驱动交易引擎 (替代周频调仓)
3. TenbaggerScorer - 十倍股阶段评估 (S0-S5)
4. DynamicRiskManager - 动态风险管理 (涨停保护、多级止盈止损)
5. DynamicMainlineSelector - 动态五维主线选股 (资金/热度/动量/政策/龙头) 【V6.1新增】
6. InvestmentTargetBuilder V6.0 - 支持动态主线模式的标的构建器 【V6.1新增】

目标: 周频交易实现10%+收益

V6.1更新 (2026-01-12):
- 新增动态五维主线选股
- 主线股票与信号股票加权融合
- 从全A股出发，不再局限于固定AI主题
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import pandas as pd
import json

logger = logging.getLogger(__name__)

# 导入V6模块（可选升级到V7）
try:
    from core.strategy.market_character_classifier_v7 import (
        MarketCharacterClassifierV7 as MarketCharacterClassifierV6,
    )
    logger.info("使用MarketCharacterClassifierV7（增强版）")
except ImportError:
    from core.strategy.market_character_classifier_v6 import (
        MarketCharacterClassifierV6,
    )
    logger.info("使用MarketCharacterClassifierV6（标准版）")

from core.strategy.market_character_classifier_v6 import (
    MarketCharacterV6 as MarketCharacter, 
    MarketTypeV6 as MarketType, 
    StrategyModeV6 as StrategyMode
)
from core.strategy.event_driven_engine_v6 import (
    EventDrivenEngineV6, 
    TradeSignal,
)
from core.strategy.bull_market_params_v4 import SignalParamsV4 as SignalParamsV6
from core.strategy.dynamic_risk_manager import DynamicRiskManager, DynamicRiskParams as RiskParams
from core.tenbagger.tenbagger_scorer import TenbaggerScorer, TenbaggerStage, StageScore

# V6.1新增: 动态主线选股
from core.strategy.dynamic_mainline_selector import DynamicMainlineSelector, SelectorConfig, MainlineResult
from core.strategy.investment_target_builder import InvestmentTargetBuilder, FilterConfig


@dataclass
class StrategyDecision:
    """策略决策结果"""
    allow_trade: bool = False
    market_type: str = "震荡"
    strategy_mode: str = "保守"
    position_cap: float = 0.5
    buy_targets: List[Dict] = field(default_factory=list)
    sell_targets: List[Dict] = field(default_factory=list)
    risk_params: Optional[RiskParams] = None
    reasoning: str = ""
    confidence: float = 0.0
    timestamp: str = ""
    # V6.1新增: 主线信息
    top_mainlines: List[Dict] = field(default_factory=list)  # 当前主线列表
    selection_mode: str = "dynamic_mainline"  # dynamic_mainline / fixed_theme


class BullMarketStrategyV6:
    """
    牛市高回报策略 V6.0/V6.1 - 完整策略引擎
    
    核心特性:
    1. 市场趋势自动识别与策略模式切换 (快牛/慢牛/震荡/熊市)
    2. 事件驱动交易 (首板涨停、连板加速、强势突破、量价齐升)
    3. 十倍股阶段评估辅助选股 (S1启动期优先)
    4. 动态风险管理 (涨停保护、软止损、移动止损)
    5. 动态五维主线选股 (资金/热度/动量/政策/龙头) 【V6.1新增】
    
    V6.1更新:
    - 从全A股出发，动态识别市场主线
    - 主线股票与信号股票加权融合
    - 支持切换固定主题/动态主线模式
    """
    
    def __init__(
        self, 
        initial_params: Optional[SignalParamsV6] = None,
        use_dynamic_mainline: bool = True,  # V6.1: 是否使用动态主线选股
    ):
        """初始化V6策略引擎"""
        self.params = initial_params if initial_params else SignalParamsV6()
        self.use_dynamic_mainline = use_dynamic_mainline
        
        # 初始化子模块
        self.market_classifier = MarketCharacterClassifierV6()
        self.event_engine = EventDrivenEngineV6(self.params)
        self.risk_manager = DynamicRiskManager(strategy_mode="正常")
        self.tenbagger_scorer = TenbaggerScorer()
        
        # V6.1: 动态主线选股器
        self.mainline_selector: Optional[DynamicMainlineSelector] = None
        self.target_builder: Optional[InvestmentTargetBuilder] = None
        self.current_mainlines: List[MainlineResult] = []
        
        if self.use_dynamic_mainline:
            try:
                # 初始化动态主线选股器
                selector_config = SelectorConfig(
                    top_n_mainlines=5,
                    mainline_weight=0.7,
                    signal_weight=0.3,
                )
                self.mainline_selector = DynamicMainlineSelector(config=selector_config)
                
                # 初始化标的构建器
                filter_config = FilterConfig(
                    use_dynamic_mainline=True,
                    top_n_mainlines=5,
                    mainline_weight=0.7,
                    signal_weight=0.3,
                )
                self.target_builder = InvestmentTargetBuilder(filter_config=filter_config)
                
                logger.info("V6.1 动态主线选股模块初始化成功")
            except Exception as e:
                logger.warning(f"动态主线选股模块初始化失败: {e}")
                self.use_dynamic_mainline = False
        
        # 状态缓存
        self.current_market_character: Optional[MarketCharacter] = None
        self.current_positions: Dict[str, Any] = {}
        
        logger.info(f"BullMarketStrategyV6{'（含动态主线）' if self.use_dynamic_mainline else ''} 初始化完成")
        logger.info(f"  - 选股模式: {'动态主线' if self.use_dynamic_mainline else '固定主题'}")
        logger.info(f"  - 初始最大持仓: {self.params.max_positions}只")
        logger.info(f"  - 初始单只上限: {self.params.single_position_max*100:.0f}%")
    
    def analyze_market(self, as_of_date: str, index_code: str = "000300.XSHG") -> MarketCharacter:
        """分析市场趋势"""
        market_char = self.market_classifier.classify(as_of_date, index_code)
        self.current_market_character = market_char
        
        # 根据市场特征调整策略参数
        self.risk_manager.update_mode(market_char.strategy_mode.value)
        
        logger.info(f"市场分析: {market_char.market_type.value} -> {market_char.strategy_mode.value} (置信度: {market_char.confidence:.0%})")
        
        return market_char
    
    def evaluate_stock_stage(self, stock: str, date: str = None) -> Tuple[TenbaggerStage, float, str]:
        """评估股票的十倍股阶段"""
        try:
            score = self.tenbagger_scorer.score_stock(stock, date)
            return score.stage, score.score, score.recommendation
        except Exception as e:
            logger.warning(f"评估 {stock} 阶段失败: {e}")
            return TenbaggerStage.S0_LATENT, 0, "数据不足"
    
    def select_targets(
        self,
        candidate_stocks: List[str],
        as_of_date: str,
        max_targets: int = 5,
    ) -> List[Dict]:
        """
        选择投资标的
        
        筛选流程:
        1. 计算十倍股阶段评分
        2. 过滤S4/S5衰退期股票
        3. 按阶段评分排序
        4. 取TopN
        """
        scored_stocks = []
        
        for stock in candidate_stocks:
            stage, score, recommendation = self.evaluate_stock_stage(stock, as_of_date)
            
            # 过滤衰退期和尾声期
            if stage in [TenbaggerStage.S4_DECLINE, TenbaggerStage.S5_END]:
                logger.debug(f"过滤 {stock}: {stage.value}")
                continue
            
            # 阶段权重调整
            stage_weight = {
                TenbaggerStage.S0_LATENT: 0.5,
                TenbaggerStage.S1_LAUNCH: 1.5,
                TenbaggerStage.S2_ACCELERATE: 1.2,
                TenbaggerStage.S3_MATURE: 0.7,
            }.get(stage, 1.0)
            
            final_score = score * stage_weight
            
            scored_stocks.append({
                "stock": stock,
                "stage": stage.value,
                "raw_score": score,
                "final_score": final_score,
                "recommendation": recommendation,
            })
        
        # 按最终评分排序
        scored_stocks.sort(key=lambda x: x["final_score"], reverse=True)
        
        # 取TopN
        selected = scored_stocks[:max_targets]
        
        logger.info(f"标的筛选: {len(candidate_stocks)}只 -> {len(selected)}只")
        for s in selected:
            logger.info(f"  - {s['stock']}: {s['stage']} 评分={s['final_score']:.1f}")
        
        return selected
    
    def generate_signals(
        self,
        as_of_date: str,
        price_data: pd.DataFrame,
        factors: Any,
        all_stocks: List[str],
    ) -> List[TradeSignal]:
        """
        生成交易信号
        
        使用EventDrivenEngineV6生成信号
        """
        return self.event_engine.generate_trade_signals(
            as_of_date=as_of_date,
            factors=factors,
            all_stocks=all_stocks,
        )
    
    def make_decision(
        self,
        as_of_date: str,
        candidate_stocks: List[str],
        price_data: Optional[pd.DataFrame] = None,
        factors: Any = None,
        use_mainline: Optional[bool] = None,  # V6.1: 覆盖默认选股模式
    ) -> StrategyDecision:
        """
        做出完整的策略决策
        
        V6.1更新: 支持动态主线选股模式
        
        Args:
            as_of_date: 决策日期
            candidate_stocks: 候选股票池 (传统模式使用)
            price_data: 价格数据 (可选)
            factors: 因子数据 (可选)
            use_mainline: 是否使用主线选股 (覆盖默认值)
        
        Returns:
            StrategyDecision: 完整的策略决策
        """
        decision = StrategyDecision(timestamp=as_of_date)
        
        # 确定选股模式
        use_mainline_mode = use_mainline if use_mainline is not None else self.use_dynamic_mainline
        decision.selection_mode = "dynamic_mainline" if use_mainline_mode else "fixed_theme"
        
        # 1. 分析市场趋势
        market_char = self.analyze_market(as_of_date)
        decision.market_type = market_char.market_type.value
        decision.strategy_mode = market_char.strategy_mode.value
        decision.confidence = market_char.confidence
        
        # 2. 检查是否允许交易
        if market_char.strategy_mode == StrategyMode.DEFENSIVE:
            decision.allow_trade = False
            decision.reasoning = f"市场处于{market_char.market_type.value}，采取防御策略，不进行交易"
            decision.position_cap = 0.0
            logger.warning(decision.reasoning)
            return decision
        
        # 3. 设置仓位上限
        decision.position_cap = market_char.suggested_params.get("position_cap", 0.5)
        decision.allow_trade = True
        
        # 4. 获取风险参数
        decision.risk_params = self.risk_manager.params
        
        # 5. V6.1: 动态主线选股
        if use_mainline_mode and self.mainline_selector:
            decision = self._make_decision_with_mainline(
                decision, as_of_date, candidate_stocks
            )
        else:
            decision = self._make_decision_with_theme(
                decision, as_of_date, candidate_stocks
            )
        
        return decision
    
    def _make_decision_with_mainline(
        self,
        decision: StrategyDecision,
        as_of_date: str,
        fallback_stocks: List[str],
    ) -> StrategyDecision:
        """
        V6.1新增: 使用动态主线选股做出决策
        """
        logger.info("使用动态主线选股模式...")
        
        try:
            # 1. 识别市场主线
            mainlines_dict, top_mainlines = self.mainline_selector.get_mainline_stocks(
                as_of_date, top_n=5
            )
            self.current_mainlines = top_mainlines
            
            # 记录主线信息
            for ml in top_mainlines[:5]:
                decision.top_mainlines.append({
                    "name": ml.name,
                    "type": ml.mainline_type,
                    "score": ml.total_score,
                    "signal": ml.signal.value,
                    "change_pct": ml.change_pct,
                    "stocks_count": len(ml.stocks),
                })
            
            # 2. 收集主线股票
            mainline_stocks = []
            for stocks in mainlines_dict.values():
                mainline_stocks.extend(stocks)
            mainline_stocks = list(set(mainline_stocks))[:500]  # 去重并限制数量
            
            logger.info(f"从主线获取 {len(mainline_stocks)} 只候选股票")
            
            # 3. 使用十倍股评分筛选
            max_positions = self.params.max_positions
            selected_targets = self.select_targets(
                candidate_stocks=mainline_stocks,
                as_of_date=as_of_date,
                max_targets=max_positions,
            )
            
            # 4. 转换为买入目标
            for target in selected_targets:
                buy_target = {
                    "stock": target["stock"],
                    "stage": target["stage"],
                    "score": target["final_score"],
                    "recommendation": target["recommendation"],
                    "target_weight": decision.position_cap / max_positions,
                    "source": "mainline",  # V6.1: 标记来源
                }
                decision.buy_targets.append(buy_target)
            
            # 5. 生成决策理由
            mainline_names = ", ".join([ml.name for ml in top_mainlines[:3]])
            decision.reasoning = (
                f"市场{decision.market_type}，"
                f"策略模式{decision.strategy_mode}，"
                f"主线: [{mainline_names}]，"
                f"仓位上限{decision.position_cap*100:.0f}%，"
                f"筛选出{len(decision.buy_targets)}只标的"
            )
            
            logger.info(f"策略决策(主线模式): {decision.reasoning}")
            
        except Exception as e:
            logger.warning(f"动态主线选股失败: {e}，回退到传统模式")
            return self._make_decision_with_theme(decision, as_of_date, fallback_stocks)
        
        return decision
    
    def _make_decision_with_theme(
        self,
        decision: StrategyDecision,
        as_of_date: str,
        candidate_stocks: List[str],
    ) -> StrategyDecision:
        """
        使用传统主题模式做出决策
        """
        logger.info("使用传统主题选股模式...")
        decision.selection_mode = "fixed_theme"
        
        max_positions = self.params.max_positions
        selected_targets = self.select_targets(
            candidate_stocks=candidate_stocks,
            as_of_date=as_of_date,
            max_targets=max_positions,
        )
        
        for target in selected_targets:
            buy_target = {
                "stock": target["stock"],
                "stage": target["stage"],
                "score": target["final_score"],
                "recommendation": target["recommendation"],
                "target_weight": decision.position_cap / max_positions,
                "source": "theme",
            }
            decision.buy_targets.append(buy_target)
        
        decision.reasoning = (
            f"市场{decision.market_type}，"
            f"策略模式{decision.strategy_mode}，"
            f"仓位上限{decision.position_cap*100:.0f}%，"
            f"筛选出{len(decision.buy_targets)}只标的"
        )
        
        logger.info(f"策略决策(主题模式): {decision.reasoning}")
        
        return decision
    
    def get_trading_rules(self) -> str:
        """获取当前交易规则"""
        rules = []
        
        rules.append("=" * 60)
        rules.append("🎯 牛市高回报策略 V6.0 - 交易规则")
        rules.append("=" * 60)
        
        # 市场状态
        if self.current_market_character:
            rules.append(f"\n【市场状态】")
            rules.append(f"  市场类型: {self.current_market_character.market_type.value}")
            rules.append(f"  策略模式: {self.current_market_character.strategy_mode.value}")
            rules.append(f"  置信度: {self.current_market_character.confidence:.0%}")
        
        # 买入规则
        rules.append(f"\n【买入触发条件】(满足任一)")
        rules.append(f"  1. 首板涨停: 首次涨停 + 量比>{self.params.vol_ratio_threshold_first:.1f}")
        rules.append(f"  2. 连板加速: 近5日涨停次数>=2")
        rules.append(f"  3. 强势突破: 突破60日高点 + 5日动量>{self.params.mom_5d_threshold_breakout:.0f}% + 量比>1.5")
        rules.append(f"  4. 量价齐升: 5日动量>{self.params.mom_5d_threshold_volume:.0f}% + 量比>2.0")
        
        # 卖出规则
        risk_params = self.risk_manager.params
        rules.append(f"\n【卖出触发条件】")
        rules.append(f"  1. 涨停中不卖 (涨停保护)")
        rules.append(f"  2. 硬止损: {risk_params.hard_stop_loss*100:.0f}%")
        rules.append(f"  3. 软止损: {risk_params.soft_stop_loss*100:.0f}% (持仓>{risk_params.soft_stop_days}天)")
        rules.append(f"  4. 第一批止盈: +{risk_params.take_profit_1*100:.0f}% 减仓{risk_params.take_profit_1_ratio*100:.0f}%")
        rules.append(f"  5. 全止盈: +{risk_params.take_profit_2*100:.0f}%")
        rules.append(f"  6. 移动止损: 盈利>{risk_params.trailing_trigger*100:.0f}%后回撤>{-risk_params.trailing_stop*100:.0f}%")
        rules.append(f"  7. 时间止损: 持仓>{risk_params.time_stop_days}天无盈利")
        
        # 仓位管理
        rules.append(f"\n【仓位管理】")
        rules.append(f"  最大持仓: {self.params.max_positions}只")
        rules.append(f"  单只上限: {self.params.single_position_max*100:.0f}%")
        rules.append(f"  总仓位上限: {risk_params.position_cap*100:.0f}%")
        
        # 十倍股阶段筛选
        rules.append(f"\n【十倍股阶段筛选】")
        rules.append(f"  ⭐ S1启动期: 最佳买点，权重1.5x")
        rules.append(f"  📈 S2加速期: 持有加仓，权重1.2x")
        rules.append(f"  👀 S0潜伏期: 关注观察，权重0.5x")
        rules.append(f"  ⚠️ S3成熟期: 分批减仓，权重0.7x")
        rules.append(f"  ❌ S4/S5衰退期: 严格回避，过滤")
        
        rules.append("\n" + "=" * 60)
        
        return "\n".join(rules)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """获取策略状态摘要"""
        summary = {
            "strategy_version": "V6.0",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market_analysis": {
                "market_type": self.current_market_character.market_type.value if self.current_market_character else "未分析",
                "strategy_mode": self.current_market_character.strategy_mode.value if self.current_market_character else "未知",
                "confidence": self.current_market_character.confidence if self.current_market_character else 0,
            },
            "risk_params": {
                "hard_stop_loss": f"{self.risk_manager.params.hard_stop_loss*100:.0f}%",
                "take_profit": f"{self.risk_manager.params.take_profit_2*100:.0f}%",
                "max_positions": self.params.max_positions,
            },
            "modules_status": {
                "market_classifier": "✅ 正常",
                "event_engine": "✅ 正常",
                "risk_manager": "✅ 正常",
                "tenbagger_scorer": "✅ 正常",
            }
        }
        return summary


def test_bull_market_strategy_v6():
    """测试BullMarketStrategyV6"""
    
    print("=" * 60)
    print("🎯 牛市高回报策略 V6.0 - 完整测试")
    print("=" * 60)
    
    # 初始化策略引擎
    strategy = BullMarketStrategyV6()
    
    # 测试AI智能体核心标的
    ai_targets = [
        "002230.XSHE",  # 科大讯飞
        "688111.XSHG",  # 金山办公
        "300058.XSHE",  # 蓝色光标
        "300418.XSHE",  # 昆仑万维
        "300253.XSHE",  # 卫宁健康
        "300033.XSHE",  # 同花顺
    ]
    
    # 做出策略决策
    decision = strategy.make_decision(
        as_of_date=datetime.now().strftime("%Y-%m-%d"),
        candidate_stocks=ai_targets,
    )
    
    # 打印决策结果
    print(f"\n【策略决策】")
    print(f"  允许交易: {decision.allow_trade}")
    print(f"  市场类型: {decision.market_type}")
    print(f"  策略模式: {decision.strategy_mode}")
    print(f"  仓位上限: {decision.position_cap*100:.0f}%")
    print(f"  置信度: {decision.confidence:.0%}")
    print(f"  决策理由: {decision.reasoning}")
    
    print(f"\n【买入目标】")
    for target in decision.buy_targets:
        print(f"  - {target['stock']}: {target['stage']} 评分={target['score']:.1f}")
    
    # 打印交易规则
    print("\n" + strategy.get_trading_rules())
    
    # 打印状态摘要
    print("\n【策略状态摘要】")
    summary = strategy.get_status_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ BullMarketStrategyV6 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    test_bull_market_strategy_v6()
