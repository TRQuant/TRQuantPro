"""
文件名: code_4_2_filter_by_industries.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2_filter_by_industries.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: filter_by_industries

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_by_industries(
    mainlines: List[Mainline],
    industries: List[str],
    match_all: bool = False
) -> List[Mainline]:
    """
    根据行业筛选主线
    
    Args:
        mainlines: 主线列表
        industries: 行业列表
        match_all: 是否要求匹配所有行业（默认False，匹配任一即可）
    
    Returns:
        筛选后的主线列表
    """
    # 设计原理：行业筛选支持两种模式
    # 原因：不同场景需要不同的筛选逻辑
    # match_all=True：要求匹配所有行业（交集），适用于精确筛选
    # match_all=False：匹配任一行业即可（并集），适用于宽泛筛选
    # 为什么这样设计：提供灵活性，适应不同的筛选需求
    if match_all:
        # 设计原理：交集筛选（AND逻辑）
        # 原因：要求主线同时包含所有指定行业，筛选更严格
        # 使用场景：需要主线同时涉及多个相关行业时
        filtered = [
            mainline for mainline in mainlines
            if all(ind in mainline.sectors for ind in industries)
        ]
    else:
        # 设计原理：并集筛选（OR逻辑）
        # 原因：主线包含任一指定行业即可，筛选更宽松
        # 使用场景：需要主线涉及任一相关行业时
        filtered = [
            mainline for mainline in mainlines
            if any(ind in mainline.sectors for ind in industries)
        ]
    
    return filtered

# 使用示例
mainlines = get_all_mainlines()
# 筛选包含"新能源"或"人工智能"的主线
filtered_mainlines = filter_by_industries(
    mainlines,
    industries=["新能源", "人工智能"],
    match_all=False
)