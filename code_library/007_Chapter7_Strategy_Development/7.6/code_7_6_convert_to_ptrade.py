"""
文件名: code_7_6_convert_to_ptrade.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.6/code_7_6_convert_to_ptrade.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.6_Strategy_Deployment_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: convert_to_ptrade

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, Any
import re

class StrategyCodeConverter:
    """策略代码转换器（聚宽风格 → PTrade/QMT格式）"""
    
    def convert_to_ptrade(
        self,
        jq_strategy_code: str
    ) -> str:
        """
        将聚宽风格策略代码转换为PTrade格式
        
        **设计原理**：
        - **正则替换**：使用正则表达式替换API调用，保持代码逻辑不变
        - **模块映射**：将聚宽API映射到PTrade API，保持功能一致性
        - **初始化注入**：自动添加PTrade初始化代码，确保平台正确初始化
        
        **为什么这样设计**：
        1. **自动化**：自动转换减少人工错误，提高部署效率
        2. **一致性**：保持策略逻辑不变，只替换API调用
        3. **可维护性**：集中管理转换规则，便于维护和扩展
        
        **使用场景**：
        - 策略部署到PTrade平台前，自动转换代码格式
        - 策略从聚宽平台迁移到PTrade平台
        - 策略代码格式标准化
        
        **注意事项**：
        - 转换后需要人工检查，确保API映射正确
        - 某些聚宽特有功能可能需要手动调整
        - 建议在转换后进行回测验证，确保功能正常
        
        Args:
            jq_strategy_code: 聚宽风格策略代码
        
        Returns:
            str: PTrade格式策略代码
        """
        # 设计原理：代码转换采用正则替换
        # 原因：聚宽和PTrade API相似，只需替换模块名和函数调用
        # 实现方式：使用re.sub进行批量替换，保持代码逻辑不变
        ptrade_code = jq_strategy_code
        
        # 设计原理：替换导入语句
        # 原因：PTrade使用不同的API模块，需要替换导入
        # 映射关系：jqdata → ptrade_api
        ptrade_code = re.sub(
            r'from jqdata import \*',
            'from ptrade_api import *',
            ptrade_code
        )
        
        # 设计原理：替换API调用
        # 原因：PTrade API需要模块前缀，聚宽API是全局函数
        # 实现方式：在函数名前添加ptrade.前缀
        # get_price -> ptrade.get_price
        ptrade_code = re.sub(
            r'get_price\(',
            'ptrade.get_price(',
            ptrade_code
        )
        
        # order -> ptrade.order
        ptrade_code = re.sub(
            r'order\(',
            'ptrade.order(',
            ptrade_code
        )
        
        # 设计原理：添加PTrade初始化代码
        # 原因：PTrade平台需要显式初始化，聚宽平台自动初始化
        # 实现方式：在代码开头添加初始化代码
        ptrade_init = """
# PTrade平台初始化
import ptrade_api as ptrade
ptrade.init()
"""
        ptrade_code = ptrade_init + ptrade_code
        
        return ptrade_code
    
    def convert_to_qmt(
        self,
        jq_strategy_code: str
    ) -> str:
        """
        将聚宽风格策略代码转换为QMT格式
        
        Args:
            jq_strategy_code: 聚宽风格策略代码
        
        Returns:
            str: QMT格式策略代码
        """
        # 1. 替换导入语句
        qmt_code = jq_strategy_code
        
        # 替换 jqdata 导入
        qmt_code = re.sub(
            r'from jqdata import \*',
            'from qmt_api import *',
            qmt_code
        )
        
        # 2. 替换API调用
        # get_price -> qmt.get_price
        qmt_code = re.sub(
            r'get_price\(',
            'qmt.get_price(',
            qmt_code
        )
        
        # order -> qmt.order
        qmt_code = re.sub(
            r'order\(',
            'qmt.order(',
            qmt_code
        )
        
        # 3. 添加QMT初始化代码
        qmt_init = """
# QMT平台初始化
import qmt_api as qmt
qmt.init()
"""
        qmt_code = qmt_init + qmt_code
        
        return qmt_code