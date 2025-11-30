"""
周期筛选器

根据短中长期不同的筛选条件，对股票进行分类

短期（1-20日）：技术信号、资金验证、风险过滤
中期（20-120日）：趋势确认、主线验证、资金持续性、基本面支撑
长期（120-500日）：基本面筛选、行业前景、技术位置、机构认可
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..models import StockPoolItem, StockPool, Period

logger = logging.getLogger(__name__)

try:
    import akshare as ak
    import pandas as pd
    import numpy as np
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False


@dataclass
class PeriodConfig:
    """周期配置"""
    name: str
    hold_days: tuple
    description: str
    
    # 技术指标
    momentum_days: int
    ma_list: List[int]
    
    # 筛选阈值
    min_change_pct: float
    min_volume_ratio: float
    min_turnover: float
    max_turnover: float
    
    # 基本面
    max_pe: float
    min_roe: float
    
    # 输出
    target_count: int


class PeriodSelector:
    """
    周期筛选器
    
    根据投资周期对股票进行筛选和分类
    """
    
    # 周期配置
    PERIOD_CONFIGS = {
        "short": PeriodConfig(
            name="短期",
            hold_days=(1, 20),
            description="短线博弈，快进快出",
            momentum_days=5,
            ma_list=[5, 10, 20],
            min_change_pct=3.0,
            min_volume_ratio=1.5,
            min_turnover=3.0,
            max_turnover=20.0,
            max_pe=100,
            min_roe=0,
            target_count=15
        ),
        "medium": PeriodConfig(
            name="中期",
            hold_days=(20, 120),
            description="趋势跟踪，顺势而为",
            momentum_days=60,
            ma_list=[20, 60],
            min_change_pct=10.0,
            min_volume_ratio=1.0,
            min_turnover=1.0,
            max_turnover=10.0,
            max_pe=50,
            min_roe=10,
            target_count=30
        ),
        "long": PeriodConfig(
            name="长期",
            hold_days=(120, 500),
            description="价值发现，长期持有",
            momentum_days=250,
            ma_list=[60, 120, 250],
            min_change_pct=0,
            min_volume_ratio=0.5,
            min_turnover=0.5,
            max_turnover=5.0,
            max_pe=30,
            min_roe=15,
            target_count=20
        )
    }
    
    def __init__(self):
        pass
    
    def get_period_config(self, period: str) -> PeriodConfig:
        """获取周期配置"""
        return self.PERIOD_CONFIGS.get(period, self.PERIOD_CONFIGS["medium"])
    
    def filter_by_period(
        self, 
        stocks: List[StockPoolItem], 
        period: str
    ) -> List[StockPoolItem]:
        """
        按周期筛选股票
        
        Args:
            stocks: 候选股票列表
            period: 目标周期
            
        Returns:
            符合周期条件的股票
        """
        if not stocks:
            return []
        
        config = self.get_period_config(period)
        result = []
        
        for stock in stocks:
            if self._match_period_criteria(stock, config):
                stock.period = period
                result.append(stock)
        
        # 限制数量
        result = result[:config.target_count]
        
        logger.info(f"{config.name}周期筛选：{len(result)}/{len(stocks)} 只")
        return result
    
    def _match_period_criteria(self, stock: StockPoolItem, config: PeriodConfig) -> bool:
        """检查股票是否符合周期条件"""
        # 涨跌幅
        if stock.change_pct < config.min_change_pct:
            return False
        
        # 其他条件需要额外数据，这里简化处理
        # 实际实现中需要获取更多历史数据
        
        return True
    
    def classify_stocks(self, pool: StockPool) -> Dict[str, List[StockPoolItem]]:
        """
        将股票池按周期分类
        
        Returns:
            {"short": [...], "medium": [...], "long": [...]}
        """
        classified = {
            "short": [],
            "medium": [],
            "long": []
        }
        
        for stock in pool.stocks:
            # 根据评分和信号分类
            if self._is_short_term_candidate(stock):
                classified["short"].append(stock)
            elif self._is_long_term_candidate(stock):
                classified["long"].append(stock)
            else:
                classified["medium"].append(stock)
        
        return classified
    
    def _is_short_term_candidate(self, stock: StockPoolItem) -> bool:
        """判断是否适合短期"""
        # 涨停、放量等短期信号
        short_signals = ["涨停", "大涨", "放量", "突破"]
        for signal in stock.tech_signals:
            if any(s in signal for s in short_signals):
                return True
        
        # 高换手率
        if stock.change_pct >= 7:
            return True
        
        return False
    
    def _is_long_term_candidate(self, stock: StockPoolItem) -> bool:
        """判断是否适合长期"""
        # 高ROE、低估值等长期信号
        long_signals = ["低估值", "高ROE", "基本面优秀"]
        for signal in stock.tech_signals:
            if any(s in signal for s in long_signals):
                return True
        
        # 低波动、主线龙头
        if stock.priority <= 2 and stock.mainline_score >= 80:
            return True
        
        return False
    
    def get_period_report(self, classified: Dict[str, List[StockPoolItem]]) -> str:
        """生成周期分类报告"""
        report = []
        report.append("=" * 50)
        report.append("股票池周期分类报告")
        report.append("=" * 50)
        
        for period, stocks in classified.items():
            config = self.get_period_config(period)
            report.append(f"\n【{config.name}】{config.description}")
            report.append(f"  持有周期：{config.hold_days[0]}-{config.hold_days[1]}天")
            report.append(f"  股票数量：{len(stocks)} 只")
            
            if stocks:
                report.append("  Top 5:")
                for i, stock in enumerate(stocks[:5], 1):
                    report.append(f"    {i}. {stock.name}({stock.code}) - {stock.entry_reason[:30]}")
        
        report.append("\n" + "=" * 50)
        return "\n".join(report)




