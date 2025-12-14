"""
文件名: code_5_1___post_init__.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.1/code_5_1___post_init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __post_init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

@dataclass
class StockPool:
    """
    股票池
    
    包含：
    - 股票列表：StockPoolItem列表
    - 元信息：描述、创建时间、更新时间
    - 统计信息：按来源、周期、类型统计
    """
    stocks: List[StockPoolItem] = field(default_factory=list)
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    summary: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
    
    def add_stock(self, stock: StockPoolItem) -> bool:
        """
        添加股票（去重）
        
        **设计原理**：
        - **去重机制**：基于股票代码去重，避免重复添加
        - **时间戳更新**：添加股票时自动更新更新时间
        - **返回值设计**：返回是否成功添加，便于调用者判断
        
        **为什么这样设计**：
        1. **数据一致性**：避免同一股票重复添加，保证数据一致性
        2. **可追溯性**：更新时间戳记录股票池变更历史
        3. **调用便利**：返回值明确，便于调用者处理
        
        **使用场景**：
        - 从多个来源合并股票池时，自动去重
        - 动态更新股票池时，避免重复添加
        - 批量添加股票时，自动过滤重复
        
        **注意事项**：
        - 去重基于股票代码，不同来源的同一股票会被去重
        - 如果需要保留不同来源的同一股票，需要修改去重逻辑
        
        Args:
            stock: 股票池条目
        
        Returns:
            是否成功添加（False表示已存在）
        """
        # 设计原理：基于股票代码去重
        # 原因：同一股票不应重复添加，避免数据冗余
        # 实现方式：遍历现有股票列表，检查代码是否已存在
        if any(s.code == stock.code for s in self.stocks):
            return False
        
        # 设计原理：添加股票并更新时间戳
        # 原因：记录股票池变更历史，便于追踪和审计
        self.stocks.append(stock)
        self.updated_at = datetime.now().isoformat()
        return True
    
    def get_codes(self) -> List[str]:
        """获取股票代码列表"""
        return [s.code for s in self.stocks]
    
    def calculate_summary(self):
        """
        计算统计信息
        
        **设计原理**：
        - **多维度统计**：按来源、周期、类型等多个维度统计
        - **实时计算**：每次调用时重新计算，保证数据准确性
        - **结构化输出**：返回结构化字典，便于展示和分析
        
        **为什么这样设计**：
        1. **全面性**：多维度统计提供全面的股票池信息
        2. **准确性**：实时计算保证统计信息与股票池一致
        3. **可扩展性**：可以轻松添加新的统计维度
        
        **使用场景**：
        - 股票池创建后，查看统计信息
        - 股票池更新后，重新计算统计信息
        - 股票池分析时，使用统计信息进行决策
        
        **注意事项**：
        - 统计信息是实时计算的，大量股票时可能耗时
        - 可以添加缓存机制，在股票池未变更时复用统计结果
        
        Returns:
            Dict: 统计信息字典，包含total_count、by_source、by_period、by_type
        """
        # 设计原理：初始化统计结构
        # 原因：结构化输出便于展示和分析
        summary = {
            "total_count": len(self.stocks),
            "by_source": {},  # 按来源统计（如主线、技术、基本面）
            "by_period": {},  # 按周期统计（如短期、中期、长期）
            "by_type": {}     # 按类型统计（如基础池、自定义池）
        }
        
        # 设计原理：遍历股票列表，按维度统计
        # 原因：多维度统计提供全面的股票池信息
        for stock in self.stocks:
            # 按来源统计
            # 设计考虑：了解股票池的来源分布，便于分析
            summary["by_source"][stock.source] = \
                summary["by_source"].get(stock.source, 0) + 1
            
            # 按周期统计
            # 设计考虑：了解股票池的周期分布，便于策略选择
            summary["by_period"][stock.period] = \
                summary["by_period"].get(stock.period, 0) + 1
            
            # 按类型统计
            # 设计考虑：了解股票池的类型分布，便于管理
            summary["by_type"][stock.pool_type] = \
                summary["by_type"].get(stock.pool_type, 0) + 1
        
        # 设计原理：保存统计信息到实例变量
        # 原因：便于后续访问，避免重复计算
        self.summary = summary
        return summary
    
    def to_dict(self) -> Dict:
        """转换为字典（用于JSON序列化）"""
        from dataclasses import asdict
        return {
            "stocks": [s.to_dict() for s in self.stocks],
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "summary": self.summary
        }