#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Workflow Server - Strategy KB集成函数
=====================================

这个文件包含Strategy KB与Workflow集成的辅助函数
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger('WorkflowServer')

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent

# 导入Strategy KB Server的函数
try:
    from mcp_servers.strategy_kb_server import (
        _handle_rule_get,
        _handle_rule_validate,
        _handle_query as _handle_strategy_kb_query,
        _handle_version_get as _handle_strategy_kb_version_get
    )
    STRATEGY_KB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Strategy KB Server不可用: {e}")
    STRATEGY_KB_AVAILABLE = False


def _generate_python_strategy_code(strategy_draft: Dict[str, Any]) -> str:
    """生成Python策略代码"""
    strategy_id = strategy_draft.get("id", "unknown")
    strategy_name = strategy_draft.get("name", "未命名策略")
    mainline = strategy_draft.get("mainline", "")
    factors = strategy_draft.get("factors", [])
    candidate_pool = strategy_draft.get("candidate_pool", [])
    signals = strategy_draft.get("signals", {})
    constraints = strategy_draft.get("constraints", {})
    citations = strategy_draft.get("citations", [])
    
    # 构建因子列表
    factor_names = [f.get("name", "") for f in factors]
    factor_weights = {f.get("name", ""): f.get("weight", 0) for f in factors}
    
    # 构建入场条件
    entry_conditions = signals.get("entry", {}).get("conditions", [])
    # 构建出场条件
    exit_conditions = signals.get("exit", {}).get("conditions", [])
    
    # 生成Python代码
    code = f'''# -*- coding: utf-8 -*-
"""
策略代码: {strategy_name}
策略ID: {strategy_id}
投资主线: {mainline}
生成时间: {datetime.now().isoformat()}

研究卡引用:
'''
    
    for i, citation in enumerate(citations[:3], 1):
        code += f'''- {citation.get("title", "N/A")} (分数: {citation.get("score", 0):.3f})
'''
    
    code += f'''
约束条件:
- 单票最大仓位: {constraints.get("max_position_size", "N/A")}
- 最大回撤: {constraints.get("max_drawdown", "N/A")}
- 最小持仓数: {constraints.get("min_positions", "N/A")}
- 最大持仓数: {constraints.get("max_positions", "N/A")}
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any

# 策略参数
STRATEGY_ID = "{strategy_id}"
STRATEGY_NAME = "{strategy_name}"
MAINLINE = "{mainline}"

# 因子配置
FACTORS = {json.dumps(factor_names, ensure_ascii=False, indent=2)}
FACTOR_WEIGHTS = {json.dumps(factor_weights, ensure_ascii=False, indent=2)}

# 候选股票池
CANDIDATE_POOL = {json.dumps(candidate_pool, ensure_ascii=False, indent=2)}

# 约束条件
MAX_POSITION_SIZE = {constraints.get("max_position_size", 0.10)}
MAX_DRAWDOWN = {constraints.get("max_drawdown", 0.15)}
MIN_POSITIONS = {constraints.get("min_positions", 10)}
MAX_POSITIONS = {constraints.get("max_positions", 50)}

# 入场条件
ENTRY_CONDITIONS = {json.dumps(entry_conditions, ensure_ascii=False, indent=2)}

# 出场条件
EXIT_CONDITIONS = {json.dumps(exit_conditions, ensure_ascii=False, indent=2)}


def calculate_factor_scores(data: pd.DataFrame) -> pd.DataFrame:
    """
    计算因子得分
    
    Args:
        data: 股票数据DataFrame
    
    Returns:
        包含因子得分的DataFrame
    """
    scores = pd.DataFrame(index=data.index)
    
    for factor_name in FACTORS:
        # 这里需要根据实际因子计算逻辑实现
        # 示例：假设因子值在data中
        if factor_name in data.columns:
            scores[f"{{factor_name}}_score"] = data[factor_name]
        else:
            # 默认得分
            scores[f"{{factor_name}}_score"] = 0.5
    
    return scores


def check_entry_conditions(data: pd.DataFrame, scores: pd.DataFrame) -> pd.Series:
    """
    检查入场条件
    
    Args:
        data: 股票数据
        scores: 因子得分
    
    Returns:
        布尔Series，True表示满足入场条件
    """
    result = pd.Series(True, index=data.index)
    
    # 简化实现：检查因子得分
    for factor_name in FACTORS:
        score_col = f"{{factor_name}}_score"
        if score_col in scores.columns:
            result = result & (scores[score_col] > 0.6)
    
    return result


def check_exit_conditions(positions: Dict[str, Any], current_data: pd.DataFrame) -> List[str]:
    """
    检查出场条件
    
    Args:
        positions: 当前持仓
        current_data: 当前数据
    
    Returns:
        需要平仓的股票列表
    """
    exit_stocks = []
    
    for stock_code, position in positions.items():
        # 检查回撤
        if "drawdown" in position and position["drawdown"] > MAX_DRAWDOWN:
            exit_stocks.append(stock_code)
            continue
        
        # 检查持仓天数
        if "holding_days" in position and position["holding_days"] > 20:
            exit_stocks.append(stock_code)
            continue
    
    return exit_stocks


def select_stocks(data: pd.DataFrame, scores: pd.DataFrame) -> List[str]:
    """
    选择股票
    
    Args:
        data: 股票数据
        scores: 因子得分
    
    Returns:
        选中的股票代码列表
    """
    # 计算综合得分
    total_score = pd.Series(0.0, index=data.index)
    for factor_name, weight in FACTOR_WEIGHTS.items():
        score_col = f"{{factor_name}}_score"
        if score_col in scores.columns:
            total_score += scores[score_col] * weight
    
    # 检查入场条件
    entry_mask = check_entry_conditions(data, scores)
    
    # 筛选候选池
    candidate_mask = data.index.isin(CANDIDATE_POOL) if CANDIDATE_POOL else pd.Series(True, index=data.index)
    
    # 综合筛选
    final_mask = entry_mask & candidate_mask
    
    # 按得分排序
    selected = total_score[final_mask].sort_values(ascending=False)
    
    # 限制持仓数
    num_positions = min(MAX_POSITIONS, max(MIN_POSITIONS, len(selected)))
    selected_stocks = selected.head(num_positions).index.tolist()
    
    return selected_stocks


def calculate_position_weights(stocks: List[str], scores: pd.DataFrame) -> Dict[str, float]:
    """
    计算仓位权重
    
    Args:
        stocks: 选中的股票列表
        scores: 因子得分
    
    Returns:
        股票代码到权重的字典
    """
    if not stocks:
        return {{}}
    
    # 计算综合得分
    total_scores = {{}}
    for stock in stocks:
        score = 0.0
        for factor_name, weight in FACTOR_WEIGHTS.items():
            score_col = f"{{factor_name}}_score"
            if score_col in scores.columns and stock in scores.index:
                score += scores.loc[stock, score_col] * weight
        total_scores[stock] = score
    
    # 归一化权重
    total = sum(total_scores.values())
    if total == 0:
        # 等权重
        weight = 1.0 / len(stocks)
        return {{stock: min(weight, MAX_POSITION_SIZE) for stock in stocks}}
    
    weights = {{stock: min(score / total, MAX_POSITION_SIZE) for stock, score in total_scores.items()}}
    
    # 确保总权重为1
    total_weight = sum(weights.values())
    if total_weight > 0:
        weights = {{stock: weight / total_weight for stock, weight in weights.items()}}
    
    return weights


def run_strategy(data: pd.DataFrame) -> Dict[str, Any]:
    """
    运行策略
    
    Args:
        data: 股票数据DataFrame
    
    Returns:
        策略结果字典
    """
    # 计算因子得分
    scores = calculate_factor_scores(data)
    
    # 选择股票
    selected_stocks = select_stocks(data, scores)
    
    # 计算仓位权重
    weights = calculate_position_weights(selected_stocks, scores)
    
    return {{
        "selected_stocks": selected_stocks,
        "weights": weights,
        "num_positions": len(selected_stocks),
        "total_weight": sum(weights.values())
    }}


if __name__ == "__main__":
    # 示例使用
    print(f"策略: {{STRATEGY_NAME}}")
    print(f"主线: {{MAINLINE}}")
    print(f"因子: {{', '.join(FACTORS)}}")
    print(f"候选池大小: {{len(CANDIDATE_POOL)}}")
'''
    
    return code


