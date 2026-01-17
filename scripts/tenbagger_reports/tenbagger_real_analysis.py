#!/usr/bin/env python3
"""
十倍股真实数据分析
使用JQData获取真实数据，识别潜在十倍股并验证
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

def authenticate():
    """认证JQData"""
    jq_client = JQDataClient()
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    jq_client.authenticate(jq_config['username'], jq_config['password'])
    return jq_client

def get_candidate_stocks(jq_client, date: str):
    """获取候选股票池"""
    from jqdatasdk import query, valuation, indicator, get_fundamentals, get_all_securities
    
    # 获取所有股票
    all_stocks = get_all_securities(types=['stock'], date=date)
    
    # 过滤条件：排除ST、科创板、北交所
    stocks = all_stocks[
        (~all_stocks['display_name'].str.contains('ST')) &
        (~all_stocks.index.str.startswith('688')) &
        (~all_stocks.index.str.startswith('8'))
    ].head(500)  # 取前500只进行分析
    
    return stocks.index.tolist()

def analyze_stock(jq_client, symbol: str, analysis_date: str):
    """分析单只股票"""
    from jqdatasdk import query, valuation, indicator, get_fundamentals, get_price
    
    result = {
        'symbol': symbol,
        'name': '',
        'analysis_date': analysis_date,
        'financial': {},
        'valuation': {},
        'technical': {},
        'score': 0,
        'stage': 'S0',
        'recommendation': 'D'
    }
    
    try:
        # 获取股票名称
        from jqdatasdk import get_security_info
        info = get_security_info(symbol)
        result['name'] = info.display_name if info else symbol
        
        # 1. 获取财务指标
        q = query(
            indicator.roe,
            indicator.gross_profit_margin,
            indicator.net_profit_margin,
            indicator.inc_revenue_year_on_year,
            indicator.inc_net_profit_year_on_year,
            indicator.eps
        ).filter(indicator.code == symbol)
        
        df_fin = get_fundamentals(q, date=analysis_date)
        if df_fin is not None and len(df_fin) > 0:
            row = df_fin.iloc[0]
            result['financial'] = {
                'roe': float(row.get('roe', 0) or 0),
                'gross_margin': float(row.get('gross_profit_margin', 0) or 0),
                'net_margin': float(row.get('net_profit_margin', 0) or 0),
                'revenue_growth': float(row.get('inc_revenue_year_on_year', 0) or 0),
                'profit_growth': float(row.get('inc_net_profit_year_on_year', 0) or 0),
                'eps': float(row.get('eps', 0) or 0)
            }
        
        # 2. 获取估值指标
        q2 = query(
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap,
            valuation.turnover_ratio
        ).filter(valuation.code == symbol)
        
        df_val = get_fundamentals(q2, date=analysis_date)
        if df_val is not None and len(df_val) > 0:
            row = df_val.iloc[0]
            result['valuation'] = {
                'pe': float(row.get('pe_ratio', 0) or 0),
                'pb': float(row.get('pb_ratio', 0) or 0),
                'market_cap': float(row.get('market_cap', 0) or 0),
                'turnover': float(row.get('turnover_ratio', 0) or 0)
            }
        
        # 3. 获取价格数据计算技术指标
        start_date = (datetime.strptime(analysis_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')
        prices = get_price(symbol, start_date=start_date, end_date=analysis_date, 
                          frequency='daily', fields=['close', 'volume'])
        
        if prices is not None and len(prices) >= 20:
            close = prices['close']
            volume = prices['volume']
            
            # 均线
            ma5 = close.tail(5).mean()
            ma20 = close.tail(20).mean()
            ma60 = close.tail(60).mean() if len(close) >= 60 else ma20
            
            # 均线多头
            current_price = close.iloc[-1]
            ma_bullish = current_price > ma5 > ma20
            
            # 成交量比率
            vol_5 = volume.tail(5).mean()
            vol_20 = volume.tail(20).mean()
            vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
            
            # 20日涨幅
            if len(close) >= 20:
                price_20d_ago = close.iloc[-20]
                change_20d = (current_price - price_20d_ago) / price_20d_ago * 100 if price_20d_ago > 0 else 0
            else:
                change_20d = 0
            
            result['technical'] = {
                'price': current_price,
                'ma5': ma5,
                'ma20': ma20,
                'ma60': ma60,
                'ma_bullish': ma_bullish,
                'vol_ratio': vol_ratio,
                'change_20d': change_20d
            }
        
        # 4. 计算综合得分
        score = calculate_score(result)
        result['score'] = score
        
        # 5. 判定阶段和推荐等级
        result['stage'] = determine_stage(result)
        result['recommendation'] = determine_recommendation(score)
        
    except Exception as e:
        print(f"  ❌ 分析{symbol}失败: {e}")
    
    return result

def calculate_score(data: dict) -> float:
    """计算综合得分（100分制）"""
    score = 0
    
    fin = data.get('financial', {})
    val = data.get('valuation', {})
    tech = data.get('technical', {})
    
    # 财务因子（40分）
    # 营收增速（10分）
    rev_growth = fin.get('revenue_growth', 0)
    if rev_growth >= 30:
        score += 10
    elif rev_growth >= 15:
        score += 7
    elif rev_growth >= 0:
        score += 3
    
    # 利润增速（10分）
    profit_growth = fin.get('profit_growth', 0)
    if profit_growth >= 50:
        score += 10
    elif profit_growth >= 20:
        score += 7
    elif profit_growth >= 0:
        score += 3
    
    # 毛利率（8分）
    gross_margin = fin.get('gross_margin', 0)
    if gross_margin >= 40:
        score += 8
    elif gross_margin >= 25:
        score += 5.6
    elif gross_margin >= 15:
        score += 2.4
    
    # ROE（7分）
    roe = fin.get('roe', 0)
    if roe >= 15:
        score += 7
    elif roe >= 10:
        score += 4.9
    elif roe >= 5:
        score += 2.1
    
    # 净利率（5分）
    net_margin = fin.get('net_margin', 0)
    if net_margin >= 15:
        score += 5
    elif net_margin >= 5:
        score += 3.5
    
    # 估值因子（20分）
    # PE（8分）
    pe = val.get('pe', 0)
    if 0 < pe <= 30:
        score += 8
    elif 0 < pe <= 50:
        score += 5.6
    elif 0 < pe <= 100:
        score += 2.4
    
    # PEG（7分）- 简化计算
    if profit_growth > 0 and pe > 0:
        peg = pe / profit_growth
        if peg <= 1:
            score += 7
        elif peg <= 2:
            score += 4.9
        elif peg <= 3:
            score += 2.1
    
    # 市值（5分）
    market_cap = val.get('market_cap', 0)
    if 20 <= market_cap <= 100:
        score += 5
    elif 100 < market_cap <= 300:
        score += 3.5
    elif market_cap < 20:
        score += 1.5
    
    # 技术因子（15分）
    # 均线多头（5分）
    if tech.get('ma_bullish', False):
        score += 5
    
    # 成交量趋势（5分）
    vol_ratio = tech.get('vol_ratio', 1)
    if vol_ratio >= 1.5:
        score += 5
    elif vol_ratio >= 1.2:
        score += 3.5
    
    # 20日涨幅（5分）
    change_20d = tech.get('change_20d', 0)
    if change_20d >= 20:
        score += 5
    elif change_20d >= 10:
        score += 3.5
    elif change_20d >= 0:
        score += 1.5
    
    return round(score, 1)

def determine_stage(data: dict) -> str:
    """判定阶段"""
    fin = data.get('financial', {})
    tech = data.get('technical', {})
    
    rev_growth = fin.get('revenue_growth', 0)
    profit_growth = fin.get('profit_growth', 0)
    ma_bullish = tech.get('ma_bullish', False)
    vol_ratio = tech.get('vol_ratio', 1)
    
    if rev_growth >= 40 and profit_growth >= 50 and ma_bullish and vol_ratio >= 1.5:
        return 'S3'  # 放量期
    elif rev_growth >= 25 and profit_growth >= 30 and ma_bullish:
        return 'S2'  # 导入期（最佳买入点）
    elif rev_growth >= 15 and profit_growth >= 20:
        return 'S1'  # 验证期
    else:
        return 'S0'  # 观察期

def determine_recommendation(score: float) -> str:
    """判定推荐等级"""
    if score >= 80:
        return 'S+'
    elif score >= 70:
        return 'S'
    elif score >= 60:
        return 'A'
    elif score >= 50:
        return 'B'
    elif score >= 40:
        return 'C'
    else:
        return 'D'

def get_current_price(jq_client, symbol: str, current_date: str) -> dict:
    """获取当前价格信息（优先使用AKShare获取最近3个月数据）"""
    # 优先尝试AKShare（可以获取最近3个月数据，无限制）
    try:
        import akshare as ak
        
        # 转换代码格式：000001.XSHE -> 000001
        code = symbol.split('.')[0]
        
        # 获取最近3个月数据
        end_date = datetime.strptime(current_date, '%Y-%m-%d').strftime('%Y%m%d')
        start_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y%m%d')
        
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if df is not None and len(df) > 0:
            latest_price = float(df['收盘'].iloc[-1])
            latest_date = df['日期'].iloc[-1]
            return {
                'price': latest_price,
                'date': latest_date if isinstance(latest_date, str) else latest_date.strftime('%Y-%m-%d'),
                'source': 'akshare'
            }
    except Exception as e:
        print(f"  AKShare获取{symbol}价格失败，降级到AllTick: {e}")
    
    # 降级到AllTick
    try:
        from data_sources.alltick_source import AllTickSource
        alltick = AllTickSource()
        if alltick.connect():
            price_info = alltick.get_realtime_price(symbol)
            if price_info and price_info.get('price'):
                return {
                    'price': price_info['price'],
                    'date': price_info['timestamp'].strftime('%Y-%m-%d') if hasattr(price_info['timestamp'], 'strftime') else current_date,
                    'source': 'alltick'
                }
    except Exception as e:
        print(f"  AllTick获取{symbol}价格失败，降级到JQData: {e}")
    
    # 最后降级到JQData
    try:
        from jqdatasdk import get_price
        prices = get_price(symbol, end_date=current_date, count=1, 
                          frequency='daily', fields=['close'])
        if prices is not None and len(prices) > 0:
            return {
                'price': float(prices['close'].iloc[-1]),
                'date': current_date,
                'source': 'jqdata'
            }
    except Exception as e:
        print(f"  获取{symbol}当前价格失败: {e}")
    
    return {'price': 0, 'date': current_date, 'source': 'none'}

def main():
    """主函数"""
    print("=" * 60)
    print("📊 十倍股真实数据分析")
    print("=" * 60)
    
    # 认证
    print("\n1️⃣ 认证JQData...")
    jq_client = authenticate()
    
    # 获取可用日期
    end_date = jq_client.get_available_end_date()
    print(f"   可用数据截止日期: {end_date}")
    
    # 分析日期（3个月前）
    analysis_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
    print(f"   分析基准日期: {analysis_date}")
    
    # 获取候选股票
    print("\n2️⃣ 获取候选股票池...")
    candidates = get_candidate_stocks(jq_client, analysis_date)
    print(f"   候选股票数量: {len(candidates)}")
    
    # 分析股票
    print("\n3️⃣ 分析股票...")
    results = []
    
    # 分析前300只以获取更多样本
    for i, symbol in enumerate(candidates[:300]):
        if i % 50 == 0:
            print(f"   进度: {i+1}/{min(300, len(candidates))}")
        
        result = analyze_stock(jq_client, symbol, analysis_date)
        if result['score'] > 0:
            results.append(result)
    
    # 按得分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # 筛选高分股票（降低阈值以获取更多样本）
    high_score_stocks = [r for r in results if r['score'] >= 35]
    
    print(f"\n4️⃣ 筛选结果:")
    print(f"   总分析数量: {len(results)}")
    print(f"   35分以上数量: {len(high_score_stocks)}")
    
    # 获取当前价格进行验证
    print("\n5️⃣ 获取当前价格验证...")
    top_stocks = high_score_stocks[:20]  # 取前20只
    
    for stock in top_stocks:
        current_info = get_current_price(jq_client, stock['symbol'], end_date)
        stock['current_price'] = current_info['price']
        stock['current_date'] = current_info['date']
        
        # 计算收益
        analysis_price = stock['technical'].get('price', 0)
        if analysis_price > 0 and current_info['price'] > 0:
            stock['return_pct'] = round((current_info['price'] - analysis_price) / analysis_price * 100, 2)
        else:
            stock['return_pct'] = 0
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📈 潜在十倍股分析结果（Top 20）")
    print("=" * 60)
    
    print(f"\n{'代码':<12} {'名称':<10} {'得分':<6} {'阶段':<4} {'等级':<4} {'分析价':<10} {'当前价':<10} {'收益%':<8}")
    print("-" * 80)
    
    for stock in top_stocks:
        analysis_price = stock['technical'].get('price', 0)
        print(f"{stock['symbol']:<12} {stock['name'][:8]:<10} {stock['score']:<6.1f} {stock['stage']:<4} {stock['recommendation']:<4} {analysis_price:<10.2f} {stock['current_price']:<10.2f} {stock['return_pct']:>7.2f}%")
    
    # 保存结果
    output_file = '/home/taotao/dev/QuantTest/TRQuant/docs/tenbagger_analysis_data.json'
    output_data = {
        'analysis_date': analysis_date,
        'current_date': end_date,
        'total_analyzed': len(results),
        'high_score_count': len(high_score_stocks),
        'top_stocks': top_stocks
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ 结果已保存到: {output_file}")
    
    # 统计验证结果
    print("\n" + "=" * 60)
    print("📊 验证统计")
    print("=" * 60)
    
    positive_returns = [s for s in top_stocks if s['return_pct'] > 0]
    avg_return = sum(s['return_pct'] for s in top_stocks) / len(top_stocks) if top_stocks else 0
    
    print(f"   正收益股票数: {len(positive_returns)}/{len(top_stocks)} ({len(positive_returns)/len(top_stocks)*100:.1f}%)")
    print(f"   平均收益率: {avg_return:.2f}%")
    
    if positive_returns:
        max_return = max(s['return_pct'] for s in top_stocks)
        min_return = min(s['return_pct'] for s in top_stocks)
        print(f"   最大收益: {max_return:.2f}%")
        print(f"   最小收益: {min_return:.2f}%")
    
    return output_data

if __name__ == '__main__':
    main()

