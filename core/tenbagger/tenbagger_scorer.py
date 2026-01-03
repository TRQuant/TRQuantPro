#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股评分与阶段识别模块

阶段定义：
- S0: 潜伏期 - 业绩开始改善，尚未被市场发现
- S1: 启动期 - 业绩确认，股价开始上涨
- S2: 加速期 - 业绩高增长，股价快速上涨
- S3: 成熟期 - 业绩增速放缓，股价高位震荡
- S4: 衰退期 - 业绩下滑，股价回落
- S5: 尾声期 - 业绩恶化，需要规避
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
import logging

logger = logging.getLogger(__name__)


class TenbaggerStage(Enum):
    S0_LATENT = "S0_潜伏期"
    S1_LAUNCH = "S1_启动期"
    S2_ACCELERATE = "S2_加速期"
    S3_MATURE = "S3_成熟期"
    S4_DECLINE = "S4_衰退期"
    S5_END = "S5_尾声期"


@dataclass
class StageScore:
    stage: TenbaggerStage
    score: float
    confidence: float
    factors: Dict[str, float]
    recommendation: str


class TenbaggerScorer:
    """十倍股评分器"""
    
    def __init__(self):
        self.jq = None
        self._ensure_jqdata()
        
        # 阶段权重
        self.stage_weights = {
            TenbaggerStage.S0_LATENT: 1.2,
            TenbaggerStage.S1_LAUNCH: 1.5,
            TenbaggerStage.S2_ACCELERATE: 1.3,
            TenbaggerStage.S3_MATURE: 0.8,
            TenbaggerStage.S4_DECLINE: 0.4,
            TenbaggerStage.S5_END: 0.1
        }
    
    def _ensure_jqdata(self):
        if self.jq is None:
            try:
                import jqdatasdk as jq
                with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self.jq = jq
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def score_stock(self, stock: str, date: str = None) -> StageScore:
        factors = self._calc_factors(stock, date)
        stage, score, confidence = self._determine_stage(factors)
        recommendation = self._get_recommendation(stage)
        return StageScore(stage=stage, score=score, confidence=confidence, 
                         factors=factors, recommendation=recommendation)
    
    def _calc_factors(self, stock: str, date: str = None) -> Dict[str, float]:
        factors = {'profit_growth': 0.0, 'revenue_growth': 0.0, 
                  'price_momentum': 0.0, 'roe': 0.0}
        if self.jq is None:
            return factors
        try:
            df = self.jq.get_price(stock, end_date=date, count=60, fields=['close'])
            if df is not None and len(df) >= 60:
                factors['price_momentum'] = df['close'].iloc[-1] / df['close'].iloc[0] - 1
        except:
            pass
        return factors
    
    def _determine_stage(self, factors: Dict[str, float]) -> Tuple[TenbaggerStage, float, float]:
        momentum = factors.get('price_momentum', 0)
        if momentum < -0.20:
            return TenbaggerStage.S4_DECLINE, 30, 0.7
        elif momentum < 0:
            return TenbaggerStage.S0_LATENT, 60, 0.7
        elif momentum < 0.30:
            return TenbaggerStage.S1_LAUNCH, 80, 0.8
        elif momentum < 0.80:
            return TenbaggerStage.S2_ACCELERATE, 70, 0.75
        else:
            return TenbaggerStage.S3_MATURE, 50, 0.6
    
    def _get_recommendation(self, stage: TenbaggerStage) -> str:
        recs = {
            TenbaggerStage.S0_LATENT: "关注观察",
            TenbaggerStage.S1_LAUNCH: "⭐ 最佳买点",
            TenbaggerStage.S2_ACCELERATE: "持有加仓",
            TenbaggerStage.S3_MATURE: "分批减仓",
            TenbaggerStage.S4_DECLINE: "清仓离场",
            TenbaggerStage.S5_END: "严格回避"
        }
        return recs.get(stage, "")
    
    def get_stage_weight(self, stage: TenbaggerStage) -> float:
        return self.stage_weights.get(stage, 1.0)
    
    def batch_score(self, stocks: List[str], date: str = None) -> List[Tuple[str, StageScore]]:
        results = []
        for stock in stocks:
            try:
                results.append((stock, self.score_stock(stock, date)))
            except:
                pass
        results.sort(key=lambda x: x[1].score, reverse=True)
        return results


def test_scorer():
    print("="*60)
    print("🎯 十倍股评分器测试")
    print("="*60)
    scorer = TenbaggerScorer()
    for stock in ['000001.XSHE', '600519.XSHG', '300750.XSHE']:
        r = scorer.score_stock(stock)
        print(f"\n{stock}: {r.stage.value} 得分:{r.score:.0f} {r.recommendation}")


if __name__ == "__main__":
    test_scorer()
