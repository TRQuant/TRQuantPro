"""
热度评分引擎

基于《市场主线识别模块之热度评分设计方案.pdf》设计

7个热度因子：
1. 新闻数量 (20%) - 媒体曝光度
2. 关键词提及次数 (10%) - 市场舆论热度
3. 搜索指数 (10%) - 大众关注度
4. 研报覆盖度 (15%) - 机构关注度
5. 社交媒体传播度 (15%) - 散户情绪热度
6. 龙虎榜次数 (15%) - 游资动向
7. 涨停股数量 (15%) - 板块爆炒程度

标准化方法：
- Min-Max归一化
- 对数缩放
- Z-Score标准化
- 指数时间衰减
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

logger = logging.getLogger(__name__)


class PeriodType(Enum):
    """时间周期类型"""
    SHORT = "short"      # 短期: 3-7日
    MEDIUM = "medium"    # 中期: 15-30日
    LONG = "long"        # 长期: 60-180日


@dataclass
class HeatFactor:
    """热度因子"""
    name: str                    # 因子名称
    weight: float                # 权重
    raw_value: float = 0.0       # 原始值
    normalized_value: float = 0.0  # 标准化后的值 (0-100)
    time_window: int = 7         # 时间窗口（天）
    decay_half_life: int = 3     # 半衰期（天）
    data_source: str = ""        # 数据来源
    
    @property
    def weighted_score(self) -> float:
        """加权得分"""
        return self.normalized_value * self.weight


@dataclass
class HeatmapScore:
    """热度评分结果"""
    
    # 主线标识
    mainline_name: str = ""
    mainline_type: str = ""  # industry/concept
    
    # 7个因子得分 (0-100)
    news_score: float = 0.0          # 新闻数量 (20%)
    keyword_score: float = 0.0       # 关键词提及 (10%)
    search_score: float = 0.0        # 搜索指数 (10%)
    report_score: float = 0.0        # 研报覆盖度 (15%)
    social_score: float = 0.0        # 社交媒体传播度 (15%)
    lhb_score: float = 0.0           # 龙虎榜次数 (15%)
    limit_up_score: float = 0.0      # 涨停股数量 (15%)
    
    # 综合得分
    total_score: float = 0.0
    
    # 时间维度
    period_type: str = "short"
    
    # 趋势信息
    score_change: float = 0.0        # 相比上期变化
    trend: str = "unknown"           # rising/stable/falling/unknown
    
    # 排名
    rank: int = 0
    
    # 因子详情
    factors: List[HeatFactor] = field(default_factory=list)
    
    def calculate_total(self) -> float:
        """计算总分（加权求和）"""
        self.total_score = (
            self.news_score * 0.20 +
            self.keyword_score * 0.10 +
            self.search_score * 0.10 +
            self.report_score * 0.15 +
            self.social_score * 0.15 +
            self.lhb_score * 0.15 +
            self.limit_up_score * 0.15
        )
        return self.total_score
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "mainline_name": self.mainline_name,
            "mainline_type": self.mainline_type,
            "news_score": round(self.news_score, 1),
            "keyword_score": round(self.keyword_score, 1),
            "search_score": round(self.search_score, 1),
            "report_score": round(self.report_score, 1),
            "social_score": round(self.social_score, 1),
            "lhb_score": round(self.lhb_score, 1),
            "limit_up_score": round(self.limit_up_score, 1),
            "total_score": round(self.total_score, 1),
            "period_type": self.period_type,
            "score_change": round(self.score_change, 1),
            "trend": self.trend,
            "rank": self.rank,
        }
    
    def get_factor_breakdown(self) -> List[Dict]:
        """获取因子分解"""
        return [
            {"name": "新闻数量", "score": self.news_score, "weight": 20, "desc": "媒体曝光度"},
            {"name": "关键词提及", "score": self.keyword_score, "weight": 10, "desc": "市场舆论热度"},
            {"name": "搜索指数", "score": self.search_score, "weight": 10, "desc": "大众关注度"},
            {"name": "研报覆盖度", "score": self.report_score, "weight": 15, "desc": "机构关注度"},
            {"name": "社交传播度", "score": self.social_score, "weight": 15, "desc": "散户情绪热度"},
            {"name": "龙虎榜次数", "score": self.lhb_score, "weight": 15, "desc": "游资动向"},
            {"name": "涨停股数量", "score": self.limit_up_score, "weight": 15, "desc": "板块爆炒程度"},
        ]


class HeatmapEngine:
    """
    热度评分引擎
    
    计算流程：
    1. 获取各因子原始数据
    2. 应用时间衰减
    3. 标准化处理
    4. 加权合成总分
    """
    
    # 因子权重配置
    FACTOR_WEIGHTS = {
        "news": 0.20,        # 新闻数量
        "keyword": 0.10,     # 关键词提及
        "search": 0.10,      # 搜索指数
        "report": 0.15,      # 研报覆盖度
        "social": 0.15,      # 社交媒体
        "lhb": 0.15,         # 龙虎榜
        "limit_up": 0.15,    # 涨停股
    }
    
    # 时间窗口配置（天数）
    TIME_WINDOWS = {
        "short": {"news": 7, "social": 5, "lhb": 5, "limit_up": 5, "report": 15},
        "medium": {"news": 30, "social": 15, "lhb": 15, "limit_up": 15, "report": 30},
        "long": {"news": 90, "social": 30, "lhb": 30, "limit_up": 30, "report": 90},
    }
    
    # 衰减半衰期（天数）
    DECAY_HALF_LIFE = {
        "news": 3,
        "keyword": 5,
        "search": 7,
        "report": 15,
        "social": 2,
        "lhb": 2,
        "limit_up": 2,
    }
    
    def __init__(self):
        """初始化引擎"""
        self.all_mainlines_data: Dict[str, Dict] = {}  # 用于归一化的全局数据
    
    def calculate_heatmap_scores(
        self,
        mainlines_data: List[Dict],
        period_type: str = "short"
    ) -> List[HeatmapScore]:
        """
        批量计算多个主线的热度评分
        
        Args:
            mainlines_data: 主线数据列表，每个元素包含主线名称和各因子数据
            period_type: 时间周期 (short/medium/long)
        
        Returns:
            热度评分结果列表（已排序）
        """
        if not mainlines_data:
            return []
        
        # 第一遍：收集所有原始数据，用于归一化
        all_news = []
        all_keywords = []
        all_lhb = []
        all_limit_up = []
        all_social = []
        all_report = []
        
        for data in mainlines_data:
            all_news.append(data.get("news_count", 0))
            all_keywords.append(data.get("keyword_mentions", 0))
            all_lhb.append(data.get("lhb_count", 0))
            all_limit_up.append(data.get("limit_up_count", 0))
            all_social.append(data.get("social_mentions", 0))
            all_report.append(data.get("report_count", 0))
        
        # 计算归一化参数
        norm_params = {
            "news": self._get_norm_params(all_news),
            "keyword": self._get_norm_params(all_keywords, use_log=True),
            "lhb": self._get_norm_params(all_lhb),
            "limit_up": self._get_norm_params(all_limit_up),
            "social": self._get_norm_params(all_social),
            "report": self._get_norm_params(all_report),
        }
        
        # 第二遍：计算每个主线的评分
        scores = []
        for data in mainlines_data:
            score = self._calculate_single_score(data, norm_params, period_type)
            scores.append(score)
        
        # 排序（按总分降序）
        scores.sort(key=lambda x: x.total_score, reverse=True)
        
        # 设置排名
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        return scores
    
    def _calculate_single_score(
        self,
        data: Dict,
        norm_params: Dict,
        period_type: str
    ) -> HeatmapScore:
        """计算单个主线的热度评分"""
        
        score = HeatmapScore(
            mainline_name=data.get("name", ""),
            mainline_type=data.get("type", ""),
            period_type=period_type,
        )
        
        # 1. 新闻数量 (20%)
        news_raw = data.get("news_count", 0)
        news_data = data.get("news_data", [])
        if news_data:
            news_raw = self._apply_time_decay(news_data, self.DECAY_HALF_LIFE["news"])
        score.news_score = self._normalize_value(news_raw, norm_params["news"])
        
        # 2. 关键词提及 (10%) - 对数缩放
        keyword_raw = data.get("keyword_mentions", 0)
        if keyword_raw > 0:
            keyword_raw = math.log(keyword_raw + 1)
        score.keyword_score = self._normalize_value(keyword_raw, norm_params["keyword"])
        
        # 3. 搜索指数 (10%) - 直接使用相对值
        search_raw = data.get("search_index", 0)
        score.search_score = min(search_raw, 100)  # 假设搜索指数已是0-100
        
        # 4. 研报覆盖度 (15%) - Z-Score
        report_raw = data.get("report_count", 0)
        report_history = data.get("report_history", [])
        if report_history:
            score.report_score = self._calculate_zscore(report_raw, report_history)
        else:
            score.report_score = self._normalize_value(report_raw, norm_params["report"])
        
        # 5. 社交媒体传播度 (15%)
        social_raw = data.get("social_mentions", 0)
        social_data = data.get("social_data", [])
        if social_data:
            social_raw = self._apply_time_decay(social_data, self.DECAY_HALF_LIFE["social"])
        score.social_score = self._normalize_value(social_raw, norm_params["social"])
        
        # 6. 龙虎榜次数 (15%)
        lhb_raw = data.get("lhb_count", 0)
        lhb_data = data.get("lhb_data", [])
        if lhb_data:
            lhb_raw = self._apply_time_decay(lhb_data, self.DECAY_HALF_LIFE["lhb"])
        score.lhb_score = self._normalize_value(lhb_raw, norm_params["lhb"])
        
        # 7. 涨停股数量 (15%)
        limit_up_raw = data.get("limit_up_count", 0)
        limit_up_data = data.get("limit_up_data", [])
        if limit_up_data:
            limit_up_raw = self._apply_time_decay(limit_up_data, self.DECAY_HALF_LIFE["limit_up"])
        score.limit_up_score = self._normalize_value(limit_up_raw, norm_params["limit_up"])
        
        # 计算总分
        score.calculate_total()
        
        # 计算趋势
        prev_score = data.get("prev_total_score", 0)
        if prev_score > 0:
            score.score_change = score.total_score - prev_score
            if score.score_change > 5:
                score.trend = "rising"
            elif score.score_change < -5:
                score.trend = "falling"
            else:
                score.trend = "stable"
        else:
            # 没有历史数据，标记为未知
            score.trend = "unknown"
            score.score_change = 0.0
        
        return score
    
    def _get_norm_params(
        self,
        values: List[float],
        use_log: bool = False
    ) -> Dict:
        """获取归一化参数"""
        if not values:
            return {"min": 0, "max": 1, "mean": 0, "std": 1}
        
        if use_log:
            values = [math.log(v + 1) if v > 0 else 0 for v in values]
        
        import statistics
        min_val = min(values)
        max_val = max(values)
        mean_val = statistics.mean(values) if values else 0
        std_val = statistics.stdev(values) if len(values) > 1 else 1
        
        return {
            "min": min_val,
            "max": max_val,
            "mean": mean_val,
            "std": std_val if std_val > 0 else 1,
        }
    
    def _normalize_value(
        self,
        value: float,
        params: Dict,
        target_min: float = 0,
        target_max: float = 100
    ) -> float:
        """
        Min-Max归一化
        
        修复：处理所有值相同的情况
        - 如果所有值都是0，返回0
        - 如果所有值都相同且>0，返回中间值（50）
        - 如果只有一个非零值，返回100
        """
        min_val = params["min"]
        max_val = params["max"]
        
        # 处理边界情况：所有值相同
        if max_val == min_val:
            if value == 0:
                # 所有值都是0，返回0
                return target_min
            elif max_val == 0:
                # 所有值都是0
                return target_min
            else:
                # 所有值都相同且>0，返回中间值
                # 这样可以区分"有数据但相同"和"无数据"
                return (target_min + target_max) / 2
        
        # 正常归一化
        normalized = (value - min_val) / (max_val - min_val)
        scaled = normalized * (target_max - target_min) + target_min
        
        return max(target_min, min(target_max, scaled))
    
    def _calculate_zscore(
        self,
        current_value: float,
        history: List[float]
    ) -> float:
        """
        Z-Score标准化（转换为0-100分）
        
        Z-Score = (当前值 - 历史均值) / 历史标准差
        然后映射到0-100范围
        """
        if not history:
            return 50.0  # 无历史数据，返回中间值
        
        import statistics
        mean_val = statistics.mean(history)
        std_val = statistics.stdev(history) if len(history) > 1 else 1
        
        if std_val == 0:
            return 50.0
        
        zscore = (current_value - mean_val) / std_val
        
        # 将Z-Score映射到0-100（假设正态分布，-3到+3映射到0-100）
        normalized = (zscore + 3) / 6 * 100
        return max(0, min(100, normalized))
    
    def _apply_time_decay(
        self,
        data: List[Dict],
        half_life: int = 3
    ) -> float:
        """
        应用指数时间衰减
        
        衰减公式: w(t) = e^(-λ * Δt)
        其中 λ = ln(2) / half_life
        
        Args:
            data: 数据列表，每个元素包含 'value'/'count' 和 'date'/'time'
            half_life: 半衰期（天数）
        
        Returns:
            衰减加权后的总和
        """
        if not data:
            return 0.0
        
        now = datetime.now()
        lambda_param = math.log(2) / half_life
        decayed_sum = 0.0
        
        for item in data:
            try:
                # 获取值
                if isinstance(item, dict):
                    value = float(item.get("value", item.get("count", 1)))
                    date_str = item.get("date", item.get("time", ""))
                else:
                    value = float(item)
                    date_str = ""
                
                # 解析日期
                if date_str:
                    try:
                        if isinstance(date_str, datetime):
                            item_date = date_str
                        elif isinstance(date_str, str):
                            # 尝试多种格式
                            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d"]:
                                try:
                                    item_date = datetime.strptime(date_str, fmt)
                                    break
                                except:
                                    continue
                            else:
                                item_date = now
                        else:
                            item_date = now
                    except:
                        item_date = now
                else:
                    item_date = now
                
                # 计算时间差（天数）
                delta_days = (now - item_date).total_seconds() / 86400
                delta_days = max(0, delta_days)  # 确保非负
                
                # 指数衰减权重
                weight = math.exp(-lambda_param * delta_days)
                decayed_sum += value * weight
                
            except Exception as e:
                logger.debug(f"时间衰减计算异常: {e}")
                continue
        
        return decayed_sum
    
    def get_config(self) -> Dict:
        """获取引擎配置"""
        return {
            "factor_weights": self.FACTOR_WEIGHTS,
            "time_windows": self.TIME_WINDOWS,
            "decay_half_life": self.DECAY_HALF_LIFE,
        }


class HeatmapDataAggregator:
    """
    热度数据聚合器
    
    从多个数据源聚合热度因子数据
    """
    
    def __init__(self):
        pass
    
    def aggregate_from_market_data(
        self,
        sector_data: List[Dict],
        concept_data: List[Dict],
        lhb_data: List[Dict],
        limit_up_data: Dict,
    ) -> List[Dict]:
        """
        从市场数据聚合热度因子
        
        目前可用的数据：
        - 板块资金流向 (sector_data)
        - 概念板块行情 (concept_data)
        - 龙虎榜数据 (lhb_data)
        - 涨停统计 (limit_up_data)
        
        暂时缺少的数据（使用估算）：
        - 新闻数量
        - 关键词提及
        - 搜索指数
        - 研报覆盖度
        - 社交媒体传播度
        """
        mainlines_data = []
        
        # 处理行业板块
        for sector in sector_data:
            name = sector.get("sector_name", "")
            if not name:
                continue
            
            # 从现有数据估算热度因子
            change_pct = abs(sector.get("change_pct", 0))
            net_inflow = abs(sector.get("main_net_inflow", 0))
            
            # 查找该板块的龙虎榜次数
            lhb_count = self._count_lhb_for_sector(name, lhb_data)
            
            # 查找该板块的涨停数
            limit_up_count = self._count_limit_up_for_sector(name, limit_up_data)
            
            mainlines_data.append({
                "name": name,
                "type": "industry",
                # 已有数据
                "lhb_count": lhb_count,
                "limit_up_count": limit_up_count,
                # 估算数据（基于涨跌幅和资金流向）
                "news_count": self._estimate_news_count(change_pct, net_inflow),
                "keyword_mentions": self._estimate_keyword_mentions(change_pct),
                "search_index": self._estimate_search_index(change_pct, net_inflow),
                "report_count": self._estimate_report_count(net_inflow),
                "social_mentions": self._estimate_social_mentions(change_pct, lhb_count),
                # 原始市场数据
                "change_pct": sector.get("change_pct", 0),
                "net_inflow": sector.get("main_net_inflow", 0),
            })
        
        # 处理概念板块
        for concept in concept_data:
            name = concept.get("board_name", "")
            if not name:
                continue
            
            change_pct = abs(concept.get("change_pct", 0))
            net_inflow = abs(concept.get("net_inflow", 0))
            
            lhb_count = self._count_lhb_for_sector(name, lhb_data)
            limit_up_count = self._count_limit_up_for_sector(name, limit_up_data)
            
            mainlines_data.append({
                "name": name,
                "type": "concept",
                "lhb_count": lhb_count,
                "limit_up_count": limit_up_count,
                "news_count": self._estimate_news_count(change_pct, net_inflow),
                "keyword_mentions": self._estimate_keyword_mentions(change_pct),
                "search_index": self._estimate_search_index(change_pct, net_inflow),
                "report_count": self._estimate_report_count(net_inflow),
                "social_mentions": self._estimate_social_mentions(change_pct, lhb_count),
                "change_pct": concept.get("change_pct", 0),
                "net_inflow": concept.get("net_inflow", 0),
            })
        
        return mainlines_data
    
    def _count_lhb_for_sector(self, sector_name: str, lhb_data: List[Dict]) -> int:
        """统计板块的龙虎榜次数"""
        count = 0
        for item in lhb_data:
            # 检查股票是否属于该板块（简化逻辑）
            stock_name = item.get("股票名称", "")
            if sector_name in stock_name or stock_name in sector_name:
                count += 1
        return count
    
    def _count_limit_up_for_sector(self, sector_name: str, limit_up_data: Dict) -> int:
        """统计板块的涨停股数量"""
        # 从涨停数据中查找
        limit_up_list = limit_up_data.get("limit_up_stocks", [])
        count = 0
        for stock in limit_up_list:
            if sector_name in stock.get("所属行业", "") or sector_name in stock.get("所属概念", ""):
                count += 1
        return count
    
    def _estimate_news_count(self, change_pct: float, net_inflow: float) -> float:
        """估算新闻数量（基于涨跌幅和资金流向）"""
        # 涨跌幅越大、资金流入越多，新闻可能越多
        base = 5
        change_factor = abs(change_pct) * 2
        inflow_factor = abs(net_inflow) / 10
        return base + change_factor + inflow_factor
    
    def _estimate_keyword_mentions(self, change_pct: float) -> float:
        """估算关键词提及次数"""
        base = 10
        return base + abs(change_pct) * 5
    
    def _estimate_search_index(self, change_pct: float, net_inflow: float) -> float:
        """估算搜索指数（0-100）"""
        base = 30
        change_factor = abs(change_pct) * 5
        inflow_factor = abs(net_inflow) / 5
        return min(100, base + change_factor + inflow_factor)
    
    def _estimate_report_count(self, net_inflow: float) -> float:
        """估算研报数量"""
        base = 2
        return base + abs(net_inflow) / 20
    
    def _estimate_social_mentions(self, change_pct: float, lhb_count: int) -> float:
        """估算社交媒体提及"""
        base = 20
        change_factor = abs(change_pct) * 10
        lhb_factor = lhb_count * 15
        return base + change_factor + lhb_factor


class MultiPeriodMainlineClassifier:
    """
    短中长期主线分类器
    
    根据PDF设计方案：
    - 短期主线 (3-5日): 注重瞬时热点，高频热度因子权重更高
    - 中期主线 (15-30日): 平衡热度持续性，参考基本面和政策支撑
    - 长期主线 (60-180日): 产业趋势，热度指标作用相对降低
    """
    
    # 不同周期的因子权重调整
    PERIOD_WEIGHTS = {
        "short": {
            "news": 0.15,
            "keyword": 0.05,
            "search": 0.10,
            "report": 0.10,
            "social": 0.20,
            "lhb": 0.20,
            "limit_up": 0.20,
        },
        "medium": {
            "news": 0.20,
            "keyword": 0.10,
            "search": 0.10,
            "report": 0.20,
            "social": 0.15,
            "lhb": 0.15,
            "limit_up": 0.10,
        },
        "long": {
            "news": 0.25,
            "keyword": 0.15,
            "search": 0.10,
            "report": 0.25,
            "social": 0.10,
            "lhb": 0.10,
            "limit_up": 0.05,
        },
    }
    
    # 主线类型阈值
    THRESHOLDS = {
        "short": {"min_score": 60, "max_duration": 14},
        "medium": {"min_score": 65, "max_duration": 90},
        "long": {"min_score": 70, "max_duration": 365},
    }
    
    def __init__(self):
        self.engine = HeatmapEngine()
    
    def classify_mainlines(
        self,
        mainlines_data: List[Dict]
    ) -> Dict[str, List[HeatmapScore]]:
        """
        将主线分类为短中长期
        
        Args:
            mainlines_data: 主线数据列表
        
        Returns:
            {
                "short": [...],  # 短期主线
                "medium": [...], # 中期主线
                "long": [...]    # 长期主线
            }
        """
        result = {
            "short": [],
            "medium": [],
            "long": [],
        }
        
        # 分别计算三个周期的评分
        for period in ["short", "medium", "long"]:
            scores = self.engine.calculate_heatmap_scores(
                mainlines_data, 
                period_type=period
            )
            
            # 筛选符合阈值的主线
            threshold = self.THRESHOLDS[period]["min_score"]
            qualified = [s for s in scores if s.total_score >= threshold]
            
            result[period] = qualified[:10]  # 每个周期取Top 10
        
        return result
    
    def get_comprehensive_ranking(
        self,
        mainlines_data: List[Dict]
    ) -> List[Dict]:
        """
        获取综合排名（考虑多周期）
        
        Returns:
            综合排名列表，包含各周期得分
        """
        # 计算三个周期的评分
        short_scores = self.engine.calculate_heatmap_scores(mainlines_data, "short")
        medium_scores = self.engine.calculate_heatmap_scores(mainlines_data, "medium")
        long_scores = self.engine.calculate_heatmap_scores(mainlines_data, "long")
        
        # 创建映射
        short_map = {s.mainline_name: s.total_score for s in short_scores}
        medium_map = {s.mainline_name: s.total_score for s in medium_scores}
        long_map = {s.mainline_name: s.total_score for s in long_scores}
        
        # 综合评分
        comprehensive = []
        for score in short_scores:
            name = score.mainline_name
            
            short_s = short_map.get(name, 0)
            medium_s = medium_map.get(name, 0)
            long_s = long_map.get(name, 0)
            
            # 综合得分 = 短期40% + 中期35% + 长期25%
            comp_score = short_s * 0.4 + medium_s * 0.35 + long_s * 0.25
            
            # 判断最适合的周期类型
            if short_s >= 70 and short_s > medium_s and short_s > long_s:
                best_period = "short"
            elif long_s >= 70 and long_s > short_s:
                best_period = "long"
            elif medium_s >= 60:
                best_period = "medium"
            else:
                best_period = "short"
            
            comprehensive.append({
                "name": name,
                "type": score.mainline_type,
                "short_score": round(short_s, 1),
                "medium_score": round(medium_s, 1),
                "long_score": round(long_s, 1),
                "comprehensive_score": round(comp_score, 1),
                "best_period": best_period,
                "trend": score.trend,
            })
        
        # 按综合得分排序
        comprehensive.sort(key=lambda x: x["comprehensive_score"], reverse=True)
        
        # 添加排名
        for i, item in enumerate(comprehensive):
            item["rank"] = i + 1
        
        return comprehensive
    
    def get_period_description(self, period: str) -> Dict:
        """获取周期说明"""
        descriptions = {
            "short": {
                "name": "短期主线",
                "duration": "3-5日",
                "characteristics": [
                    "事件驱动",
                    "主题炒作",
                    "情绪推动",
                ],
                "focus_factors": ["社交媒体", "龙虎榜", "涨停数"],
                "strategy": "短线交易，快进快出",
            },
            "medium": {
                "name": "中期主线",
                "duration": "15-30日",
                "characteristics": [
                    "政策催化",
                    "基本面改善",
                    "资金持续流入",
                ],
                "focus_factors": ["新闻覆盖", "研报数量", "社交热度"],
                "strategy": "波段操作，趋势跟随",
            },
            "long": {
                "name": "长期主线",
                "duration": "60-180日",
                "characteristics": [
                    "产业趋势",
                    "经济结构",
                    "长期政策支持",
                ],
                "focus_factors": ["研报覆盖", "新闻持续性", "关键词提及"],
                "strategy": "价值投资，长期持有",
            },
        }
        return descriptions.get(period, {})


# 导出
__all__ = [
    "HeatmapEngine",
    "HeatmapScore",
    "HeatFactor",
    "HeatmapDataAggregator",
    "PeriodType",
    "MultiPeriodMainlineClassifier",
]
