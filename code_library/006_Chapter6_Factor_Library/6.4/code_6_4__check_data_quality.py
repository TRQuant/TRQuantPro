"""
文件名: code_6_4__check_data_quality.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4__check_data_quality.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: _check_data_quality

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def _check_data_quality(self, stocks: List[str], date: datetime) -> bool:
        """
    _check_data_quality函数
    
    **设计原理**：
    - **核心功能**：实现_check_data_quality的核心逻辑
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
    try:
        import jqdatasdk as jq
        
        # 检查价格数据
        prices = jq.get_price(
            stocks[:100],  # 抽样检查
            end_date=date,
            count=1,
            fields=["close"],
            panel=False
        )
        
        if prices.empty:
            logger.warning("价格数据为空")
            return False
        
        # 检查覆盖率
        coverage = len(prices) / len(stocks[:100])
        if coverage < 0.8:
            logger.warning(f"数据覆盖率过低: {coverage:.2%}")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"数据质量检查失败: {e}")
        return False