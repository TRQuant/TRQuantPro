"""
股票池管理器

【核心模块】统筹管理股票池的构建、更新和输出

职责：
1. 调用各筛选器构建初筛股票池
2. 合并去重和优先级排序
3. 与前后模块衔接：
   - 前：读取主线识别结果
   - 后：输出标准化股票池供因子模块和策略模块使用
4. 持久化管理

完整流程位置：
    主线识别 → 【股票池构建】→ 因子开发 → 策略生成 → 回测验证 → 实盘交易
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional, Callable
from pathlib import Path
import json

from .models import (
    StockPool, StockPoolItem, TradeSignal,
    PoolSource, Period, PoolType, SignalAction,
    load_mainline_scores, save_pool_for_factor_module, load_pool_for_strategy_module
)
from .selectors import (
    MainlineSelector,
    TechBreakoutScanner,
    PeriodSelector,
    ExternalDataParser
)
from .fallback_selector import FallbackSelector, build_fallback_pool
from .data_layer import get_theme_manager, DataSourceStatus

logger = logging.getLogger(__name__)


class StockPoolManager:
    """
    股票池管理器
    
    核心功能：
    1. 构建股票池（调用各筛选器）
    2. 合并和去重
    3. 与因子模块和策略模块对接
    4. 持久化管理
    """
    
    # 数据目录
    DATA_DIR = Path.home() / ".local/share/trquant/data/stock_pool"
    REPORT_DIR = Path.home() / ".local/share/trquant/reports/stock_pool"
    
    def __init__(self):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 初始化筛选器
        self.mainline_selector = MainlineSelector()
        self.tech_scanner = TechBreakoutScanner()
        self.period_selector = PeriodSelector()
        self.external_parser = ExternalDataParser()
        
        # 当前股票池
        self.current_pool: Optional[StockPool] = None
        
        # 进度回调
        self.progress_callback: Optional[Callable] = None
    
    def set_progress_callback(self, callback: Callable):
        """设置进度回调（供GUI使用）"""
        self.progress_callback = callback
    
    def _report_progress(self, step: str, progress: int, message: str):
        """报告进度"""
        if self.progress_callback:
            self.progress_callback(step, progress, message)
        logger.info(f"[{progress}%] {step}: {message}")
    
    # ============================================================
    # 核心方法：构建股票池
    # ============================================================
    
    def build_pool(
        self,
        include_mainline: bool = True,
        include_tech: bool = True,
        include_external: bool = True,
        period: str = "medium",
        use_fallback: bool = True  # 新增：是否启用Fallback策略
    ) -> StockPool:
        """
        构建完整的股票池
        
        三层数据保障架构：
        1. 优先使用实时API获取数据
        2. API失败时使用缓存数据
        3. 缓存也失败时使用Fallback策略（龙头股+龙虎榜）
        
        Args:
            include_mainline: 是否包含主线强势股
            include_tech: 是否包含技术突破股
            include_external: 是否包含外部推荐
            period: 默认投资周期
            use_fallback: 是否启用Fallback策略
            
        Returns:
            合并后的股票池
        """
        logger.info("=" * 60)
        logger.info("开始构建股票池（三层数据保障架构）...")
        logger.info("=" * 60)
        
        self._report_progress("初始化", 0, "开始构建股票池")
        
        # 创建主股票池
        self.current_pool = StockPool(
            description=f"综合股票池 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        api_success = True  # 标记API是否成功
        
        # 1. 主线强势股筛选
        if include_mainline:
            self._report_progress("主线筛选", 10, "从主线识别结果提取强势股...")
            try:
                mainline_pool = self.mainline_selector.select(period=period)
                self._merge_pool(mainline_pool, "mainline")
                self._report_progress("主线筛选", 40, f"主线强势股：{len(mainline_pool.stocks)} 只")
                if len(mainline_pool.stocks) == 0:
                    api_success = False
            except Exception as e:
                logger.warning(f"主线筛选失败: {e}")
                api_success = False
        
        # 2. 技术突破扫描
        if include_tech:
            self._report_progress("技术扫描", 45, "全市场技术突破扫描...")
            try:
                tech_pool = self.tech_scanner.scan(period=period)
                self._merge_pool(tech_pool, "tech_breakout")
                self._report_progress("技术扫描", 70, f"技术突破股：{len(tech_pool.stocks)} 只")
            except Exception as e:
                logger.warning(f"技术扫描失败: {e}")
        
        # 3. 外部推荐整合
        if include_external:
            self._report_progress("外部数据", 75, "整合外部筛选结果...")
            try:
                external_pool = self.external_parser.parse_all()
                self._merge_pool(external_pool, "external")
                self._report_progress("外部数据", 85, f"外部推荐：{len(external_pool.stocks)} 只")
            except Exception as e:
                logger.warning(f"外部数据整合失败: {e}")
        
        # ============================================================
        # 【关键】Fallback策略：如果股票池为空，使用备选方案
        # ============================================================
        if use_fallback and len(self.current_pool.stocks) == 0:
            self._report_progress("降级策略", 87, "启用Fallback选股策略...")
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
                self._report_progress("降级策略", 89, f"Fallback选股：{len(fallback_pool.stocks)} 只")
                
                # 更新描述，标记为降级策略
                self.current_pool.description += " [Fallback模式]"
                
            except Exception as e:
                logger.error(f"Fallback策略也失败: {e}")
        
        # 4. 交叉验证和优先级调整
        self._report_progress("交叉验证", 90, "执行交叉验证...")
        self._cross_validate_and_adjust()
        
        # 5. 按周期分类
        classified = self.period_selector.classify_stocks(self.current_pool)
        for stock in self.current_pool.stocks:
            if stock in classified.get("short", []):
                stock.period = "short"
            elif stock in classified.get("long", []):
                stock.period = "long"
            else:
                stock.period = "medium"
        
        # 6. 保存
        self._report_progress("保存", 95, "保存股票池...")
        self.save_current_pool()
        
        self._report_progress("完成", 100, f"股票池构建完成，共 {len(self.current_pool.stocks)} 只股票")
        
        logger.info("=" * 60)
        logger.info(f"股票池构建完成")
        logger.info(f"  总数：{len(self.current_pool.stocks)} 只")
        logger.info(f"  来源分布：{self.current_pool.summary.get('by_source', {})}")
        logger.info(f"  周期分布：{self.current_pool.summary.get('by_period', {})}")
        if not api_success:
            logger.warning("  ⚠️ 注意：使用了Fallback降级策略")
        logger.info("=" * 60)
        
        return self.current_pool
    
    def _merge_pool(self, source_pool: StockPool, source_name: str):
        """合并股票池（去重）"""
        added = 0
        for stock in source_pool.stocks:
            if self.current_pool.add_stock(stock):
                added += 1
        logger.info(f"合并 {source_name}：新增 {added} 只，已存在 {len(source_pool.stocks) - added} 只")
    
    def _cross_validate_and_adjust(self):
        """交叉验证和优先级调整"""
        # 找出在多个来源中出现的股票
        code_sources = {}
        for stock in self.current_pool.stocks:
            if stock.code not in code_sources:
                code_sources[stock.code] = []
            code_sources[stock.code].append(stock.source)
        
        # 调整优先级
        for stock in self.current_pool.stocks:
            sources = code_sources.get(stock.code, [])
            if len(set(sources)) > 1:
                # 多来源确认，提升优先级
                stock.priority = max(1, stock.priority - 1)
                stock.tech_signals.append(f"多来源确认({len(set(sources))})")
    
    # ============================================================
    # 与因子模块衔接
    # ============================================================
    
    def get_stocks_for_factor_module(self) -> List[str]:
        """
        获取股票代码列表，供因子模块使用
        
        这是与后续因子开发模块的衔接点
        
        Returns:
            股票代码列表
        """
        if not self.current_pool:
            self.load_latest_pool()
        
        if self.current_pool:
            return self.current_pool.get_codes()
        return []
    
    def update_factor_scores(self, factor_scores: Dict[str, Dict[str, float]]):
        """
        更新因子评分（由因子模块调用）
        
        Args:
            factor_scores: {股票代码: {因子名: 分数}}
        """
        if not self.current_pool:
            return
        
        for stock in self.current_pool.stocks:
            if stock.code in factor_scores:
                stock.factor_scores = factor_scores[stock.code]
        
        logger.info(f"更新了 {len(factor_scores)} 只股票的因子评分")
    
    def calculate_composite_scores(self, weights: Dict[str, float] = None):
        """
        计算综合评分
        
        Args:
            weights: 因子权重
        """
        if not self.current_pool:
            return
        
        for stock in self.current_pool.stocks:
            stock.calculate_composite_score(weights)
    
    # ============================================================
    # 与策略模块衔接
    # ============================================================
    
    def generate_signals(
        self,
        strategy_name: str = "default",
        top_n: int = 20
    ) -> List[TradeSignal]:
        """
        生成交易信号
        
        这是与后续策略模块的衔接点
        
        Args:
            strategy_name: 策略名称
            top_n: 取前N只股票
            
        Returns:
            交易信号列表
        """
        if not self.current_pool:
            self.load_latest_pool()
        
        if not self.current_pool:
            return []
        
        signals = []
        top_stocks = self.current_pool.get_top_stocks(top_n)
        
        for i, stock in enumerate(top_stocks):
            signal = TradeSignal(
                signal_id=f"{strategy_name}_{stock.code}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                stock_code=stock.code,
                stock_name=stock.name,
                
                action=SignalAction.BUY.value,
                target_position=1.0 / len(top_stocks),  # 等权分配
                
                entry_price=stock.current_price,
                stop_loss=stock.current_price * 0.95,   # 5%止损
                take_profit=stock.current_price * 1.15, # 15%止盈
                current_price=stock.current_price,
                
                strategy=strategy_name,
                pool_source=stock.source,
                reason=stock.entry_reason,
                
                priority=stock.priority,
                
                factor_scores=stock.factor_scores,
                composite_score=stock.composite_score
            )
            signals.append(signal)
        
        logger.info(f"生成 {len(signals)} 个交易信号")
        return signals
    
    def export_for_ptrade(self, signals: List[TradeSignal] = None) -> str:
        """
        导出PTrade策略代码
        
        Args:
            signals: 交易信号列表
            
        Returns:
            PTrade策略代码
        """
        if signals is None:
            signals = self.generate_signals()
        
        stock_list = [s.stock_code for s in signals]
        
        code = f'''# -*- coding: utf-8 -*-
"""
韬睿量化 - 股票池策略
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
股票数量: {len(stock_list)}
"""

def initialize(context):
    """初始化"""
    set_benchmark('000300.XSHG')
    
    # 股票池
    context.stock_pool = {stock_list}
    
    # 调仓频率
    run_monthly(rebalance, 1, time='open')

def rebalance(context):
    """月度调仓"""
    stocks = context.stock_pool
    
    # 卖出不在池中的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in stocks:
            order_target(stock, 0)
    
    # 等权买入
    if len(stocks) > 0:
        weight = 1.0 / len(stocks)
        for stock in stocks:
            order_target_value(stock, context.portfolio.total_value * weight)
'''
        return code
    
    def export_for_qmt(self, signals: List[TradeSignal] = None) -> str:
        """
        导出QMT策略代码
        
        Args:
            signals: 交易信号列表
            
        Returns:
            QMT策略代码
        """
        if signals is None:
            signals = self.generate_signals()
        
        stock_list = [s.stock_code for s in signals]
        
        code = f'''# -*- coding: utf-8 -*-
"""
韬睿量化 - QMT股票池策略
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
股票数量: {len(stock_list)}
"""

from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader

# 股票池
STOCK_POOL = {stock_list}

def on_start():
    """策略启动"""
    print(f"股票池策略启动，池内 {{len(STOCK_POOL)}} 只股票")

def execute_signals(trader, account):
    """执行交易信号"""
    for stock in STOCK_POOL:
        # 获取当前持仓
        positions = trader.query_stock_positions(account)
        current = positions.get(stock, 0)
        
        # 目标持仓（等权）
        target = 1.0 / len(STOCK_POOL)
        
        # 执行调仓
        if current < target:
            trader.order_stock(account, stock, xtconstant.STOCK_BUY, ...)
'''
        return code
    
    # ============================================================
    # 持久化管理
    # ============================================================
    
    def save_current_pool(self, filepath: Path = None) -> Path:
        """保存当前股票池"""
        if not self.current_pool:
            return None
        
        if filepath is None:
            date_str = datetime.now().strftime("%Y%m%d")
            filepath = self.DATA_DIR / "daily" / f"pool_{date_str}.json"
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self.current_pool.save(filepath)
        
        # 同时保存为latest供其他模块使用
        latest_path = self.DATA_DIR / "latest_pool.json"
        self.current_pool.save(latest_path)
        
        logger.info(f"股票池已保存: {filepath}")
        return filepath
    
    def load_latest_pool(self) -> Optional[StockPool]:
        """加载最新股票池"""
        latest_path = self.DATA_DIR / "latest_pool.json"
        
        if latest_path.exists():
            self.current_pool = StockPool.load(latest_path)
            logger.info(f"加载股票池: {len(self.current_pool.stocks)} 只股票")
            return self.current_pool
        
        # 尝试加载最近的每日股票池
        daily_dir = self.DATA_DIR / "daily"
        if daily_dir.exists():
            files = sorted(daily_dir.glob("pool_*.json"), reverse=True)
            if files:
                self.current_pool = StockPool.load(files[0])
                logger.info(f"加载股票池 {files[0].name}: {len(self.current_pool.stocks)} 只股票")
                return self.current_pool
        
        logger.warning("未找到股票池文件")
        return None
    
    def load_pool_by_date(self, date_str: str) -> Optional[StockPool]:
        """加载指定日期的股票池"""
        filepath = self.DATA_DIR / "daily" / f"pool_{date_str}.json"
        if filepath.exists():
            return StockPool.load(filepath)
        return None
    
    # ============================================================
    # 报告生成
    # ============================================================
    
    def generate_report(self) -> str:
        """生成股票池报告（HTML格式）"""
        if not self.current_pool:
            return "<html><body><h1>无股票池数据</h1></body></html>"
        
        # 按周期分组
        classified = self.period_selector.classify_stocks(self.current_pool)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>韬睿量化 - 股票池报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #0d1117; color: #c9d1d9; }}
        h1 {{ color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }}
        h2 {{ color: #8b949e; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .summary-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; text-align: center; }}
        .summary-card .number {{ font-size: 32px; font-weight: bold; color: #58a6ff; }}
        .summary-card .label {{ color: #8b949e; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #30363d; }}
        th {{ background: #161b22; color: #8b949e; }}
        tr:hover {{ background: #161b22; }}
        .priority-1 {{ color: #f85149; font-weight: bold; }}
        .priority-2 {{ color: #f0883e; }}
        .priority-3 {{ color: #d29922; }}
        .period-tag {{ background: #238636; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .period-short {{ background: #f85149; }}
        .period-long {{ background: #1f6feb; }}
    </style>
</head>
<body>
    <h1>📊 韬睿量化 - 股票池报告</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="summary">
        <div class="summary-card">
            <div class="number">{len(self.current_pool.stocks)}</div>
            <div class="label">总股票数</div>
        </div>
        <div class="summary-card">
            <div class="number">{len(classified.get('short', []))}</div>
            <div class="label">短期标的</div>
        </div>
        <div class="summary-card">
            <div class="number">{len(classified.get('medium', []))}</div>
            <div class="label">中期标的</div>
        </div>
        <div class="summary-card">
            <div class="number">{len(classified.get('long', []))}</div>
            <div class="label">长期标的</div>
        </div>
    </div>
    
    <h2>📈 股票列表</h2>
    <table>
        <tr>
            <th>排名</th>
            <th>代码</th>
            <th>名称</th>
            <th>来源</th>
            <th>周期</th>
            <th>优先级</th>
            <th>主线评分</th>
            <th>涨跌幅</th>
            <th>入池原因</th>
        </tr>
'''
        
        for i, stock in enumerate(self.current_pool.get_top_stocks(50), 1):
            period_class = f"period-{stock.period}" if stock.period in ['short', 'long'] else ""
            priority_class = f"priority-{stock.priority}" if stock.priority <= 3 else ""
            
            html += f'''
        <tr>
            <td>{i}</td>
            <td>{stock.code}</td>
            <td>{stock.name}</td>
            <td>{stock.source}</td>
            <td><span class="period-tag {period_class}">{stock.period}</span></td>
            <td class="{priority_class}">{stock.priority}</td>
            <td>{stock.mainline_score:.1f}</td>
            <td>{stock.change_pct:+.2f}%</td>
            <td>{stock.entry_reason[:50]}...</td>
        </tr>
'''
        
        html += '''
    </table>
    
    <h2>📋 来源分布</h2>
    <p>{}</p>
    
    <h2>🔗 与其他模块的衔接</h2>
    <ul>
        <li><strong>前置模块</strong>: 主线识别（五维评分 + 热度评分）</li>
        <li><strong>后续模块</strong>: 因子开发 → 策略生成 → 回测验证 → 实盘交易</li>
    </ul>
    
    <p style="color: #8b949e; margin-top: 30px; text-align: center;">
        韬睿量化系统 - 让投资更智能
    </p>
</body>
</html>
'''.format(self.current_pool.summary.get('by_source', {}))
        
        # 保存报告
        report_path = self.REPORT_DIR / f"pool_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"报告已保存: {report_path}")
        return html
    
    def get_pool_summary(self) -> Dict:
        """获取股票池摘要（供GUI使用）"""
        if not self.current_pool:
            return {"total": 0, "by_source": {}, "by_period": {}}
        
        return {
            "total": len(self.current_pool.stocks),
            "by_source": self.current_pool.summary.get("by_source", {}),
            "by_period": self.current_pool.summary.get("by_period", {}),
            "by_pool_type": self.current_pool.summary.get("by_pool_type", {}),
            "updated_at": self.current_pool.updated_at
        }


# ============================================================
# 便捷函数
# ============================================================

def build_stock_pool(
    include_mainline: bool = True,
    include_tech: bool = True,
    include_external: bool = True,
    period: str = "medium"
) -> StockPool:
    """
    构建股票池的便捷函数
    
    使用方法：
        from markets.ashare.stock_pool import build_stock_pool
        pool = build_stock_pool()
        codes = pool.get_codes()  # 供因子模块使用
    """
    manager = StockPoolManager()
    return manager.build_pool(
        include_mainline=include_mainline,
        include_tech=include_tech,
        include_external=include_external,
        period=period
    )


def get_stock_codes_for_factor() -> List[str]:
    """
    获取股票代码列表供因子模块使用
    
    这是与因子模块衔接的便捷入口
    """
    manager = StockPoolManager()
    return manager.get_stocks_for_factor_module()


def generate_trade_signals(strategy_name: str = "default", top_n: int = 20) -> List[TradeSignal]:
    """
    生成交易信号供策略模块使用
    
    这是与策略模块衔接的便捷入口
    """
    manager = StockPoolManager()
    return manager.generate_signals(strategy_name, top_n)

