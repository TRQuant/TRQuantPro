#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报策略 V6.0 - Phase 4: TenbaggerScorer评估AI智能体核心标的

使用十倍股早期识别系统评估AI智能体标的的成长阶段 (S0-S5)
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# 导入TenbaggerScorer
from core.tenbagger.tenbagger_scorer import TenbaggerScorer, TenbaggerStage, StageScore


# AI智能体核心标的清单 (从知识库提取)
AI_TARGETS_A_SHARE = {
    # Tier 1 核心标的
    "002230.XSHE": {"name": "科大讯飞", "tier": 1, "sector": "AI智能体", "note": "AI应用绝对龙头"},
    "688111.XSHG": {"name": "金山办公", "tier": 1, "sector": "AI办公", "note": "WPS AI助手"},
    "300058.XSHE": {"name": "蓝色光标", "tier": 1, "sector": "AI营销", "note": "All in AI战略"},
    "300418.XSHE": {"name": "昆仑万维", "tier": 1, "sector": "AI智能体", "note": "天工超级智能体"},
    
    # Tier 2 潜力标的
    "300071.XSHE": {"name": "福石控股", "tier": 2, "sector": "AI营销", "note": "迪思AI智链"},
    "603598.XSHG": {"name": "引力传媒", "tier": 2, "sector": "AI营销", "note": "AI赋能全链路"},
    "300253.XSHE": {"name": "卫宁健康", "tier": 2, "sector": "AI医疗", "note": "医院信息系统+AI"},
    "600570.XSHG": {"name": "恒生电子", "tier": 2, "sector": "AI金融", "note": "AI智能投研"},
    "300033.XSHE": {"name": "同花顺", "tier": 2, "sector": "AI金融", "note": "AI资讯投顾"},
    "600588.XSHG": {"name": "用友网络", "tier": 2, "sector": "AI办公", "note": "友间AI"},
    "300624.XSHE": {"name": "万兴科技", "tier": 2, "sector": "AI办公", "note": "AI视频剪辑"},
    "300229.XSHE": {"name": "拓尔思", "tier": 2, "sector": "AI智能体", "note": "大模型+知识管理"},
    "300496.XSHE": {"name": "中科创达", "tier": 2, "sector": "AI智能体", "note": "智能终端操作系统"},
    "688271.XSHG": {"name": "联影医疗", "tier": 2, "sector": "AI医疗", "note": "AI影像分析"},
    "300010.XSHE": {"name": "豆神教育", "tier": 2, "sector": "AI教育", "note": "AI虚拟教师"},
}


@dataclass
class EnhancedStageResult:
    """增强的阶段评估结果"""
    stock: str
    name: str
    tier: int
    sector: str
    stage: TenbaggerStage
    score: float
    confidence: float
    recommendation: str
    investment_weight: float  # 投资权重调整
    note: str


