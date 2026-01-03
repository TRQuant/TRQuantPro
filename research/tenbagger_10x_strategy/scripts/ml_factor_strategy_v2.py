#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略 V2（优化版）
==========================================

改进：
1. 添加负样本（非十倍股）平衡数据集
2. 使用完整因子库
3. 更精确的因子计算
4. 优化的策略参数
5. 循环迭代优化

目标：1年2倍回报率（100%）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_v2.py
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfigV2:
    """ML策略配置V2"""
    
    def __init__(self):
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001
        
        # ML配置
        self.train_ratio = 0.7
        self.n_estimators = 200
        self.max_depth = 8
        
        # 优化后的策略参数
        self.max_holdings = 3           # 更集中
        self.single_stock_max = 0.35    # 单票更高
        self.min_score = 0.6            # 概率阈值
        self.stop_loss = -0.12          # 更紧止损
        self.take_profit = 2.0          # 让利润奔跑
        self.trailing_stop = 0.15
        self.rebalance_days = 5         # 更频繁调仓


# ============================================================
# 增强数据加载器
# ============================================================

class EnhancedDataLoader:
    """增强数据加载器（添加负样本）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.tenbagger_codes = set()
        self.all_features = None
        self.jq_authenticated = False
    
    def authenticate(self) -> bool:
        if self.jq_authenticated:
            return True
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def load_tenbagger_codes(self):
        """加载十倍股代码"""
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
        conn.close()
        self.tenbagger_codes = set(df['stock_code'].tolist())
        logger.info(f"   十倍股数量: {len(self.tenbagger_codes)}")
    
    def build_training_data(self) -> tuple:
        """
        构建训练数据（十倍股 + 非十倍股）
        """
        logger.info("📥 构建训练数据集...")
        
        if not self.authenticate():
            return None, None
        
        self.load_tenbagger_codes()
        
        # 获取股票池
        all_stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300
        all_stocks += jq.get_index_stocks('000905.XSHG')[:100]  # 中证500部分
        all_stocks = list(set(all_stocks))
        
        logger.info(f"   股票池: {len(all_stocks)}只")
        
        # 训练日期
        train_date = "2024-06-01"
        
        features_list = []
        labels = []
        
        for i, stock in enumerate(all_stocks):
            if i % 50 == 0:
                logger.info(f"   处理: {i}/{len(all_stocks)}")
            
            try:
                # 获取因子数据
                features = self._get_stock_features(stock, train_date)
                if features is not None:
                    features_list.append(features)
                    # 标签：是否为十倍股
                    label = 1 if stock in self.tenbagger_codes else 0
                    labels.append(label)
            except:
                continue
        
        if not features_list:
            return None, None
        
        X = pd.DataFrame(features_list)
        y = pd.Series(labels)
        
        logger.info(f"   训练数据: {len(X)}样本, 正样本: {y.sum()}, 负样本: {len(y) - y.sum()}")
        
        return X, y
    
    def _get_stock_features(self, stock: str, date: str) -> dict:
        """获取单只股票的因子"""
        try:
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if fund_df.empty:
                return None
            
            # 价格数据（计算动量和波动率）
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is None or len(price_df) < 60:
                return None
            
            close = price_df['close']
            volume = price_df['volume']
            
            features = {
                # 估值因子
                'pe_ratio': fund_df['pe_ratio'].iloc[0] or 0,
                'pb_ratio': fund_df['pb_ratio'].iloc[0] or 0,
                'ps_ratio': fund_df['ps_ratio'].iloc[0] or 0,
                
                # 规模因子
                'market_cap': fund_df['market_cap'].iloc[0] or 0,
                'log_market_cap': np.log(fund_df['market_cap'].iloc[0] + 1) if fund_df['market_cap'].iloc[0] else 0,
                
                # 质量因子
                'roe': fund_df['roe'].iloc[0] or 0,
                'roa': fund_df['roa'].iloc[0] or 0,
                'gross_margin': fund_df['gross_profit_margin'].iloc[0] or 0,
                
                # 成长因子
                'revenue_growth': fund_df['inc_revenue_year_on_year'].iloc[0] or 0,
                'profit_growth': fund_df['inc_net_profit_year_on_year'].iloc[0] or 0,
                
                # 动量因子
                'momentum_5d': (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0,
                'momentum_20d': (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0,
                'momentum_60d': (close.iloc[-1] / close.iloc[0] - 1) * 100,
                
                # 波动率因子
                'volatility_20d': close.iloc[-20:].pct_change().std() * np.sqrt(252) * 100 if len(close) >= 20 else 0,
                
                # 成交量因子
                'volume_ratio': volume.iloc[-5:].mean() / volume.iloc[-20:].mean() if volume.iloc[-20:].mean() > 0 else 1,
                
                # 技术因子
                'price_to_ma20': (close.iloc[-1] / close.iloc[-20:].mean() - 1) * 100 if len(close) >= 20 else 0,
            }
            
            return features
            
        except Exception as e:
            return None


# ============================================================
# ML分类器
# ============================================================

class MLClassifier:
    """ML分类器（预测是否为潜在十倍股）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.feature_names = None
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练分类模型"""
        logger.info("🤖 训练ML分类模型...")
        
        self.feature_names = X.columns.tolist()
        
        # 处理缺失值和无穷值
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # 标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分数据
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}, 测试集: {len(X_test)}")
        
        # 创建模型（使用分类器）
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
        
        # 训练
        self.model.fit(X_train, y_train)
        
        # 评估
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        y_test_proba = self.model.predict_proba(X_test)[:, 1]
        
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_auc = roc_auc_score(y_test, y_test_proba) if len(set(y_test)) > 1 else 0
        
        logger.info(f"   训练集准确率: {train_acc:.4f}")
        logger.info(f"   测试集准确率: {test_acc:.4f}")
        logger.info(f"   测试集AUC: {test_auc:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=self.feature_names
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'test_auc': test_auc,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """预测概率"""
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        # 对齐特征
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0
        X = X[self.feature_names]
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]


# ============================================================
# 优化回测引擎
# ============================================================

class OptimizedBacktestEngine:
    """优化回测引擎"""
    
    def __init__(self, config: MLStrategyConfigV2, classifier: MLClassifier, data_loader: EnhancedDataLoader):
        self.config = config
        self.classifier = classifier
        self.data_loader = data_loader
        self.equity_curve = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行优化回测...")
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stocks = jq.get_index_stocks('000300.XSHG')[:100]
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载价格数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in stocks:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分
                scores = {}
                for stock in list(price_cache.keys())[:30]:
                    try:
                        features = self.data_loader._get_stock_features(stock, date)
                        if features:
                            features_df = pd.DataFrame([features])
                            proba = self.classifier.predict_proba(features_df)[0]
                            if proba >= self.config.min_score:
                                scores[stock] = proba
                    except:
                        continue
                
                if scores:
                    # 选股
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions and stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                buy_value = min(target_value, cash)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0:
                                    cost = shares * price * (1 + self.config.commission_rate)
                                    if cost <= cash:
                                        cash -= cost
                                        self.positions[stock] = {
                                            'shares': shares,
                                            'cost': price
                                        }
            
            # 风控
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
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
        equity = pd.Series(self.equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 回测完成: 总收益 {total_return*100:.2f}%, 年化 {annual_return*100:.2f}%, 夏普 {sharpe:.2f}")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "volatility": volatility
            },
            "equity_curve": self.equity_curve
        }


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略 V2（优化版）")
    logger.info("=" * 80)
    
    config = MLStrategyConfigV2()
    
    # 1. 数据加载
    loader = EnhancedDataLoader(config)
    X, y = loader.build_training_data()
    
    if X is None:
        logger.error("数据加载失败")
        return
    
    # 2. 训练ML模型
    classifier = MLClassifier(config)
    ml_results = classifier.train(X, y)
    
    # 3. 回测
    engine = OptimizedBacktestEngine(config, classifier, loader)
    backtest_results = engine.run()
    
    # 4. 保存结果
    results = {
        'ml_results': ml_results,
        'backtest_results': backtest_results['metrics'],
        'config': {
            'max_holdings': config.max_holdings,
            'min_score': config.min_score,
            'stop_loss': config.stop_loss,
            'take_profit': config.take_profit
        }
    }
    
    results_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_strategy_v2_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✅ 结果已保存: {results_path}")
    
    # 5. 登出
    jq.logout()
    
    return results


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略 V2（优化版）
==========================================

改进：
1. 添加负样本（非十倍股）平衡数据集
2. 使用完整因子库
3. 更精确的因子计算
4. 优化的策略参数
5. 循环迭代优化

目标：1年2倍回报率（100%）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_v2.py
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfigV2:
    """ML策略配置V2"""
    
    def __init__(self):
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001
        
        # ML配置
        self.train_ratio = 0.7
        self.n_estimators = 200
        self.max_depth = 8
        
        # 优化后的策略参数
        self.max_holdings = 3           # 更集中
        self.single_stock_max = 0.35    # 单票更高
        self.min_score = 0.6            # 概率阈值
        self.stop_loss = -0.12          # 更紧止损
        self.take_profit = 2.0          # 让利润奔跑
        self.trailing_stop = 0.15
        self.rebalance_days = 5         # 更频繁调仓


# ============================================================
# 增强数据加载器
# ============================================================

class EnhancedDataLoader:
    """增强数据加载器（添加负样本）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.tenbagger_codes = set()
        self.all_features = None
        self.jq_authenticated = False
    
    def authenticate(self) -> bool:
        if self.jq_authenticated:
            return True
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def load_tenbagger_codes(self):
        """加载十倍股代码"""
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
        conn.close()
        self.tenbagger_codes = set(df['stock_code'].tolist())
        logger.info(f"   十倍股数量: {len(self.tenbagger_codes)}")
    
    def build_training_data(self) -> tuple:
        """
        构建训练数据（十倍股 + 非十倍股）
        """
        logger.info("📥 构建训练数据集...")
        
        if not self.authenticate():
            return None, None
        
        self.load_tenbagger_codes()
        
        # 获取股票池
        all_stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300
        all_stocks += jq.get_index_stocks('000905.XSHG')[:100]  # 中证500部分
        all_stocks = list(set(all_stocks))
        
        logger.info(f"   股票池: {len(all_stocks)}只")
        
        # 训练日期
        train_date = "2024-06-01"
        
        features_list = []
        labels = []
        
        for i, stock in enumerate(all_stocks):
            if i % 50 == 0:
                logger.info(f"   处理: {i}/{len(all_stocks)}")
            
            try:
                # 获取因子数据
                features = self._get_stock_features(stock, train_date)
                if features is not None:
                    features_list.append(features)
                    # 标签：是否为十倍股
                    label = 1 if stock in self.tenbagger_codes else 0
                    labels.append(label)
            except:
                continue
        
        if not features_list:
            return None, None
        
        X = pd.DataFrame(features_list)
        y = pd.Series(labels)
        
        logger.info(f"   训练数据: {len(X)}样本, 正样本: {y.sum()}, 负样本: {len(y) - y.sum()}")
        
        return X, y
    
    def _get_stock_features(self, stock: str, date: str) -> dict:
        """获取单只股票的因子"""
        try:
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if fund_df.empty:
                return None
            
            # 价格数据（计算动量和波动率）
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is None or len(price_df) < 60:
                return None
            
            close = price_df['close']
            volume = price_df['volume']
            
            features = {
                # 估值因子
                'pe_ratio': fund_df['pe_ratio'].iloc[0] or 0,
                'pb_ratio': fund_df['pb_ratio'].iloc[0] or 0,
                'ps_ratio': fund_df['ps_ratio'].iloc[0] or 0,
                
                # 规模因子
                'market_cap': fund_df['market_cap'].iloc[0] or 0,
                'log_market_cap': np.log(fund_df['market_cap'].iloc[0] + 1) if fund_df['market_cap'].iloc[0] else 0,
                
                # 质量因子
                'roe': fund_df['roe'].iloc[0] or 0,
                'roa': fund_df['roa'].iloc[0] or 0,
                'gross_margin': fund_df['gross_profit_margin'].iloc[0] or 0,
                
                # 成长因子
                'revenue_growth': fund_df['inc_revenue_year_on_year'].iloc[0] or 0,
                'profit_growth': fund_df['inc_net_profit_year_on_year'].iloc[0] or 0,
                
                # 动量因子
                'momentum_5d': (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0,
                'momentum_20d': (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0,
                'momentum_60d': (close.iloc[-1] / close.iloc[0] - 1) * 100,
                
                # 波动率因子
                'volatility_20d': close.iloc[-20:].pct_change().std() * np.sqrt(252) * 100 if len(close) >= 20 else 0,
                
                # 成交量因子
                'volume_ratio': volume.iloc[-5:].mean() / volume.iloc[-20:].mean() if volume.iloc[-20:].mean() > 0 else 1,
                
                # 技术因子
                'price_to_ma20': (close.iloc[-1] / close.iloc[-20:].mean() - 1) * 100 if len(close) >= 20 else 0,
            }
            
            return features
            
        except Exception as e:
            return None


# ============================================================
# ML分类器
# ============================================================

class MLClassifier:
    """ML分类器（预测是否为潜在十倍股）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.feature_names = None
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练分类模型"""
        logger.info("🤖 训练ML分类模型...")
        
        self.feature_names = X.columns.tolist()
        
        # 处理缺失值和无穷值
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # 标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分数据
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}, 测试集: {len(X_test)}")
        
        # 创建模型（使用分类器）
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
        
        # 训练
        self.model.fit(X_train, y_train)
        
        # 评估
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        y_test_proba = self.model.predict_proba(X_test)[:, 1]
        
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_auc = roc_auc_score(y_test, y_test_proba) if len(set(y_test)) > 1 else 0
        
        logger.info(f"   训练集准确率: {train_acc:.4f}")
        logger.info(f"   测试集准确率: {test_acc:.4f}")
        logger.info(f"   测试集AUC: {test_auc:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=self.feature_names
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'test_auc': test_auc,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """预测概率"""
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        # 对齐特征
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0
        X = X[self.feature_names]
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]


# ============================================================
# 优化回测引擎
# ============================================================

class OptimizedBacktestEngine:
    """优化回测引擎"""
    
    def __init__(self, config: MLStrategyConfigV2, classifier: MLClassifier, data_loader: EnhancedDataLoader):
        self.config = config
        self.classifier = classifier
        self.data_loader = data_loader
        self.equity_curve = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行优化回测...")
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stocks = jq.get_index_stocks('000300.XSHG')[:100]
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载价格数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in stocks:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分
                scores = {}
                for stock in list(price_cache.keys())[:30]:
                    try:
                        features = self.data_loader._get_stock_features(stock, date)
                        if features:
                            features_df = pd.DataFrame([features])
                            proba = self.classifier.predict_proba(features_df)[0]
                            if proba >= self.config.min_score:
                                scores[stock] = proba
                    except:
                        continue
                
                if scores:
                    # 选股
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions and stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                buy_value = min(target_value, cash)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0:
                                    cost = shares * price * (1 + self.config.commission_rate)
                                    if cost <= cash:
                                        cash -= cost
                                        self.positions[stock] = {
                                            'shares': shares,
                                            'cost': price
                                        }
            
            # 风控
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
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
        equity = pd.Series(self.equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 回测完成: 总收益 {total_return*100:.2f}%, 年化 {annual_return*100:.2f}%, 夏普 {sharpe:.2f}")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "volatility": volatility
            },
            "equity_curve": self.equity_curve
        }


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略 V2（优化版）")
    logger.info("=" * 80)
    
    config = MLStrategyConfigV2()
    
    # 1. 数据加载
    loader = EnhancedDataLoader(config)
    X, y = loader.build_training_data()
    
    if X is None:
        logger.error("数据加载失败")
        return
    
    # 2. 训练ML模型
    classifier = MLClassifier(config)
    ml_results = classifier.train(X, y)
    
    # 3. 回测
    engine = OptimizedBacktestEngine(config, classifier, loader)
    backtest_results = engine.run()
    
    # 4. 保存结果
    results = {
        'ml_results': ml_results,
        'backtest_results': backtest_results['metrics'],
        'config': {
            'max_holdings': config.max_holdings,
            'min_score': config.min_score,
            'stop_loss': config.stop_loss,
            'take_profit': config.take_profit
        }
    }
    
    results_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_strategy_v2_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✅ 结果已保存: {results_path}")
    
    # 5. 登出
    jq.logout()
    
    return results


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略 V2（优化版）
==========================================

