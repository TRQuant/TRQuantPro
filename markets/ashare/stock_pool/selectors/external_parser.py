"""
外部数据解析器

解析和整合外部筛选器的结果：
1. 券商月度金股
2. GuruFocus价值筛选
3. 其他第三方数据

这些数据用于交叉验证内部筛选结果
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json
import csv

from ..models import StockPoolItem, StockPool, PoolSource, PoolType

logger = logging.getLogger(__name__)


class ExternalDataParser:
    """
    外部数据解析器
    
    整合券商金股、GuruFocus等外部筛选结果
    """
    
    # 数据目录
    DATA_DIR = Path.home() / ".local/share/trquant/data/stock_pool/external"
    
    def __init__(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # ============================================================
    # 券商金股
    # ============================================================
    
    def parse_broker_picks(self, filepath: Path = None) -> List[StockPoolItem]:
        """
        解析券商金股数据
        
        文件格式（CSV）：
        代码,名称,推荐券商,推荐日期,推荐理由
        600519,贵州茅台,中信证券,2024-11,业绩稳定增长
        
        Args:
            filepath: CSV文件路径
            
        Returns:
            股票池条目列表
        """
        if filepath is None:
            # 查找最新文件
            broker_dir = self.DATA_DIR / "broker_picks"
            broker_dir.mkdir(exist_ok=True)
            files = sorted(broker_dir.glob("broker_picks_*.csv"), reverse=True)
            if files:
                filepath = files[0]
            else:
                logger.warning("未找到券商金股文件")
                return []
        
        if not filepath.exists():
            logger.warning(f"文件不存在: {filepath}")
            return []
        
        result = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = StockPoolItem(
                        code=row.get('代码', ''),
                        name=row.get('名称', ''),
                        
                        source=PoolSource.BROKER.value,
                        entry_reason=f"券商推荐：{row.get('推荐券商', '')}，{row.get('推荐理由', '')}",
                        entry_date=row.get('推荐日期', datetime.now().strftime("%Y-%m-%d")),
                        
                        period="medium",  # 券商金股通常是中期视角
                        pool_type=PoolType.SATELLITE.value,
                        priority=3,  # 中等优先级
                        
                        notes=row.get('推荐理由', '')
                    )
                    result.append(item)
            
            logger.info(f"解析券商金股：{len(result)} 只")
        except Exception as e:
            logger.error(f"解析券商金股失败: {e}")
        
        return result
    
    def save_broker_picks_template(self):
        """保存券商金股模板文件"""
        template_path = self.DATA_DIR / "broker_picks" / "template.csv"
        template_path.parent.mkdir(exist_ok=True)
        
        with open(template_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['代码', '名称', '推荐券商', '推荐日期', '推荐理由'])
            writer.writerow(['600519', '贵州茅台', '中信证券', '2024-11', '业绩稳定增长'])
            writer.writerow(['000858', '五粮液', '华泰证券', '2024-11', '白酒龙头'])
        
        logger.info(f"模板已保存: {template_path}")
        return template_path
    
    # ============================================================
    # GuruFocus
    # ============================================================
    
    def parse_gurufocus(self, filepath: Path = None) -> List[StockPoolItem]:
        """
        解析GuruFocus筛选结果
        
        文件格式（JSON）：
        [
            {
                "code": "600519",
                "name": "贵州茅台",
                "pe": 25,
                "roe": 30,
                "peg": 0.8,
                "score": 85,
                "strategy": "巴菲特策略"
            }
        ]
        
        Args:
            filepath: JSON文件路径
            
        Returns:
            股票池条目列表
        """
        if filepath is None:
            gurufocus_dir = self.DATA_DIR / "gurufocus"
            gurufocus_dir.mkdir(exist_ok=True)
            files = sorted(gurufocus_dir.glob("gurufocus_*.json"), reverse=True)
            if files:
                filepath = files[0]
            else:
                logger.warning("未找到GuruFocus文件")
                return []
        
        if not filepath.exists():
            logger.warning(f"文件不存在: {filepath}")
            return []
        
        result = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for stock in data:
                item = StockPoolItem(
                    code=stock.get('code', ''),
                    name=stock.get('name', ''),
                    
                    source=PoolSource.GURUFOCUS.value,
                    entry_reason=f"GuruFocus筛选：{stock.get('strategy', '')}，评分{stock.get('score', 0)}",
                    
                    period="long",  # GuruFocus偏长期价值
                    pool_type=PoolType.CORE.value if stock.get('score', 0) >= 80 else PoolType.WATCH.value,
                    priority=2 if stock.get('score', 0) >= 80 else 4,
                    
                    factor_scores={
                        "PE": stock.get('pe', 0),
                        "ROE": stock.get('roe', 0),
                        "PEG": stock.get('peg', 0)
                    },
                    composite_score=stock.get('score', 0),
                    
                    notes=stock.get('strategy', '')
                )
                result.append(item)
            
            logger.info(f"解析GuruFocus：{len(result)} 只")
        except Exception as e:
            logger.error(f"解析GuruFocus失败: {e}")
        
        return result
    
    def save_gurufocus_template(self):
        """保存GuruFocus模板文件"""
        template_path = self.DATA_DIR / "gurufocus" / "template.json"
        template_path.parent.mkdir(exist_ok=True)
        
        template = [
            {
                "code": "600519",
                "name": "贵州茅台",
                "pe": 25,
                "roe": 30,
                "peg": 0.8,
                "score": 85,
                "strategy": "巴菲特策略"
            }
        ]
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        logger.info(f"模板已保存: {template_path}")
        return template_path
    
    # ============================================================
    # 整合
    # ============================================================
    
    def parse_all(self) -> StockPool:
        """
        解析所有外部数据
        
        Returns:
            外部推荐股票池
        """
        logger.info("开始解析外部数据...")
        
        pool = StockPool(
            description=f"外部推荐股池 - {datetime.now().strftime('%Y-%m-%d')}"
        )
        
        # 券商金股
        broker_stocks = self.parse_broker_picks()
        for item in broker_stocks:
            pool.add_stock(item)
        
        # GuruFocus
        gurufocus_stocks = self.parse_gurufocus()
        for item in gurufocus_stocks:
            pool.add_stock(item)
        
        logger.info(f"外部数据解析完成，共 {len(pool.stocks)} 只股票")
        return pool
    
    def cross_validate(
        self, 
        internal_pool: StockPool, 
        external_pool: StockPool
    ) -> List[StockPoolItem]:
        """
        交叉验证：找出同时出现在内部筛选和外部推荐中的股票
        
        这些股票优先级应提升
        
        Args:
            internal_pool: 内部筛选股票池
            external_pool: 外部推荐股票池
            
        Returns:
            交叉验证通过的股票列表
        """
        internal_codes = set(internal_pool.get_codes())
        external_codes = set(external_pool.get_codes())
        
        overlap_codes = internal_codes & external_codes
        
        if not overlap_codes:
            logger.info("无交叉验证结果")
            return []
        
        result = []
        for code in overlap_codes:
            internal_stock = internal_pool.get_stock(code)
            external_stock = external_pool.get_stock(code)
            
            if internal_stock:
                # 提升优先级
                internal_stock.priority = max(1, internal_stock.priority - 1)
                internal_stock.entry_reason += f" | 外部验证：{external_stock.source if external_stock else 'N/A'}"
                internal_stock.tech_signals.append("交叉验证通过")
                result.append(internal_stock)
        
        logger.info(f"交叉验证通过：{len(result)} 只股票")
        return result