class TenbaggerIntegrator:
    """TenbaggerScorer与策略的集成器"""
    
    def __init__(self):
        self.scorer = TenbaggerScorer()
        
        # 根据阶段调整投资权重
        self.stage_weight_multiplier = {
            TenbaggerStage.S0_LATENT: 0.5,      # 潜伏期: 观察，轻仓
            TenbaggerStage.S1_LAUNCH: 1.5,      # 启动期: 最佳买点，重仓
            TenbaggerStage.S2_ACCELERATE: 1.2,  # 加速期: 持有，加仓
            TenbaggerStage.S3_MATURE: 0.7,      # 成熟期: 减仓
            TenbaggerStage.S4_DECLINE: 0.2,     # 衰退期: 清仓
            TenbaggerStage.S5_END: 0.0,         # 尾声期: 回避
        }
        
        logger.info("TenbaggerIntegrator 初始化完成")
    
    def evaluate_single_stock(
        self,
        stock: str,
        stock_info: Dict,
        date: str = None,
    ) -> EnhancedStageResult:
        """评估单只股票"""
        try:
            stage_score = self.scorer.score_stock(stock, date)
            
            # 计算投资权重调整
            base_weight = 1.0 if stock_info['tier'] == 1 else 0.7  # Tier1权重更高
            stage_multiplier = self.stage_weight_multiplier.get(stage_score.stage, 1.0)
            investment_weight = base_weight * stage_multiplier
            
            return EnhancedStageResult(
                stock=stock,
                name=stock_info['name'],
                tier=stock_info['tier'],
                sector=stock_info['sector'],
                stage=stage_score.stage,
                score=stage_score.score,
                confidence=stage_score.confidence,
                recommendation=stage_score.recommendation,
                investment_weight=investment_weight,
                note=stock_info.get('note', ''),
            )
        except Exception as e:
            logger.error(f"评估 {stock} 失败: {e}")
            return EnhancedStageResult(
                stock=stock,
                name=stock_info['name'],
                tier=stock_info['tier'],
                sector=stock_info['sector'],
                stage=TenbaggerStage.S0_LATENT,
                score=0,
                confidence=0,
                recommendation="数据不足",
                investment_weight=0,
                note=f"评估失败: {e}",
            )
    
    def evaluate_all_targets(
        self,
        targets: Dict[str, Dict],
        date: str = None,
    ) -> List[EnhancedStageResult]:
        """评估所有标的"""
        results = []
        
        for stock, info in targets.items():
            result = self.evaluate_single_stock(stock, info, date)
            results.append(result)
            logger.info(f"{result.name} ({stock}): {result.stage.value} 得分:{result.score:.0f} 权重:{result.investment_weight:.2f}")
        
        # 按投资权重排序
        results.sort(key=lambda x: x.investment_weight, reverse=True)
        return results
    
    def generate_investment_allocation(
        self,
        results: List[EnhancedStageResult],
        total_capital: float = 1000000,  # 总资金100万
        max_single_position: float = 0.15,  # 单只最大15%
    ) -> Dict[str, Dict]:
        """生成投资配置建议"""
        
        # 过滤掉衰退期和尾声期的股票
        investable = [r for r in results if r.stage not in [TenbaggerStage.S4_DECLINE, TenbaggerStage.S5_END]]
        
        if not investable:
            logger.warning("没有可投资的标的")
            return {}
        
        # 计算总权重
        total_weight = sum(r.investment_weight for r in investable)
        
        allocation = {}
        for result in investable:
            if total_weight > 0:
                raw_allocation = result.investment_weight / total_weight
                # 限制单只仓位
                final_allocation = min(raw_allocation, max_single_position)
                
                allocation[result.stock] = {
                    "name": result.name,
                    "stage": result.stage.value,
                    "score": result.score,
                    "recommendation": result.recommendation,
                    "allocation_pct": final_allocation * 100,
                    "allocation_amount": total_capital * final_allocation,
                    "tier": result.tier,
                    "sector": result.sector,
                }
        
        return allocation
    
    def generate_report(
        self,
        results: List[EnhancedStageResult],
        allocation: Dict[str, Dict],
        date: str = None,
    ) -> str:
        """生成评估报告"""
        
        report = []
        report.append("=" * 70)
        report.append("🎯 AI智能体核心标的 十倍股阶段评估报告")
        report.append("=" * 70)
        report.append(f"评估日期: {date or datetime.now().strftime('%Y-%m-%d')}")
        report.append(f"评估标的数: {len(results)}")
        report.append("")
        
        # 阶段分布统计
        stage_counts = {}
        for r in results:
            stage_counts[r.stage.value] = stage_counts.get(r.stage.value, 0) + 1
        
        report.append("【阶段分布】")
        for stage, count in sorted(stage_counts.items()):
            report.append(f"  {stage}: {count}只")
        report.append("")
        
        # 详细评估结果
        report.append("【详细评估】")
        report.append("-" * 70)
        report.append(f"{'股票代码':<15} {'名称':<10} {'Tier':<5} {'阶段':<15} {'得分':<6} {'建议':<12}")
        report.append("-" * 70)
        
        for r in results:
            report.append(f"{r.stock:<15} {r.name:<10} T{r.tier:<4} {r.stage.value:<15} {r.score:<6.0f} {r.recommendation:<12}")
        
        report.append("-" * 70)
        report.append("")
        
        # 投资配置建议
        report.append("【投资配置建议】 (假设总资金100万)")
        report.append("-" * 70)
        report.append(f"{'股票代码':<15} {'名称':<10} {'阶段':<15} {'配置比例':<10} {'配置金额':<12}")
        report.append("-" * 70)
        
        total_allocated = 0
        for stock, info in allocation.items():
            report.append(f"{stock:<15} {info['name']:<10} {info['stage']:<15} {info['allocation_pct']:.1f}%      ¥{info['allocation_amount']:,.0f}")
            total_allocated += info['allocation_pct']
        
        report.append("-" * 70)
        report.append(f"{'总计':<15} {'':<10} {'':<15} {total_allocated:.1f}%      ¥{total_allocated * 10000:,.0f}")
        report.append("")
        
        # 分板块统计
        report.append("【板块配置统计】")
        sector_allocation = {}
        for stock, info in allocation.items():
            sector = info['sector']
            sector_allocation[sector] = sector_allocation.get(sector, 0) + info['allocation_pct']
        
        for sector, pct in sorted(sector_allocation.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {sector}: {pct:.1f}%")
        
        report.append("")
        
        # 投资建议总结
        report.append("【投资建议总结】")
        
        # 找出最佳买点(S1)的股票
        s1_stocks = [r for r in results if r.stage == TenbaggerStage.S1_LAUNCH]
        if s1_stocks:
            report.append("⭐ 最佳买点 (S1启动期):")
            for r in s1_stocks:
                report.append(f"   - {r.name} ({r.stock}): 得分{r.score:.0f}")
        
        # 找出加速期(S2)的股票
        s2_stocks = [r for r in results if r.stage == TenbaggerStage.S2_ACCELERATE]
        if s2_stocks:
            report.append("📈 加速期 (S2持有加仓):")
            for r in s2_stocks:
                report.append(f"   - {r.name} ({r.stock}): 得分{r.score:.0f}")
        
        # 找出潜伏期(S0)的股票
        s0_stocks = [r for r in results if r.stage == TenbaggerStage.S0_LATENT]
        if s0_stocks:
            report.append("👀 潜伏期 (S0关注观察):")
            for r in s0_stocks:
                report.append(f"   - {r.name} ({r.stock}): 得分{r.score:.0f}")
        
        # 风险提示
        s3_s4_stocks = [r for r in results if r.stage in [TenbaggerStage.S3_MATURE, TenbaggerStage.S4_DECLINE]]
        if s3_s4_stocks:
            report.append("⚠️ 风险提示 (需减仓或清仓):")
            for r in s3_s4_stocks:
                report.append(f"   - {r.name} ({r.stock}): {r.stage.value}")
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)


def run_tenbagger_evaluation():
    """运行TenbaggerScorer评估"""
    
    logger.info("=" * 60)
    logger.info("牛市高回报策略 V6.0 - Phase 4: TenbaggerScorer评估")
    logger.info("=" * 60)
    
    # 初始化集成器
    integrator = TenbaggerIntegrator()
    
    # 评估所有AI智能体标的
    logger.info(f"开始评估 {len(AI_TARGETS_A_SHARE)} 只AI智能体标的...")
    
    results = integrator.evaluate_all_targets(
        targets=AI_TARGETS_A_SHARE,
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    
    # 生成投资配置
    allocation = integrator.generate_investment_allocation(
        results=results,
        total_capital=1000000,
        max_single_position=0.15,
    )
    
    # 生成报告
    report = integrator.generate_report(
        results=results,
        allocation=allocation,
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    
    # 打印报告
    print(report)
    
    # 保存报告
    output_path = f"/home/taotao/.cursor/worktrees/TRQuant/ope/output/tenbagger_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"报告已保存到: {output_path}")
    
    return results, allocation


if __name__ == "__main__":
    run_tenbagger_evaluation()
