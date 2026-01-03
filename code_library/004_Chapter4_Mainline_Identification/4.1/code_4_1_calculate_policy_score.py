"""
文件名: code_4_1_calculate_policy_score.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_calculate_policy_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: calculate_policy_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def calculate_policy_score(policy_data: Dict[str, float]) -> DimensionScore:
        """
    calculate_policy_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_policy_score的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    factors = []
    total_score = 0.0
    
    # 因子1：政策提及频率
    mention_freq = policy_data.get("policy_mention_freq", 0)
    mention_score = min(100, mention_freq * 10)  # 标准化到0-100
    factor1 = FactorScore(
        name="policy_mention_freq",
        raw_value=mention_freq,
        normalized_score=mention_score,
        weight=0.30,
        weighted_score=mention_score * 0.30,
        data_source="政策文件/新闻",
        calculation_method="近30天政策提及次数，标准化到0-100",
        confidence=0.9
    )
    factors.append(factor1)
    total_score += factor1.weighted_score
    
    # 因子2：政策支持力度
    policy_strength = policy_data.get("policy_strength", 0)
    strength_score = (policy_strength / 5.0) * 100  # 1-5分制转0-100
    factor2 = FactorScore(
        name="policy_strength",
        raw_value=policy_strength,
        normalized_score=strength_score,
        weight=0.35,
        weighted_score=strength_score * 0.35,
        data_source="政策文件分析",
        calculation_method="政策级别×支持方向，1-5分制",
        confidence=0.85
    )
    factors.append(factor2)
    total_score += factor2.weighted_score
    
    # 因子3：政策持续性
    policy_continuity = policy_data.get("policy_continuity", 0)
    continuity_score = min(100, (policy_continuity / 12.0) * 100)  # 12个月为满分
    factor3 = FactorScore(
        name="policy_continuity",
        raw_value=policy_continuity,
        normalized_score=continuity_score,
        weight=0.20,
        weighted_score=continuity_score * 0.20,
        data_source="历史政策分析",
        calculation_method="连续支持月数/预期持续时间",
        confidence=0.8
    )
    factors.append(factor3)
    total_score += factor3.weighted_score
    
    # 因子4：政策落地进度
    implementation = policy_data.get("policy_implementation", 0)
    implementation_score = implementation * 100  # 0-1转0-100
    factor4 = FactorScore(
        name="policy_implementation",
        raw_value=implementation,
        normalized_score=implementation_score,
        weight=0.15,
        weighted_score=implementation_score * 0.15,
        data_source="执行情况跟踪",
        calculation_method="已落地措施数/计划措施数",
        confidence=0.75
    )
    factors.append(factor4)
    total_score += factor4.weighted_score
    
    # 确定评分等级
    level = ScoreLevel.VERY_HIGH if total_score >= 90 else \
            ScoreLevel.HIGH if total_score >= 75 else \
            ScoreLevel.MEDIUM if total_score >= 60 else \
            ScoreLevel.LOW if total_score >= 40 else \
            ScoreLevel.VERY_LOW
    
    return DimensionScore(
        dimension="policy",
        factors=factors,
        total_score=total_score,
        weight=0.20,
        weighted_score=total_score * 0.20,
        level=level,
        interpretation=f"政策支持度得分{total_score:.2f}，{level.value}"
    )