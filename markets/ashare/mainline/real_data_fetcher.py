"""
A股主线识别 - 真实数据获取器

连接真实数据源获取市场数据：
1. AKShare - 免费开源金融数据
2. MongoDB - 本地数据缓存
3. 文件系统 - 调研报告存储

数据类型：
- 板块行情数据
- 资金流向数据
- 北向资金数据
- 市场情绪数据
- 宏观经济数据
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json
import os

logger = logging.getLogger(__name__)

# 尝试导入akshare
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
    logger.info("✅ AKShare 可用")
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("⚠️ AKShare 未安装，将使用缓存数据")

# 尝试导入pymongo
try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("⚠️ PyMongo 未安装，将使用文件缓存")

# 尝试导入pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


@dataclass
class DataFetchResult:
    """数据获取结果"""
    success: bool
    data: Any
    source: str                  # 数据来源: akshare, mongodb, cache, mock
    fetch_time: datetime
    cache_time: Optional[datetime] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "source": self.source,
            "fetch_time": self.fetch_time.isoformat(),
            "cache_time": self.cache_time.isoformat() if self.cache_time else None,
            "error": self.error,
            "data_preview": str(self.data)[:200] if self.data else None,
        }


class RealDataFetcher:
    """
    真实数据获取器
    
    数据获取优先级：
    1. AKShare API（实时数据）
    2. MongoDB缓存（近期数据）
    3. 文件缓存（历史数据）
    """
    
    def __init__(self, mongo_uri: str = "mongodb://localhost:27017"):
        self.mongo_uri = mongo_uri
        self.db = None
        self.cache_dir = os.path.expanduser("~/.local/share/trquant/cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self._init_mongodb()
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        if MONGODB_AVAILABLE:
            try:
                client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
                client.server_info()  # 测试连接
                self.db = client.jqquant
                logger.info("✅ MongoDB 连接成功")
            except Exception as e:
                logger.warning(f"⚠️ MongoDB 连接失败: {e}")
                self.db = None
    
    # ================================================================
    # 板块数据（使用同花顺数据源，避免东方财富反爬虫）
    # ================================================================
    
    def fetch_sector_flow(self, timeout: int = 15) -> DataFetchResult:
        """
        获取板块资金流向数据
        
        数据源: 同花顺 -> AKShare (stock_fund_flow_industry)
        字段: 行业名称、涨跌幅、资金流入流出、净额等
        """
        try:
            if AKSHARE_AVAILABLE:
                import socket
                socket.setdefaulttimeout(timeout)
                
                # 使用同花顺行业资金流向API（更稳定）
                df = ak.stock_fund_flow_industry(symbol="即时")
                
                if df is not None and not df.empty:
                    # 转换为标准格式
                    data = []
                    for _, row in df.head(30).iterrows():
                        # 净额单位是亿元
                        net_inflow = float(row.get("净额", 0))
                        inflow = float(row.get("流入资金", 0))
                        outflow = float(row.get("流出资金", 0))
                        
                        data.append({
                            "sector_name": row.get("行业", ""),
                            "change_pct": float(row.get("行业-涨跌幅", 0)),
                            "main_net_inflow": net_inflow,
                            "main_net_ratio": (net_inflow / inflow * 100) if inflow > 0 else 0,
                            "inflow": inflow,
                            "outflow": outflow,
                            "leader_stock": row.get("领涨股", ""),
                            "leader_change": float(row.get("领涨股-涨跌幅", 0)),
                        })
                    
                    # 缓存到MongoDB
                    self._cache_to_mongo("sector_flow", data)
                    
                    return DataFetchResult(
                        success=True,
                        data=data,
                        source="akshare(同花顺)",
                        fetch_time=datetime.now(),
                    )
            
            # 尝试从缓存获取
            cached = self._get_from_cache("sector_flow")
            if cached:
                return cached
            
            # 使用示例数据（网络不可用时）
            return self._get_sample_sector_flow()
            
        except Exception as e:
            logger.warning(f"获取板块资金流向失败: {e}，尝试使用缓存...")
            cached = self._get_from_cache("sector_flow")
            if cached:
                return cached
            # 使用示例数据
            return self._get_sample_sector_flow()
    
    def _get_sample_sector_flow(self) -> DataFetchResult:
        """获取示例板块数据（网络不可用时使用）"""
        sample_data = [
            {"sector_name": "人工智能", "change_pct": 3.25, "main_net_inflow": 45.6, "main_net_ratio": 12.5, "super_large_inflow": 25.3, "large_inflow": 20.3},
            {"sector_name": "半导体", "change_pct": 2.88, "main_net_inflow": 38.2, "main_net_ratio": 10.8, "super_large_inflow": 20.1, "large_inflow": 18.1},
            {"sector_name": "光模块", "change_pct": 4.52, "main_net_inflow": 28.5, "main_net_ratio": 15.2, "super_large_inflow": 15.8, "large_inflow": 12.7},
            {"sector_name": "算力", "change_pct": 3.15, "main_net_inflow": 22.3, "main_net_ratio": 11.3, "super_large_inflow": 12.5, "large_inflow": 9.8},
            {"sector_name": "新能源", "change_pct": 1.25, "main_net_inflow": 15.8, "main_net_ratio": 5.6, "super_large_inflow": 8.5, "large_inflow": 7.3},
            {"sector_name": "消费电子", "change_pct": 1.88, "main_net_inflow": 12.5, "main_net_ratio": 6.8, "super_large_inflow": 7.2, "large_inflow": 5.3},
            {"sector_name": "医药生物", "change_pct": 0.95, "main_net_inflow": 8.6, "main_net_ratio": 3.2, "super_large_inflow": 4.8, "large_inflow": 3.8},
            {"sector_name": "汽车", "change_pct": 1.55, "main_net_inflow": 10.2, "main_net_ratio": 4.5, "super_large_inflow": 5.5, "large_inflow": 4.7},
            {"sector_name": "银行", "change_pct": -0.35, "main_net_inflow": -5.8, "main_net_ratio": -1.2, "super_large_inflow": -3.2, "large_inflow": -2.6},
            {"sector_name": "房地产", "change_pct": -1.25, "main_net_inflow": -12.5, "main_net_ratio": -4.5, "super_large_inflow": -7.2, "large_inflow": -5.3},
        ]
        return DataFetchResult(
            success=True,
            data=sample_data,
            source="sample_data（网络不可用）",
            fetch_time=datetime.now(),
            error="网络连接失败，使用示例数据",
        )
    
    def fetch_concept_board(self) -> DataFetchResult:
        """
        获取概念板块行情
        
        数据源: 同花顺 -> AKShare (stock_fund_flow_concept)
        """
        try:
            if AKSHARE_AVAILABLE:
                import socket
                socket.setdefaulttimeout(20)
                
                # 使用同花顺概念资金流向API（更稳定）
                df = ak.stock_fund_flow_concept(symbol="即时")
                
                if df is not None and not df.empty:
                    data = []
                    for _, row in df.head(50).iterrows():
                        net_inflow = float(row.get("净额", 0))
                        
                        data.append({
                            "board_name": row.get("行业", ""),  # 概念名称
                            "change_pct": float(row.get("行业-涨跌幅", 0)),
                            "net_inflow": net_inflow,
                            "inflow": float(row.get("流入资金", 0)),
                            "outflow": float(row.get("流出资金", 0)),
                            "company_count": int(row.get("公司家数", 0)),
                            "leader_stock": row.get("领涨股", ""),
                            "leader_change": float(row.get("领涨股-涨跌幅", 0)),
                        })
                    
                    self._cache_to_mongo("concept_board", data)
                    
                    return DataFetchResult(
                        success=True,
                        data=data,
                        source="akshare(同花顺)",
                        fetch_time=datetime.now(),
                    )
            
            cached = self._get_from_cache("concept_board")
            if cached:
                return cached
            
            return self._get_sample_concept_board()
            
        except Exception as e:
            logger.warning(f"获取概念板块失败: {e}")
            cached = self._get_from_cache("concept_board")
            return cached if cached else self._get_sample_concept_board()
    
    def _get_sample_concept_board(self) -> DataFetchResult:
        """获取示例概念板块数据"""
        sample_data = [
            {"board_name": "ChatGPT概念", "change_pct": 4.25, "total_mv": 15000, "turnover_rate": 5.2, "up_count": 45, "down_count": 5, "leader_stock": "科大讯飞", "leader_change": 8.5},
            {"board_name": "算力", "change_pct": 3.88, "total_mv": 12000, "turnover_rate": 4.8, "up_count": 38, "down_count": 8, "leader_stock": "中科曙光", "leader_change": 7.2},
            {"board_name": "光模块", "change_pct": 5.15, "total_mv": 3500, "turnover_rate": 8.5, "up_count": 18, "down_count": 2, "leader_stock": "中际旭创", "leader_change": 10.0},
            {"board_name": "半导体设备", "change_pct": 2.95, "total_mv": 8000, "turnover_rate": 3.8, "up_count": 28, "down_count": 6, "leader_stock": "北方华创", "leader_change": 5.5},
            {"board_name": "机器人", "change_pct": 3.45, "total_mv": 5500, "turnover_rate": 6.2, "up_count": 32, "down_count": 4, "leader_stock": "汇川技术", "leader_change": 6.8},
        ]
        return DataFetchResult(
            success=True,
            data=sample_data,
            source="sample_data（网络不可用）",
            fetch_time=datetime.now(),
        )
    
    # ================================================================
    # 北向资金
    # ================================================================
    
    def fetch_northbound_flow(self) -> DataFetchResult:
        """
        获取北向资金流向
        
        数据源: 东方财富 -> AKShare
        API: stock_hsgt_fund_flow_summary_em (新版API)
        """
        try:
            if AKSHARE_AVAILABLE:
                import socket
                socket.setdefaulttimeout(15)
                
                # 使用新版API: stock_hsgt_fund_flow_summary_em
                df = ak.stock_hsgt_fund_flow_summary_em()
                
                if df is not None and not df.empty:
                    # 筛选北向资金（沪股通+深股通）
                    north_df = df[df["资金方向"] == "北向"]
                    
                    # 计算今日净流入
                    today_net = 0
                    for _, row in north_df.iterrows():
                        try:
                            # 资金净流入列
                            net = float(row.get("资金净流入", 0))
                            today_net += net
                        except:
                            pass
                    
                    # 转换为亿元
                    today_net = today_net / 1e8 if today_net > 1e6 else today_net
                    
                    data = {
                        "today_net": today_net,
                        "week_net": today_net * 5,  # 估算值
                        "month_net": today_net * 20,  # 估算值
                        "details": [
                            {
                                "板块": row.get("板块", ""),
                                "成交净买额": float(row.get("成交净买额", 0)) / 1e8,
                                "资金净流入": float(row.get("资金净流入", 0)) / 1e8,
                            }
                            for _, row in north_df.iterrows()
                        ],
                        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    
                    self._cache_to_mongo("northbound_flow", data)
                    
                    return DataFetchResult(
                        success=True,
                        data=data,
                        source="akshare",
                        fetch_time=datetime.now(),
                    )
            
            cached = self._get_from_cache("northbound_flow")
            if cached:
                return cached
            
            return self._get_sample_northbound()
            
        except Exception as e:
            logger.warning(f"获取北向资金失败: {e}")
            cached = self._get_from_cache("northbound_flow")
            return cached if cached else self._get_sample_northbound()
    
    def _get_sample_northbound(self) -> DataFetchResult:
        """获取示例北向资金数据"""
        return DataFetchResult(
            success=True,
            data={
                "today_net": 45.8,
                "week_net": 125.6,
                "month_net": 380.2,
                "history": [
                    {"date": "2024-01-25", "net_flow": 45.8},
                    {"date": "2024-01-24", "net_flow": 32.5},
                    {"date": "2024-01-23", "net_flow": -15.2},
                ]
            },
            source="sample_data（网络不可用）",
            fetch_time=datetime.now(),
        )
    
    # ================================================================
    # 市场情绪
    # ================================================================
    
    def fetch_market_sentiment(self) -> DataFetchResult:
        """
        获取市场情绪数据
        
        包含：涨跌家数、涨停跌停、连板数等
        """
        try:
            if AKSHARE_AVAILABLE:
                import socket
                socket.setdefaulttimeout(10)
                
                df_zt = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))
                
                try:
                    df_dt = ak.stock_zt_pool_dtgc_em(date=datetime.now().strftime("%Y%m%d"))
                    down_limit_count = len(df_dt) if df_dt is not None else 0
                except:
                    down_limit_count = 0
                
                up_limit_count = len(df_zt) if df_zt is not None else 0
                
                continuous_limit = {}
                if df_zt is not None and not df_zt.empty and "连板数" in df_zt.columns:
                    for _, row in df_zt.iterrows():
                        lb = int(row.get("连板数", 1))
                        continuous_limit[lb] = continuous_limit.get(lb, 0) + 1
                
                data = {
                    "up_limit_count": up_limit_count,
                    "down_limit_count": down_limit_count,
                    "continuous_limit": continuous_limit,
                    "sentiment_score": min(100, max(0, 50 + (up_limit_count - down_limit_count) * 2)),
                    "fetch_date": datetime.now().strftime("%Y-%m-%d"),
                }
                
                self._cache_to_mongo("market_sentiment", data)
                
                return DataFetchResult(
                    success=True,
                    data=data,
                    source="akshare",
                    fetch_time=datetime.now(),
                )
            
            cached = self._get_from_cache("market_sentiment")
            if cached:
                return cached
            
            return self._get_sample_sentiment()
            
        except Exception as e:
            logger.warning(f"获取市场情绪失败: {e}")
            cached = self._get_from_cache("market_sentiment")
            return cached if cached else self._get_sample_sentiment()
    
    def _get_sample_sentiment(self) -> DataFetchResult:
        """获取示例市场情绪数据"""
        return DataFetchResult(
            success=True,
            data={
                "up_limit_count": 68,
                "down_limit_count": 12,
                "continuous_limit": {1: 45, 2: 15, 3: 5, 4: 2, 5: 1},
                "sentiment_score": 72,
                "fetch_date": datetime.now().strftime("%Y-%m-%d"),
            },
            source="sample_data（网络不可用）",
            fetch_time=datetime.now(),
        )
    
    # ================================================================
    # 宏观数据
    # ================================================================
    
    def fetch_macro_data(self) -> DataFetchResult:
        """
        获取宏观经济数据
        
        包含：PMI、CPI、社融等
        """
        try:
            data = {}
            
            if AKSHARE_AVAILABLE:
                # PMI数据
                try:
                    df_pmi = ak.macro_china_pmi_yearly()
                    if df_pmi is not None and not df_pmi.empty:
                        latest_pmi = df_pmi.iloc[-1]
                        data["pmi"] = {
                            "value": float(latest_pmi.get("制造业-Loss", latest_pmi.iloc[-1])),
                            "date": str(latest_pmi.name if hasattr(latest_pmi, 'name') else ""),
                        }
                except Exception as e:
                    logger.warning(f"获取PMI失败: {e}")
                
                # 尝试获取其他宏观数据
                try:
                    # M2数据
                    df_m2 = ak.macro_china_money_supply()
                    if df_m2 is not None and not df_m2.empty:
                        latest = df_m2.iloc[-1]
                        data["m2_growth"] = float(latest.get("M2-同比增长", 0))
                except:
                    pass
                
                if data:
                    self._cache_to_mongo("macro_data", data)
                    return DataFetchResult(
                        success=True,
                        data=data,
                        source="akshare",
                        fetch_time=datetime.now(),
                    )
            
            cached = self._get_from_cache("macro_data")
            if cached:
                return cached
                
            return DataFetchResult(
                success=False, data=None, source="none",
                fetch_time=datetime.now(), error="无法获取数据"
            )
            
        except Exception as e:
            logger.error(f"获取宏观数据失败: {e}")
            cached = self._get_from_cache("macro_data")
            return cached if cached else DataFetchResult(
                success=False, data=None, source="error",
                fetch_time=datetime.now(), error=str(e)
            )
    
    # ================================================================
    # 龙虎榜
    # ================================================================
    
    def fetch_dragon_tiger(self) -> DataFetchResult:
        """
        获取龙虎榜数据
        """
        try:
            if AKSHARE_AVAILABLE:
                df = ak.stock_lhb_detail_em(
                    start_date=datetime.now().strftime("%Y%m%d"),
                    end_date=datetime.now().strftime("%Y%m%d")
                )
                
                if df is not None and not df.empty:
                    data = []
                    for _, row in df.head(20).iterrows():
                        # 安全获取值，防止None类型错误
                        net_buy = row.get("净买额", 0)
                        try:
                            net_buy_val = float(net_buy) / 1e4 if net_buy is not None else 0.0
                        except (TypeError, ValueError):
                            net_buy_val = 0.0
                        data.append({
                            "code": str(row.get("代码", "") or ""),
                            "name": str(row.get("名称", "") or ""),
                            "reason": str(row.get("上榜原因", "") or ""),
                            "net_buy": net_buy_val,  # 万元
                        })
                    
                    self._cache_to_mongo("dragon_tiger", data)
                    
                    return DataFetchResult(
                        success=True,
                        data=data,
                        source="akshare",
                        fetch_time=datetime.now(),
                    )
            
            cached = self._get_from_cache("dragon_tiger")
            if cached:
                return cached
                
            return DataFetchResult(
                success=False, data=None, source="none",
                fetch_time=datetime.now(), error="无法获取数据"
            )
            
        except Exception as e:
            logger.error(f"获取龙虎榜失败: {e}")
            cached = self._get_from_cache("dragon_tiger")
            return cached if cached else DataFetchResult(
                success=False, data=None, source="error",
                fetch_time=datetime.now(), error=str(e)
            )
    
    # ================================================================
    # 综合数据获取
    # ================================================================
    
    def fetch_all_data(self) -> Dict[str, DataFetchResult]:
        """
        获取所有数据源的数据
        """
        results = {}
        
        logger.info("📡 开始获取真实市场数据...")
        
        # 板块资金流向
        logger.info("  → 获取板块资金流向...")
        results["sector_flow"] = self.fetch_sector_flow()
        
        # 概念板块
        logger.info("  → 获取概念板块行情...")
        results["concept_board"] = self.fetch_concept_board()
        
        # 北向资金
        logger.info("  → 获取北向资金流向...")
        results["northbound_flow"] = self.fetch_northbound_flow()
        
        # 市场情绪
        logger.info("  → 获取市场情绪数据...")
        results["market_sentiment"] = self.fetch_market_sentiment()
        
        # 宏观数据
        logger.info("  → 获取宏观经济数据...")
        results["macro_data"] = self.fetch_macro_data()
        
        # 龙虎榜
        logger.info("  → 获取龙虎榜数据...")
        results["dragon_tiger"] = self.fetch_dragon_tiger()
        
        # 统计
        success_count = sum(1 for r in results.values() if r.success)
        logger.info(f"✅ 数据获取完成: {success_count}/{len(results)} 成功")
        
        return results
    
    # ================================================================
    # 缓存管理
    # ================================================================
    
    def _cache_to_mongo(self, key: str, data: Any):
        """缓存数据到MongoDB"""
        if self.db is not None:
            try:
                # 确保数据可以被MongoDB存储（将int键转为str）
                safe_data = self._make_mongo_safe(data)
                self.db.cache.update_one(
                    {"key": key},
                    {
                        "$set": {
                            "data": safe_data,
                            "updated_at": datetime.now(),
                        }
                    },
                    upsert=True
                )
            except Exception as e:
                logger.warning(f"MongoDB缓存失败: {e}")
        
        # 同时保存到文件
        self._cache_to_file(key, data)
    
    def _make_mongo_safe(self, data: Any) -> Any:
        """确保数据可以被MongoDB存储"""
        if isinstance(data, dict):
            return {str(k): self._make_mongo_safe(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_mongo_safe(item) for item in data]
        else:
            return data
    
    def _cache_to_file(self, key: str, data: Any):
        """缓存数据到文件"""
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "data": data,
                    "updated_at": datetime.now().isoformat(),
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"文件缓存失败: {e}")
    
    def _get_from_cache(self, key: str) -> Optional[DataFetchResult]:
        """从缓存获取数据"""
        # 先尝试MongoDB
        if self.db is not None:
            try:
                doc = self.db.cache.find_one({"key": key})
                if doc:
                    return DataFetchResult(
                        success=True,
                        data=doc["data"],
                        source="mongodb",
                        fetch_time=datetime.now(),
                        cache_time=doc.get("updated_at"),
                    )
            except:
                pass
        
        # 再尝试文件缓存
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                    return DataFetchResult(
                        success=True,
                        data=cached["data"],
                        source="file_cache",
                        fetch_time=datetime.now(),
                        cache_time=datetime.fromisoformat(cached["updated_at"]),
                    )
        except:
            pass
        
        return None
    
    def get_data_status(self) -> Dict:
        """获取数据源状态"""
        return {
            "akshare_available": AKSHARE_AVAILABLE,
            "akshare_version": ak.__version__ if AKSHARE_AVAILABLE else None,
            "mongodb_available": self.db is not None,
            "mongodb_uri": self.mongo_uri if self.db is not None else None,
            "cache_dir": self.cache_dir,
            "cache_files": os.listdir(self.cache_dir) if os.path.exists(self.cache_dir) else [],
        }
    
    def test_all_connections(self) -> Dict[str, Dict]:
        """
        测试所有数据源连接
        
        Returns:
            {
                "akshare": {"status": "ok/error", "message": "...", "latency_ms": 123},
                "mongodb": {"status": "ok/error", "message": "...", "latency_ms": 123},
                "apis": {
                    "northbound": {"status": "ok/error", "message": "...", "data_count": 10},
                    "sector_flow": {...},
                    ...
                }
            }
        """
        import time
        results = {
            "akshare": {"status": "unknown", "message": "", "latency_ms": 0},
            "mongodb": {"status": "unknown", "message": "", "latency_ms": 0},
            "apis": {},
            "test_time": datetime.now().isoformat(),
        }
        
        # 测试AKShare
        if AKSHARE_AVAILABLE:
            results["akshare"]["status"] = "available"
            results["akshare"]["version"] = ak.__version__
            results["akshare"]["message"] = f"AKShare {ak.__version__} 已安装"
        else:
            results["akshare"]["status"] = "not_installed"
            results["akshare"]["message"] = "AKShare 未安装"
        
        # 测试MongoDB
        start = time.time()
        if self.db is not None:
            try:
                self.db.command("ping")
                latency = (time.time() - start) * 1000
                results["mongodb"]["status"] = "connected"
                results["mongodb"]["message"] = f"MongoDB 连接正常"
                results["mongodb"]["latency_ms"] = int(latency)
            except Exception as e:
                results["mongodb"]["status"] = "error"
                results["mongodb"]["message"] = str(e)
        else:
            results["mongodb"]["status"] = "not_connected"
            results["mongodb"]["message"] = "MongoDB 未连接"
        
        # 测试各个API
        api_tests = [
            ("northbound", self._test_northbound_api),
            ("market_fund_flow", self._test_market_fund_flow_api),
            ("limit_up", self._test_limit_up_api),
            ("dragon_tiger", self._test_dragon_tiger_api),
            ("concept_board", self._test_concept_board_api),
            ("sector_flow", self._test_sector_flow_api),
        ]
        
        for api_name, test_func in api_tests:
            try:
                start = time.time()
                result = test_func()
                latency = (time.time() - start) * 1000
                results["apis"][api_name] = {
                    "status": "ok" if result["success"] else "error",
                    "message": result.get("message", ""),
                    "data_count": result.get("data_count", 0),
                    "latency_ms": int(latency),
                }
            except Exception as e:
                results["apis"][api_name] = {
                    "status": "error",
                    "message": str(e),
                    "data_count": 0,
                    "latency_ms": 0,
                }
        
        return results
    
    def _test_northbound_api(self) -> Dict:
        """测试北向资金API"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(10)
        
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is not None and not df.empty:
            return {"success": True, "message": "北向资金API正常", "data_count": len(df)}
        return {"success": False, "message": "返回数据为空"}
    
    def _test_market_fund_flow_api(self) -> Dict:
        """测试市场资金流向API"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(10)
        
        df = ak.stock_market_fund_flow()
        if df is not None and not df.empty:
            return {"success": True, "message": "市场资金流向API正常", "data_count": len(df)}
        return {"success": False, "message": "返回数据为空"}
    
    def _test_limit_up_api(self) -> Dict:
        """测试涨停池API"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(10)
        
        df = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))
        if df is not None and not df.empty:
            return {"success": True, "message": "涨停池API正常", "data_count": len(df)}
        return {"success": False, "message": "返回数据为空"}
    
    def _test_dragon_tiger_api(self) -> Dict:
        """测试龙虎榜API"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(15)
        
        today = datetime.now().strftime("%Y%m%d")
        df = ak.stock_lhb_detail_em(start_date=today, end_date=today)
        if df is not None and not df.empty:
            return {"success": True, "message": "龙虎榜API正常", "data_count": len(df)}
        return {"success": True, "message": "龙虎榜API正常（今日无数据）", "data_count": 0}
    
    def _test_concept_board_api(self) -> Dict:
        """测试概念板块API（同花顺数据源）"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(20)
        
        try:
            # 使用同花顺概念资金流向API
            df = ak.stock_fund_flow_concept(symbol="即时")
            if df is not None and not df.empty:
                return {"success": True, "message": "概念板块API正常(同花顺)", "data_count": len(df)}
            return {"success": False, "message": "返回数据为空"}
        except Exception as e:
            return {"success": False, "message": f"网络超时或API错误: {str(e)[:50]}"}
    
    def _test_sector_flow_api(self) -> Dict:
        """测试板块资金流向API（同花顺数据源）"""
        if not AKSHARE_AVAILABLE:
            return {"success": False, "message": "AKShare未安装"}
        
        import socket
        socket.setdefaulttimeout(15)
        
        try:
            # 使用同花顺行业资金流向API
            df = ak.stock_fund_flow_industry(symbol="即时")
            if df is not None and not df.empty:
                return {"success": True, "message": "板块资金流向API正常(同花顺)", "data_count": len(df)}
            return {"success": False, "message": "返回数据为空"}
        except Exception as e:
            return {"success": False, "message": f"网络超时或API错误: {str(e)[:50]}"}


# 全局实例
real_data_fetcher = RealDataFetcher()

