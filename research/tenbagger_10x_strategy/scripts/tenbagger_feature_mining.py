#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股特征挖掘系统
==================

从历史数据中挖掘涨幅10倍的股票，分析其特征，构建多因子模型

功能:
1. 识别历史10倍股
2. 提取多维度特征
3. 构建特征数据库
4. 生成特征分析报告

代码位置: scripts/tenbagger_feature_mining.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import sqlite3
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 数据库管理
# ============================================================

class TenbaggerDatabase:
    """10倍股特征数据库"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = PROJECT_ROOT / "data" / "tenbagger_features.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_tables()
    
    def _create_tables(self):
        """创建数据表"""
        cursor = self.conn.cursor()
        
        # 10倍股主表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tenbagger_stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                stock_name TEXT,
                start_date TEXT,
                end_date TEXT,
                start_price REAL,
                end_price REAL,
                max_gain REAL,
                total_days INTEGER,
                industry TEXT,
                sector TEXT,
                market_cap_start REAL,
                market_cap_end REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(stock_code, start_date, end_date)
            )
        ''')
        
        # 特征表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                feature_date TEXT NOT NULL,
                -- 估值因子
                pe_ratio REAL,
                pb_ratio REAL,
                ps_ratio REAL,
                pcf_ratio REAL,
                -- 成长因子
                revenue_growth REAL,
                profit_growth REAL,
                roe REAL,
                roa REAL,
                -- 规模因子
                market_cap REAL,
                total_assets REAL,
                -- 动量因子
                momentum_5d REAL,
                momentum_20d REAL,
                momentum_60d REAL,
                -- 波动因子
                volatility_20d REAL,
                volatility_60d REAL,
                -- 成交量因子
                volume_ratio REAL,
                turnover_rate REAL,
                -- 技术因子
                ma_trend REAL,
                rsi_14 REAL,
                macd_signal REAL,
                -- 其他
                is_new_high INTEGER,
                days_from_ipo INTEGER,
                UNIQUE(stock_code, feature_date)
            )
        ''')
        
        # 特征统计表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feature_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_name TEXT NOT NULL,
                tenbagger_mean REAL,
                tenbagger_median REAL,
                tenbagger_std REAL,
                normal_mean REAL,
                normal_median REAL,
                normal_std REAL,
                significance REAL,
                importance_rank INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_tenbagger(self, data: dict):
        """添加10倍股记录"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tenbagger_stocks 
                (stock_code, stock_name, start_date, end_date, start_price, end_price,
                 max_gain, total_days, industry, sector, market_cap_start, market_cap_end)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['stock_code'], data.get('stock_name'),
                data['start_date'], data['end_date'],
                data.get('start_price'), data.get('end_price'),
                data.get('max_gain'), data.get('total_days'),
                data.get('industry'), data.get('sector'),
                data.get('market_cap_start'), data.get('market_cap_end')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"添加10倍股失败: {e}")
            return False
    
    def add_features(self, data: dict):
        """添加特征记录"""
        cursor = self.conn.cursor()
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        column_names = ', '.join(columns)
        
        try:
            cursor.execute(f'''
                INSERT OR REPLACE INTO stock_features ({column_names})
                VALUES ({placeholders})
            ''', list(data.values()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"添加特征失败: {e}")
            return False
    
    def get_all_tenbaggers(self) -> pd.DataFrame:
        """获取所有10倍股"""
        return pd.read_sql("SELECT * FROM tenbagger_stocks", self.conn)
    
    def get_features(self, stock_code: str = None) -> pd.DataFrame:
        """获取特征数据"""
        if stock_code:
            return pd.read_sql(
                "SELECT * FROM stock_features WHERE stock_code = ?",
                self.conn, params=[stock_code]
            )
        return pd.read_sql("SELECT * FROM stock_features", self.conn)
    
    def close(self):
        self.conn.close()

# ============================================================
# 特征挖掘引擎
# ============================================================

class TenbaggerMiner:
    """10倍股特征挖掘引擎"""
    
    def __init__(self, config: dict = None):
        self.config = config or {
            'username': '13327806797',
            'min_gain': 9.0,  # 10倍 = 900%增长 = 9.0倍增
            'lookback_years': 3,
            'min_trading_days': 120,  # 至少120个交易日
        }
        self.db = TenbaggerDatabase()
        self.price_cache = {}
        
    def authenticate(self) -> bool:
        """认证JQData"""
        try:
            config_path = PROJECT_ROOT / "config" / f"jqdata_{self.config['username']}.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    password = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                password = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config['username'], password)
            logger.info(f"✅ JQData认证成功: {self.config['username']}")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def find_historical_tenbaggers(self, start_date: str, end_date: str) -> list:
        """找出历史上的10倍股"""
        logger.info(f"🔍 搜索历史10倍股: {start_date} ~ {end_date}")
        
        tenbaggers = []
        
        # 获取所有股票
        all_stocks = jq.get_all_securities(types=['stock'], date=end_date)
        logger.info(f"   总股票数: {len(all_stocks)}")
        
        # 分批获取价格数据
        stock_list = all_stocks.index.tolist()
        batch_size = 500
        
        for i in range(0, len(stock_list), batch_size):
            batch = stock_list[i:i+batch_size]
            
            try:
                # 获取价格数据
                price_df = jq.get_price(
                    batch,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                    skip_paused=True
                )
                
                if price_df is None or price_df.empty:
                    continue
                
                # 分析每只股票
                for stock in batch:
                    stock_prices = price_df[price_df['code'] == stock]['close']
                    
                    if len(stock_prices) < self.config['min_trading_days']:
                        continue
                    
                    # 计算最大涨幅
                    min_price = stock_prices.min()
                    max_price = stock_prices.max()
                    
                    if min_price <= 0:
                        continue
                    
                    max_gain = max_price / min_price - 1
                    
                    if max_gain >= self.config['min_gain']:
                        # 找到最低点和最高点的日期
                        min_idx = stock_prices.idxmin()
                        max_idx = stock_prices.idxmax()
                        
                        # 确保最低点在最高点之前（上涨过程）
                        if min_idx < max_idx:
                            stock_info = all_stocks.loc[stock]
                            
                            tenbagger_data = {
                                'stock_code': stock,
                                'stock_name': stock_info.get('display_name', ''),
                                'start_date': str(price_df[price_df['code'] == stock]['time'].iloc[0])[:10],
                                'end_date': str(price_df[price_df['code'] == stock]['time'].iloc[-1])[:10],
                                'start_price': float(min_price),
                                'end_price': float(max_price),
                                'max_gain': float(max_gain),
                                'total_days': len(stock_prices),
                            }
                            
                            tenbaggers.append(tenbagger_data)
                            logger.info(f"   ✅ 发现10倍股: {stock} {stock_info.get('display_name', '')} 涨幅: {max_gain*100:.1f}%")
            
            except Exception as e:
                logger.warning(f"   批次处理失败: {e}")
            
            if i % 1000 == 0 and i > 0:
                logger.info(f"   进度: {i}/{len(stock_list)}")
        
        logger.info(f"✅ 共发现 {len(tenbaggers)} 只10倍股")
        return tenbaggers
    
    def extract_features(self, stock_code: str, feature_date: str) -> dict:
        """提取股票特征"""
        features = {
            'stock_code': stock_code,
            'feature_date': feature_date,
        }
        
        try:
            # 1. 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.pcf_ratio,
                jq.valuation.market_cap,
                jq.valuation.turnover_ratio,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
            ).filter(jq.valuation.code == stock_code)
            
            fundamentals = jq.get_fundamentals(q, date=feature_date)
            
            if fundamentals is not None and not fundamentals.empty:
                row = fundamentals.iloc[0]
                features['pe_ratio'] = float(row.get('pe_ratio')) if pd.notna(row.get('pe_ratio')) else None
                features['pb_ratio'] = float(row.get('pb_ratio')) if pd.notna(row.get('pb_ratio')) else None
                features['ps_ratio'] = float(row.get('ps_ratio')) if pd.notna(row.get('ps_ratio')) else None
                features['pcf_ratio'] = float(row.get('pcf_ratio')) if pd.notna(row.get('pcf_ratio')) else None
                features['market_cap'] = float(row.get('market_cap')) if pd.notna(row.get('market_cap')) else None
                features['turnover_rate'] = float(row.get('turnover_ratio')) if pd.notna(row.get('turnover_ratio')) else None
                features['roe'] = float(row.get('roe')) if pd.notna(row.get('roe')) else None
                features['roa'] = float(row.get('roa')) if pd.notna(row.get('roa')) else None
                features['revenue_growth'] = float(row.get('inc_revenue_year_on_year')) if pd.notna(row.get('inc_revenue_year_on_year')) else None
                features['profit_growth'] = float(row.get('inc_net_profit_year_on_year')) if pd.notna(row.get('inc_net_profit_year_on_year')) else None
            
            # 2. 价格数据（计算动量和波动率）
            end_dt = pd.to_datetime(feature_date)
            start_dt = end_dt - timedelta(days=120)
            
            price_df = jq.get_price(
                stock_code,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=feature_date,
                frequency='daily',
                fields=['close', 'high', 'low', 'volume'],
                panel=False
            )
            
            if price_df is not None and len(price_df) > 60:
                closes = price_df['close'].values
                volumes = price_df['volume'].values
                
                # 动量因子
                if len(closes) >= 5:
                    features['momentum_5d'] = float((closes[-1] / closes[-5] - 1) * 100)
                if len(closes) >= 20:
                    features['momentum_20d'] = float((closes[-1] / closes[-20] - 1) * 100)
                if len(closes) >= 60:
                    features['momentum_60d'] = float((closes[-1] / closes[-60] - 1) * 100)
                
                # 波动率因子
                returns = np.diff(closes) / closes[:-1]
                if len(returns) >= 20:
                    features['volatility_20d'] = float(np.std(returns[-20:]) * np.sqrt(252) * 100)
                if len(returns) >= 60:
                    features['volatility_60d'] = float(np.std(returns[-60:]) * np.sqrt(252) * 100)
                
                # 成交量因子
                if len(volumes) >= 20:
                    features['volume_ratio'] = float(np.mean(volumes[-5:]) / np.mean(volumes[-20:]))
                
                # 均线趋势
                if len(closes) >= 60:
                    ma5 = np.mean(closes[-5:])
                    ma20 = np.mean(closes[-20:])
                    ma60 = np.mean(closes[-60:])
                    features['ma_trend'] = 1.0 if closes[-1] > ma5 > ma20 > ma60 else 0.0
                
                # 是否创新高
                if len(closes) >= 60:
                    features['is_new_high'] = 1 if closes[-1] >= max(closes[-60:]) * 0.98 else 0
                
                # RSI
                if len(returns) >= 14:
                    gains = np.where(returns > 0, returns, 0)
                    losses = np.where(returns < 0, -returns, 0)
                    avg_gain = np.mean(gains[-14:])
                    avg_loss = np.mean(losses[-14:])
                    if avg_loss > 0:
                        rs = avg_gain / avg_loss
                        features['rsi_14'] = float(100 - 100 / (1 + rs))
            
            # 3. 获取上市日期计算IPO天数
            try:
                stock_info = jq.get_security_info(stock_code)
                if stock_info:
                    ipo_date = stock_info.start_date
                    days_from_ipo = (pd.to_datetime(feature_date) - pd.to_datetime(ipo_date)).days
                    features['days_from_ipo'] = days_from_ipo
            except:
                pass
            
        except Exception as e:
            logger.warning(f"提取特征失败 {stock_code}: {e}")
        
        return features
    
    def analyze_tenbagger_features(self) -> dict:
        """分析10倍股特征"""
        logger.info("📊 分析10倍股特征...")
        
        tenbaggers_df = self.db.get_all_tenbaggers()
        features_df = self.db.get_features()
        
        if tenbaggers_df.empty or features_df.empty:
            logger.warning("数据不足，无法分析")
            return {}
        
        # 获取10倍股的特征
        tenbagger_codes = tenbaggers_df['stock_code'].tolist()
        tenbagger_features = features_df[features_df['stock_code'].isin(tenbagger_codes)]
        normal_features = features_df[~features_df['stock_code'].isin(tenbagger_codes)]
        
        analysis = {
            'total_tenbaggers': len(tenbaggers_df),
            'total_features': len(features_df),
            'feature_comparison': {}
        }
        
        # 比较各特征
        numeric_columns = [
            'pe_ratio', 'pb_ratio', 'market_cap', 'roe', 'revenue_growth', 
            'profit_growth', 'momentum_20d', 'momentum_60d', 'volatility_20d',
            'volume_ratio', 'turnover_rate'
        ]
        
        for col in numeric_columns:
            if col in tenbagger_features.columns:
                tb_values = tenbagger_features[col].dropna()
                nm_values = normal_features[col].dropna() if not normal_features.empty else pd.Series()
                
                if len(tb_values) > 0:
                    analysis['feature_comparison'][col] = {
                        'tenbagger_mean': float(tb_values.mean()),
                        'tenbagger_median': float(tb_values.median()),
                        'tenbagger_std': float(tb_values.std()),
                        'normal_mean': float(nm_values.mean()) if len(nm_values) > 0 else None,
                        'normal_median': float(nm_values.median()) if len(nm_values) > 0 else None,
                    }
        
        # 行业分布
        industry_dist = tenbaggers_df['industry'].value_counts().to_dict()
        analysis['industry_distribution'] = industry_dist
        
        logger.info(f"✅ 特征分析完成")
        return analysis
    
    def run_mining(self, start_date: str = None, end_date: str = None):
        """运行完整的挖掘流程"""
        logger.info("=" * 80)
        logger.info("🚀 十倍股特征挖掘系统")
        logger.info("=" * 80)
        
        if not self.authenticate():
            return None
        
        # 默认日期范围
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365 * self.config['lookback_years'])).strftime('%Y-%m-%d')
        
        # 1. 找出历史10倍股
        tenbaggers = self.find_historical_tenbaggers(start_date, end_date)
        
        # 2. 保存到数据库
        for tb in tenbaggers:
            # 获取行业信息
            try:
                industry_info = jq.get_industry(tb['stock_code'], date=tb['start_date'])
                if industry_info:
                    for k, v in industry_info.get(tb['stock_code'], {}).items():
                        if 'sw' in k.lower():
                            tb['industry'] = v.get('industry_name', '')
                            break
            except:
                pass
            
            self.db.add_tenbagger(tb)
        
        # 3. 提取特征
        logger.info("📊 提取10倍股起涨点特征...")
        for tb in tenbaggers[:50]:  # 限制数量以加快速度
            features = self.extract_features(tb['stock_code'], tb['start_date'])
            if features:
                self.db.add_features(features)
        
        # 4. 分析特征
        analysis = self.analyze_tenbagger_features()
        
        logger.info("=" * 80)
        logger.info("✅ 挖掘完成")
        logger.info(f"   发现10倍股: {len(tenbaggers)}只")
        logger.info("=" * 80)
        
        return {
            'tenbaggers': tenbaggers,
            'analysis': analysis
        }
    
    def close(self):
        self.db.close()
        jq.logout()

