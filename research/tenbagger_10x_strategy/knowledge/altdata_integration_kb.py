#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AltData Integration Knowledge Base - 另类数据整合知识库
=======================================================

将另类数据信号与十倍股识别系统整合：

1. AltData信号类型定义
2. 信号与阶段转换映射
3. 十倍股证据链构建
4. 多源数据融合评分
5. 早期预警信号组合

参考资料:
- docs/altdata数据源.txt
- mcp_servers/utils/altdata_tier2.py
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import numpy as np


# ============== AltData信号类型 ==============

class AltDataSource(Enum):
    """另类数据源类型"""
    ANNOUNCEMENT = "公告年报"           # 交易所公告
    INTERACTIVE = "互动易"              # 互动易问答
    BIDDING = "招投标"                  # 招投标数据
    RECRUITMENT = "招聘数据"            # 招聘趋势
    ENVIRONMENTAL = "环评项目"          # 环评公示
    NEWS = "新闻舆情"                   # 财经新闻
    RESEARCH = "研报数量"               # 券商研报


class AltDataSignalType(Enum):
    """另类数据信号类型"""
    # 送样验证信号
    SAMPLE_DELIVERY = "送样信号"
    VALIDATION_PASS = "验证通过"
    CERTIFICATION = "认证获取"
    
    # 客户进入信号
    CUSTOMER_ENTRY = "客户导入"
    SUPPLIER_QUALIFY = "供应商认证"
    FRAMEWORK_SIGN = "框架协议"
    
    # 量产扩产信号
    SMALL_BATCH = "小批量订单"
    MASS_PRODUCTION = "量产启动"
    CAPACITY_EXPANSION = "产能扩张"
    
    # 组织变化信号
    HIRING_SURGE = "招聘激增"
    TECH_TO_PROD = "研发转产"
    SALES_EXPANSION = "销售扩张"
    
    # 项目进展信号
    ENV_APPROVAL = "环评批复"
    PROJECT_START = "项目开工"
    PROJECT_COMPLETE = "项目完工"
    
    # 财务拐点信号
    REVENUE_INFLECTION = "营收拐点"
    MARGIN_IMPROVEMENT = "毛利提升"
    CASH_TURNAROUND = "现金流转正"


# ============== 信号与阶段映射 ==============

@dataclass
class SignalStageMapping:
    """信号到阶段的映射"""
    signal_type: AltDataSignalType
    from_stage: str
    to_stage: str
    confidence_boost: float  # 置信度提升
    evidence_weight: float   # 证据权重


SIGNAL_STAGE_MAPPINGS = {
    # S0 → S1: 送样验证阶段
    AltDataSignalType.SAMPLE_DELIVERY: SignalStageMapping(
        signal_type=AltDataSignalType.SAMPLE_DELIVERY,
        from_stage="S0", to_stage="S1",
        confidence_boost=0.30, evidence_weight=0.20
    ),
    AltDataSignalType.CERTIFICATION: SignalStageMapping(
        signal_type=AltDataSignalType.CERTIFICATION,
        from_stage="S0", to_stage="S1",
        confidence_boost=0.25, evidence_weight=0.15
    ),
    
    # S1 → S2: 客户导入阶段
    AltDataSignalType.VALIDATION_PASS: SignalStageMapping(
        signal_type=AltDataSignalType.VALIDATION_PASS,
        from_stage="S1", to_stage="S2",
        confidence_boost=0.40, evidence_weight=0.25
    ),
    AltDataSignalType.CUSTOMER_ENTRY: SignalStageMapping(
        signal_type=AltDataSignalType.CUSTOMER_ENTRY,
        from_stage="S1", to_stage="S2",
        confidence_boost=0.45, evidence_weight=0.30
    ),
    AltDataSignalType.SUPPLIER_QUALIFY: SignalStageMapping(
        signal_type=AltDataSignalType.SUPPLIER_QUALIFY,
        from_stage="S1", to_stage="S2",
        confidence_boost=0.35, evidence_weight=0.25
    ),
    
    # S2 → S3: 量产扩张阶段
    AltDataSignalType.SMALL_BATCH: SignalStageMapping(
        signal_type=AltDataSignalType.SMALL_BATCH,
        from_stage="S2", to_stage="S3",
        confidence_boost=0.35, evidence_weight=0.20
    ),
    AltDataSignalType.MASS_PRODUCTION: SignalStageMapping(
        signal_type=AltDataSignalType.MASS_PRODUCTION,
        from_stage="S2", to_stage="S3",
        confidence_boost=0.50, evidence_weight=0.35
    ),
    AltDataSignalType.CAPACITY_EXPANSION: SignalStageMapping(
        signal_type=AltDataSignalType.CAPACITY_EXPANSION,
        from_stage="S2", to_stage="S3",
        confidence_boost=0.40, evidence_weight=0.30
    ),
    
    # S3 → S4: 业绩兑现阶段
    AltDataSignalType.REVENUE_INFLECTION: SignalStageMapping(
        signal_type=AltDataSignalType.REVENUE_INFLECTION,
        from_stage="S3", to_stage="S4",
        confidence_boost=0.45, evidence_weight=0.35
    ),
    AltDataSignalType.MARGIN_IMPROVEMENT: SignalStageMapping(
        signal_type=AltDataSignalType.MARGIN_IMPROVEMENT,
        from_stage="S3", to_stage="S4",
        confidence_boost=0.40, evidence_weight=0.30
    ),
}


