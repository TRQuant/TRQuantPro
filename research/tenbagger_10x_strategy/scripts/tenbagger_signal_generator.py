#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股实时信号生成器
====================

功能：
1. 每日扫描生成买入信号
2. 持仓跟踪与卖出信号
3. 样本外验证
4. 信号历史记录

使用验证有效的最优参数：
- max_holdings: 2
- momentum_period: 20
- rebalance_days: 3
- stop_loss: -8%
- take_profit: 50%

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_signal_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

@dataclass
class SignalConfig:
    """信号配置"""
    max_holdings: int = 2
    momentum_period: int = 20
    min_momentum: float = 10.0  # 最低20日涨幅%
    stop_loss: float = -0.08
    take_profit: float = 0.50
    trailing_stop: float = 0.15
    
    # 股票池配置
    stock_pool: str = "growth"  # growth/value/all
    max_pool_size: int = 100


# ============================================================
# 信号数据结构
# ============================================================

@dataclass
class Signal:
    """交易信号"""
    date: str
    symbol: str
    name: str
    action: str  # BUY/SELL/HOLD
    reason: str
    score: float
    momentum_20d: float
    momentum_60d: float
    current_price: float
    target_price: float = 0.0
    stop_price: float = 0.0
    priority: int = 0


@dataclass
class Position:
    """持仓记录"""
    symbol: str
    name: str
    shares: int
    cost: float
    entry_date: str
    highest_price: float
    current_price: float
    pnl_pct: float
    status: str  # OPEN/CLOSED


# ============================================================
# 信号生成器
# ============================================================

