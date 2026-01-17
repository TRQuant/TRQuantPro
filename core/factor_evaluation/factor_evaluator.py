#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因子评估引擎
============

自动化IC/IR/衰减分析，结果写回知识库
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


class FactorEvaluator:
    """因子评估引擎"""
    
    def __init__(self):
        self.kb_type = "factor_behavior"
    
    def calculate_ic(self, factor_values: pd.Series, returns: pd.Series) -> Dict[str, float]:
        """
        计算IC（信息系数）
        
        Args:
            factor_values: 因子值序列
            returns: 收益率序列
            
        Returns:
            IC统计信息
        """
        # 对齐数据
        aligned = pd.DataFrame({
            'factor': factor_values,
            'return': returns
        }).dropna()
        
        if len(aligned) < 10:
            return {"ic_mean": 0.0, "ic_std": 0.0, "ir": 0.0}
        
        # 计算IC（相关系数）
        ic = aligned['factor'].corr(aligned['return'])
        
        # 计算IC序列（滚动窗口）
        ic_series = aligned['factor'].rolling(20).corr(aligned['return'])
        ic_mean = ic_series.mean()
        ic_std = ic_series.std()
        
        # 计算IR（信息比率）
        ir = ic_mean / ic_std if ic_std > 0 else 0.0
        
        return {
            "ic": float(ic),
            "ic_mean": float(ic_mean),
            "ic_std": float(ic_std),
            "ir": float(ir)
        }
    
    def calculate_ic_by_regime(
        self,
        factor_values: pd.Series,
        returns: pd.Series,
        regime_labels: pd.Series
    ) -> Dict[str, Dict[str, float]]:
        """
        按市场状态计算IC
        
        Args:
            factor_values: 因子值序列
            returns: 收益率序列
            regime_labels: 市场状态标签序列
            
        Returns:
            各状态下的IC统计
        """
        aligned = pd.DataFrame({
            'factor': factor_values,
            'return': returns,
            'regime': regime_labels
        }).dropna()
        
        ic_by_regime = {}
        
        for regime in aligned['regime'].unique():
            regime_data = aligned[aligned['regime'] == regime]
            if len(regime_data) >= 10:
                ic = regime_data['factor'].corr(regime_data['return'])
                ic_by_regime[regime] = {
                    "ic": float(ic),
                    "sample_count": len(regime_data)
                }
        
        return ic_by_regime
    
    def evaluate_factor(
        self,
        factor_name: str,
        factor_values: pd.Series,
        returns: pd.Series,
        regime_labels: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        评估因子并写回知识库
        
        Args:
            factor_name: 因子名称
            factor_values: 因子值序列
            returns: 收益率序列
            regime_labels: 市场状态标签（可选）
            
        Returns:
            评估结果
        """
        # 计算IC
        ic_stats = self.calculate_ic(factor_values, returns)
        
        # 按状态计算IC（如果有状态标签）
        ic_by_regime = {}
        if regime_labels is not None:
            ic_by_regime = self.calculate_ic_by_regime(
                factor_values, returns, regime_labels
            )
        
        # 生成有效性建议
        recommendation = self._generate_recommendation(ic_stats, ic_by_regime)
        
        # 构建知识库条目
        content = f"""## {factor_name} 因子评估结果

### IC统计
- **IC均值**: {ic_stats['ic_mean']:.4f}
- **IC标准差**: {ic_stats['ic_std']:.4f}
- **IR（信息比率）**: {ic_stats['ir']:.4f}

### 按市场状态IC分析
"""
        
        if ic_by_regime:
            for regime, stats in ic_by_regime.items():
                content += f"- **{regime}**: IC = {stats['ic']:.4f} (样本数: {stats['sample_count']})\n"
        else:
            content += "- 暂无分状态数据\n"
        
        content += f"""
### 有效性建议
{recommendation}

### 使用建议
- IC > 0.05: 因子有效，可用于策略
- IC 0.02-0.05: 因子弱有效，需配合其他因子
- IC < 0.02: 因子无效，不建议使用
- IR > 1.0: 因子稳定性好
- IR < 0.5: 因子稳定性差

### 更新时间
{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 写回知识库
        try:
            result = knowledge_add(
                title=f"{factor_name} 因子评估结果",
                content=content,
                type=self.kb_type,
                tags=["因子评估", factor_name, "IC分析", "回测验证"],
                source="因子评估引擎自动生成"
            )
            
            if result.get('success') or result.get('knowledge_id'):
                return {
                    "success": True,
                    "knowledge_id": result.get('knowledge_id'),
                    "ic_stats": ic_stats,
                    "ic_by_regime": ic_by_regime,
                    "recommendation": recommendation
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "ic_stats": ic_stats,
                "ic_by_regime": ic_by_regime
            }
        
        return {
            "success": False,
            "error": "写入知识库失败",
            "ic_stats": ic_stats,
            "ic_by_regime": ic_by_regime
        }
    
    def _generate_recommendation(
        self,
        ic_stats: Dict[str, float],
        ic_by_regime: Dict[str, Dict[str, float]]
    ) -> str:
        """生成有效性建议"""
        ic_mean = ic_stats['ic_mean']
        ir = ic_stats['ir']
        
        recommendations = []
        
        # 整体有效性
        if ic_mean > 0.05:
            recommendations.append("因子整体有效，可用于策略")
        elif ic_mean > 0.02:
            recommendations.append("因子弱有效，需配合其他因子使用")
        else:
            recommendations.append("因子整体无效，不建议单独使用")
        
        # 稳定性
        if ir > 1.0:
            recommendations.append("因子稳定性好，可长期使用")
        elif ir > 0.5:
            recommendations.append("因子稳定性一般，需谨慎使用")
        else:
            recommendations.append("因子稳定性差，不建议使用")
        
        # 分状态有效性
        if ic_by_regime:
            valid_regimes = [
                regime for regime, stats in ic_by_regime.items()
                if stats['ic'] > 0.05
            ]
            invalid_regimes = [
                regime for regime, stats in ic_by_regime.items()
                if stats['ic'] < 0.02
            ]
            
            if valid_regimes:
                recommendations.append(f"在{', '.join(valid_regimes)}状态下有效")
            if invalid_regimes:
                recommendations.append(f"在{', '.join(invalid_regimes)}状态下失效")
        
        return "\n".join(f"- {r}" for r in recommendations)


def get_factor_evaluator() -> FactorEvaluator:
    """获取因子评估引擎实例"""
    return FactorEvaluator()