改进：
1. 添加负样本（非十倍股）平衡数据集
2. 使用完整因子库
3. 更精确的因子计算
4. 优化的策略参数
5. 循环迭代优化

目标：1年2倍回报率（100%）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_v2.py
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfigV2:
    """ML策略配置V2"""
    
    def __init__(self):
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001
        
        # ML配置
        self.train_ratio = 0.7
        self.n_estimators = 200
        self.max_depth = 8
        
        # 优化后的策略参数
        self.max_holdings = 3           # 更集中
        self.single_stock_max = 0.35    # 单票更高
        self.min_score = 0.6            # 概率阈值
        self.stop_loss = -0.12          # 更紧止损
        self.take_profit = 2.0          # 让利润奔跑
        self.trailing_stop = 0.15
        self.rebalance_days = 5         # 更频繁调仓


# ============================================================
# 增强数据加载器
# ============================================================

class EnhancedDataLoader:
    """增强数据加载器（添加负样本）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.tenbagger_codes = set()
        self.all_features = None
        self.jq_authenticated = False
    
    def authenticate(self) -> bool:
        if self.jq_authenticated:
            return True
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def load_tenbagger_codes(self):
        """加载十倍股代码"""
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
        conn.close()
        self.tenbagger_codes = set(df['stock_code'].tolist())
        logger.info(f"   十倍股数量: {len(self.tenbagger_codes)}")
    
    def build_training_data(self) -> tuple:
        """
        构建训练数据（十倍股 + 非十倍股）
        """
        logger.info("📥 构建训练数据集...")
        
        if not self.authenticate():
            return None, None
        
        self.load_tenbagger_codes()
        
        # 获取股票池
        all_stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300
        all_stocks += jq.get_index_stocks('000905.XSHG')[:100]  # 中证500部分
        all_stocks = list(set(all_stocks))
        
        logger.info(f"   股票池: {len(all_stocks)}只")
        
        # 训练日期
        train_date = "2024-06-01"
        
        features_list = []
        labels = []
        
        for i, stock in enumerate(all_stocks):
            if i % 50 == 0:
                logger.info(f"   处理: {i}/{len(all_stocks)}")
            
            try:
                # 获取因子数据
                features = self._get_stock_features(stock, train_date)
                if features is not None:
                    features_list.append(features)
                    # 标签：是否为十倍股
                    label = 1 if stock in self.tenbagger_codes else 0
                    labels.append(label)
            except:
                continue
        
        if not features_list:
            return None, None
        
        X = pd.DataFrame(features_list)
        y = pd.Series(labels)
        
        logger.info(f"   训练数据: {len(X)}样本, 正样本: {y.sum()}, 负样本: {len(y) - y.sum()}")
        
        return X, y
    
    def _get_stock_features(self, stock: str, date: str) -> dict:
        """获取单只股票的因子"""
        try:
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if fund_df.empty:
                return None
            
            # 价格数据（计算动量和波动率）
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is None or len(price_df) < 60:
                return None
            
            close = price_df['close']
            volume = price_df['volume']
            
            features = {
                # 估值因子
                'pe_ratio': fund_df['pe_ratio'].iloc[0] or 0,
                'pb_ratio': fund_df['pb_ratio'].iloc[0] or 0,
                'ps_ratio': fund_df['ps_ratio'].iloc[0] or 0,
                
                # 规模因子
                'market_cap': fund_df['market_cap'].iloc[0] or 0,
                'log_market_cap': np.log(fund_df['market_cap'].iloc[0] + 1) if fund_df['market_cap'].iloc[0] else 0,
                
                # 质量因子
                'roe': fund_df['roe'].iloc[0] or 0,
                'roa': fund_df['roa'].iloc[0] or 0,
                'gross_margin': fund_df['gross_profit_margin'].iloc[0] or 0,
                
                # 成长因子
                'revenue_growth': fund_df['inc_revenue_year_on_year'].iloc[0] or 0,
                'profit_growth': fund_df['inc_net_profit_year_on_year'].iloc[0] or 0,
                
                # 动量因子
                'momentum_5d': (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0,
                'momentum_20d': (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0,
                'momentum_60d': (close.iloc[-1] / close.iloc[0] - 1) * 100,
                
                # 波动率因子
                'volatility_20d': close.iloc[-20:].pct_change().std() * np.sqrt(252) * 100 if len(close) >= 20 else 0,
                
                # 成交量因子
                'volume_ratio': volume.iloc[-5:].mean() / volume.iloc[-20:].mean() if volume.iloc[-20:].mean() > 0 else 1,
                
                # 技术因子
                'price_to_ma20': (close.iloc[-1] / close.iloc[-20:].mean() - 1) * 100 if len(close) >= 20 else 0,
            }
            
            return features
            
        except Exception as e:
            return None


# ============================================================
# ML分类器
# ============================================================

class MLClassifier:
    """ML分类器（预测是否为潜在十倍股）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.feature_names = None
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练分类模型"""
        logger.info("🤖 训练ML分类模型...")
        
        self.feature_names = X.columns.tolist()
        
        # 处理缺失值和无穷值
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # 标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分数据
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}, 测试集: {len(X_test)}")
        
        # 创建模型（使用分类器）
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
        
        # 训练
        self.model.fit(X_train, y_train)
        
        # 评估
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        y_test_proba = self.model.predict_proba(X_test)[:, 1]
        
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_auc = roc_auc_score(y_test, y_test_proba) if len(set(y_test)) > 1 else 0
        
        logger.info(f"   训练集准确率: {train_acc:.4f}")
        logger.info(f"   测试集准确率: {test_acc:.4f}")
        logger.info(f"   测试集AUC: {test_auc:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=self.feature_names
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'test_auc': test_auc,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """预测概率"""
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        # 对齐特征
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0
        X = X[self.feature_names]
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]


# ============================================================
# 优化回测引擎
# ============================================================

class OptimizedBacktestEngine:
    """优化回测引擎"""
    
    def __init__(self, config: MLStrategyConfigV2, classifier: MLClassifier, data_loader: EnhancedDataLoader):
        self.config = config
        self.classifier = classifier
        self.data_loader = data_loader
        self.equity_curve = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行优化回测...")
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stocks = jq.get_index_stocks('000300.XSHG')[:100]
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载价格数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in stocks:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分
                scores = {}
                for stock in list(price_cache.keys())[:30]:
                    try:
                        features = self.data_loader._get_stock_features(stock, date)
                        if features:
                            features_df = pd.DataFrame([features])
                            proba = self.classifier.predict_proba(features_df)[0]
                            if proba >= self.config.min_score:
                                scores[stock] = proba
                    except:
                        continue
                
                if scores:
                    # 选股
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions and stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                buy_value = min(target_value, cash)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0:
                                    cost = shares * price * (1 + self.config.commission_rate)
                                    if cost <= cash:
                                        cash -= cost
                                        self.positions[stock] = {
                                            'shares': shares,
                                            'cost': price
                                        }
            
            # 风控
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
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
        equity = pd.Series(self.equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 回测完成: 总收益 {total_return*100:.2f}%, 年化 {annual_return*100:.2f}%, 夏普 {sharpe:.2f}")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "volatility": volatility
            },
            "equity_curve": self.equity_curve
        }


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略 V2（优化版）")
    logger.info("=" * 80)
    
    config = MLStrategyConfigV2()
    
    # 1. 数据加载
    loader = EnhancedDataLoader(config)
    X, y = loader.build_training_data()
    
    if X is None:
        logger.error("数据加载失败")
        return
    
    # 2. 训练ML模型
    classifier = MLClassifier(config)
    ml_results = classifier.train(X, y)
    
    # 3. 回测
    engine = OptimizedBacktestEngine(config, classifier, loader)
    backtest_results = engine.run()
    
    # 4. 保存结果
    results = {
        'ml_results': ml_results,
        'backtest_results': backtest_results['metrics'],
        'config': {
            'max_holdings': config.max_holdings,
            'min_score': config.min_score,
            'stop_loss': config.stop_loss,
            'take_profit': config.take_profit
        }
    }
    
    results_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_strategy_v2_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✅ 结果已保存: {results_path}")
    
    # 5. 登出
    jq.logout()
    
    return results


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
机器学习因子挖掘与十倍股策略 V2（优化版）
==========================================

改进：
1. 添加负样本（非十倍股）平衡数据集
2. 使用完整因子库
3. 更精确的因子计算
4. 优化的策略参数
5. 循环迭代优化

目标：1年2倍回报率（100%）

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_v2.py
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

class MLStrategyConfigV2:
    """ML策略配置V2"""
    
    def __init__(self):
        self.db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
        self.jqdata_username = "13327806797"
        
        # 回测配置
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.commission_rate = 0.0001
        
        # ML配置
        self.train_ratio = 0.7
        self.n_estimators = 200
        self.max_depth = 8
        
        # 优化后的策略参数
        self.max_holdings = 3           # 更集中
        self.single_stock_max = 0.35    # 单票更高
        self.min_score = 0.6            # 概率阈值
        self.stop_loss = -0.12          # 更紧止损
        self.take_profit = 2.0          # 让利润奔跑
        self.trailing_stop = 0.15
        self.rebalance_days = 5         # 更频繁调仓


# ============================================================
# 增强数据加载器
# ============================================================

class EnhancedDataLoader:
    """增强数据加载器（添加负样本）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.tenbagger_codes = set()
        self.all_features = None
        self.jq_authenticated = False
    
    def authenticate(self) -> bool:
        if self.jq_authenticated:
            return True
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.config.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def load_tenbagger_codes(self):
        """加载十倍股代码"""
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
        conn.close()
        self.tenbagger_codes = set(df['stock_code'].tolist())
        logger.info(f"   十倍股数量: {len(self.tenbagger_codes)}")
    
    def build_training_data(self) -> tuple:
        """
        构建训练数据（十倍股 + 非十倍股）
        """
        logger.info("📥 构建训练数据集...")
        
        if not self.authenticate():
            return None, None
        
        self.load_tenbagger_codes()
        
        # 获取股票池
        all_stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300
        all_stocks += jq.get_index_stocks('000905.XSHG')[:100]  # 中证500部分
        all_stocks = list(set(all_stocks))
        
        logger.info(f"   股票池: {len(all_stocks)}只")
        
        # 训练日期
        train_date = "2024-06-01"
        
        features_list = []
        labels = []
        
        for i, stock in enumerate(all_stocks):
            if i % 50 == 0:
                logger.info(f"   处理: {i}/{len(all_stocks)}")
            
            try:
                # 获取因子数据
                features = self._get_stock_features(stock, train_date)
                if features is not None:
                    features_list.append(features)
                    # 标签：是否为十倍股
                    label = 1 if stock in self.tenbagger_codes else 0
                    labels.append(label)
            except:
                continue
        
        if not features_list:
            return None, None
        
        X = pd.DataFrame(features_list)
        y = pd.Series(labels)
        
        logger.info(f"   训练数据: {len(X)}样本, 正样本: {y.sum()}, 负样本: {len(y) - y.sum()}")
        
        return X, y
    
    def _get_stock_features(self, stock: str, date: str) -> dict:
        """获取单只股票的因子"""
        try:
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if fund_df.empty:
                return None
            
            # 价格数据（计算动量和波动率）
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is None or len(price_df) < 60:
                return None
            
            close = price_df['close']
            volume = price_df['volume']
            
            features = {
                # 估值因子
                'pe_ratio': fund_df['pe_ratio'].iloc[0] or 0,
                'pb_ratio': fund_df['pb_ratio'].iloc[0] or 0,
                'ps_ratio': fund_df['ps_ratio'].iloc[0] or 0,
                
                # 规模因子
                'market_cap': fund_df['market_cap'].iloc[0] or 0,
                'log_market_cap': np.log(fund_df['market_cap'].iloc[0] + 1) if fund_df['market_cap'].iloc[0] else 0,
                
                # 质量因子
                'roe': fund_df['roe'].iloc[0] or 0,
                'roa': fund_df['roa'].iloc[0] or 0,
                'gross_margin': fund_df['gross_profit_margin'].iloc[0] or 0,
                
                # 成长因子
                'revenue_growth': fund_df['inc_revenue_year_on_year'].iloc[0] or 0,
                'profit_growth': fund_df['inc_net_profit_year_on_year'].iloc[0] or 0,
                
                # 动量因子
                'momentum_5d': (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0,
                'momentum_20d': (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0,
                'momentum_60d': (close.iloc[-1] / close.iloc[0] - 1) * 100,
                
                # 波动率因子
                'volatility_20d': close.iloc[-20:].pct_change().std() * np.sqrt(252) * 100 if len(close) >= 20 else 0,
                
                # 成交量因子
                'volume_ratio': volume.iloc[-5:].mean() / volume.iloc[-20:].mean() if volume.iloc[-20:].mean() > 0 else 1,
                
                # 技术因子
                'price_to_ma20': (close.iloc[-1] / close.iloc[-20:].mean() - 1) * 100 if len(close) >= 20 else 0,
            }
            
            return features
            
        except Exception as e:
            return None


# ============================================================
# ML分类器
# ============================================================

class MLClassifier:
    """ML分类器（预测是否为潜在十倍股）"""
    
    def __init__(self, config: MLStrategyConfigV2):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        self.feature_names = None
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """训练分类模型"""
        logger.info("🤖 训练ML分类模型...")
        
        self.feature_names = X.columns.tolist()
        
        # 处理缺失值和无穷值
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # 标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 划分数据
        split_idx = int(len(X) * self.config.train_ratio)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"   训练集: {len(X_train)}, 测试集: {len(X_test)}")
        
        # 创建模型（使用分类器）
        if XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                learning_rate=0.1,
                random_state=42
            )
        
        # 训练
        self.model.fit(X_train, y_train)
        
        # 评估
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        y_test_proba = self.model.predict_proba(X_test)[:, 1]
        
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_auc = roc_auc_score(y_test, y_test_proba) if len(set(y_test)) > 1 else 0
        
        logger.info(f"   训练集准确率: {train_acc:.4f}")
        logger.info(f"   测试集准确率: {test_acc:.4f}")
        logger.info(f"   测试集AUC: {test_auc:.4f}")
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=self.feature_names
            ).sort_values(ascending=False)
            
            logger.info("   特征重要性Top 10:")
            for feat, imp in self.feature_importance.head(10).items():
                logger.info(f"      {feat}: {imp:.4f}")
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'test_auc': test_auc,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else {}
        }
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """预测概率"""
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        # 对齐特征
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0
        X = X[self.feature_names]
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]


