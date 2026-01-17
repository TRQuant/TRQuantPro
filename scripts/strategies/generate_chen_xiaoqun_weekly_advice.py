#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成陈小群战法一周投资建议
========================

基于JQData、AKShare和知识库，生成实际的一周投资建议
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

try:
    import jqdatasdk as jq
    JQDATA_AVAILABLE = True
except ImportError:
    JQDATA_AVAILABLE = False
    print("⚠️  JQData未安装，将使用AKShare数据")

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️  AKShare未安装")

from mcp_servers.unified_dev_server import knowledge_search


def get_jqdata_config():
    """获取JQData配置"""
    config_file = TRQUANT_ROOT / "config" / "jqdata_config.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def init_jqdata():
    """初始化JQData"""
    if not JQDATA_AVAILABLE:
        return False
    
    config = get_jqdata_config()
    if not config:
        print("⚠️  JQData配置不存在")
        return False
    
    try:
        jq.auth(config['username'], config['password'])
        print("✅ JQData登录成功")
        return True
    except Exception as e:
        print(f"❌ JQData登录失败: {e}")
        return False


def get_market_index_data():
    """获取市场指数数据"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    if JQDATA_AVAILABLE and init_jqdata():
        try:
            # 获取沪深300指数
            hs300 = jq.get_price(
                '000300.XSHG',
                count=20,
                end_date=today,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            # 获取中证1000指数
            zz1000 = jq.get_price(
                '000852.XSHG',
                count=20,
                end_date=today,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            return {
                'hs300': hs300,
                'zz1000': zz1000,
                'source': 'jqdata'
            }
        except Exception as e:
            print(f"⚠️  JQData获取指数数据失败: {e}")
    
    # 使用AKShare作为备用
    if AKSHARE_AVAILABLE:
        try:
            # 获取沪深300指数
            hs300 = ak.stock_zh_index_daily(symbol="sh000300")
            zz1000 = ak.stock_zh_index_daily(symbol="sz399852")
            
            return {
                'hs300': hs300.tail(20),
                'zz1000': zz1000.tail(20),
                'source': 'akshare'
            }
        except Exception as e:
            print(f"⚠️  AKShare获取指数数据失败: {e}")
    
    return None


def judge_market_sentiment(index_data):
    """判断市场情绪周期"""
    if not index_data:
        return "未知"
    
    hs300 = index_data['hs300']
    zz1000 = index_data['zz1000']
    
    # 计算最近5日和20日涨跌幅
    hs300_5d_change = (hs300['close'].iloc[-1] / hs300['close'].iloc[-6] - 1) * 100 if len(hs300) >= 6 else 0
    hs300_20d_change = (hs300['close'].iloc[-1] / hs300['close'].iloc[-21] - 1) * 100 if len(hs300) >= 21 else 0
    
    zz1000_5d_change = (zz1000['close'].iloc[-1] / zz1000['close'].iloc[-6] - 1) * 100 if len(zz1000) >= 6 else 0
    zz1000_20d_change = (zz1000['close'].iloc[-1] / zz1000['close'].iloc[-21] - 1) * 100 if len(zz1000) >= 21 else 0
    
    # 计算成交量变化
    hs300_volume_5d_avg = hs300['volume'].tail(5).mean()
    hs300_volume_20d_avg = hs300['volume'].tail(20).mean()
    volume_ratio = hs300_volume_5d_avg / hs300_volume_20d_avg if hs300_volume_20d_avg > 0 else 1
    
    # 判断情绪周期
    if hs300_5d_change > 2 and zz1000_5d_change > 2 and volume_ratio > 1.2:
        return "加速期"
    elif hs300_5d_change > 0 and zz1000_5d_change > 0 and volume_ratio > 1.0:
        return "启动期"
    elif hs300_5d_change < -2 and zz1000_5d_change < -2:
        return "退潮期"
    else:
        return "高位震荡期"


def get_limit_up_stocks():
    """获取涨停股票"""
    if AKSHARE_AVAILABLE:
        try:
            # 获取实时行情
            spot_data = ak.stock_zh_a_spot_em()
            
            # 筛选涨停股票
            limit_up_stocks = spot_data[
                (spot_data['最新价'] == spot_data['涨停价']) &
                (spot_data['涨跌幅'] >= 9.5)
            ]
            
            return limit_up_stocks
        except Exception as e:
            print(f"⚠️  获取涨停股票失败: {e}")
    
    return None


def get_hot_boards():
    """获取热点板块"""
    if AKSHARE_AVAILABLE:
        try:
            # 获取概念板块
            concept_data = ak.stock_board_concept_name_em()
            
            # 检查字段是否存在
            if '涨跌幅' in concept_data.columns:
                # 筛选热点板块（涨幅>3%）
                hot_boards = concept_data[concept_data['涨跌幅'] > 3].head(10)
                
                # 如果有涨停数字段，进一步筛选
                if '涨停数' in concept_data.columns:
                    hot_boards = hot_boards[hot_boards['涨停数'] > 3]
                
                return hot_boards
        except Exception as e:
            print(f"⚠️  获取热点板块失败: {e}")
    
    return None


def get_first_board_candidates():
    """获取首板卡位候选股"""
    limit_up_stocks = get_limit_up_stocks()
    if limit_up_stocks is None or len(limit_up_stocks) == 0:
        return []
    
    candidates = []
    for _, stock in limit_up_stocks.iterrows():
        # 条件1: 流通市值<30亿
        market_cap = stock.get('总市值', 0)
        if market_cap > 0 and market_cap < 30 * 100000000:
            # 条件2: 封单量>2%（需要计算）
            limit_up_amount = stock.get('封单额', 0)
            if limit_up_amount > 0 and limit_up_amount / market_cap > 0.02:
                candidates.append({
                    'code': stock.get('代码', ''),
                    'name': stock.get('名称', ''),
                    'market_cap': market_cap / 100000000,  # 转换为亿
                    'limit_up_amount': limit_up_amount / 100000000,  # 转换为亿
                    'change_pct': stock.get('涨跌幅', 0)
                })
    
    return candidates


def search_knowledge_base(query):
    """搜索知识库"""
    try:
        result = knowledge_search(query, limit=3)
        if result.get("success") and result.get("results"):
            return result["results"]
    except Exception as e:
        print(f"⚠️  知识库搜索失败: {e}")
    
    return []


def generate_daily_advice(date, market_sentiment, index_data):
    """生成每日投资建议"""
    advice = {
        'date': date,
        'market_sentiment': market_sentiment,
        'position_suggestion': '',
        'strategy': '',
        'candidates': [],
        'risk_control': ''
    }
    
    # 根据情绪周期给出建议
    if market_sentiment == "启动期":
        advice['position_suggestion'] = "10%轻仓试错"
        advice['strategy'] = "首板卡位术"
        advice['candidates'] = get_first_board_candidates()
        advice['risk_control'] = "止损-5%，止盈+10%"
    elif market_sentiment == "加速期":
        advice['position_suggestion'] = "50%+重仓持有"
        advice['strategy'] = "二板定龙术或三板加速术"
        advice['risk_control'] = "止损-8%，止盈+20%"
    elif market_sentiment == "高位震荡期":
        advice['position_suggestion'] = "逐步减仓"
        advice['strategy'] = "锁定利润，防范风险"
        advice['risk_control'] = "逐步减仓，保留核心仓位"
    else:  # 退潮期
        advice['position_suggestion'] = "空仓观望"
        advice['strategy'] = "等待下一轮机会"
        advice['risk_control'] = "空仓，不操作"
    
    return advice


def generate_weekly_advice():
    """生成一周投资建议"""
    print("=" * 70)
    print("📊 生成陈小群战法一周投资建议")
    print("=" * 70)
    print()
    
    # 获取市场数据
    print("📡 获取市场数据...")
    index_data = get_market_index_data()
    market_sentiment = judge_market_sentiment(index_data) if index_data else "未知"
    
    print(f"✅ 市场情绪周期: {market_sentiment}")
    print()
    
    # 获取热点板块
    print("🔥 获取热点板块...")
    hot_boards = get_hot_boards()
    if hot_boards is not None and len(hot_boards) > 0:
        print(f"✅ 找到 {len(hot_boards)} 个热点板块")
        for _, board in hot_boards.head(5).iterrows():
            print(f"   - {board.get('板块名称', '')}: 涨幅{board.get('涨跌幅', 0):.2f}%, 涨停{board.get('涨停数', 0)}只")
    print()
    
    # 搜索知识库
    print("📚 搜索知识库...")
    kb_results = search_knowledge_base("陈小群三板斧战法")
    if kb_results:
        print(f"✅ 找到 {len(kb_results)} 条相关知识")
        for item in kb_results[:2]:
            print(f"   - {item.get('title', '')}")
    print()
    
    # 生成一周建议
    print("📝 生成一周投资建议...")
    weekly_advice = []
    
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        day_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][i]
        
        # 根据日期调整情绪周期（简化处理）
        if i == 0:
            current_sentiment = market_sentiment
        elif i < 3:
            # 前三天可能进入加速期
            current_sentiment = "加速期" if market_sentiment == "启动期" else market_sentiment
        else:
            # 后四天可能进入高位震荡或退潮
            current_sentiment = "高位震荡期" if market_sentiment == "加速期" else "退潮期"
        
        advice = generate_daily_advice(date, current_sentiment, index_data)
        advice['day_name'] = day_name
        weekly_advice.append(advice)
    
    return weekly_advice, market_sentiment, hot_boards


def format_weekly_advice(weekly_advice, market_sentiment, hot_boards):
    """格式化一周投资建议"""
    output = []
    
    output.append("=" * 70)
    output.append("📊 陈小群战法一周投资建议")
    output.append("=" * 70)
    output.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"当前市场情绪: {market_sentiment}")
    output.append("")
    
    if hot_boards is not None and len(hot_boards) > 0:
        output.append("🔥 热点板块:")
        for _, board in hot_boards.head(5).iterrows():
            output.append(f"   - {board.get('板块名称', '')}: 涨幅{board.get('涨跌幅', 0):.2f}%, 涨停{board.get('涨停数', 0)}只")
        output.append("")
    
    for advice in weekly_advice:
        output.append("-" * 70)
        output.append(f"📅 {advice['day_name']} ({advice['date']})")
        output.append("-" * 70)
        output.append(f"市场情绪: {advice['market_sentiment']}")
        output.append(f"建议仓位: {advice['position_suggestion']}")
        output.append(f"操作策略: {advice['strategy']}")
        output.append(f"风险控制: {advice['risk_control']}")
        
        if advice['candidates']:
            output.append("")
            output.append("候选股票:")
            for i, candidate in enumerate(advice['candidates'][:5], 1):
                output.append(f"   {i}. {candidate['name']} ({candidate['code']})")
                output.append(f"      流通市值: {candidate['market_cap']:.2f}亿")
                output.append(f"      封单额: {candidate['limit_up_amount']:.2f}亿")
                output.append(f"      涨跌幅: {candidate['change_pct']:.2f}%")
        
        output.append("")
    
    output.append("=" * 70)
    output.append("⚠️  风险提示:")
    output.append("1. 游资战法属于高风险策略，需要严格的风险控制")
    output.append("2. 战法效果与市场情绪周期密切相关")
    output.append("3. 需要极强的执行力和纪律性")
    output.append("4. 投资有风险，入市需谨慎")
    output.append("=" * 70)
    
    return "\n".join(output)


def main():
    """主函数"""
    weekly_advice, market_sentiment, hot_boards = generate_weekly_advice()
    
    # 格式化输出
    output = format_weekly_advice(weekly_advice, market_sentiment, hot_boards)
    
    # 打印到控制台
    print(output)
    
    # 保存到文件
    output_file = TRQUANT_ROOT / "docs" / "strategies" / "weekly_advice.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print()
    print(f"✅ 一周投资建议已保存到: {output_file}")


if __name__ == "__main__":
    main()
