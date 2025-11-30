#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于主线的一键扫描模块

从MongoDB读取已映射的主线（综合评分时已完成JQData映射），
直接使用JQData获取成分股进行筛选
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# 尝试导入MongoDB
try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

# 尝试导入JQData
try:
    from jqdata.client import JQDataClient
    JQDATA_AVAILABLE = True
except ImportError:
    JQDATA_AVAILABLE = False
    JQDataClient = None

from core.momentum_growth_scanner import MomentumGrowthScanner, MomentumGrowthStock


class MainlineBasedScanner:
    """
    基于主线的扫描器
    
    流程（已优化）：
    1. 从MongoDB读取已映射的主线（综合评分时已完成AKShare→JQData映射）
    2. 直接使用JQData获取成分股（无需重新映射）
    3. 对成分股进行动量和成长潜力筛选
    4. 返回推荐股票和特征条件
    
    数据流：
    投资主线(AKShare) → 综合评分 → JQData映射 → MongoDB
                                                    ↓
    候选池扫描 ← 读取已映射主线 ← MongoDB
                    ↓
    JQData获取成分股 → 动量/成长筛选 → 推荐股票
    """
    
    def __init__(
        self,
        jq_client: Optional[JQDataClient] = None,
        mongo_uri: str = "mongodb://localhost:27017"
    ):
        """
        初始化扫描器
        
        Args:
            jq_client: JQData客户端（必须，用于获取成分股）
            mongo_uri: MongoDB连接URI
        """
        self.jq_client = jq_client
        self.mongo_uri = mongo_uri
        self.db = None
        
        # 初始化MongoDB
        if MONGODB_AVAILABLE:
            try:
                client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
                client.server_info()
                self.db = client.jqquant
                logger.info("✅ MongoDB连接成功")
            except Exception as e:
                logger.warning(f"⚠️ MongoDB连接失败: {e}")
        
        # 初始化扫描器（仅使用JQData，不用AKShare）
        self.scanner = MomentumGrowthScanner(jq_client=jq_client, use_akshare=False)
    
    def scan_from_mainlines(
        self,
        period: str = 'medium',
        min_score: float = 60.0,
        max_mainlines: int = 10,
        max_stocks_per_mainline: int = 20
    ) -> Dict[str, any]:
        """
        从已映射的主线扫描候选股票
        
        Args:
            period: 期限（short/medium/long）
            min_score: 最小综合得分
            max_mainlines: 最多处理的主线数
            max_stocks_per_mainline: 每个主线最多返回的股票数
        
        Returns:
            Dict: {
                'mainlines': [...],  # 处理的主线列表
                'stocks': [...],     # 推荐的股票列表
                'features': {...}    # 推荐的特征条件
            }
        """
        # 1. 从MongoDB读取已映射的主线（优先）
        mapped_mainlines_data = self._load_mapped_mainlines_from_mongodb()
        
        if not mapped_mainlines_data:
            # 如果MongoDB没有，尝试从文件读取（需要重新映射）
            logger.warning("⚠️ MongoDB中未找到已映射的主线，请先运行综合评分")
            raise Exception("未找到已映射的主线数据，请先运行「投资主线 → 综合评分」")
        
        logger.info(f"✅ 从MongoDB读取到 {len(mapped_mainlines_data)} 个已映射主线")
        
        # 2. 过滤出已成功映射到JQData的主线
        jqdata_mapped = [m for m in mapped_mainlines_data if m.get('jqdata_mapped')]
        if not jqdata_mapped:
            raise Exception("所有主线都未能映射到JQData，请检查主线名称")
        
        logger.info(f"✅ 其中 {len(jqdata_mapped)} 个已映射到JQData")
        
        # 3. 限制主线数量
        jqdata_mapped = jqdata_mapped[:max_mainlines]
        
        # 4. 直接使用JQData获取成分股并筛选
        processed_mainlines = []
        all_stocks = []
        
        for mainline in jqdata_mapped:
            mainline_name = mainline.get('name', '')
            jqdata_code = mainline.get('jqdata_code')
            jqdata_name = mainline.get('jqdata_name')
            jqdata_type = mainline.get('jqdata_type')
            
            if not jqdata_code:
                continue
            
            logger.info(f"处理主线: {mainline_name} → {jqdata_name}")
            
            # 直接使用JQData获取成分股（无需重新映射）
            stocks = self._get_stocks_by_jqdata(jqdata_code, jqdata_type)
            if not stocks:
                logger.warning(f"  ⚠️ 未获取到成分股")
                continue
            
            logger.info(f"  → 获取到 {len(stocks)} 只成分股（JQData）")
            
            # 筛选股票
            filtered_stocks = self._filter_stocks_jqdata(
                stocks=stocks,
                mainline_name=mainline_name,
                period=period,
                min_score=min_score,
                max_stocks=max_stocks_per_mainline
            )
            
            logger.info(f"  → 筛选后剩余 {len(filtered_stocks)} 只股票")
            
            processed_mainlines.append({
                'akshare_name': mainline_name,
                'jqdata_name': jqdata_name,
                'jqdata_code': jqdata_code,
                'mapping_type': jqdata_type,
                'total_score': mainline.get('total_score', 0),
                'stock_count': len(filtered_stocks)
            })
            
            all_stocks.extend(filtered_stocks)
        
        # 5. 去重和排序
        unique_stocks = self._deduplicate_stocks(all_stocks)
        unique_stocks.sort(key=lambda x: x.composite_score, reverse=True)
        
        # 6. 获取推荐特征条件
        features = self._get_recommended_features(period, processed_mainlines)
        
        return {
            'mainlines': processed_mainlines,
            'stocks': unique_stocks,
            'features': features,
            'total_count': len(unique_stocks),
            'data_source': 'JQData'  # 明确标注数据源
        }
    
    def _load_mapped_mainlines_from_mongodb(self) -> List[Dict]:
        """从MongoDB读取已映射的主线数据"""
        if not self.db:
            return []
        
        try:
            # 从mainline_mapped集合读取（综合评分时写入）
            collection = self.db.mainline_mapped
            latest = collection.find_one(
                sort=[("timestamp", -1)]
            )
            if latest:
                mainlines = latest.get('mainlines', [])
                logger.info(f"从MongoDB读取: {latest.get('mapped_count', 0)}/{latest.get('total_count', 0)} 个映射成功")
                return mainlines
                
        except Exception as e:
            logger.warning(f"从MongoDB读取已映射主线失败: {e}")
        
        return []
    
    def _get_stocks_by_jqdata(self, jqdata_code: str, jqdata_type: str) -> List[str]:
        """使用JQData获取成分股"""
        if not self.jq_client or not self.jq_client.is_authenticated():
            return []
        
        try:
            if jqdata_type == 'concept':
                stocks = self.jq_client.get_concept_stocks(jqdata_code)
            elif jqdata_type == 'industry':
                stocks = self.jq_client.get_industry_stocks(jqdata_code)
            else:
                return []
            
            # 转换为股票代码列表
            if isinstance(stocks, list):
                return stocks
            elif hasattr(stocks, 'tolist'):
                return stocks.tolist()
            else:
                return []
        except Exception as e:
            logger.error(f"JQData获取成分股失败: {e}")
            return []
    
    def _filter_stocks_jqdata(
        self,
        stocks: List[str],
        mainline_name: str,
        period: str,
        min_score: float,
        max_stocks: int
    ) -> List[MomentumGrowthStock]:
        """使用JQData筛选股票"""
        filtered = []
        
        # 限制处理数量，避免超时
        stocks_to_process = stocks[:50]
        
        for i, stock_code in enumerate(stocks_to_process):
            if i % 10 == 0:
                logger.debug(f"  筛选进度: {i}/{len(stocks_to_process)}")
            
            try:
                # 使用JQData分析股票
                stock = self.scanner._analyze_stock(
                    stock_code=stock_code,
                    period=period,
                    lookback_days=self.scanner.period_configs[period]['lookback_days'],
                    end_date=self.jq_client.get_available_end_date() if self.jq_client else datetime.now().strftime('%Y-%m-%d'),
                    start_date=None
                )
                
                if stock and stock.composite_score >= min_score:
                    # 添加主线信息
                    stock.tags.append(mainline_name)
                    filtered.append(stock)
                    
            except Exception as e:
                logger.debug(f"分析股票 {stock_code} 失败: {e}")
                continue
        
        # 排序并限制数量
        filtered.sort(key=lambda x: x.composite_score, reverse=True)
        return filtered[:max_stocks]
    
    def _deduplicate_stocks(self, stocks: List[MomentumGrowthStock]) -> List[MomentumGrowthStock]:
        """去重股票"""
        seen = set()
        unique = []
        for stock in stocks:
            if stock.code not in seen:
                seen.add(stock.code)
                unique.append(stock)
        return unique
    
    def _get_recommended_features(
        self,
        period: str,
        mapped_mainlines: List[Dict]
    ) -> Dict:
        """获取推荐的特征条件"""
        if not mapped_mainlines:
            return {}
        
        # 使用第一个主线的映射结果作为参考
        first_mapping = mapped_mainlines[0]
        # 这里需要从mapper获取推荐特征，但需要MainlineMapping对象
        # 简化处理，直接返回通用特征
        features = {
            'period': period,
            'min_composite_score': 65.0,
            'min_momentum_score': 60.0,
            'min_growth_score': 60.0,
        }
        
        if period == 'short':
            features['min_momentum_score'] = 70.0
        elif period == 'long':
            features['min_growth_score'] = 70.0
        
        return features

