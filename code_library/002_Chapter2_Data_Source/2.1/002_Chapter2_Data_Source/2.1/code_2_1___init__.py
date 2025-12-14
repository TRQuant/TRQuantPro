"""
文件名: code_2_1___init__.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:30:08
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

import akshare as ak
import pandas as pd

class AKShareSource(BaseDataSource):
    """AKShare数据源实现"""
    
    def __init__(self):
        super().__init__("akshare")
    
    def connect(self, **kwargs) -> bool:
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
        self._connected = True
        return True
    
    def disconnect(self):
        """AKShare无需断开"""
        self._connected = False
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            start_time = datetime.now()
            # 测试查询
            ak.stock_zh_a_hist(symbol="000001", period="daily", adjust="")
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
        # AKShare的股票代码格式：000001（不带后缀）
        code = symbol.split('.')[0]
        
        # 获取数据
        data = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
            adjust=""
        )
        
        # 重命名列
        data.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount'
        }, inplace=True)
        
        # 设置日期为索引
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        
        return data