"""
文件名: code_9_4_execute_step_with_mcp.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.4/code_9_4_execute_step_with_mcp.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.4_GUI_Workflow_System_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: execute_step_with_mcp

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/widgets/workflow_executor.py (MCP集成部分)
class WorkflowExecutor(QThread):
    """工作流执行引擎（扩展MCP集成）"""
    
    def execute_step_with_mcp(self, step_id: str):
            """
    execute_step_with_mcp函数
    
    **设计原理**：
    - **核心功能**：实现execute_step_with_mcp的核心逻辑
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
        # 步骤2: 市场分析 - 使用MCP工具
        if step_id == "market_trend":
            from mcp_client import MCPClient
            
            mcp_client = MCPClient()
            
            # 调用MCP工具获取市场状态
            market_status = mcp_client.call_tool(
                "trquant_market_status",
                {"universe": "CN_EQ"}
            )
            
            # 调用MCP工具获取投资主线
            mainlines = mcp_client.call_tool(
                "trquant_mainlines",
                {"time_horizon": "short", "top_n": 10}
            )
            
            return {
                'success': True,
                'summary': '市场分析完成',
                'details': {
                    'market_status': market_status,
                    'mainlines': mainlines
                }
            }
        
        # 步骤5: 因子推荐 - 使用MCP工具
        elif step_id == "factor":
            from mcp_client import MCPClient
            
            mcp_client = MCPClient()
            
            # 获取市场状态
            market_status = self.state_manager.states.get("market_trend")
            market_regime = "neutral"
            if market_status and market_status.result:
                market_regime = market_status.result.get('details', {}).get('regime', 'neutral')
            
            # 调用MCP工具推荐因子
            factors = mcp_client.call_tool(
                "trquant_recommend_factors",
                {
                    "market_regime": market_regime,
                    "top_n": 10
                }
            )
            
            return {
                'success': True,
                'summary': '因子推荐完成',
                'details': {
                    'factors': factors
                }
            }
        
        # 步骤6: 策略生成 - 使用MCP工具
        elif step_id == "strategy":
            from mcp_client import MCPClient
            
            mcp_client = MCPClient()
            
            # 获取因子列表
            factor_state = self.state_manager.states.get("factor")
            factors = []
            if factor_state and factor_state.result:
                factors = [
                    f['name'] for f in factor_state.result.get('details', {}).get('factors', [])
                ]
            
            # 调用MCP工具生成策略
            strategy_code = mcp_client.call_tool(
                "trquant_generate_strategy",
                {
                    "factors": factors,
                    "style": "multi_factor",
                    "platform": "ptrade",
                    "max_position": 0.1,
                    "stop_loss": 0.08,
                    "take_profit": 0.2
                }
            )
            
            # 保存策略代码
            strategy_file = self._save_strategy_code(strategy_code)
            
            return {
                'success': True,
                'summary': '策略生成完成',
                'details': {
                    'strategy_file': strategy_file,
                    'strategy_code': strategy_code
                }
            }
        
        # 其他步骤使用WorkflowOrchestrator
        else:
            return self.execute_step(step_id)