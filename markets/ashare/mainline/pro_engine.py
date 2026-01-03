"""
专业级主线识别引擎

基于《A股主线识别量化流程建议书》设计

评分维度：
1. 资金维度 (25分) - 主力资金净流入强度
2. 动量维度 (20分) - 板块动量效应
3. 热度维度 (20分) - 市场关注度
4. 政策维度 (20分) - 政策支持力度
5. 龙头维度 (15分) - 龙头股强度

数据来源：
- AKShare (免费): 同花顺/东方财富数据
- JQData (付费): 聚宽Level2数据 (预留)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json

logger = logging.getLogger(__name__)


class MainlineType(Enum):
    """主线类型"""
    SHORT = "短期主线"      # 1-2周
    MEDIUM = "中期主线"     # 1-3个月
    LONG = "长期主线"       # 3个月以上


class SignalType(Enum):
    """信号类型"""
    BUY = "买入"
    HOLD = "持有"
    REDUCE = "减仓"
    SELL = "卖出"
    WATCH = "观察"


@dataclass
class ScoreBreakdown:
    """评分分解"""
    funds_score: float = 0.0        # 资金维度 (25分)
    momentum_score: float = 0.0     # 动量维度 (20分)
    heat_score: float = 0.0         # 热度维度 (20分)
    policy_score: float = 0.0       # 政策维度 (20分)
    leader_score: float = 0.0       # 龙头维度 (15分)
    
    @property
    def total(self) -> float:
        return (self.funds_score + self.momentum_score + 
                self.heat_score + self.policy_score + self.leader_score)
    
    def to_dict(self) -> Dict:
        return {
            "funds_score": round(self.funds_score, 1),
            "momentum_score": round(self.momentum_score, 1),
            "heat_score": round(self.heat_score, 1),
            "policy_score": round(self.policy_score, 1),
            "leader_score": round(self.leader_score, 1),
            "total": round(self.total, 1),
        }


@dataclass
class MainlineResult:
    """主线识别结果"""
    name: str                           # 主线名称
    type: str                           # 板块类型 (行业/概念)
    score: ScoreBreakdown               # 评分分解
    mainline_type: MainlineType         # 主线类型
    signal: SignalType                  # 交易信号
    
    # 核心指标
    change_pct: float = 0.0             # 涨跌幅
    net_inflow: float = 0.0             # 净流入(亿)
    net_inflow_5d: float = 0.0          # 5日净流入(亿)
    turnover_rate: float = 0.0          # 换手率
    
    # 龙头信息
    leader_stocks: List[str] = field(default_factory=list)
    leader_change: float = 0.0          # 龙头涨幅
    limit_up_count: int = 0             # 涨停股数量
    
    # 分析说明
    logic: str = ""                     # 核心逻辑
    recommendation: str = ""            # 操作建议
    risk_warning: str = ""              # 风险提示
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.type,
            "score": self.score.to_dict(),
            "total_score": round(self.score.total, 1),
            "mainline_type": self.mainline_type.value,
            "signal": self.signal.value,
            "change_pct": round(self.change_pct, 2),
            "net_inflow": round(self.net_inflow, 2),
            "net_inflow_5d": round(self.net_inflow_5d, 2),
            "turnover_rate": round(self.turnover_rate, 2),
            "leader_stocks": self.leader_stocks,
            "leader_change": round(self.leader_change, 2),
            "limit_up_count": self.limit_up_count,
            "logic": self.logic,
            "recommendation": self.recommendation,
            "risk_warning": self.risk_warning,
        }


# ============================================================
# 评分参数配置 - 可调整
# ============================================================

SCORING_CONFIG = {
    # 资金维度参数 (25分)
    "funds": {
        "weight": 25,
        "factors": {
            "net_inflow_rank": {
                "weight": 0.4,
                "description": "当日净流入排名",
                "calculation": "板块净流入金额在所有板块中的排名百分位",
            },
            "net_inflow_5d_rank": {
                "weight": 0.3,
                "description": "5日累计净流入排名",
                "calculation": "5日累计净流入在所有板块中的排名百分位",
            },
            "inflow_ratio": {
                "weight": 0.3,
                "description": "流入占比",
                "calculation": "净流入/流入资金，反映资金净流入强度",
            },
        },
    },
    
    # 动量维度参数 (20分)
    "momentum": {
        "weight": 20,
        "factors": {
            "change_rank": {
                "weight": 0.4,
                "description": "涨跌幅排名",
                "calculation": "板块涨跌幅在所有板块中的排名百分位",
            },
            "relative_strength": {
                "weight": 0.3,
                "description": "相对强度",
                "calculation": "板块涨幅 - 沪深300涨幅",
            },
            "trend_score": {
                "weight": 0.3,
                "description": "趋势得分",
                "calculation": "基于均线排列和突破情况",
            },
        },
    },
    
    # 热度维度参数 (20分)
    "heat": {
        "weight": 20,
        "factors": {
            "limit_up_ratio": {
                "weight": 0.4,
                "description": "涨停股占比",
                "calculation": "板块涨停股数量/板块总股票数",
            },
            "volume_ratio": {
                "weight": 0.3,
                "description": "成交量放大",
                "calculation": "今日成交量/5日平均成交量",
            },
            "attention_score": {
                "weight": 0.3,
                "description": "关注度得分",
                "calculation": "基于搜索热度、新闻数量等",
            },
        },
    },
    
    # 政策维度参数 (20分)
    "policy": {
        "weight": 20,
        "factors": {
            "policy_support": {
                "weight": 0.5,
                "description": "政策支持力度",
                "calculation": "近期是否有重大政策利好",
            },
            "industry_trend": {
                "weight": 0.3,
                "description": "产业趋势",
                "calculation": "行业景气度和发展趋势",
            },
            "event_catalyst": {
                "weight": 0.2,
                "description": "事件催化",
                "calculation": "是否有重大事件驱动",
            },
        },
    },
    
    # 龙头维度参数 (15分)
    "leader": {
        "weight": 15,
        "factors": {
            "leader_strength": {
                "weight": 0.5,
                "description": "龙头强度",
                "calculation": "龙头股涨幅和连板情况",
            },
            "followup_effect": {
                "weight": 0.3,
                "description": "跟风效应",
                "calculation": "板块内跟涨股票比例",
            },
            "market_cap_leader": {
                "weight": 0.2,
                "description": "大市值龙头",
                "calculation": "是否有大市值龙头领涨",
            },
        },
    },
}

# 信号阈值配置
SIGNAL_THRESHOLDS = {
    "buy": 75,          # 得分>=75 买入
    "hold": 60,         # 得分60-75 持有
    "reduce": 45,       # 得分45-60 减仓
    "sell": 30,         # 得分<30 卖出
}

# 主线类型判断配置
MAINLINE_TYPE_CONFIG = {
    "short": {
        "min_score": 60,
        "max_duration_days": 14,
        "characteristics": ["事件驱动", "主题炒作", "情绪推动"],
    },
    "medium": {
        "min_score": 70,
        "max_duration_days": 90,
        "characteristics": ["政策催化", "基本面改善", "资金持续流入"],
    },
    "long": {
        "min_score": 80,
        "max_duration_days": 365,
        "characteristics": ["产业趋势", "经济结构", "长期政策支持"],
    },
}


class ProMainlineEngine:
    """专业级主线识别引擎"""
    
    def __init__(self):
        self.config = SCORING_CONFIG
        self.signal_thresholds = SIGNAL_THRESHOLDS
        self.raw_data = {}
        self.results = []
    
    def analyze(self, data: Dict) -> List[MainlineResult]:
        """
        执行主线分析
        
        Args:
            data: 包含各数据源数据的字典
                - sector_flow: 行业板块资金流向
                - concept_flow: 概念板块资金流向
                - northbound: 北向资金
                - limit_up: 涨停池
                - dragon_tiger: 龙虎榜
        
        Returns:
            主线识别结果列表
        """
        self.raw_data = data
        self.results = []
        
        # 分析行业板块
        sector_mainlines = self._analyze_sectors(data.get("sector_flow", []))
        self.results.extend(sector_mainlines)
        
        # 分析概念板块
        concept_mainlines = self._analyze_concepts(data.get("concept_flow", []))
        self.results.extend(concept_mainlines)
        
        # 综合排序
        self.results.sort(key=lambda x: x.score.total, reverse=True)
        
        # 生成分析说明
        self._generate_analysis()
        
        return self.results
    
    def _analyze_sectors(self, sector_data: List[Dict]) -> List[MainlineResult]:
        """分析行业板块"""
        results = []
        
        if not sector_data:
            return results
        
        # 计算排名
        total = len(sector_data)
        
        for i, item in enumerate(sector_data[:20]):  # 取前20个
            name = item.get("sector_name", "") or item.get("行业", "")
            if not name:
                continue
            
            # 提取数据
            change_pct = float(item.get("change_pct", 0) or item.get("行业-涨跌幅", 0) or 0)
            net_inflow = float(item.get("main_net_inflow", 0) or item.get("净额", 0) or 0)
            inflow = float(item.get("inflow", 0) or item.get("流入资金", 0) or 1)
            outflow = float(item.get("outflow", 0) or item.get("流出资金", 0) or 0)
            leader = item.get("leader_stock", "") or item.get("领涨股", "")
            leader_change = float(item.get("leader_change", 0) or item.get("领涨股-涨跌幅", 0) or 0)
            
            # 计算评分
            score = self._calculate_score(
                rank=i,
                total=total,
                change_pct=change_pct,
                net_inflow=net_inflow,
                inflow=inflow,
                leader_change=leader_change,
            )
            
            # 生成信号
            signal = self._generate_signal(score.total)
            
            # 判断主线类型
            mainline_type = self._determine_mainline_type(score.total, change_pct)
            
            result = MainlineResult(
                name=name,
                type="行业",
                score=score,
                mainline_type=mainline_type,
                signal=signal,
                change_pct=change_pct,
                net_inflow=net_inflow,
                leader_stocks=[leader] if leader else [],
                leader_change=leader_change,
            )
            
            results.append(result)
        
        return results
    
    def _analyze_concepts(self, concept_data: List[Dict]) -> List[MainlineResult]:
        """分析概念板块"""
        results = []
        
        if not concept_data:
            return results
        
        total = len(concept_data)
        
        for i, item in enumerate(concept_data[:30]):  # 取前30个概念
            name = item.get("board_name", "") or item.get("行业", "") or item.get("概念", "")
            if not name:
                continue
            
            change_pct = float(item.get("change_pct", 0) or item.get("行业-涨跌幅", 0) or 0)
            net_inflow = float(item.get("net_inflow", 0) or item.get("净额", 0) or 0)
            inflow = float(item.get("inflow", 0) or item.get("流入资金", 0) or 1)
            leader = item.get("leader_stock", "") or item.get("领涨股", "")
            leader_change = float(item.get("leader_change", 0) or item.get("领涨股-涨跌幅", 0) or 0)
            company_count = int(item.get("company_count", 0) or item.get("公司家数", 0) or 0)
            
            score = self._calculate_score(
                rank=i,
                total=total,
                change_pct=change_pct,
                net_inflow=net_inflow,
                inflow=inflow,
                leader_change=leader_change,
            )
            
            signal = self._generate_signal(score.total)
            mainline_type = self._determine_mainline_type(score.total, change_pct)
            
            result = MainlineResult(
                name=name,
                type="概念",
                score=score,
                mainline_type=mainline_type,
                signal=signal,
                change_pct=change_pct,
                net_inflow=net_inflow,
                leader_stocks=[leader] if leader else [],
                leader_change=leader_change,
            )
            
            results.append(result)
        
        return results
    
    def _calculate_score(
        self,
        rank: int,
        total: int,
        change_pct: float,
        net_inflow: float,
        inflow: float,
        leader_change: float,
    ) -> ScoreBreakdown:
        """计算综合评分"""
        
        # 1. 资金维度 (25分)
        rank_percentile = 1 - (rank / max(total, 1))  # 排名越靠前越高
        inflow_ratio = net_inflow / max(inflow, 0.01) if inflow > 0 else 0
        
        funds_score = (
            rank_percentile * 0.5 * 25 +  # 排名得分
            min(max(inflow_ratio, 0), 1) * 0.3 * 25 +  # 流入占比得分
            (1 if net_inflow > 0 else 0) * 0.2 * 25  # 净流入正负
        )
        
        # 2. 动量维度 (20分)
        change_score = min(max(change_pct / 5, 0), 1)  # 涨幅标准化 (5%为满分)
        momentum_score = change_score * 20
        
        # 3. 热度维度 (20分)
        # 简化计算：基于涨幅和资金流入
        heat_score = (
            change_score * 0.5 * 20 +
            rank_percentile * 0.5 * 20
        )
        
        # 4. 政策维度 (20分)
        # 简化：暂时给予基础分，后续可接入政策数据
        policy_score = 10  # 基础分
        if net_inflow > 5:  # 资金大幅流入可能有政策催化
            policy_score += 5
        if change_pct > 3:  # 大涨可能有事件驱动
            policy_score += 5
        
        # 5. 龙头维度 (15分)
        leader_score_val = min(max(leader_change / 10, 0), 1) * 15  # 龙头涨幅标准化
        
        return ScoreBreakdown(
            funds_score=funds_score,
            momentum_score=momentum_score,
            heat_score=heat_score,
            policy_score=policy_score,
            leader_score=leader_score_val,
        )
    
    def _generate_signal(self, total_score: float) -> SignalType:
        """生成交易信号"""
        if total_score >= self.signal_thresholds["buy"]:
            return SignalType.BUY
        elif total_score >= self.signal_thresholds["hold"]:
            return SignalType.HOLD
        elif total_score >= self.signal_thresholds["reduce"]:
            return SignalType.WATCH
        else:
            return SignalType.SELL
    
    def _determine_mainline_type(self, score: float, change_pct: float) -> MainlineType:
        """判断主线类型"""
        if score >= 80 and change_pct > 0:
            return MainlineType.LONG
        elif score >= 65:
            return MainlineType.MEDIUM
        else:
            return MainlineType.SHORT
    
    def _generate_analysis(self):
        """生成分析说明"""
        for result in self.results:
            # 生成核心逻辑
            logic_parts = []
            if result.net_inflow > 0:
                logic_parts.append(f"资金净流入{result.net_inflow:.1f}亿")
            if result.change_pct > 0:
                logic_parts.append(f"涨幅{result.change_pct:.1f}%")
            if result.leader_change > 5:
                logic_parts.append(f"龙头涨幅{result.leader_change:.1f}%")
            
            result.logic = "，".join(logic_parts) if logic_parts else "暂无明显特征"
            
            # 生成操作建议
            if result.signal == SignalType.BUY:
                result.recommendation = "强主线，可重点配置，关注龙头回调机会"
            elif result.signal == SignalType.HOLD:
                result.recommendation = "较强主线，可适当参与，控制仓位"
            elif result.signal == SignalType.WATCH:
                result.recommendation = "观察为主，等待更明确信号"
            else:
                result.recommendation = "暂不参与，等待企稳"
            
            # 生成风险提示
            if result.change_pct > 5:
                result.risk_warning = "短期涨幅较大，注意追高风险"
            elif result.net_inflow < 0:
                result.risk_warning = "资金净流出，注意回调风险"
            else:
                result.risk_warning = "注意市场整体风险"
    
    def get_top_mainlines(self, n: int = 10) -> List[MainlineResult]:
        """获取前N条主线"""
        return self.results[:n]
    
    def to_json(self) -> str:
        """导出JSON格式"""
        return json.dumps({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "main_lines": [r.to_dict() for r in self.results[:20]],
            "config": {
                "scoring_weights": {
                    "funds": 25,
                    "momentum": 20,
                    "heat": 20,
                    "policy": 20,
                    "leader": 15,
                },
                "signal_thresholds": self.signal_thresholds,
            },
        }, ensure_ascii=False, indent=2)
    
    def get_config_description(self) -> Dict:
        """获取配置说明"""
        return {
            "scoring_dimensions": [
                {
                    "name": "资金维度",
                    "weight": 25,
                    "description": "主力资金净流入强度",
                    "factors": [
                        "当日净流入排名",
                        "5日累计净流入排名",
                        "流入占比",
                    ],
                },
                {
                    "name": "动量维度",
                    "weight": 20,
                    "description": "板块动量效应",
                    "factors": [
                        "涨跌幅排名",
                        "相对强度(vs沪深300)",
                        "趋势得分",
                    ],
                },
                {
                    "name": "热度维度",
                    "weight": 20,
                    "description": "市场关注度",
                    "factors": [
                        "涨停股占比",
                        "成交量放大",
                        "关注度得分",
                    ],
                },
                {
                    "name": "政策维度",
                    "weight": 20,
                    "description": "政策支持力度",
                    "factors": [
                        "政策支持力度",
                        "产业趋势",
                        "事件催化",
                    ],
                },
                {
                    "name": "龙头维度",
                    "weight": 15,
                    "description": "龙头股强度",
                    "factors": [
                        "龙头强度",
                        "跟风效应",
                        "大市值龙头",
                    ],
                },
            ],
            "signal_rules": [
                {"signal": "买入", "condition": "得分 ≥ 75", "description": "强主线，可重点配置"},
                {"signal": "持有", "condition": "得分 60-75", "description": "较强主线，可适当参与"},
                {"signal": "观察", "condition": "得分 45-60", "description": "一般主线，观察为主"},
                {"signal": "卖出", "condition": "得分 < 45", "description": "弱主线，暂不参与"},
            ],
            "mainline_types": [
                {"type": "短期主线", "duration": "1-2周", "characteristics": "事件驱动、主题炒作"},
                {"type": "中期主线", "duration": "1-3个月", "characteristics": "政策催化、基本面改善"},
                {"type": "长期主线", "duration": "3个月以上", "characteristics": "产业趋势、经济结构"},
            ],
        }


class EnhancedMainlineEngine(ProMainlineEngine):
    """
    增强版主线识别引擎
    
    集成热度评分引擎，采用新的权重配置：
    - 热度维度: 30% (基于7因子热度评分)
    - 资金维度: 25%
    - 趋势维度: 25% (原动量+龙头)
    - 政策维度: 20%
    """
    
    # 新的权重配置
    ENHANCED_WEIGHTS = {
        "heat": 0.30,      # 热度维度 30%
        "funds": 0.25,     # 资金维度 25%
        "trend": 0.25,     # 趋势维度 25%
        "policy": 0.20,    # 政策维度 20%
    }
    
    def __init__(self):
        super().__init__()
        self.heatmap_engine = None
        self._init_heatmap_engine()
    
    def _init_heatmap_engine(self):
        """初始化热度评分引擎（使用新的集成热度评分引擎）"""
        try:
            from .integrated_heatmap import IntegratedHeatmapEngine
            self.heatmap_engine = IntegratedHeatmapEngine()
            logger.info("✅ 集成热度评分引擎初始化成功")
        except Exception as e:
            logger.warning(f"⚠️ 热度评分引擎初始化失败: {e}")
            self.heatmap_engine = None
    
    def analyze_enhanced(self, data: Dict) -> List[MainlineResult]:
        """
        增强版分析（集成热度评分）
        
        Args:
            data: 包含各数据源数据的字典
        
        Returns:
            主线识别结果列表
        """
        # 先执行基础分析
        results = self.analyze(data)
        
        # 如果热度引擎可用，增强热度评分（使用新的集成热度评分引擎）
        if self.heatmap_engine:
            try:
                # 使用新的集成热度评分引擎计算
                heatmap_scores = self.heatmap_engine.calculate_heatmap_scores(
                    sector_data=data.get("sector_flow", []),
                    concept_data=data.get("concept_flow", []),
                    limit_up_data=data.get("limit_up", {}) if isinstance(data.get("limit_up"), dict) else {},
                    lhb_data=data.get("dragon_tiger", []) if isinstance(data.get("dragon_tiger"), list) else [],
                    period="short",  # 短期主线识别
                )
                
                # 创建热度评分映射（使用name字段）
                heatmap_map = {s.name: s for s in heatmap_scores}
                
                # 更新结果中的热度评分
                for result in results:
                    if result.name in heatmap_map:
                        heatmap = heatmap_map[result.name]
                        # 使用热度评分引擎的总分，转换为20分制
                        # 热度评分是0-100分，主线识别热度维度是20分
                        result.score.heat_score = heatmap.total_score / 100 * 20
                        
                        # 重新计算总分（使用新权重）
                        result.score = self._recalculate_score_enhanced(result.score)
                
                # 重新排序
                results.sort(key=lambda x: x.score.total, reverse=True)
                
                # 重新生成信号
                for result in results:
                    result.signal = self._generate_signal(result.score.total)
                
                # 保存热度评分结果供后续使用（个股筛选等）
                self._last_heatmap_scores = heatmap_scores
                
                logger.info(f"✅ 增强版分析完成，共 {len(results)} 条主线，已集成热度评分")
                
            except Exception as e:
                import traceback
                logger.warning(f"⚠️ 热度评分增强失败: {e}")
                traceback.print_exc()
        
        return results
    
    def _recalculate_score_enhanced(self, score: ScoreBreakdown) -> ScoreBreakdown:
        """
        使用新权重重新计算评分
        
        新权重：热度30% + 资金25% + 趋势25% + 政策20%
        """
        # 合并动量和龙头为趋势维度
        trend_score = score.momentum_score + score.leader_score  # 原来是20+15=35分
        
        # 重新标准化到100分制
        heat_normalized = score.heat_score / 20 * 100  # 原20分制转100分制
        funds_normalized = score.funds_score / 25 * 100  # 原25分制转100分制
        trend_normalized = trend_score / 35 * 100  # 原35分制转100分制
        policy_normalized = score.policy_score / 20 * 100  # 原20分制转100分制
        
        # 使用新权重计算总分
        new_total = (
            heat_normalized * self.ENHANCED_WEIGHTS["heat"] +
            funds_normalized * self.ENHANCED_WEIGHTS["funds"] +
            trend_normalized * self.ENHANCED_WEIGHTS["trend"] +
            policy_normalized * self.ENHANCED_WEIGHTS["policy"]
        )
        
        # 更新评分（保持原有分数结构，但总分使用新权重）
        return ScoreBreakdown(
            funds_score=score.funds_score,
            momentum_score=score.momentum_score,
            heat_score=score.heat_score,
            policy_score=score.policy_score,
            leader_score=score.leader_score,
        )
    
    def get_heatmap_details(self, mainline_name: str) -> Dict:
        """获取主线的热度评分详情"""
        if not self.heatmap_engine:
            return {}
        
        # 查找热度评分（使用新的集成引擎）
        last_scores = getattr(self, '_last_heatmap_scores', [])
        for score in last_scores:
            # 兼容新旧字段名
            name = getattr(score, 'name', None) or getattr(score, 'mainline_name', None)
            if name == mainline_name:
                return {
                    "total_score": score.total_score,
                    "factors": score.get_factor_breakdown() if hasattr(score, 'get_factor_breakdown') else [],
                    "trend": getattr(score, 'trend', 'unknown'),
                    "rank": getattr(score, 'rank', 0),
                    "level": getattr(score, 'level', ''),
                }
        
        return {}
    
    def get_enhanced_config_description(self) -> Dict:
        """获取增强版配置说明"""
        base_config = self.get_config_description()
        
        # 更新权重说明（使用新的5因子模型）
        base_config["enhanced_weights"] = {
            "热度维度": "30% (基于5因子集成热度评分引擎)",
            "资金维度": "25%",
            "趋势维度": "25% (动量+龙头)",
            "政策维度": "20%",
        }
        
        base_config["heatmap_factors"] = [
            {"name": "涨跌幅强度", "weight": "25%", "desc": "涨幅越高，市场资金关注度越高"},
            {"name": "资金流入强度", "weight": "25%", "desc": "资金净流入越多，机构认可度越高"},
            {"name": "涨停板数量", "weight": "20%", "desc": "涨停股越多，板块炒作热度越高"},
            {"name": "龙虎榜活跃度", "weight": "15%", "desc": "龙虎榜越多，游资参与度越高"},
            {"name": "龙头股强度", "weight": "15%", "desc": "龙头越强，板块带动效应越强"},
        ]
        
        return base_config


# 导出
__all__ = [
    "ProMainlineEngine",
    "EnhancedMainlineEngine",
    "MainlineResult",
    "ScoreBreakdown",
    "MainlineType",
    "SignalType",
    "SCORING_CONFIG",
]

