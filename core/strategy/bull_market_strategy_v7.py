# -*- coding: utf-8 -*-
"""
牛市高收益策略 V7.0
===================

核心改进:
1. 专业回测引擎（对标BulletTrade）
2. 主题周期判断与自适应参数
3. 多因子信号组合优化
4. 主线强度与个股信号融合
5. 完整止损止盈机制

目标: 周频10%+收益

作者: TRQuant Team
版本: V7.0
日期: 2026-01-12
"""

from __future__ import annotations

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

import pandas as pd
import numpy as np

# 导入核心模块
from core.research.data_provider import ResearchDataProvider, DataMatrices
from core.research.factors import FactorCalculator, FactorMatrices
from core.research.signals_v7 import SignalEngineV7, SignalParamsV7, SignalMatricesV7
from core.research.vbt_backtest_v7 import (
    VBTBacktestV7, BacktestResultV7, 
    TradeCostModel, StopLossConfig, ExecutionMode
)
from core.strategy.theme_cycle_judge import ThemeCycleJudge, ThemeCycle, CycleJudgeResult
from core.strategy.dynamic_mainline_selector import DynamicMainlineSelector

logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

@dataclass
class StrategyConfigV7:
    """V7策略配置"""
    # 基本配置
    initial_capital: float = 1000000.0
    max_stocks_per_period: int = 1000
    
    # 信号配置
    signal_params: Optional[SignalParamsV7] = None
    
    # 止损止盈配置
    stop_loss_config: Optional[StopLossConfig] = None
    
    # 交易成本配置
    cost_model: Optional[TradeCostModel] = None
    
    # 是否使用周期自适应
    use_cycle_adaptive: bool = True
    
    # 是否使用主线选股
    use_mainline_selection: bool = True
    
    # 主线数量
    top_n_mainlines: int = 3


@dataclass
class StrategyResultV7:
    """V7策略结果"""
    period: str
    start_date: str
    end_date: str
    market_type: str = ""
    
    # 周期判断
    cycle: str = ""
    cycle_confidence: float = 0.0
    
    # 主线信息
    top_mainlines: List[Dict] = field(default_factory=list)
    selected_stocks: List[str] = field(default_factory=list)
    
    # 回测结果
    backtest_result: Optional[BacktestResultV7] = None
    
    # 汇总指标
    total_return: float = 0.0
    weekly_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'period': self.period,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'market_type': self.market_type,
            'cycle': self.cycle,
            'cycle_confidence': self.cycle_confidence,
            'top_mainlines': [m.get('name', '') for m in self.top_mainlines[:3]],
            'num_stocks': len(self.selected_stocks),
            'total_return': self.total_return,
            'weekly_return': self.weekly_return,
            'sharpe_ratio': self.sharpe_ratio,
            'max_drawdown': self.max_drawdown,
            'win_rate': self.win_rate,
        }


# ============== 牛市策略V7 ==============

