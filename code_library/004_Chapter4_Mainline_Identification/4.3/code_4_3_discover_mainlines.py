"""
文件名: code_4_3_discover_mainlines.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_discover_mainlines.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: discover_mainlines

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.base_mainline import BaseMainlineEngine, Mainline, MainlineStage
from typing import List, Dict, Any

class AShareMainlineEngine(BaseMainlineEngine):
    """A股主线识别引擎实现"""
    
    def discover_mainlines(
        self, 
        include_emerging: bool = True, 
        min_score: float = 60
    ) -> List[Mainline]:
            """
    discover_mainlines函数
    
    **设计原理**：
    - **核心功能**：实现discover_mainlines的核心逻辑
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
        # Step 1: 宏观前瞻分析
        macro_data = self._analyze_macro()
        
        # Step 2: 中观验证分析
        capital_data = self._analyze_capital()
        industry_data = self._analyze_industry()
        catalyst_calendar = self.get_catalyst_calendar(days=90)
        
        # Step 3: 微观确认分析
        technical_data = self._analyze_technical()
        sentiment_data = self.analyze_market_sentiment()
        
        # Step 4: 综合生成主线
        mainlines = self._generate_mainlines(
            macro_data=macro_data,
            capital_data=capital_data,
            industry_data=industry_data,
            technical_data=technical_data,
            sentiment_data=sentiment_data,
            catalyst_calendar=catalyst_calendar
        )
        
        # Step 5: 过滤主线
        if not include_emerging:
            mainlines = [
                m for m in mainlines 
                if m.stage != MainlineStage.EMERGING
            ]
        
        mainlines = [
            m for m in mainlines 
            if m.score.total_score >= min_score
        ]
        
        # Step 6: 排序
        mainlines.sort(
            key=lambda m: m.score.total_score, 
            reverse=True
        )
        
        return mainlines
    
    def _generate_mainlines(
        self,
        macro_data: Dict,
        capital_data: Dict,
        industry_data: Dict,
        technical_data: Dict,
        sentiment_data: Dict,
        catalyst_calendar: List
    ) -> List[Mainline]:
        """
        综合生成主线
        
        基于三层分析结果，综合生成投资主线
        """
        mainlines = []
        
        # 1. 从宏观前瞻中提取主线方向
        policy_mainlines = self._extract_policy_mainlines(macro_data)
        industry_mainlines = self._extract_industry_mainlines(industry_data)
        
        # 2. 用中观验证过滤主线
        validated_mainlines = self._validate_mainlines(
            policy_mainlines + industry_mainlines,
            capital_data,
            catalyst_calendar
        )
        
        # 3. 用微观确认优化主线
        confirmed_mainlines = self._confirm_mainlines(
            validated_mainlines,
            technical_data,
            sentiment_data
        )
        
        # 4. 为主线评分
        for mainline in confirmed_mainlines:
            score = self.scoring_model.score_mainline(mainline)
            mainline.score = score
            mainlines.append(mainline)
        
        return mainlines