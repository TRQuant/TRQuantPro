"""
文件名: code_9_1___init__.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.1/code_9_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.1_PTrade_Integration_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.strategy_converter import StrategyCodeConverter

class PTradeStrategyDeployer:
    """PTrade策略部署器"""
    
    def __init__(self, connection: PTradeConnection):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        self.connection = connection
        self.converter = StrategyCodeConverter()
    
    def deploy_strategy(
        self,
        jq_strategy_path: str,
        strategy_name: str
    ) -> Dict[str, Any]:
        """
        部署策略到PTrade平台
        
        Args:
            jq_strategy_path: 聚宽风格策略代码路径
            strategy_name: 策略名称
        
        Returns:
            Dict: 部署结果
        """
        # 1. 读取聚宽风格策略代码
        with open(jq_strategy_path, 'r', encoding='utf-8') as f:
            jq_code = f.read()
        
        # 2. 转换为PTrade格式
        ptrade_code = self.converter.convert_to_ptrade(jq_code)
        
        # 3. 保存PTrade格式代码
        ptrade_strategy_path = jq_strategy_path.replace('.py', '_ptrade.py')
        with open(ptrade_strategy_path, 'w', encoding='utf-8') as f:
            f.write(ptrade_code)
        
        # 4. 上传到PTrade平台
        upload_result = self._upload_to_ptrade(
            ptrade_strategy_path,
            strategy_name
        )
        
        return {
            'strategy_name': strategy_name,
            'ptrade_code_path': ptrade_strategy_path,
            'upload_result': upload_result
        }
    
    def _upload_to_ptrade(
        self,
        strategy_path: str,
        strategy_name: str
    ) -> Dict[str, Any]:
        """上传策略到PTrade平台"""
        # 读取策略代码
        with open(strategy_path, 'r', encoding='utf-8') as f:
            strategy_code = f.read()
        
        # 构建上传消息
        upload_msg = {
            'action': 'upload_strategy',
            'session_id': self.connection.session_id,
            'strategy_name': strategy_name,
            'strategy_code': strategy_code,
            'timestamp': datetime.now().isoformat()
        }
        
        # 发送上传消息
        self.connection._send_message(upload_msg)
        
        # 接收上传响应
        response = self.connection._receive_message()
        
        if response.get('status') == 'success':
            return {
                'success': True,
                'strategy_id': response.get('strategy_id'),
                'message': '策略上传成功'
            }
        else:
            return {
                'success': False,
                'error': response.get('message'),
                'message': '策略上传失败'
            }