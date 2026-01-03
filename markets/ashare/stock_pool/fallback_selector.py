"""
Fallback选股逻辑

当主数据源（API）不可用时，使用备选策略构建股票池：

1. 龙头股直投池：从主线识别结果中提取龙头股
2. 龙虎榜热门池：从缓存的龙虎榜数据中提取
3. 涨停强势池：从涨停板数据中提取

使用优先级：主线成分股 → 龙头股 → 龙虎榜 → 涨停板
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json

from .models import StockPoolItem, StockPool, PoolSource
from .data_layer import get_theme_manager, get_cache_manager, get_sector_cache

logger = logging.getLogger(__name__)

# 缓存目录
CACHE_DIR = Path.home() / ".local/share/trquant/cache"


class FallbackSelector:
    """
    Fallback选股器
    
    提供多通道备选选股逻辑，确保始终能构建候选池
    """
    
    def __init__(self):
        self.theme_manager = get_theme_manager()
        self.cache_manager = get_cache_manager()
        self.sector_cache = get_sector_cache()
        
        # 选股结果来源标记
        self.source_tags = {
            "theme_member": "主线成分",
            "leader": "主线龙头",
            "dragon_tiger": "龙虎榜",
            "limit_up": "涨停板",
            "fallback": "降级策略"
        }
    
    def select_with_fallback(
        self, 
        theme_names: List[str] = None,
        max_stocks: int = 50
    ) -> StockPool:
        """
        执行带Fallback的选股
        
        Args:
            theme_names: 指定的主线名称列表（可选）
            max_stocks: 最大股票数量
            
        Returns:
            股票池（始终非空）
        """
        logger.info("=" * 60)
        logger.info("执行Fallback选股策略...")
        
        pool = StockPool(
            description=f"Fallback选股池 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # ============================================================
        # 通道1：主线成分股（如果可用）
        # ============================================================
        if theme_names:
            theme_stocks = self._select_from_theme_members(theme_names)
            for item in theme_stocks:
                pool.add_stock(item)
            logger.info(f"通道1 - 主线成分股: {len(theme_stocks)} 只")
        
        # ============================================================
        # 通道2：龙头股直投（核心Fallback）
        # ============================================================
        leader_stocks = self._select_from_leaders(theme_names)
        added_leaders = 0
        for item in leader_stocks:
            if pool.add_stock(item):
                added_leaders += 1
        logger.info(f"通道2 - 主线龙头股: {added_leaders} 只")
        
        # ============================================================
        # 通道3：龙虎榜热门
        # ============================================================
        if len(pool.stocks) < max_stocks:
            dragon_stocks = self._select_from_dragon_tiger()
            added_dragons = 0
            for item in dragon_stocks:
                if pool.add_stock(item):
                    added_dragons += 1
                if len(pool.stocks) >= max_stocks:
                    break
            logger.info(f"通道3 - 龙虎榜: {added_dragons} 只")
        
        # ============================================================
        # 通道4：涨停强势
        # ============================================================
        if len(pool.stocks) < max_stocks:
            limit_up_stocks = self._select_from_limit_up()
            added_limit = 0
            for item in limit_up_stocks:
                if pool.add_stock(item):
                    added_limit += 1
                if len(pool.stocks) >= max_stocks:
                    break
            logger.info(f"通道4 - 涨停板: {added_limit} 只")
        
        # ============================================================
        # 结果汇总
        # ============================================================
        logger.info("=" * 60)
        logger.info(f"Fallback选股完成，共 {len(pool.stocks)} 只股票")
        logger.info(f"来源分布: {pool.summary.get('by_source', {})}")
        
        # 标记为降级策略结果
        if len(pool.stocks) > 0:
            pool.description += " [Fallback模式]"
        
        return pool
    
    def _select_from_theme_members(self, theme_names: List[str]) -> List[StockPoolItem]:
        """从主线成分股中选取"""
        items = []
        
        for theme_name in theme_names:
            members = self.theme_manager.get_theme_members(theme_name)
            for member in members[:10]:  # 每个主线最多10只
                item = StockPoolItem(
                    code=member.get("symbol", member.get("code", "")),
                    name=member.get("name", ""),
                    sector=theme_name,
                    source=PoolSource.MAINLINE.value,
                    entry_reason=f"主线成分股：{theme_name}",
                    period="medium",
                    priority=2
                )
                items.append(item)
        
        return items
    
    def _select_from_leaders(self, theme_names: List[str] = None) -> List[StockPoolItem]:
        """
        从龙头股中选取
        
        这是核心Fallback策略：使用主线识别已输出的龙头股
        """
        items = []
        
        # 获取所有龙头股
        all_leaders = self.theme_manager.get_all_leader_stocks()
        
        # 如果指定了主线，只取这些主线的龙头
        if theme_names:
            leaders = [l for l in all_leaders if l.get("theme") in theme_names]
        else:
            # 取评分最高的前20个主线的龙头
            leaders = sorted(all_leaders, key=lambda x: x.get("theme_score", 0), reverse=True)[:20]
        
        for leader in leaders:
            item = StockPoolItem(
                code="",  # 需要后续查找
                name=leader.get("name", ""),
                sector=leader.get("theme", ""),
                source="leader",  # 标记为龙头股来源
                entry_reason=f"主线龙头：{leader.get('theme')}（评分{leader.get('theme_score', 0):.1f}）",
                period="short",
                priority=1,  # 龙头股优先级最高
                mainline_name=leader.get("theme", ""),
                mainline_score=leader.get("theme_score", 0),
                change_pct=leader.get("change", 0)
            )
            items.append(item)
            logger.debug(f"龙头股入选: {leader.get('name')} ({leader.get('theme')})")
        
        return items
    
    def _select_from_dragon_tiger(self) -> List[StockPoolItem]:
        """从龙虎榜缓存中选取"""
        items = []
        
        # 读取龙虎榜缓存
        cache_file = CACHE_DIR / "dragon_tiger.json"
        if not cache_file.exists():
            logger.warning("龙虎榜缓存不存在")
            return items
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 解析龙虎榜数据
            records = data.get("data", [])
            if isinstance(records, list):
                for record in records[:30]:
                    item = StockPoolItem(
                        code=record.get("代码", record.get("code", "")),
                        name=record.get("名称", record.get("name", "")),
                        source="dragon_tiger",
                        entry_reason=f"龙虎榜上榜",
                        period="short",
                        priority=3
                    )
                    if item.code or item.name:
                        items.append(item)
        except Exception as e:
            logger.warning(f"读取龙虎榜缓存失败: {e}")
        
        return items
    
    def _select_from_limit_up(self) -> List[StockPoolItem]:
        """从涨停板数据中选取"""
        items = []
        
        # 读取市场情绪缓存（包含涨停数据）
        cache_file = CACHE_DIR / "market_sentiment.json"
        if not cache_file.exists():
            logger.warning("市场情绪缓存不存在")
            return items
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 解析涨停股数据
            limit_up_data = data.get("data", {}).get("limit_up_stocks", [])
            if isinstance(limit_up_data, list):
                for stock in limit_up_data[:20]:
                    item = StockPoolItem(
                        code=stock.get("代码", stock.get("code", "")),
                        name=stock.get("名称", stock.get("name", "")),
                        source="limit_up",
                        entry_reason="涨停板强势股",
                        period="short",
                        priority=4
                    )
                    if item.code or item.name:
                        items.append(item)
        except Exception as e:
            logger.warning(f"读取涨停板缓存失败: {e}")
        
        return items
    
    def get_fallback_summary(self, pool: StockPool) -> str:
        """生成Fallback选股报告"""
        summary = []
        summary.append("=" * 50)
        summary.append("📊 Fallback选股报告")
        summary.append("=" * 50)
        summary.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"总股票数: {len(pool.stocks)}")
        summary.append("")
        
        # 按来源统计
        by_source = pool.summary.get("by_source", {})
        summary.append("📌 来源分布:")
        for source, count in by_source.items():
            tag = self.source_tags.get(source, source)
            summary.append(f"  - {tag}: {count} 只")
        
        summary.append("")
        summary.append("⚠️ 注意: 当前结果使用降级策略生成")
        summary.append("建议: 待数据源恢复后重新构建")
        summary.append("=" * 50)
        
        return "\n".join(summary)


# ============================================================
# 便捷函数
# ============================================================

def build_fallback_pool(theme_names: List[str] = None, max_stocks: int = 50) -> StockPool:
    """构建Fallback股票池的便捷函数"""
    selector = FallbackSelector()
    return selector.select_with_fallback(theme_names, max_stocks)


def get_available_leaders() -> List[Dict]:
    """获取可用的龙头股列表"""
    manager = get_theme_manager()
    return manager.get_all_leader_stocks()