# ============== 数据源可信度 ==============

DATA_SOURCE_RELIABILITY = {
    AltDataSource.ANNOUNCEMENT: {
        "reliability": 1.0,       # 最高可信度
        "timeliness": 0.7,        # 时效性中等（滞后）
        "cost": 0,                # 免费
        "coverage": 1.0           # 全覆盖
    },
    AltDataSource.INTERACTIVE: {
        "reliability": 0.85,      # 高可信度
        "timeliness": 0.9,        # 高时效性（实时）
        "cost": 0,                # 免费
        "coverage": 0.8           # 主要公司
    },
    AltDataSource.BIDDING: {
        "reliability": 0.9,       # 高可信度（官方数据）
        "timeliness": 0.85,       # 较高时效性
        "cost": 0,                # 免费（官方网站）
        "coverage": 0.6           # 部分行业
    },
    AltDataSource.RECRUITMENT: {
        "reliability": 0.7,       # 中等可信度
        "timeliness": 0.95,       # 极高时效性
        "cost": 0,                # 免费（公开网站）
        "coverage": 0.7           # 大部分公司
    },
    AltDataSource.ENVIRONMENTAL: {
        "reliability": 0.95,      # 极高可信度
        "timeliness": 0.6,        # 中等时效性
        "cost": 0,                # 免费
        "coverage": 0.4           # 制造业为主
    },
    AltDataSource.NEWS: {
        "reliability": 0.5,       # 中低可信度
        "timeliness": 1.0,        # 极高时效性
        "cost": 0,                # 免费
        "coverage": 0.9           # 高覆盖
    },
    AltDataSource.RESEARCH: {
        "reliability": 0.75,      # 中高可信度
        "timeliness": 0.7,        # 中等时效性
        "cost": 0.5,              # 中等成本
        "coverage": 0.5           # 覆盖头部公司
    },
}


# ============== 十倍股事件关键词 ==============

TENBAGGER_EVENT_KEYWORDS = {
    # 送样验证相关
    "sample_validation": [
        "送样", "样品", "验证", "认证", "测试通过",
        "导入测试", "小批量验证", "客户测试"
    ],
    
    # 客户进入相关
    "customer_entry": [
        "进入", "导入", "认证通过", "供应商资格",
        "框架协议", "战略合作", "批量供货"
    ],
    
    # 产能扩张相关
    "capacity_expansion": [
        "扩产", "新产线", "新厂房", "产能", "技改",
        "募投项目", "环评", "开工", "投产"
    ],
    
    # 业绩拐点相关
    "performance_inflection": [
        "业绩预增", "净利润增长", "营收增长", "毛利率提升",
        "扭亏", "大幅增长", "同比增长"
    ],
    
    # 组织扩张相关
    "organization_expansion": [
        "招聘", "扩招", "研发团队", "销售团队",
        "新增岗位", "人才引进", "高管任命"
    ],
}


