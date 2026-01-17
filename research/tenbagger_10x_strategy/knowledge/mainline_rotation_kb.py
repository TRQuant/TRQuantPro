#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Market Mainline Rotation Knowledge Base - 市场主线轮动知识库
============================================================

基于A股市场特征构建的主线轮动跟踪系统：

1. 主线生命周期模型
2. 热度评估体系
3. 轮动规律知识
4. 主线切换信号
5. 十倍股与主线关联

参考研究：
- 行业轮动策略
- 动量因子应用
- 板块联动效应
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import numpy as np
import pandas as pd


# ============== 主线生命周期阶段 ==============

class MainlinePhase(Enum):
    """主线生命周期阶段"""
    EMERGENCE = "萌芽期"        # 刚开始有资金关注
    ACCELERATION = "加速期"     # 资金持续流入，涨幅加速
    CONSENSUS = "共识期"        # 市场形成共识，参与度最高
    EXHAUSTION = "衰竭期"       # 涨幅过大，资金开始撤离
    DECAY = "衰退期"            # 热度消退，主线结束


# ============== 主线热度评分 ==============

@dataclass
class MainlineHeatScore:
    """主线热度评分"""
    momentum_score: float       # 动量得分 (0-100)
    volume_score: float         # 成交量得分 (0-100)
    participation_score: float  # 参与度得分 (0-100)
    durability_score: float     # 持续性得分 (0-100)
    leadership_score: float     # 龙头强度得分 (0-100)
    
    @property
    def total_score(self) -> float:
        """综合得分（加权平均）"""
        weights = {
            'momentum': 0.30,
            'volume': 0.20,
            'participation': 0.20,
            'durability': 0.15,
            'leadership': 0.15
        }
        return (
            self.momentum_score * weights['momentum'] +
            self.volume_score * weights['volume'] +
            self.participation_score * weights['participation'] +
            self.durability_score * weights['durability'] +
            self.leadership_score * weights['leadership']
        )
    
    @property
    def phase(self) -> MainlinePhase:
        """根据得分判断阶段"""
        total = self.total_score
        if total >= 80:
            return MainlinePhase.CONSENSUS
        elif total >= 60:
            if self.momentum_score > self.durability_score:
                return MainlinePhase.ACCELERATION
            else:
                return MainlinePhase.EXHAUSTION
        elif total >= 40:
            if self.volume_score > 50:
                return MainlinePhase.EMERGENCE
            else:
                return MainlinePhase.DECAY
        else:
            return MainlinePhase.DECAY


# ============== 主线轮动规律 ==============

MAINLINE_ROTATION_PATTERNS = {
    # 经济周期轮动规律
    "economic_cycle": {
        "recovery": ["金融", "地产", "可选消费"],
        "expansion": ["科技", "周期", "工业"],
        "peak": ["能源", "材料", "大宗商品"],
        "recession": ["医药", "公用事业", "必需消费"]
    },
    
    # A股特有轮动规律
    "astock_pattern": {
        "policy_driven": {
            "description": "政策驱动型轮动",
            "duration": "1-3个月",
            "examples": ["新能源补贴→新能源车", "碳中和→光伏风电", "国产替代→半导体"]
        },
        "event_driven": {
            "description": "事件驱动型轮动",
            "duration": "1-2周",
            "examples": ["业绩季→业绩预增", "节假日→旅游消费", "疫情→医药疫苗"]
        },
        "style_rotation": {
            "description": "风格轮动",
            "duration": "3-6个月",
            "examples": ["成长→价值", "大盘→小盘", "低估值→高成长"]
        }
    },
    
    # 主线传导规律
    "transmission": {
        "龙头→跟风": "龙头股启动后，同板块二三线股票跟涨",
        "上游→下游": "原材料涨价传导至下游制造",
        "行业→配套": "核心行业带动配套设备、服务",
        "A股→港股": "A股热点传导至港股同板块"
    }
}


# ============== 主线切换信号 ==============

@dataclass
class MainlineSwitchSignal:
    """主线切换信号"""
    name: str
    description: str
    weight: float
    threshold: Any
    action: str


