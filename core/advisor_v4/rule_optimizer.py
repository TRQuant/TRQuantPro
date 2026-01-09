"""
规则阈值优化器（V4.0 周频版）
==========================

实现目标（phase3.3）：
- 基于历史样本（prediction_date -> target_week_end 的真实收益）对规则阈值做小规模网格搜索
- 输出最优阈值组合与基础指标（precision/recall/f1）

设计原则：
- 小步快跑：先支持小样本快速验证，再扩展到更长历史与更大股票池
- 可复用：与 RuleBasedStrategy / MultiFactorCalculator / PredictorFactorExtractor 解耦
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from core.advisor_v4.multi_factor_calculator import MultiFactorCalculator
from core.advisor_v4.predictor_factor_extractor import PredictorFactorExtractor
from core.advisor_v4.rule_based_strategy import RuleBasedStrategy, RuleConfig


@dataclass
class RuleOptimizationResult:
    best_config: RuleConfig
    best_metrics: Dict[str, float]
    trials: pd.DataFrame


class RuleThresholdOptimizer:
    """规则阈值网格搜索（周频）"""

    def __init__(
        self,
        factor_calculator: Optional[MultiFactorCalculator] = None,
        extractor: Optional[PredictorFactorExtractor] = None,
    ):
        self.factor_calculator = factor_calculator or MultiFactorCalculator(verbose=False)
        self.extractor = extractor or PredictorFactorExtractor(verbose=False)

    @staticmethod
    def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        tp = float(((y_true == 1) & (y_pred == 1)).sum())
        fp = float(((y_true == 0) & (y_pred == 1)).sum())
        fn = float(((y_true == 1) & (y_pred == 0)).sum())
        tn = float(((y_true == 0) & (y_pred == 0)).sum())

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        acc = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0

        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "accuracy": acc,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
        }

    def _prepare_weekly_labeled_samples(
        self,
        samples: pd.DataFrame,
        weekly_threshold_pct: float = 5.0,
    ) -> pd.DataFrame:
        """给样本补齐：未来周收益（%）+ label（0/1）+ 规则所需因子（total_score 等）"""
        required = {"code", "prediction_date", "target_date"}
        missing = required - set(samples.columns)
        if missing:
            raise ValueError(f"samples缺少字段: {missing}")

        df = samples.copy()

        # 计算真实周收益（%）
        future_returns: List[Optional[float]] = []
        for _, row in df.iterrows():
            r = self.extractor.compute_future_week_return_pct(
                code=row["code"],
                prediction_date=row["prediction_date"],
                target_date=row["target_date"],
            )
            future_returns.append(r)
        df["future_week_return_pct"] = future_returns
        df = df.dropna(subset=["future_week_return_pct"]).reset_index(drop=True)
        df["label"] = (df["future_week_return_pct"] >= weekly_threshold_pct).astype(int)

        # 按 prediction_date 分组批量拉取因子（避免逐行调用）
        factor_rows: List[pd.DataFrame] = []
        for pred_date, g in df.groupby("prediction_date"):
            codes = g["code"].astype(str).tolist()
            factors = self.factor_calculator.calculate_all_factors(codes, str(pred_date))
            factors["prediction_date"] = str(pred_date)
            factor_rows.append(factors)

        factor_df = pd.concat(factor_rows, ignore_index=True) if factor_rows else pd.DataFrame()
        df = df.merge(factor_df, on=["code", "prediction_date"], how="left")
        return df

    def grid_search(
        self,
        samples: pd.DataFrame,
        weekly_threshold_pct: float = 5.0,
        min_total_score_grid: Sequence[float] = (60, 65, 70, 75),
        min_alpha_score_grid: Sequence[float] = (50, 55, 60),
        min_cne5_score_grid: Sequence[float] = (45, 50, 55),
        min_fundamental_score_grid: Sequence[float] = (45, 50, 55),
    ) -> RuleOptimizationResult:
        """网格搜索最优阈值组合（以F1为主目标）"""
        base = self._prepare_weekly_labeled_samples(samples, weekly_threshold_pct=weekly_threshold_pct)

        trials: List[Dict] = []
        best = None
        best_cfg = None

        for t in min_total_score_grid:
            for a in min_alpha_score_grid:
                for c in min_cne5_score_grid:
                    for f in min_fundamental_score_grid:
                        cfg = RuleConfig(
                            min_total_score=float(t),
                            min_alpha_score=float(a),
                            min_cne5_score=float(c),
                            min_fundamental_score=float(f),
                        )
                        strat = RuleBasedStrategy(cfg)
                        scored = strat.score_candidates(base)

                        y_true = scored["label"].values.astype(int)
                        y_pred = scored["rule_passed"].values.astype(int)
                        m = self._metrics(y_true, y_pred)

                        row = {
                            "min_total_score": t,
                            "min_alpha_score": a,
                            "min_cne5_score": c,
                            "min_fundamental_score": f,
                            **m,
                        }
                        trials.append(row)

                        if best is None or m["f1"] > best["f1"]:
                            best = m
                            best_cfg = cfg

        trials_df = pd.DataFrame(trials).sort_values(["f1", "precision", "recall"], ascending=False)
        return RuleOptimizationResult(best_config=best_cfg, best_metrics=best or {}, trials=trials_df)