# ============== 证据链评估器 ==============

@dataclass
class EvidenceItem:
    """证据项"""
    source: AltDataSource
    signal_type: AltDataSignalType
    content: str
    date: str
    reliability: float  # 可信度
    weight: float       # 权重


class EvidenceChainEvaluator:
    """证据链评估器
    
    功能：
    1. 收集多源证据
    2. 评估证据可信度
    3. 交叉验证
    4. 计算综合置信度
    """
    
    def __init__(self):
        self.evidence_chain: List[EvidenceItem] = []
        
    def add_evidence(self, evidence: EvidenceItem):
        """添加证据"""
        self.evidence_chain.append(evidence)
        
    def cross_validate(self) -> Tuple[float, List[str]]:
        """交叉验证证据链
        
        Returns:
            (综合置信度, 验证说明列表)
        """
        if not self.evidence_chain:
            return 0.0, ["无证据"]
            
        validations = []
        confidence = 0.0
        
        # 按信号类型分组
        signal_groups = {}
        for e in self.evidence_chain:
            if e.signal_type not in signal_groups:
                signal_groups[e.signal_type] = []
            signal_groups[e.signal_type].append(e)
            
        # 单一来源置信度
        for signal_type, evidences in signal_groups.items():
            weight_sum = sum(e.weight * e.reliability for e in evidences)
            confidence += weight_sum * 0.3  # 单一来源权重30%
            validations.append(f"{signal_type.value}: {len(evidences)}条证据")
            
        # 多源交叉验证加成
        unique_sources = set(e.source for e in self.evidence_chain)
        if len(unique_sources) >= 2:
            cross_bonus = 0.2 * min(len(unique_sources) - 1, 3)
            confidence += cross_bonus
            validations.append(f"多源验证加成: +{cross_bonus*100:.0f}%")
            
        # 证据链连续性加成
        sorted_evidences = sorted(self.evidence_chain, key=lambda x: x.date)
        if len(sorted_evidences) >= 3:
            # 检查是否形成连续的证据链
            chain_count = 0
            for i in range(len(sorted_evidences) - 1):
                mapping = SIGNAL_STAGE_MAPPINGS.get(sorted_evidences[i].signal_type)
                next_mapping = SIGNAL_STAGE_MAPPINGS.get(sorted_evidences[i+1].signal_type)
                if mapping and next_mapping:
                    if mapping.to_stage == next_mapping.from_stage:
                        chain_count += 1
            
            if chain_count > 0:
                chain_bonus = 0.1 * min(chain_count, 3)
                confidence += chain_bonus
                validations.append(f"证据链连续性: +{chain_bonus*100:.0f}%")
                
        return min(confidence, 1.0), validations
    
    def get_stage_recommendation(self) -> Tuple[str, float]:
        """根据证据链推荐阶段
        
        Returns:
            (推荐阶段, 置信度)
        """
        if not self.evidence_chain:
            return "S0", 0.0
            
        # 统计各阶段的证据权重
        stage_scores = {"S0": 0, "S1": 0, "S2": 0, "S3": 0, "S4": 0}
        
        for evidence in self.evidence_chain:
            mapping = SIGNAL_STAGE_MAPPINGS.get(evidence.signal_type)
            if mapping:
                stage_scores[mapping.to_stage] += (
                    evidence.weight * evidence.reliability * mapping.confidence_boost
                )
                
        # 找出最高分阶段
        best_stage = max(stage_scores, key=stage_scores.get)
        confidence, _ = self.cross_validate()
        
        return best_stage, confidence


# ============== AltData信号生成器 ==============

