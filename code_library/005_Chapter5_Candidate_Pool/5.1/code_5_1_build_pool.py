"""
文件名: code_5_1_build_pool.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.1/code_5_1_build_pool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: build_pool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class StockPoolManager:
    """股票池管理器"""
    
    def build_pool(
        self,
        include_mainline: bool = True,
        include_tech: bool = True,
        include_external: bool = True,
        period: str = "medium",
        use_fallback: bool = True
    ) -> StockPool:
            """
    build_pool函数
    
    **设计原理**：
    - **核心功能**：实现build_pool的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        # 创建主股票池
        self.current_pool = StockPool(
            description=f"综合股票池 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        api_success = True  # 标记API是否成功
        
        # ============================================================
        # 第一层：实时API（优先使用）
        # ============================================================
        
        # 1. 主线强势股筛选
        if include_mainline:
            try:
                mainline_pool = self.mainline_selector.select(period=period)
                self._merge_pool(mainline_pool, "mainline")
                if len(mainline_pool.stocks) == 0:
                    api_success = False
            except Exception as e:
                logger.warning(f"主线筛选失败: {e}")
                api_success = False
        
        # 2. 技术突破扫描
        if include_tech:
            try:
                tech_pool = self.tech_scanner.scan(period=period)
                self._merge_pool(tech_pool, "tech_breakout")
            except Exception as e:
                logger.warning(f"技术扫描失败: {e}")
        
        # 3. 外部推荐整合
        if include_external:
            try:
                external_pool = self.external_parser.parse_all()
                self._merge_pool(external_pool, "external")
            except Exception as e:
                logger.warning(f"外部数据整合失败: {e}")
        
        # ============================================================
        # 第二层：缓存数据（API失败时使用）
        # ============================================================
        
        if not api_success:
            logger.warning("API失败，尝试使用缓存数据...")
            try:
                cached_pool = self._load_from_cache()
                if cached_pool and len(cached_pool.stocks) > 0:
                    self._merge_pool(cached_pool, "cache")
                    logger.info(f"从缓存加载了{len(cached_pool.stocks)}只股票")
            except Exception as e:
                logger.warning(f"缓存加载失败: {e}")
        
        # ============================================================
        # 第三层：Fallback策略（缓存也失败时使用）
        # ============================================================
        
        if use_fallback and len(self.current_pool.stocks) == 0:
            logger.warning("⚠️ 主数据源失败，启用Fallback策略")
            try:
                fallback_selector = FallbackSelector()
                
                # 获取主线名称列表
                theme_manager = get_theme_manager()
                themes = theme_manager.load_themes()
                theme_names = [t.get("name") for t in themes[:10] if t.get("name")]
                
                fallback_pool = fallback_selector.select_with_fallback(
                    theme_names=theme_names,
                    max_stocks=50
                )
                
                self._merge_pool(fallback_pool, "fallback")
                self.current_pool.description += " [Fallback模式]"
                
            except Exception as e:
                logger.error(f"Fallback策略也失败: {e}")
        
        # 交叉验证和优先级调整
        self._cross_validate_and_adjust()
        
        # 按周期分类
        self._classify_by_period()
        
        # 保存
        self.save_current_pool()
        
        return self.current_pool