# ============================================================
# 优化回测引擎
# ============================================================

class OptimizedBacktestEngine:
    """优化回测引擎"""
    
    def __init__(self, config: MLStrategyConfigV2, classifier: MLClassifier, data_loader: EnhancedDataLoader):
        self.config = config
        self.classifier = classifier
        self.data_loader = data_loader
        self.equity_curve = []
        self.positions = {}
    
    def run(self) -> dict:
        """运行回测"""
        logger.info("🚀 运行优化回测...")
        
        # 获取交易日
        trade_days = jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池
        stocks = jq.get_index_stocks('000300.XSHG')[:100]
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载价格数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in stocks:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 初始化
        cash = self.config.initial_capital
        self.equity_curve = [cash]
        self.positions = {}
        
        rebalance_counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 计算持仓价值
            portfolio_value = cash
            for stock, pos in self.positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    portfolio_value += pos['shares'] * price
            
            # 调仓
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 计算ML得分
                scores = {}
                for stock in list(price_cache.keys())[:30]:
                    try:
                        features = self.data_loader._get_stock_features(stock, date)
                        if features:
                            features_df = pd.DataFrame([features])
                            proba = self.classifier.predict_proba(features_df)[0]
                            if proba >= self.config.min_score:
                                scores[stock] = proba
                    except:
                        continue
                
                if scores:
                    # 选股
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                    
                    # 卖出
                    to_sell = [s for s in self.positions if s not in [x[0] for x in selected]]
                    for stock in to_sell:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
                            cash += sell_value
                            del self.positions[stock]
                    
                    # 买入
                    if selected:
                        target_value = portfolio_value / len(selected)
                        for stock, score in selected:
                            if stock not in self.positions and stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                buy_value = min(target_value, cash)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0:
                                    cost = shares * price * (1 + self.config.commission_rate)
                                    if cost <= cash:
                                        cash -= cost
                                        self.positions[stock] = {
                                            'shares': shares,
                                            'cost': price
                                        }
            
            # 风控
            for stock in list(self.positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    cost = self.positions[stock]['cost']
                    pnl = (price - cost) / cost
                    
                    if pnl <= self.config.stop_loss or pnl >= self.config.take_profit:
                        sell_value = self.positions[stock]['shares'] * price * (1 - self.config.commission_rate - 0.001)
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
        equity = pd.Series(self.equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / self.config.initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 回测完成: 总收益 {total_return*100:.2f}%, 年化 {annual_return*100:.2f}%, 夏普 {sharpe:.2f}")
        
        return {
            "success": True,
            "metrics": {
                "total_return": total_return,
                "annual_return": annual_return,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "volatility": volatility
            },
            "equity_curve": self.equity_curve
        }


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘与十倍股策略 V2（优化版）")
    logger.info("=" * 80)
    
    config = MLStrategyConfigV2()
    
    # 1. 数据加载
    loader = EnhancedDataLoader(config)
    X, y = loader.build_training_data()
    
    if X is None:
        logger.error("数据加载失败")
        return
    
    # 2. 训练ML模型
    classifier = MLClassifier(config)
    ml_results = classifier.train(X, y)
    
    # 3. 回测
    engine = OptimizedBacktestEngine(config, classifier, loader)
    backtest_results = engine.run()
    
    # 4. 保存结果
    results = {
        'ml_results': ml_results,
        'backtest_results': backtest_results['metrics'],
        'config': {
            'max_holdings': config.max_holdings,
            'min_score': config.min_score,
            'stop_loss': config.stop_loss,
            'take_profit': config.take_profit
        }
    }
    
    results_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "ml_strategy_v2_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✅ 结果已保存: {results_path}")
    
    # 5. 登出
    jq.logout()
    
    return results


if __name__ == "__main__":
    main()









