class AltDataSignalGenerator:
    """AltData信号生成器
    
    功能：
    1. 从原始数据提取信号
    2. 关键词匹配
    3. 信号强度评估
    4. 与StageMachine集成
    """
    
    def __init__(self):
        self.signal_cache = {}
        
    def extract_signals_from_text(self, text: str, source: AltDataSource) -> List[Tuple[AltDataSignalType, float]]:
        """从文本提取信号
        
        Args:
            text: 原始文本（公告、问答等）
            source: 数据源
            
        Returns:
            [(信号类型, 信号强度), ...]
        """
        signals = []
        text_lower = text.lower()
        
        # 遍历关键词组
        for category, keywords in TENBAGGER_EVENT_KEYWORDS.items():
            matched_count = 0
            for kw in keywords:
                if kw in text:
                    matched_count += 1
                    
            if matched_count > 0:
                # 根据类别确定信号类型
                signal_type = self._category_to_signal_type(category)
                if signal_type:
                    # 信号强度 = 匹配关键词数 / 总关键词数 * 数据源可信度
                    strength = (matched_count / len(keywords)) * DATA_SOURCE_RELIABILITY[source]["reliability"]
                    signals.append((signal_type, min(strength, 1.0)))
                    
        return signals
    
    def _category_to_signal_type(self, category: str) -> Optional[AltDataSignalType]:
        """类别转信号类型"""
        mapping = {
            "sample_validation": AltDataSignalType.VALIDATION_PASS,
            "customer_entry": AltDataSignalType.CUSTOMER_ENTRY,
            "capacity_expansion": AltDataSignalType.CAPACITY_EXPANSION,
            "performance_inflection": AltDataSignalType.REVENUE_INFLECTION,
            "organization_expansion": AltDataSignalType.HIRING_SURGE,
        }
        return mapping.get(category)
    
    def analyze_recruitment_trend(self, job_records: List[Dict]) -> List[Tuple[AltDataSignalType, float]]:
        """分析招聘趋势信号
        
        Args:
            job_records: [{job_type, count, date}, ...]
        """
        signals = []
        
        if len(job_records) < 5:
            return signals
            
        # 统计各类型招聘变化
        tech_jobs = [r for r in job_records if r.get('job_type') == 'tech']
        prod_jobs = [r for r in job_records if r.get('job_type') == 'production']
        sales_jobs = [r for r in job_records if r.get('job_type') == 'sales']
        
        # 研发转产信号：生产岗位增加，研发岗位稳定
        if len(prod_jobs) >= 3:
            recent_prod = sum(r.get('count', 0) for r in prod_jobs[-3:])
            older_prod = sum(r.get('count', 0) for r in prod_jobs[-6:-3]) if len(prod_jobs) >= 6 else 0
            if recent_prod > older_prod * 1.5:
                signals.append((AltDataSignalType.TECH_TO_PROD, 0.7))
                
        # 销售扩张信号
        if len(sales_jobs) >= 3:
            recent_sales = sum(r.get('count', 0) for r in sales_jobs[-3:])
            older_sales = sum(r.get('count', 0) for r in sales_jobs[-6:-3]) if len(sales_jobs) >= 6 else 0
            if recent_sales > older_sales * 2:
                signals.append((AltDataSignalType.SALES_EXPANSION, 0.6))
                
        # 整体招聘激增信号
        total_recent = sum(r.get('count', 0) for r in job_records[-5:])
        total_older = sum(r.get('count', 0) for r in job_records[-10:-5]) if len(job_records) >= 10 else 0
        if total_recent > total_older * 1.8:
            signals.append((AltDataSignalType.HIRING_SURGE, 0.65))
            
        return signals
    
    def analyze_bidding_trend(self, bid_records: List[Dict]) -> List[Tuple[AltDataSignalType, float]]:
        """分析招投标趋势信号
        
        Args:
            bid_records: [{bid_type, amount, date, title}, ...]
        """
        signals = []
        
        if len(bid_records) < 3:
            return signals
            
        # 检查扩产相关招标
        expansion_keywords = ["产能", "扩产", "新建", "技改", "设备"]
        expansion_count = 0
        total_amount = 0
        
        for bid in bid_records:
            title = bid.get('title', '')
            if any(kw in title for kw in expansion_keywords):
                expansion_count += 1
                total_amount += bid.get('amount', 0)
                
        if expansion_count >= 2:
            signals.append((AltDataSignalType.CAPACITY_EXPANSION, 0.75))
            
        # 项目类招标
        project_keywords = ["项目", "工程", "建设"]
        project_count = sum(1 for bid in bid_records if any(kw in bid.get('title', '') for kw in project_keywords))
        
        if project_count >= 2:
            signals.append((AltDataSignalType.PROJECT_START, 0.6))
            
        return signals


