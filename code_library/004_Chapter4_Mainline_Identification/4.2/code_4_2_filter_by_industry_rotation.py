"""
文件名: code_4_2_filter_by_industry_rotation.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2_filter_by_industry_rotation.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: filter_by_industry_rotation

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_by_industry_rotation(
    mainlines: List[Mainline],
    rotation_signal: Dict[str, str]
) -> List[Mainline]:
        """
    filter_by_industry_rotation函数
    
    **设计原理**：
    - **核心功能**：实现filter_by_industry_rotation的核心逻辑
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
    filtered = []
    
    for mainline in mainlines:
        # 检查主线的行业轮动信号
        rotation_scores = []
        for sector in mainline.sectors:
            signal = rotation_signal.get(sector, "neutral")
            if signal == "up":
                rotation_scores.append(1.0)
            elif signal == "neutral":
                rotation_scores.append(0.5)
            else:  # down
                rotation_scores.append(0.0)
        
        # 如果平均轮动得分>0.5，则保留
        avg_rotation_score = sum(rotation_scores) / len(rotation_scores) if rotation_scores else 0.0
        if avg_rotation_score > 0.5:
            mainline.rotation_score = avg_rotation_score
            filtered.append(mainline)
    
    # 按轮动得分排序
    filtered.sort(key=lambda m: m.rotation_score, reverse=True)
    
    return filtered

# 使用示例
mainlines = get_all_mainlines()
rotation_signal = {
    "新能源": "up",
    "人工智能": "up",
    "半导体": "neutral",
    "医药": "down",
    "消费": "neutral"
}
filtered_mainlines = filter_by_industry_rotation(mainlines, rotation_signal)