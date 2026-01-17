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
import hashlib
import pickle
from pathlib import Path
from bson import ObjectId

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
            # 新增索引：支持缓存查找和查询
            self.db[self.BACKTEST_COLLECTION].create_index([("config_hash", ASCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([
                ("backtest_type", ASCENDING),
                ("config_hash", ASCENDING)
            ], name="idx_type_hash")
            self.db[self.BACKTEST_COLLECTION].create_index([("created_at", DESCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([
                ("start_date", ASCENDING),
                ("end_date", ASCENDING)
            ], name="idx_date_range")
            self.db[self.BACKTEST_COLLECTION].create_index([("backtest_type", ASCENDING)])
            
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
    
    @staticmethod
    def _compute_algorithm_version() -> str:
        """
        计算算法版本（基于SignalBacktester的关键方法代码哈希）
        
        通过读取SignalBacktester类的源代码，提取关键方法，
        计算哈希值作为算法版本标识。
        
        Returns:
            算法版本字符串，格式：v{hash前8位}
        """
        try:
            import inspect
            import sys
            from pathlib import Path
            
            # 导入SignalBacktester类
            from core.signal_backtest import SignalBacktester
            
            # 获取类的源代码
            source = inspect.getsource(SignalBacktester)
            
            # 定义关键方法（影响回测结果的方法）
            key_methods = [
                'run_backtest',
                '_generate_enhanced_signal',
                '_calculate_technical_scores',
                '_calculate_technical_scores_via_trend_analyzer',
                '_calculate_technical_scores_simple'
            ]
            
            # 提取关键方法的代码
            method_code_parts = []
            lines = source.split('\n')
            in_method = False
            current_method = None
            current_code = []
            indent_level = 0
            
            for line in lines:
                # 检查是否是关键方法的定义
                for method_name in key_methods:
                    if f'def {method_name}' in line:
                        # 保存之前的方法代码
                        if current_method and current_code:
                            method_code_parts.append(f"{current_method}:\n" + '\n'.join(current_code))
                        current_method = method_name
                        current_code = [line]
                        in_method = True
                        # 计算初始缩进
                        indent_level = len(line) - len(line.lstrip())
                        break
                else:
                    if in_method:
                        # 检查是否还在当前方法内
                        if line.strip() == '':
                            current_code.append(line)
                        elif line.startswith(' ' * (indent_level + 1)) or line.startswith('\t'):
                            # 仍在方法内
                            current_code.append(line)
                        else:
                            # 方法结束
                            if current_method:
                                method_code_parts.append(f"{current_method}:\n" + '\n'.join(current_code))
                            current_method = None
                            current_code = []
                            in_method = False
            
            # 保存最后一个方法
            if current_method and current_code:
                method_code_parts.append(f"{current_method}:\n" + '\n'.join(current_code))
            
            # 合并所有关键方法的代码
            all_code = '\n\n'.join(method_code_parts)
            
            # 移除注释和空行（简化版，只移除明显的注释行）
            cleaned_lines = []
            for line in all_code.split('\n'):
                stripped = line.strip()
                # 保留非空行和非纯注释行
                if stripped and not stripped.startswith('#'):
                    cleaned_lines.append(line)
            cleaned_code = '\n'.join(cleaned_lines)
            
            # 计算MD5哈希
            code_hash = hashlib.md5(cleaned_code.encode('utf-8')).hexdigest()
            
            # 返回版本字符串（前8位）
            return f"v{code_hash[:8]}"
            
        except Exception as e:
            logger.warning(f"计算算法版本失败，使用legacy版本: {e}")
            # 如果计算失败，返回legacy版本
            return "vlegacy"
    
    @staticmethod
    def _compute_config_hash(config: Dict[str, Any]) -> str:
        """
        计算配置哈希（用于缓存查找）
        
        Args:
            config: 配置字典
            
        Returns:
            MD5哈希字符串
        """
        # 提取关键参数（排除时间戳、随机种子等）
        key_params = {
            k: v for k, v in config.items()
            if k not in ['timestamp', 'random_seed', 'created_at', 'saved_at']
        }
        # 排序后序列化为JSON字符串
        config_str = json.dumps(key_params, sort_keys=True, ensure_ascii=False)
        # 计算MD5哈希
        return hashlib.md5(config_str.encode('utf-8')).hexdigest()
    
    def _convert_numpy_types(self, obj: Any) -> Any:
        """
        递归转换NumPy类型为Python原生类型（MongoDB兼容性）
        
        Args:
            obj: 要转换的对象（可以是dict, list, 或NumPy类型）
            
        Returns:
            转换后的对象
        """
        import numpy as np
        
        if isinstance(obj, dict):
            return {k: self._convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_numpy_types(item) for item in obj)
        elif isinstance(obj, np.bool_):
            # 注意：NumPy 2.0+ 移除了 np.bool8，只使用 np.bool_
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def _extract_result_summary(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取结果摘要（关键指标）
        
        Args:
            result_dict: 完整结果字典
            
        Returns:
            摘要字典
        """
        summary = {}
        # 基本统计
        for key in ['total_signals', 'bullish_signals', 'bearish_signals', 'neutral_signals']:
            if key in result_dict:
                summary[key] = result_dict[key]
        # 准确率
        for key in ['accuracy_5d', 'accuracy_10d', 'accuracy_20d', 'accuracy_60d',
                    'short_accuracy_5d', 'medium_accuracy_20d', 'long_accuracy_60d',
                    'state_accuracy_60d']:
            if key in result_dict:
                summary[key] = result_dict[key]
        # 时间信息
        if 'duration_seconds' in result_dict:
            summary['duration_seconds'] = result_dict['duration_seconds']
        return summary
    
    def save_backtest_result(
        self,
        result: Any,
        config: Dict[str, Any],
        backtest_type: str,
        version_tag: Optional[str] = None,
        use_cache: bool = False
    ) -> Optional[str]:
        """
        保存回测结果（增强版，支持版本标签）
        
        Args:
            result: BacktestResult对象（需有to_dict方法）
            config: 配置字典
            backtest_type: 回测类型（如'signal_phase1', 'signal_phase2'）
            version_tag: 版本标签（可选，用户指定的版本标识）
            use_cache: 是否使用缓存（如果已存在相同配置的结果，则不重复保存，默认False由调用方控制）
            
        Returns:
            结果ID（MongoDB _id的字符串形式），失败返回None
        """
        if not self._connected:
            logger.warning("MongoDB未连接，无法保存回测结果")
            return None
        
        try:
            # 计算配置哈希
            config_hash = self._compute_config_hash(config)
            
            # 计算算法版本（自动计算当前算法版本）
            algorithm_version_val = self._compute_algorithm_version()
            
            # 检查缓存（如果启用）- 需要匹配算法版本和配置
            if use_cache:
                cached = self.find_cached_backtest(config, backtest_type, algorithm_version=algorithm_version_val)
                if cached:
                    logger.info(f"✅ 回测结果已存在（缓存）: {cached['_id']}, 跳过保存")
                    return str(cached['_id'])
            
            # 转换为字典
            if hasattr(result, 'to_dict'):
                result_dict = result.to_dict()
            elif hasattr(result, '__dict__'):
                result_dict = result.__dict__
            else:
                result_dict = result
            
            # 转换NumPy类型为Python原生类型（MongoDB兼容性）
            result_dict = self._convert_numpy_types(result_dict)
            
            # 提取摘要
            summary = self._extract_result_summary(result_dict)
            
            # 获取日期范围
            start_date = config.get('start_date', '')
            end_date = config.get('end_date', '')
            if not start_date and 'config' in result_dict:
                start_date = result_dict['config'].get('start_date', '')
                end_date = result_dict['config'].get('end_date', '')
            
            # 准备文档（algorithm_version_val已在上面计算）
            doc = {
                'backtest_type': backtest_type,
                'config_hash': config_hash,
                'config': config,
                'start_date': start_date,
                'end_date': end_date,
                'created_at': datetime.now().isoformat(),
                'summary': summary,
                'algorithm_version': algorithm_version_val,
                'version_tag': version_tag,  # 用户指定的版本标签（可选）
                'migrated_from': None,  # 迁移来源（如果是从文件迁移的，当前未使用）
            }
            
            # 添加时间信息
            if 'duration_seconds' in result_dict:
                doc['duration_seconds'] = result_dict['duration_seconds']
            if 'backtest_time' in result_dict:
                doc['backtest_time'] = result_dict['backtest_time']
            
            # 检查结果大小（MongoDB文档限制16MB，我们使用10MB作为阈值）
            result_json = json.dumps(result_dict, default=str, ensure_ascii=False)
            result_size = len(result_json.encode('utf-8'))
            
            if result_size > 10 * 1024 * 1024:  # 10MB
                # 结果太大，保存到文件系统
                result_dir = Path("output/backtest_results")
                result_dir.mkdir(parents=True, exist_ok=True)
                result_id = ObjectId()
                result_file = result_dir / f"{result_id}.pkl"
                
                # 使用最高协议版本以兼容numpy 2.4+（避免deprecation警告）
                with open(result_file, 'wb') as f:
                    pickle.dump(result_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
                
                doc['file_path'] = str(result_file)
                doc['file_size'] = result_size
                doc['result_data'] = None  # 不存储完整数据
                logger.info(f"回测结果较大({result_size / 1024 / 1024:.1f}MB)，保存到文件: {result_file}")
            else:
                # 直接存储在MongoDB中
                doc['result_data'] = result_dict
                doc['file_path'] = None
                doc['file_size'] = result_size
            
            # 保存到MongoDB（使用upsert避免重复记录）
            # 基于 backtest_type + config_hash + algorithm_version 唯一标识
            filter_query = {
                'backtest_type': backtest_type,
                'config_hash': config_hash,
                'algorithm_version': algorithm_version_val
            }
            
            # 确保整个文档中所有NumPy类型都被转换（包括config、summary等）
            doc = self._convert_numpy_types(doc)
            
            # 使用 replace_one 的 upsert 模式：
            # - 如果存在匹配记录，替换（更新）
            # - 如果不存在，插入新记录
            result_obj = self.db[self.BACKTEST_COLLECTION].replace_one(
                filter_query,
                doc,
                upsert=True
            )
            
            # 获取结果ID
            if result_obj.upserted_id:
                result_id = str(result_obj.upserted_id)
                logger.info(f"✅ 已保存新回测结果: {backtest_type}, ID={result_id}, config_hash={config_hash[:8]}...")
            else:
                # 更新了已有记录，需要查询获取ID
                existing = self.db[self.BACKTEST_COLLECTION].find_one(filter_query)
                result_id = str(existing['_id']) if existing else None
                logger.info(f"✅ 已更新回测结果: {backtest_type}, ID={result_id}, config_hash={config_hash[:8]}...")
            return result_id
            
        except Exception as e:
            logger.error(f"保存回测结果失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def find_cached_backtest(
        self,
        config: Dict[str, Any],
        backtest_type: str,
        algorithm_version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        基于配置哈希查找缓存的结果
        
        Args:
            config: 配置字典
            backtest_type: 回测类型
            algorithm_version: 算法版本（可选，如果提供则匹配版本）
            
        Returns:
            缓存的文档（包含_id），未找到返回None
        """
        if not self._connected:
            return None
        
        try:
            config_hash = self._compute_config_hash(config)
            
            # 构建查询条件
            query = {
                'backtest_type': backtest_type,
                'config_hash': config_hash
            }
            
            # 如果指定了算法版本，也需要匹配
            if algorithm_version:
                query['algorithm_version'] = algorithm_version
            
            doc = self.db[self.BACKTEST_COLLECTION].find_one(
                query, 
                sort=[("created_at", DESCENDING)]
            )
            
            if doc:
                # 保留_id用于后续加载
                doc['_id'] = str(doc['_id'])
                return doc
            
            return None
            
        except Exception as e:
            logger.error(f"查找缓存失败: {e}")
            return None
    
    def load_backtest_result(self, result_id: str) -> Optional[Any]:
        """
        加载完整的回测结果
        
        Args:
            result_id: 结果ID（MongoDB _id的字符串形式）
            
        Returns:
            EnhancedBacktestResult对象或字典，失败返回None
        """
        if not self._connected:
            return None
        
        try:
            doc = self.db[self.BACKTEST_COLLECTION].find_one({'_id': ObjectId(result_id)})
            if not doc:
                logger.warning(f"未找到回测结果: {result_id}")
                return None
            
            # 从文件系统或MongoDB加载完整结果
            if doc.get('file_path'):
                # 从文件加载（抑制pandas内部的deprecation警告）
                result_file = Path(doc['file_path'])
                if result_file.exists():
                    import warnings
                    with warnings.catch_warnings():
                        # 临时抑制pandas内部pickle兼容处理的deprecation警告
                        warnings.filterwarnings('ignore', category=DeprecationWarning, 
                                                module='pandas.compat.pickle_compat')
                        with open(result_file, 'rb') as f:
                            result_dict = pickle.load(f)
                else:
                    logger.error(f"结果文件不存在: {result_file}")
                    return None
            else:
                # 从MongoDB加载
                result_dict = doc.get('result_data')
                if not result_dict:
                    logger.warning(f"结果数据为空: {result_id}")
                    return None
            
            # 尝试转换为EnhancedBacktestResult对象
            try:
                from core.signal_backtest import EnhancedBacktestResult, BacktestConfig
                # 重建config对象
                config_dict = doc.get('config', {})
                config = BacktestConfig(**config_dict) if config_dict else BacktestConfig()
                # 重建result对象
                result_dict['config'] = config
                result = EnhancedBacktestResult(**result_dict)
                result._from_cache = True  # 标记来自缓存
                return result
            except Exception as e:
                logger.debug(f"无法转换为EnhancedBacktestResult对象，返回字典: {e}")
                result_dict['_from_cache'] = True
                return result_dict
            
        except Exception as e:
            logger.error(f"加载回测结果失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def query_backtest_results(
        self,
        backtest_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        algorithm_version: Optional[str] = None,
        limit: int = 100,
        sort_by: str = 'created_at',
        sort_order: int = DESCENDING
    ) -> List[Dict[str, Any]]:
        """
        查询回测结果
        
        Args:
            backtest_type: 回测类型（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            algorithm_version: 算法版本（可选）
            limit: 返回结果数量限制
            sort_by: 排序字段
            sort_order: 排序顺序（DESCENDING或ASCENDING）
            
        Returns:
            结果列表（只包含元数据和摘要，不包含完整结果数据）
        """
        if not self._connected:
            return []
        
        try:
            query = {}
            if backtest_type:
                query['backtest_type'] = backtest_type
            if algorithm_version:
                query['algorithm_version'] = algorithm_version
            if start_date or end_date:
                date_query = {}
                if start_date:
                    date_query['$gte'] = start_date
                if end_date:
                    date_query['$lte'] = end_date
                query['start_date'] = date_query
            
            cursor = self.db[self.BACKTEST_COLLECTION].find(
                query,
                {
                    'result_data': 0  # 排除完整结果数据，只返回元数据和摘要
                }
            ).sort([(sort_by, sort_order)]).limit(limit)
            
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"查询回测结果失败: {e}")
            return []
    
    def list_backtest_results(
        self,
        backtest_type: Optional[str] = None,
        limit: int = 10,
        sort_by: str = 'created_at'
    ) -> List[Dict[str, Any]]:
        """
        列出回测结果（便捷方法）
        
        Args:
            backtest_type: 回测类型（可选）
            limit: 返回结果数量
            sort_by: 排序字段
            
        Returns:
            结果列表
        """
        return self.query_backtest_results(
            backtest_type=backtest_type,
            limit=limit,
            sort_by=sort_by
        )
    
    def delete_backtest_result(self, result_id: str) -> bool:
        """
        删除回测结果
        
        Args:
            result_id: 结果ID
            
        Returns:
            是否成功
        """
        if not self._connected:
            return False
        
        try:
            doc = self.db[self.BACKTEST_COLLECTION].find_one({'_id': ObjectId(result_id)})
            if not doc:
                logger.warning(f"未找到回测结果: {result_id}")
                return False
            
            # 如果结果存储在文件中，删除文件
            if doc.get('file_path'):
                result_file = Path(doc['file_path'])
                if result_file.exists():
                    try:
                        result_file.unlink()
                        logger.info(f"已删除结果文件: {result_file}")
                    except Exception as e:
                        logger.warning(f"删除结果文件失败: {e}")
            
            # 从MongoDB删除
            self.db[self.BACKTEST_COLLECTION].delete_one({'_id': ObjectId(result_id)})
            logger.info(f"✅ 已删除回测结果: {result_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除回测结果失败: {e}")
            return False
    
    def list_results_by_version(
        self,
        backtest_type: Optional[str] = None,
        algorithm_version: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        按版本列出回测结果
        
        Args:
            backtest_type: 回测类型（可选）
            algorithm_version: 算法版本（可选）
            limit: 返回结果数量限制
            
        Returns:
            结果列表（按创建时间排序）
        """
        return self.query_backtest_results(
            backtest_type=backtest_type,
            algorithm_version=algorithm_version,
            limit=limit,
            sort_by='created_at'
        )
    
    def compare_versions(
        self,
        result_id1: str,
        result_id2: str
    ) -> Optional[Dict[str, Any]]:
        """
        比较两个版本的回测结果
        
        Args:
            result_id1: 结果ID 1
            result_id2: 结果ID 2
            
        Returns:
            比较结果字典，失败返回None
        """
        if not self._connected:
            return None
        
        try:
            doc1 = self.db[self.BACKTEST_COLLECTION].find_one({'_id': ObjectId(result_id1)})
            doc2 = self.db[self.BACKTEST_COLLECTION].find_one({'_id': ObjectId(result_id2)})
            
            if not doc1 or not doc2:
                logger.warning("无法找到要比较的结果")
                return None
            
            summary1 = doc1.get('summary', {})
            summary2 = doc2.get('summary', {})
            
            # 比较关键指标
            metrics = [
                'accuracy_5d', 'accuracy_10d', 'accuracy_20d', 'accuracy_60d',
                'short_accuracy_5d', 'medium_accuracy_20d', 'long_accuracy_60d',
                'state_accuracy_60d',
                'total_signals', 'bullish_signals', 'bearish_signals', 'neutral_signals',
                'duration_seconds'
            ]
            
            metrics_diff = {}
            for metric in metrics:
                v1 = summary1.get(metric, 0)
                v2 = summary2.get(metric, 0)
                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    diff = v2 - v1
                    metrics_diff[metric] = {
                        'v1': v1,
                        'v2': v2,
                        'diff': diff
                    }
            
            # 生成摘要
            accuracy_improvements = []
            if 'accuracy_5d' in metrics_diff:
                diff = metrics_diff['accuracy_5d']['diff']
                if diff > 0:
                    accuracy_improvements.append(f"5日准确率提升{diff:.1f}%")
                elif diff < 0:
                    accuracy_improvements.append(f"5日准确率下降{abs(diff):.1f}%")
            
            if 'accuracy_20d' in metrics_diff:
                diff = metrics_diff['accuracy_20d']['diff']
                if diff > 0:
                    accuracy_improvements.append(f"20日准确率提升{diff:.1f}%")
                elif diff < 0:
                    accuracy_improvements.append(f"20日准确率下降{abs(diff):.1f}%")
            
            summary_text = '; '.join(accuracy_improvements) if accuracy_improvements else '关键指标变化较小'
            
            return {
                'version1': {
                    'algorithm_version': doc1.get('algorithm_version', 'unknown'),
                    'version_tag': doc1.get('version_tag'),
                    'result_id': str(doc1['_id']),
                    'created_at': doc1.get('created_at', '')
                },
                'version2': {
                    'algorithm_version': doc2.get('algorithm_version', 'unknown'),
                    'version_tag': doc2.get('version_tag'),
                    'result_id': str(doc2['_id']),
                    'created_at': doc2.get('created_at', '')
                },
                'metrics_diff': metrics_diff,
                'summary': summary_text
            }
            
        except Exception as e:
            logger.error(f"比较版本失败: {e}")
            return None
    
    def get_latest_version(
        self,
        backtest_type: str,
        config_hash: str,
        algorithm_version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        获取指定配置的最新版本结果
        
        Args:
            backtest_type: 回测类型
            config_hash: 配置哈希
            algorithm_version: 算法版本（如果为None，返回任意版本的最新结果）
            
        Returns:
            最新结果文档，未找到返回None
        """
        if not self._connected:
            return None
        
        try:
            query = {
                'backtest_type': backtest_type,
                'config_hash': config_hash
            }
            if algorithm_version:
                query['algorithm_version'] = algorithm_version
            
            doc = self.db[self.BACKTEST_COLLECTION].find_one(
                query,
                sort=[("created_at", DESCENDING)]
            )
            
            if doc:
                doc['_id'] = str(doc['_id'])
                return doc
            
            return None
            
        except Exception as e:
            logger.error(f"获取最新版本失败: {e}")
            return None
    
    def save_backtest_result_legacy(self, result) -> bool:
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