# ============== 十倍股AltData评分器 ==============

class TenbaggerAltDataScorer:
    """十倍股AltData评分器
    
    将AltData信号整合到十倍股评分系统
    """
    
    def __init__(self):
        self.signal_generator = AltDataSignalGenerator()
        self.evidence_evaluator = EvidenceChainEvaluator()
        
    def calculate_altdata_score(self, stock_symbol: str, 
                                 altdata_records: Dict[str, List[Dict]]) -> Tuple[float, Dict]:
        """计算AltData评分
        
        Args:
            stock_symbol: 股票代码
            altdata_records: {
                'announcements': [...],
                'interactive': [...],
                'bidding': [...],
                'recruitment': [...],
                ...
            }
            
        Returns:
            (AltData评分0-100, 详细信息)
        """
        all_signals = []
        details = {}
        
        # 1. 分析公告信号
        announcements = altdata_records.get('announcements', [])
        for ann in announcements:
            signals = self.signal_generator.extract_signals_from_text(
                ann.get('content', ''), 
                AltDataSource.ANNOUNCEMENT
            )
            all_signals.extend(signals)
            
            # 添加证据
            for signal_type, strength in signals:
                self.evidence_evaluator.add_evidence(EvidenceItem(
                    source=AltDataSource.ANNOUNCEMENT,
                    signal_type=signal_type,
                    content=ann.get('title', ''),
                    date=ann.get('date', ''),
                    reliability=DATA_SOURCE_RELIABILITY[AltDataSource.ANNOUNCEMENT]["reliability"],
                    weight=strength
                ))
        details['announcement_signals'] = len([s for s in all_signals if s[0]])
        
        # 2. 分析互动易信号
        interactive = altdata_records.get('interactive', [])
        for qa in interactive:
            signals = self.signal_generator.extract_signals_from_text(
                qa.get('answer', ''),
                AltDataSource.INTERACTIVE
            )
            all_signals.extend(signals)
            
            for signal_type, strength in signals:
                self.evidence_evaluator.add_evidence(EvidenceItem(
                    source=AltDataSource.INTERACTIVE,
                    signal_type=signal_type,
                    content=qa.get('question', ''),
                    date=qa.get('date', ''),
                    reliability=DATA_SOURCE_RELIABILITY[AltDataSource.INTERACTIVE]["reliability"],
                    weight=strength
                ))
        details['interactive_signals'] = len(interactive)
        
        # 3. 分析招聘趋势
        recruitment = altdata_records.get('recruitment', [])
        job_signals = self.signal_generator.analyze_recruitment_trend(recruitment)
        all_signals.extend(job_signals)
        details['recruitment_signals'] = len(job_signals)
        
        # 4. 分析招投标趋势
        bidding = altdata_records.get('bidding', [])
        bid_signals = self.signal_generator.analyze_bidding_trend(bidding)
        all_signals.extend(bid_signals)
        details['bidding_signals'] = len(bid_signals)
        
        # 5. 计算综合评分
        if not all_signals:
            return 0, details
            
        # 信号强度加权平均
        total_strength = sum(s[1] for s in all_signals)
        avg_strength = total_strength / len(all_signals) if all_signals else 0
        
        # 证据链验证
        confidence, validations = self.evidence_evaluator.cross_validate()
        details['cross_validations'] = validations
        
        # 最终评分
        altdata_score = (avg_strength * 50 + confidence * 50)
        
        # 阶段推荐
        stage, stage_confidence = self.evidence_evaluator.get_stage_recommendation()
        details['recommended_stage'] = stage
        details['stage_confidence'] = stage_confidence
        
        return min(altdata_score, 100), details


# ============== 导出 ==============

__all__ = [
    'AltDataSource',
    'AltDataSignalType',
    'SignalStageMapping',
    'SIGNAL_STAGE_MAPPINGS',
    'DATA_SOURCE_RELIABILITY',
    'TENBAGGER_EVENT_KEYWORDS',
    'EvidenceItem',
    'EvidenceChainEvaluator',
    'AltDataSignalGenerator',
    'TenbaggerAltDataScorer'
]







