MAINLINE_SWITCH_SIGNALS = {
    # 热度衰退信号
    "heat_decay": MainlineSwitchSignal(
        name="热度衰退",
        description="主线综合热度连续3天下降",
        weight=0.25,
        threshold={"decay_days": 3, "decay_rate": 0.15},
        action="减少该主线配置，关注新兴主线"
    ),
    
    # 龙头见顶信号
    "leader_top": MainlineSwitchSignal(
        name="龙头见顶",
        description="龙头股MACD顶背离或放量滞涨",
        weight=0.30,
        threshold={"macd_divergence": True, "volume_spike": True},
        action="立即减仓龙头股，准备切换主线"
    ),
    
    # 资金流出信号
    "capital_outflow": MainlineSwitchSignal(
        name="资金流出",
        description="板块连续3天净流出",
        weight=0.20,
        threshold={"outflow_days": 3, "outflow_amount": 1e9},
        action="减少配置，等待资金重新流入"
    ),
    
    # 新主线崛起信号
    "new_mainline": MainlineSwitchSignal(
        name="新主线崛起",
        description="新板块连续放量上涨，热度快速提升",
        weight=0.15,
        threshold={"up_days": 3, "volume_ratio": 2.0, "heat_increase": 20},
        action="关注新主线，逐步配置"
    ),
    
    # 政策转向信号
    "policy_shift": MainlineSwitchSignal(
        name="政策转向",
        description="政策利好转向其他行业",
        weight=0.10,
        threshold={"policy_change": True},
        action="重新评估主线逻辑，考虑切换"
    ),
}


# ============== 十倍股与主线关联 ==============

TENBAGGER_MAINLINE_RULES = {
    # 选择主线时的十倍股倾向
    "mainline_selection": {
        "prefer_emerging": True,      # 优先选择萌芽期主线
        "avoid_exhaustion": True,     # 避免衰竭期主线
        "min_duration": 30,           # 主线持续时间至少30天
        "focus_on_leader": True       # 优先关注龙头股
    },
    
    # 十倍股在主线中的特征
    "tenbagger_in_mainline": {
        "market_cap_rank": "中等偏小",  # 不是龙头但有潜力
        "momentum_rank": "前20%",        # 涨幅靠前
        "volume_increase": ">1.5x",      # 成交放大
        "fundamental_improvement": True   # 基本面改善
    },
    
    # 最佳介入时机
    "best_entry_timing": {
        "phase": MainlinePhase.ACCELERATION,  # 加速期介入
        "leader_status": "龙头确立后",         # 龙头确立后跟进二线
        "pullback": "5-10%回调",               # 回调买入
        "volume": "缩量企稳"                   # 量能配合
    }
}


# ============== 主线轮动追踪器 ==============

