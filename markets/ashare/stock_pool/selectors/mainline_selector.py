"""
主线强势股筛选器

【核心衔接点】与主线识别模块对接：
- 读取主线识别的五维评分结果
- 读取热度评分结果
- 从高评分主线板块中提取强势股

筛选逻辑：
1. 读取主线识别结果（latest_heatmap_scores.json）
2. 筛选高评分主线（总分>=60）
3. 获取主线板块成分股（JQData/AKShare/关键词搜索）
4. 在成分股中按技术/资金条件筛选
5. 输出主线强势股池
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

from ..models import StockPoolItem, StockPool, PoolSource, Period, PoolType, load_mainline_scores

logger = logging.getLogger(__name__)

# 使用AKShare包装器（带重试和缓存）
try:
    from markets.ashare.utils.akshare_wrapper import get_akshare_wrapper
    ak_wrapper = get_akshare_wrapper()
    AKSHARE_AVAILABLE = ak_wrapper.available if ak_wrapper else False
except ImportError:
    AKSHARE_AVAILABLE = False
    ak_wrapper = None
    logger.warning("AKShare未安装，部分功能受限")

# JQData提供者
try:
    from ..data_layer import get_jqdata_provider
    jqdata_provider = get_jqdata_provider()
except:
    jqdata_provider = None

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class MainlineSelector:
    """
    主线强势股筛选器
    
    从主线识别模块的输出中提取强势股候选
    """
    
    # 筛选阈值配置
    DEFAULT_CONFIG = {
        "min_mainline_score": 60,       # 最低主线评分
        "min_heat_score": 50,           # 最低热度评分
        "top_mainline_count": 10,       # 取前N个主线
        "max_stocks_per_mainline": 10,  # 每个主线最多取N只股票
        "min_change_pct_5d": 0,         # 5日最低涨幅
        "require_above_ma20": True,     # 要求在20日均线上方
        "exclude_st": True,             # 排除ST
        "min_market_cap": 20,           # 最低市值（亿）
        "max_market_cap": 5000,         # 最高市值（亿）
    }
    
    # 全市场行情缓存
    _market_data_cache = None
    _market_data_time = None
    
    def __init__(self, config: Dict = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.mainline_data = None
        self.last_update = None
    
    def load_mainline_data(self, filepath: Path = None) -> Dict:
        """
        加载主线识别模块的输出
        
        这是与前置模块的核心衔接点
        """
        self.mainline_data = load_mainline_scores(filepath)
        self.last_update = datetime.now()
        
        if self.mainline_data.get("scores"):
            logger.info(f"✅ 加载主线识别结果：{len(self.mainline_data['scores'])} 个主线")
        else:
            logger.warning("⚠️ 主线识别结果为空")
        
        return self.mainline_data
    
    def get_qualified_mainlines(self) -> List[Dict]:
        """
        获取符合条件的主线
        
        条件：
        - 总分 >= min_mainline_score
        - 排名在前 top_mainline_count
        """
        if not self.mainline_data:
            self.load_mainline_data()
        
        scores = self.mainline_data.get("scores", [])
        
        # 筛选 - 只检查总分
        qualified = []
        for mainline in scores:
            total_score = mainline.get("total_score", 0)
            
            if total_score >= self.config["min_mainline_score"]:
                qualified.append(mainline)
                logger.debug(f"主线入选: {mainline.get('name')} (评分:{total_score:.1f})")
        
        if not qualified:
            # 如果没有符合条件的，降低门槛取Top N
            logger.warning(f"无主线达到{self.config['min_mainline_score']}分，降低门槛取Top10")
            sorted_scores = sorted(scores, key=lambda x: x.get("total_score", 0), reverse=True)
            qualified = sorted_scores[:10]
        
        # 排序并取TopN
        qualified.sort(key=lambda x: x.get("total_score", 0), reverse=True)
        result = qualified[:self.config["top_mainline_count"]]
        logger.info(f"符合条件的主线：{len(result)} 个")
        return result
    
    def _get_market_data(self) -> Optional['pd.DataFrame']:
        """获取全市场行情数据（带缓存）"""
        if not PANDAS_AVAILABLE:
            return None
        
        # 检查内存缓存（5分钟有效）
        now = datetime.now()
        if (MainlineSelector._market_data_cache is not None and 
            MainlineSelector._market_data_time is not None and
            (now - MainlineSelector._market_data_time).seconds < 300):
            if isinstance(MainlineSelector._market_data_cache, pd.DataFrame):
                return MainlineSelector._market_data_cache
        
        # 尝试获取实时数据
        if AKSHARE_AVAILABLE and ak_wrapper:
            try:
                df = ak_wrapper.get_stock_spot()
                # 验证返回值是DataFrame
                if isinstance(df, pd.DataFrame) and not df.empty:
                    MainlineSelector._market_data_cache = df
                    MainlineSelector._market_data_time = now
                    logger.info(f"✅ 获取全市场行情: {len(df)} 只股票")
                    return df
            except Exception as e:
                logger.warning(f"获取全市场行情失败: {e}")
        
        # 返回旧缓存（如果是DataFrame）
        if isinstance(MainlineSelector._market_data_cache, pd.DataFrame):
            return MainlineSelector._market_data_cache
        
        return None
    
    def _find_stock_by_name(self, stock_name: str, df: 'pd.DataFrame' = None) -> Optional[Dict]:
        """通过股票名称查找股票信息"""
        if df is None:
            df = self._get_market_data()
        
        if df is None or df.empty:
            return None
        
        try:
            # 精确匹配
            match = df[df['名称'] == stock_name]
            if not match.empty:
                row = match.iloc[0]
                return {
                    "code": row['代码'],
                    "name": row['名称'],
                    "price": float(row.get('最新价', 0) or 0),
                    "change_pct": float(row.get('涨跌幅', 0) or 0),
                    "market_cap": float(row.get('总市值', 0) or 0) / 100000000,
                    "volume_ratio": float(row.get('量比', 1) or 1),
                    "turnover": float(row.get('换手率', 0) or 0),
                }
        except Exception as e:
            logger.debug(f"查找股票失败: {stock_name} - {e}")
        
        return None
    
    def _search_stocks_by_keyword(self, keyword: str, df: 'pd.DataFrame' = None, max_count: int = 20) -> List[Dict]:
        """通过关键词搜索相关股票"""
        if df is None:
            df = self._get_market_data()
        
        if df is None or df.empty:
            return []
        
        result = []
        try:
            # 去除常见后缀
            clean_keyword = keyword.replace("概念", "").replace("板块", "").replace("主题", "")
            
            # 在股票名称中搜索
            if len(clean_keyword) >= 2:
                matches = df[df['名称'].str.contains(clean_keyword, na=False)]
                for _, row in matches.head(max_count).iterrows():
                    name = row['名称']
                    # 排除ST
                    if self.config["exclude_st"] and ('ST' in name or '*ST' in name):
                        continue
                    
                    result.append({
                        "code": row['代码'],
                        "name": name,
                        "price": float(row.get('最新价', 0) or 0),
                        "change_pct": float(row.get('涨跌幅', 0) or 0),
                        "market_cap": float(row.get('总市值', 0) or 0) / 100000000,
                        "match_type": "keyword",
                    })
            
            logger.debug(f"关键词搜索 '{keyword}': 找到 {len(result)} 只股票")
        except Exception as e:
            logger.debug(f"关键词搜索失败: {e}")
        
        return result
    
    def get_mainline_stocks(self, mainline_name: str, mainline_info: Dict = None) -> List[Dict]:
        """
        获取主线板块的成分股
        
        优先级：
        1. JQData概念成分股
        2. AKShare概念/行业板块成分股
        3. 龙头股 + 关键词搜索
        """
        stocks = []
        df = self._get_market_data()  # 预先获取市场数据
        
        # ============================================================
        # 方法1：JQData（如果已认证）
        # ============================================================
        if jqdata_provider and jqdata_provider.available:
            try:
                # 获取所有概念，通过名称匹配
                all_concepts = jqdata_provider.get_all_concepts()
                concept_code = None
                
                for concept in all_concepts:
                    concept_name = concept.get("name", "")
                    # 模糊匹配
                    if (concept_name == mainline_name or 
                        mainline_name in concept_name or 
                        concept_name in mainline_name):
                        concept_code = concept.get("code")
                        logger.debug(f"JQData匹配: {mainline_name} -> {concept_name} ({concept_code})")
                        break
                
                if concept_code:
                    concept_stocks = jqdata_provider.get_concept_stocks(concept_code)
                    if concept_stocks:
                        for stock in concept_stocks:
                            # 转换代码格式
                            code = stock.get("symbol", "").replace(".XSHE", "").replace(".XSHG", "")
                            if code:
                                stocks.append({
                                    "code": code,
                                    "name": stock.get("name", ""),
                                    "sector": mainline_name,
                                    "sector_type": "jqdata_concept",
                                })
                        logger.info(f"✅ JQData获取 {mainline_name} 成分股 {len(stocks)} 只")
                        return stocks
            except Exception as e:
                logger.debug(f"JQData获取失败: {e}")
        
        # ============================================================
        # 方法2：AKShare概念/行业板块
        # ============================================================
        if ak_wrapper:
            try:
                df_cons = ak_wrapper.get_concept_board_cons(mainline_name)
                if df_cons is not None and not df_cons.empty:
                    for _, row in df_cons.iterrows():
                        stocks.append({
                            "code": row.get("代码", ""),
                            "name": row.get("名称", ""),
                            "sector": mainline_name,
                            "sector_type": "akshare_concept",
                        })
                    logger.info(f"✅ AKShare获取 {mainline_name} 概念成分股 {len(stocks)} 只")
                    return stocks
            except Exception as e:
                logger.debug(f"AKShare概念板块获取失败: {e}")
            
            try:
                df_cons = ak_wrapper.get_industry_board_cons(mainline_name)
                if df_cons is not None and not df_cons.empty:
                    for _, row in df_cons.iterrows():
                        stocks.append({
                            "code": row.get("代码", ""),
                            "name": row.get("名称", ""),
                            "sector": mainline_name,
                            "sector_type": "akshare_industry",
                        })
                    logger.info(f"✅ AKShare获取 {mainline_name} 行业成分股 {len(stocks)} 只")
                    return stocks
            except Exception as e:
                logger.debug(f"AKShare行业板块获取失败: {e}")
        
        # ============================================================
        # 方法3：龙头股 + 关键词搜索（Fallback）
        # ============================================================
        logger.warning(f"无法获取 {mainline_name} 成分股，使用龙头股+关键词搜索")
        
        # 添加龙头股
        if mainline_info:
            leader_name = mainline_info.get("leader_stock", "")
            if leader_name:
                leader_info = self._find_stock_by_name(leader_name, df)
                if leader_info:
                    leader_info["sector"] = mainline_name
                    leader_info["sector_type"] = "leader"
                    leader_info["is_leader"] = True
                    stocks.append(leader_info)
                    logger.info(f"添加龙头股: {leader_name} ({leader_info['code']})")
        
        # 关键词搜索
        keyword_stocks = self._search_stocks_by_keyword(mainline_name, df, max_count=15)
        for stock in keyword_stocks:
            # 检查是否已存在
            if not any(s.get("code") == stock.get("code") for s in stocks):
                stock["sector"] = mainline_name
                stock["sector_type"] = "keyword_match"
                stocks.append(stock)
        
        if stocks:
            logger.info(f"龙头+关键词搜索 {mainline_name}: {len(stocks)} 只股票")
        
        return stocks
    
    def filter_and_create_items(
        self, 
        stocks: List[Dict], 
        mainline_info: Dict,
        period: str = "medium"
    ) -> List[StockPoolItem]:
        """
        从成分股中筛选强势股并创建股票池条目
        """
        if not stocks:
            return []
        
        result = []
        df = self._get_market_data()
        
        for stock_data in stocks:
            code = stock_data.get("code", "")
            if not code:
                continue
            
            # 获取实时行情（如果还没有）
            if "price" not in stock_data and df is not None:
                try:
                    match = df[df['代码'] == code]
                    if not match.empty:
                        row = match.iloc[0]
                        stock_data["price"] = float(row.get('最新价', 0) or 0)
                        stock_data["change_pct"] = float(row.get('涨跌幅', 0) or 0)
                        stock_data["market_cap"] = float(row.get('总市值', 0) or 0) / 100000000
                        stock_data["volume_ratio"] = float(row.get('量比', 1) or 1)
                        stock_data["turnover"] = float(row.get('换手率', 0) or 0)
                except:
                    pass
            
            name = stock_data.get("name", "")
            
            # 排除ST
            if self.config["exclude_st"] and ('ST' in name or '*ST' in name):
                continue
            
            # 市值筛选
            market_cap = stock_data.get("market_cap", 0)
            if market_cap > 0:
                if market_cap < self.config["min_market_cap"]:
                    continue
                if market_cap > self.config["max_market_cap"]:
                    continue
            
            # 计算优先级
            is_leader = stock_data.get("is_leader", False)
            change_pct = stock_data.get("change_pct", 0)
            mainline_score = mainline_info.get("total_score", 0)
            
            if is_leader:
                priority = 1  # 龙头股最高优先级
            elif mainline_score >= 85 and change_pct > 3:
                priority = 2
            elif mainline_score >= 75:
                priority = 3
            elif mainline_score >= 65:
                priority = 4
            else:
                priority = 5
            
            # 确定持仓类型
            if mainline_score >= 80 or is_leader:
                pool_type = PoolType.CORE.value
            elif mainline_score >= 60:
                pool_type = PoolType.SATELLITE.value
            else:
                pool_type = PoolType.WATCH.value
            
            # 技术信号
            tech_signals = []
            if change_pct >= 9.9:
                tech_signals.append("涨停")
            elif change_pct >= 5:
                tech_signals.append("大涨")
            
            volume_ratio = stock_data.get("volume_ratio", 1)
            if volume_ratio >= 2:
                tech_signals.append("放量")
            
            if is_leader:
                tech_signals.append("龙头股")
            
            # 入池原因
            sector_type = stock_data.get("sector_type", "unknown")
            if is_leader:
                entry_reason = f"主线龙头：{mainline_info.get('name', '')}，评分{mainline_score:.1f}"
            elif sector_type == "keyword_match":
                entry_reason = f"关键词匹配：{mainline_info.get('name', '')}，评分{mainline_score:.1f}"
            else:
                entry_reason = f"主线强势股：{mainline_info.get('name', '')}，评分{mainline_score:.1f}"
            
            # 创建条目
            item = StockPoolItem(
                code=code,
                name=name,
                industry=stock_data.get("sector_type", ""),
                sector=stock_data.get("sector", mainline_info.get("name", "")),
                
                source=PoolSource.MAINLINE.value,
                entry_reason=entry_reason,
                
                period=period,
                pool_type=pool_type,
                priority=priority,
                
                mainline_name=mainline_info.get("name", ""),
                mainline_score=mainline_score,
                heat_score=mainline_info.get("heat_score", mainline_info.get("热度维度", 0)),
                funds_score=mainline_info.get("funds_score", mainline_info.get("资金维度", 0)),
                momentum_score=mainline_info.get("momentum_score", mainline_info.get("动量维度", 0)),
                
                current_price=stock_data.get("price", 0),
                change_pct=change_pct,
                
                tech_signals=tech_signals
            )
            
            result.append(item)
        
        # 排序：先按优先级，再按涨跌幅
        result.sort(key=lambda x: (x.priority, -x.change_pct))
        return result[:self.config["max_stocks_per_mainline"]]
    
    def select(self, period: str = "medium") -> StockPool:
        """
        执行完整的主线强势股筛选
        
        Args:
            period: 投资周期（short/medium/long）
            
        Returns:
            股票池
        """
        logger.info("=" * 50)
        logger.info("开始主线强势股筛选...")
        
        # 加载主线数据
        if not self.mainline_data:
            self.load_mainline_data()
        
        # 获取符合条件的主线
        qualified_mainlines = self.get_qualified_mainlines()
        logger.info(f"符合条件的主线：{len(qualified_mainlines)} 个")
        
        if not qualified_mainlines:
            logger.warning("无符合条件的主线，返回空股票池")
            return StockPool(description="主线强势股池 - 无数据")
        
        # 创建股票池
        pool = StockPool(
            description=f"主线强势股池 - {datetime.now().strftime('%Y-%m-%d')}",
            mainline_source=str(Path.home() / ".local/share/trquant/reports/heatmap/latest_heatmap_scores.json"),
            mainline_timestamp=self.mainline_data.get("timestamp", "")
        )
        
        # 遍历每个主线，提取强势股
        total_stocks = 0
        for mainline in qualified_mainlines:
            mainline_name = mainline.get("name", "")
            if not mainline_name:
                continue
            
            logger.info(f"处理主线：{mainline_name}（评分：{mainline.get('total_score', 0):.1f}）")
            
            # 获取成分股
            stocks = self.get_mainline_stocks(mainline_name, mainline)
            
            if not stocks:
                logger.warning(f"  → 未获取到成分股")
                continue
            
            # 筛选强势股
            selected = self.filter_and_create_items(stocks, mainline, period)
            
            # 添加到股票池
            added = 0
            for item in selected:
                if pool.add_stock(item):
                    added += 1
            
            total_stocks += added
            logger.info(f"  → 筛选出 {len(selected)} 只，新增 {added} 只")
        
        logger.info("=" * 50)
        logger.info(f"主线强势股筛选完成，共 {len(pool.stocks)} 只股票")
        
        return pool