class TenbaggerSignalGenerator:
    """十倍股信号生成器"""
    
    def __init__(self, config: SignalConfig = None):
        self.config = config or SignalConfig()
        self.db_path = PROJECT_ROOT / "data" / "tenbagger_signals.db"
        self._init_db()
        self.jq_authenticated = False
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                symbol TEXT,
                name TEXT,
                action TEXT,
                reason TEXT,
                score REAL,
                momentum_20d REAL,
                momentum_60d REAL,
                current_price REAL,
                target_price REAL,
                stop_price REAL,
                created_at TEXT
            )
        ''')
        
        # 持仓表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                shares INTEGER,
                cost REAL,
                entry_date TEXT,
                highest_price REAL,
                current_price REAL,
                pnl_pct REAL,
                status TEXT,
                exit_date TEXT,
                exit_reason TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth("13327806797", pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_stock_pool(self) -> List[str]:
        """获取股票池"""
        stocks = []
        
        # 创业板
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        # 中证500
        stocks += jq.get_index_stocks('000905.XSHG')[:30]
        # 科创50
        try:
            kc50 = jq.get_index_stocks('000688.XSHG')
            if kc50:
                stocks += kc50[:20]
        except:
            pass
        
        return list(set(stocks))[:self.config.max_pool_size]
    
    def compute_momentum_score(self, df: pd.DataFrame) -> Dict:
        """计算动量得分"""
        if len(df) < self.config.momentum_period:
            return None
        
        close = df['close'].values
        volume = df['volume'].values
        
        # 动量
        m5 = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
        m20 = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
        m60 = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
        
        # 量比
        vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
        
        # 价格位置
        ma20 = np.mean(close[-20:])
        price_to_ma20 = (close[-1] / ma20 - 1) * 100 if ma20 > 0 else 0
        
        # 综合得分
        score = (
            m20 * 0.4 +
            m60 * 0.2 +
            (vol_ratio - 1) * 20 +
            (20 if price_to_ma20 > 0 else 0)
        )
        
        return {
            'momentum_5d': m5,
            'momentum_20d': m20,
            'momentum_60d': m60,
            'vol_ratio': vol_ratio,
            'price_to_ma20': price_to_ma20,
            'score': score,
            'current_price': close[-1]
        }
    
    def generate_buy_signals(self, date: str = None) -> List[Signal]:
        """生成买入信号"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 扫描买入信号 ({date})...")
        
        # 获取股票池
        stocks = self.get_stock_pool()
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 获取历史数据
        start_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=date,
            frequency='daily',
            fields=['close', 'volume', 'high', 'low'],
            panel=False,
            skip_paused=True
        )
        
        # 计算得分
        candidates = []
        for stock in stocks:
            try:
                sdf = price_df[price_df['code'] == stock].copy()
                if sdf.empty or len(sdf) < 60:
                    continue
                
                result = self.compute_momentum_score(sdf)
                if result is None:
                    continue
                
                # 筛选条件
                if result['momentum_20d'] >= self.config.min_momentum:
                    # 获取名称
                    info = jq.get_security_info(stock)
                    name = info.display_name if info else stock
                    
                    candidates.append({
                        'symbol': stock,
                        'name': name,
                        **result
                    })
            except Exception as e:
                continue
        
        # 排序并选择Top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:self.config.max_holdings]
        
        # 生成信号
        signals = []
        for c in top_candidates:
            signal = Signal(
                date=date,
                symbol=c['symbol'],
                name=c['name'],
                action='BUY',
                reason=f"动量{c['momentum_20d']:.1f}%，得分{c['score']:.1f}",
                score=c['score'],
                momentum_20d=c['momentum_20d'],
                momentum_60d=c['momentum_60d'],
                current_price=c['current_price'],
                target_price=c['current_price'] * (1 + self.config.take_profit),
                stop_price=c['current_price'] * (1 + self.config.stop_loss),
                priority=len(signals)
            )
            signals.append(signal)
        
        logger.info(f"✅ 生成 {len(signals)} 个买入信号")
        
        # 保存到数据库
        self._save_signals(signals)
        
        return signals
    
    def generate_sell_signals(self, positions: List[Position]) -> List[Signal]:
        """生成卖出信号"""
        if not self.authenticate_jqdata():
            return []
        
        signals = []
        date = datetime.now().strftime('%Y-%m-%d')
        
        for pos in positions:
            if pos.status != 'OPEN':
                continue
            
            # 获取最新价格
            try:
                df = jq.get_price(pos.symbol, end_date=date, count=1, fields=['close'])
                if df.empty:
                    continue
                
                current_price = df['close'].iloc[0]
                pnl = (current_price - pos.cost) / pos.cost
                drawdown = (current_price - pos.highest_price) / pos.highest_price if pos.highest_price > 0 else 0
                
                reason = None
                
                # 止损
                if pnl <= self.config.stop_loss:
                    reason = f'止损 {pnl*100:.1f}%'
                # 止盈
                elif pnl >= self.config.take_profit:
                    reason = f'止盈 {pnl*100:.1f}%'
                # 移动止损
                elif drawdown <= -self.config.trailing_stop and pnl > 0.1:
                    reason = f'移动止损 {drawdown*100:.1f}%'
                
                if reason:
                    signal = Signal(
                        date=date,
                        symbol=pos.symbol,
                        name=pos.name,
                        action='SELL',
                        reason=reason,
                        score=0,
                        momentum_20d=0,
                        momentum_60d=0,
                        current_price=current_price,
                        priority=0
                    )
                    signals.append(signal)
                    
            except Exception as e:
                logger.warning(f"检查{pos.symbol}失败: {e}")
        
        return signals
    
    def _save_signals(self, signals: List[Signal]):
        """保存信号到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for s in signals:
            cursor.execute('''
                INSERT INTO signals (date, symbol, name, action, reason, score, 
                                    momentum_20d, momentum_60d, current_price, 
                                    target_price, stop_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s.date, s.symbol, s.name, s.action, s.reason, s.score,
                  s.momentum_20d, s.momentum_60d, s.current_price,
                  s.target_price, s.stop_price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_latest_signals(self, n: int = 10) -> List[Dict]:
        """获取最新信号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals ORDER BY created_at DESC LIMIT ?
        ''', (n,))
        
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def validate_out_of_sample(self, train_end: str, test_start: str, test_end: str) -> Dict:
        """样本外验证"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': '认证失败'}
        
        logger.info(f"🔬 样本外验证: 训练截止{train_end}, 测试{test_start}~{test_end}")
        
        # 获取数据
        stocks = self.get_stock_pool()
        
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(test_start, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
            end_date=test_end,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        # 简化回测
        close_df = price_df.pivot(index='time', columns='code', values='close')
        momentum = close_df.pct_change(self.config.momentum_period)
        
        dates = close_df.index
        test_dates = [d for d in dates if str(d.date()) >= test_start]
        
        initial_capital = 1000000
        cash = initial_capital
        positions = {}
        equity_curve = []
        
        rebalance_days = 3
        counter = 0
        
        for date in test_dates:
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            # 调仓
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                mom_today = momentum.loc[date].dropna()
                if len(mom_today) > 0:
                    top_stocks = mom_today.nlargest(self.config.max_holdings).index.tolist()
                    
                    # 卖出
                    for stock in list(positions.keys()):
                        if stock not in top_stocks:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price):
                                cash += positions[stock]['shares'] * price * 0.999
                                del positions[stock]
                    
                    # 买入
                    for stock in top_stocks:
                        if stock not in positions:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price) and price > 0:
                                buy_value = min(portfolio_value / self.config.max_holdings, cash * 0.9)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0 and shares * price <= cash:
                                    cash -= shares * price * 1.001
                                    positions[stock] = {'shares': shares, 'cost': price}
            
            # 记录
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        
        returns = equity.pct_change().fillna(0)
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 验证完成:")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化: {annual_return*100:.2f}%")
        logger.info(f"   夏普: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'train_period': f'~{train_end}',
            'test_period': f'{test_start}~{test_end}',
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'max_drawdown': max_dd,
                'volatility': volatility
            }
        }
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成信号
        buy_signals = self.generate_buy_signals(date)
        
        # 获取历史信号
        history = self.get_latest_signals(20)
        
        # 生成HTML
        signals_html = ""
        for s in buy_signals:
            signals_html += f"""
            <div class="signal-card">
                <h3>{s.name} ({s.symbol})</h3>
                <p>📈 动量20d: {s.momentum_20d:.1f}% | 动量60d: {s.momentum_60d:.1f}%</p>
                <p>💰 当前价: ¥{s.current_price:.2f}</p>
                <p>🎯 目标价: ¥{s.target_price:.2f} (+{self.config.take_profit*100:.0f}%)</p>
                <p>🛑 止损价: ¥{s.stop_price:.2f} ({self.config.stop_loss*100:.0f}%)</p>
                <p>📊 得分: {s.score:.1f}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股每日信号报告 - {date}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: #1a1a2e; }}
        .signals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .signal-card {{ background: rgba(255,255,255,0.08); padding: 25px; border-radius: 16px; border-left: 4px solid #ff6b6b; }}
        .signal-card h3 {{ color: #ff6b6b; margin-top: 0; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 25px; }}
        .section h2 {{ color: #feca57; margin-top: 0; }}
        .config {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .config-item {{ background: rgba(255,107,107,0.2); padding: 15px; border-radius: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股每日信号</h1>
            <p>{date} | 基于动量因子选股</p>
        </div>
        
        <div class="section">
            <h2>📊 今日买入信号 ({len(buy_signals)}只)</h2>
            <div class="signals">
                {signals_html if signals_html else '<p>今日无买入信号</p>'}
            </div>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略配置</h2>
            <div class="config">
                <div class="config-item">
                    <div>持仓数量</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.max_holdings}</div>
                </div>
                <div class="config-item">
                    <div>动量周期</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.momentum_period}天</div>
                </div>
                <div class="config-item">
                    <div>止损线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.stop_loss*100:.0f}%</div>
                </div>
                <div class="config-item">
                    <div>止盈线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.take_profit*100:.0f}%</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 使用说明</h2>
            <ul>
                <li>信号基于20日动量排名生成</li>
                <li>建议集中持有2只股票</li>
                <li>严格执行止损(-8%)和止盈(+50%)</li>
                <li>每3天调仓一次</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股信号生成器")
    logger.info("=" * 80)
    
    generator = TenbaggerSignalGenerator()
    
    # 1. 生成今日信号
    logger.info("\n📊 生成今日信号...")
    signals = generator.generate_buy_signals()
    
    for s in signals:
        logger.info(f"   {s.name} ({s.symbol}): {s.reason}")
    
    # 2. 样本外验证
    logger.info("\n🔬 样本外验证...")
    validation = generator.validate_out_of_sample(
        train_end="2024-06-30",
        test_start="2024-07-01",
        test_end="2025-12-20"
    )
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generator.generate_daily_report()
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    report_path = reports_dir / f"daily_signal_{datetime.now().strftime('%Y%m%d')}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info("=" * 80)
    
    return {
        'signals': [asdict(s) for s in signals],
        'validation': validation,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
十倍股实时信号生成器
====================

功能：
1. 每日扫描生成买入信号
2. 持仓跟踪与卖出信号
3. 样本外验证
4. 信号历史记录

使用验证有效的最优参数：
- max_holdings: 2
- momentum_period: 20
- rebalance_days: 3
- stop_loss: -8%
- take_profit: 50%

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_signal_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

@dataclass
class SignalConfig:
    """信号配置"""
    max_holdings: int = 2
    momentum_period: int = 20
    min_momentum: float = 10.0  # 最低20日涨幅%
    stop_loss: float = -0.08
    take_profit: float = 0.50
    trailing_stop: float = 0.15
    
    # 股票池配置
    stock_pool: str = "growth"  # growth/value/all
    max_pool_size: int = 100


# ============================================================
# 信号数据结构
# ============================================================

@dataclass
class Signal:
    """交易信号"""
    date: str
    symbol: str
    name: str
    action: str  # BUY/SELL/HOLD
    reason: str
    score: float
    momentum_20d: float
    momentum_60d: float
    current_price: float
    target_price: float = 0.0
    stop_price: float = 0.0
    priority: int = 0


@dataclass
class Position:
    """持仓记录"""
    symbol: str
    name: str
    shares: int
    cost: float
    entry_date: str
    highest_price: float
    current_price: float
    pnl_pct: float
    status: str  # OPEN/CLOSED


# ============================================================
# 信号生成器
# ============================================================

class TenbaggerSignalGenerator:
    """十倍股信号生成器"""
    
    def __init__(self, config: SignalConfig = None):
        self.config = config or SignalConfig()
        self.db_path = PROJECT_ROOT / "data" / "tenbagger_signals.db"
        self._init_db()
        self.jq_authenticated = False
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                symbol TEXT,
                name TEXT,
                action TEXT,
                reason TEXT,
                score REAL,
                momentum_20d REAL,
                momentum_60d REAL,
                current_price REAL,
                target_price REAL,
                stop_price REAL,
                created_at TEXT
            )
        ''')
        
        # 持仓表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                shares INTEGER,
                cost REAL,
                entry_date TEXT,
                highest_price REAL,
                current_price REAL,
                pnl_pct REAL,
                status TEXT,
                exit_date TEXT,
                exit_reason TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth("13327806797", pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_stock_pool(self) -> List[str]:
        """获取股票池"""
        stocks = []
        
        # 创业板
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        # 中证500
        stocks += jq.get_index_stocks('000905.XSHG')[:30]
        # 科创50
        try:
            kc50 = jq.get_index_stocks('000688.XSHG')
            if kc50:
                stocks += kc50[:20]
        except:
            pass
        
        return list(set(stocks))[:self.config.max_pool_size]
    
    def compute_momentum_score(self, df: pd.DataFrame) -> Dict:
        """计算动量得分"""
        if len(df) < self.config.momentum_period:
            return None
        
        close = df['close'].values
        volume = df['volume'].values
        
        # 动量
        m5 = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
        m20 = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
        m60 = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
        
        # 量比
        vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
        
        # 价格位置
        ma20 = np.mean(close[-20:])
        price_to_ma20 = (close[-1] / ma20 - 1) * 100 if ma20 > 0 else 0
        
        # 综合得分
        score = (
            m20 * 0.4 +
            m60 * 0.2 +
            (vol_ratio - 1) * 20 +
            (20 if price_to_ma20 > 0 else 0)
        )
        
        return {
            'momentum_5d': m5,
            'momentum_20d': m20,
            'momentum_60d': m60,
            'vol_ratio': vol_ratio,
            'price_to_ma20': price_to_ma20,
            'score': score,
            'current_price': close[-1]
        }
    
    def generate_buy_signals(self, date: str = None) -> List[Signal]:
        """生成买入信号"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 扫描买入信号 ({date})...")
        
        # 获取股票池
        stocks = self.get_stock_pool()
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 获取历史数据
        start_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=date,
            frequency='daily',
            fields=['close', 'volume', 'high', 'low'],
            panel=False,
            skip_paused=True
        )
        
        # 计算得分
        candidates = []
        for stock in stocks:
            try:
                sdf = price_df[price_df['code'] == stock].copy()
                if sdf.empty or len(sdf) < 60:
                    continue
                
                result = self.compute_momentum_score(sdf)
                if result is None:
                    continue
                
                # 筛选条件
                if result['momentum_20d'] >= self.config.min_momentum:
                    # 获取名称
                    info = jq.get_security_info(stock)
                    name = info.display_name if info else stock
                    
                    candidates.append({
                        'symbol': stock,
                        'name': name,
                        **result
                    })
            except Exception as e:
                continue
        
        # 排序并选择Top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:self.config.max_holdings]
        
        # 生成信号
        signals = []
        for c in top_candidates:
            signal = Signal(
                date=date,
                symbol=c['symbol'],
                name=c['name'],
                action='BUY',
                reason=f"动量{c['momentum_20d']:.1f}%，得分{c['score']:.1f}",
                score=c['score'],
                momentum_20d=c['momentum_20d'],
                momentum_60d=c['momentum_60d'],
                current_price=c['current_price'],
                target_price=c['current_price'] * (1 + self.config.take_profit),
                stop_price=c['current_price'] * (1 + self.config.stop_loss),
                priority=len(signals)
            )
            signals.append(signal)
        
        logger.info(f"✅ 生成 {len(signals)} 个买入信号")
        
        # 保存到数据库
        self._save_signals(signals)
        
        return signals
    
    def generate_sell_signals(self, positions: List[Position]) -> List[Signal]:
        """生成卖出信号"""
        if not self.authenticate_jqdata():
            return []
        
        signals = []
        date = datetime.now().strftime('%Y-%m-%d')
        
        for pos in positions:
            if pos.status != 'OPEN':
                continue
            
            # 获取最新价格
            try:
                df = jq.get_price(pos.symbol, end_date=date, count=1, fields=['close'])
                if df.empty:
                    continue
                
                current_price = df['close'].iloc[0]
                pnl = (current_price - pos.cost) / pos.cost
                drawdown = (current_price - pos.highest_price) / pos.highest_price if pos.highest_price > 0 else 0
                
                reason = None
                
                # 止损
                if pnl <= self.config.stop_loss:
                    reason = f'止损 {pnl*100:.1f}%'
                # 止盈
                elif pnl >= self.config.take_profit:
                    reason = f'止盈 {pnl*100:.1f}%'
                # 移动止损
                elif drawdown <= -self.config.trailing_stop and pnl > 0.1:
                    reason = f'移动止损 {drawdown*100:.1f}%'
                
                if reason:
                    signal = Signal(
                        date=date,
                        symbol=pos.symbol,
                        name=pos.name,
                        action='SELL',
                        reason=reason,
                        score=0,
                        momentum_20d=0,
                        momentum_60d=0,
                        current_price=current_price,
                        priority=0
                    )
                    signals.append(signal)
                    
            except Exception as e:
                logger.warning(f"检查{pos.symbol}失败: {e}")
        
        return signals
    
    def _save_signals(self, signals: List[Signal]):
        """保存信号到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for s in signals:
            cursor.execute('''
                INSERT INTO signals (date, symbol, name, action, reason, score, 
                                    momentum_20d, momentum_60d, current_price, 
                                    target_price, stop_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s.date, s.symbol, s.name, s.action, s.reason, s.score,
                  s.momentum_20d, s.momentum_60d, s.current_price,
                  s.target_price, s.stop_price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_latest_signals(self, n: int = 10) -> List[Dict]:
        """获取最新信号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals ORDER BY created_at DESC LIMIT ?
        ''', (n,))
        
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def validate_out_of_sample(self, train_end: str, test_start: str, test_end: str) -> Dict:
        """样本外验证"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': '认证失败'}
        
        logger.info(f"🔬 样本外验证: 训练截止{train_end}, 测试{test_start}~{test_end}")
        
        # 获取数据
        stocks = self.get_stock_pool()
        
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(test_start, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
            end_date=test_end,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        # 简化回测
        close_df = price_df.pivot(index='time', columns='code', values='close')
        momentum = close_df.pct_change(self.config.momentum_period)
        
        dates = close_df.index
        test_dates = [d for d in dates if str(d.date()) >= test_start]
        
        initial_capital = 1000000
        cash = initial_capital
        positions = {}
        equity_curve = []
        
        rebalance_days = 3
        counter = 0
        
        for date in test_dates:
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            # 调仓
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                mom_today = momentum.loc[date].dropna()
                if len(mom_today) > 0:
                    top_stocks = mom_today.nlargest(self.config.max_holdings).index.tolist()
                    
                    # 卖出
                    for stock in list(positions.keys()):
                        if stock not in top_stocks:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price):
                                cash += positions[stock]['shares'] * price * 0.999
                                del positions[stock]
                    
                    # 买入
                    for stock in top_stocks:
                        if stock not in positions:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price) and price > 0:
                                buy_value = min(portfolio_value / self.config.max_holdings, cash * 0.9)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0 and shares * price <= cash:
                                    cash -= shares * price * 1.001
                                    positions[stock] = {'shares': shares, 'cost': price}
            
            # 记录
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        
        returns = equity.pct_change().fillna(0)
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 验证完成:")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化: {annual_return*100:.2f}%")
        logger.info(f"   夏普: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'train_period': f'~{train_end}',
            'test_period': f'{test_start}~{test_end}',
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'max_drawdown': max_dd,
                'volatility': volatility
            }
        }
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成信号
        buy_signals = self.generate_buy_signals(date)
        
        # 获取历史信号
        history = self.get_latest_signals(20)
        
        # 生成HTML
        signals_html = ""
        for s in buy_signals:
            signals_html += f"""
            <div class="signal-card">
                <h3>{s.name} ({s.symbol})</h3>
                <p>📈 动量20d: {s.momentum_20d:.1f}% | 动量60d: {s.momentum_60d:.1f}%</p>
                <p>💰 当前价: ¥{s.current_price:.2f}</p>
                <p>🎯 目标价: ¥{s.target_price:.2f} (+{self.config.take_profit*100:.0f}%)</p>
                <p>🛑 止损价: ¥{s.stop_price:.2f} ({self.config.stop_loss*100:.0f}%)</p>
                <p>📊 得分: {s.score:.1f}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股每日信号报告 - {date}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: #1a1a2e; }}
        .signals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .signal-card {{ background: rgba(255,255,255,0.08); padding: 25px; border-radius: 16px; border-left: 4px solid #ff6b6b; }}
        .signal-card h3 {{ color: #ff6b6b; margin-top: 0; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 25px; }}
        .section h2 {{ color: #feca57; margin-top: 0; }}
        .config {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .config-item {{ background: rgba(255,107,107,0.2); padding: 15px; border-radius: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股每日信号</h1>
            <p>{date} | 基于动量因子选股</p>
        </div>
        
        <div class="section">
            <h2>📊 今日买入信号 ({len(buy_signals)}只)</h2>
            <div class="signals">
                {signals_html if signals_html else '<p>今日无买入信号</p>'}
            </div>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略配置</h2>
            <div class="config">
                <div class="config-item">
                    <div>持仓数量</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.max_holdings}</div>
                </div>
                <div class="config-item">
                    <div>动量周期</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.momentum_period}天</div>
                </div>
                <div class="config-item">
                    <div>止损线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.stop_loss*100:.0f}%</div>
                </div>
                <div class="config-item">
                    <div>止盈线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.take_profit*100:.0f}%</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 使用说明</h2>
            <ul>
                <li>信号基于20日动量排名生成</li>
                <li>建议集中持有2只股票</li>
                <li>严格执行止损(-8%)和止盈(+50%)</li>
                <li>每3天调仓一次</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股信号生成器")
    logger.info("=" * 80)
    
    generator = TenbaggerSignalGenerator()
    
    # 1. 生成今日信号
    logger.info("\n📊 生成今日信号...")
    signals = generator.generate_buy_signals()
    
    for s in signals:
        logger.info(f"   {s.name} ({s.symbol}): {s.reason}")
    
    # 2. 样本外验证
    logger.info("\n🔬 样本外验证...")
    validation = generator.validate_out_of_sample(
        train_end="2024-06-30",
        test_start="2024-07-01",
        test_end="2025-12-20"
    )
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generator.generate_daily_report()
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    report_path = reports_dir / f"daily_signal_{datetime.now().strftime('%Y%m%d')}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info("=" * 80)
    
    return {
        'signals': [asdict(s) for s in signals],
        'validation': validation,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()





















# -*- coding: utf-8 -*-
"""
十倍股实时信号生成器
====================

功能：
1. 每日扫描生成买入信号
2. 持仓跟踪与卖出信号
3. 样本外验证
4. 信号历史记录

使用验证有效的最优参数：
- max_holdings: 2
- momentum_period: 20
- rebalance_days: 3
- stop_loss: -8%
- take_profit: 50%

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_signal_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

@dataclass
class SignalConfig:
    """信号配置"""
    max_holdings: int = 2
    momentum_period: int = 20
    min_momentum: float = 10.0  # 最低20日涨幅%
    stop_loss: float = -0.08
    take_profit: float = 0.50
    trailing_stop: float = 0.15
    
    # 股票池配置
    stock_pool: str = "growth"  # growth/value/all
    max_pool_size: int = 100


# ============================================================
# 信号数据结构
# ============================================================

@dataclass
class Signal:
    """交易信号"""
    date: str
    symbol: str
    name: str
    action: str  # BUY/SELL/HOLD
    reason: str
    score: float
    momentum_20d: float
    momentum_60d: float
    current_price: float
    target_price: float = 0.0
    stop_price: float = 0.0
    priority: int = 0


@dataclass
class Position:
    """持仓记录"""
    symbol: str
    name: str
    shares: int
    cost: float
    entry_date: str
    highest_price: float
    current_price: float
    pnl_pct: float
    status: str  # OPEN/CLOSED


# ============================================================
# 信号生成器
# ============================================================

class TenbaggerSignalGenerator:
    """十倍股信号生成器"""
    
    def __init__(self, config: SignalConfig = None):
        self.config = config or SignalConfig()
        self.db_path = PROJECT_ROOT / "data" / "tenbagger_signals.db"
        self._init_db()
        self.jq_authenticated = False
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                symbol TEXT,
                name TEXT,
                action TEXT,
                reason TEXT,
                score REAL,
                momentum_20d REAL,
                momentum_60d REAL,
                current_price REAL,
                target_price REAL,
                stop_price REAL,
                created_at TEXT
            )
        ''')
        
        # 持仓表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                shares INTEGER,
                cost REAL,
                entry_date TEXT,
                highest_price REAL,
                current_price REAL,
                pnl_pct REAL,
                status TEXT,
                exit_date TEXT,
                exit_reason TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth("13327806797", pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_stock_pool(self) -> List[str]:
        """获取股票池"""
        stocks = []
        
        # 创业板
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        # 中证500
        stocks += jq.get_index_stocks('000905.XSHG')[:30]
        # 科创50
        try:
            kc50 = jq.get_index_stocks('000688.XSHG')
            if kc50:
                stocks += kc50[:20]
        except:
            pass
        
        return list(set(stocks))[:self.config.max_pool_size]
    
    def compute_momentum_score(self, df: pd.DataFrame) -> Dict:
        """计算动量得分"""
        if len(df) < self.config.momentum_period:
            return None
        
        close = df['close'].values
        volume = df['volume'].values
        
        # 动量
        m5 = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
        m20 = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
        m60 = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
        
        # 量比
        vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
        
        # 价格位置
        ma20 = np.mean(close[-20:])
        price_to_ma20 = (close[-1] / ma20 - 1) * 100 if ma20 > 0 else 0
        
        # 综合得分
        score = (
            m20 * 0.4 +
            m60 * 0.2 +
            (vol_ratio - 1) * 20 +
            (20 if price_to_ma20 > 0 else 0)
        )
        
        return {
            'momentum_5d': m5,
            'momentum_20d': m20,
            'momentum_60d': m60,
            'vol_ratio': vol_ratio,
            'price_to_ma20': price_to_ma20,
            'score': score,
            'current_price': close[-1]
        }
    
    def generate_buy_signals(self, date: str = None) -> List[Signal]:
        """生成买入信号"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 扫描买入信号 ({date})...")
        
        # 获取股票池
        stocks = self.get_stock_pool()
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 获取历史数据
        start_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=date,
            frequency='daily',
            fields=['close', 'volume', 'high', 'low'],
            panel=False,
            skip_paused=True
        )
        
        # 计算得分
        candidates = []
        for stock in stocks:
            try:
                sdf = price_df[price_df['code'] == stock].copy()
                if sdf.empty or len(sdf) < 60:
                    continue
                
                result = self.compute_momentum_score(sdf)
                if result is None:
                    continue
                
                # 筛选条件
                if result['momentum_20d'] >= self.config.min_momentum:
                    # 获取名称
                    info = jq.get_security_info(stock)
                    name = info.display_name if info else stock
                    
                    candidates.append({
                        'symbol': stock,
                        'name': name,
                        **result
                    })
            except Exception as e:
                continue
        
        # 排序并选择Top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:self.config.max_holdings]
        
        # 生成信号
        signals = []
        for c in top_candidates:
            signal = Signal(
                date=date,
                symbol=c['symbol'],
                name=c['name'],
                action='BUY',
                reason=f"动量{c['momentum_20d']:.1f}%，得分{c['score']:.1f}",
                score=c['score'],
                momentum_20d=c['momentum_20d'],
                momentum_60d=c['momentum_60d'],
                current_price=c['current_price'],
                target_price=c['current_price'] * (1 + self.config.take_profit),
                stop_price=c['current_price'] * (1 + self.config.stop_loss),
                priority=len(signals)
            )
            signals.append(signal)
        
        logger.info(f"✅ 生成 {len(signals)} 个买入信号")
        
        # 保存到数据库
        self._save_signals(signals)
        
        return signals
    
    def generate_sell_signals(self, positions: List[Position]) -> List[Signal]:
        """生成卖出信号"""
        if not self.authenticate_jqdata():
            return []
        
        signals = []
        date = datetime.now().strftime('%Y-%m-%d')
        
        for pos in positions:
            if pos.status != 'OPEN':
                continue
            
            # 获取最新价格
            try:
                df = jq.get_price(pos.symbol, end_date=date, count=1, fields=['close'])
                if df.empty:
                    continue
                
                current_price = df['close'].iloc[0]
                pnl = (current_price - pos.cost) / pos.cost
                drawdown = (current_price - pos.highest_price) / pos.highest_price if pos.highest_price > 0 else 0
                
                reason = None
                
                # 止损
                if pnl <= self.config.stop_loss:
                    reason = f'止损 {pnl*100:.1f}%'
                # 止盈
                elif pnl >= self.config.take_profit:
                    reason = f'止盈 {pnl*100:.1f}%'
                # 移动止损
                elif drawdown <= -self.config.trailing_stop and pnl > 0.1:
                    reason = f'移动止损 {drawdown*100:.1f}%'
                
                if reason:
                    signal = Signal(
                        date=date,
                        symbol=pos.symbol,
                        name=pos.name,
                        action='SELL',
                        reason=reason,
                        score=0,
                        momentum_20d=0,
                        momentum_60d=0,
                        current_price=current_price,
                        priority=0
                    )
                    signals.append(signal)
                    
            except Exception as e:
                logger.warning(f"检查{pos.symbol}失败: {e}")
        
        return signals
    
    def _save_signals(self, signals: List[Signal]):
        """保存信号到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for s in signals:
            cursor.execute('''
                INSERT INTO signals (date, symbol, name, action, reason, score, 
                                    momentum_20d, momentum_60d, current_price, 
                                    target_price, stop_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s.date, s.symbol, s.name, s.action, s.reason, s.score,
                  s.momentum_20d, s.momentum_60d, s.current_price,
                  s.target_price, s.stop_price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_latest_signals(self, n: int = 10) -> List[Dict]:
        """获取最新信号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals ORDER BY created_at DESC LIMIT ?
        ''', (n,))
        
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def validate_out_of_sample(self, train_end: str, test_start: str, test_end: str) -> Dict:
        """样本外验证"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': '认证失败'}
        
        logger.info(f"🔬 样本外验证: 训练截止{train_end}, 测试{test_start}~{test_end}")
        
        # 获取数据
        stocks = self.get_stock_pool()
        
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(test_start, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
            end_date=test_end,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        # 简化回测
        close_df = price_df.pivot(index='time', columns='code', values='close')
        momentum = close_df.pct_change(self.config.momentum_period)
        
        dates = close_df.index
        test_dates = [d for d in dates if str(d.date()) >= test_start]
        
        initial_capital = 1000000
        cash = initial_capital
        positions = {}
        equity_curve = []
        
        rebalance_days = 3
        counter = 0
        
        for date in test_dates:
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            # 调仓
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                mom_today = momentum.loc[date].dropna()
                if len(mom_today) > 0:
                    top_stocks = mom_today.nlargest(self.config.max_holdings).index.tolist()
                    
                    # 卖出
                    for stock in list(positions.keys()):
                        if stock not in top_stocks:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price):
                                cash += positions[stock]['shares'] * price * 0.999
                                del positions[stock]
                    
                    # 买入
                    for stock in top_stocks:
                        if stock not in positions:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price) and price > 0:
                                buy_value = min(portfolio_value / self.config.max_holdings, cash * 0.9)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0 and shares * price <= cash:
                                    cash -= shares * price * 1.001
                                    positions[stock] = {'shares': shares, 'cost': price}
            
            # 记录
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        
        returns = equity.pct_change().fillna(0)
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 验证完成:")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化: {annual_return*100:.2f}%")
        logger.info(f"   夏普: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'train_period': f'~{train_end}',
            'test_period': f'{test_start}~{test_end}',
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'max_drawdown': max_dd,
                'volatility': volatility
            }
        }
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成信号
        buy_signals = self.generate_buy_signals(date)
        
        # 获取历史信号
        history = self.get_latest_signals(20)
        
        # 生成HTML
        signals_html = ""
        for s in buy_signals:
            signals_html += f"""
            <div class="signal-card">
                <h3>{s.name} ({s.symbol})</h3>
                <p>📈 动量20d: {s.momentum_20d:.1f}% | 动量60d: {s.momentum_60d:.1f}%</p>
                <p>💰 当前价: ¥{s.current_price:.2f}</p>
                <p>🎯 目标价: ¥{s.target_price:.2f} (+{self.config.take_profit*100:.0f}%)</p>
                <p>🛑 止损价: ¥{s.stop_price:.2f} ({self.config.stop_loss*100:.0f}%)</p>
                <p>📊 得分: {s.score:.1f}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股每日信号报告 - {date}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: #1a1a2e; }}
        .signals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .signal-card {{ background: rgba(255,255,255,0.08); padding: 25px; border-radius: 16px; border-left: 4px solid #ff6b6b; }}
        .signal-card h3 {{ color: #ff6b6b; margin-top: 0; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 25px; }}
        .section h2 {{ color: #feca57; margin-top: 0; }}
        .config {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .config-item {{ background: rgba(255,107,107,0.2); padding: 15px; border-radius: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股每日信号</h1>
            <p>{date} | 基于动量因子选股</p>
        </div>
        
        <div class="section">
            <h2>📊 今日买入信号 ({len(buy_signals)}只)</h2>
            <div class="signals">
                {signals_html if signals_html else '<p>今日无买入信号</p>'}
            </div>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略配置</h2>
            <div class="config">
                <div class="config-item">
                    <div>持仓数量</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.max_holdings}</div>
                </div>
                <div class="config-item">
                    <div>动量周期</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.momentum_period}天</div>
                </div>
                <div class="config-item">
                    <div>止损线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.stop_loss*100:.0f}%</div>
                </div>
                <div class="config-item">
                    <div>止盈线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.take_profit*100:.0f}%</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 使用说明</h2>
            <ul>
                <li>信号基于20日动量排名生成</li>
                <li>建议集中持有2只股票</li>
                <li>严格执行止损(-8%)和止盈(+50%)</li>
                <li>每3天调仓一次</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股信号生成器")
    logger.info("=" * 80)
    
    generator = TenbaggerSignalGenerator()
    
    # 1. 生成今日信号
    logger.info("\n📊 生成今日信号...")
    signals = generator.generate_buy_signals()
    
    for s in signals:
        logger.info(f"   {s.name} ({s.symbol}): {s.reason}")
    
    # 2. 样本外验证
    logger.info("\n🔬 样本外验证...")
    validation = generator.validate_out_of_sample(
        train_end="2024-06-30",
        test_start="2024-07-01",
        test_end="2025-12-20"
    )
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generator.generate_daily_report()
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    report_path = reports_dir / f"daily_signal_{datetime.now().strftime('%Y%m%d')}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info("=" * 80)
    
    return {
        'signals': [asdict(s) for s in signals],
        'validation': validation,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
十倍股实时信号生成器
====================

功能：
1. 每日扫描生成买入信号
2. 持仓跟踪与卖出信号
3. 样本外验证
4. 信号历史记录

使用验证有效的最优参数：
- max_holdings: 2
- momentum_period: 20
- rebalance_days: 3
- stop_loss: -8%
- take_profit: 50%

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_signal_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq


# ============================================================
# 配置
# ============================================================

@dataclass
class SignalConfig:
    """信号配置"""
    max_holdings: int = 2
    momentum_period: int = 20
    min_momentum: float = 10.0  # 最低20日涨幅%
    stop_loss: float = -0.08
    take_profit: float = 0.50
    trailing_stop: float = 0.15
    
    # 股票池配置
    stock_pool: str = "growth"  # growth/value/all
    max_pool_size: int = 100


# ============================================================
# 信号数据结构
# ============================================================

@dataclass
class Signal:
    """交易信号"""
    date: str
    symbol: str
    name: str
    action: str  # BUY/SELL/HOLD
    reason: str
    score: float
    momentum_20d: float
    momentum_60d: float
    current_price: float
    target_price: float = 0.0
    stop_price: float = 0.0
    priority: int = 0


@dataclass
class Position:
    """持仓记录"""
    symbol: str
    name: str
    shares: int
    cost: float
    entry_date: str
    highest_price: float
    current_price: float
    pnl_pct: float
    status: str  # OPEN/CLOSED


# ============================================================
# 信号生成器
# ============================================================

class TenbaggerSignalGenerator:
    """十倍股信号生成器"""
    
    def __init__(self, config: SignalConfig = None):
        self.config = config or SignalConfig()
        self.db_path = PROJECT_ROOT / "data" / "tenbagger_signals.db"
        self._init_db()
        self.jq_authenticated = False
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 信号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                symbol TEXT,
                name TEXT,
                action TEXT,
                reason TEXT,
                score REAL,
                momentum_20d REAL,
                momentum_60d REAL,
                current_price REAL,
                target_price REAL,
                stop_price REAL,
                created_at TEXT
            )
        ''')
        
        # 持仓表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                shares INTEGER,
                cost REAL,
                entry_date TEXT,
                highest_price REAL,
                current_price REAL,
                pnl_pct REAL,
                status TEXT,
                exit_date TEXT,
                exit_reason TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth("13327806797", pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_stock_pool(self) -> List[str]:
        """获取股票池"""
        stocks = []
        
        # 创业板
        stocks += jq.get_index_stocks('399006.XSHE')[:50]
        # 中证500
        stocks += jq.get_index_stocks('000905.XSHG')[:30]
        # 科创50
        try:
            kc50 = jq.get_index_stocks('000688.XSHG')
            if kc50:
                stocks += kc50[:20]
        except:
            pass
        
        return list(set(stocks))[:self.config.max_pool_size]
    
    def compute_momentum_score(self, df: pd.DataFrame) -> Dict:
        """计算动量得分"""
        if len(df) < self.config.momentum_period:
            return None
        
        close = df['close'].values
        volume = df['volume'].values
        
        # 动量
        m5 = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
        m20 = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
        m60 = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
        
        # 量比
        vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
        
        # 价格位置
        ma20 = np.mean(close[-20:])
        price_to_ma20 = (close[-1] / ma20 - 1) * 100 if ma20 > 0 else 0
        
        # 综合得分
        score = (
            m20 * 0.4 +
            m60 * 0.2 +
            (vol_ratio - 1) * 20 +
            (20 if price_to_ma20 > 0 else 0)
        )
        
        return {
            'momentum_5d': m5,
            'momentum_20d': m20,
            'momentum_60d': m60,
            'vol_ratio': vol_ratio,
            'price_to_ma20': price_to_ma20,
            'score': score,
            'current_price': close[-1]
        }
    
    def generate_buy_signals(self, date: str = None) -> List[Signal]:
        """生成买入信号"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 扫描买入信号 ({date})...")
        
        # 获取股票池
        stocks = self.get_stock_pool()
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 获取历史数据
        start_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=date,
            frequency='daily',
            fields=['close', 'volume', 'high', 'low'],
            panel=False,
            skip_paused=True
        )
        
        # 计算得分
        candidates = []
        for stock in stocks:
            try:
                sdf = price_df[price_df['code'] == stock].copy()
                if sdf.empty or len(sdf) < 60:
                    continue
                
                result = self.compute_momentum_score(sdf)
                if result is None:
                    continue
                
                # 筛选条件
                if result['momentum_20d'] >= self.config.min_momentum:
                    # 获取名称
                    info = jq.get_security_info(stock)
                    name = info.display_name if info else stock
                    
                    candidates.append({
                        'symbol': stock,
                        'name': name,
                        **result
                    })
            except Exception as e:
                continue
        
        # 排序并选择Top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:self.config.max_holdings]
        
        # 生成信号
        signals = []
        for c in top_candidates:
            signal = Signal(
                date=date,
                symbol=c['symbol'],
                name=c['name'],
                action='BUY',
                reason=f"动量{c['momentum_20d']:.1f}%，得分{c['score']:.1f}",
                score=c['score'],
                momentum_20d=c['momentum_20d'],
                momentum_60d=c['momentum_60d'],
                current_price=c['current_price'],
                target_price=c['current_price'] * (1 + self.config.take_profit),
                stop_price=c['current_price'] * (1 + self.config.stop_loss),
                priority=len(signals)
            )
            signals.append(signal)
        
        logger.info(f"✅ 生成 {len(signals)} 个买入信号")
        
        # 保存到数据库
        self._save_signals(signals)
        
        return signals
    
    def generate_sell_signals(self, positions: List[Position]) -> List[Signal]:
        """生成卖出信号"""
        if not self.authenticate_jqdata():
            return []
        
        signals = []
        date = datetime.now().strftime('%Y-%m-%d')
        
        for pos in positions:
            if pos.status != 'OPEN':
                continue
            
            # 获取最新价格
            try:
                df = jq.get_price(pos.symbol, end_date=date, count=1, fields=['close'])
                if df.empty:
                    continue
                
                current_price = df['close'].iloc[0]
                pnl = (current_price - pos.cost) / pos.cost
                drawdown = (current_price - pos.highest_price) / pos.highest_price if pos.highest_price > 0 else 0
                
                reason = None
                
                # 止损
                if pnl <= self.config.stop_loss:
                    reason = f'止损 {pnl*100:.1f}%'
                # 止盈
                elif pnl >= self.config.take_profit:
                    reason = f'止盈 {pnl*100:.1f}%'
                # 移动止损
                elif drawdown <= -self.config.trailing_stop and pnl > 0.1:
                    reason = f'移动止损 {drawdown*100:.1f}%'
                
                if reason:
                    signal = Signal(
                        date=date,
                        symbol=pos.symbol,
                        name=pos.name,
                        action='SELL',
                        reason=reason,
                        score=0,
                        momentum_20d=0,
                        momentum_60d=0,
                        current_price=current_price,
                        priority=0
                    )
                    signals.append(signal)
                    
            except Exception as e:
                logger.warning(f"检查{pos.symbol}失败: {e}")
        
        return signals
    
    def _save_signals(self, signals: List[Signal]):
        """保存信号到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for s in signals:
            cursor.execute('''
                INSERT INTO signals (date, symbol, name, action, reason, score, 
                                    momentum_20d, momentum_60d, current_price, 
                                    target_price, stop_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (s.date, s.symbol, s.name, s.action, s.reason, s.score,
                  s.momentum_20d, s.momentum_60d, s.current_price,
                  s.target_price, s.stop_price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_latest_signals(self, n: int = 10) -> List[Dict]:
        """获取最新信号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals ORDER BY created_at DESC LIMIT ?
        ''', (n,))
        
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def validate_out_of_sample(self, train_end: str, test_start: str, test_end: str) -> Dict:
        """样本外验证"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': '认证失败'}
        
        logger.info(f"🔬 样本外验证: 训练截止{train_end}, 测试{test_start}~{test_end}")
        
        # 获取数据
        stocks = self.get_stock_pool()
        
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(test_start, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
            end_date=test_end,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        # 简化回测
        close_df = price_df.pivot(index='time', columns='code', values='close')
        momentum = close_df.pct_change(self.config.momentum_period)
        
        dates = close_df.index
        test_dates = [d for d in dates if str(d.date()) >= test_start]
        
        initial_capital = 1000000
        cash = initial_capital
        positions = {}
        equity_curve = []
        
        rebalance_days = 3
        counter = 0
        
        for date in test_dates:
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            # 调仓
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                mom_today = momentum.loc[date].dropna()
                if len(mom_today) > 0:
                    top_stocks = mom_today.nlargest(self.config.max_holdings).index.tolist()
                    
                    # 卖出
                    for stock in list(positions.keys()):
                        if stock not in top_stocks:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price):
                                cash += positions[stock]['shares'] * price * 0.999
                                del positions[stock]
                    
                    # 买入
                    for stock in top_stocks:
                        if stock not in positions:
                            price = close_df.loc[date, stock]
                            if not pd.isna(price) and price > 0:
                                buy_value = min(portfolio_value / self.config.max_holdings, cash * 0.9)
                                shares = int(buy_value / price / 100) * 100
                                if shares > 0 and shares * price <= cash:
                                    cash -= shares * price * 1.001
                                    positions[stock] = {'shares': shares, 'cost': price}
            
            # 记录
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in close_df.columns:
                    price = close_df.loc[date, stock]
                    if not pd.isna(price):
                        portfolio_value += pos['shares'] * price
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        
        returns = equity.pct_change().fillna(0)
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        logger.info(f"✅ 验证完成:")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化: {annual_return*100:.2f}%")
        logger.info(f"   夏普: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'train_period': f'~{train_end}',
            'test_period': f'{test_start}~{test_end}',
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'max_drawdown': max_dd,
                'volatility': volatility
            }
        }
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成信号
        buy_signals = self.generate_buy_signals(date)
        
        # 获取历史信号
        history = self.get_latest_signals(20)
        
        # 生成HTML
        signals_html = ""
        for s in buy_signals:
            signals_html += f"""
            <div class="signal-card">
                <h3>{s.name} ({s.symbol})</h3>
                <p>📈 动量20d: {s.momentum_20d:.1f}% | 动量60d: {s.momentum_60d:.1f}%</p>
                <p>💰 当前价: ¥{s.current_price:.2f}</p>
                <p>🎯 目标价: ¥{s.target_price:.2f} (+{self.config.take_profit*100:.0f}%)</p>
                <p>🛑 止损价: ¥{s.stop_price:.2f} ({self.config.stop_loss*100:.0f}%)</p>
                <p>📊 得分: {s.score:.1f}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股每日信号报告 - {date}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: #1a1a2e; }}
        .signals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .signal-card {{ background: rgba(255,255,255,0.08); padding: 25px; border-radius: 16px; border-left: 4px solid #ff6b6b; }}
        .signal-card h3 {{ color: #ff6b6b; margin-top: 0; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; margin-bottom: 25px; }}
        .section h2 {{ color: #feca57; margin-top: 0; }}
        .config {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .config-item {{ background: rgba(255,107,107,0.2); padding: 15px; border-radius: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股每日信号</h1>
            <p>{date} | 基于动量因子选股</p>
        </div>
        
        <div class="section">
            <h2>📊 今日买入信号 ({len(buy_signals)}只)</h2>
            <div class="signals">
                {signals_html if signals_html else '<p>今日无买入信号</p>'}
            </div>
        </div>
        
        <div class="section">
            <h2>⚙️ 策略配置</h2>
            <div class="config">
                <div class="config-item">
                    <div>持仓数量</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.max_holdings}</div>
                </div>
                <div class="config-item">
                    <div>动量周期</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.momentum_period}天</div>
                </div>
                <div class="config-item">
                    <div>止损线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.stop_loss*100:.0f}%</div>
                </div>
                <div class="config-item">
                    <div>止盈线</div>
                    <div style="font-size:1.5em;font-weight:bold">{self.config.take_profit*100:.0f}%</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 使用说明</h2>
            <ul>
                <li>信号基于20日动量排名生成</li>
                <li>建议集中持有2只股票</li>
                <li>严格执行止损(-8%)和止盈(+50%)</li>
                <li>每3天调仓一次</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股信号生成器")
    logger.info("=" * 80)
    
    generator = TenbaggerSignalGenerator()
    
    # 1. 生成今日信号
    logger.info("\n📊 生成今日信号...")
    signals = generator.generate_buy_signals()
    
    for s in signals:
        logger.info(f"   {s.name} ({s.symbol}): {s.reason}")
    
    # 2. 样本外验证
    logger.info("\n🔬 样本外验证...")
    validation = generator.validate_out_of_sample(
        train_end="2024-06-30",
        test_start="2024-07-01",
        test_end="2025-12-20"
    )
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generator.generate_daily_report()
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    report_path = reports_dir / f"daily_signal_{datetime.now().strftime('%Y%m%d')}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info("=" * 80)
    
    return {
        'signals': [asdict(s) for s in signals],
        'validation': validation,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()








































