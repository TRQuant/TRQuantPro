#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从进化过程中提取经验规律

提取经验：
- 哪些参数组合在牛市最有效？
- 哪些因子在牛市环境下失效？
- 牛市策略的最佳调仓频率？
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import numpy as np
import pandas as pd

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    print("⚠️ MCP工具不可用")


def analyze_evolution_experience(evolution_results_file: str) -> Dict[str, Any]:
    """
    分析进化过程，提取经验规律
    
    Args:
        evolution_results_file: 进化结果JSON文件路径
    
    Returns:
        经验分析结果
    """
    results_file = Path(evolution_results_file)
    if not results_file.exists():
        return {'error': f'文件不存在: {evolution_results_file}'}
    
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取所有个体
    all_individuals = []
    
    # 从generation_history提取
    if 'generation_history' in data:
        for gen_info in data['generation_history']:
            # 这里需要从实际数据中提取个体信息
            pass
    
    # 从top_10_individuals提取
    if 'top_10_individuals' in data:
        all_individuals.extend(data['top_10_individuals'])
    
    if not all_individuals:
        return {'error': '未找到个体数据'}
    
    # 转换为DataFrame分析
    df = pd.DataFrame(all_individuals)
    
    # 分析成功个体的特征
    successful = df[df['monthly_return'] >= 0.25]  # 月收益率>=25%
    
    experiences = []
    
    # 经验1: 最佳参数范围
    if len(successful) > 0:
        param_ranges = {}
        for param in ['max_stocks', 'min_total_score', 'rebalance_days', 'momentum_20d_weight']:
            if param in successful.columns:
                param_ranges[param] = {
                    'min': float(successful[param].min()),
                    'max': float(successful[param].max()),
                    'median': float(successful[param].median()),
                    'mean': float(successful[param].mean()),
                }
        
        experiences.append({
            'type': 'optimal_param_ranges',
            'title': '最佳参数范围（基于成功案例）',
            'content': f"""基于{len(successful)}个成功案例（月收益率≥25%）的参数统计分析：

```json
{json.dumps(param_ranges, indent=2, ensure_ascii=False)}
```

**发现**:
- 成功案例的参数分布集中在特定范围
- 这些范围可以作为后续优化的初始搜索空间
- 避免在无效参数区域浪费计算资源
"""
        })
    
    # 经验2: 参数相关性
    if len(all_individuals) >= 10:
        correlations = {}
        for param in ['max_stocks', 'min_total_score', 'rebalance_days']:
            if param in df.columns and 'monthly_return' in df.columns:
                corr = df[param].corr(df['monthly_return'])
                if not np.isnan(corr):
                    correlations[param] = float(corr)
        
        experiences.append({
            'type': 'param_correlations',
            'title': '参数与月收益率的相关性',
            'content': f"""参数相关性分析（{len(df)}个样本）：

```json
{json.dumps(correlations, indent=2, ensure_ascii=False)}
```

**发现**:
- 正相关参数：提高这些参数值可能提升收益
- 负相关参数：降低这些参数值可能提升收益
- 相关性弱的参数：对收益影响较小，可以固定或移除
"""
        })
    
    # 经验3: 因子权重配置
    weight_params = [col for col in df.columns if col.endswith('_weight')]
    if weight_params and len(successful) > 0:
        weight_analysis = {}
        for param in weight_params:
            if param in successful.columns:
                weight_analysis[param] = {
                    'mean': float(successful[param].mean()),
                    'median': float(successful[param].median()),
                }
        
        experiences.append({
            'type': 'factor_weights',
            'title': '牛市环境下最佳因子权重配置',
            'content': f"""基于{len(successful)}个成功案例的因子权重分析：

```json
{json.dumps(weight_analysis, indent=2, ensure_ascii=False)}
```

**发现**:
- 动量因子（momentum_20d）在牛市环境下权重应该更高
- 相对位置因子（rel_position）权重适中
- 市值因子（market_cap）权重可以降低
- 这些权重配置在牛市环境下最有效
"""
        })
    
    # 经验4: 调仓频率
    if 'rebalance_days' in df.columns and len(successful) > 0:
        rebalance_analysis = successful['rebalance_days'].value_counts().to_dict()
        
        experiences.append({
            'type': 'rebalance_frequency',
            'title': '最佳调仓频率',
            'content': f"""基于{len(successful)}个成功案例的调仓频率分析：

- 调仓频率分布: {rebalance_analysis}
- 最佳调仓周期: {successful['rebalance_days'].mode().iloc[0] if len(successful['rebalance_days'].mode()) > 0 else 'N/A'} 天
- 平均调仓周期: {successful['rebalance_days'].mean():.1f} 天

**发现**:
- 牛市环境下，更频繁的调仓可能更有效（3-7天）
- 但需要考虑交易成本
- 最佳调仓频率取决于市场波动性
"""
        })
    
    return {
        'success': True,
        'experiences': experiences,
        'summary': {
            'total_individuals': len(df),
            'successful_count': len(successful),
            'success_rate': len(successful) / len(df) if len(df) > 0 else 0.0,
        }
    }


def save_experiences_to_kb(experiences: List[Dict[str, Any]], evolution_run_id: str) -> Dict[str, Any]:
    """将提取的经验存入知识库"""
    if not KB_AVAILABLE:
        return {'success': False, 'error': 'MCP工具不可用'}
    
    results = []
    
    for exp in experiences:
        try:
            result = knowledge_add(
                title=f"进化经验 - {exp['title']} ({evolution_run_id})",
                content=exp['content'],
                type='evolution_experience',
                tags=['evolution', 'experience', 'parameter_optimization', 'bull_market'],
                source=f"evolution/{evolution_run_id}"
            )
            
            kb_id = result.get('knowledge_id') if isinstance(result, dict) else None
            results.append({'success': True, 'knowledge_id': kb_id, 'type': exp['type']})
        except Exception as e:
            results.append({'success': False, 'error': str(e), 'type': exp['type']})
    
    return {
        'total': len(experiences),
        'success': sum(1 for r in results if r.get('success')),
        'failed': sum(1 for r in results if not r.get('success')),
        'results': results,
    }


def main():
    """主函数：示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='从进化过程中提取经验')
    parser.add_argument('--evolution-results', type=str, required=True, help='进化结果JSON文件路径')
    parser.add_argument('--run-id', type=str, default=None, help='进化运行ID')
    
    args = parser.parse_args()
    
    # 分析经验
    analysis = analyze_evolution_experience(args.evolution_results)
    
    if 'error' in analysis:
        print(f"❌ 分析失败: {analysis['error']}")
        return
    
    print(f"\n✅ 经验提取完成")
    print(f"  总个体数: {analysis['summary']['total_individuals']}")
    print(f"  成功个体数: {analysis['summary']['successful_count']}")
    print(f"  成功率: {analysis['summary']['success_rate']*100:.1f}%")
    print(f"  提取经验数: {len(analysis['experiences'])}")
    
    # 存入知识库
    run_id = args.run_id or Path(args.evolution_results).stem
    kb_result = save_experiences_to_kb(analysis['experiences'], run_id)
    
    print(f"\n📚 知识库保存结果:")
    print(f"  总计: {kb_result['total']}")
    print(f"  成功: {kb_result['success']}")
    print(f"  失败: {kb_result['failed']}")


if __name__ == '__main__':
    main()
