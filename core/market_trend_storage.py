#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarketTrendStorage - 市场趋势信号存储
======================================

功能:
1. 保存A股特色指标到MongoDB
2. 保存市场趋势信号供后续流程调用
3. 查询历史信号和指标数据

数据库结构:
- jqquant.market_trend_signals  - 综合市场趋势信号
- jqquant.astock_indicators     - A股特色指标历史
- jqquant.signal_backtest       - 回测结果存档

作者: TRQuant Team
日期: 2026-01-02
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger(__name__)

# MongoDB可用性检测
try:
    from pymongo import MongoClient, DESCENDING, ASCENDING
    from pymongo.errors import ConnectionFailure
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("pymongo未安装，MongoDB存储功能不可用")


@dataclass
class MarketTrendSignal:
    """市场趋势信号数据结构"""
    date: str                        # 信号日期
    
    # 综合评分
    composite_score: float           # 综合得分 (-100 ~ 100)
    signal_level: str                # bullish/bearish/neutral
    
    # 北向资金
    north_fund_daily: float          # 当日净买入(亿)
    north_fund_5d: float             # 5日累计(亿)
    north_fund_score: float          # 北向资金得分
    
    # 融资融券
    margin_balance: float            # 融资余额(亿)
    margin_change_rate: float        # 融资变化率(%)
    margin_score: float              # 两融得分
    
    # 市场宽度
    limit_up_count: int              # 涨停家数
    limit_down_count: int            # 跌停家数
    limit_up_down_ratio: float       # 涨跌停比
    up_down_ratio: float             # 涨跌比
    breadth_score: float             # 宽度得分
    
    # 仓位建议
    position_advice: float           # 建议仓位 (0-1)
    recommendation: str              # 操作建议
    
    # 元数据
    data_source: str = "jqdata"
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d['created_at']:
            d['created_at'] = datetime.now().isoformat()
        return d