class MainlineRotationTracker:
    """主线轮动追踪器
    
    功能：
    1. 追踪多个主线的热度变化
    2. 识别主线生命周期阶段
    3. 生成轮动建议
    4. 关联十倍股候选
    """
    
    def __init__(self, max_mainlines: int = 10):
        self.max_mainlines = max_mainlines
        self.mainline_history = {}  # {主线名: [历史热度]}
        self.current_focus = []     # 当前关注的主线
        
    def calculate_mainline_heat(self, mainline_data: Dict) -> MainlineHeatScore:
        """计算主线热度
        
        Args:
            mainline_data: {
                'stocks': [股票列表],
                'returns': [收益率序列],
                'volumes': [成交量序列],
                'leaders': [龙头股列表]
            }
        """
        stocks = mainline_data.get('stocks', [])
        returns = mainline_data.get('returns', [])
        volumes = mainline_data.get('volumes', [])
        leaders = mainline_data.get('leaders', [])
        
        # 1. 动量得分
        if returns:
            avg_return = np.mean(returns[-5:]) if len(returns) >= 5 else np.mean(returns)
            momentum_score = min(100, max(0, 50 + avg_return * 1000))
        else:
            momentum_score = 50
            
        # 2. 成交量得分
        if len(volumes) >= 10:
            vol_ratio = np.mean(volumes[-5:]) / np.mean(volumes[-10:-5]) if np.mean(volumes[-10:-5]) > 0 else 1
            volume_score = min(100, max(0, 50 * vol_ratio))
        else:
            volume_score = 50
            
        # 3. 参与度得分（上涨股票占比）
        if returns:
            up_ratio = sum(1 for r in returns[-5:] if r > 0) / len(returns[-5:])
            participation_score = up_ratio * 100
        else:
            participation_score = 50
            
        # 4. 持续性得分
        if len(returns) >= 10:
            # 计算10日内正收益天数
            positive_days = sum(1 for r in returns[-10:] if r > 0)
            durability_score = positive_days * 10
        else:
            durability_score = 50
            
        # 5. 龙头强度得分
        if leaders:
            leader_return = np.mean([l.get('return', 0) for l in leaders[-5:]])
            leadership_score = min(100, max(0, 50 + leader_return * 500))
        else:
            leadership_score = 50
            
        return MainlineHeatScore(
            momentum_score=momentum_score,
            volume_score=volume_score,
            participation_score=participation_score,
            durability_score=durability_score,
            leadership_score=leadership_score
        )
    
    def detect_phase(self, mainline_name: str, heat_score: MainlineHeatScore) -> MainlinePhase:
        """检测主线所处阶段"""
        # 更新历史
        if mainline_name not in self.mainline_history:
            self.mainline_history[mainline_name] = []
        self.mainline_history[mainline_name].append(heat_score.total_score)
        
        history = self.mainline_history[mainline_name]
        
        # 根据热度变化判断阶段
        if len(history) < 3:
            return heat_score.phase
            
        recent_avg = np.mean(history[-3:])
        older_avg = np.mean(history[-6:-3]) if len(history) >= 6 else np.mean(history[:-3])
        
        trend = (recent_avg - older_avg) / max(older_avg, 1)
        
        if trend > 0.1:
            # 热度上升
            if heat_score.total_score < 50:
                return MainlinePhase.EMERGENCE
            else:
                return MainlinePhase.ACCELERATION
        elif trend < -0.1:
            # 热度下降
            if heat_score.total_score > 60:
                return MainlinePhase.EXHAUSTION
            else:
                return MainlinePhase.DECAY
        else:
            # 热度稳定
            if heat_score.total_score > 70:
                return MainlinePhase.CONSENSUS
            else:
                return heat_score.phase
    
    def should_switch(self, mainline_name: str, heat_score: MainlineHeatScore) -> Tuple[bool, List[str]]:
        """判断是否应该切换主线
        
        Returns:
            (是否切换, 触发的信号列表)
        """
        signals_triggered = []
        switch_score = 0
        
        history = self.mainline_history.get(mainline_name, [])
        
        # 1. 检测热度衰退
        if len(history) >= 3:
            recent = history[-3:]
            if all(recent[i] < recent[i-1] for i in range(1, len(recent))):
                decay_rate = (recent[0] - recent[-1]) / recent[0] if recent[0] > 0 else 0
                if decay_rate > 0.15:
                    signals_triggered.append("heat_decay")
                    switch_score += MAINLINE_SWITCH_SIGNALS["heat_decay"].weight * 100
                    
        # 2. 检测龙头见顶（通过热度分数间接判断）
        if heat_score.leadership_score < 40 and heat_score.momentum_score > 60:
            signals_triggered.append("leader_top")
            switch_score += MAINLINE_SWITCH_SIGNALS["leader_top"].weight * 100
            
        # 3. 检测资金流出
        if heat_score.volume_score < 40:
            signals_triggered.append("capital_outflow")
            switch_score += MAINLINE_SWITCH_SIGNALS["capital_outflow"].weight * 100
            
        # 4. 检测阶段（衰竭或衰退）
        phase = self.detect_phase(mainline_name, heat_score)
        if phase in [MainlinePhase.EXHAUSTION, MainlinePhase.DECAY]:
            signals_triggered.append("phase_decay")
            switch_score += 20
            
        return switch_score >= 50, signals_triggered
    
    def find_new_mainlines(self, all_mainlines: List[Dict]) -> List[Dict]:
        """寻找新兴主线
        
        Args:
            all_mainlines: [{name, heat_score, phase}, ...]
            
        Returns:
            排序后的新兴主线列表
        """
        candidates = []
        
        for ml in all_mainlines:
            heat = ml.get('heat_score')
            phase = ml.get('phase')
            
            if not heat:
                continue
                
            # 筛选萌芽期或加速期的主线
            if phase in [MainlinePhase.EMERGENCE, MainlinePhase.ACCELERATION]:
                # 检查热度是否在上升
                history = self.mainline_history.get(ml['name'], [])
                if len(history) >= 2:
                    if history[-1] > history[-2]:
                        candidates.append({
                            'name': ml['name'],
                            'heat_score': heat.total_score,
                            'phase': phase.value,
                            'momentum': heat.momentum_score,
                            'volume': heat.volume_score
                        })
                else:
                    # 新主线，直接加入候选
                    candidates.append({
                        'name': ml['name'],
                        'heat_score': heat.total_score,
                        'phase': phase.value,
                        'momentum': heat.momentum_score,
                        'volume': heat.volume_score
                    })
                    
        # 按热度排序
        candidates.sort(key=lambda x: x['heat_score'], reverse=True)
        return candidates[:self.max_mainlines]
    
    def get_tenbagger_candidates(self, mainline_stocks: List[Dict]) -> List[Dict]:
        """从主线中筛选十倍股候选
        
        Args:
            mainline_stocks: [{code, name, return, volume, market_cap, fundamentals}, ...]
        """
        candidates = []
        
        for stock in mainline_stocks:
            score = 0
            
            # 1. 市值评分（中等偏小加分）
            market_cap = stock.get('market_cap', 0)
            if 30e8 < market_cap < 200e8:  # 30-200亿
                score += 25
            elif market_cap < 30e8:
                score += 15
                
            # 2. 动量评分（前20%加分）
            ret = stock.get('return', 0)
            if ret > 0.10:  # 10%以上涨幅
                score += 25
            elif ret > 0.05:
                score += 15
                
            # 3. 成交放大评分
            vol_ratio = stock.get('volume_ratio', 1)
            if vol_ratio > 1.5:
                score += 20
            elif vol_ratio > 1.2:
                score += 10
                
            # 4. 基本面改善评分
            fundamentals = stock.get('fundamentals', {})
            if fundamentals.get('profit_growth', 0) > 0.30:  # 利润增长30%+
                score += 20
            elif fundamentals.get('profit_growth', 0) > 0.15:
                score += 10
                
            # 5. 回调买入机会
            pullback = stock.get('pullback', 0)
            if 0.05 < pullback < 0.10:  # 5-10%回调
                score += 10
                
            if score >= 50:  # 总分50以上加入候选
                candidates.append({
                    **stock,
                    'tenbagger_score': score
                })
                
        # 按得分排序
        candidates.sort(key=lambda x: x['tenbagger_score'], reverse=True)
        return candidates[:10]  # 返回前10名