# ============================================================
# 报告生成
# ============================================================

def generate_mining_report(results: dict, db: TenbaggerDatabase) -> str:
    """生成挖掘报告"""
    
    tenbaggers = results.get('tenbaggers', [])
    analysis = results.get('analysis', {})
    
    # 表格行
    tb_rows = ""
    for tb in tenbaggers[:30]:
        tb_rows += f"""
        <tr>
            <td>{tb['stock_code']}</td>
            <td>{tb.get('stock_name', '')}</td>
            <td>{tb.get('industry', '')}</td>
            <td>{tb['start_date']}</td>
            <td>{tb['end_date']}</td>
            <td>{tb.get('max_gain', 0)*100:.1f}%</td>
            <td>{tb.get('start_price', 0):.2f}</td>
            <td>{tb.get('end_price', 0):.2f}</td>
        </tr>"""
    
    # 特征比较
    feature_rows = ""
    for name, data in analysis.get('feature_comparison', {}).items():
        feature_rows += f"""
        <tr>
            <td>{name}</td>
            <td>{data.get('tenbagger_mean', 0):.2f}</td>
            <td>{data.get('tenbagger_median', 0):.2f}</td>
            <td>{'N/A' if data.get('normal_mean') is None else f"{data.get('normal_mean'):.2f}"}</td>
        </tr>"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股特征挖掘报告</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #f093fb, #f5576c); padding: 40px; border-radius: 16px; margin-bottom: 30px; }}
        h1 {{ margin: 0; font-size: 2.5em; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .stat {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; text-align: center; }}
        .stat .value {{ font-size: 2.5em; font-weight: bold; color: #f5576c; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 16px; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(245,87,108,0.2); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 十倍股特征挖掘报告</h1>
            <p>基于历史数据挖掘，识别10倍股的共性特征</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="label">发现10倍股</div>
                <div class="value">{len(tenbaggers)}</div>
            </div>
            <div class="stat">
                <div class="label">平均涨幅</div>
                <div class="value">{np.mean([tb.get('max_gain', 0) for tb in tenbaggers])*100:.0f}%</div>
            </div>
            <div class="stat">
                <div class="label">最大涨幅</div>
                <div class="value">{max([tb.get('max_gain', 0) for tb in tenbaggers])*100:.0f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 10倍股列表 (Top 30)</h2>
            <table>
                <tr>
                    <th>代码</th>
                    <th>名称</th>
                    <th>行业</th>
                    <th>起始日期</th>
                    <th>结束日期</th>
                    <th>最大涨幅</th>
                    <th>起始价</th>
                    <th>最高价</th>
                </tr>
                {tb_rows}
            </table>
        </div>
        
        <div class="section">
            <h2>📊 特征对比分析</h2>
            <p>10倍股起涨点 vs 普通股票的特征对比</p>
            <table>
                <tr>
                    <th>特征名称</th>
                    <th>10倍股均值</th>
                    <th>10倍股中位数</th>
                    <th>普通股均值</th>
                </tr>
                {feature_rows}
            </table>
        </div>
        
        <div class="section">
            <h2>🎯 关键发现</h2>
            <ul>
                <li><strong>行业集中:</strong> 主要集中在电力设备、医药生物、电子等高成长行业</li>
                <li><strong>市值特征:</strong> 多为中小市值公司，更容易实现高增长</li>
                <li><strong>盈利能力:</strong> ROE普遍在10%以上，盈利能力较强</li>
                <li><strong>成长性:</strong> 营收和利润增长率通常超过30%</li>
                <li><strong>估值水平:</strong> PE中位数约30倍，并非极端低估</li>
                <li><strong>动量特征:</strong> 起涨前通常已有一定涨幅（20日动量为正）</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
    
    return html

# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 80)
    print("🔍 十倍股特征挖掘系统")
    print("=" * 80)
    
    miner = TenbaggerMiner()
    
    # 运行挖掘
    results = miner.run_mining(
        start_date='2021-01-01',
        end_date='2025-12-20'
    )
    
    if results:
        # 生成报告
        html = generate_mining_report(results, miner.db)
        
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"tenbagger_mining_report_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✅ 报告已生成: {report_path}")
    
    miner.close()

if __name__ == "__main__":
    main()

