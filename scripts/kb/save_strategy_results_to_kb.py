#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
策略结果归档到RAG知识库

每次回测后自动归档：策略参数、回测结果、优化建议
成功案例归档：达到月回报率30%的策略详细记录
失败案例归档：失败原因分析、改进方向
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入知识库工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    print("⚠️ MCP工具不可用，将使用直接文件操作")


def save_backtest_result_to_kb(
    backtest_result: Dict[str, Any],
    strategy_params: Dict[str, Any],
    backtest_id: str,
    success: bool = False,
    failure_reasons: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    保存回测结果到知识库
    
    Args:
        backtest_result: 回测结果字典
        strategy_params: 策略参数字典
        backtest_id: 回测ID
        success: 是否成功（达到目标）
        failure_reasons: 失败原因列表
    
    Returns:
        保存结果
    """
    if not KB_AVAILABLE:
        return {'success': False, 'error': 'MCP工具不可用'}
    
    # 生成标题
    monthly_return = backtest_result.get('monthly_return', 0.0) * 100
    title = f"{'✅ 成功' if success else '❌ 失败'} - 回测结果 {backtest_id} (月收益率: {monthly_return:.2f}%)"
    
    # 生成内容
    content = f"""# 回测结果归档 - {backtest_id}

## 基本信息
- 回测ID: {backtest_id}
- 归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 是否达到目标: {'✅ 是' if success else '❌ 否'}

## 绩效指标
- 月收益率: {backtest_result.get('monthly_return', 0.0)*100:.2f}%
- 年化收益率: {backtest_result.get('annual_return', 0.0)*100:.2f}%
- 总收益率: {backtest_result.get('total_return', 0.0)*100:.2f}%
- 最大回撤: {backtest_result.get('max_drawdown', 0.0)*100:.2f}%
- 夏普比率: {backtest_result.get('sharpe_ratio', 0.0):.2f}
- 胜率: {backtest_result.get('win_rate', 0.0)*100:.2f}%
- 总交易次数: {backtest_result.get('total_trades', 0)}
- 平均持仓周期: {backtest_result.get('avg_holding_period', 0.0):.1f}天

## 策略参数
```json
{json.dumps(strategy_params, indent=2, ensure_ascii=False)}
```

## 回测配置
- 开始日期: {backtest_result.get('start_date', 'N/A')}
- 结束日期: {backtest_result.get('end_date', 'N/A')}
- 初始资金: {backtest_result.get('initial_capital', 0):,.0f}
"""
    
    if success:
        content += f"""
## 成功经验

### 关键成功因素
1. **策略参数优化**: 当前参数组合在牛市环境下表现优秀
2. **选股质量**: 因子筛选和评分体系有效
3. **风险管理**: 止损止盈机制发挥作用
4. **调仓频率**: 调仓周期设置合理

### 可复用经验
- 参数组合: 可在类似市场环境下直接使用
- 因子权重: 牛市环境下动量因子权重应提高
- 仓位管理: 当前仓位分配方式有效
"""
    else:
        content += f"""
## 失败分析

### 失败原因
{f'<br>'.join(f'- {reason}' for reason in (failure_reasons or ['未知原因']))}

### 改进方向
"""
        
        # 基于失败原因生成改进建议
        if backtest_result.get('monthly_return', 0.0) < 0.15:
            content += "- **月收益率过低**: 需要提高选股标准或调整因子权重\n"
        if backtest_result.get('max_drawdown', 0.0) < -0.20:
            content += "- **最大回撤过大**: 需要收紧止损或降低仓位\n"
        if backtest_result.get('sharpe_ratio', 0.0) < 2.0:
            content += "- **夏普比率过低**: 需要优化调仓频率或平衡收益风险\n"
        if backtest_result.get('total_trades', 0) < 10:
            content += "- **交易次数过少**: 可能选股标准过严，需要放宽筛选条件\n"
    
    # 存入知识库
    try:
        result = knowledge_add(
            title=title,
            content=content,
            type='backtest_result' if success else 'backtest_failure',
            tags=['backtest', 'strategy_result', 'bull_market' if success else 'failure_analysis'],
            source=f"backtest/{backtest_id}"
        )
        
        kb_id = result.get('knowledge_id') if isinstance(result, dict) else None
        return {'success': True, 'knowledge_id': kb_id}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def save_evolution_result_to_kb(
    evolution_result: Dict[str, Any],
    evolution_run_id: str,
    reached_target: bool = False
) -> Dict[str, Any]:
    """
    保存进化结果到知识库
    
    Args:
        evolution_result: 进化结果字典
        evolution_run_id: 进化运行ID
        reached_target: 是否达到目标
    
    Returns:
        保存结果
    """
    if not KB_AVAILABLE:
        return {'success': False, 'error': 'MCP工具不可用'}
    
    best_result = evolution_result.get('best_result', {})
    monthly_return = best_result.get('monthly_return', 0.0) * 100
    
    title = f"{'✅ 成功' if reached_target else '⚠️ 未达标'} - 进化优化结果 {evolution_run_id} (最佳月收益率: {monthly_return:.2f}%)"
    
    content = f"""# 进化优化结果归档 - {evolution_run_id}

## 基本信息
- 运行ID: {evolution_run_id}
- 归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 是否达到目标: {'✅ 是' if reached_target else '❌ 否'}

## 进化配置
- 种群大小: {evolution_result.get('evolution_config', {}).get('population_size', 0)}
- 进化代数: {evolution_result.get('total_generations', 0)}
- 目标月收益率: {evolution_result.get('evolution_config', {}).get('target_monthly_return', 0.0)*100:.0f}%
- 最大回撤限制: {evolution_result.get('evolution_config', {}).get('max_drawdown_limit', 0.0)*100:.0f}%
- 最小夏普比率: {evolution_result.get('evolution_config', {}).get('min_sharpe_ratio', 0.0):.1f}

## 最佳结果
- 月收益率: {monthly_return:.2f}%
- 最大回撤: {best_result.get('max_drawdown', 0.0)*100:.2f}%
- 夏普比率: {best_result.get('sharpe_ratio', 0.0):.2f}
- 总交易次数: {best_result.get('total_trades', 0)}

## 最佳策略参数
```json
{json.dumps(evolution_result.get('best_params', {}), indent=2, ensure_ascii=False)}
```

## 进化过程
- 总代数: {evolution_result.get('total_generations', 0)}
- 是否早停: {evolution_result.get('early_stopped', False)}
- 早停原因: {evolution_result.get('stop_reason', 'N/A')}

## 经验总结
"""
    
    if reached_target:
        content += f"""
### 成功经验
1. **参数优化有效**: 进化算法成功找到达到目标的参数组合
2. **参数范围合理**: 参数空间定义准确，搜索方向正确
3. **适应度函数设计**: 适应度函数能有效引导进化方向

### 最佳参数特征
- 这些参数在牛市环境下最有效
- 可在类似市场环境下直接使用
- 因子权重配置合理
"""
    else:
        content += f"""
### 未达标分析
- 最佳月收益率: {monthly_return:.2f}% < 目标30%
- 可能原因:
  1. 参数空间定义过窄，未包含最优解
  2. 适应度函数设计不合理
  3. 回测期间市场环境不利
  4. 策略逻辑本身存在缺陷

### 改进方向
1. 扩大参数搜索空间
2. 调整适应度函数（增加奖励项）
3. 增加进化代数
4. 优化初始种群（使用更好的初始化策略）
"""
    
    try:
        result = knowledge_add(
            title=title,
            content=content,
            type='evolution_result',
            tags=['evolution', 'genetic_algorithm', 'optimization', 'bull_market'],
            source=f"evolution/{evolution_run_id}"
        )
        
        kb_id = result.get('knowledge_id') if isinstance(result, dict) else None
        return {'success': True, 'knowledge_id': kb_id}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def save_workflow_result_to_kb(workflow_result: Dict[str, Any]) -> Dict[str, Any]:
    """保存工作流结果到知识库"""
    if not KB_AVAILABLE:
        return {'success': False, 'error': 'MCP工具不可用'}
    
    workflow_id = workflow_result.get('workflow_id', 'unknown')
    reached_target = workflow_result.get('reached_target', False)
    
    title = f"{'✅ 成功' if reached_target else '⚠️ 未完成'} - 完整工作流结果 {workflow_id}"
    
    content = f"""# 完整工作流执行结果 - {workflow_id}

## 执行信息
- 工作流ID: {workflow_id}
- 开始时间: {workflow_result.get('start_time', 'N/A')}
- 结束时间: {workflow_result.get('end_time', 'N/A')}
- 是否达到目标: {'✅ 是' if reached_target else '❌ 否'}

## 各阶段结果

### 阶段1: 市场状态检测
- 牛市概率: {workflow_result.get('market_detection', {}).get('bull_probability', 0):.1f}%
- 强度等级: {workflow_result.get('market_detection', {}).get('strength_level', 'UNKNOWN')}
- 强度得分: {workflow_result.get('market_detection', {}).get('strength_score', 0):.1f}/100

### 阶段2: 数据挖掘
- 高回报案例数: {workflow_result.get('data_mining', {}).get('case_count', 0) if workflow_result.get('data_mining') else 0}

### 阶段3: 模式提取
- 提取模式数: {workflow_result.get('pattern_extraction', {}).get('pattern_count', 0) if workflow_result.get('pattern_extraction') else 0}

### 阶段4: 策略生成
- 策略模式: {workflow_result.get('strategy_generation', {}).get('strategy_mode', 'UNKNOWN')}

### 阶段5: 回测
- 回测次数: {workflow_result.get('backtest_results_count', 0)}

### 阶段6: 进化优化
- 是否执行: {workflow_result.get('evolution_results') is not None}
- 是否达到目标: {workflow_result.get('evolution_results', {}).get('reached_target', False) if workflow_result.get('evolution_results') else False}

## 最终结果
- 最佳策略参数:
```json
{json.dumps(workflow_result.get('best_strategy_params', {}), indent=2, ensure_ascii=False)}
```

- 最佳回测结果:
  - 月收益率: {workflow_result.get('best_backtest_result', {}).get('monthly_return', 0.0)*100:.2f}% if workflow_result.get('best_backtest_result') else 'N/A'
  - 最大回撤: {workflow_result.get('best_backtest_result', {}).get('max_drawdown', 0.0)*100:.2f}% if workflow_result.get('best_backtest_result') else 'N/A'
  - 夏普比率: {workflow_result.get('best_backtest_result', {}).get('sharpe_ratio', 0.0):.2f} if workflow_result.get('best_backtest_result') else 'N/A'

## 错误信息
{chr(10).join(f'- {e}' for e in workflow_result.get('errors', [])) if workflow_result.get('errors') else '无错误'}

## 经验总结
"""
    
    if reached_target:
        content += """
### 成功经验
1. **工作流完整执行**: 所有阶段成功完成
2. **市场状态判断准确**: 牛市检测有效
3. **策略生成合理**: 混合策略模式有效
4. **进化优化成功**: 找到达到目标的参数组合

### 可复用模式
- 完整工作流可以作为标准流程
- 各阶段的衔接逻辑正确
- 知识库归档机制有效
"""
    else:
        content += """
### 未达标原因
- 分析各阶段结果，找出瓶颈
- 检查策略逻辑和参数空间
- 考虑市场环境因素

### 改进方向
- 优化数据挖掘阶段（增加案例数量）
- 改进模式提取算法
- 调整进化参数（种群大小、代数等）
- 扩大参数搜索空间
"""
    
    try:
        result = knowledge_add(
            title=title,
            content=content,
            type='workflow_result',
            tags=['workflow', 'complete_pipeline', 'bull_market', 'strategy_development'],
            source=f"workflow/{workflow_id}"
        )
        
        kb_id = result.get('knowledge_id') if isinstance(result, dict) else None
        return {'success': True, 'knowledge_id': kb_id}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    """主函数：示例用法"""
    print("策略结果归档工具")
    print("="*70)
    
    # 示例：保存回测结果
    backtest_result = {
        'monthly_return': 0.32,
        'max_drawdown': -0.15,
        'sharpe_ratio': 2.5,
        'total_trades': 50,
        'win_rate': 0.6,
    }
    
    strategy_params = {
        'max_stocks': 12,
        'min_total_score': 32.0,
        'rebalance_days': 5,
    }
    
    result = save_backtest_result_to_kb(
        backtest_result=backtest_result,
        strategy_params=strategy_params,
        backtest_id='test_backtest_001',
        success=True
    )
    
    print(f"保存结果: {result}")


if __name__ == '__main__':
    main()
