"""
文件名: code_4_2_filter_by_industry_weights.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2_filter_by_industry_weights.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: filter_by_industry_weights

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_by_industry_weights(
    mainlines: List[Mainline],
    industry_weights: Dict[str, float],
    min_weight: float = 0.1
) -> List[Mainline]:
    """
    根据行业权重筛选主线
    
    Args:
        mainlines: 主线列表
        industry_weights: 行业权重字典 {行业名: 权重}
        min_weight: 最小权重阈值
    
    Returns:
        筛选后的主线列表（按行业权重排序）
    """
    filtered = []
    
    # 设计原理：行业权重筛选
    # 原因：不同行业的重要性不同，需要根据权重筛选
    # 实现方式：计算主线的行业权重得分，按得分筛选和排序
    # 为什么这样设计：优先选择权重高的行业，提高筛选的针对性
    for mainline in mainlines:
        # 设计原理：累加行业权重得分
        # 原因：主线可能涉及多个行业，需要累加权重
        # 实现方式：遍历主线的所有行业，累加对应的权重
        industry_score = 0.0
        for sector in mainline.sectors:
            weight = industry_weights.get(sector, 0.0)
            industry_score += weight
        
        # 设计原理：阈值筛选
        # 原因：只保留行业权重得分达到阈值的主线
        # 为什么这样设计：过滤掉行业权重过低的主线，提高筛选质量
        if industry_score >= min_weight:
            # 设计原理：临时属性存储得分
            # 原因：便于后续排序，不修改主线原始数据
            mainline.industry_score = industry_score
            filtered.append(mainline)
    
    # 设计原理：按得分排序
    # 原因：优先展示权重高的主线，便于用户选择
    # 实现方式：使用sort按industry_score降序排序
    filtered.sort(key=lambda m: m.industry_score, reverse=True)
    
    return filtered

# 使用示例
mainlines = get_all_mainlines()
industry_weights = {
    "新能源": 0.3,
    "人工智能": 0.25,
    "半导体": 0.2,
    "医药": 0.15,
    "消费": 0.1
}
filtered_mainlines = filter_by_industry_weights(
    mainlines,
    industry_weights,
    min_weight=0.2
)