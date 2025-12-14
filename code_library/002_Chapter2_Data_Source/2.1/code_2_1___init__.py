"""
文件名: code_2_1___init__.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:42
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from data_sources.base_source import BaseDataSource
import jqdatasdk as jq
import pandas as pd

class JQDataSource(BaseDataSource):
    """聚宽数据源实现"""
    
    def __init__(self):
        super().__init__("jqdata")
        self.username = None
        self.password = None
    
    def connect(self, username: str = None, password: str = None, **kwargs) -> bool:
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
        try:
            if username and password:
                self.username = username
                self.password = password
            else:
                # 从配置文件读取
                from core.config import get_config
                config = get_config()
                self.username = config.get("jqdata", "username")
                self.password = config.get("jqdata", "password")
            
            jq.auth(self.username, self.password)
            self._connected = True
            self._connection_time = datetime.now()
            logger.info("JQData连接成功")
            return True
        except Exception as e:
            self._connected = False
            self._last_error = str(e)
            logger.error(f"JQData连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self._connected:
            jq.logout()
            self._connected = False
            logger.info("JQData已断开")
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        if not self._connected:
            return {"status": "error", "latency": None, "error": "未连接"}
        
        try:
            start_time = datetime.now()
            # 测试查询
            jq.get_price("000001.XSHE", count=1, end_date=datetime.now().strftime("%Y-%m-%d"))
            latency = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "status": "ok",
                "latency": int(latency),
                "error": None,
                "checked_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "latency": None,
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }
    
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str, fields: List[str] = None) -> pd.DataFrame:
        """获取日线数据"""
        if not self._connected:
            raise ConnectionError("JQData未连接")
        
        # 转换股票代码格式
        jq_symbol = self._convert_symbol(symbol)
        
        # 获取数据
        data = jq.get_price(
            jq_symbol,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=fields or ['open', 'high', 'low', 'close', 'volume', 'money']
        )
        
        # 重命名列
        data.rename(columns={'money': 'amount'}, inplace=True)
        data.index.name = 'date'
        
        return data
    
<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1___init__.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：