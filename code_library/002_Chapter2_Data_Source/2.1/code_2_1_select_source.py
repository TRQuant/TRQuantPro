"""
文件名: code_2_1_select_source.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_select_source.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:59
函数/类名: select_source

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def select_source(self, data_type: str, criteria: List[str] = None) -> str:
        """
    select_source函数
    
    **设计原理**：
    - **核心功能**：实现select_source的核心逻辑
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
    if criteria is None:
        criteria = ["data_quality", "completeness", "speed"]
    
    candidates = self.priority.get(data_type, list(self.sources.keys()))
    
    # 评分系统
    scores = {}
    for source_name in candidates:
        if source_name not in self.sources:
            continue
        
        source = self.sources[source_name]
        score = 0
        
        # 健康检查
        health = source.health_check()
        if health["status"] != "ok":
            continue  # 跳过不健康的数据源
        
        # 根据标准评分
        if "speed" in criteria:
            # 速度评分：延迟越低分数越高
            latency = health.get("latency", 1000)
            speed_score = max(0, 100 - latency / 10)
            score += speed_score * 0.3
        
        if "data_quality" in criteria:
            # 数据质量评分（基于历史统计）
            quality_score = self._get_quality_score(source_name)
            score += quality_score * 0.4
        
        if "completeness" in criteria:
            # 完整性评分（基于历史统计）
            completeness_score = self._get_completeness_score(source_name, data_type)
            score += completeness_score * 0.3
        
        scores[source_name] = score
    
    # 选择分数最高的数据源
    if sc<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1_health_check_all.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：