"""
A股主线识别 - 数据源管理

数据源分类：
1. 宏观数据源 - 政策、经济周期
2. 行业数据源 - 板块行情、资金流向
3. 个股数据源 - 龙头表现、技术指标
4. 另类数据源 - 舆情、研报、调研

每个数据源都有明确的：
- 来源 (source)
- 更新频率 (frequency)
- 可靠性评级 (reliability)
- 数据字段 (fields)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """数据源类型"""
    MACRO = "macro"           # 宏观数据
    INDUSTRY = "industry"     # 行业数据
    STOCK = "stock"           # 个股数据
    ALTERNATIVE = "alternative"  # 另类数据
    RESEARCH = "research"     # 研报数据


class UpdateFrequency(Enum):
    """更新频率"""
    REALTIME = "realtime"     # 实时
    DAILY = "daily"           # 日频
    WEEKLY = "weekly"         # 周频
    MONTHLY = "monthly"       # 月频
    QUARTERLY = "quarterly"   # 季频


class ReliabilityLevel(Enum):
    """可靠性等级"""
    HIGH = "high"             # 高可靠 - 官方数据
    MEDIUM = "medium"         # 中可靠 - 第三方数据
    LOW = "low"               # 低可靠 - 估算/推测


@dataclass
class DataSource:
    """数据源定义"""
    id: str                          # 数据源ID
    name: str                        # 数据源名称
    type: DataSourceType             # 数据类型
    provider: str                    # 数据提供商
    api_module: str                  # API模块路径
    frequency: UpdateFrequency       # 更新频率
    reliability: ReliabilityLevel    # 可靠性
    fields: List[str]                # 数据字段
    description: str                 # 描述
    url: Optional[str] = None        # 数据源URL
    cost: str = "免费"               # 费用
    last_update: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "provider": self.provider,
            "frequency": self.frequency.value,
            "reliability": self.reliability.value,
            "fields": self.fields,
            "description": self.description,
            "url": self.url,
            "cost": self.cost,
        }


# ============================================================
# 数据源注册表
# ============================================================

DATA_SOURCES: Dict[str, DataSource] = {
    # ========== 宏观数据源 ==========
    "macro_policy": DataSource(
        id="macro_policy",
        name="政策周期数据",
        type=DataSourceType.MACRO,
        provider="东方财富/新华社",
        api_module="akshare.macro.policy",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "policy_name",           # 政策名称
            "publish_date",          # 发布日期
            "policy_type",           # 政策类型：货币/财政/产业
            "policy_direction",      # 政策方向：宽松/中性/收紧
            "affected_industries",   # 影响行业
            "policy_strength",       # 政策力度：1-5
        ],
        description="国务院、央行、发改委等政策发布",
        url="https://data.eastmoney.com/cjsj/",
    ),
    
    "macro_economic": DataSource(
        id="macro_economic",
        name="经济周期指标",
        type=DataSourceType.MACRO,
        provider="国家统计局",
        api_module="akshare.macro.economic",
        frequency=UpdateFrequency.MONTHLY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "gdp_growth",            # GDP增速
            "pmi",                   # 制造业PMI
            "pmi_non_mfg",           # 非制造业PMI
            "cpi",                   # CPI同比
            "ppi",                   # PPI同比
            "m2_growth",             # M2增速
            "social_financing",      # 社融增量
            "fixed_investment",      # 固定资产投资
            "retail_sales",          # 社会消费品零售
            "industrial_production", # 工业增加值
        ],
        description="国家统计局月度/季度经济数据",
        url="https://data.stats.gov.cn/",
    ),
    
    "macro_liquidity": DataSource(
        id="macro_liquidity",
        name="流动性指标",
        type=DataSourceType.MACRO,
        provider="央行/同业拆借中心",
        api_module="akshare.macro.liquidity",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "shibor_on",             # 隔夜SHIBOR
            "shibor_1w",             # 1周SHIBOR
            "shibor_1m",             # 1月SHIBOR
            "dr007",                 # DR007
            "lpr_1y",                # 1年期LPR
            "lpr_5y",                # 5年期LPR
            "reverse_repo_rate",     # 逆回购利率
            "mlf_rate",              # MLF利率
            "omo_net",               # 公开市场操作净投放
        ],
        description="银行间市场流动性数据",
        url="https://www.chinamoney.com.cn/",
    ),
    
    # ========== 行业数据源 ==========
    "industry_flow": DataSource(
        id="industry_flow",
        name="板块资金流向",
        type=DataSourceType.INDUSTRY,
        provider="东方财富",
        api_module="akshare.stock.sector_fund_flow",
        frequency=UpdateFrequency.REALTIME,
        reliability=ReliabilityLevel.MEDIUM,
        fields=[
            "sector_name",           # 板块名称
            "main_net_inflow",       # 主力净流入
            "main_net_ratio",        # 主力净占比
            "super_large_inflow",    # 超大单净流入
            "large_inflow",          # 大单净流入
            "medium_inflow",         # 中单净流入
            "small_inflow",          # 小单净流入
            "close_price",           # 收盘价
            "change_pct",            # 涨跌幅
        ],
        description="东方财富板块资金流向数据",
        url="https://data.eastmoney.com/bkzj/hy.html",
    ),
    
    "industry_performance": DataSource(
        id="industry_performance",
        name="行业涨跌统计",
        type=DataSourceType.INDUSTRY,
        provider="同花顺/东方财富",
        api_module="akshare.stock.sector_performance",
        frequency=UpdateFrequency.REALTIME,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "sector_name",           # 板块名称
            "change_pct",            # 涨跌幅
            "turnover_rate",         # 换手率
            "volume_ratio",          # 量比
            "up_count",              # 上涨家数
            "down_count",            # 下跌家数
            "limit_up_count",        # 涨停家数
            "limit_down_count",      # 跌停家数
            "amplitude",             # 振幅
            "total_market_value",    # 总市值
        ],
        description="行业板块实时行情统计",
        url="https://q.10jqka.com.cn/thshy/",
    ),
    
    "industry_northbound": DataSource(
        id="industry_northbound",
        name="北向资金行业分布",
        type=DataSourceType.INDUSTRY,
        provider="东方财富/沪深港通",
        api_module="akshare.stock.hk_hold_industry",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "industry",              # 行业
            "hold_market_value",     # 持股市值
            "hold_ratio",            # 持股比例
            "hold_change",           # 持股变动
            "net_buy",               # 净买入
            "hold_stock_count",      # 持股数量
        ],
        description="北向资金行业持仓分布",
        url="https://data.eastmoney.com/hsgtcg/hy.html",
    ),
    
    "industry_margin": DataSource(
        id="industry_margin",
        name="两融行业数据",
        type=DataSourceType.INDUSTRY,
        provider="交易所/东方财富",
        api_module="akshare.stock.margin_industry",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "industry",              # 行业
            "margin_balance",        # 融资余额
            "margin_buy",            # 融资买入
            "margin_repay",          # 融资偿还
            "short_balance",         # 融券余额
            "short_sell",            # 融券卖出
        ],
        description="行业两融数据",
        url="https://data.eastmoney.com/rzrq/",
    ),
    
    # ========== 个股数据源 ==========
    "stock_realtime": DataSource(
        id="stock_realtime",
        name="个股实时行情",
        type=DataSourceType.STOCK,
        provider="新浪财经/东方财富",
        api_module="akshare.stock.realtime",
        frequency=UpdateFrequency.REALTIME,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "code", "name", "open", "high", "low", "close",
            "volume", "amount", "change_pct", "turnover_rate",
            "pe_ttm", "pb", "market_value", "circulating_value",
        ],
        description="A股实时行情数据",
    ),
    
    "stock_technical": DataSource(
        id="stock_technical",
        name="技术指标数据",
        type=DataSourceType.STOCK,
        provider="计算生成",
        api_module="core.indicators",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "ma5", "ma10", "ma20", "ma60", "ma120", "ma250",
            "macd", "macd_signal", "macd_hist",
            "rsi_6", "rsi_12", "rsi_24",
            "kdj_k", "kdj_d", "kdj_j",
            "boll_upper", "boll_mid", "boll_lower",
            "atr", "obv", "cci",
        ],
        description="基于行情计算的技术指标",
    ),
    
    "stock_fundamental": DataSource(
        id="stock_fundamental",
        name="基本面数据",
        type=DataSourceType.STOCK,
        provider="JQData/AKShare",
        api_module="akshare.stock.fundamental",
        frequency=UpdateFrequency.QUARTERLY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "roe", "roa", "gross_margin", "net_margin",
            "revenue_growth", "profit_growth",
            "debt_ratio", "current_ratio",
            "eps", "bps", "operating_cash_flow",
        ],
        description="上市公司财务数据",
    ),
    
    # ========== 另类数据源 ==========
    "alt_sentiment": DataSource(
        id="alt_sentiment",
        name="市场情绪指标",
        type=DataSourceType.ALTERNATIVE,
        provider="东方财富/同花顺",
        api_module="akshare.stock.sentiment",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.MEDIUM,
        fields=[
            "limit_up_count",        # 涨停数
            "limit_down_count",      # 跌停数
            "broken_board_count",    # 炸板数
            "continuous_limit_up",   # 连板股数
            "up_down_ratio",         # 涨跌比
            "new_high_count",        # 创新高数
            "new_low_count",         # 创新低数
            "volume_ratio_market",   # 市场量比
        ],
        description="市场情绪量化指标",
    ),
    
    "alt_dragon_tiger": DataSource(
        id="alt_dragon_tiger",
        name="龙虎榜数据",
        type=DataSourceType.ALTERNATIVE,
        provider="交易所/东方财富",
        api_module="akshare.stock.dragon_tiger",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.HIGH,
        fields=[
            "code", "name", "reason",
            "buy_amount", "sell_amount", "net_amount",
            "buy_seats", "sell_seats",
            "institution_buy", "institution_sell",
        ],
        description="龙虎榜席位买卖数据",
    ),
    
    # ========== 研报数据源 ==========
    "research_broker": DataSource(
        id="research_broker",
        name="券商研报",
        type=DataSourceType.RESEARCH,
        provider="东方财富/萝卜投研",
        api_module="akshare.stock.research",
        frequency=UpdateFrequency.DAILY,
        reliability=ReliabilityLevel.MEDIUM,
        fields=[
            "title", "author", "institution",
            "rating", "target_price", "publish_date",
            "industry", "stock_code", "summary",
        ],
        description="券商研究报告",
        url="https://data.eastmoney.com/report/",
    ),
    
    "research_consensus": DataSource(
        id="research_consensus",
        name="一致预期数据",
        type=DataSourceType.RESEARCH,
        provider="东方财富/Wind",
        api_module="akshare.stock.consensus",
        frequency=UpdateFrequency.WEEKLY,
        reliability=ReliabilityLevel.MEDIUM,
        fields=[
            "eps_forecast", "revenue_forecast",
            "profit_forecast", "target_price_avg",
            "rating_buy", "rating_hold", "rating_sell",
            "analyst_count", "report_count",
        ],
        description="分析师一致预期",
    ),
}


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources = DATA_SOURCES
        self._cache = {}
        self._last_fetch = {}
    
    def get_source(self, source_id: str) -> Optional[DataSource]:
        """获取数据源定义"""
        return self.sources.get(source_id)
    
    def list_sources(self, type_filter: Optional[DataSourceType] = None) -> List[DataSource]:
        """列出数据源"""
        sources = list(self.sources.values())
        if type_filter:
            sources = [s for s in sources if s.type == type_filter]
        return sources
    
    def get_source_summary(self) -> Dict[str, Any]:
        """获取数据源汇总"""
        summary = {
            "total": len(self.sources),
            "by_type": {},
            "by_reliability": {},
            "by_frequency": {},
        }
        
        for source in self.sources.values():
            # 按类型统计
            type_name = source.type.value
            if type_name not in summary["by_type"]:
                summary["by_type"][type_name] = []
            summary["by_type"][type_name].append(source.name)
            
            # 按可靠性统计
            rel = source.reliability.value
            summary["by_reliability"][rel] = summary["by_reliability"].get(rel, 0) + 1
            
            # 按频率统计
            freq = source.frequency.value
            summary["by_frequency"][freq] = summary["by_frequency"].get(freq, 0) + 1
        
        return summary
    
    def fetch_data(self, source_id: str, **kwargs) -> Dict[str, Any]:
        """
        获取数据源数据
        
        Returns:
            {
                "source": DataSource,
                "data": actual_data,
                "fetch_time": datetime,
                "status": "success" | "error",
                "error": Optional[str]
            }
        """
        source = self.get_source(source_id)
        if not source:
            return {"status": "error", "error": f"未知数据源: {source_id}"}
        
        result = {
            "source": source.to_dict(),
            "fetch_time": datetime.now().isoformat(),
            "status": "success",
        }
        
        try:
            # 这里调用实际的数据获取逻辑
            # 目前返回模拟数据
            result["data"] = self._fetch_mock_data(source_id, **kwargs)
            self._last_fetch[source_id] = datetime.now()
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"获取数据源 {source_id} 失败: {e}")
        
        return result
    
    def _fetch_mock_data(self, source_id: str, **kwargs) -> Any:
        """获取模拟数据（实际实现时替换为真实API调用）"""
        mock_data = {
            "macro_policy": {
                "latest_policies": [
                    {"name": "央行降准0.25个百分点", "date": "2024-01-24", "direction": "宽松", "strength": 4},
                    {"name": "国务院支持民营经济发展", "date": "2024-01-20", "direction": "积极", "strength": 3},
                ],
                "policy_cycle": "宽松",
            },
            "macro_economic": {
                "gdp_growth": 5.2,
                "pmi": 50.8,
                "cpi": 0.2,
                "ppi": -2.7,
                "m2_growth": 9.7,
                "economic_cycle": "复苏",
            },
            "industry_flow": {
                "top_inflow": [
                    {"sector": "半导体", "net_inflow": 45.6, "change_pct": 3.2},
                    {"sector": "人工智能", "net_inflow": 38.2, "change_pct": 2.8},
                    {"sector": "新能源", "net_inflow": 25.1, "change_pct": 1.5},
                ],
            },
        }
        return mock_data.get(source_id, {})


# 全局实例
data_source_manager = DataSourceManager()