# ============== 主线轮动策略建议 ==============

@dataclass
class MainlineAllocation:
    """主线配置建议"""
    mainline_name: str
    phase: MainlinePhase
    allocation_ratio: float  # 配置比例 (0-1)
    action: str              # 建议动作
    risk_level: str          # 风险等级


def get_allocation_suggestion(phase: MainlinePhase, heat_score: float) -> Tuple[float, str, str]:
    """根据阶段获取配置建议
    
    Returns:
        (配置比例, 建议动作, 风险等级)
    """
    suggestions = {
        MainlinePhase.EMERGENCE: (0.20, "轻仓试探，逐步加仓", "medium"),
        MainlinePhase.ACCELERATION: (0.40, "加仓持有，跟踪龙头", "low"),
        MainlinePhase.CONSENSUS: (0.30, "保持仓位，设好止盈", "medium"),
        MainlinePhase.EXHAUSTION: (0.15, "逐步减仓，锁定利润", "high"),
        MainlinePhase.DECAY: (0.0, "清仓离场，寻找新机会", "high")
    }
    
    ratio, action, risk = suggestions.get(phase, (0.10, "观望", "high"))
    
    # 根据热度微调
    if heat_score > 80:
        ratio = min(ratio * 1.2, 0.50)
    elif heat_score < 40:
        ratio = max(ratio * 0.5, 0)
        
    return ratio, action, risk


# ============== 导出 ==============

__all__ = [
    'MainlinePhase',
    'MainlineHeatScore',
    'MAINLINE_ROTATION_PATTERNS',
    'MAINLINE_SWITCH_SIGNALS',
    'TENBAGGER_MAINLINE_RULES',
    'MainlineRotationTracker',
    'MainlineAllocation',
    'get_allocation_suggestion'
]







































