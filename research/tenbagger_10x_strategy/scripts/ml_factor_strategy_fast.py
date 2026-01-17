#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ML因子挖掘策略 - 快速版
========================
使用预加载数据，避免频繁API调用

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_fast.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import sqlite3
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

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


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def load_tenbagger_codes() -> set:
    """加载十倍股代码"""
    db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
    conn.close()
    return set(df['stock_code'].tolist())


def build_features_from_price(price_df: pd.DataFrame, stock: str, date: str) -> dict:
    """从价格数据构建特征"""
    try:
        sdf = price_df[price_df['code'] == stock].copy()
        if len(sdf) < 60:
            return None
        
        sdf = sdf.sort_values('time')
        date_dt = pd.to_datetime(date)
        sdf = sdf[sdf['time'] <= date_dt]
        
        if len(sdf) < 60:
            return None
        
        sdf = sdf.tail(60)
        close = sdf['close'].values.astype(float)
        volume = sdf['volume'].values.astype(float)
        
        if len(close) < 60 or close[-5] <= 0 or close[-20] <= 0 or close[0] <= 0:
            return None
        
        # 计算波动率
        vol_20d = 0
        if len(close) >= 21:
            pct = np.diff(close[-21:]) / close[-21:-1]
            if np.all(np.isfinite(pct)):
                vol_20d = np.std(pct) * np.sqrt(252) * 100
        
        features = {
            'momentum_5d': (close[-1] / close[-5] - 1) * 100,
            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
            'momentum_60d': (close[-1] / close[0] - 1) * 100,
            'volatility_20d': vol_20d,
            'volume_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
            'price_to_ma60': (close[-1] / np.mean(close) - 1) * 100,
            'ma5_to_ma20': (np.mean(close[-5:]) / np.mean(close[-20:]) - 1) * 100,
        }
        return features
    except Exception as e:
        return None


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘策略 - 快速版")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    tenbagger_codes = load_tenbagger_codes()
    logger.info(f"   十倍股数量: {len(tenbagger_codes)}")
    
    # ======== 配置 ========
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    initial_capital = 1000000.0
    commission = 0.0001  # 万一
    
    max_holdings = 3           # 更集中
    min_score = 0.3             # 降低阈值，让更多股票进入
    stop_loss = -0.08           # 更紧止损
    take_profit = 0.5           # 快速止盈
    rebalance_days = 5          # 更频繁调仓
    
    # ======== 获取股票池 ========
    stocks = jq.get_index_stocks('000905.XSHG')[:100]  # 中证500前100
    stocks += jq.get_index_stocks('399006.XSHE')[:50]   # 创业板前50
    stocks = list(set(stocks))
    logger.info(f"   股票池: {len(stocks)}只")
    
    # ======== 预加载所有数据 ========
    logger.info("📥 预加载价格数据...")
    price_df = jq.get_price(
        stocks,
        start_date="2023-06-01",  # 多加载一些历史数据
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume'],
        panel=False,
        skip_paused=True
    )
    logger.info(f"   数据行数: {len(price_df)}")
    
    # ======== 构建训练数据 ========
    logger.info("🔧 构建训练数据...")
    train_date = "2024-06-01"
    
    features_list = []
    labels = []
    
    for stock in stocks:
        features = build_features_from_price(price_df, stock, train_date)
        if features:
            features_list.append(features)
            labels.append(1 if stock in tenbagger_codes else 0)
    
    X_train = pd.DataFrame(features_list)
    y_train = pd.Series(labels)
    
    logger.info(f"   训练样本: {len(X_train)}, 正样本: {sum(labels)}")
    
    # ======== 训练模型 ========
    logger.info("🤖 训练ML模型...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train.fillna(0))
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_scaled, y_train)
    
    feature_importance = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    logger.info("   特征重要性:")
    for feat, imp in feature_importance.head(8).items():
        logger.info(f"      {feat}: {imp:.4f}")
    
    # ======== 回测 ========
    logger.info("🚀 运行回测...")
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    trade_days = [str(d) for d in trade_days]
    
    # 按股票建立价格缓存
    price_cache = {}
    for stock in stocks:
        sdf = price_df[price_df['code'] == stock].copy()
        if not sdf.empty:
            sdf = sdf.set_index('time')
            price_cache[stock] = sdf
    
    cash = initial_capital
    equity_curve = [cash]
    positions = {}
    
    rebalance_counter = 0
    
    for i, date in enumerate(trade_days):
        if i % 100 == 0:
            logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
        
        # 计算持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                portfolio_value += pos['shares'] * price
        
        # 调仓
        rebalance_counter += 1
        if rebalance_counter >= rebalance_days:
            rebalance_counter = 0
            
            # 计算得分
            scores = {}
            for stock in stocks:
                features = build_features_from_price(price_df, stock, date)
                if features:
                    feat_df = pd.DataFrame([features])
                    feat_scaled = scaler.transform(feat_df.fillna(0))
                    proba = model.predict_proba(feat_scaled)[0, 1]
                    
                    # 结合动量信号
                    momentum_20d = features.get('momentum_20d', 0)
                    momentum_60d = features.get('momentum_60d', 0)
                    price_to_ma20 = features.get('price_to_ma20', 0)
                    
                    # 多因子综合得分
                    if proba >= min_score and momentum_20d > 0:  # 要求正动量
                        # 动量占主导
                        score = 0.3 * proba + 0.4 * (momentum_20d / 50) + 0.3 * (momentum_60d / 100)
                        if price_to_ma20 > 0:  # 价格在均线上方
                            score *= 1.2
                        scores[stock] = max(score, 0.01)
            
            if scores:
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_holdings]
                
                # 卖出
                for stock in list(positions.keys()):
                    if stock not in [s[0] for s in selected]:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                            del positions[stock]
                
                # 买入
                if selected:
                    target_value = portfolio_value / len(selected)
                    for stock, score in selected:
                        if stock not in positions and stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            if shares > 0:
                                cost = shares * price * (1 + commission)
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {'shares': shares, 'cost': price}
        
        # 风控
        for stock in list(positions.keys()):
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                pnl = (price - positions[stock]['cost']) / positions[stock]['cost']
                
                if pnl <= stop_loss or pnl >= take_profit:
                    cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                    del positions[stock]
        
        # 更新净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
        
        equity_curve.append(portfolio_value)
    
    # ======== 计算指标 ========
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    sortino = 0
    down_returns = returns[returns < 0]
    if len(down_returns) > 0:
        down_std = down_returns.std() * np.sqrt(252)
        if down_std > 0:
            sortino = annual_return / down_std
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
    
    # ======== 生成报告 ========
    logger.info("📝 生成报告...")
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 净值曲线
        axes[0, 0].plot(equity.values, linewidth=2, color='#667eea')
        axes[0, 0].axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(range(len(equity)), initial_capital, equity.values, alpha=0.3, color='#667eea')
        axes[0, 0].set_title('Portfolio Value', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 特征重要性
        axes[0, 1].barh(feature_importance.head(8).index[::-1], feature_importance.head(8).values[::-1], color='#4ade80')
        axes[0, 1].set_title('Feature Importance', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 回撤
        axes[1, 0].fill_between(range(len(drawdown)), 0, drawdown.values * 100, color='#f87171', alpha=0.6)
        axes[1, 0].set_title('Drawdown (%)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 日度收益分布
        axes[1, 1].hist(returns[returns != 0] * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 1].axvline(x=0, color='red', linestyle='--')
        axes[1, 1].set_title('Daily Return Distribution (%)', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.2em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.85em; margin-bottom: 8px; }}
        .metric .value {{ font-size: 1.8em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        .highlight {{ color: #4ade80; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘策略报告</h1>
            <p>基于{len(tenbagger_codes)}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {start_date} ~ {end_date} | 初始资金: ¥{initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if total_return > 0 else 'negative'}">{total_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if annual_return > 0 else 'negative'}">{annual_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{sharpe:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{sortino:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{calmar:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{max_dd*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{volatility*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{win_rate*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 特征重要性分析</h2>
            <p>ML模型自动识别出的关键因子：</p>
            <table>
                <tr><th>排名</th><th>因子</th><th>重要性</th><th>说明</th></tr>
                {''.join([f"<tr><td>{i+1}</td><td><span class='highlight'>{feat}</span></td><td>{imp:.4f}</td><td></td></tr>" for i, (feat, imp) in enumerate(feature_importance.head(8).items())])}
            </table>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{min_score}</td><td>最低ML概率</td></tr>
                <tr><td>stop_loss</td><td>{stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_fast_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 登出
    jq.logout()
    
    # 打印结果
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   总收益: {total_return*100:.2f}%")
    logger.info(f"   年化收益: {annual_return*100:.2f}%")
    logger.info(f"   夏普比率: {sharpe:.2f}")
    logger.info(f"   最大回撤: {max_dd*100:.2f}%")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()


"""
ML因子挖掘策略 - 快速版
========================
使用预加载数据，避免频繁API调用

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_fast.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import sqlite3
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

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


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def load_tenbagger_codes() -> set:
    """加载十倍股代码"""
    db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
    conn.close()
    return set(df['stock_code'].tolist())


def build_features_from_price(price_df: pd.DataFrame, stock: str, date: str) -> dict:
    """从价格数据构建特征"""
    try:
        sdf = price_df[price_df['code'] == stock].copy()
        if len(sdf) < 60:
            return None
        
        sdf = sdf.sort_values('time')
        date_dt = pd.to_datetime(date)
        sdf = sdf[sdf['time'] <= date_dt]
        
        if len(sdf) < 60:
            return None
        
        sdf = sdf.tail(60)
        close = sdf['close'].values.astype(float)
        volume = sdf['volume'].values.astype(float)
        
        if len(close) < 60 or close[-5] <= 0 or close[-20] <= 0 or close[0] <= 0:
            return None
        
        # 计算波动率
        vol_20d = 0
        if len(close) >= 21:
            pct = np.diff(close[-21:]) / close[-21:-1]
            if np.all(np.isfinite(pct)):
                vol_20d = np.std(pct) * np.sqrt(252) * 100
        
        features = {
            'momentum_5d': (close[-1] / close[-5] - 1) * 100,
            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
            'momentum_60d': (close[-1] / close[0] - 1) * 100,
            'volatility_20d': vol_20d,
            'volume_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
            'price_to_ma60': (close[-1] / np.mean(close) - 1) * 100,
            'ma5_to_ma20': (np.mean(close[-5:]) / np.mean(close[-20:]) - 1) * 100,
        }
        return features
    except Exception as e:
        return None


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘策略 - 快速版")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    tenbagger_codes = load_tenbagger_codes()
    logger.info(f"   十倍股数量: {len(tenbagger_codes)}")
    
    # ======== 配置 ========
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    initial_capital = 1000000.0
    commission = 0.0001  # 万一
    
    max_holdings = 3           # 更集中
    min_score = 0.3             # 降低阈值，让更多股票进入
    stop_loss = -0.08           # 更紧止损
    take_profit = 0.5           # 快速止盈
    rebalance_days = 5          # 更频繁调仓
    
    # ======== 获取股票池 ========
    stocks = jq.get_index_stocks('000905.XSHG')[:100]  # 中证500前100
    stocks += jq.get_index_stocks('399006.XSHE')[:50]   # 创业板前50
    stocks = list(set(stocks))
    logger.info(f"   股票池: {len(stocks)}只")
    
    # ======== 预加载所有数据 ========
    logger.info("📥 预加载价格数据...")
    price_df = jq.get_price(
        stocks,
        start_date="2023-06-01",  # 多加载一些历史数据
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume'],
        panel=False,
        skip_paused=True
    )
    logger.info(f"   数据行数: {len(price_df)}")
    
    # ======== 构建训练数据 ========
    logger.info("🔧 构建训练数据...")
    train_date = "2024-06-01"
    
    features_list = []
    labels = []
    
    for stock in stocks:
        features = build_features_from_price(price_df, stock, train_date)
        if features:
            features_list.append(features)
            labels.append(1 if stock in tenbagger_codes else 0)
    
    X_train = pd.DataFrame(features_list)
    y_train = pd.Series(labels)
    
    logger.info(f"   训练样本: {len(X_train)}, 正样本: {sum(labels)}")
    
    # ======== 训练模型 ========
    logger.info("🤖 训练ML模型...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train.fillna(0))
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_scaled, y_train)
    
    feature_importance = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    logger.info("   特征重要性:")
    for feat, imp in feature_importance.head(8).items():
        logger.info(f"      {feat}: {imp:.4f}")
    
    # ======== 回测 ========
    logger.info("🚀 运行回测...")
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    trade_days = [str(d) for d in trade_days]
    
    # 按股票建立价格缓存
    price_cache = {}
    for stock in stocks:
        sdf = price_df[price_df['code'] == stock].copy()
        if not sdf.empty:
            sdf = sdf.set_index('time')
            price_cache[stock] = sdf
    
    cash = initial_capital
    equity_curve = [cash]
    positions = {}
    
    rebalance_counter = 0
    
    for i, date in enumerate(trade_days):
        if i % 100 == 0:
            logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
        
        # 计算持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                portfolio_value += pos['shares'] * price
        
        # 调仓
        rebalance_counter += 1
        if rebalance_counter >= rebalance_days:
            rebalance_counter = 0
            
            # 计算得分
            scores = {}
            for stock in stocks:
                features = build_features_from_price(price_df, stock, date)
                if features:
                    feat_df = pd.DataFrame([features])
                    feat_scaled = scaler.transform(feat_df.fillna(0))
                    proba = model.predict_proba(feat_scaled)[0, 1]
                    
                    # 结合动量信号
                    momentum_20d = features.get('momentum_20d', 0)
                    momentum_60d = features.get('momentum_60d', 0)
                    price_to_ma20 = features.get('price_to_ma20', 0)
                    
                    # 多因子综合得分
                    if proba >= min_score and momentum_20d > 0:  # 要求正动量
                        # 动量占主导
                        score = 0.3 * proba + 0.4 * (momentum_20d / 50) + 0.3 * (momentum_60d / 100)
                        if price_to_ma20 > 0:  # 价格在均线上方
                            score *= 1.2
                        scores[stock] = max(score, 0.01)
            
            if scores:
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_holdings]
                
                # 卖出
                for stock in list(positions.keys()):
                    if stock not in [s[0] for s in selected]:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                            del positions[stock]
                
                # 买入
                if selected:
                    target_value = portfolio_value / len(selected)
                    for stock, score in selected:
                        if stock not in positions and stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            if shares > 0:
                                cost = shares * price * (1 + commission)
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {'shares': shares, 'cost': price}
        
        # 风控
        for stock in list(positions.keys()):
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                pnl = (price - positions[stock]['cost']) / positions[stock]['cost']
                
                if pnl <= stop_loss or pnl >= take_profit:
                    cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                    del positions[stock]
        
        # 更新净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
        
        equity_curve.append(portfolio_value)
    
    # ======== 计算指标 ========
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    sortino = 0
    down_returns = returns[returns < 0]
    if len(down_returns) > 0:
        down_std = down_returns.std() * np.sqrt(252)
        if down_std > 0:
            sortino = annual_return / down_std
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
    
    # ======== 生成报告 ========
    logger.info("📝 生成报告...")
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 净值曲线
        axes[0, 0].plot(equity.values, linewidth=2, color='#667eea')
        axes[0, 0].axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(range(len(equity)), initial_capital, equity.values, alpha=0.3, color='#667eea')
        axes[0, 0].set_title('Portfolio Value', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 特征重要性
        axes[0, 1].barh(feature_importance.head(8).index[::-1], feature_importance.head(8).values[::-1], color='#4ade80')
        axes[0, 1].set_title('Feature Importance', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 回撤
        axes[1, 0].fill_between(range(len(drawdown)), 0, drawdown.values * 100, color='#f87171', alpha=0.6)
        axes[1, 0].set_title('Drawdown (%)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 日度收益分布
        axes[1, 1].hist(returns[returns != 0] * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 1].axvline(x=0, color='red', linestyle='--')
        axes[1, 1].set_title('Daily Return Distribution (%)', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.2em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.85em; margin-bottom: 8px; }}
        .metric .value {{ font-size: 1.8em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        .highlight {{ color: #4ade80; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘策略报告</h1>
            <p>基于{len(tenbagger_codes)}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {start_date} ~ {end_date} | 初始资金: ¥{initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if total_return > 0 else 'negative'}">{total_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if annual_return > 0 else 'negative'}">{annual_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{sharpe:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{sortino:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{calmar:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{max_dd*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{volatility*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{win_rate*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 特征重要性分析</h2>
            <p>ML模型自动识别出的关键因子：</p>
            <table>
                <tr><th>排名</th><th>因子</th><th>重要性</th><th>说明</th></tr>
                {''.join([f"<tr><td>{i+1}</td><td><span class='highlight'>{feat}</span></td><td>{imp:.4f}</td><td></td></tr>" for i, (feat, imp) in enumerate(feature_importance.head(8).items())])}
            </table>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{min_score}</td><td>最低ML概率</td></tr>
                <tr><td>stop_loss</td><td>{stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_fast_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 登出
    jq.logout()
    
    # 打印结果
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   总收益: {total_return*100:.2f}%")
    logger.info(f"   年化收益: {annual_return*100:.2f}%")
    logger.info(f"   夏普比率: {sharpe:.2f}")
    logger.info(f"   最大回撤: {max_dd*100:.2f}%")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()


"""
ML因子挖掘策略 - 快速版
========================
使用预加载数据，避免频繁API调用

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_fast.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import sqlite3
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

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


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def load_tenbagger_codes() -> set:
    """加载十倍股代码"""
    db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
    conn.close()
    return set(df['stock_code'].tolist())


def build_features_from_price(price_df: pd.DataFrame, stock: str, date: str) -> dict:
    """从价格数据构建特征"""
    try:
        sdf = price_df[price_df['code'] == stock].copy()
        if len(sdf) < 60:
            return None
        
        sdf = sdf.sort_values('time')
        date_dt = pd.to_datetime(date)
        sdf = sdf[sdf['time'] <= date_dt]
        
        if len(sdf) < 60:
            return None
        
        sdf = sdf.tail(60)
        close = sdf['close'].values.astype(float)
        volume = sdf['volume'].values.astype(float)
        
        if len(close) < 60 or close[-5] <= 0 or close[-20] <= 0 or close[0] <= 0:
            return None
        
        # 计算波动率
        vol_20d = 0
        if len(close) >= 21:
            pct = np.diff(close[-21:]) / close[-21:-1]
            if np.all(np.isfinite(pct)):
                vol_20d = np.std(pct) * np.sqrt(252) * 100
        
        features = {
            'momentum_5d': (close[-1] / close[-5] - 1) * 100,
            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
            'momentum_60d': (close[-1] / close[0] - 1) * 100,
            'volatility_20d': vol_20d,
            'volume_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
            'price_to_ma60': (close[-1] / np.mean(close) - 1) * 100,
            'ma5_to_ma20': (np.mean(close[-5:]) / np.mean(close[-20:]) - 1) * 100,
        }
        return features
    except Exception as e:
        return None


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘策略 - 快速版")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    tenbagger_codes = load_tenbagger_codes()
    logger.info(f"   十倍股数量: {len(tenbagger_codes)}")
    
    # ======== 配置 ========
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    initial_capital = 1000000.0
    commission = 0.0001  # 万一
    
    max_holdings = 3           # 更集中
    min_score = 0.3             # 降低阈值，让更多股票进入
    stop_loss = -0.08           # 更紧止损
    take_profit = 0.5           # 快速止盈
    rebalance_days = 5          # 更频繁调仓
    
    # ======== 获取股票池 ========
    stocks = jq.get_index_stocks('000905.XSHG')[:100]  # 中证500前100
    stocks += jq.get_index_stocks('399006.XSHE')[:50]   # 创业板前50
    stocks = list(set(stocks))
    logger.info(f"   股票池: {len(stocks)}只")
    
    # ======== 预加载所有数据 ========
    logger.info("📥 预加载价格数据...")
    price_df = jq.get_price(
        stocks,
        start_date="2023-06-01",  # 多加载一些历史数据
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume'],
        panel=False,
        skip_paused=True
    )
    logger.info(f"   数据行数: {len(price_df)}")
    
    # ======== 构建训练数据 ========
    logger.info("🔧 构建训练数据...")
    train_date = "2024-06-01"
    
    features_list = []
    labels = []
    
    for stock in stocks:
        features = build_features_from_price(price_df, stock, train_date)
        if features:
            features_list.append(features)
            labels.append(1 if stock in tenbagger_codes else 0)
    
    X_train = pd.DataFrame(features_list)
    y_train = pd.Series(labels)
    
    logger.info(f"   训练样本: {len(X_train)}, 正样本: {sum(labels)}")
    
    # ======== 训练模型 ========
    logger.info("🤖 训练ML模型...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train.fillna(0))
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_scaled, y_train)
    
    feature_importance = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    logger.info("   特征重要性:")
    for feat, imp in feature_importance.head(8).items():
        logger.info(f"      {feat}: {imp:.4f}")
    
    # ======== 回测 ========
    logger.info("🚀 运行回测...")
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    trade_days = [str(d) for d in trade_days]
    
    # 按股票建立价格缓存
    price_cache = {}
    for stock in stocks:
        sdf = price_df[price_df['code'] == stock].copy()
        if not sdf.empty:
            sdf = sdf.set_index('time')
            price_cache[stock] = sdf
    
    cash = initial_capital
    equity_curve = [cash]
    positions = {}
    
    rebalance_counter = 0
    
    for i, date in enumerate(trade_days):
        if i % 100 == 0:
            logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
        
        # 计算持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                portfolio_value += pos['shares'] * price
        
        # 调仓
        rebalance_counter += 1
        if rebalance_counter >= rebalance_days:
            rebalance_counter = 0
            
            # 计算得分
            scores = {}
            for stock in stocks:
                features = build_features_from_price(price_df, stock, date)
                if features:
                    feat_df = pd.DataFrame([features])
                    feat_scaled = scaler.transform(feat_df.fillna(0))
                    proba = model.predict_proba(feat_scaled)[0, 1]
                    
                    # 结合动量信号
                    momentum_20d = features.get('momentum_20d', 0)
                    momentum_60d = features.get('momentum_60d', 0)
                    price_to_ma20 = features.get('price_to_ma20', 0)
                    
                    # 多因子综合得分
                    if proba >= min_score and momentum_20d > 0:  # 要求正动量
                        # 动量占主导
                        score = 0.3 * proba + 0.4 * (momentum_20d / 50) + 0.3 * (momentum_60d / 100)
                        if price_to_ma20 > 0:  # 价格在均线上方
                            score *= 1.2
                        scores[stock] = max(score, 0.01)
            
            if scores:
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_holdings]
                
                # 卖出
                for stock in list(positions.keys()):
                    if stock not in [s[0] for s in selected]:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                            del positions[stock]
                
                # 买入
                if selected:
                    target_value = portfolio_value / len(selected)
                    for stock, score in selected:
                        if stock not in positions and stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            if shares > 0:
                                cost = shares * price * (1 + commission)
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {'shares': shares, 'cost': price}
        
        # 风控
        for stock in list(positions.keys()):
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                pnl = (price - positions[stock]['cost']) / positions[stock]['cost']
                
                if pnl <= stop_loss or pnl >= take_profit:
                    cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                    del positions[stock]
        
        # 更新净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
        
        equity_curve.append(portfolio_value)
    
    # ======== 计算指标 ========
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    sortino = 0
    down_returns = returns[returns < 0]
    if len(down_returns) > 0:
        down_std = down_returns.std() * np.sqrt(252)
        if down_std > 0:
            sortino = annual_return / down_std
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
    
    # ======== 生成报告 ========
    logger.info("📝 生成报告...")
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 净值曲线
        axes[0, 0].plot(equity.values, linewidth=2, color='#667eea')
        axes[0, 0].axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(range(len(equity)), initial_capital, equity.values, alpha=0.3, color='#667eea')
        axes[0, 0].set_title('Portfolio Value', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 特征重要性
        axes[0, 1].barh(feature_importance.head(8).index[::-1], feature_importance.head(8).values[::-1], color='#4ade80')
        axes[0, 1].set_title('Feature Importance', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 回撤
        axes[1, 0].fill_between(range(len(drawdown)), 0, drawdown.values * 100, color='#f87171', alpha=0.6)
        axes[1, 0].set_title('Drawdown (%)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 日度收益分布
        axes[1, 1].hist(returns[returns != 0] * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 1].axvline(x=0, color='red', linestyle='--')
        axes[1, 1].set_title('Daily Return Distribution (%)', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.2em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.85em; margin-bottom: 8px; }}
        .metric .value {{ font-size: 1.8em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        .highlight {{ color: #4ade80; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘策略报告</h1>
            <p>基于{len(tenbagger_codes)}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {start_date} ~ {end_date} | 初始资金: ¥{initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if total_return > 0 else 'negative'}">{total_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if annual_return > 0 else 'negative'}">{annual_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{sharpe:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{sortino:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{calmar:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{max_dd*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{volatility*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{win_rate*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 特征重要性分析</h2>
            <p>ML模型自动识别出的关键因子：</p>
            <table>
                <tr><th>排名</th><th>因子</th><th>重要性</th><th>说明</th></tr>
                {''.join([f"<tr><td>{i+1}</td><td><span class='highlight'>{feat}</span></td><td>{imp:.4f}</td><td></td></tr>" for i, (feat, imp) in enumerate(feature_importance.head(8).items())])}
            </table>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{min_score}</td><td>最低ML概率</td></tr>
                <tr><td>stop_loss</td><td>{stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_fast_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 登出
    jq.logout()
    
    # 打印结果
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   总收益: {total_return*100:.2f}%")
    logger.info(f"   年化收益: {annual_return*100:.2f}%")
    logger.info(f"   夏普比率: {sharpe:.2f}")
    logger.info(f"   最大回撤: {max_dd*100:.2f}%")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()


"""
ML因子挖掘策略 - 快速版
========================
使用预加载数据，避免频繁API调用

代码位置: research/tenbagger_10x_strategy/scripts/ml_factor_strategy_fast.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import sqlite3
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

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


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def load_tenbagger_codes() -> set:
    """加载十倍股代码"""
    db_path = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "data" / "tenbagger_features.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT stock_code FROM tenbagger_stocks", conn)
    conn.close()
    return set(df['stock_code'].tolist())


def build_features_from_price(price_df: pd.DataFrame, stock: str, date: str) -> dict:
    """从价格数据构建特征"""
    try:
        sdf = price_df[price_df['code'] == stock].copy()
        if len(sdf) < 60:
            return None
        
        sdf = sdf.sort_values('time')
        date_dt = pd.to_datetime(date)
        sdf = sdf[sdf['time'] <= date_dt]
        
        if len(sdf) < 60:
            return None
        
        sdf = sdf.tail(60)
        close = sdf['close'].values.astype(float)
        volume = sdf['volume'].values.astype(float)
        
        if len(close) < 60 or close[-5] <= 0 or close[-20] <= 0 or close[0] <= 0:
            return None
        
        # 计算波动率
        vol_20d = 0
        if len(close) >= 21:
            pct = np.diff(close[-21:]) / close[-21:-1]
            if np.all(np.isfinite(pct)):
                vol_20d = np.std(pct) * np.sqrt(252) * 100
        
        features = {
            'momentum_5d': (close[-1] / close[-5] - 1) * 100,
            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
            'momentum_60d': (close[-1] / close[0] - 1) * 100,
            'volatility_20d': vol_20d,
            'volume_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
            'price_to_ma60': (close[-1] / np.mean(close) - 1) * 100,
            'ma5_to_ma20': (np.mean(close[-5:]) / np.mean(close[-20:]) - 1) * 100,
        }
        return features
    except Exception as e:
        return None


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🤖 ML因子挖掘策略 - 快速版")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    tenbagger_codes = load_tenbagger_codes()
    logger.info(f"   十倍股数量: {len(tenbagger_codes)}")
    
    # ======== 配置 ========
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    initial_capital = 1000000.0
    commission = 0.0001  # 万一
    
    max_holdings = 3           # 更集中
    min_score = 0.3             # 降低阈值，让更多股票进入
    stop_loss = -0.08           # 更紧止损
    take_profit = 0.5           # 快速止盈
    rebalance_days = 5          # 更频繁调仓
    
    # ======== 获取股票池 ========
    stocks = jq.get_index_stocks('000905.XSHG')[:100]  # 中证500前100
    stocks += jq.get_index_stocks('399006.XSHE')[:50]   # 创业板前50
    stocks = list(set(stocks))
    logger.info(f"   股票池: {len(stocks)}只")
    
    # ======== 预加载所有数据 ========
    logger.info("📥 预加载价格数据...")
    price_df = jq.get_price(
        stocks,
        start_date="2023-06-01",  # 多加载一些历史数据
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume'],
        panel=False,
        skip_paused=True
    )
    logger.info(f"   数据行数: {len(price_df)}")
    
    # ======== 构建训练数据 ========
    logger.info("🔧 构建训练数据...")
    train_date = "2024-06-01"
    
    features_list = []
    labels = []
    
    for stock in stocks:
        features = build_features_from_price(price_df, stock, train_date)
        if features:
            features_list.append(features)
            labels.append(1 if stock in tenbagger_codes else 0)
    
    X_train = pd.DataFrame(features_list)
    y_train = pd.Series(labels)
    
    logger.info(f"   训练样本: {len(X_train)}, 正样本: {sum(labels)}")
    
    # ======== 训练模型 ========
    logger.info("🤖 训练ML模型...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train.fillna(0))
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_scaled, y_train)
    
    feature_importance = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    logger.info("   特征重要性:")
    for feat, imp in feature_importance.head(8).items():
        logger.info(f"      {feat}: {imp:.4f}")
    
    # ======== 回测 ========
    logger.info("🚀 运行回测...")
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    trade_days = [str(d) for d in trade_days]
    
    # 按股票建立价格缓存
    price_cache = {}
    for stock in stocks:
        sdf = price_df[price_df['code'] == stock].copy()
        if not sdf.empty:
            sdf = sdf.set_index('time')
            price_cache[stock] = sdf
    
    cash = initial_capital
    equity_curve = [cash]
    positions = {}
    
    rebalance_counter = 0
    
    for i, date in enumerate(trade_days):
        if i % 100 == 0:
            logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
        
        # 计算持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                portfolio_value += pos['shares'] * price
        
        # 调仓
        rebalance_counter += 1
        if rebalance_counter >= rebalance_days:
            rebalance_counter = 0
            
            # 计算得分
            scores = {}
            for stock in stocks:
                features = build_features_from_price(price_df, stock, date)
                if features:
                    feat_df = pd.DataFrame([features])
                    feat_scaled = scaler.transform(feat_df.fillna(0))
                    proba = model.predict_proba(feat_scaled)[0, 1]
                    
                    # 结合动量信号
                    momentum_20d = features.get('momentum_20d', 0)
                    momentum_60d = features.get('momentum_60d', 0)
                    price_to_ma20 = features.get('price_to_ma20', 0)
                    
                    # 多因子综合得分
                    if proba >= min_score and momentum_20d > 0:  # 要求正动量
                        # 动量占主导
                        score = 0.3 * proba + 0.4 * (momentum_20d / 50) + 0.3 * (momentum_60d / 100)
                        if price_to_ma20 > 0:  # 价格在均线上方
                            score *= 1.2
                        scores[stock] = max(score, 0.01)
            
            if scores:
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_holdings]
                
                # 卖出
                for stock in list(positions.keys()):
                    if stock not in [s[0] for s in selected]:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                            del positions[stock]
                
                # 买入
                if selected:
                    target_value = portfolio_value / len(selected)
                    for stock, score in selected:
                        if stock not in positions and stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            if shares > 0:
                                cost = shares * price * (1 + commission)
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {'shares': shares, 'cost': price}
        
        # 风控
        for stock in list(positions.keys()):
            if stock in price_cache and date in price_cache[stock].index:
                price = price_cache[stock].loc[date, 'close']
                pnl = (price - positions[stock]['cost']) / positions[stock]['cost']
                
                if pnl <= stop_loss or pnl >= take_profit:
                    cash += positions[stock]['shares'] * price * (1 - commission - 0.001)
                    del positions[stock]
        
        # 更新净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in price_cache and date in price_cache[stock].index:
                portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
        
        equity_curve.append(portfolio_value)
    
    # ======== 计算指标 ========
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    sortino = 0
    down_returns = returns[returns < 0]
    if len(down_returns) > 0:
        down_std = down_returns.std() * np.sqrt(252)
        if down_std > 0:
            sortino = annual_return / down_std
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    win_rate = (returns > 0).sum() / len(returns[returns != 0]) if len(returns[returns != 0]) > 0 else 0
    
    # ======== 生成报告 ========
    logger.info("📝 生成报告...")
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 净值曲线
        axes[0, 0].plot(equity.values, linewidth=2, color='#667eea')
        axes[0, 0].axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(range(len(equity)), initial_capital, equity.values, alpha=0.3, color='#667eea')
        axes[0, 0].set_title('Portfolio Value', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 特征重要性
        axes[0, 1].barh(feature_importance.head(8).index[::-1], feature_importance.head(8).values[::-1], color='#4ade80')
        axes[0, 1].set_title('Feature Importance', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 回撤
        axes[1, 0].fill_between(range(len(drawdown)), 0, drawdown.values * 100, color='#f87171', alpha=0.6)
        axes[1, 0].set_title('Drawdown (%)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 日度收益分布
        axes[1, 1].hist(returns[returns != 0] * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 1].axvline(x=0, color='red', linestyle='--')
        axes[1, 1].set_title('Daily Return Distribution (%)', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ML因子挖掘策略报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.2em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.85em; margin-bottom: 8px; }}
        .metric .value {{ font-size: 1.8em; font-weight: bold; color: #667eea; }}
        .metric .value.positive {{ color: #4ade80; }}
        .metric .value.negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .section h2 {{ color: #667eea; margin-top: 0; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 10px; }}
        .chart {{ text-align: center; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        .highlight {{ color: #4ade80; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ML因子挖掘策略报告</h1>
            <p>基于{len(tenbagger_codes)}只历史十倍股特征 | 机器学习因子挖掘</p>
            <p>回测区间: {start_date} ~ {end_date} | 初始资金: ¥{initial_capital:,.0f}</p>
            <p>佣金: 万分之一 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if total_return > 0 else 'negative'}">{total_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if annual_return > 0 else 'negative'}">{annual_return*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{sharpe:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">索提诺比率</div>
                <div class="value">{sortino:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{calmar:.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{max_dd*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{volatility*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">胜率</div>
                <div class="value">{win_rate*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 特征重要性分析</h2>
            <p>ML模型自动识别出的关键因子：</p>
            <table>
                <tr><th>排名</th><th>因子</th><th>重要性</th><th>说明</th></tr>
                {''.join([f"<tr><td>{i+1}</td><td><span class='highlight'>{feat}</span></td><td>{imp:.4f}</td><td></td></tr>" for i, (feat, imp) in enumerate(feature_importance.head(8).items())])}
            </table>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th><th>说明</th></tr>
                <tr><td>max_holdings</td><td>{max_holdings}</td><td>最大持仓数</td></tr>
                <tr><td>min_score</td><td>{min_score}</td><td>最低ML概率</td></tr>
                <tr><td>stop_loss</td><td>{stop_loss*100:.0f}%</td><td>止损比例</td></tr>
                <tr><td>take_profit</td><td>{take_profit*100:.0f}%</td><td>止盈比例</td></tr>
                <tr><td>rebalance_days</td><td>{rebalance_days}</td><td>调仓周期</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"ml_factor_fast_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 登出
    jq.logout()
    
    # 打印结果
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   总收益: {total_return*100:.2f}%")
    logger.info(f"   年化收益: {annual_return*100:.2f}%")
    logger.info(f"   夏普比率: {sharpe:.2f}")
    logger.info(f"   最大回撤: {max_dd*100:.2f}%")
    logger.info(f"   报告: {report_path}")
    logger.info("=" * 80)
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()

