"""
文件名: code_9_2___init__.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.2/code_9_2___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.2_QMT_Integration_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.strategy_converter import StrategyCodeConverter

class QMTStrategyDeployer:
    """QMT策略部署器"""
    
    def __init__(self, connection: QMTConnection):
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
        部署策略到QMT平台
        
        Args:
            jq_strategy_path: 聚宽风格策略代码路径
            strategy_name: 策略名称
        
        Returns:
            Dict: 部署结果
        """
        # 1. 读取聚宽风格策略代码
        with open(jq_strategy_path, 'r', encoding='utf-8') as f:
            jq_code = f.read()
        
        # 2. 转换为QMT格式
        qmt_code = self.converter.convert_to_qmt(jq_code)
        
        # 3. 保存QMT格式代码
        qmt_strategy_path = jq_strategy_path.replace('.py', '_qmt.py')
        with open(qmt_strategy_path, 'w', encoding='utf-8') as f:
            f.write(qmt_code)
        
        # 4. 上传到QMT平台
        upload_result = self._upload_to_qmt(
            qmt_strategy_path,
            strategy_name
        )
        
        return {
            'strategy_name': strategy_name,
            'qmt_code_path': qmt_strategy_path,
            'upload_result': upload_result
        }
    
    def _upload_to_qmt(
        self,
        strategy_path: str,
        strategy_name: str
    ) -> Dict[str, Any]:
        """上传策略到QMT平台"""
        # QMT策略文件需要放在QMT的策略目录
        qmt_strategies_dir = Path(self.connection.config.qmt_path) / "userdata_mini" / "strategies"
        qmt_strategies_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制策略文件到QMT策略目录
        target_path = qmt_strategies_dir / f"{strategy_name}.py"
        shutil.copy2(strategy_path, target_path)
        
        return {
            'success': True,
            'strategy_path': str(target_path),
            'message': '策略上传成功'
        }