def _save_strategy_code(strategy_code: str, strategy_draft: Dict[str, Any], trace_id: Optional[str]) -> Optional[Path]:
    """保存策略代码到文件"""
    try:
        # 策略保存目录
        strategy_dir = TRQUANT_ROOT / "strategies" / "generated"
        strategy_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        strategy_id = strategy_draft.get("id", f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        strategy_name = strategy_draft.get("name", "未命名策略")
        
        # 清理文件名（移除特殊字符）
        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in strategy_name)
        filename = f"{strategy_id}_{safe_name}.py"
        
        strategy_file = strategy_dir / filename
        
        # 保存文件
        strategy_file.write_text(strategy_code, encoding='utf-8')
        
        logger.info(f"策略代码已保存: {strategy_file}")
        return strategy_file
        
    except Exception as e:
        logger.error(f"保存策略代码失败: {e}", exc_info=True)
        return None


async def _handle_strategy_generate_candidate(
    mainline: str,
    candidate_pool: List[str],
    factors: List[str],
    research_query: str,
    rule_set: str,
    trace_id: Optional[str],
    artifact_policy: str
) -> List:
    """生成候选策略（受Strategy KB规则约束）"""
    from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response
    from mcp_servers.utils.artifacts import create_artifact_if_needed
    from mcp.types import TextContent
    
    if not STRATEGY_KB_AVAILABLE:
        envelope = wrap_error_response(
            error_code="DEPENDENCY_ERROR",
            error_message="Strategy KB Server不可用",
            server_name="trquant-workflow",
            tool_name="workflow.strategy.generate_candidate",
            version="1.0.0",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    try:
        # 1. 获取规则
        rules_result = _handle_rule_get({
            "rule_name": rule_set
        }, trace_id, "inline")
        rules_response = json.loads(rules_result[0].text)
        if not (rules_response.get("ok") or rules_response.get("status") == "success"):
            raise ValueError(f"获取规则失败: {rules_response.get('error', {}).get('message', 'Unknown error')}")
        rules_data = rules_response.get("data", rules_response)
        rules = rules_data.get("rules", {})
        
        # 2. 检索研究卡（如果提供了查询）
        research_cards = []
        citations = []
        if research_query:
            query_result = _handle_strategy_kb_query({
                "query": research_query,
                "top_k": 5
            }, trace_id, "inline")
            query_response = json.loads(query_result[0].text)
            if query_response.get("ok") or query_response.get("status") == "success":
                query_data = query_response.get("data", query_response)
                citations = query_data.get("citations", [])
        
        # 3. 生成策略草案（简化实现）
        strategy_draft = {
            "id": f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": f"{mainline}策略",
            "mainline": mainline,
            "universe": "CN_EQ",
            "candidate_pool": candidate_pool,
            "factors": [{"name": f, "weight": 1.0 / len(factors)} for f in factors],
            "signals": {
                "entry": {
                    "conditions": [f"factor_{f}_score > 0.6" for f in factors]
                },
                "exit": {
                    "conditions": [
                        "drawdown > 10%",
                        "holding_days > 20"
                    ]
                }
            },
            "constraints": rules.get("strategy_constraints", {}) if isinstance(rules, dict) else {},
            "citations": citations,
            "generated_at": datetime.now().isoformat()
        }
        
        # 4. 校验策略草案
        validation_result = _handle_rule_validate({
            "strategy_draft": strategy_draft,
            "rule_set": rule_set
        }, trace_id, "inline")
        validation_response = json.loads(validation_result[0].text)
        if validation_response.get("ok") or validation_response.get("status") == "success":
            validation_data = validation_response.get("data", validation_response)
            is_valid = validation_data.get("is_valid", False)
            errors = validation_data.get("errors", [])
            
            # 如果校验失败，尝试修正（简化实现：仅记录错误）
            if not is_valid:
                strategy_draft["validation_errors"] = errors
                strategy_draft["validation_status"] = "failed"
            else:
                strategy_draft["validation_status"] = "passed"
        else:
            strategy_draft["validation_status"] = "unknown"
            strategy_draft["validation_errors"] = ["校验失败"]
        
        # 5. 获取KB版本
        version_result = _handle_strategy_kb_version_get({}, trace_id, "inline")
        version_response = json.loads(version_result[0].text)
        if version_response.get("ok") or version_response.get("status") == "success":
            version_data = version_response.get("data", version_response)
            strategy_draft["kb_version"] = version_data.get("kb_version", "unknown")
            strategy_draft["factor_version"] = version_data.get("factor_version", "unknown")
            strategy_draft["template_version"] = version_data.get("template_version", "unknown")
        
        # 6. 生成Python策略代码
        strategy_code = _generate_python_strategy_code(strategy_draft)
        
        # 7. 保存Python策略代码
        strategy_file = _save_strategy_code(strategy_code, strategy_draft, trace_id)
        
        # 8. 构建结果
        result = {
            "strategy_draft": strategy_draft,
            "strategy_code": strategy_code,
            "strategy_file": str(strategy_file) if strategy_file else None,
            "citations": citations,
            "validation": {
                "is_valid": strategy_draft.get("validation_status") == "passed",
                "errors": strategy_draft.get("validation_errors", [])
            },
            "kb_version": strategy_draft.get("kb_version", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
        result = create_artifact_if_needed(result, "strategy_draft", artifact_policy, trace_id or "unknown")
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-workflow",
            tool_name="workflow.strategy.generate_candidate",
            version="1.0.0",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
    except Exception as e:
        logger.error(f"生成候选策略失败: {e}", exc_info=True)
        from mcp_servers.utils.error_handler import wrap_exception_response
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-workflow",
            tool_name="workflow.strategy.generate_candidate",
            version="1.0.0",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
