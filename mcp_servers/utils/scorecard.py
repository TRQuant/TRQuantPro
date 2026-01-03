#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ScoreCard - 十倍股7维评分卡
==========================

M3.2核心组件：多维度评分，支持可解释性输出

7维评分：
1. 产业位置 (20%) - 产业链关键节点
2. 兑现路径 (20%) - 送样→量产进度
3. 财务拐点 (15%) - 毛利/营收/现金流
4. 组织信号 (10%) - 招聘/高管变化
5. 估值错配 (15%) - PE/PB vs 增速
6. 研究关注 (10%) - 研报数量（越少越好）
7. 证据密度 (10%) - 多证据交叉
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class DimensionScore:
    """维度评分"""
    dimension: str          # 维度名称
    score: float           # 得分 (0-100)
    weight: float          # 权重 (0-1)
    weighted_score: float  # 加权得分
    
    # 可解释性
    factors: List[Dict] = field(default_factory=list)  # 影响因子
    explanation: str = ""   # 解释文本
    data_source: str = ""   # 数据来源


@dataclass
class ScoreCard:
    """
    十倍股评分卡
    
    综合7维度评分
    """
    card_id: str
    security_id: str
    
    # 总分
    total_score: float = 0.0
    grade: str = ""  # A/B/C/D/F
    
    # 维度得分
    dimensions: List[DimensionScore] = field(default_factory=list)
    
    # 阶段关联
    current_stage: str = ""
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "v1"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "security_id": self.security_id,
            "total_score": self.total_score,
            "grade": self.grade,
            "dimensions": [asdict(d) for d in self.dimensions],
            "current_stage": self.current_stage,
            "created_at": self.created_at,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScoreCard":
        dims = [DimensionScore(**d) for d in data.get("dimensions", [])]
        return cls(
            card_id=data["card_id"],
            security_id=data["security_id"],
            total_score=data.get("total_score", 0),
            grade=data.get("grade", ""),
            dimensions=dims,
            current_stage=data.get("current_stage", ""),
            created_at=data.get("created_at", ""),
            version=data.get("version", "v1")
        )


