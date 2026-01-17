# -*- coding: utf-8 -*-
"""
牛市高回报策略 V4.0 参数模块
============================

整合所有已优化参数，包括：
- 追涨策略优化结果 (output/chase_rise_optimization/best_params_20260111_161516.json)
- 牛市VBT优化结果 (output/bull_market_optimization_vbt_v2/best_params_20260111_205302.json)
- V3最新优化结果 (output/bull_market_v3/best_params_v3_20260111_222058.json)

核心特点：
1. 涨停因子参数（首板量比、连板判定）
2. 突破因子参数（动量阈值、量比阈值）
3. 量价齐升参数（参数化，非硬编码）
4. 分级止损止盈参数
5. 市场趋势开关参数

开发记录：
- 2026-01-12: 创建V4参数类，整合所有已验证参数
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class StrategyMode(Enum):
    """策略模式"""
    BULL_AGGRESSIVE = "牛市激进"      # 牛市确认，高仓位高频
    BULL_NORMAL = "牛市正常"          # 牛市中，正常仓位
    MIXED = "混合模式"                # 震荡市，平衡收益风险
    DEFENSIVE = "防御模式"            # 熊市或不确定，低仓位
    STOP = "停止交易"                 # 强熊市，不交易


@dataclass
class SignalParamsV4:
    """
    V4策略完整参数（整合所有已优化参数）
    
    参数来源：
    - 追涨优化: limit_up_threshold, vol_ratio_threshold_first, mom_5d_threshold_*
    - VBT优化: min_mom_20d, max_mom_20d, trailing_stop_*, partial_profit_*
    - V3优化: max_positions, stop_loss_pct, take_profit_pct
    
    验证结果：
    - V3最优: 周收益4.32%, 夏普6.30, 最大回撤1.91%
    """
    
    # =========================================================================
    # 动量因子参数（来自VBT优化）
    # =========================================================================
    min_mom_20d: float = -1.25      # 20日动量下限（几乎不限制）
    max_mom_20d: float = 25.0       # 20日动量上限（防止追高）
    max_rel_position: float = 80.0  # 最大相对位置（防止追高）
    min_vol_ratio: float = 1.0      # 最小量比（要求放量）
    
    # =========================================================================
    # 涨停因子参数（来自追涨优化，核心！）
    # =========================================================================
    limit_up_threshold: float = 0.093          # 涨停判定阈值(9.3%)
    vol_ratio_threshold_first: float = 2.5     # 首板量比阈值
    limit_up_lookback: int = 30                # 首板回溯周期
    
    # =========================================================================
    # 突破因子参数（来自追涨优化）
    # =========================================================================
    mom_5d_threshold_breakout: float = 16.0    # 突破动量阈值
    vol_ratio_threshold_breakout: float = 1.5  # 突破量比阈值
    breakout_ratio_min: float = 5.0            # 最小突破幅度%
    breakout_period: int = 60                  # 突破回溯周期（60日高点）
    
    # =========================================================================
    # 量价齐升参数（来自追涨优化，解决硬编码问题！）
    # =========================================================================
    mom_5d_threshold_volume: float = 10.0      # 量价齐升动量阈值
    vol_ratio_threshold_volume: float = 2.0    # 量价齐升量比阈值
    
    # =========================================================================
    # 资金流向参数
    # =========================================================================
    min_flow_strength: float = 0.3             # 最小资金流向强度（0=不限制）
    
    # =========================================================================
    # 信号评分参数（来自追涨优化）
    # =========================================================================
    min_signal_score: float = 55.0             # 最小信号评分
    
    # 信号评分权重
    first_limit_base_score: float = 80.0       # 首板启动基础分
    first_limit_breakout_bonus: float = 10.0   # 首板+突破加分
    consecutive_base_score: float = 70.0       # 连板基础分
    consecutive_per_board_bonus: float = 5.0   # 每多一板加分
    breakout_base_score: float = 65.0          # 突破基础分
    volume_price_base_score: float = 60.0      # 量价齐升基础分
    
    # =========================================================================
    # 持仓配置（综合V3和VBT优化）
    # =========================================================================
    max_positions: int = 5                     # 最大持仓数
    single_position_max: float = 0.20          # 单只股票最大权重
    rebalance_period: int = 5                  # 调仓周期（周调仓）
    
    # =========================================================================
    # 止损参数（分级止损）
    # =========================================================================
    stop_loss_pct: float = -0.10               # 硬止损（-10%立即止损）
    soft_stop_loss_pct: float = -0.08          # 软止损（-8%且持仓>=soft_stop_days）
    soft_stop_days: int = 3                    # 软止损触发天数
    soft_stop_ratio: float = 0.50              # 软止损减仓比例
    
    # =========================================================================
    # 止盈参数（分批止盈）
    # =========================================================================
    take_profit_pct: float = 0.40              # 全止盈（+40%全平）
    partial_profit_1_pct: float = 0.20         # 第一批止盈触发（+20%）
    partial_profit_1_ratio: float = 0.50       # 第一批减仓比例（50%）
    partial_profit_2_pct: float = 0.30         # 第二批止盈触发（+30%）
    partial_profit_2_ratio: float = 0.30       # 第二批减仓比例（30%）
    
    # =========================================================================
    # 移动止损参数（来自VBT优化）
    # =========================================================================
    trailing_stop_pct: float = -0.09           # 移动止损回撤（-9%）
    trailing_stop_trigger: float = 0.15        # 移动止损触发（+15%）
    
    # =========================================================================
    # 时间止损
    # =========================================================================
    time_stop_days: int = 20                   # 时间止损天数
    
    # =========================================================================
    # 市场趋势开关参数（新增！）
    # =========================================================================
    market_trend_enabled: bool = True          # 是否启用市场趋势开关
    bull_threshold: float = 30.0               # 牛市阈值（ensemble_score）
    bear_threshold: float = -30.0              # 熊市阈值
    position_cap_bull: float = 1.0             # 牛市仓位上限
    position_cap_neutral: float = 0.6          # 震荡市仓位上限
    position_cap_bear: float = 0.3             # 熊市仓位上限
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SignalParamsV4":
        """从字典创建"""
        # 只取存在的字段
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    @classmethod
    def from_json(cls, json_path: str) -> "SignalParamsV4":
        """从JSON文件加载"""
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"参数文件不存在: {json_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 支持嵌套结构（如 {"params": {...}}）
        if "params" in data:
            data = data["params"]
        
        return cls.from_dict(data)
    
    def save_json(self, json_path: str):
        """保存为JSON文件"""
        path = Path(json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"参数已保存: {json_path}")
    
    def validate(self) -> List[str]:
        """验证参数合理性，返回警告列表"""
        warnings = []
        
        # 止损止盈验证
        if self.stop_loss_pct >= 0:
            warnings.append(f"stop_loss_pct应为负数: {self.stop_loss_pct}")
        if self.take_profit_pct <= 0:
            warnings.append(f"take_profit_pct应为正数: {self.take_profit_pct}")
        if self.partial_profit_1_pct >= self.partial_profit_2_pct:
            warnings.append(f"partial_profit_1_pct应小于partial_profit_2_pct")
        if self.partial_profit_2_pct >= self.take_profit_pct:
            warnings.append(f"partial_profit_2_pct应小于take_profit_pct")
        
        # 仓位验证
        if self.max_positions < 1:
            warnings.append(f"max_positions应>=1: {self.max_positions}")
        if not 0 < self.single_position_max <= 1:
            warnings.append(f"single_position_max应在(0,1]: {self.single_position_max}")
        
        # 涨停参数验证
        if not 0.09 <= self.limit_up_threshold <= 0.11:
            warnings.append(f"limit_up_threshold应在[0.09,0.11]: {self.limit_up_threshold}")
        
        return warnings
    
    def get_strategy_mode(self, ensemble_score: float) -> StrategyMode:
        """根据市场趋势得分获取策略模式"""
        if not self.market_trend_enabled:
            return StrategyMode.BULL_NORMAL
        
        if ensemble_score >= self.bull_threshold + 20:
            return StrategyMode.BULL_AGGRESSIVE
        elif ensemble_score >= self.bull_threshold:
            return StrategyMode.BULL_NORMAL
        elif ensemble_score >= self.bear_threshold:
            return StrategyMode.MIXED
        elif ensemble_score >= self.bear_threshold - 20:
            return StrategyMode.DEFENSIVE
        else:
            return StrategyMode.STOP
    
    def get_position_cap(self, ensemble_score: float) -> float:
        """根据市场趋势得分获取仓位上限"""
        if not self.market_trend_enabled:
            return 1.0
        
        if ensemble_score >= self.bull_threshold:
            return self.position_cap_bull
        elif ensemble_score >= self.bear_threshold:
            return self.position_cap_neutral
        else:
            return self.position_cap_bear


# ============================================================================
# 预定义参数配置
# ============================================================================

# V4默认参数（整合所有优化结果）
DEFAULT_PARAMS_V4 = SignalParamsV4()

# 激进模式（牛市专用）
AGGRESSIVE_PARAMS_V4 = SignalParamsV4(
    max_positions=8,
    single_position_max=0.15,
    stop_loss_pct=-0.12,
    take_profit_pct=0.50,
    min_signal_score=50.0,
)

# 保守模式（震荡市/防御）
CONSERVATIVE_PARAMS_V4 = SignalParamsV4(
    max_positions=3,
    single_position_max=0.25,
    stop_loss_pct=-0.08,
    take_profit_pct=0.25,
    min_signal_score=60.0,
    position_cap_bull=0.8,
    position_cap_neutral=0.5,
    position_cap_bear=0.2,
)


def load_best_params_v4() -> SignalParamsV4:
    """
    加载最优参数（自动选择最新的优化结果）
    
    Returns:
        SignalParamsV4: 最优参数实例
    """
    project_root = Path(__file__).parent.parent.parent
    
    # 优先级：V4 > V3 > VBT_V2 > chase_rise
    candidates = [
        project_root / "output/bull_market_v4/best_params_v4_latest.json",
        project_root / "output/bull_market_v3/best_params_v3_20260111_222058.json",
        project_root / "output/bull_market_optimization_vbt_v2/best_params_20260111_205302.json",
    ]
    
    for path in candidates:
        if path.exists():
            logger.info(f"加载最优参数: {path}")
            return SignalParamsV4.from_json(str(path))
    
    logger.warning("未找到优化参数文件，使用默认参数")
    return DEFAULT_PARAMS_V4


# ============================================================================
# 测试函数
# ============================================================================

def test_params_v4():
    """测试参数类功能"""
    print("=" * 60)
    print("测试 SignalParamsV4")
    print("=" * 60)
    
    # 测试默认参数
    params = SignalParamsV4()
    print(f"\n1. 默认参数验证:")
    warnings = params.validate()
    if warnings:
        for w in warnings:
            print(f"   ⚠️  {w}")
    else:
        print("   ✅ 参数验证通过")
    
    # 测试策略模式
    print(f"\n2. 策略模式测试:")
    test_scores = [50, 30, 0, -30, -60]
    for score in test_scores:
        mode = params.get_strategy_mode(score)
        cap = params.get_position_cap(score)
        print(f"   得分{score:+3d}: {mode.value}, 仓位上限{cap:.0%}")
    
    # 测试JSON序列化
    print(f"\n3. JSON序列化测试:")
    dict_data = params.to_dict()
    print(f"   参数数量: {len(dict_data)}")
    
    # 测试从V3文件加载
    print(f"\n4. 加载V3优化参数测试:")
    try:
        v3_params = load_best_params_v4()
        print(f"   ✅ 加载成功")
        print(f"   止损: {v3_params.stop_loss_pct:.0%}")
        print(f"   止盈: {v3_params.take_profit_pct:.0%}")
        print(f"   持仓数: {v3_params.max_positions}")
    except Exception as e:
        print(f"   ❌ 加载失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_params_v4()
