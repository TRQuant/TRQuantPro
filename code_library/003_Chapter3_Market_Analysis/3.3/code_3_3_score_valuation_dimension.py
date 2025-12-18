"""估值维度评分函数"""
import pandas as pd
from typing import Dict, Any

def score_valuation_dimension(pe_ratio: float, pb_ratio: float, pe_percentile: float, pb_percentile: float) -> Dict[str, Any]:
    score = 0.0
    details = {}
    if pe_percentile <= 20: pe_score = 30
    elif pe_percentile <= 40: pe_score = 25
    elif pe_percentile <= 60: pe_score = 20
    elif pe_percentile <= 80: pe_score = 12
    else: pe_score = max(0, 12 - (pe_percentile - 80) * 0.6)
    score += pe_score
    details['pe_score'] = round(pe_score, 2)
    details['pe_ratio'] = pe_ratio
    details['pe_percentile'] = pe_percentile
    if pb_percentile <= 20: pb_score = 30
    elif pb_percentile <= 40: pb_score = 25
    elif pb_percentile <= 60: pb_score = 20
    elif pb_percentile <= 80: pb_score = 12
    else: pb_score = max(0, 12 - (pb_percentile - 80) * 0.6)
    score += pb_score
    details['pb_score'] = round(pb_score, 2)
    details['pb_ratio'] = pb_ratio
    details['pb_percentile'] = pb_percentile
    combined_score = (pe_percentile + pb_percentile) / 2
    if combined_score <= 30: combined_bonus = 20
    elif combined_score <= 50: combined_bonus = 15
    elif combined_score <= 70: combined_bonus = 10
    else: combined_bonus = 5
    score += combined_bonus
    details['combined_bonus'] = combined_bonus
    details['combined_percentile'] = round(combined_score, 2)
    return {'valuation_score': round(score, 2), 'details': details, 'level': '优秀' if score >= 80 else '良好' if score >= 60 else '一般' if score >= 40 else '较差'}
