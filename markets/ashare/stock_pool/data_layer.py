"""
三层数据保障架构

一级：实时API层（AKShare，限频使用）
二级：缓存层（JSON/MongoDB，默认读取）
三级：机构级数据源（JQData接口预留）

使用优先级：缓存 → API → JQData
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)

# 数据目录
CACHE_DIR = Path.home() / ".local/share/trquant/cache"
DATA_DIR = Path.home() / ".local/share/trquant/data"

# 确保目录存在
CACHE_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "themes").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "stock_pool").mkdir(parents=True, exist_ok=True)


@dataclass
class CacheConfig:
    """缓存配置"""
    # 各类数据的缓存有效期（小时）
    sector_members: int = 24      # 板块成分股：每日更新
    stock_spot: int = 1           # 行情快照：每小时
    dragon_tiger: int = 24        # 龙虎榜：每日
    northbound: int = 4           # 北向资金：4小时
    limit_up: int = 4             # 涨停板：4小时
    themes: int = 24              # 主线数据：每日


class DataSourceStatus:
    """数据源状态监控"""
    
    _status = {
        "akshare": {"available": True, "last_check": None, "fail_count": 0},
        "jqdata": {"available": False, "last_check": None, "fail_count": 0},   # 聚宽（已集成，按需启用）
        "tushare": {"available": False, "last_check": None, "fail_count": 0},  # TuShare Pro（折衷方案）
        "cache": {"available": True, "last_check": None, "fail_count": 0},
    }
    
    @classmethod
    def mark_failed(cls, source: str):
        """标记数据源失败"""
        if source in cls._status:
            cls._status[source]["fail_count"] += 1
            if cls._status[source]["fail_count"] >= 3:
                cls._status[source]["available"] = False
                logger.warning(f"⚠️ 数据源 {source} 连续失败3次，标记为不可用")
    
    @classmethod
    def mark_success(cls, source: str):
        """标记数据源成功"""
        if source in cls._status:
            cls._status[source]["available"] = True
            cls._status[source]["fail_count"] = 0
            cls._status[source]["last_check"] = datetime.now().isoformat()
    
    @classmethod
    def is_available(cls, source: str) -> bool:
        """检查数据源是否可用"""
        return cls._status.get(source, {}).get("available", False)
    
    @classmethod
    def get_status(cls) -> Dict:
        """获取所有数据源状态"""
        return cls._status.copy()


class CacheManager:
    """
    缓存管理器
    
    提供统一的缓存读写接口，支持JSON和MongoDB
    """
    
    def __init__(self):
        self.config = CacheConfig()
        self._mongo_client = None
        self._mongo_db = None
        self._init_mongo()
    
    def _init_mongo(self):
        """初始化MongoDB连接"""
        try:
            from pymongo import MongoClient
            self._mongo_client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
            self._mongo_db = self._mongo_client.jqquant
            # 测试连接
            self._mongo_client.server_info()
            logger.info("✅ MongoDB连接成功")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB连接失败: {e}，使用JSON缓存")
            self._mongo_db = None
    
    def _get_cache_key(self, data_type: str, identifier: str = "") -> str:
        """生成缓存键"""
        return f"{data_type}_{identifier}" if identifier else data_type
    
    def _get_cache_file(self, data_type: str, identifier: str = "") -> Path:
        """获取缓存文件路径"""
        filename = self._get_cache_key(data_type, identifier)
        # 对过长的标识符进行哈希
        if len(filename) > 100:
            filename = f"{data_type}_{hashlib.md5(identifier.encode()).hexdigest()}"
        return CACHE_DIR / f"{filename}.json"
    
    def _is_cache_valid(self, data_type: str, cache_time: str) -> bool:
        """检查缓存是否有效"""
        try:
            cache_dt = datetime.fromisoformat(cache_time)
            ttl_hours = getattr(self.config, data_type, 24)
            return datetime.now() - cache_dt < timedelta(hours=ttl_hours)
        except:
            return False
    
    # ============================================================
    # JSON缓存操作
    # ============================================================
    
    def save_to_json(self, data_type: str, data: Any, identifier: str = ""):
        """保存到JSON文件"""
        filepath = self._get_cache_file(data_type, identifier)
        cache_data = {
            "_meta": {
                "data_type": data_type,
                "identifier": identifier,
                "cache_time": datetime.now().isoformat(),
                "source": "cache"
            },
            "data": data
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2, default=str)
        logger.debug(f"缓存已保存: {filepath}")
    
    def load_from_json(self, data_type: str, identifier: str = "") -> Optional[Any]:
        """从JSON文件加载"""
        filepath = self._get_cache_file(data_type, identifier)
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 检查有效期
            cache_time = cache_data.get("_meta", {}).get("cache_time", "")
            if not self._is_cache_valid(data_type, cache_time):
                logger.debug(f"缓存已过期: {filepath}")
                return None
            
            return cache_data.get("data")
        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
            return None
    
    # ============================================================
    # MongoDB缓存操作
    # ============================================================
    
    def save_to_mongo(self, collection: str, data: Dict, identifier: str = ""):
        """保存到MongoDB"""
        if self._mongo_db is None:
            return False
        
        try:
            doc = {
                **data,
                "_cache_time": datetime.now(),
                "_identifier": identifier
            }
            # 使用upsert
            self._mongo_db[collection].update_one(
                {"_identifier": identifier} if identifier else {},
                {"$set": doc},
                upsert=True
            )
            return True
        except Exception as e:
            logger.warning(f"MongoDB保存失败: {e}")
            return False
    
    def load_from_mongo(self, collection: str, identifier: str = "") -> Optional[Dict]:
        """从MongoDB加载"""
        if self._mongo_db is None:
            return None
        
        try:
            query = {"_identifier": identifier} if identifier else {}
            doc = self._mongo_db[collection].find_one(query)
            if doc:
                # 检查有效期
                cache_time = doc.get("_cache_time")
                if cache_time and isinstance(cache_time, datetime):
                    ttl_hours = getattr(self.config, collection, 24)
                    if datetime.now() - cache_time < timedelta(hours=ttl_hours):
                        return doc
            return None
        except Exception as e:
            logger.warning(f"MongoDB读取失败: {e}")
            return None
    
    # ============================================================
    # 统一接口
    # ============================================================
    
    def save(self, data_type: str, data: Any, identifier: str = ""):
        """统一保存接口（同时写入JSON和MongoDB）"""
        self.save_to_json(data_type, data, identifier)
        if isinstance(data, dict):
            self.save_to_mongo(data_type, data, identifier)
    
    def load(self, data_type: str, identifier: str = "") -> Optional[Any]:
        """统一加载接口（优先MongoDB，其次JSON）"""
        # 优先MongoDB
        data = self.load_from_mongo(data_type, identifier)
        if data:
            DataSourceStatus.mark_success("cache")
            return data
        
        # 其次JSON
        data = self.load_from_json(data_type, identifier)
        if data:
            DataSourceStatus.mark_success("cache")
            return data
        
        return None


class ThemeDataManager:
    """
    主线数据管理器
    
    负责主线识别结果的存储和读取，包含完整的成员股信息
    
    数据结构：
    {
        "name": "军工电子",
        "total_score": 89.3,
        "scores": {"heat": 81.2, "momentum": 92.3, ...},
        "leader_stock": "宏达电子",
        "leader_change": 14.31,
        "stock_members": [
            {"symbol": "002865.SZ", "name": "钧达股份"},
            ...
        ],
        "update_time": "2025-11-30T09:00:00"
    }
    """
    
    def __init__(self):
        self.cache = CacheManager()
        self.themes_file = DATA_DIR / "themes" / "themes_latest.json"
        self.members_file = DATA_DIR / "themes" / "themes_member_mapping.json"
    
    def save_themes(self, themes: List[Dict]):
        """
        保存主线数据（包含成员股）
        
        这是主线识别模块输出的接口
        """
        # 确保每个主线都有members字段
        for theme in themes:
            if "stock_members" not in theme:
                theme["stock_members"] = []
            theme["update_time"] = datetime.now().isoformat()
        
        # 保存完整主线数据
        themes_data = {
            "timestamp": datetime.now().isoformat(),
            "count": len(themes),
            "themes": themes
        }
        
        with open(self.themes_file, 'w', encoding='utf-8') as f:
            json.dump(themes_data, f, ensure_ascii=False, indent=2)
        
        # 保存成员映射（便于快速查询）
        member_mapping = {}
        for theme in themes:
            name = theme.get("name", "")
            if name:
                member_mapping[name] = theme.get("stock_members", [])
        
        with open(self.members_file, 'w', encoding='utf-8') as f:
            json.dump(member_mapping, f, ensure_ascii=False, indent=2)
        
        # 同时保存到MongoDB
        self.cache.save_to_mongo("themes", themes_data, "latest")
        
        logger.info(f"✅ 主线数据已保存: {len(themes)} 个主线")
    
    def load_themes(self) -> List[Dict]:
        """加载主线数据"""
        # 优先从MongoDB读取
        data = self.cache.load_from_mongo("themes", "latest")
        if data and "themes" in data:
            return data["themes"]
        
        # 其次从JSON读取
        if self.themes_file.exists():
            with open(self.themes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("themes", [])
        
        return []
    
    def get_theme_members(self, theme_name: str) -> List[Dict]:
        """获取主线的成员股"""
        # 优先从映射文件读取
        if self.members_file.exists():
            with open(self.members_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
                if theme_name in mapping:
                    return mapping[theme_name]
        
        # 其次从完整数据中查找
        themes = self.load_themes()
        for theme in themes:
            if theme.get("name") == theme_name:
                return theme.get("stock_members", [])
        
        return []
    
    def get_all_leader_stocks(self) -> List[Dict]:
        """获取所有主线的龙头股"""
        themes = self.load_themes()
        leaders = []
        for theme in themes:
            if theme.get("leader_stock"):
                leaders.append({
                    "name": theme["leader_stock"],
                    "theme": theme["name"],
                    "theme_score": theme.get("total_score", 0),
                    "change": theme.get("leader_change", 0)
                })
        return leaders


class SectorMemberCache:
    """
    板块成分股缓存
    
    为每个板块/概念维护成分股列表
    """
    
    def __init__(self):
        self.cache = CacheManager()
        self.cache_dir = CACHE_DIR / "sector_members"
        self.cache_dir.mkdir(exist_ok=True)
    
    def save_members(self, sector_name: str, sector_type: str, members: List[Dict]):
        """保存板块成分股"""
        data = {
            "sector_name": sector_name,
            "sector_type": sector_type,
            "count": len(members),
            "members": members,
            "update_time": datetime.now().isoformat()
        }
        
        filepath = self.cache_dir / f"{sector_type}_{sector_name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"板块成分股已缓存: {sector_name} ({len(members)} 只)")
    
    def load_members(self, sector_name: str, sector_type: str = "") -> List[Dict]:
        """加载板块成分股"""
        # 尝试指定类型
        if sector_type:
            filepath = self.cache_dir / f"{sector_type}_{sector_name}.json"
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("members", [])
        
        # 尝试所有类型
        for st in ["concept", "industry"]:
            filepath = self.cache_dir / f"{st}_{sector_name}.json"
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("members", [])
        
        return []
    
    def get_all_cached_sectors(self) -> List[str]:
        """获取所有已缓存的板块名称"""
        sectors = []
        for f in self.cache_dir.glob("*.json"):
            name = f.stem.split("_", 1)[-1]
            sectors.append(name)
        return sectors


# ============================================================
# TuShare Pro 数据提供者（折衷方案）
# ============================================================


class TuShareProvider:
    """
    TuShare Pro 数据提供者
    
    用途：
    - 在未购买JQData/Wind之前，提供低成本的日线行情和基础数据
    - 主要服务于：技术突破扫描、候选池构建、验证算法
    
    设计原则：
    - 初始化失败不影响主流程（自动降级为缓存/模拟数据）
    - 所有异常内部消化，通过 DataSourceStatus 记录状态
    """
    
    def __init__(self):
        self.available = False
        self.pro = None
        self._try_init()
    
    def _try_init(self):
        """尝试初始化 TuShare Pro"""
        try:
            import tushare as ts  # type: ignore
        except ImportError:
            logger.debug("TuShare 未安装，跳过折衷数据源初始化")
            DataSourceStatus.mark_failed("tushare")
            return
        
        # 读取配置文件（主项目 / 本地安装 / 当前项目）
        config_paths = [
            Path("/home/taotao/dev/QuantTest/TRQuant/config/tushare_config.json"),
            Path.home() / ".local/share/trquant/config/tushare_config.json",
            Path(__file__).parent.parent.parent.parent / "config" / "tushare_config.json",
        ]
        
        ts_config = None
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        ts_config = json.load(f)
                    logger.debug(f"从 {config_path} 读取 TuShare 配置")
                    break
                except Exception as e:
                    logger.debug(f"读取 TuShare 配置失败 {config_path}: {e}")
        
        token = ts_config.get("token") if isinstance(ts_config, dict) else None
        username = ts_config.get("username", "") if isinstance(ts_config, dict) else ""
        
        if not token:
            logger.debug("未找到 TuShare token，折衷数据源暂不可用")
            DataSourceStatus.mark_failed("tushare")
            return
        
        try:
            # TuShare官方用法：先set_token，再pro_api()
            ts.set_token(token)
            self.pro = ts.pro_api()
            
            # 测试接口权限：尝试获取交易日历（通常是最基础的接口）
            from datetime import datetime, timedelta
            today = datetime.now()
            test_date = today.strftime("%Y%m%d")
            
            try:
                # 测试获取交易日历（基础接口）
                cal = self.pro.trade_cal(exchange='SSE', start_date=test_date, end_date=test_date)
                if cal is not None and not cal.empty:
                    # 权限测试通过，继续测试日线数据接口
                    for i in range(5):
                        test_date = (today - timedelta(days=i)).strftime("%Y%m%d")
                        try:
                            daily = self.pro.daily(trade_date=test_date)
                            if daily is not None and not daily.empty:
                                self.available = True
                                DataSourceStatus.mark_success("tushare")
                                logger.info(f"✅ TuShare Pro 初始化成功（测试日期：{test_date}，{len(daily)} 条数据）")
                                return
                        except Exception as e:
                            error_msg = str(e)
                            if "权限" in error_msg or "积分" in error_msg:
                                # 权限不足，给出明确提示
                                logger.warning(f"⚠️ TuShare Pro 接口权限不足: {error_msg}")
                                logger.warning(f"   请登录 https://tushare.pro 查看积分和权限")
                                if username:
                                    logger.warning(f"   账户: {username}，请完成新手任务获取积分或购买会员")
                                self.available = False
                                DataSourceStatus.mark_failed("tushare")
                                return
                            logger.debug(f"TuShare测试日期{test_date}失败: {error_msg[:100]}")
                            continue
                    
                    # 如果所有日期都失败，但pro_api创建成功，仍然标记为可用（可能是非交易日）
                    self.available = True
                    DataSourceStatus.mark_success("tushare")
                    logger.info("✅ TuShare Pro 初始化成功（折衷数据源就绪，当前可能非交易日）")
                else:
                    logger.warning("⚠️ TuShare Pro 返回空数据，可能权限不足")
                    self.available = False
                    DataSourceStatus.mark_failed("tushare")
            except Exception as e:
                error_msg = str(e)
                if "权限" in error_msg or "积分" in error_msg:
                    # 权限不足，给出明确提示
                    logger.warning(f"⚠️ TuShare Pro 接口权限不足: {error_msg}")
                    logger.warning(f"   请登录 https://tushare.pro 查看积分和权限")
                    if username:
                        logger.warning(f"   账户: {username}，请完成新手任务获取积分或购买会员")
                else:
                    logger.warning(f"⚠️ TuShare Pro 初始化失败: {error_msg}")
                self.available = False
                DataSourceStatus.mark_failed("tushare")
            
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"⚠️ TuShare Pro 初始化失败: {error_msg}")
            self.available = False
            DataSourceStatus.mark_failed("tushare")
    
    def get_stock_spot_like(self):
        """
        获取接近 AKShare stock_zh_a_spot_em 结构的 DataFrame
        
        返回列：
        - 代码: 6位股票代码
        - 名称: 股票名称
        - 涨跌幅: pct_chg
        - 量比: 默认 1.0（TuShare不直接提供）
        - 换手率: turnover_rate
        - 总市值: 按 float_mv 估算（单位：元）
        """
        if not self.available or self.pro is None:
            return None
        
        try:
            import pandas as pd  # type: ignore  # noqa: F401
            from datetime import datetime, timedelta
        except ImportError:
            logger.debug("pandas 未安装，无法使用 TuShare 折衷数据源")
            return None
        
        try:
            today = datetime.now().date()
            daily = None
            basic = None
            mv = None
            
            # 尝试最近 5 个自然日，找到最近一个有成交数据的交易日
            for i in range(5):
                d = today - timedelta(days=i)
                trade_date = d.strftime("%Y%m%d")
                try:
                    daily = self.pro.daily(trade_date=trade_date)
                    if daily is not None and not daily.empty:
                        try:
                            basic = self.pro.stock_basic(
                                exchange="",
                                list_status="L",
                                fields="ts_code,name"
                            )
                        except Exception as e:
                            error_msg = str(e)
                            if "权限" in error_msg or "积分" in error_msg:
                                logger.warning(f"⚠️ TuShare Pro stock_basic 接口权限不足")
                                basic = None
                            else:
                                logger.debug(f"TuShare stock_basic 失败: {error_msg[:100]}")
                                basic = None
                        
                        try:
                            mv = self.pro.daily_basic(
                                trade_date=trade_date,
                                fields="ts_code,turnover_rate,float_mv"
                            )
                        except Exception as e:
                            error_msg = str(e)
                            if "权限" in error_msg or "积分" in error_msg:
                                logger.warning(f"⚠️ TuShare Pro daily_basic 接口权限不足")
                                mv = None
                            else:
                                logger.debug(f"TuShare daily_basic 失败: {error_msg[:100]}")
                                mv = None
                        
                        logger.info(f"✅ TuShare 获取日行情: {trade_date}，{len(daily)} 条")
                        break
                except Exception as e:
                    error_msg = str(e)
                    if "权限" in error_msg or "积分" in error_msg:
                        # 权限不足，标记为不可用并返回
                        logger.warning(f"⚠️ TuShare Pro daily 接口权限不足: {error_msg}")
                        logger.warning(f"   请登录 https://tushare.pro 查看积分和权限")
                        self.available = False
                        DataSourceStatus.mark_failed("tushare")
                        return None
                    logger.debug(f"TuShare 获取 {trade_date} 行情失败: {error_msg[:100]}")
                    continue
            
            if daily is None or daily.empty:
                logger.warning("TuShare 未能获取到最近交易日行情")
                DataSourceStatus.mark_failed("tushare")
                return None
            
            df = daily.copy()
            if basic is not None and not basic.empty:
                df = df.merge(basic, on="ts_code", how="left")
            if mv is not None and not mv.empty:
                df = df.merge(mv, on="ts_code", how="left")
            
            def _to_symbol(ts_code: str) -> str:
                if not isinstance(ts_code, str):
                    return ""
                return ts_code.split(".")[0]
            
            df["代码"] = df["ts_code"].apply(_to_symbol)
            if "name" in df.columns:
                df["名称"] = df["name"]
            else:
                df["名称"] = df["代码"]
            
            df["涨跌幅"] = df.get("pct_chg", 0.0)
            df["换手率"] = df.get("turnover_rate", 0.0)
            float_mv = df.get("float_mv", 0.0).fillna(0.0)
            # float_mv 单位为万元，这里换算为元
            df["总市值"] = float_mv * 10000 * 10000
            df["量比"] = 1.0  # TuShare暂无量比，这里统一设置为1.0
            
            keep_cols = ["代码", "名称", "涨跌幅", "量比", "换手率", "总市值"]
            df = df[keep_cols]
            
            DataSourceStatus.mark_success("tushare")
            return df
        except Exception as e:
            logger.warning(f"TuShare 生成快照失败: {e}")
            DataSourceStatus.mark_failed("tushare")
            return None


# ============================================================
# JQData接口预留（待购买后启用）
# ============================================================

class JQDataProvider:
    """
    JQData数据提供者
    
    聚宽（JQData）提供的接口：
    - get_industries(): 获取行业列表
    - get_concepts(): 获取概念列表
    - get_industry_stocks(industry_code): 行业成分股
    - get_concept_stocks(concept_code): 概念成分股
    - get_price(security, ...): 历史/实时行情
    - get_money_flow(security, ...): 资金流向
    
    使用前需要：
    1. 注册聚宽账号
    2. pip install jqdatasdk
    3. jq.auth(username, password)
    
    支持两种模式：
    - 历史模式（免费版）：只能获取3个月前~1年前的数据
    - 实时模式（付费版）：可获取实时数据
    """
    
    def __init__(self):
        self.available = False
        self.jq = None
        self.permission_start_date = None  # 权限开始日期
        self.permission_end_date = None    # 权限结束日期
        self.is_realtime = False           # 是否支持实时数据
        self._try_init()
    
    def _try_init(self):
        """尝试初始化JQData"""
        try:
            import jqdatasdk as jq
            self.jq = jq
            
            # 尝试从配置文件读取账号信息并自动认证
            # 优先从主项目目录读取，其次从.local目录读取
            config_paths = [
                Path("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json"),
                Path.home() / ".local/share/trquant/config/jqdata_config.json",
                Path(__file__).parent.parent.parent.parent / "config" / "jqdata_config.json"
            ]
            
            jq_config = None
            for config_path in config_paths:
                if config_path.exists():
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            import json
                            jq_config = json.load(f)
                        logger.debug(f"从 {config_path} 读取JQData配置")
                        break
                    except Exception as e:
                        logger.debug(f"读取配置文件失败 {config_path}: {e}")
            
            if jq_config:
                username = jq_config.get("username")
                password = jq_config.get("password")
                
                if username and password:
                    logger.info(f"🔐 从配置文件读取JQData账号，尝试自动认证...")
                    try:
                        jq.auth(username, password)
                        self.available = True
                        logger.info("✅ JQData自动认证成功！")
                        # 检测权限范围
                        self._detect_permission()
                        return
                    except Exception as e:
                        logger.warning(f"⚠️ JQData自动认证失败: {e}")
                        logger.warning("   请检查账号密码是否正确")
                else:
                    logger.debug("JQData配置文件缺少账号信息")
            else:
                logger.debug("未找到JQData配置文件")
            
            # 如果没有配置文件或认证失败，检查是否已手动认证
            try:
                # 尝试获取一个测试数据
                test = jq.get_all_securities(types=['stock'], date=None)
                if test is not None:
                    self.available = True
                    logger.info("✅ JQData已认证并可用")
            except Exception as e:
                if "auth" in str(e).lower() or "login" in str(e).lower():
                    logger.warning("⚠️ JQData需要认证，请检查配置文件或手动调用 jq.auth()")
                else:
                    logger.debug(f"JQData初始化检查: {e}")
                    
        except ImportError:
            logger.debug("JQData未安装")
            self.available = False
    
    def _detect_permission(self):
        """
        检测账号数据权限范围
        
        通过尝试获取数据并解析错误信息来确定权限范围
        """
        if not self.jq:
            return
        
        import re
        from datetime import date, timedelta
        
        logger.info("🔍 检测JQData账号权限范围...")
        
        try:
            # 尝试获取今天的数据
            today = date.today().strftime('%Y-%m-%d')
            yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            try:
                test_data = self.jq.get_price(
                    '000001.XSHE',
                    start_date=yesterday,
                    end_date=today,
                    frequency='daily',
                    fields=['close']
                )
                
                if test_data is not None and len(test_data) > 0:
                    self.is_realtime = True
                    self.permission_end_date = today
                    self.permission_start_date = (date.today() - timedelta(days=365*5)).strftime('%Y-%m-%d')
                    logger.info(f"✅ 实时账号权限: {self.permission_start_date} 至 {self.permission_end_date}")
                    return
            except Exception as e:
                error_msg = str(e)
                if "账号权限仅能获取" in error_msg:
                    date_pattern = r'(\d{4}-\d{2}-\d{2})'
                    dates = re.findall(date_pattern, error_msg)
                    if len(dates) >= 2:
                        self.permission_start_date = dates[0]
                        self.permission_end_date = dates[1]
                        self.is_realtime = False
                        logger.info(f"📅 历史账号权限: {self.permission_start_date} 至 {self.permission_end_date}")
                        return
            
            # 默认设置
            self.permission_start_date = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')
            self.permission_end_date = (date.today() - timedelta(days=90)).strftime('%Y-%m-%d')
            self.is_realtime = False
            logger.warning(f"⚠️ 使用默认权限范围: {self.permission_start_date} 至 {self.permission_end_date}")
            
        except Exception as e:
            logger.error(f"权限检测失败: {e}")
    
    def get_available_date(self) -> str:
        """获取权限范围内的最新可用日期"""
        if self.is_realtime:
            from datetime import date
            return date.today().strftime('%Y-%m-%d')
        elif self.permission_end_date:
            return self.permission_end_date
        else:
            return '2025-08-28'  # 默认
    
    def get_permission_info(self) -> dict:
        """获取权限信息"""
        return {
            'start_date': self.permission_start_date,
            'end_date': self.permission_end_date,
            'is_realtime': self.is_realtime,
            'mode': '实时模式' if self.is_realtime else '历史模式'
        }
    
    def auth(self, username: str, password: str) -> bool:
        """
        认证JQData
        
        Args:
            username: 聚宽用户名
            password: 聚宽密码
            
        Returns:
            是否认证成功
        """
        if not self.jq:
            logger.error("JQData未安装")
            return False
        
        try:
            self.jq.auth(username, password)
            self.available = True
            logger.info("✅ JQData认证成功")
            # 检测权限范围
            self._detect_permission()
            return True
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            self.available = False
            return False
    
    def get_industry_stocks(self, industry_code: str, date: str = None) -> List[Dict]:
        """
        获取行业成分股
        
        Args:
            industry_code: 行业代码（如 'jq.industry_sw_l1'）
            date: 日期 'YYYY-MM-DD'，默认使用权限范围内的最新日期
            
        Returns:
            股票列表 [{"symbol": "000001.XSHE", "name": "平安银行"}, ...]
        """
        if not self.available or not self.jq:
            return []
        
        try:
            # 如果没有指定日期，使用权限范围内的最新日期
            if date is None:
                date = self.get_available_date()
            
            stocks = self.jq.get_industry_stocks(industry_code, date=date)
            result = []
            for code in stocks:
                # 获取股票名称
                try:
                    info = self.jq.get_security_info(code)
                    result.append({
                        "symbol": code,
                        "name": info.display_name if hasattr(info, 'display_name') else code
                    })
                except:
                    result.append({"symbol": code, "name": code})
            
            logger.info(f"✅ JQData获取行业成分股: {industry_code} - {len(result)} 只 (日期: {date})")
            return result
        except Exception as e:
            logger.error(f"❌ JQData获取行业成分股失败: {e}")
            return []
    
    def get_concept_stocks(self, concept_code: str, date: str = None) -> List[Dict]:
        """
        获取概念成分股
        
        Args:
            concept_code: 概念代码（如 'SC0001'）或概念名称
            date: 日期 'YYYY-MM-DD'，默认使用权限范围内的最新日期
            
        Returns:
            股票列表
        """
        if not self.available or not self.jq:
            return []
        
        try:
            # 如果没有指定日期，使用权限范围内的最新日期
            if date is None:
                date = self.get_available_date()
            
            # 如果输入的是名称，尝试查找对应的代码
            if not concept_code.startswith('SC'):
                try:
                    concepts = self.jq.get_concepts()
                    if concepts is not None and not concepts.empty:
                        matched = concepts[concepts['name'] == concept_code]
                        if not matched.empty:
                            concept_code = matched.index[0]
                            logger.info(f"将概念名称 '{concept_code}' 转换为代码: {concept_code}")
                        else:
                            # 尝试模糊匹配
                            matched = concepts[concepts['name'].str.contains(concept_code, na=False)]
                            if not matched.empty:
                                concept_code = matched.index[0]
                                name = matched.iloc[0]['name']
                                logger.info(f"模糊匹配概念: {name} ({concept_code})")
                except Exception as e:
                    logger.warning(f"概念名称转换失败: {e}")
            
            stocks = self.jq.get_concept_stocks(concept_code, date=date)
            result = []
            for code in stocks:
                try:
                    info = self.jq.get_security_info(code)
                    result.append({
                        "symbol": code,
                        "name": info.display_name if hasattr(info, 'display_name') else code
                    })
                except:
                    result.append({"symbol": code, "name": code})
            
            logger.info(f"✅ JQData获取概念成分股: {concept_code} - {len(result)} 只 (日期: {date})")
            return result
        except Exception as e:
            logger.error(f"❌ JQData获取概念成分股失败: {e}")
            return []
    
    def get_price(
        self, 
        codes: List[str], 
        start_date: str, 
        end_date: str,
        frequency: str = 'daily'
    ) -> Any:
        """
        获取历史行情
        
        Args:
            codes: 股票代码列表（JQData格式，如 '000001.XSHE'）
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            frequency: 频率 'daily'/'1m'/'5m'等
            
        Returns:
            DataFrame或Panel
        """
        if not self.available or not self.jq:
            return None
        
        try:
            df = self.jq.get_price(
                codes,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                fields=['open', 'close', 'high', 'low', 'volume', 'money']
            )
            logger.info(f"✅ JQData获取行情: {len(codes)} 只股票")
            return df
        except Exception as e:
            logger.error(f"❌ JQData获取行情失败: {e}")
            return None
    
    def get_money_flow(
        self,
        codes: List[str],
        start_date: str,
        end_date: str
    ) -> Any:
        """
        获取资金流向
        
        Args:
            codes: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame
        """
        if not self.available or not self.jq:
            return None
        
        try:
            df = self.jq.get_money_flow(
                codes,
                start_date=start_date,
                end_date=end_date
            )
            logger.info(f"✅ JQData获取资金流向: {len(codes)} 只股票")
            return df
        except Exception as e:
            logger.error(f"❌ JQData获取资金流向失败: {e}")
            return None
    
    def get_all_industries(self, date: str = None) -> List[Dict]:
        """
        获取所有行业列表
        
        Args:
            date: 日期 'YYYY-MM-DD'，默认使用权限范围内的最新日期
        """
        if not self.available or not self.jq:
            return []
        
        try:
            # 如果没有指定日期，使用权限范围内的最新日期
            if date is None:
                from datetime import datetime
                date = '2025-08-28'  # 试用账号权限范围
            
            industries = self.jq.get_industries(date=date)
            result = []
            
            # get_industries返回字典
            if isinstance(industries, dict):
                for code, info in industries.items():
                    result.append({
                        "code": code,
                        "name": info.get("name", code) if isinstance(info, dict) else str(info),
                        "type": "industry"
                    })
            logger.info(f"✅ JQData获取行业列表: {len(result)} 个")
            return result
        except Exception as e:
            logger.error(f"❌ JQData获取行业列表失败: {e}")
            return []
    
    def get_all_concepts(self) -> List[Dict]:
        """获取所有概念列表"""
        if not self.available or not self.jq:
            return []
        
        try:
            concepts = self.jq.get_concepts()
            result = []
            
            # get_concepts返回DataFrame
            if hasattr(concepts, 'iterrows'):
                for idx, row in concepts.iterrows():
                    result.append({
                        "code": idx,  # DataFrame的index是概念代码
                        "name": row.get("name", idx),
                        "type": "concept"
                    })
            elif isinstance(concepts, dict):
                for code, info in concepts.items():
                    result.append({
                        "code": code,
                        "name": info.get("name", code) if isinstance(info, dict) else str(info),
                        "type": "concept"
                    })
            
            logger.info(f"✅ JQData获取概念列表: {len(result)} 个")
            return result
        except Exception as e:
            logger.error(f"❌ JQData获取概念列表失败: {e}")
            return []


# ============================================================
# 全局单例
# ============================================================

_cache_manager = None
_theme_manager = None
_sector_cache = None
_jqdata_provider = None
_tushare_provider = None


def get_cache_manager() -> CacheManager:
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def get_theme_manager() -> ThemeDataManager:
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeDataManager()
    return _theme_manager


def get_sector_cache() -> SectorMemberCache:
    global _sector_cache
    if _sector_cache is None:
        _sector_cache = SectorMemberCache()
    return _sector_cache


def get_jqdata_provider() -> JQDataProvider:
    global _jqdata_provider
    if _jqdata_provider is None:
        _jqdata_provider = JQDataProvider()
    return _jqdata_provider


def get_tushare_provider() -> TuShareProvider:
    """获取 TuShare 折衷数据源单例"""
    global _tushare_provider
    if _tushare_provider is None:
        _tushare_provider = TuShareProvider()
    return _tushare_provider

                                                            