class MarketTrendStorage:
    """
    市场趋势信号存储管理器
    
    使用MongoDB存储市场趋势信号和A股特色指标
    """
    
    # MongoDB配置
    MONGO_URI = "mongodb://localhost:27017"
    DB_NAME = "jqquant"
    
    # 集合名称
    SIGNALS_COLLECTION = "market_trend_signals"
    INDICATORS_COLLECTION = "astock_indicators"
    BACKTEST_COLLECTION = "signal_backtest_results"
    
    def __init__(self, mongo_uri: str = None, db_name: str = None):
        """
        初始化存储管理器
        
        Args:
            mongo_uri: MongoDB连接URI
            db_name: 数据库名称
        """
        self.mongo_uri = mongo_uri or self.MONGO_URI
        self.db_name = db_name or self.DB_NAME
        
        self.client = None
        self.db = None
        self._connected = False
        
        self._connect()
    
    def _connect(self):
        """连接MongoDB"""
        if not MONGODB_AVAILABLE:
            logger.warning("pymongo不可用")
            return
        
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            # 测试连接
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self._connected = True
            
            # 创建索引
            self._create_indexes()
            
            logger.info(f"MongoDB连接成功: {self.db_name}")
            
        except Exception as e:
            logger.warning(f"MongoDB连接失败: {e}")
            self._connected = False
    
    def _create_indexes(self):
        """创建索引"""
        if not self._connected:
            return
        
        try:
            # 信号集合索引
            self.db[self.SIGNALS_COLLECTION].create_index(
                [("date", DESCENDING)], unique=True
            )
            self.db[self.SIGNALS_COLLECTION].create_index([("signal_level", ASCENDING)])
            self.db[self.SIGNALS_COLLECTION].create_index([("composite_score", DESCENDING)])
            
            # 指标集合索引
            self.db[self.INDICATORS_COLLECTION].create_index(
                [("date", DESCENDING), ("indicator_type", ASCENDING)], unique=True
            )
            
            # 回测结果索引
            self.db[self.BACKTEST_COLLECTION].create_index([("backtest_time", DESCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([("config.start_date", ASCENDING)])
            
            logger.debug("MongoDB索引已创建")
            
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self._connected
    
    # ==================== 信号存储 ====================
    
    def save_signal(self, signal: MarketTrendSignal) -> bool:
        """
        保存市场趋势信号
        
        Args:
            signal: 信号数据
            
        Returns:
            是否成功
        """
        if not self._connected:
            logger.warning("MongoDB未连接，无法保存信号")
            return False
        
        try:
            doc = signal.to_dict()
            
            # 使用upsert更新或插入
            result = self.db[self.SIGNALS_COLLECTION].update_one(
                {"date": signal.date},
                {"$set": doc},
                upsert=True
            )
            
            logger.info(f"已保存市场趋势信号: {signal.date}, score={signal.composite_score:.1f}")
            return True
            
        except Exception as e:
            logger.error(f"保存信号失败: {e}")
            return False
    
    def save_signal_from_aggregator(self, agg_result, north_result=None, 
                                      margin_result=None, breadth_result=None) -> bool:
        """
        从AStockIndicatorAggregator结果保存信号
        
        Args:
            agg_result: AStockAggregateResult
            north_result: NorthFundData (可选)
            margin_result: MarginData (可选)
            breadth_result: MarketBreadthData (可选)
            
        Returns:
            是否成功
        """
        try:
            # 计算建议仓位
            score = agg_result.composite_score
            if score > 50:
                position = 0.8
            elif score > 20:
                position = 0.6
            elif score > -20:
                position = 0.5
            elif score > -50:
                position = 0.3
            else:
                position = 0.2
            
            signal = MarketTrendSignal(
                date=agg_result.date,
                composite_score=agg_result.composite_score,
                signal_level=agg_result.signal_level,
                
                # 北向资金
                north_fund_daily=north_result.net_buy_amount if north_result else 0.0,
                north_fund_5d=north_result.net_buy_5d if north_result else 0.0,
                north_fund_score=north_result.signal_score if north_result else 0.0,
                
                # 融资融券
                margin_balance=margin_result.fin_balance if margin_result else 0.0,
                margin_change_rate=margin_result.fin_change_rate if margin_result else 0.0,
                margin_score=margin_result.signal_score if margin_result else 0.0,
                
                # 市场宽度
                limit_up_count=breadth_result.limit_up_count if breadth_result else 0,
                limit_down_count=breadth_result.limit_down_count if breadth_result else 0,
                limit_up_down_ratio=breadth_result.limit_up_down_ratio if breadth_result else 1.0,
                up_down_ratio=breadth_result.up_down_ratio if breadth_result else 1.0,
                breadth_score=breadth_result.signal_score if breadth_result else 0.0,
                
                # 建议
                position_advice=position,
                recommendation=agg_result.recommendation,
                data_source=agg_result.data_source
            )
            
            return self.save_signal(signal)
            
        except Exception as e:
            logger.error(f"转换并保存信号失败: {e}")
            return False
    
    def get_latest_signal(self) -> Optional[Dict]:
        """获取最新的市场趋势信号"""
        if not self._connected:
            return None
        
        try:
            doc = self.db[self.SIGNALS_COLLECTION].find_one(
                sort=[("date", DESCENDING)]
            )
            if doc:
                doc.pop('_id', None)
            return doc
            
        except Exception as e:
            logger.error(f"获取最新信号失败: {e}")
            return None
    
    def get_signal_by_date(self, date: str) -> Optional[Dict]:
        """根据日期获取信号"""
        if not self._connected:
            return None
        
        try:
            doc = self.db[self.SIGNALS_COLLECTION].find_one({"date": date})
            if doc:
                doc.pop('_id', None)
            return doc
            
        except Exception as e:
            logger.error(f"获取信号失败: {e}")
            return None
    
    def get_signals_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取日期范围内的信号"""
        if not self._connected:
            return []
        
        try:
            cursor = self.db[self.SIGNALS_COLLECTION].find(
                {"date": {"$gte": start_date, "$lte": end_date}},
                sort=[("date", ASCENDING)]
            )
            
            results = []
            for doc in cursor:
                doc.pop('_id', None)
                results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"获取信号范围失败: {e}")
            return []
    
    def get_recent_signals(self, days: int = 30) -> List[Dict]:
        """获取最近N天的信号"""
        if not self._connected:
            return []
        
        try:
            cursor = self.db[self.SIGNALS_COLLECTION].find(
                sort=[("date", DESCENDING)]
            ).limit(days)
            
            results = []
            for doc in cursor:
                doc.pop('_id', None)
                results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"获取最近信号失败: {e}")
            return []
    
    # ==================== 指标存储 ====================
    
    def save_indicator(self, date: str, indicator_type: str, data: Dict) -> bool:
        """
        保存单个指标数据
        
        Args:
            date: 日期
            indicator_type: 指标类型 (north_fund/margin/breadth)
            data: 指标数据
            
        Returns:
            是否成功
        """
        if not self._connected:
            return False
        
        try:
            doc = {
                "date": date,
                "indicator_type": indicator_type,
                "data": data,
                "updated_at": datetime.now().isoformat()
            }
            
            self.db[self.INDICATORS_COLLECTION].update_one(
                {"date": date, "indicator_type": indicator_type},
                {"$set": doc},
                upsert=True
            )
            
            return True
            
        except Exception as e:
            logger.error(f"保存指标失败: {e}")
            return False
    
    def get_indicator(self, date: str, indicator_type: str) -> Optional[Dict]:
        """获取指标数据"""
        if not self._connected:
            return None
        
        try:
            doc = self.db[self.INDICATORS_COLLECTION].find_one(
                {"date": date, "indicator_type": indicator_type}
            )
            if doc:
                doc.pop('_id', None)
                return doc.get('data')
            return None
            
        except Exception as e:
            logger.error(f"获取指标失败: {e}")
            return None
    
    # ==================== 回测结果存储 ====================
    
    def save_backtest_result(self, result) -> bool:
        """
        保存回测结果
        
        Args:
            result: BacktestResult对象
            
        Returns:
            是否成功
        """
        if not self._connected:
            return False
        
        try:
            # 转换为可序列化的字典
            doc = result.to_dict()
            
            # 截断信号列表 (只保存统计摘要)
            if 'signals' in doc:
                doc['signals_count'] = len(doc['signals'])
                doc['signals'] = doc['signals'][:10]  # 只保留前10条作为样本
            
            doc['saved_at'] = datetime.now().isoformat()
            
            self.db[self.BACKTEST_COLLECTION].insert_one(doc)
            
            logger.info(f"已保存回测结果: {result.backtest_time}")
            return True
            
        except Exception as e:
            logger.error(f"保存回测结果失败: {e}")
            return False
    
    def get_latest_backtest(self) -> Optional[Dict]:
        """获取最新的回测结果"""
        if not self._connected:
            return None
        
        try:
            doc = self.db[self.BACKTEST_COLLECTION].find_one(
                sort=[("backtest_time", DESCENDING)]
            )
            if doc:
                doc.pop('_id', None)
            return doc
            
        except Exception as e:
            logger.error(f"获取回测结果失败: {e}")
            return None
    
    # ==================== 统计方法 ====================
    
    def get_signal_stats(self, days: int = 30) -> Dict:
        """
        获取信号统计
        
        Args:
            days: 统计天数
            
        Returns:
            统计信息
        """
        if not self._connected:
            return {}
        
        try:
            signals = self.get_recent_signals(days)
            
            if not signals:
                return {}
            
            bullish = sum(1 for s in signals if s.get('signal_level') == 'bullish')
            bearish = sum(1 for s in signals if s.get('signal_level') == 'bearish')
            neutral = sum(1 for s in signals if s.get('signal_level') == 'neutral')
            
            scores = [s.get('composite_score', 0) for s in signals]
            
            return {
                "total": len(signals),
                "bullish": bullish,
                "bearish": bearish,
                "neutral": neutral,
                "avg_score": sum(scores) / len(scores) if scores else 0,
                "max_score": max(scores) if scores else 0,
                "min_score": min(scores) if scores else 0,
                "latest_date": signals[0].get('date') if signals else None,
                "latest_signal": signals[0].get('signal_level') if signals else None
            }
            
        except Exception as e:
            logger.error(f"获取信号统计失败: {e}")
            return {}


# ==================== 便捷函数 ====================

_storage_instance: Optional[MarketTrendStorage] = None


def get_market_trend_storage() -> MarketTrendStorage:
    """获取市场趋势存储单例"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = MarketTrendStorage()
    return _storage_instance


def save_current_signal(jq_client=None) -> bool:
    """
    保存当前市场趋势信号
    
    自动获取当日A股指标并保存到MongoDB
    """
    try:
        from core.astock_indicators import AStockIndicatorAggregator
        
        aggregator = AStockIndicatorAggregator(jq_client)
        result = aggregator.analyze()
        
        # 获取详细数据
        from core.astock_indicators import (
            NorthFundAnalyzer, MarginAnalyzer, MarketBreadthAnalyzer
        )
        
        north = NorthFundAnalyzer(jq_client).analyze()
        margin = MarginAnalyzer(jq_client).analyze()
        breadth = MarketBreadthAnalyzer(jq_client).analyze()
        
        storage = get_market_trend_storage()
        return storage.save_signal_from_aggregator(result, north, margin, breadth)
        
    except Exception as e:
        logger.error(f"保存当前信号失败: {e}")
        return False


def get_latest_market_signal() -> Optional[Dict]:
    """获取最新的市场信号"""
    storage = get_market_trend_storage()
    return storage.get_latest_signal()


if __name__ == "__main__":
    # 测试存储
    logging.basicConfig(level=logging.INFO)
    
    storage = MarketTrendStorage()
    
    print("=== 测试MongoDB连接 ===")
    print(f"连接状态: {storage.is_connected()}")
    
    if storage.is_connected():
        print("\n=== 保存测试信号 ===")
        test_signal = MarketTrendSignal(
            date="2024-08-16",
            composite_score=-8.2,
            signal_level="neutral",
            north_fund_daily=-67.75,
            north_fund_5d=-50.36,
            north_fund_score=-54.9,
            margin_balance=25305.33,
            margin_change_rate=0.15,
            margin_score=26.8,
            limit_up_count=32,
            limit_down_count=13,
            limit_up_down_ratio=2.46,
            up_down_ratio=0.53,
            breadth_score=10.7,
            position_advice=0.5,
            recommendation="A股资金面中性，维持现有仓位"
        )
        
        success = storage.save_signal(test_signal)
        print(f"保存结果: {success}")
        
        print("\n=== 获取最新信号 ===")
        latest = storage.get_latest_signal()
        if latest:
            print(f"日期: {latest['date']}")
            print(f"综合得分: {latest['composite_score']}")
            print(f"信号级别: {latest['signal_level']}")
            print(f"仓位建议: {latest['position_advice']}")

