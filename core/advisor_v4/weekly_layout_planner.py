#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Layout Planner (phase5)
==============================

定义“提前一周布局”的核心数据结构，并提供基础的计划生成入口。

注意：
- 时间口径：**自然周**（考虑节假日由上层 workflow 负责换算交易日）
- 本模块只定义结构与基础拼装逻辑；更复杂的入场/调仓规则在 phase5-entry/phase5-rebalance 完成
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any


@dataclass
class LayoutTarget:
    """周度布局标的"""

    code: str
    name: str = ""
    weight: float = 0.0  # 目标权重（0~1，通常加总<=position_advice）
    score: float = 0.0
    reason: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class EntryPlan:
    """入场计划（分批建仓）"""

    plan_type: str = "staged"  # staged/market/limit
    stages: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""


@dataclass
class ExitPlan:
    """出场计划（止盈/止损/时间止损等）"""

    take_profit: float = 0.15
    stop_loss: float = -0.08
    trailing_stop: float = 0.03
    time_stop_days: int = 10
    notes: str = ""


@dataclass
class WeeklyLayoutPlan:
    """周度布局计划（对外的统一结构）"""

    week_start: str
    week_end: str
    market_outlook: str
    position_advice: float  # 建议仓位（0~1）

    # 投资标的
    targets: List[LayoutTarget] = field(default_factory=list)

    # 交易计划
    entry_plan: Dict[str, EntryPlan] = field(default_factory=dict)
    exit_plan: Dict[str, ExitPlan] = field(default_factory=dict)

    # 风险控制
    risk_controls: List[str] = field(default_factory=list)

    # 调仓计划（phase5-rebalance）
    rebalance_plan: List[Dict[str, Any]] = field(default_factory=list)

    # 元数据
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WeeklyLayoutPlanner:
    """周度布局计划生成器（phase5-structure）"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def create_empty(
        self,
        week_start: str,
        week_end: str,
        market_outlook: str = "neutral",
        position_advice: float = 0.5,
    ) -> WeeklyLayoutPlan:
        return WeeklyLayoutPlan(
            week_start=week_start,
            week_end=week_end,
            market_outlook=market_outlook,
            position_advice=position_advice,
            targets=[],
            entry_plan={},
            exit_plan={},
            risk_controls=[],
            meta={},
        )

    def build_basic(
        self,
        week_start: str,
        week_end: str,
        targets: List[LayoutTarget],
        market_outlook: str = "neutral",
        position_advice: float = 0.5,
        default_exit: Optional[ExitPlan] = None,
    ) -> WeeklyLayoutPlan:
        """基础拼装：目标列表 + 默认退出规则（入场/调仓细节后续phase补齐）。"""
        default_exit = default_exit or ExitPlan()

        plan = self.create_empty(
            week_start=week_start,
            week_end=week_end,
            market_outlook=market_outlook,
            position_advice=position_advice,
        )
        plan.targets = targets

        for t in targets:
            plan.entry_plan[t.code] = EntryPlan(
                plan_type="staged",
                stages=[],
                notes="phase5-entry 将补充：分批建仓/触发条件/价格区间",
            )
            plan.exit_plan[t.code] = default_exit

        plan.risk_controls = [
            "若市场环境转弱（指数跌破关键均线/情绪转负），将仓位降至 0~30%",
            "单票最大仓位不超过 20%，避免单点风险",
            "触发止损或时间止损后，优先保护本金，等待下一周再评估",
        ]
        plan.rebalance_plan = self._default_rebalance_plan()
        plan.meta = {"planner_version": "phase5-structure"}
        return plan

    def _default_rebalance_plan(self) -> List[Dict[str, Any]]:
        """默认调仓计划（每日检查 + 周中调整 + 周末总结）。"""
        return [
            {
                "cadence": "daily",
                "time": "收盘后",
                "checks": [
                    "检查大盘环境：若风险开关转弱，整体仓位下调",
                    "检查持仓：止损/移动止盈/时间止损是否触发",
                    "检查流动性与异动：跌停/大幅跳空/成交异常则降风险",
                ],
            },
            {
                "cadence": "mid_week",
                "time": "周三~周四",
                "actions": [
                    "若强势股回撤不破支撑：按入场计划S2加仓",
                    "若突破确认放量：按入场计划S3加仓（避免追高）",
                    "若个股逻辑破坏/跌破关键位：减仓或清仓，保留现金",
                ],
            },
            {
                "cadence": "week_end",
                "time": "周五收盘后",
                "summary": [
                    "复盘：本周执行是否符合计划（入场/止损/止盈/调仓）",
                    "评估：下周继续持有/换股/降低仓位（结合市场状态与个股趋势）",
                    "记录：关键事件与价格行为，用于规则与模型迭代（奖励机制输入）",
                ],
            },
        ]

    # ==================== phase5-entry: 入场计划生成 ====================

    def _build_staged_entry_plan(
        self,
        ref_price: float,
        position_weight: float,
        take_profit: float,
        stop_loss: float,
    ) -> EntryPlan:
        """生成分批入场计划（价格区间 + 触发条件）。"""
        if ref_price is None or ref_price <= 0:
            return EntryPlan(
                plan_type="staged",
                stages=[],
                notes="缺少参考价（entry_price），请在phase6集成推荐流程时补全",
            )

        # 以“参考价”为中心构建三段入场
        # - S1: 试仓（靠近参考价）
        # - S2: 回踩加仓（-2%~-5%区间）
        # - S3: 确认加仓（+2%~+5%区间）
        s1 = {
            "stage": "S1_starter",
            "weight": round(position_weight * 0.40, 6),
            "price_low": round(ref_price * 0.99, 4),
            "price_high": round(ref_price * 1.01, 4),
            "trigger": "开盘后价格稳定在参考价附近（不追高），且分时不放量跳水",
            "time_window": "周一~周二",
        }
        s2 = {
            "stage": "S2_pullback_add",
            "weight": round(position_weight * 0.30, 6),
            "price_low": round(ref_price * 0.95, 4),
            "price_high": round(ref_price * 0.98, 4),
            "trigger": "回踩不破关键支撑（如MA5/MA10或前高），缩量企稳后分批加仓",
            "time_window": "周二~周四",
        }
        s3 = {
            "stage": "S3_confirm_add",
            "weight": round(position_weight * 0.30, 6),
            "price_low": round(ref_price * 1.02, 4),
            "price_high": round(ref_price * 1.05, 4),
            "trigger": "放量突破/创新高确认（避免假突破），突破后回踩不破可加仓",
            "time_window": "全周（偏后半周）",
        }

        notes = (
            f"止损: {stop_loss:+.0%}（以建仓均价为基准）；"
            f"止盈: {take_profit:+.0%}（可分批止盈）；"
            f"若周内出现系统性风险信号，优先减仓/止损。"
        )
        return EntryPlan(plan_type="staged", stages=[s1, s2, s3], notes=notes)

    def build_with_entry_plans(
        self,
        week_start: str,
        week_end: str,
        targets: List[LayoutTarget],
        ref_prices: Dict[str, float],
        market_outlook: str = "neutral",
        position_advice: float = 0.5,
        default_exit: Optional[ExitPlan] = None,
    ) -> WeeklyLayoutPlan:
        """在基础计划上补齐入场计划（phase5-entry）。"""
        plan = self.build_basic(
            week_start=week_start,
            week_end=week_end,
            targets=targets,
            market_outlook=market_outlook,
            position_advice=position_advice,
            default_exit=default_exit,
        )

        for t in plan.targets:
            rp = float(ref_prices.get(t.code, 0.0)) if ref_prices else 0.0
            ex = plan.exit_plan.get(t.code, ExitPlan())
            plan.entry_plan[t.code] = self._build_staged_entry_plan(
                ref_price=rp,
                position_weight=float(t.weight),
                take_profit=float(ex.take_profit),
                stop_loss=float(ex.stop_loss),
            )

        plan.meta = {**plan.meta, "planner_version": "phase5-entry"}
        return plan

    def build_from_candidates(
        self,
        week_start: str,
        week_end: str,
        candidates: List[Dict[str, Any]],
        market_outlook: str = "neutral",
        position_advice: float = 0.5,
        max_targets: int = 5,
        single_position_cap: float = 0.20,
    ) -> WeeklyLayoutPlan:
        """从候选列表生成周度布局（用于phase6集成前的独立测试）。

        candidates 期望字段：
        - code (必需)
        - name, score, reason, entry_price (可选)
        """
        candidates = candidates or []
        picks = candidates[: max(1, int(max_targets))] if candidates else []
        if not picks:
            return self.create_empty(week_start, week_end, market_outlook, position_advice)

        n = len(picks)
        base_w = min(float(single_position_cap), float(position_advice) / max(n, 1))

        targets: List[LayoutTarget] = []
        ref_prices: Dict[str, float] = {}
        for c in picks:
            code = str(c.get("code", "")).strip()
            if not code:
                continue
            targets.append(
                LayoutTarget(
                    code=code,
                    name=str(c.get("name", "")),
                    weight=base_w,
                    score=float(c.get("score", 0.0) or 0.0),
                    reason=str(c.get("reason", "")),
                    tags=list(c.get("tags", []) or []),
                )
            )
            if c.get("entry_price"):
                ref_prices[code] = float(c["entry_price"])

        # 默认退出规则（后续可按市场环境动态调整）
        exit_plan = ExitPlan()
        return self.build_with_entry_plans(
            week_start=week_start,
            week_end=week_end,
            targets=targets,
            ref_prices=ref_prices,
            market_outlook=market_outlook,
            position_advice=position_advice,
            default_exit=exit_plan,
        )

