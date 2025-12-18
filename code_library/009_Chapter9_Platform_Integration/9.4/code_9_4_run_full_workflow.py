"""
文件名: code_9_4_run_full_workflow.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.4/code_9_4_run_full_workflow.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.4_GUI_Workflow_System_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: run_full_workflow

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# core/workflow_orchestrator.py (关键方法)
class WorkflowOrchestrator:
    """工作流编排器"""
    
    def run_full_workflow(
        self,
        callback: Optional[Callable[[str, WorkflowResult], None]] = None
    ) -> FullWorkflowResult:
            """
    run_full_workflow函数
    
    **设计原理**：
    - **核心功能**：实现run_full_workflow的核心逻辑
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
        import time
        start_time = time.time()
        
        steps = []
        
        # 步骤1: 数据源检测
        result = self.check_data_sources()
        steps.append(result)
        if callback:
            callback("数据源检测", result)
        
        if not result.success:
            return FullWorkflowResult(
                success=False,
                steps=steps,
                total_time=time.time() - start_time
            )
        
        # 步骤2: 市场趋势分析
        result = self.analyze_market_trend()
        steps.append(result)
        if callback:
            callback("市场趋势", result)
        
        # 步骤3: 投资主线识别
        result = self.identify_mainlines()
        steps.append(result)
        if callback:
            callback("投资主线", result)
        
        # 步骤4: 候选池构建
        result = self.build_candidate_pool()
        steps.append(result)
        if callback:
            callback("候选池构建", result)
        
        # 步骤5: 因子推荐
        result = self.recommend_factors()
        steps.append(result)
        if callback:
            callback("因子推荐", result)
        
        # 步骤6: 策略生成
        result = self.generate_strategy()
        steps.append(result)
        if callback:
            callback("策略生成", result)
        
        strategy_file = result.details.get('strategy_file') if result.success else None
        
        return FullWorkflowResult(
            success=all(s.success for s in steps),
            steps=steps,
            strategy_file=strategy_file,
            total_time=time.time() - start_time
        )