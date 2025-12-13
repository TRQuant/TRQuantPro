"""
五维综合评分函数

设计原理：
1. 综合五个维度的评分，按权重加权求和
2. 各维度权重：宏观(20%)、资金(25%)、行业(20%)、技术(15%)、估值(20%)
3. 返回综合评分和各维度详细评分
"""

import pandas as pd
from typing import Dict, Any
import sys
import os
from pathlib import Path

# 添加当前目录到路径，以便导入同目录下的模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入各维度评分函数
try:
    from code_3_3_score_macro_dimension import score_macro_dimension
    from code_3_3_score_capital_dimension import score_capital_dimension
    from code_3_3_score_industry_dimension import score_industry_dimension
    from code_3_3_score_technical_dimension import score_technical_dimension
    from code_3_3_score_valuation_dimension import score_valuation_dimension
except ImportError:
    # 如果直接导入失败，尝试动态导入
    import importlib.util
    def load_module(name):
        spec = importlib.util.spec_from_file_location(name, current_dir / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    macro_module = load_module("code_3_3_score_macro_dimension")
    capital_module = load_module("code_3_3_score_capital_dimension")
    industry_module = load_module("code_3_3_score_industry_dimension")
    technical_module = load_module("code_3_3_score_technical_dimension")
    valuation_module = load_module("code_3_3_score_valuation_dimension")
    
    score_macro_dimension = macro_module.score_macro_dimension
    score_capital_dimension = capital_module.score_capital_dimension
    score_industry_dimension = industry_module.score_industry_dimension
    score_technical_dimension = technical_module.score_technical_dimension
    score_valuation_dimension = valuation_module.score_valuation_dimension

DIMENSION_WEIGHTS = {
    'macro': 0.20,
    'capital': 0.25,
    'industry': 0.20,
    'technical': 0.15,
    'valuation': 0.20
}

def calculate_comprehensive_score(macro_data: dict, capital_data: dict, industry_data: dict, technical_data: dict, valuation_data: dict) -> Dict[str, Any]:
    macro_result = score_macro_dimension(**macro_data)
    capital_result = score_capital_dimension(**capital_data)
    industry_result = score_industry_dimension(**industry_data)
    technical_result = score_technical_dimension(**technical_data)
    valuation_result = score_valuation_dimension(**valuation_data)
    
    weighted_score = (
        macro_result['macro_score'] * DIMENSION_WEIGHTS['macro'] +
        capital_result['capital_score'] * DIMENSION_WEIGHTS['capital'] +
        industry_result['industry_score'] * DIMENSION_WEIGHTS['industry'] +
        technical_result['technical_score'] * DIMENSION_WEIGHTS['technical'] +
        valuation_result['valuation_score'] * DIMENSION_WEIGHTS['valuation']
    )
    
    return {
        'comprehensive_score': round(weighted_score, 2),
        'dimension_scores': {
            'macro': macro_result,
            'capital': capital_result,
            'industry': industry_result,
            'technical': technical_result,
            'valuation': valuation_result
        },
        'weights': DIMENSION_WEIGHTS,
        'level': '优秀' if weighted_score >= 80 else '良好' if weighted_score >= 60 else '一般' if weighted_score >= 40 else '较差'
    }
