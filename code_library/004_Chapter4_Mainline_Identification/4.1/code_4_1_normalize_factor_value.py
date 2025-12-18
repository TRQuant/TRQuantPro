"""
文件名: code_4_1_normalize_factor_value.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_normalize_factor_value.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: normalize_factor_value

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def normalize_factor_value(
    raw_value: float,
    thresholds: Dict[str, float],
    inverse: bool = False
) -> float:
    """
    标准化因子值到0-100分
    
    **设计原理**：
    - **分段线性映射**：使用阈值分段，每段内线性插值
    - **阈值设计**：高/中/低三个阈值，对应100/60/30分
    - **反向支持**：支持正向指标（越大越好）和反向指标（越小越好）
    
    **为什么这样设计**：
    1. **直观性**：阈值分段比连续函数更直观，便于理解和调优
    2. **灵活性**：不同因子可以使用不同阈值，适应不同分布
    3. **鲁棒性**：分段线性映射对异常值不敏感，比非线性映射更稳定
    
    **阈值设计**：
    - **高阈值**：对应100分，表示优秀水平
    - **中阈值**：对应60分，表示中等水平
    - **低阈值**：对应30分，表示较差水平
    - **分段插值**：阈值之间线性插值，保证连续性
    
    **替代方案对比**：
    - **方案A：Z-score标准化**
      - 优点：统计意义明确
      - 缺点：需要历史数据，对异常值敏感
    - **方案B：分位数映射**
      - 优点：自适应，不依赖阈值
      - 缺点：需要大量历史数据，计算复杂
    - **当前方案：阈值分段线性映射**
      - 优点：直观、灵活、鲁棒
      - 缺点：需要人工设定阈值
    
    **使用场景**：
    - 主线评分时，将不同量纲的因子值标准化到统一尺度
    - 因子组合时，需要统一量纲
    - 因子评价时，需要比较不同因子的表现
    
    Args:
        raw_value: 原始值
        thresholds: 阈值字典 {"high": 高阈值, "medium": 中阈值, "low": 低阈值}
        inverse: 是否反向（越低越好）
    
    Returns:
        标准化得分（0-100）
    """
    if inverse:
        # 设计原理：反向指标处理
        # 原因：某些因子（如PE、PB）越低越好，需要反向评分
        # 反向指标：值越小，得分越高
        if raw_value <= thresholds["low"]:
            return 100
        elif raw_value <= thresholds["medium"]:
            # 设计原理：线性插值
            # 原因：保证连续性，避免跳跃
            # 线性插值：low->100, medium->60
            return 100 - (raw_value - thresholds["low"]) / \
                   (thresholds["medium"] - thresholds["low"]) * 40
        elif raw_value <= thresholds["high"]:
            # 线性插值：medium->60, high->30
            return 60 - (raw_value - thresholds["medium"]) / \
                   (thresholds["high"] - thresholds["medium"]) * 30
        else:
            # 设计原理：超过高阈值时得分递减
            # 原因：避免极端值获得过高分数
            return max(0, 30 - (raw_value - thresholds["high"]) * 10)
    else:
        # 设计原理：正向指标处理
        # 原因：大多数因子（如增长率、收益率）越大越好
        # 正向指标：值越大，得分越高
        if raw_value >= thresholds["high"]:
            return 100
        elif raw_value >= thresholds["medium"]:
            # 线性插值：medium->60, high->100
            return 60 + (raw_value - thresholds["medium"]) / \
                   (thresholds["high"] - thresholds["medium"]) * 40
        elif raw_value >= thresholds["low"]:
            # 线性插值：low->30, medium->60
            return 30 + (raw_value - thresholds["low"]) / \
                   (thresholds["medium"] - thresholds["low"]) * 30
        else:
            # 低于低阈值，得分递减
            return max(0, 30 - (thresholds["low"] - raw_value) * 10)