class ScoreCardEngine:
    """
    评分卡引擎
    
    计算7维评分
    """
    
    # 维度配置
    DIMENSIONS = {
        "industry_position": {
            "name": "产业位置",
            "weight": 0.20,
            "description": "产业链关键节点评估"
        },
        "fulfillment_path": {
            "name": "兑现路径",
            "weight": 0.20,
            "description": "送样→量产进度评估"
        },
        "financial_inflection": {
            "name": "财务拐点",
            "weight": 0.15,
            "description": "毛利/营收/现金流评估"
        },
        "organization_signal": {
            "name": "组织信号",
            "weight": 0.10,
            "description": "招聘/高管变化评估"
        },
        "valuation_mismatch": {
            "name": "估值错配",
            "weight": 0.15,
            "description": "PE/PB vs 增速评估"
        },
        "research_attention": {
            "name": "研究关注",
            "weight": 0.10,
            "description": "研报数量评估（越少越好）"
        },
        "evidence_density": {
            "name": "证据密度",
            "weight": 0.10,
            "description": "多证据交叉评估"
        }
    }
    
    # 等级划分
    GRADE_THRESHOLDS = [
        (80, "A"),   # >= 80: A
        (65, "B"),   # >= 65: B
        (50, "C"),   # >= 50: C
        (35, "D"),   # >= 35: D
        (0, "F")     # < 35: F
    ]
    
    def __init__(self):
        self._mongo_db = None
        self._collection = None
        self._init_mongo()
    
    def _init_mongo(self):
        """初始化MongoDB连接"""
        try:
            from pymongo import MongoClient, DESCENDING
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            self._mongo_db = client.get_database("trquant")
            self._collection = self._mongo_db.scorecards
            
            self._collection.create_index([("security_id", 1), ("created_at", DESCENDING)])
            self._collection.create_index([("total_score", DESCENDING)])
            self._collection.create_index([("grade", 1)])
            
            logger.info("ScoreCardEngine: MongoDB连接成功")
        except Exception as e:
            logger.warning(f"ScoreCardEngine: MongoDB连接失败: {e}")
    
    def compute(
        self,
        security_id: str,
        stage_record: Dict = None,
        events: List[Dict] = None,
        financial_data: Dict = None
    ) -> ScoreCard:
        """
        计算评分卡
        
        Args:
            security_id: 股票代码
            stage_record: 阶段记录（可选）
            events: 事件列表（可选）
            financial_data: 财务数据（可选）
        
        Returns:
            ScoreCard对象
        """
        import uuid
        
        dimensions = []
        
        # 1. 产业位置评分
        dim1 = self._score_industry_position(security_id)
        dimensions.append(dim1)
        
        # 2. 兑现路径评分（基于Stage）
        dim2 = self._score_fulfillment_path(security_id, stage_record)
        dimensions.append(dim2)
        
        # 3. 财务拐点评分
        dim3 = self._score_financial_inflection(security_id, financial_data)
        dimensions.append(dim3)
        
        # 4. 组织信号评分
        dim4 = self._score_organization_signal(security_id, events)
        dimensions.append(dim4)
        
        # 5. 估值错配评分
        dim5 = self._score_valuation_mismatch(security_id, financial_data)
        dimensions.append(dim5)
        
        # 6. 研究关注评分
        dim6 = self._score_research_attention(security_id)
        dimensions.append(dim6)
        
        # 7. 证据密度评分
        dim7 = self._score_evidence_density(security_id, events)
        dimensions.append(dim7)
        
        # 计算总分
        total_score = sum(d.weighted_score for d in dimensions)
        grade = self._compute_grade(total_score)
        
        card = ScoreCard(
            card_id=f"sc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
            security_id=security_id,
            total_score=round(total_score, 2),
            grade=grade,
            dimensions=dimensions,
            current_stage=stage_record.get("current_stage", "") if stage_record else ""
        )
        
        self._save(card)
        return card
    
    def _score_industry_position(self, security_id: str) -> DimensionScore:
        """评估产业位置"""
        config = self.DIMENSIONS["industry_position"]
        
        # TODO: 实际实现需要产业链图谱数据
        # 这里使用默认值
        score = 60.0
        factors = [{"factor": "产业链位置", "value": "待评估"}]
        explanation = "产业位置评估需要产业链图谱数据支持"
        
        return DimensionScore(
            dimension=config["name"],
            score=score,
            weight=config["weight"],
            weighted_score=round(score * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="industry_graph"
        )
    
    def _score_fulfillment_path(self, security_id: str, stage_record: Dict = None) -> DimensionScore:
        """评估兑现路径"""
        config = self.DIMENSIONS["fulfillment_path"]
        
        # 根据Stage计算得分
        stage_scores = {
            "S0": 20, "S1": 40, "S2": 60, "S3": 80, "S4": 90, "S5": 50
        }
        
        if stage_record:
            stage = stage_record.get("current_stage", "S0")
            confidence = stage_record.get("confidence", 0)
            base_score = stage_scores.get(stage, 20)
            score = base_score + (confidence * 10)  # 置信度加成
            factors = [
                {"factor": "当前阶段", "value": stage},
                {"factor": "置信度", "value": f"{confidence:.2f}"}
            ]
            explanation = f"当前处于{stage}阶段，置信度{confidence:.2f}"
        else:
            score = 30.0
            factors = [{"factor": "阶段数据", "value": "缺失"}]
            explanation = "缺少阶段数据"
        
        return DimensionScore(
            dimension=config["name"],
            score=min(score, 100),
            weight=config["weight"],
            weighted_score=round(min(score, 100) * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="stage_machine"
        )
    
    def _score_financial_inflection(self, security_id: str, financial_data: Dict = None) -> DimensionScore:
        """评估财务拐点"""
        config = self.DIMENSIONS["financial_inflection"]
        
        if financial_data:
            # 评估关键财务指标
            factors = []
            score = 50.0
            
            # 毛利率变化
            gross_margin_change = financial_data.get("gross_margin_change", 0)
            if gross_margin_change > 5:
                score += 20
                factors.append({"factor": "毛利率提升", "value": f"+{gross_margin_change}%"})
            
            # 营收增速
            revenue_growth = financial_data.get("revenue_growth", 0)
            if revenue_growth > 30:
                score += 15
                factors.append({"factor": "营收增速", "value": f"+{revenue_growth}%"})
            
            # 现金流
            if financial_data.get("positive_cash_flow", False):
                score += 15
                factors.append({"factor": "经营现金流", "value": "正向"})
            
            explanation = "基于毛利率、营收增速、现金流综合评估"
        else:
            score = 50.0
            factors = [{"factor": "财务数据", "value": "待获取"}]
            explanation = "需要JQData财务数据"
        
        return DimensionScore(
            dimension=config["name"],
            score=min(score, 100),
            weight=config["weight"],
            weighted_score=round(min(score, 100) * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="jqdata"
        )
    
    def _score_organization_signal(self, security_id: str, events: List[Dict] = None) -> DimensionScore:
        """评估组织信号"""
        config = self.DIMENSIONS["organization_signal"]
        
        score = 50.0
        factors = []
        
        if events:
            # 统计组织相关事件
            org_events = [e for e in events if e.get("event_type") in 
                         ["executive_change", "equity_incentive", "hiring_surge"]]
            
            if org_events:
                score += len(org_events) * 10
                factors.append({"factor": "组织事件数", "value": len(org_events)})
                
                # 股权激励加分
                if any(e.get("event_type") == "equity_incentive" for e in org_events):
                    score += 15
                    factors.append({"factor": "股权激励", "value": "有"})
        
        if not factors:
            factors = [{"factor": "组织事件", "value": "无"}]
        
        explanation = f"发现{len(factors)}个组织信号"
        
        return DimensionScore(
            dimension=config["name"],
            score=min(score, 100),
            weight=config["weight"],
            weighted_score=round(min(score, 100) * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="events"
        )
    
    def _score_valuation_mismatch(self, security_id: str, financial_data: Dict = None) -> DimensionScore:
        """评估估值错配"""
        config = self.DIMENSIONS["valuation_mismatch"]
        
        score = 50.0
        factors = []
        
        if financial_data:
            pe = financial_data.get("pe_ratio", 0)
            growth = financial_data.get("revenue_growth", 0)
            
            if pe > 0 and growth > 0:
                peg = pe / growth
                if peg < 1:
                    score = 80 + (1 - peg) * 20
                    factors.append({"factor": "PEG", "value": f"{peg:.2f} (低估)"})
                elif peg < 2:
                    score = 60
                    factors.append({"factor": "PEG", "value": f"{peg:.2f} (合理)"})
                else:
                    score = 40
                    factors.append({"factor": "PEG", "value": f"{peg:.2f} (偏高)"})
        else:
            factors = [{"factor": "估值数据", "value": "待获取"}]
        
        explanation = "基于PEG估值模型评估"
        
        return DimensionScore(
            dimension=config["name"],
            score=min(score, 100),
            weight=config["weight"],
            weighted_score=round(min(score, 100) * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="jqdata"
        )
    
    def _score_research_attention(self, security_id: str) -> DimensionScore:
        """评估研究关注度（越少越好，十倍股早期特征）"""
        config = self.DIMENSIONS["research_attention"]
        
        # TODO: 实际需要研报数据
        # 模拟：假设研报少
        report_count = 5  # 假设值
        
        if report_count <= 3:
            score = 90
            explanation = "研报极少，早期信号明显"
        elif report_count <= 10:
            score = 70
            explanation = "研报较少，关注度适中"
        elif report_count <= 30:
            score = 50
            explanation = "研报较多，已有一定关注"
        else:
            score = 30
            explanation = "研报众多，共识度高"
        
        factors = [{"factor": "研报数量", "value": report_count}]
        
        return DimensionScore(
            dimension=config["name"],
            score=score,
            weight=config["weight"],
            weighted_score=round(score * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="research_reports"
        )
    
    def _score_evidence_density(self, security_id: str, events: List[Dict] = None) -> DimensionScore:
        """评估证据密度"""
        config = self.DIMENSIONS["evidence_density"]
        
        event_count = len(events) if events else 0
        
        # 事件越多，证据越充分
        if event_count >= 10:
            score = 90
        elif event_count >= 5:
            score = 70
        elif event_count >= 2:
            score = 50
        else:
            score = 30
        
        factors = [{"factor": "证据事件数", "value": event_count}]
        explanation = f"发现{event_count}个支撑事件"
        
        return DimensionScore(
            dimension=config["name"],
            score=score,
            weight=config["weight"],
            weighted_score=round(score * config["weight"], 2),
            factors=factors,
            explanation=explanation,
            data_source="events"
        )
    
    def _compute_grade(self, score: float) -> str:
        """计算等级"""
        for threshold, grade in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "F"
    
    def get_latest(self, security_id: str) -> Optional[ScoreCard]:
        """获取最新评分卡"""
        if self._collection is None:
            return None
        
        data = self._collection.find_one(
            {"security_id": security_id},
            sort=[("created_at", -1)]
        )
        if data:
            data.pop("_id", None)
            return ScoreCard.from_dict(data)
        return None
    
    def get_history(self, security_id: str, limit: int = 10) -> List[ScoreCard]:
        """获取评分历史"""
        if self._collection is None:
            return []
        
        results = []
        for data in self._collection.find({"security_id": security_id}).sort("created_at", -1).limit(limit):
            data.pop("_id", None)
            results.append(ScoreCard.from_dict(data))
        return results
    
    def list_by_grade(self, grade: str, limit: int = 100) -> List[ScoreCard]:
        """按等级列出"""
        if self._collection is None:
            return []
        
        results = []
        for data in self._collection.find({"grade": grade}).sort("total_score", -1).limit(limit):
            data.pop("_id", None)
            results.append(ScoreCard.from_dict(data))
        return results
    
    def explain(self, card: ScoreCard) -> str:
        """生成评分解释"""
        lines = [
            f"📊 {card.security_id} 评分卡 (v{card.version})",
            f"总分: {card.total_score} / 等级: {card.grade}",
            f"阶段: {card.current_stage or '未知'}",
            "",
            "维度评分:"
        ]
        
        for dim in card.dimensions:
            lines.append(f"  [{dim.dimension}] {dim.score:.0f}分 × {dim.weight:.0%} = {dim.weighted_score:.1f}")
            lines.append(f"    └ {dim.explanation}")
        
        return "\n".join(lines)
    
    def _save(self, card: ScoreCard):
        """保存评分卡"""
        if self._collection is not None:
            self._collection.insert_one(card.to_dict())


# 全局实例
_engine: Optional[ScoreCardEngine] = None

def get_scorecard_engine() -> ScoreCardEngine:
    """获取评分卡引擎"""
    global _engine
    if _engine is None:
        _engine = ScoreCardEngine()
    return _engine
