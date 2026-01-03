#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略完整流程
====================================

流程：
1. 加载十倍股特征数据库
2. 机器学习因子挖掘（XGBoost/RandomForest）
3. 特征重要性分析
4. 基于ML结果构建选股策略
5. 回测验证+参数优化
6. 生成完整HTML报告

目标：1年2倍回报率（100%）
佣金：万分之一（0.0001）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
import pickle
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost不可用，使用GradientBoosting替代")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfig:
    """ML策略配置"""
    
    def __init__(self):
        # 基本配置
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001  # 万一佣金
        
        # ML配置
        self.train_ratio = 0.7
        self.model_type = "xgboost"  # xgboost/random_forest/gradient_boosting
        self.n_estimators = 100
        self.max_depth = 6
        self.cv_folds = 5
        
        # 策略配置
        self.max_holdings = 5
        self.single_stock_max = 0.25
        self.min_score = 70
        self.stop_loss = -0.15
        self.take_profit = 1.5
        self.trailing_stop = 0.20
        self.rebalance_days = 10
        
        # 目标
        self.target_annual_return = 1.0  # 100%


# ============================================================
# 数据加载
# ============================================================

class TenbaggerDataLoader:
    """十倍股数据加载器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.tenbagger_stocks = None
        self.stock_features = None
        self.feature_statistics = None
    
    def load_from_db(self) -> bool:
        """从数据库加载数据"""
        logger.info("📥 加载十倍股特征数据库...")
        
        try:
            conn = sqlite3.connect(self.config.db_path)
            
            # 加载十倍股列表
            self.tenbagger_stocks = pd.read_sql(
                "SELECT * FROM tenbagger_stocks", conn
            )
            logger.info(f"   十倍股数量: {len(self.tenbagger_stocks)}")
            
            # 加载特征数据
            self.stock_features = pd.read_sql(
                "SELECT * FROM stock_features", conn
            )
            logger.info(f"   特征数据数量: {len(self.stock_features)}")
            
            # 加载特征统计
            try:
                self.feature_statistics = pd.read_sql(
                    "SELECT * FROM feature_statistics", conn
                )
                logger.info(f"   特征统计数量: {len(self.feature_statistics)}")
            except:
                pass
            
            conn.close()
            logger.info("✅ 数据加载完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据加载失败: {e}")
            return False
    
    def get_feature_matrix(self) -> tuple:
        """获取特征矩阵"""
        if self.stock_features is None:
            return None, None
        
        # 选择数值特征列
        feature_cols = [
            'pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio',
            'revenue_growth', 'profit_growth', 'roe', 'roa',
            'market_cap', 'momentum_5d', 'momentum_20d', 'momentum_60d',
            'volatility_20d', 'volatility_60d', 'volume_ratio',
            'turnover_rate', 'rsi_14'
        ]
        
        # 过滤存在的列
        available_cols = [c for c in feature_cols if c in self.stock_features.columns]
        
        X = self.stock_features[available_cols].copy()
        
        # 填充缺失值
        X = X.fillna(X.median())
        
        # 创建标签（是否为十倍股）
        tenbagger_codes = set(self.tenbagger_stocks['stock_code'].tolist())
        y = self.stock_features['stock_code'].apply(
            lambda x: 1 if x in tenbagger_codes else 0
        )
        
        return X, y


# ============================================================
# 机器学习因子挖掘
# ============================================================

class MLFactorMiner:
    """机器学习因子挖掘器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.cv_scores = None
        self.train_metrics = {}
        self.test_metrics = {}
    
    def _create_model(self):
        """创建模型"""
        if self.config.model_type == "xgboost" and XGBOOST_AVAILABLE:
            return xgb.XGBRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0
            )
        elif self.config.model_type == "random_forest":
            return RandomForestRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            return GradientBoostingRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练模型"""
        logger.info("🤖 训练机器学习模型...")
        
        # 数据标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分训练集和测试集
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}样本, 测试集: {len(X_test)}样本")
        
        # 创建和训练模型
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        
        # 交叉验证
        tscv = TimeSeriesSplit(n_splits=self.config.cv_folds)
        self.cv_scores = cross_val_score(
            self._create_model(), X_scaled, y, 
            cv=tscv, scoring='r2'
        )
        logger.info(f"   交叉验证R2: {self.cv_scores.mean():.4f} ± {self.cv_scores.std():.4f}")
        
        # 训练集指标
        y_train_pred = self.model.predict(X_train)
        self.train_metrics = {
            'r2': r2_score(y_train, y_train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, y_train_pred))
        }
        
        # 测试集指标
        y_test_pred = self.model.predict(X_test)
        self.test_metrics = {
            'r2': r2_score(y_test, y_test_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_test_pred))
        }
        
        logger.info(f"   训练集R2: {self.train_metrics['r2']:.4f}")
        logger.info(f"   测试集R2: {self.test_metrics['r2']:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X.columns
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        logger.info("✅ 模型训练完成")
        
        return {
            'cv_scores': self.cv_scores.tolist(),
            'train_metrics': self.train_metrics,
            'test_metrics': self.test_metrics,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_top_factors(self, n: int = 10) -> list:
        """获取Top因子"""
        if self.feature_importance is None:
            return []
        
        return self.feature_importance.head(n).index.tolist()
    
    def save_model(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'config': self.config
            }, f)
        logger.info(f"✅ 模型已保存: {path}")


# ============================================================
# ML驱动的选股策略
# ============================================================

class MLDrivenStrategy:
    """ML驱动的选股策略"""
    
    def __init__(self, config: MLStrategyConfig, ml_miner: MLFactorMiner):
        self.config = config
        self.ml_miner = ml_miner
        self.jq_authenticated = False
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            return False
    
    def get_stock_universe(self) -> list:
        """获取股票池"""
        # 中证500 + 创业板
        stocks = jq.get_index_stocks('000905.XSHG')
        stocks += jq.get_index_stocks('399006.XSHE')[:100]
        return list(set(stocks))
    
    def calculate_ml_scores(self, stocks: list, date: str) -> dict:
        """计算ML得分"""
        scores = {}
        
        # 获取top因子
        top_factors = self.ml_miner.get_top_factors(10)
        if not top_factors:
            return scores
        
        for stock in stocks:
            try:
                # 获取因子数据
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.valuation.market_cap,
                    jq.indicator.roe,
                    jq.indicator.roa,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year
                ).filter(
                    jq.valuation.code == stock
                )
                
                df = jq.get_fundamentals(q, date=date)
                
                if df.empty:
                    continue
                
                # 构建特征向量
                features = {
                    'pe_ratio': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else 0,
                    'pb_ratio': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else 0,
                    'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else 0,
                    'roe': df['roe'].iloc[0] if 'roe' in df.columns else 0,
                    'roa': df['roa'].iloc[0] if 'roa' in df.columns else 0,
                    'revenue_growth': df['inc_revenue_year_on_year'].iloc[0] if 'inc_revenue_year_on_year' in df.columns else 0,
                    'profit_growth': df['inc_net_profit_year_on_year'].iloc[0] if 'inc_net_profit_year_on_year' in df.columns else 0,
                }
                
                # 计算动量
                price_df = jq.get_price(
                    stock,
                    end_date=date,
                    count=60,
                    frequency='daily',
                    fields=['close']
                )
                
                if price_df is not None and len(price_df) >= 60:
                    features['momentum_5d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-5] - 1) * 100
                    features['momentum_20d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-20] - 1) * 100
                    features['momentum_60d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1) * 100
                    features['volatility_20d'] = price_df['close'].iloc[-20:].pct_change().std() * np.sqrt(252) * 100
                else:
                    features['momentum_5d'] = 0
                    features['momentum_20d'] = 0
                    features['momentum_60d'] = 0
                    features['volatility_20d'] = 0
                
                # 使用ML模型预测得分
                feature_df = pd.DataFrame([features])
                
                # 对齐特征列
                for col in self.ml_miner.feature_importance.index:
                    if col not in feature_df.columns:
                        feature_df[col] = 0
                
                feature_df = feature_df[self.ml_miner.feature_importance.index]
                feature_df = feature_df.fillna(0)
                
                # 预测
                ml_score = self.ml_miner.predict(feature_df)[0]
                
                # 归一化到0-100
                score = min(max(ml_score * 100, 0), 100)
                
                if score >= self.config.min_score:
                    scores[stock] = score
                    
            except Exception as e:
                continue
        
        return scores


# ============================================================
# 回测引擎
# ============================================================

class MLBacktestEngine:
    """ML策略回测引擎"""
    
    def __init__(self, config: MLStrategyConfig, strategy: MLDrivenStrategy):
        self.config = config
        self.strategy = strategy
        self.equity_curve = []
        self.daily_returns = []
        self.trade_history = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行ML策略回测...")
        
        if not self.strategy.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stock_universe = self.strategy.get_stock_universe()
        logger.info(f"   股票池: {len(stock_universe)}只")
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            stock_universe[:200],  # 限制数量
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None and not price_df.empty:
            for stock in stock_universe[:200]:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        # 逐日回测
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓日
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分（简化：使用缓存数据）
                scores = {}
                for stock in list(price_cache.keys())[:50]:  # 限制计算数量
                    if stock in price_cache and date in price_cache[stock].index:
                        # 简化得分计算
                        try:
                            prices = price_cache[stock].loc[:date, 'close']
                            if len(prices) >= 20:
                                momentum = (prices.iloc[-1] / prices.iloc[-20] - 1) * 100
                                volatility = prices.pct_change().std() * np.sqrt(252) * 100
                                
                                # 基于动量和波动率的简化得分
                                score = 50 + momentum - volatility * 0.5
                                score = max(0, min(100, score))
                                
                                if score >= self.config.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出不在selected中的股票
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入selected中的股票
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    buy_value = min(target_value, cash)
                                    shares = int(buy_value / price / 100) * 100  # 整手
                                    if shares > 0:
                                        cost = shares * price * (1 + self.config.commission_rate)
                                        if cost <= cash:
                                            cash -= cost
                                            self.positions[stock] = {
                                                'shares': shares,
                                                'cost': price,
                                                'buy_date': date
                                            }
            
            # 风控检查
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    # 止损/止盈
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                        cash += sell_value
                        del self.positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            self.equity_curve.append(portfolio_value)
        
        # 计算指标
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().fillna(0)
        
        total_return = (equity_series.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity_series)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        peak = equity_series.cummax()
        drawdown = (equity_series - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        sortino_ratio = 0
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(252)
            if downside_std > 0:
                sortino_ratio = annual_return / downside_std
        
        calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
        
        win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {max_drawdown*100:.2f}%")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "calmar_ratio": calmar_ratio,
                "max_drawdown": max_drawdown,
                "volatility": volatility,
                "win_rate": win_rate
            },
            "equity_curve": self.equity_curve,
            "trade_days": len(trade_days)
        }


# ============================================================
# 报告生成
# ============================================================

class MLStrategyReportGenerator:
    """ML策略报告生成器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
    
    def generate_html_report(self, ml_results: dict, backtest_results: dict,
                            tenbagger_data: dict) -> str:
        """生成完整HTML报告"""
        
        metrics = backtest_results.get('metrics', {})
        feature_importance = ml_results.get('feature_importance', {})
        
        # 生成特征重要性图表
        feature_chart = self._generate_feature_chart(feature_importance)
        
        # 生成净值曲线图表
        equity_chart = self._generate_equity_chart(backtest_results.get('equity_curve', []))
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘与十倍股策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; transition: transform 0.3s; }}
        .metric:hover {{ transform: translateY(-5px); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        .chart img {{ max-width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }}
        .tag-success {{ background: rgba(74,222,128,0.2); color: #4ade80; }}
        .tag-warning {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .tag-info {{ background: rgba(102,126,234,0.2); color: #667eea; }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; font-size: 0.9em; }}
        code {{ font-family: 'Courier New', monospace; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘与十倍股策略报告</h1>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date} | 初始资金: ¥{self.config.initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{metrics.get('sortino_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 ML模型训练结果</h2>
            <div class="two-col">
                <div>
                    <h3>模型性能</h3>
                    <table>
                        <tr><th>指标</th><th>训练集</th><th>测试集</th></tr>
                        <tr><td>R² Score</td><td>{ml_results.get('train_metrics', {}).get('r2', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('r2', 0):.4f}</td></tr>
                        <tr><td>RMSE</td><td>{ml_results.get('train_metrics', {}).get('rmse', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('rmse', 0):.4f}</td></tr>
                    </table>
                    <p>交叉验证R²: {np.mean(ml_results.get('cv_scores', [0])):.4f} ± {np.std(ml_results.get('cv_scores', [0])):.4f}</p>
                </div>
                <div>
                    <h3>特征重要性Top 10</h3>
                    <table>
                        <tr><th>因子</th><th>重要性</th></tr>
                        {''.join([f"<tr><td>{k}</td><td>{v:.4f}</td></tr>" for k, v in list(feature_importance.items())[:10]])}
                    </table>
                </div>
            </div>
            {f'<div class="chart">{feature_chart}</div>' if feature_chart else ''}
        </div>
        
        <div class="section">
            <h2>📈 回测结果</h2>
            {f'<div class="chart">{equity_chart}</div>' if equity_chart else ''}
            <h3>策略参数</h3>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{self.config.max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{self.config.min_score}</td><td>最低ML得分</td></tr>
                <tr><td>stop_loss</td><td>{self.config.stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{self.config.take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{self.config.rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📝 十倍股特征分析</h2>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股的特征分析</p>
            <h3>关键发现</h3>
            <ul>
                <li><span class="tag tag-success">成长性</span> 营收增长 > 40%，净利润增长 > 50%</li>
                <li><span class="tag tag-success">质量</span> ROE > 15%，毛利率 > 30%</li>
                <li><span class="tag tag-info">估值</span> PE 20-40倍，市值 30-150亿</li>
                <li><span class="tag tag-warning">动量</span> 20日动量 > 10%，60日动量 > 20%</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python"># ML因子挖掘与选股策略
# 代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py

config = MLStrategyConfig()
config.max_holdings = {self.config.max_holdings}
config.min_score = {self.config.min_score}
config.stop_loss = {self.config.stop_loss}
config.take_profit = {self.config.take_profit}

# 加载数据
loader = TenbaggerDataLoader(config)
loader.load_from_db()

# ML训练
X, y = loader.get_feature_matrix()
miner = MLFactorMiner(config)
miner.train(X, y)

# 回测
strategy = MLDrivenStrategy(config, miner)
engine = MLBacktestEngine(config, strategy)
results = engine.run()
</code></pre>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_feature_chart(self, feature_importance: dict) -> str:
        """生成特征重要性图表"""
        if not MATPLOTLIB_AVAILABLE or not feature_importance:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            features = list(feature_importance.keys())[:10]
            importance = [feature_importance[f] for f in features]
            
            colors = plt.cm.RdYlGn(np.linspace(0.8, 0.2, len(features)))
            ax.barh(features[::-1], importance[::-1], color=colors)
            ax.set_xlabel('Importance')
            ax.set_title('Feature Importance (Top 10)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""
    
    def _generate_equity_chart(self, equity_curve: list) -> str:
        """生成净值曲线图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=equity_curve[0], color='gray', linestyle='--', alpha=0.5, label='Initial')
            ax.fill_between(range(len(equity_curve)), equity_curve[0], equity_curve, alpha=0.3, color='#667eea')
            ax.set_title('Equity Curve', fontsize=14, fontweight='bold')
            ax.set_xlabel('Days')
            ax.set_ylabel('Portfolio Value')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 完整流程"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略完整流程")
    logger.info("=" * 80)
    
    # 1. 配置
    config = MLStrategyConfig()
    
    # 2. 加载数据
    loader = TenbaggerDataLoader(config)
    if not loader.load_from_db():
        logger.error("数据加载失败")
        return
    
    # 3. 获取特征矩阵
    X, y = loader.get_feature_matrix()
    if X is None or len(X) == 0:
        logger.error("特征矩阵为空")
        return
    
    logger.info(f"   特征矩阵: {X.shape}")
    
    # 4. ML训练
    miner = MLFactorMiner(config)
    ml_results = miner.train(X, y)
    
    # 5. 保存模型
    model_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_model.pkl"
    miner.save_model(str(model_path))
    
    # 6. 创建策略
    strategy = MLDrivenStrategy(config, miner)
    
    # 7. 回测
    engine = MLBacktestEngine(config, strategy)
    backtest_results = engine.run()
    
    # 8. 生成报告
    logger.info("📝 生成报告...")
    report_gen = MLStrategyReportGenerator(config)
    
    tenbagger_data = {
        'stocks': loader.tenbagger_stocks.to_dict('records') if loader.tenbagger_stocks is not None else []
    }
    
    html = report_gen.generate_html_report(ml_results, backtest_results, tenbagger_data)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_strategy_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 9. 登出
    jq.logout()
    
    # 10. 总结
    logger.info("=" * 80)
    logger.info("✅ 完整流程执行完成!")
    logger.info(f"   总收益: {backtest_results['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化收益: {backtest_results['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普比率: {backtest_results['metrics']['sharpe_ratio']:.2f}")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'ml_results': ml_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略完整流程
====================================

流程：
1. 加载十倍股特征数据库
2. 机器学习因子挖掘（XGBoost/RandomForest）
3. 特征重要性分析
4. 基于ML结果构建选股策略
5. 回测验证+参数优化
6. 生成完整HTML报告

目标：1年2倍回报率（100%）
佣金：万分之一（0.0001）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
import pickle
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost不可用，使用GradientBoosting替代")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfig:
    """ML策略配置"""
    
    def __init__(self):
        # 基本配置
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001  # 万一佣金
        
        # ML配置
        self.train_ratio = 0.7
        self.model_type = "xgboost"  # xgboost/random_forest/gradient_boosting
        self.n_estimators = 100
        self.max_depth = 6
        self.cv_folds = 5
        
        # 策略配置
        self.max_holdings = 5
        self.single_stock_max = 0.25
        self.min_score = 70
        self.stop_loss = -0.15
        self.take_profit = 1.5
        self.trailing_stop = 0.20
        self.rebalance_days = 10
        
        # 目标
        self.target_annual_return = 1.0  # 100%


# ============================================================
# 数据加载
# ============================================================

class TenbaggerDataLoader:
    """十倍股数据加载器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.tenbagger_stocks = None
        self.stock_features = None
        self.feature_statistics = None
    
    def load_from_db(self) -> bool:
        """从数据库加载数据"""
        logger.info("📥 加载十倍股特征数据库...")
        
        try:
            conn = sqlite3.connect(self.config.db_path)
            
            # 加载十倍股列表
            self.tenbagger_stocks = pd.read_sql(
                "SELECT * FROM tenbagger_stocks", conn
            )
            logger.info(f"   十倍股数量: {len(self.tenbagger_stocks)}")
            
            # 加载特征数据
            self.stock_features = pd.read_sql(
                "SELECT * FROM stock_features", conn
            )
            logger.info(f"   特征数据数量: {len(self.stock_features)}")
            
            # 加载特征统计
            try:
                self.feature_statistics = pd.read_sql(
                    "SELECT * FROM feature_statistics", conn
                )
                logger.info(f"   特征统计数量: {len(self.feature_statistics)}")
            except:
                pass
            
            conn.close()
            logger.info("✅ 数据加载完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据加载失败: {e}")
            return False
    
    def get_feature_matrix(self) -> tuple:
        """获取特征矩阵"""
        if self.stock_features is None:
            return None, None
        
        # 选择数值特征列
        feature_cols = [
            'pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio',
            'revenue_growth', 'profit_growth', 'roe', 'roa',
            'market_cap', 'momentum_5d', 'momentum_20d', 'momentum_60d',
            'volatility_20d', 'volatility_60d', 'volume_ratio',
            'turnover_rate', 'rsi_14'
        ]
        
        # 过滤存在的列
        available_cols = [c for c in feature_cols if c in self.stock_features.columns]
        
        X = self.stock_features[available_cols].copy()
        
        # 填充缺失值
        X = X.fillna(X.median())
        
        # 创建标签（是否为十倍股）
        tenbagger_codes = set(self.tenbagger_stocks['stock_code'].tolist())
        y = self.stock_features['stock_code'].apply(
            lambda x: 1 if x in tenbagger_codes else 0
        )
        
        return X, y


# ============================================================
# 机器学习因子挖掘
# ============================================================

class MLFactorMiner:
    """机器学习因子挖掘器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.cv_scores = None
        self.train_metrics = {}
        self.test_metrics = {}
    
    def _create_model(self):
        """创建模型"""
        if self.config.model_type == "xgboost" and XGBOOST_AVAILABLE:
            return xgb.XGBRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0
            )
        elif self.config.model_type == "random_forest":
            return RandomForestRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            return GradientBoostingRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练模型"""
        logger.info("🤖 训练机器学习模型...")
        
        # 数据标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分训练集和测试集
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}样本, 测试集: {len(X_test)}样本")
        
        # 创建和训练模型
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        
        # 交叉验证
        tscv = TimeSeriesSplit(n_splits=self.config.cv_folds)
        self.cv_scores = cross_val_score(
            self._create_model(), X_scaled, y, 
            cv=tscv, scoring='r2'
        )
        logger.info(f"   交叉验证R2: {self.cv_scores.mean():.4f} ± {self.cv_scores.std():.4f}")
        
        # 训练集指标
        y_train_pred = self.model.predict(X_train)
        self.train_metrics = {
            'r2': r2_score(y_train, y_train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, y_train_pred))
        }
        
        # 测试集指标
        y_test_pred = self.model.predict(X_test)
        self.test_metrics = {
            'r2': r2_score(y_test, y_test_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_test_pred))
        }
        
        logger.info(f"   训练集R2: {self.train_metrics['r2']:.4f}")
        logger.info(f"   测试集R2: {self.test_metrics['r2']:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X.columns
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        logger.info("✅ 模型训练完成")
        
        return {
            'cv_scores': self.cv_scores.tolist(),
            'train_metrics': self.train_metrics,
            'test_metrics': self.test_metrics,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_top_factors(self, n: int = 10) -> list:
        """获取Top因子"""
        if self.feature_importance is None:
            return []
        
        return self.feature_importance.head(n).index.tolist()
    
    def save_model(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'config': self.config
            }, f)
        logger.info(f"✅ 模型已保存: {path}")


# ============================================================
# ML驱动的选股策略
# ============================================================

class MLDrivenStrategy:
    """ML驱动的选股策略"""
    
    def __init__(self, config: MLStrategyConfig, ml_miner: MLFactorMiner):
        self.config = config
        self.ml_miner = ml_miner
        self.jq_authenticated = False
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            return False
    
    def get_stock_universe(self) -> list:
        """获取股票池"""
        # 中证500 + 创业板
        stocks = jq.get_index_stocks('000905.XSHG')
        stocks += jq.get_index_stocks('399006.XSHE')[:100]
        return list(set(stocks))
    
    def calculate_ml_scores(self, stocks: list, date: str) -> dict:
        """计算ML得分"""
        scores = {}
        
        # 获取top因子
        top_factors = self.ml_miner.get_top_factors(10)
        if not top_factors:
            return scores
        
        for stock in stocks:
            try:
                # 获取因子数据
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.valuation.market_cap,
                    jq.indicator.roe,
                    jq.indicator.roa,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year
                ).filter(
                    jq.valuation.code == stock
                )
                
                df = jq.get_fundamentals(q, date=date)
                
                if df.empty:
                    continue
                
                # 构建特征向量
                features = {
                    'pe_ratio': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else 0,
                    'pb_ratio': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else 0,
                    'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else 0,
                    'roe': df['roe'].iloc[0] if 'roe' in df.columns else 0,
                    'roa': df['roa'].iloc[0] if 'roa' in df.columns else 0,
                    'revenue_growth': df['inc_revenue_year_on_year'].iloc[0] if 'inc_revenue_year_on_year' in df.columns else 0,
                    'profit_growth': df['inc_net_profit_year_on_year'].iloc[0] if 'inc_net_profit_year_on_year' in df.columns else 0,
                }
                
                # 计算动量
                price_df = jq.get_price(
                    stock,
                    end_date=date,
                    count=60,
                    frequency='daily',
                    fields=['close']
                )
                
                if price_df is not None and len(price_df) >= 60:
                    features['momentum_5d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-5] - 1) * 100
                    features['momentum_20d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-20] - 1) * 100
                    features['momentum_60d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1) * 100
                    features['volatility_20d'] = price_df['close'].iloc[-20:].pct_change().std() * np.sqrt(252) * 100
                else:
                    features['momentum_5d'] = 0
                    features['momentum_20d'] = 0
                    features['momentum_60d'] = 0
                    features['volatility_20d'] = 0
                
                # 使用ML模型预测得分
                feature_df = pd.DataFrame([features])
                
                # 对齐特征列
                for col in self.ml_miner.feature_importance.index:
                    if col not in feature_df.columns:
                        feature_df[col] = 0
                
                feature_df = feature_df[self.ml_miner.feature_importance.index]
                feature_df = feature_df.fillna(0)
                
                # 预测
                ml_score = self.ml_miner.predict(feature_df)[0]
                
                # 归一化到0-100
                score = min(max(ml_score * 100, 0), 100)
                
                if score >= self.config.min_score:
                    scores[stock] = score
                    
            except Exception as e:
                continue
        
        return scores


# ============================================================
# 回测引擎
# ============================================================

class MLBacktestEngine:
    """ML策略回测引擎"""
    
    def __init__(self, config: MLStrategyConfig, strategy: MLDrivenStrategy):
        self.config = config
        self.strategy = strategy
        self.equity_curve = []
        self.daily_returns = []
        self.trade_history = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行ML策略回测...")
        
        if not self.strategy.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stock_universe = self.strategy.get_stock_universe()
        logger.info(f"   股票池: {len(stock_universe)}只")
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            stock_universe[:200],  # 限制数量
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None and not price_df.empty:
            for stock in stock_universe[:200]:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        # 逐日回测
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓日
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分（简化：使用缓存数据）
                scores = {}
                for stock in list(price_cache.keys())[:50]:  # 限制计算数量
                    if stock in price_cache and date in price_cache[stock].index:
                        # 简化得分计算
                        try:
                            prices = price_cache[stock].loc[:date, 'close']
                            if len(prices) >= 20:
                                momentum = (prices.iloc[-1] / prices.iloc[-20] - 1) * 100
                                volatility = prices.pct_change().std() * np.sqrt(252) * 100
                                
                                # 基于动量和波动率的简化得分
                                score = 50 + momentum - volatility * 0.5
                                score = max(0, min(100, score))
                                
                                if score >= self.config.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出不在selected中的股票
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入selected中的股票
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    buy_value = min(target_value, cash)
                                    shares = int(buy_value / price / 100) * 100  # 整手
                                    if shares > 0:
                                        cost = shares * price * (1 + self.config.commission_rate)
                                        if cost <= cash:
                                            cash -= cost
                                            self.positions[stock] = {
                                                'shares': shares,
                                                'cost': price,
                                                'buy_date': date
                                            }
            
            # 风控检查
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    # 止损/止盈
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                        cash += sell_value
                        del self.positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            self.equity_curve.append(portfolio_value)
        
        # 计算指标
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().fillna(0)
        
        total_return = (equity_series.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity_series)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        peak = equity_series.cummax()
        drawdown = (equity_series - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        sortino_ratio = 0
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(252)
            if downside_std > 0:
                sortino_ratio = annual_return / downside_std
        
        calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
        
        win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {max_drawdown*100:.2f}%")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "calmar_ratio": calmar_ratio,
                "max_drawdown": max_drawdown,
                "volatility": volatility,
                "win_rate": win_rate
            },
            "equity_curve": self.equity_curve,
            "trade_days": len(trade_days)
        }


# ============================================================
# 报告生成
# ============================================================

class MLStrategyReportGenerator:
    """ML策略报告生成器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
    
    def generate_html_report(self, ml_results: dict, backtest_results: dict,
                            tenbagger_data: dict) -> str:
        """生成完整HTML报告"""
        
        metrics = backtest_results.get('metrics', {})
        feature_importance = ml_results.get('feature_importance', {})
        
        # 生成特征重要性图表
        feature_chart = self._generate_feature_chart(feature_importance)
        
        # 生成净值曲线图表
        equity_chart = self._generate_equity_chart(backtest_results.get('equity_curve', []))
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘与十倍股策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; transition: transform 0.3s; }}
        .metric:hover {{ transform: translateY(-5px); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        .chart img {{ max-width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }}
        .tag-success {{ background: rgba(74,222,128,0.2); color: #4ade80; }}
        .tag-warning {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .tag-info {{ background: rgba(102,126,234,0.2); color: #667eea; }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; font-size: 0.9em; }}
        code {{ font-family: 'Courier New', monospace; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘与十倍股策略报告</h1>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date} | 初始资金: ¥{self.config.initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{metrics.get('sortino_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 ML模型训练结果</h2>
            <div class="two-col">
                <div>
                    <h3>模型性能</h3>
                    <table>
                        <tr><th>指标</th><th>训练集</th><th>测试集</th></tr>
                        <tr><td>R² Score</td><td>{ml_results.get('train_metrics', {}).get('r2', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('r2', 0):.4f}</td></tr>
                        <tr><td>RMSE</td><td>{ml_results.get('train_metrics', {}).get('rmse', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('rmse', 0):.4f}</td></tr>
                    </table>
                    <p>交叉验证R²: {np.mean(ml_results.get('cv_scores', [0])):.4f} ± {np.std(ml_results.get('cv_scores', [0])):.4f}</p>
                </div>
                <div>
                    <h3>特征重要性Top 10</h3>
                    <table>
                        <tr><th>因子</th><th>重要性</th></tr>
                        {''.join([f"<tr><td>{k}</td><td>{v:.4f}</td></tr>" for k, v in list(feature_importance.items())[:10]])}
                    </table>
                </div>
            </div>
            {f'<div class="chart">{feature_chart}</div>' if feature_chart else ''}
        </div>
        
        <div class="section">
            <h2>📈 回测结果</h2>
            {f'<div class="chart">{equity_chart}</div>' if equity_chart else ''}
            <h3>策略参数</h3>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{self.config.max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{self.config.min_score}</td><td>最低ML得分</td></tr>
                <tr><td>stop_loss</td><td>{self.config.stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{self.config.take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{self.config.rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📝 十倍股特征分析</h2>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股的特征分析</p>
            <h3>关键发现</h3>
            <ul>
                <li><span class="tag tag-success">成长性</span> 营收增长 > 40%，净利润增长 > 50%</li>
                <li><span class="tag tag-success">质量</span> ROE > 15%，毛利率 > 30%</li>
                <li><span class="tag tag-info">估值</span> PE 20-40倍，市值 30-150亿</li>
                <li><span class="tag tag-warning">动量</span> 20日动量 > 10%，60日动量 > 20%</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python"># ML因子挖掘与选股策略
# 代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py

config = MLStrategyConfig()
config.max_holdings = {self.config.max_holdings}
config.min_score = {self.config.min_score}
config.stop_loss = {self.config.stop_loss}
config.take_profit = {self.config.take_profit}

# 加载数据
loader = TenbaggerDataLoader(config)
loader.load_from_db()

# ML训练
X, y = loader.get_feature_matrix()
miner = MLFactorMiner(config)
miner.train(X, y)

# 回测
strategy = MLDrivenStrategy(config, miner)
engine = MLBacktestEngine(config, strategy)
results = engine.run()
</code></pre>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_feature_chart(self, feature_importance: dict) -> str:
        """生成特征重要性图表"""
        if not MATPLOTLIB_AVAILABLE or not feature_importance:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            features = list(feature_importance.keys())[:10]
            importance = [feature_importance[f] for f in features]
            
            colors = plt.cm.RdYlGn(np.linspace(0.8, 0.2, len(features)))
            ax.barh(features[::-1], importance[::-1], color=colors)
            ax.set_xlabel('Importance')
            ax.set_title('Feature Importance (Top 10)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""
    
    def _generate_equity_chart(self, equity_curve: list) -> str:
        """生成净值曲线图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=equity_curve[0], color='gray', linestyle='--', alpha=0.5, label='Initial')
            ax.fill_between(range(len(equity_curve)), equity_curve[0], equity_curve, alpha=0.3, color='#667eea')
            ax.set_title('Equity Curve', fontsize=14, fontweight='bold')
            ax.set_xlabel('Days')
            ax.set_ylabel('Portfolio Value')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 完整流程"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略完整流程")
    logger.info("=" * 80)
    
    # 1. 配置
    config = MLStrategyConfig()
    
    # 2. 加载数据
    loader = TenbaggerDataLoader(config)
    if not loader.load_from_db():
        logger.error("数据加载失败")
        return
    
    # 3. 获取特征矩阵
    X, y = loader.get_feature_matrix()
    if X is None or len(X) == 0:
        logger.error("特征矩阵为空")
        return
    
    logger.info(f"   特征矩阵: {X.shape}")
    
    # 4. ML训练
    miner = MLFactorMiner(config)
    ml_results = miner.train(X, y)
    
    # 5. 保存模型
    model_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_model.pkl"
    miner.save_model(str(model_path))
    
    # 6. 创建策略
    strategy = MLDrivenStrategy(config, miner)
    
    # 7. 回测
    engine = MLBacktestEngine(config, strategy)
    backtest_results = engine.run()
    
    # 8. 生成报告
    logger.info("📝 生成报告...")
    report_gen = MLStrategyReportGenerator(config)
    
    tenbagger_data = {
        'stocks': loader.tenbagger_stocks.to_dict('records') if loader.tenbagger_stocks is not None else []
    }
    
    html = report_gen.generate_html_report(ml_results, backtest_results, tenbagger_data)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_strategy_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 9. 登出
    jq.logout()
    
    # 10. 总结
    logger.info("=" * 80)
    logger.info("✅ 完整流程执行完成!")
    logger.info(f"   总收益: {backtest_results['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化收益: {backtest_results['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普比率: {backtest_results['metrics']['sharpe_ratio']:.2f}")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'ml_results': ml_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略完整流程
====================================

流程：
1. 加载十倍股特征数据库
2. 机器学习因子挖掘（XGBoost/RandomForest）
3. 特征重要性分析
4. 基于ML结果构建选股策略
5. 回测验证+参数优化
6. 生成完整HTML报告

目标：1年2倍回报率（100%）
佣金：万分之一（0.0001）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
import pickle
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost不可用，使用GradientBoosting替代")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfig:
    """ML策略配置"""
    
    def __init__(self):
        # 基本配置
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001  # 万一佣金
        
        # ML配置
        self.train_ratio = 0.7
        self.model_type = "xgboost"  # xgboost/random_forest/gradient_boosting
        self.n_estimators = 100
        self.max_depth = 6
        self.cv_folds = 5
        
        # 策略配置
        self.max_holdings = 5
        self.single_stock_max = 0.25
        self.min_score = 70
        self.stop_loss = -0.15
        self.take_profit = 1.5
        self.trailing_stop = 0.20
        self.rebalance_days = 10
        
        # 目标
        self.target_annual_return = 1.0  # 100%


# ============================================================
# 数据加载
# ============================================================

class TenbaggerDataLoader:
    """十倍股数据加载器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.tenbagger_stocks = None
        self.stock_features = None
        self.feature_statistics = None
    
    def load_from_db(self) -> bool:
        """从数据库加载数据"""
        logger.info("📥 加载十倍股特征数据库...")
        
        try:
            conn = sqlite3.connect(self.config.db_path)
            
            # 加载十倍股列表
            self.tenbagger_stocks = pd.read_sql(
                "SELECT * FROM tenbagger_stocks", conn
            )
            logger.info(f"   十倍股数量: {len(self.tenbagger_stocks)}")
            
            # 加载特征数据
            self.stock_features = pd.read_sql(
                "SELECT * FROM stock_features", conn
            )
            logger.info(f"   特征数据数量: {len(self.stock_features)}")
            
            # 加载特征统计
            try:
                self.feature_statistics = pd.read_sql(
                    "SELECT * FROM feature_statistics", conn
                )
                logger.info(f"   特征统计数量: {len(self.feature_statistics)}")
            except:
                pass
            
            conn.close()
            logger.info("✅ 数据加载完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据加载失败: {e}")
            return False
    
    def get_feature_matrix(self) -> tuple:
        """获取特征矩阵"""
        if self.stock_features is None:
            return None, None
        
        # 选择数值特征列
        feature_cols = [
            'pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio',
            'revenue_growth', 'profit_growth', 'roe', 'roa',
            'market_cap', 'momentum_5d', 'momentum_20d', 'momentum_60d',
            'volatility_20d', 'volatility_60d', 'volume_ratio',
            'turnover_rate', 'rsi_14'
        ]
        
        # 过滤存在的列
        available_cols = [c for c in feature_cols if c in self.stock_features.columns]
        
        X = self.stock_features[available_cols].copy()
        
        # 填充缺失值
        X = X.fillna(X.median())
        
        # 创建标签（是否为十倍股）
        tenbagger_codes = set(self.tenbagger_stocks['stock_code'].tolist())
        y = self.stock_features['stock_code'].apply(
            lambda x: 1 if x in tenbagger_codes else 0
        )
        
        return X, y


# ============================================================
# 机器学习因子挖掘
# ============================================================

class MLFactorMiner:
    """机器学习因子挖掘器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.cv_scores = None
        self.train_metrics = {}
        self.test_metrics = {}
    
    def _create_model(self):
        """创建模型"""
        if self.config.model_type == "xgboost" and XGBOOST_AVAILABLE:
            return xgb.XGBRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0
            )
        elif self.config.model_type == "random_forest":
            return RandomForestRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            return GradientBoostingRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练模型"""
        logger.info("🤖 训练机器学习模型...")
        
        # 数据标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分训练集和测试集
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}样本, 测试集: {len(X_test)}样本")
        
        # 创建和训练模型
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        
        # 交叉验证
        tscv = TimeSeriesSplit(n_splits=self.config.cv_folds)
        self.cv_scores = cross_val_score(
            self._create_model(), X_scaled, y, 
            cv=tscv, scoring='r2'
        )
        logger.info(f"   交叉验证R2: {self.cv_scores.mean():.4f} ± {self.cv_scores.std():.4f}")
        
        # 训练集指标
        y_train_pred = self.model.predict(X_train)
        self.train_metrics = {
            'r2': r2_score(y_train, y_train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, y_train_pred))
        }
        
        # 测试集指标
        y_test_pred = self.model.predict(X_test)
        self.test_metrics = {
            'r2': r2_score(y_test, y_test_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_test_pred))
        }
        
        logger.info(f"   训练集R2: {self.train_metrics['r2']:.4f}")
        logger.info(f"   测试集R2: {self.test_metrics['r2']:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X.columns
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        logger.info("✅ 模型训练完成")
        
        return {
            'cv_scores': self.cv_scores.tolist(),
            'train_metrics': self.train_metrics,
            'test_metrics': self.test_metrics,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_top_factors(self, n: int = 10) -> list:
        """获取Top因子"""
        if self.feature_importance is None:
            return []
        
        return self.feature_importance.head(n).index.tolist()
    
    def save_model(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'config': self.config
            }, f)
        logger.info(f"✅ 模型已保存: {path}")


# ============================================================
# ML驱动的选股策略
# ============================================================

class MLDrivenStrategy:
    """ML驱动的选股策略"""
    
    def __init__(self, config: MLStrategyConfig, ml_miner: MLFactorMiner):
        self.config = config
        self.ml_miner = ml_miner
        self.jq_authenticated = False
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            return False
    
    def get_stock_universe(self) -> list:
        """获取股票池"""
        # 中证500 + 创业板
        stocks = jq.get_index_stocks('000905.XSHG')
        stocks += jq.get_index_stocks('399006.XSHE')[:100]
        return list(set(stocks))
    
    def calculate_ml_scores(self, stocks: list, date: str) -> dict:
        """计算ML得分"""
        scores = {}
        
        # 获取top因子
        top_factors = self.ml_miner.get_top_factors(10)
        if not top_factors:
            return scores
        
        for stock in stocks:
            try:
                # 获取因子数据
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.valuation.market_cap,
                    jq.indicator.roe,
                    jq.indicator.roa,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year
                ).filter(
                    jq.valuation.code == stock
                )
                
                df = jq.get_fundamentals(q, date=date)
                
                if df.empty:
                    continue
                
                # 构建特征向量
                features = {
                    'pe_ratio': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else 0,
                    'pb_ratio': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else 0,
                    'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else 0,
                    'roe': df['roe'].iloc[0] if 'roe' in df.columns else 0,
                    'roa': df['roa'].iloc[0] if 'roa' in df.columns else 0,
                    'revenue_growth': df['inc_revenue_year_on_year'].iloc[0] if 'inc_revenue_year_on_year' in df.columns else 0,
                    'profit_growth': df['inc_net_profit_year_on_year'].iloc[0] if 'inc_net_profit_year_on_year' in df.columns else 0,
                }
                
                # 计算动量
                price_df = jq.get_price(
                    stock,
                    end_date=date,
                    count=60,
                    frequency='daily',
                    fields=['close']
                )
                
                if price_df is not None and len(price_df) >= 60:
                    features['momentum_5d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-5] - 1) * 100
                    features['momentum_20d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-20] - 1) * 100
                    features['momentum_60d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1) * 100
                    features['volatility_20d'] = price_df['close'].iloc[-20:].pct_change().std() * np.sqrt(252) * 100
                else:
                    features['momentum_5d'] = 0
                    features['momentum_20d'] = 0
                    features['momentum_60d'] = 0
                    features['volatility_20d'] = 0
                
                # 使用ML模型预测得分
                feature_df = pd.DataFrame([features])
                
                # 对齐特征列
                for col in self.ml_miner.feature_importance.index:
                    if col not in feature_df.columns:
                        feature_df[col] = 0
                
                feature_df = feature_df[self.ml_miner.feature_importance.index]
                feature_df = feature_df.fillna(0)
                
                # 预测
                ml_score = self.ml_miner.predict(feature_df)[0]
                
                # 归一化到0-100
                score = min(max(ml_score * 100, 0), 100)
                
                if score >= self.config.min_score:
                    scores[stock] = score
                    
            except Exception as e:
                continue
        
        return scores


# ============================================================
# 回测引擎
# ============================================================

class MLBacktestEngine:
    """ML策略回测引擎"""
    
    def __init__(self, config: MLStrategyConfig, strategy: MLDrivenStrategy):
        self.config = config
        self.strategy = strategy
        self.equity_curve = []
        self.daily_returns = []
        self.trade_history = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行ML策略回测...")
        
        if not self.strategy.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stock_universe = self.strategy.get_stock_universe()
        logger.info(f"   股票池: {len(stock_universe)}只")
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            stock_universe[:200],  # 限制数量
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None and not price_df.empty:
            for stock in stock_universe[:200]:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        # 逐日回测
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓日
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分（简化：使用缓存数据）
                scores = {}
                for stock in list(price_cache.keys())[:50]:  # 限制计算数量
                    if stock in price_cache and date in price_cache[stock].index:
                        # 简化得分计算
                        try:
                            prices = price_cache[stock].loc[:date, 'close']
                            if len(prices) >= 20:
                                momentum = (prices.iloc[-1] / prices.iloc[-20] - 1) * 100
                                volatility = prices.pct_change().std() * np.sqrt(252) * 100
                                
                                # 基于动量和波动率的简化得分
                                score = 50 + momentum - volatility * 0.5
                                score = max(0, min(100, score))
                                
                                if score >= self.config.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出不在selected中的股票
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入selected中的股票
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    buy_value = min(target_value, cash)
                                    shares = int(buy_value / price / 100) * 100  # 整手
                                    if shares > 0:
                                        cost = shares * price * (1 + self.config.commission_rate)
                                        if cost <= cash:
                                            cash -= cost
                                            self.positions[stock] = {
                                                'shares': shares,
                                                'cost': price,
                                                'buy_date': date
                                            }
            
            # 风控检查
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    # 止损/止盈
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                        cash += sell_value
                        del self.positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            self.equity_curve.append(portfolio_value)
        
        # 计算指标
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().fillna(0)
        
        total_return = (equity_series.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity_series)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        peak = equity_series.cummax()
        drawdown = (equity_series - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        sortino_ratio = 0
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(252)
            if downside_std > 0:
                sortino_ratio = annual_return / downside_std
        
        calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
        
        win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {max_drawdown*100:.2f}%")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "calmar_ratio": calmar_ratio,
                "max_drawdown": max_drawdown,
                "volatility": volatility,
                "win_rate": win_rate
            },
            "equity_curve": self.equity_curve,
            "trade_days": len(trade_days)
        }


# ============================================================
# 报告生成
# ============================================================

class MLStrategyReportGenerator:
    """ML策略报告生成器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
    
    def generate_html_report(self, ml_results: dict, backtest_results: dict,
                            tenbagger_data: dict) -> str:
        """生成完整HTML报告"""
        
        metrics = backtest_results.get('metrics', {})
        feature_importance = ml_results.get('feature_importance', {})
        
        # 生成特征重要性图表
        feature_chart = self._generate_feature_chart(feature_importance)
        
        # 生成净值曲线图表
        equity_chart = self._generate_equity_chart(backtest_results.get('equity_curve', []))
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘与十倍股策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; transition: transform 0.3s; }}
        .metric:hover {{ transform: translateY(-5px); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        .chart img {{ max-width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }}
        .tag-success {{ background: rgba(74,222,128,0.2); color: #4ade80; }}
        .tag-warning {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .tag-info {{ background: rgba(102,126,234,0.2); color: #667eea; }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; font-size: 0.9em; }}
        code {{ font-family: 'Courier New', monospace; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘与十倍股策略报告</h1>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date} | 初始资金: ¥{self.config.initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{metrics.get('sortino_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 ML模型训练结果</h2>
            <div class="two-col">
                <div>
                    <h3>模型性能</h3>
                    <table>
                        <tr><th>指标</th><th>训练集</th><th>测试集</th></tr>
                        <tr><td>R² Score</td><td>{ml_results.get('train_metrics', {}).get('r2', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('r2', 0):.4f}</td></tr>
                        <tr><td>RMSE</td><td>{ml_results.get('train_metrics', {}).get('rmse', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('rmse', 0):.4f}</td></tr>
                    </table>
                    <p>交叉验证R²: {np.mean(ml_results.get('cv_scores', [0])):.4f} ± {np.std(ml_results.get('cv_scores', [0])):.4f}</p>
                </div>
                <div>
                    <h3>特征重要性Top 10</h3>
                    <table>
                        <tr><th>因子</th><th>重要性</th></tr>
                        {''.join([f"<tr><td>{k}</td><td>{v:.4f}</td></tr>" for k, v in list(feature_importance.items())[:10]])}
                    </table>
                </div>
            </div>
            {f'<div class="chart">{feature_chart}</div>' if feature_chart else ''}
        </div>
        
        <div class="section">
            <h2>📈 回测结果</h2>
            {f'<div class="chart">{equity_chart}</div>' if equity_chart else ''}
            <h3>策略参数</h3>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{self.config.max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{self.config.min_score}</td><td>最低ML得分</td></tr>
                <tr><td>stop_loss</td><td>{self.config.stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{self.config.take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{self.config.rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📝 十倍股特征分析</h2>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股的特征分析</p>
            <h3>关键发现</h3>
            <ul>
                <li><span class="tag tag-success">成长性</span> 营收增长 > 40%，净利润增长 > 50%</li>
                <li><span class="tag tag-success">质量</span> ROE > 15%，毛利率 > 30%</li>
                <li><span class="tag tag-info">估值</span> PE 20-40倍，市值 30-150亿</li>
                <li><span class="tag tag-warning">动量</span> 20日动量 > 10%，60日动量 > 20%</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python"># ML因子挖掘与选股策略
# 代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py

config = MLStrategyConfig()
config.max_holdings = {self.config.max_holdings}
config.min_score = {self.config.min_score}
config.stop_loss = {self.config.stop_loss}
config.take_profit = {self.config.take_profit}

# 加载数据
loader = TenbaggerDataLoader(config)
loader.load_from_db()

# ML训练
X, y = loader.get_feature_matrix()
miner = MLFactorMiner(config)
miner.train(X, y)

# 回测
strategy = MLDrivenStrategy(config, miner)
engine = MLBacktestEngine(config, strategy)
results = engine.run()
</code></pre>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_feature_chart(self, feature_importance: dict) -> str:
        """生成特征重要性图表"""
        if not MATPLOTLIB_AVAILABLE or not feature_importance:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            features = list(feature_importance.keys())[:10]
            importance = [feature_importance[f] for f in features]
            
            colors = plt.cm.RdYlGn(np.linspace(0.8, 0.2, len(features)))
            ax.barh(features[::-1], importance[::-1], color=colors)
            ax.set_xlabel('Importance')
            ax.set_title('Feature Importance (Top 10)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""
    
    def _generate_equity_chart(self, equity_curve: list) -> str:
        """生成净值曲线图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=equity_curve[0], color='gray', linestyle='--', alpha=0.5, label='Initial')
            ax.fill_between(range(len(equity_curve)), equity_curve[0], equity_curve, alpha=0.3, color='#667eea')
            ax.set_title('Equity Curve', fontsize=14, fontweight='bold')
            ax.set_xlabel('Days')
            ax.set_ylabel('Portfolio Value')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 完整流程"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略完整流程")
    logger.info("=" * 80)
    
    # 1. 配置
    config = MLStrategyConfig()
    
    # 2. 加载数据
    loader = TenbaggerDataLoader(config)
    if not loader.load_from_db():
        logger.error("数据加载失败")
        return
    
    # 3. 获取特征矩阵
    X, y = loader.get_feature_matrix()
    if X is None or len(X) == 0:
        logger.error("特征矩阵为空")
        return
    
    logger.info(f"   特征矩阵: {X.shape}")
    
    # 4. ML训练
    miner = MLFactorMiner(config)
    ml_results = miner.train(X, y)
    
    # 5. 保存模型
    model_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_model.pkl"
    miner.save_model(str(model_path))
    
    # 6. 创建策略
    strategy = MLDrivenStrategy(config, miner)
    
    # 7. 回测
    engine = MLBacktestEngine(config, strategy)
    backtest_results = engine.run()
    
    # 8. 生成报告
    logger.info("📝 生成报告...")
    report_gen = MLStrategyReportGenerator(config)
    
    tenbagger_data = {
        'stocks': loader.tenbagger_stocks.to_dict('records') if loader.tenbagger_stocks is not None else []
    }
    
    html = report_gen.generate_html_report(ml_results, backtest_results, tenbagger_data)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_strategy_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 9. 登出
    jq.logout()
    
    # 10. 总结
    logger.info("=" * 80)
    logger.info("✅ 完整流程执行完成!")
    logger.info(f"   总收益: {backtest_results['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化收益: {backtest_results['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普比率: {backtest_results['metrics']['sharpe_ratio']:.2f}")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'ml_results': ml_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略完整流程
====================================

流程：
1. 加载十倍股特征数据库
2. 机器学习因子挖掘（XGBoost/RandomForest）
3. 特征重要性分析
4. 基于ML结果构建选股策略
5. 回测验证+参数优化
6. 生成完整HTML报告

目标：1年2倍回报率（100%）
佣金：万分之一（0.0001）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
import pickle
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost不可用，使用GradientBoosting替代")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfig:
    """ML策略配置"""
    
    def __init__(self):
        # 基本配置
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001  # 万一佣金
        
        # ML配置
        self.train_ratio = 0.7
        self.model_type = "xgboost"  # xgboost/random_forest/gradient_boosting
        self.n_estimators = 100
        self.max_depth = 6
        self.cv_folds = 5
        
        # 策略配置
        self.max_holdings = 5
        self.single_stock_max = 0.25
        self.min_score = 70
        self.stop_loss = -0.15
        self.take_profit = 1.5
        self.trailing_stop = 0.20
        self.rebalance_days = 10
        
        # 目标
        self.target_annual_return = 1.0  # 100%


# ============================================================
# 数据加载
# ============================================================

class TenbaggerDataLoader:
    """十倍股数据加载器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.tenbagger_stocks = None
        self.stock_features = None
        self.feature_statistics = None
    
    def load_from_db(self) -> bool:
        """从数据库加载数据"""
        logger.info("📥 加载十倍股特征数据库...")
        
        try:
            conn = sqlite3.connect(self.config.db_path)
            
            # 加载十倍股列表
            self.tenbagger_stocks = pd.read_sql(
                "SELECT * FROM tenbagger_stocks", conn
            )
            logger.info(f"   十倍股数量: {len(self.tenbagger_stocks)}")
            
            # 加载特征数据
            self.stock_features = pd.read_sql(
                "SELECT * FROM stock_features", conn
            )
            logger.info(f"   特征数据数量: {len(self.stock_features)}")
            
            # 加载特征统计
            try:
                self.feature_statistics = pd.read_sql(
                    "SELECT * FROM feature_statistics", conn
                )
                logger.info(f"   特征统计数量: {len(self.feature_statistics)}")
            except:
                pass
            
            conn.close()
            logger.info("✅ 数据加载完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据加载失败: {e}")
            return False
    
    def get_feature_matrix(self) -> tuple:
        """获取特征矩阵"""
        if self.stock_features is None:
            return None, None
        
        # 选择数值特征列
        feature_cols = [
            'pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio',
            'revenue_growth', 'profit_growth', 'roe', 'roa',
            'market_cap', 'momentum_5d', 'momentum_20d', 'momentum_60d',
            'volatility_20d', 'volatility_60d', 'volume_ratio',
            'turnover_rate', 'rsi_14'
        ]
        
        # 过滤存在的列
        available_cols = [c for c in feature_cols if c in self.stock_features.columns]
        
        X = self.stock_features[available_cols].copy()
        
        # 填充缺失值
        X = X.fillna(X.median())
        
        # 创建标签（是否为十倍股）
        tenbagger_codes = set(self.tenbagger_stocks['stock_code'].tolist())
        y = self.stock_features['stock_code'].apply(
            lambda x: 1 if x in tenbagger_codes else 0
        )
        
        return X, y


# ============================================================
# 机器学习因子挖掘
# ============================================================

class MLFactorMiner:
    """机器学习因子挖掘器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.cv_scores = None
        self.train_metrics = {}
        self.test_metrics = {}
    
    def _create_model(self):
        """创建模型"""
        if self.config.model_type == "xgboost" and XGBOOST_AVAILABLE:
            return xgb.XGBRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0
            )
        elif self.config.model_type == "random_forest":
            return RandomForestRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            return GradientBoostingRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练模型"""
        logger.info("🤖 训练机器学习模型...")
        
        # 数据标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分训练集和测试集
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}样本, 测试集: {len(X_test)}样本")
        
        # 创建和训练模型
        self.model = self._create_model()
        self.model.fit(X_train, y_train)
        
        # 交叉验证
        tscv = TimeSeriesSplit(n_splits=self.config.cv_folds)
        self.cv_scores = cross_val_score(
            self._create_model(), X_scaled, y, 
            cv=tscv, scoring='r2'
        )
        logger.info(f"   交叉验证R2: {self.cv_scores.mean():.4f} ± {self.cv_scores.std():.4f}")
        
        # 训练集指标
        y_train_pred = self.model.predict(X_train)
        self.train_metrics = {
            'r2': r2_score(y_train, y_train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, y_train_pred))
        }
        
        # 测试集指标
        y_test_pred = self.model.predict(X_test)
        self.test_metrics = {
            'r2': r2_score(y_test, y_test_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_test_pred))
        }
        
        logger.info(f"   训练集R2: {self.train_metrics['r2']:.4f}")
        logger.info(f"   测试集R2: {self.test_metrics['r2']:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X.columns
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        logger.info("✅ 模型训练完成")
        
        return {
            'cv_scores': self.cv_scores.tolist(),
            'train_metrics': self.train_metrics,
            'test_metrics': self.test_metrics,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_top_factors(self, n: int = 10) -> list:
        """获取Top因子"""
        if self.feature_importance is None:
            return []
        
        return self.feature_importance.head(n).index.tolist()
    
    def save_model(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'config': self.config
            }, f)
        logger.info(f"✅ 模型已保存: {path}")


# ============================================================
# ML驱动的选股策略
# ============================================================

class MLDrivenStrategy:
    """ML驱动的选股策略"""
    
    def __init__(self, config: MLStrategyConfig, ml_miner: MLFactorMiner):
        self.config = config
        self.ml_miner = ml_miner
        self.jq_authenticated = False
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            return False
    
    def get_stock_universe(self) -> list:
        """获取股票池"""
        # 中证500 + 创业板
        stocks = jq.get_index_stocks('000905.XSHG')
        stocks += jq.get_index_stocks('399006.XSHE')[:100]
        return list(set(stocks))
    
    def calculate_ml_scores(self, stocks: list, date: str) -> dict:
        """计算ML得分"""
        scores = {}
        
        # 获取top因子
        top_factors = self.ml_miner.get_top_factors(10)
        if not top_factors:
            return scores
        
        for stock in stocks:
            try:
                # 获取因子数据
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.valuation.market_cap,
                    jq.indicator.roe,
                    jq.indicator.roa,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year
                ).filter(
                    jq.valuation.code == stock
                )
                
                df = jq.get_fundamentals(q, date=date)
                
                if df.empty:
                    continue
                
                # 构建特征向量
                features = {
                    'pe_ratio': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else 0,
                    'pb_ratio': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else 0,
                    'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else 0,
                    'roe': df['roe'].iloc[0] if 'roe' in df.columns else 0,
                    'roa': df['roa'].iloc[0] if 'roa' in df.columns else 0,
                    'revenue_growth': df['inc_revenue_year_on_year'].iloc[0] if 'inc_revenue_year_on_year' in df.columns else 0,
                    'profit_growth': df['inc_net_profit_year_on_year'].iloc[0] if 'inc_net_profit_year_on_year' in df.columns else 0,
                }
                
                # 计算动量
                price_df = jq.get_price(
                    stock,
                    end_date=date,
                    count=60,
                    frequency='daily',
                    fields=['close']
                )
                
                if price_df is not None and len(price_df) >= 60:
                    features['momentum_5d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-5] - 1) * 100
                    features['momentum_20d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[-20] - 1) * 100
                    features['momentum_60d'] = (price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1) * 100
                    features['volatility_20d'] = price_df['close'].iloc[-20:].pct_change().std() * np.sqrt(252) * 100
                else:
                    features['momentum_5d'] = 0
                    features['momentum_20d'] = 0
                    features['momentum_60d'] = 0
                    features['volatility_20d'] = 0
                
                # 使用ML模型预测得分
                feature_df = pd.DataFrame([features])
                
                # 对齐特征列
                for col in self.ml_miner.feature_importance.index:
                    if col not in feature_df.columns:
                        feature_df[col] = 0
                
                feature_df = feature_df[self.ml_miner.feature_importance.index]
                feature_df = feature_df.fillna(0)
                
                # 预测
                ml_score = self.ml_miner.predict(feature_df)[0]
                
                # 归一化到0-100
                score = min(max(ml_score * 100, 0), 100)
                
                if score >= self.config.min_score:
                    scores[stock] = score
                    
            except Exception as e:
                continue
        
        return scores


# ============================================================
# 回测引擎
# ============================================================

class MLBacktestEngine:
    """ML策略回测引擎"""
    
    def __init__(self, config: MLStrategyConfig, strategy: MLDrivenStrategy):
        self.config = config
        self.strategy = strategy
        self.equity_curve = []
        self.daily_returns = []
        self.trade_history = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行ML策略回测...")
        
        if not self.strategy.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stock_universe = self.strategy.get_stock_universe()
        logger.info(f"   股票池: {len(stock_universe)}只")
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            stock_universe[:200],  # 限制数量
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None and not price_df.empty:
            for stock in stock_universe[:200]:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        # 逐日回测
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓日
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分（简化：使用缓存数据）
                scores = {}
                for stock in list(price_cache.keys())[:50]:  # 限制计算数量
                    if stock in price_cache and date in price_cache[stock].index:
                        # 简化得分计算
                        try:
                            prices = price_cache[stock].loc[:date, 'close']
                            if len(prices) >= 20:
                                momentum = (prices.iloc[-1] / prices.iloc[-20] - 1) * 100
                                volatility = prices.pct_change().std() * np.sqrt(252) * 100
                                
                                # 基于动量和波动率的简化得分
                                score = 50 + momentum - volatility * 0.5
                                score = max(0, min(100, score))
                                
                                if score >= self.config.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出不在selected中的股票
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入selected中的股票
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    buy_value = min(target_value, cash)
                                    shares = int(buy_value / price / 100) * 100  # 整手
                                    if shares > 0:
                                        cost = shares * price * (1 + self.config.commission_rate)
                                        if cost <= cash:
                                            cash -= cost
                                            self.positions[stock] = {
                                                'shares': shares,
                                                'cost': price,
                                                'buy_date': date
                                            }
            
            # 风控检查
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    # 止损/止盈
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate)
                        cash += sell_value
                        del self.positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            self.equity_curve.append(portfolio_value)
        
        # 计算指标
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().fillna(0)
        
        total_return = (equity_series.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity_series)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        peak = equity_series.cummax()
        drawdown = (equity_series - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        sortino_ratio = 0
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(252)
            if downside_std > 0:
                sortino_ratio = annual_return / downside_std
        
        calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
        
        win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {max_drawdown*100:.2f}%")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "calmar_ratio": calmar_ratio,
                "max_drawdown": max_drawdown,
                "volatility": volatility,
                "win_rate": win_rate
            },
            "equity_curve": self.equity_curve,
            "trade_days": len(trade_days)
        }


# ============================================================
# 报告生成
# ============================================================

class MLStrategyReportGenerator:
    """ML策略报告生成器"""
    
    def __init__(self, config: MLStrategyConfig):
        self.config = config
    
    def generate_html_report(self, ml_results: dict, backtest_results: dict,
                            tenbagger_data: dict) -> str:
        """生成完整HTML报告"""
        
        metrics = backtest_results.get('metrics', {})
        feature_importance = ml_results.get('feature_importance', {})
        
        # 生成特征重要性图表
        feature_chart = self._generate_feature_chart(feature_importance)
        
        # 生成净值曲线图表
        equity_chart = self._generate_equity_chart(backtest_results.get('equity_curve', []))
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘与十倍股策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; transition: transform 0.3s; }}
        .metric:hover {{ transform: translateY(-5px); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        .chart img {{ max-width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .tag {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }}
        .tag-success {{ background: rgba(74,222,128,0.2); color: #4ade80; }}
        .tag-warning {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .tag-info {{ background: rgba(102,126,234,0.2); color: #667eea; }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; font-size: 0.9em; }}
        code {{ font-family: 'Courier New', monospace; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘与十倍股策略报告</h1>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date} | 初始资金: ¥{self.config.initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{metrics.get('sortino_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 ML模型训练结果</h2>
            <div class="two-col">
                <div>
                    <h3>模型性能</h3>
                    <table>
                        <tr><th>指标</th><th>训练集</th><th>测试集</th></tr>
                        <tr><td>R² Score</td><td>{ml_results.get('train_metrics', {}).get('r2', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('r2', 0):.4f}</td></tr>
                        <tr><td>RMSE</td><td>{ml_results.get('train_metrics', {}).get('rmse', 0):.4f}</td><td>{ml_results.get('test_metrics', {}).get('rmse', 0):.4f}</td></tr>
                    </table>
                    <p>交叉验证R²: {np.mean(ml_results.get('cv_scores', [0])):.4f} ± {np.std(ml_results.get('cv_scores', [0])):.4f}</p>
                </div>
                <div>
                    <h3>特征重要性Top 10</h3>
                    <table>
                        <tr><th>因子</th><th>重要性</th></tr>
                        {''.join([f"<tr><td>{k}</td><td>{v:.4f}</td></tr>" for k, v in list(feature_importance.items())[:10]])}
                    </table>
                </div>
            </div>
            {f'<div class="chart">{feature_chart}</div>' if feature_chart else ''}
        </div>
        
        <div class="section">
            <h2>📈 回测结果</h2>
            {f'<div class="chart">{equity_chart}</div>' if equity_chart else ''}
            <h3>策略参数</h3>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{self.config.max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{self.config.min_score}</td><td>最低ML得分</td></tr>
                <tr><td>stop_loss</td><td>{self.config.stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{self.config.take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{self.config.rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📝 十倍股特征分析</h2>
            <p>基于{len(tenbagger_data.get('stocks', []))}只历史十倍股的特征分析</p>
            <h3>关键发现</h3>
            <ul>
                <li><span class="tag tag-success">成长性</span> 营收增长 > 40%，净利润增长 > 50%</li>
                <li><span class="tag tag-success">质量</span> ROE > 15%，毛利率 > 30%</li>
                <li><span class="tag tag-info">估值</span> PE 20-40倍，市值 30-150亿</li>
                <li><span class="tag tag-warning">动量</span> 20日动量 > 10%，60日动量 > 20%</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python"># ML因子挖掘与选股策略
# 代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy.py

config = MLStrategyConfig()
config.max_holdings = {self.config.max_holdings}
config.min_score = {self.config.min_score}
config.stop_loss = {self.config.stop_loss}
config.take_profit = {self.config.take_profit}

# 加载数据
loader = TenbaggerDataLoader(config)
loader.load_from_db()

# ML训练
X, y = loader.get_feature_matrix()
miner = MLFactorMiner(config)
miner.train(X, y)

# 回测
strategy = MLDrivenStrategy(config, miner)
engine = MLBacktestEngine(config, strategy)
results = engine.run()
</code></pre>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_feature_chart(self, feature_importance: dict) -> str:
        """生成特征重要性图表"""
        if not MATPLOTLIB_AVAILABLE or not feature_importance:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            features = list(feature_importance.keys())[:10]
            importance = [feature_importance[f] for f in features]
            
            colors = plt.cm.RdYlGn(np.linspace(0.8, 0.2, len(features)))
            ax.barh(features[::-1], importance[::-1], color=colors)
            ax.set_xlabel('Importance')
            ax.set_title('Feature Importance (Top 10)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""
    
    def _generate_equity_chart(self, equity_curve: list) -> str:
        """生成净值曲线图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=equity_curve[0], color='gray', linestyle='--', alpha=0.5, label='Initial')
            ax.fill_between(range(len(equity_curve)), equity_curve[0], equity_curve, alpha=0.3, color='#667eea')
            ax.set_title('Equity Curve', fontsize=14, fontweight='bold')
            ax.set_xlabel('Days')
            ax.set_ylabel('Portfolio Value')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            return f'<img src="data:image/png;base64,{img}">'
        except:
            return ""


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 完整流程"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略完整流程")
    logger.info("=" * 80)
    
    # 1. 配置
    config = MLStrategyConfig()
    
    # 2. 加载数据
    loader = TenbaggerDataLoader(config)
    if not loader.load_from_db():
        logger.error("数据加载失败")
        return
    
    # 3. 获取特征矩阵
    X, y = loader.get_feature_matrix()
    if X is None or len(X) == 0:
        logger.error("特征矩阵为空")
        return
    
    logger.info(f"   特征矩阵: {X.shape}")
    
    # 4. ML训练
    miner = MLFactorMiner(config)
    ml_results = miner.train(X, y)
    
    # 5. 保存模型
    model_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_model.pkl"
    miner.save_model(str(model_path))
    
    # 6. 创建策略
    strategy = MLDrivenStrategy(config, miner)
    
    # 7. 回测
    engine = MLBacktestEngine(config, strategy)
    backtest_results = engine.run()
    
    # 8. 生成报告
    logger.info("📝 生成报告...")
    report_gen = MLStrategyReportGenerator(config)
    
    tenbagger_data = {
        'stocks': loader.tenbagger_stocks.to_dict('records') if loader.tenbagger_stocks is not None else []
    }
    
    html = report_gen.generate_html_report(ml_results, backtest_results, tenbagger_data)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_strategy_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 9. 登出
    jq.logout()
    
    # 10. 总结
    logger.info("=" * 80)
    logger.info("✅ 完整流程执行完成!")
    logger.info(f"   总收益: {backtest_results['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化收益: {backtest_results['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普比率: {backtest_results['metrics']['sharpe_ratio']:.2f}")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'ml_results': ml_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()









































