"""
规则引擎（V4.0 周频版）
====================

定位：
- 在“周频”口径下，基于聚宽精简因子组合（CNE5 + Alpha101/191 + 基础财务）生成可解释的入场/出场/仓位规则。
- 输出规则匹配度（0~100）与理由，便于后续回测优化阈值（phase3.3）。

注意：
- 本模块不依赖Notebook
- 规则引擎不替代模型预测；可与ML预测并行使用（phase6.2）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pandas as pd


@dataclass
class RuleConfig:
    """规则配置（周频）"""

    # 核心：聚宽精简组合得分（0~100）
    min_total_score: float = 70.0
    min_cne5_score: float = 50.0
    min_alpha_score: float = 55.0
    min_fundamental_score: float = 50.0

    # 市场环境过滤
    min_market_trend: float = -5.0  # %，沪深300近20日趋势（允许弱势）

    # 流动性（万元）：建议至少 3000 万/日以上（默认=3000）
    min_liquidity: float = 3000.0

    # 交易与风控（用于后续生成交易计划/回测）
    take_profit: float = 0.10   # 止盈 10%
    stop_loss: float = -0.08    # 止损 -8%
    max_positions: int = 8
    position_size: float = 0.12  # 单票建议仓位 12%


@dataclass
class RuleMatch:
    code: str
    passed: bool
    score: float
    reasons: List[str] = field(default_factory=list)


class RuleBasedStrategy:
    """规则策略（周频）"""

    def __init__(self, config: Optional[RuleConfig] = None):
        self.config = config or RuleConfig()

    def _score_row(self, row: pd.Series) -> RuleMatch:
        c = self.config
        reasons: List[str] = []
        score = 0.0

        total = float(row.get("total_score", 0) or 0)
        cne5 = float(row.get("cne5_score", 50) or 50)
        alpha = float(row.get("alpha_score", 50) or 50)
        funda = float(row.get("fundamental_score_jq", row.get("fundamental_score", 50)) or 50)
        mkt = float(row.get("market_trend", 0) or 0)
        liq = float(row.get("avg_money", 0) or 0)  # 万元

        # 规则匹配度评分（0~100）：分项打分 + 汇总
        # 采用“阈值达标得满分；未达标按比例扣分”的稳定策略，便于后续阈值网格优化
        def _ratio_score(value: float, threshold: float, max_points: float) -> float:
            if threshold <= 0:
                return 0.0
            return max(0.0, min(1.0, value / threshold)) * max_points

        score_total = _ratio_score(total, c.min_total_score, 40.0)
        score_alpha = _ratio_score(alpha, c.min_alpha_score, 20.0)
        score_cne5 = _ratio_score(cne5, c.min_cne5_score, 15.0)
        score_funda = _ratio_score(funda, c.min_fundamental_score, 10.0)
        score_mkt = 5.0 if mkt >= c.min_market_trend else 0.0
        if liq <= 0:
            score_liq = 5.0  # 未知给半分，避免过度误杀
        else:
            score_liq = _ratio_score(liq, c.min_liquidity, 10.0)

        score = score_total + score_alpha + score_cne5 + score_funda + score_mkt + score_liq

        # 条件解释
        if total < c.min_total_score:
            reasons.append(f"综合得分不足: {total:.1f} < {c.min_total_score:.1f}")
        else:
            reasons.append(f"综合得分通过: {total:.1f}")

        if cne5 < c.min_cne5_score:
            reasons.append(f"CNE5偏弱: {cne5:.1f} < {c.min_cne5_score:.1f}")
        else:
            reasons.append(f"CNE5通过: {cne5:.1f}")

        if alpha < c.min_alpha_score:
            reasons.append(f"Alpha偏弱: {alpha:.1f} < {c.min_alpha_score:.1f}")
        else:
            reasons.append(f"Alpha通过: {alpha:.1f}")

        if funda < c.min_fundamental_score:
            reasons.append(f"基本面偏弱: {funda:.1f} < {c.min_fundamental_score:.1f}")
        else:
            reasons.append(f"基本面通过: {funda:.1f}")

        if mkt < c.min_market_trend:
            reasons.append(f"市场环境偏弱: {mkt:.2f}% < {c.min_market_trend:.2f}%")
        else:
            reasons.append(f"市场环境允许: {mkt:.2f}%")

        if liq > 0 and liq < c.min_liquidity:
            reasons.append(f"流动性不足: {liq:.0f}万 < {c.min_liquidity:.0f}万")
        elif liq > 0:
            reasons.append(f"流动性通过: {liq:.0f}万")
        else:
            reasons.append("流动性未知: 缺少avg_money")

        passed = (
            total >= c.min_total_score
            and cne5 >= c.min_cne5_score
            and alpha >= c.min_alpha_score
            and funda >= c.min_fundamental_score
            and mkt >= c.min_market_trend
            and (liq == 0 or liq >= c.min_liquidity)
        )

        # clip 0~100
        score = max(0.0, min(100.0, score))

        # 记录分项（写入原因中，便于审计）
        reasons.append(
            "匹配度分解: "
            f"total={score_total:.1f}/40, alpha={score_alpha:.1f}/20, "
            f"cne5={score_cne5:.1f}/15, funda={score_funda:.1f}/10, "
            f"mkt={score_mkt:.1f}/5, liq={score_liq:.1f}/10"
        )

        return RuleMatch(code=str(row.get("code", "")), passed=passed, score=score, reasons=reasons)

    def score_candidates(self, candidates: pd.DataFrame) -> pd.DataFrame:
        """对候选集进行规则评分并返回增强后的DataFrame"""
        if candidates is None or candidates.empty:
            return pd.DataFrame()

        matches = [self._score_row(r) for _, r in candidates.iterrows()]
        out = candidates.copy()
        out["rule_score"] = [m.score for m in matches]
        out["rule_passed"] = [m.passed for m in matches]
        out["rule_reasons"] = ["; ".join(m.reasons) for m in matches]
        return out

    def suggest_trade_params(self) -> Dict:
        """输出交易参数建议（用于周度布局/回测模块复用）"""
        c = self.config
        return {
            "take_profit": c.take_profit,
            "stop_loss": c.stop_loss,
            "max_positions": c.max_positions,
            "position_size": c.position_size,
        }

