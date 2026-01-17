"""
V3.0 投资推荐系统主工作流
========================

完整工作流:
1. 市场趋势分析 (多周期共振+HMM)
2. 主线五维识别 (资金/热度/动量/政策/龙头)
3. 股票池筛选 (A股特征适配)
4. 动量评分 (可扩展接口)
5. 综合排序推荐
6. 交易策略生成
7. HTML报告输出
8. 数据存储归档
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging
import traceback
import pandas as pd

# 确保项目根目录在路径中
PROJECT_ROOT = "/home/taotao/.cursor/worktrees/TRQuant/ope"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logger = logging.getLogger(__name__)


@dataclass
class WorkflowConfig:
    """工作流配置"""
    # 市场趋势
    trend_index: str = "000300.XSHG"
    
    # 筛选风格
    filter_style: str = "balanced"  # conservative/balanced/aggressive/trend/event
    
    # 推荐数量
    top_n_stocks: int = 20
    top_n_mainlines: int = 10
    
    # 数据源
    use_akshare_realtime: bool = True
    use_jqdata: bool = True
    
    # 输出
    output_dir: str = "/home/taotao/.cursor/worktrees/TRQuant/ope/results"
    generate_html: bool = True
    save_to_mongodb: bool = True
    
    # 调试
    verbose: bool = True


class WeeklyAdvisorV3:
    """
    V3.0 本周投资推荐系统
    
    整合所有V3模块的主工作流
    """
    
    def __init__(self, config: WorkflowConfig = None):
        """
        初始化
        
        Args:
            config: 工作流配置
        """
        self.config = config or WorkflowConfig()
        self.results: Dict[str, Any] = {}
        self._workflow_id: str = None
        
        # 初始化各模块
        self._market_trend_analyzer = None
        self._mainline_scorer = None
        self._momentum_scorer = None
        self._stock_filter = None
        self._data_manager = None
        self._report_generator = None
    
    def _log(self, message: str, level: str = "info"):
        """日志输出"""
        if self.config.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
    
    def run(self, date: str = None) -> Dict:
        """
        执行完整工作流
        
        Args:
            date: 目标日期 (默认今天)
            
        Returns:
            完整推荐结果
        """
        date = date or datetime.now().strftime("%Y-%m-%d")
        
        self._log(f"=" * 60)
        self._log(f"V3.0 投资推荐系统 - {date}")
        self._log(f"=" * 60)
        
        try:
            # Step 1: 市场趋势分析
            self._log("\n📈 Step 1: 市场趋势分析...")
            market_trend = self._analyze_market_trend(date)
            self.results["market_trend"] = market_trend
            self._log(f"   趋势方向: {market_trend.get('direction', 'N/A')}")
            self._log(f"   综合评分: {market_trend.get('ensemble_score', 0):.1f}")
            self._log(f"   建议仓位: {market_trend.get('position_limit', 0)*100:.0f}%")
            
            # Step 2: 主线五维识别
            self._log("\n🎯 Step 2: 主线五维识别...")
            mainlines = self._identify_mainlines(date)
            self.results["mainlines"] = mainlines
            self._log(f"   识别主线: {len(mainlines)} 条")
            if mainlines:
                top3 = mainlines[:3]
                for ml in top3:
                    self._log(f"   • {ml.get('name', 'N/A')} ({ml.get('total_score', 0):.1f}分)")
            
            # Step 3: 股票池筛选
            self._log("\n🔍 Step 3: 股票池筛选...")
            filtered_stocks = self._filter_stocks(date, market_trend)
            self.results["filtered_stocks"] = filtered_stocks
            self._log(f"   筛选通过: {len(filtered_stocks)} 只")
            
            # Step 4: 动量评分
            self._log("\n📊 Step 4: 动量评分...")
            scored_stocks = self._score_momentum(filtered_stocks, date)
            self.results["scored_stocks"] = scored_stocks
            self._log(f"   完成评分: {len(scored_stocks)} 只")
            
            # Step 5: 综合排序推荐
            self._log("\n💎 Step 5: 综合排序推荐...")
            recommendations = self._generate_recommendations(
                scored_stocks, market_trend, mainlines
            )
            self.results["recommendations"] = recommendations
            self._log(f"   最终推荐: {len(recommendations.get('stocks', []))} 只")
            
            # Step 6: 交易策略生成
            self._log("\n📋 Step 6: 交易策略生成...")
            trading_strategy = self._generate_trading_strategy(market_trend)
            self.results["trading_strategy"] = trading_strategy
            self._log(f"   仓位建议: {trading_strategy.get('position_advice', 'N/A')}")
            
            # Step 7: HTML报告生成
            if self.config.generate_html:
                self._log("\n📄 Step 7: HTML报告生成...")
                report_path = self._generate_report(date)
                self.results["report_path"] = report_path
                self._log(f"   报告路径: {report_path}")
            
            # Step 8: 数据存储
            if self.config.save_to_mongodb:
                self._log("\n💾 Step 8: 数据存储...")
                self._save_to_database(date)
                self._log(f"   存储完成")
            
            # 完成
            self._log(f"\n{'=' * 60}")
            self._log(f"✅ 工作流完成!")
            self._log(f"{'=' * 60}")
            
            # 输出摘要
            self._print_summary()
            
            return self.results
            
        except Exception as e:
            self._log(f"\n❌ 工作流失败: {e}", "error")
            traceback.print_exc()
            return {"error": str(e)}
    
    def _analyze_market_trend(self, date: str) -> Dict:
        """分析市场趋势"""
        try:
            from .market_trend_v3 import MarketTrendAnalyzerV3
            
            if self._market_trend_analyzer is None:
                self._market_trend_analyzer = MarketTrendAnalyzerV3()
            
            result = self._market_trend_analyzer.analyze(
                index_code=self.config.trend_index,
                as_of_date=date,
            )
            
            return result.to_dict() if result else {}
            
        except Exception as e:
            self._log(f"市场趋势分析失败: {e}", "warning")
            # 返回默认值
            return {
                "ensemble_score": 0,
                "direction": "震荡盘整",
                "position_limit": 0.5,
                "strategy_mode": "观望",
                "holding_period": "中期",
            }
    
    def _identify_mainlines(self, date: str) -> List[Dict]:
        """识别市场主线"""
        try:
            from .mainline_five_dim_v3 import MainlineFiveDimScorerV3
            
            if self._mainline_scorer is None:
                self._mainline_scorer = MainlineFiveDimScorerV3(period="medium")
            
            results = self._mainline_scorer.analyze()
            
            return [r.to_dict() for r in results[:self.config.top_n_mainlines]]
            
        except Exception as e:
            self._log(f"主线识别失败: {e}", "warning")
            return []
    
    def _filter_stocks(self, date: str, market_trend: Dict) -> List[Dict]:
        """筛选股票池"""
        try:
            from .filter_options_v3 import (
                FilterPresets, StockFilterV3, FilterStyle, MarketCondition
            )
            
            # 获取筛选配置
            style = FilterStyle[self.config.filter_style.upper()]
            options = FilterPresets.get_preset(style)
            
            # 根据市场趋势调整
            score = market_trend.get("ensemble_score", 0)
            if score > 30:
                condition = MarketCondition.BULL
            elif score < -30:
                condition = MarketCondition.BEAR
            else:
                condition = MarketCondition.VOLATILE
            
            options = FilterPresets.adapt_to_market(options, condition)
            
            # 获取股票数据
            stocks_data = self._get_stocks_data(date)
            
            # 执行筛选
            if self._stock_filter is None:
                self._stock_filter = StockFilterV3(options)
            else:
                self._stock_filter.options = options
            
            filtered = self._stock_filter.filter_stocks(stocks_data)
            
            return filtered
            
        except Exception as e:
            self._log(f"股票筛选失败: {e}", "warning")
            traceback.print_exc()
            return []
    
    def _get_stocks_data(self, date: str) -> List[Dict]:
        """获取股票数据"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation, indicator
            
            # 获取基本面数据
            q = query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                indicator.roe,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year,
            ).filter(
                valuation.market_cap > 20,
                valuation.market_cap < 1000,
            ).limit(1000)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or df.empty:
                self._log("基本面数据为空", "warning")
                return []
            
            # 获取价格数据
            stocks = df['code'].tolist()[:500]
            
            price_df = jq.get_price(
                stocks,
                end_date=date,
                count=60,
                fields=['close', 'volume', 'high', 'low', 'open'],
                skip_paused=True,
                panel=False,
            )
            
            if price_df is None or price_df.empty:
                self._log("价格数据为空", "warning")
                return []
            
            result = []
            for _, row in df.iterrows():
                stock_code = row['code']
                
                try:
                    # 获取该股票的价格数据
                    stock_prices = price_df[price_df['code'] == stock_code] if 'code' in price_df.columns else None
                    
                    if stock_prices is None or len(stock_prices) < 20:
                        continue
                    
                    close = stock_prices['close'].iloc[-1]
                    close_5d = stock_prices['close'].iloc[-5] if len(stock_prices) >= 5 else close
                    close_20d = stock_prices['close'].iloc[-20] if len(stock_prices) >= 20 else close
                    high_60d = stock_prices['high'].max()
                    low_60d = stock_prices['low'].min()
                    vol_20d = stock_prices['volume'].iloc[-20:].mean() if len(stock_prices) >= 20 else stock_prices['volume'].mean()
                    
                    # 获取股票名称
                    try:
                        info = jq.get_security_info(stock_code)
                        name = info.display_name if info else ""
                    except Exception:
                        name = ""
                    
                    # 安全获取基本面数据
                    raw_roe = row.get('roe')
                    raw_profit_growth = row.get('inc_net_profit_year_on_year')
                    raw_revenue_growth = row.get('inc_revenue_year_on_year')
                    
                    roe = float(raw_roe) / 100 if raw_roe and not pd.isna(raw_roe) else None
                    profit_growth = float(raw_profit_growth) / 100 if raw_profit_growth and not pd.isna(raw_profit_growth) else None
                    revenue_growth = float(raw_revenue_growth) / 100 if raw_revenue_growth and not pd.isna(raw_revenue_growth) else None
                    
                    stock_data = {
                        "code": stock_code,
                        "name": name,
                        "market_cap": float(row.get('market_cap', 0) or 0),
                        "pe_ratio": float(row.get('pe_ratio', 0) or 0),
                        "roe": roe,
                        "profit_growth": profit_growth,
                        "revenue_growth": revenue_growth,
                        "mom_5d": (close - close_5d) / close_5d if close_5d > 0 else 0,
                        "mom_20d": (close - close_20d) / close_20d if close_20d > 0 else 0,
                        "price_pos_60d": (close - low_60d) / (high_60d - low_60d) if high_60d > low_60d else 0.5,
                        "vol_ratio": stock_prices['volume'].iloc[-1] / vol_20d if vol_20d > 0 else 1,
                        "above_ma20": close > stock_prices['close'].iloc[-20:].mean() if len(stock_prices) >= 20 else False,
                        "close": close,
                        "industry": "",  # TODO: 获取行业
                        "list_days": 1000,  # TODO: 获取上市天数
                        "turnover": 0.01,
                        "avg_amount": stock_prices['volume'].mean() * close / 10000 if close else 0,
                        "industry_score": 60,  # 默认行业分数
                    }
                    result.append(stock_data)
                    
                except Exception as e:
                    continue
            
            self._log(f"   获取股票数据: {len(result)} 只")
            return result
            
        except Exception as e:
            self._log(f"获取股票数据失败: {e}", "warning")
            traceback.print_exc()
            return []
    
    def _score_momentum(self, stocks: List[Dict], date: str) -> List[Dict]:
        """动量评分"""
        try:
            from .momentum_scorer_v3 import MomentumScorerV3
            
            if self._momentum_scorer is None:
                self._momentum_scorer = MomentumScorerV3()
            
            # 转换数据格式
            stocks_dict = {s["code"]: s for s in stocks}
            
            results = self._momentum_scorer.score_stocks(stocks_dict)
            
            # 合并评分结果
            scored = []
            for r in results:
                stock = stocks_dict.get(r.stock_code, {})
                stock["momentum_score"] = r.total_score
                stock["momentum_rating"] = r.rating
                stock["momentum_signal"] = r.signal
                stock["factor_scores"] = r.factor_scores
                scored.append(stock)
            
            return scored
            
        except Exception as e:
            self._log(f"动量评分失败: {e}", "warning")
            return stocks
    
    def _generate_recommendations(
        self,
        scored_stocks: List[Dict],
        market_trend: Dict,
        mainlines: List[Dict],
    ) -> Dict:
        """生成推荐"""
        # 综合评分
        for stock in scored_stocks:
            # 基本面分数 (40%)
            fundamental_score = 0
            if stock.get("roe", 0) > 0.15:
                fundamental_score += 30
            if stock.get("profit_growth", 0) > 0.20:
                fundamental_score += 30
            if stock.get("revenue_growth", 0) > 0.15:
                fundamental_score += 20
            pe = stock.get("pe_ratio", 0)
            if pe and 10 < pe < 40:
                fundamental_score += 20
            
            # 动量分数 (40%)
            momentum_score = stock.get("momentum_score", 50)
            
            # 主线加分 (20%)
            mainline_bonus = 0
            # TODO: 根据所属行业与主线匹配加分
            
            # 综合分数
            stock["total_score"] = (
                fundamental_score * 0.4 +
                momentum_score * 0.4 +
                mainline_bonus * 0.2
            )
            
            # 信号
            total = stock["total_score"]
            if total >= 75:
                stock["signal"] = "强买"
            elif total >= 60:
                stock["signal"] = "买入"
            elif total >= 45:
                stock["signal"] = "持有"
            else:
                stock["signal"] = "观察"
        
        # 排序
        scored_stocks.sort(key=lambda x: x.get("total_score", 0), reverse=True)
        
        # 取前N
        top_stocks = scored_stocks[:self.config.top_n_stocks]
        
        return {
            "stocks": top_stocks,
            "count": len(top_stocks),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
    
    def _generate_trading_strategy(self, market_trend: Dict) -> Dict:
        """生成交易策略"""
        score = market_trend.get("ensemble_score", 0)
        position_limit = market_trend.get("position_limit", 0.5)
        
        # 仓位建议
        if score > 30:
            position_advice = f"牛市行情，建议仓位{position_limit*100:.0f}%，可积极参与"
        elif score < -30:
            position_advice = f"熊市行情，建议仓位{position_limit*100:.0f}%，以防守为主"
        else:
            position_advice = f"震荡行情，建议仓位{position_limit*100:.0f}%，灵活操作"
        
        # 入场策略
        if score > 30:
            entry_strategy = [
                "关注突破形态，顺势买入",
                "回调至支撑位可加仓",
                "优先选择主线板块龙头",
            ]
        elif score < -30:
            entry_strategy = [
                "严格控制建仓节奏",
                "等待明确企稳信号",
                "只做超跌反弹，快进快出",
            ]
        else:
            entry_strategy = [
                "逢低建仓，分批买入",
                "关注箱体震荡的支撑位",
                "选择相对强势个股",
            ]
        
        # 出场策略
        if score > 30:
            exit_strategy = [
                "设置跟踪止盈，保护利润",
                "涨幅超预期可适当减仓",
                "破位坚决止损",
            ]
        elif score < -30:
            exit_strategy = [
                "快速止盈，落袋为安",
                "严格止损，不恋战",
                "反弹到压力位减仓",
            ]
        else:
            exit_strategy = [
                "箱体高位减仓",
                "设定目标止盈位",
                "跌破支撑及时止损",
            ]
        
        # 风控策略
        risk_control = [
            f"单只股票仓位不超过{min(20, int(100/self.config.top_n_stocks*2))}%",
            f"总仓位控制在{position_limit*100:.0f}%以内",
            "严格执行止损纪律，单笔止损不超过8%",
            "分批建仓分批出场，避免一次性重仓",
        ]
        
        return {
            "position_advice": position_advice,
            "entry_strategy": entry_strategy,
            "exit_strategy": exit_strategy,
            "risk_control": risk_control,
        }
    
    def _generate_report(self, date: str) -> str:
        """生成HTML报告"""
        try:
            from .report_generator_v3 import ReportGeneratorV3
            
            if self._report_generator is None:
                self._report_generator = ReportGeneratorV3(
                    output_dir=self.config.output_dir
                )
            
            report_data = {
                "date": date,
                "market_trend": self.results.get("market_trend", {}),
                "mainlines": self.results.get("mainlines", []),
                "recommendations": self.results.get("recommendations", {}),
                "trading_strategy": self.results.get("trading_strategy", {}),
            }
            
            return self._report_generator.generate(report_data)
            
        except Exception as e:
            self._log(f"报告生成失败: {e}", "warning")
            return ""
    
    def _save_to_database(self, date: str):
        """保存到数据库"""
        try:
            from .data_manager_v3 import DataManagerV3
            
            if self._data_manager is None:
                self._data_manager = DataManagerV3()
            
            # 保存市场趋势
            self._data_manager.save_market_trend(
                date, self.results.get("market_trend", {})
            )
            
            # 保存主线
            self._data_manager.save_mainlines(
                date, self.results.get("mainlines", [])
            )
            
            # 保存推荐
            self._data_manager.save_recommendations(
                date, self.results.get("recommendations", {})
            )
            
        except Exception as e:
            self._log(f"数据保存失败: {e}", "warning")
    
    def _print_summary(self):
        """打印摘要"""
        recommendations = self.results.get("recommendations", {})
        stocks = recommendations.get("stocks", [])[:5]
        
        print("\n" + "=" * 60)
        print("📊 本周推荐摘要")
        print("=" * 60)
        
        trend = self.results.get("market_trend", {})
        print(f"\n🎯 市场趋势: {trend.get('direction', 'N/A')} (评分: {trend.get('ensemble_score', 0):.1f})")
        print(f"💰 建议仓位: {trend.get('position_limit', 0)*100:.0f}%")
        
        print("\n🏆 Top 5 推荐股票:")
        for i, stock in enumerate(stocks):
            print(f"   {i+1}. {stock.get('name', stock.get('code', 'N/A'))} "
                  f"({stock.get('code', '')}) - "
                  f"{stock.get('total_score', 0):.1f}分 [{stock.get('signal', 'N/A')}]")
        
        strategy = self.results.get("trading_strategy", {})
        print(f"\n📋 交易建议: {strategy.get('position_advice', 'N/A')}")
        
        if self.results.get("report_path"):
            print(f"\n📄 完整报告: {self.results.get('report_path')}")
        
        print("=" * 60 + "\n")


# ============ 便捷函数 ============

def run_weekly_advisor(
    date: str = None,
    filter_style: str = "balanced",
    verbose: bool = True,
) -> Dict:
    """
    便捷函数：运行本周投资推荐
    
    Args:
        date: 目标日期 (默认今天)
        filter_style: 筛选风格
        verbose: 是否打印详情
        
    Returns:
        推荐结果
    """
    config = WorkflowConfig(
        filter_style=filter_style,
        verbose=verbose,
    )
    
    advisor = WeeklyAdvisorV3(config)
    return advisor.run(date)


# ============ 主程序入口 ============

if __name__ == "__main__":
    import jqdatasdk as jq
    
    # JQData认证
    try:
        from config.config_manager import get_config_manager
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        print("JQData认证成功")
    except Exception as e:
        print(f"JQData认证失败: {e}")
        print("请先配置JQData账号")
        sys.exit(1)
    
    # 运行推荐
    result = run_weekly_advisor()