class BullMarketStrategyV7:
    """
    牛市高收益策略V7
    
    工作流:
    1. 动态主线识别 -> 热门板块/概念
    2. 主题周期判断 -> 初期/中期/后期/衰竭
    3. 自适应参数调整 -> 根据周期调整信号权重
    4. 多因子信号生成 -> 首板/连板/突破/量价
    5. 主线+信号融合评分
    6. 专业回测执行
    """
    
    def __init__(self, config: Optional[StrategyConfigV7] = None):
        """
        初始化策略
        
        Args:
            config: 策略配置
        """
        self.config = config or StrategyConfigV7()
        
        # 初始化组件
        self._init_components()
        
        logger.info("BullMarketStrategyV7 初始化完成")
    
    def _init_components(self):
        """初始化各组件"""
        # 数据提供器
        self.data_provider = ResearchDataProvider()
        
        # 因子计算器
        self.factor_calculator = FactorCalculator()
        
        # 信号引擎
        signal_params = self.config.signal_params or SignalParamsV7()
        self.signal_engine = SignalEngineV7(params=signal_params)
        
        # 主线选择器
        self.mainline_selector = DynamicMainlineSelector()
        
        # 周期判断器
        self.cycle_judge = ThemeCycleJudge()
        
        # 回测引擎（延迟初始化）
        self._backtest_engine = None
    
    def _get_backtest_engine(self) -> VBTBacktestV7:
        """获取回测引擎"""
        if self._backtest_engine is None:
            cost_model = self.config.cost_model or TradeCostModel()
            stop_loss_config = self.config.stop_loss_config or StopLossConfig()
            
            self._backtest_engine = VBTBacktestV7(
                initial_capital=self.config.initial_capital,
                cost_model=cost_model,
                stop_loss_config=stop_loss_config,
                execution_mode=ExecutionMode.CLOSE,
            )
        return self._backtest_engine
    
    def run_period(
        self,
        start_date: str,
        end_date: str,
        period_name: str = "",
    ) -> StrategyResultV7:
        """
        运行单个时段的策略
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            period_name: 时段名称
        
        Returns:
            StrategyResultV7: 策略结果
        """
        result = StrategyResultV7(
            period=period_name,
            start_date=start_date,
            end_date=end_date,
        )
        
        try:
            logger.info(f"="*60)
            logger.info(f"开始运行: {period_name} ({start_date} ~ {end_date})")
            logger.info(f"="*60)
            
            # 1. 识别主线
            mainlines, mainline_stocks = self._identify_mainlines(start_date)
            result.top_mainlines = mainlines[:3]
            
            if not mainline_stocks:
                logger.warning("未识别到有效主线股票")
                return result
            
            logger.info(f"识别主线: {[m.get('name', '') for m in mainlines[:3]]}")
            logger.info(f"主线相关股票数: {len(mainline_stocks)}")
            
            # 2. 判断主题周期
            if mainlines and self.config.use_cycle_adaptive:
                cycle_result = self._judge_cycle(mainlines[0], start_date)
                result.cycle = cycle_result.cycle.value
                result.cycle_confidence = cycle_result.confidence
                
                # 根据周期调整参数
                signal_params = self._adapt_params_for_cycle(cycle_result)
            else:
                signal_params = self.signal_engine.params
                result.cycle = "unknown"
            
            logger.info(f"周期判断: {result.cycle} (置信度: {result.cycle_confidence:.0%})")
            
            # 3. 获取价格数据
            stocks_to_fetch = mainline_stocks[:self.config.max_stocks_per_period]
            result.selected_stocks = stocks_to_fetch
            
            data = self._fetch_data(stocks_to_fetch, start_date, end_date)
            if data is None or data.close.empty:
                logger.warning("获取数据失败")
                return result
            
            logger.info(f"获取数据: {len(data.symbols)}只股票, {len(data.dates)}个交易日")
            
            # 4. 计算因子
            factors = self._calculate_factors(data)
            
            # 5. 计算主线得分
            mainline_scores = self._calculate_mainline_scores(data.symbols, mainlines)
            
            # 6. 生成信号
            signals = self.signal_engine.generate_signals(
                data=data,
                factors=factors,
                params=signal_params,
                mainline_scores=mainline_scores,
            )
            
            logger.info(f"生成信号: 买入信号数={signals.entries.sum().sum()}")
            
            # 7. 运行回测
            engine = self._get_backtest_engine()
            # 重置引擎
            engine._reset()
            
            backtest_result = engine.run(
                close=data.close,
                open_=data.open,
                high=data.high,
                low=data.low,
                volume=data.volume,
                target_weights=signals.target_weights,
            )
            
            result.backtest_result = backtest_result
            result.total_return = backtest_result.total_return
            result.weekly_return = backtest_result.weekly_return
            result.sharpe_ratio = backtest_result.sharpe_ratio
            result.max_drawdown = backtest_result.max_drawdown
            result.win_rate = backtest_result.trade_win_rate
            
            logger.info(f"回测完成: 总收益={result.total_return:.2f}%, "
                       f"周收益={result.weekly_return:.2f}%, "
                       f"夏普={result.sharpe_ratio:.2f}")
            
        except Exception as e:
            logger.error(f"运行失败: {e}")
            import traceback
            traceback.print_exc()
        
        return result
    
    def _identify_mainlines(
        self,
        date: str,
    ) -> Tuple[List[Dict], List[str]]:
        """识别主线"""
        try:
            mainline_results = self.mainline_selector.identify_mainlines(
                as_of_date=date,
            )
            
            # 转换为字典格式
            mainlines = []
            stocks = []
            
            for ml in mainline_results[:self.config.top_n_mainlines]:
                mainlines.append({
                    'name': ml.name,
                    'code': ml.code,
                    'type': ml.mainline_type,
                    'score': ml.total_score,
                    'stocks': ml.stocks,
                })
                stocks.extend(ml.stocks)
            
            # 去重
            stocks = list(set(stocks))
            
            return mainlines, stocks
            
        except Exception as e:
            logger.warning(f"识别主线失败: {e}")
            return [], []
    
    def _judge_cycle(
        self,
        mainline: Dict,
        date: str,
    ) -> CycleJudgeResult:
        """判断主题周期"""
        try:
            name = mainline.get('name', '')
            stocks = mainline.get('stocks', [])
            
            return self.cycle_judge.judge_cycle(
                mainline_name=name,
                mainline_stocks=stocks,
                date=date,
            )
            
        except Exception as e:
            logger.warning(f"周期判断失败: {e}")
            return CycleJudgeResult(cycle=ThemeCycle.UNKNOWN)
    
    def _adapt_params_for_cycle(
        self,
        cycle_result: CycleJudgeResult,
    ) -> SignalParamsV7:
        """根据周期调整参数"""
        params = self.signal_engine.params
        cycle_params = cycle_result.params
        
        if cycle_params:
            # 更新信号权重
            params = SignalParamsV7(
                **{k: v for k, v in params.__dict__.items() if k != 'signal_weights'}
            )
            params.signal_weights = cycle_params.signal_weights
            params.max_positions = cycle_params.max_positions
            params.single_position_max = cycle_params.single_position_max
            
            logger.info(f"参数自适应: 最大持仓={params.max_positions}, "
                       f"单只上限={params.single_position_max:.0%}")
        
        return params
    
    def _fetch_data(
        self,
        stocks: List[str],
        start_date: str,
        end_date: str,
    ) -> Optional[DataMatrices]:
        """获取数据"""
        try:
            return self.data_provider.get_data_matrices(
                stocks=stocks,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            return None
    
    def _calculate_factors(self, data: DataMatrices) -> FactorMatrices:
        """计算因子"""
        return self.factor_calculator.calculate_factors(
            data=data,
            factor_list=[
                "mom_20d", "mom_5d", "rel_position", "vol_ratio",
                "is_limit_up", "limit_up_count_5d", "is_first_limit_up",
                "breakout_60d", "flow_strength"
            ]
        )
    
    def _calculate_mainline_scores(
        self,
        stocks: List[str],
        mainlines: List[Dict],
    ) -> pd.DataFrame:
        """计算主线得分"""
        # 创建评分矩阵
        scores = pd.Series(0.0, index=stocks)
        
        for i, ml in enumerate(mainlines):
            ml_stocks = ml.get('stocks', [])
            ml_score = ml.get('score', 0)
            
            # 权重递减
            weight = 1.0 / (i + 1)
            
            for stock in ml_stocks:
                if stock in scores.index:
                    scores[stock] += ml_score * weight
        
        # 归一化到0-100
        if scores.max() > 0:
            scores = scores / scores.max() * 100
        
        return scores
    
    def run_multi_periods(
        self,
        periods: List[Dict[str, str]],
    ) -> List[StrategyResultV7]:
        """
        运行多个时段
        
        Args:
            periods: 时段列表 [{'name': '...', 'start': '...', 'end': '...'}, ...]
        
        Returns:
            List[StrategyResultV7]: 结果列表
        """
        results = []
        
        for period in periods:
            name = period.get('name', '')
            start = period.get('start', '')
            end = period.get('end', '')
            
            result = self.run_period(start, end, name)
            results.append(result)
            
            # 重置回测引擎
            self._backtest_engine = None
        
        return results
    
    def generate_report(
        self,
        results: List[StrategyResultV7],
        output_path: Optional[str] = None,
    ) -> str:
        """生成回测报告"""
        from datetime import datetime as dt
        
        report = []
        report.append("# 牛市高收益策略 V7.0 回测报告")
        report.append(f"\n**生成时间**: {dt.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"**版本**: V7.0")
        report.append("")
        
        # 汇总表格
        report.append("## 1. 各时段回测结果汇总")
        report.append("")
        report.append("| 时段 | 周期 | 总收益 | 周收益 | 夏普 | 回撤 | 胜率 |")
        report.append("|------|------|--------|--------|------|------|------|")
        
        for r in results:
            report.append(
                f"| {r.period} | {r.cycle} | {r.total_return:.2f}% | "
                f"{r.weekly_return:.2f}% | {r.sharpe_ratio:.2f} | "
                f"{r.max_drawdown:.2f}% | {r.win_rate:.1f}% |"
            )
        
        # 平均值
        if results:
            avg_return = np.mean([r.total_return for r in results])
            avg_weekly = np.mean([r.weekly_return for r in results])
            avg_sharpe = np.mean([r.sharpe_ratio for r in results])
            avg_dd = np.mean([r.max_drawdown for r in results])
            avg_win = np.mean([r.win_rate for r in results])
            
            report.append(
                f"| **平均** | - | **{avg_return:.2f}%** | "
                f"**{avg_weekly:.2f}%** | **{avg_sharpe:.2f}** | "
                f"**{avg_dd:.2f}%** | **{avg_win:.1f}%** |"
            )
        
        report.append("")
        
        # 详细结果
        report.append("## 2. 各时段详细结果")
        report.append("")
        
        for r in results:
            report.append(f"### {r.period}")
            report.append(f"- **日期**: {r.start_date} ~ {r.end_date}")
            report.append(f"- **周期判断**: {r.cycle} (置信度: {r.cycle_confidence:.0%})")
            report.append(f"- **主线**: {[m.get('name', '') for m in r.top_mainlines]}")
            report.append(f"- **选股数**: {len(r.selected_stocks)}")
            report.append(f"- **总收益**: {r.total_return:.2f}%")
            report.append(f"- **周收益**: {r.weekly_return:.2f}%")
            report.append(f"- **夏普比率**: {r.sharpe_ratio:.2f}")
            report.append(f"- **最大回撤**: {r.max_drawdown:.2f}%")
            report.append(f"- **交易胜率**: {r.win_rate:.1f}%")
            report.append("")
        
        # 策略总结
        report.append("## 3. 策略配置")
        report.append("")
        report.append(f"- **初始资金**: {self.config.initial_capital:,.0f}")
        report.append(f"- **使用周期自适应**: {self.config.use_cycle_adaptive}")
        report.append(f"- **使用主线选股**: {self.config.use_mainline_selection}")
        report.append(f"- **主线数量**: {self.config.top_n_mainlines}")
        report.append("")
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"报告已保存: {output_path}")
        
        return report_text


# ============== 测试函数 ==============

def test_bull_market_strategy_v7():
    """测试牛市策略V7"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    
    print("="*60)
    print("牛市高收益策略V7 测试")
    print("="*60)
    
    # 创建策略
    config = StrategyConfigV7(
        initial_capital=1000000,
        max_stocks_per_period=100,  # 测试用小样本
        use_cycle_adaptive=True,
        use_mainline_selection=True,
    )
    
    strategy = BullMarketStrategyV7(config)
    
    # 运行单个时段
    result = strategy.run_period(
        start_date="2024-09-20",
        end_date="2024-10-15",
        period_name="2024政策牛"
    )
    
    print(f"\n回测结果:")
    print(f"  总收益: {result.total_return:.2f}%")
    print(f"  周收益: {result.weekly_return:.2f}%")
    print(f"  夏普比率: {result.sharpe_ratio:.2f}")
    print(f"  最大回撤: {result.max_drawdown:.2f}%")
    
    return result


if __name__ == "__main__":
    test_bull_market_strategy_v7()
