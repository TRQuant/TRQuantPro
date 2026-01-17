#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A股特色指标数据获取测试脚本
============================

测试内容：
1. 北向资金数据 (沪深港通)
2. 融资融券数据 (两融)
3. 市场宽度数据 (涨跌停、涨跌家数)
4. 综合指标聚合

使用方法:
    python scripts/test_astock_indicators.py
"""

import sys
import os

# 添加项目路径
project_root = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, project_root)

import logging
from datetime import datetime, timedelta
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_jqdata_connection():
    """测试JQData连接"""
    print("\n" + "="*60)
    print("📡 测试JQData连接")
    print("="*60)
    
    try:
        from jqdata.client import JQDataClient
        
        client = JQDataClient()
        # 自动从配置文件认证
        import json
        config_path = os.path.join(project_root, "config/jqdata_credentials.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            client.authenticate(config['username'], config['password'])
        else:
            # 尝试备用配置文件
            config_path2 = os.path.join(project_root, "config/jqdata_config.json")
            if os.path.exists(config_path2):
                with open(config_path2, 'r') as f:
                    config = json.load(f)
                client.authenticate(config['username'], config['password'])
        
        if client.is_authenticated():
            print("✅ JQData认证成功")
            perm = client.get_permission()
            print(f"   数据权限: {perm}")
            return client
        else:
            print("❌ JQData认证失败")
            return None
            
    except Exception as e:
        print(f"❌ JQData连接失败: {e}")
        return None


def test_north_fund_jqdata(jq_client):
    """测试北向资金数据 - JQData"""
    print("\n" + "="*60)
    print("💰 测试北向资金数据 (JQData)")
    print("="*60)
    
    try:
        import jqdatasdk as jq
        from jqdatasdk import finance, query
        
        # 获取权限范围内的日期
        end_date = jq_client.get_available_end_date()
        print(f"📅 查询日期: {end_date}")
        
        # 1. 测试 STK_ML_QUOTA - 市场通成交与额度
        print("\n📊 STK_ML_QUOTA (沪深股通成交额度):")
        q = query(
            finance.STK_ML_QUOTA
        ).filter(
            finance.STK_ML_QUOTA.day == end_date
        ).limit(10)
        
        df_quota = finance.run_query(q)
        if df_quota is not None and not df_quota.empty:
            print(f"   ✅ 获取到 {len(df_quota)} 条记录")
            print(f"   字段: {list(df_quota.columns)}")
            print(df_quota.head())
        else:
            print("   ⚠️ 未获取到数据，尝试更早日期...")
            # 尝试更早的日期
            for days_ago in [1, 2, 3, 5, 7]:
                test_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                q = query(finance.STK_ML_QUOTA).filter(finance.STK_ML_QUOTA.day == test_date).limit(10)
                df_quota = finance.run_query(q)
                if df_quota is not None and not df_quota.empty:
                    print(f"   ✅ {test_date} 获取到 {len(df_quota)} 条记录")
                    print(df_quota.head())
                    break
        
        # 2. 测试 STK_HK_HOLD_INFO - 沪深港通持股
        print("\n📊 STK_HK_HOLD_INFO (北向持股明细):")
        q2 = query(
            finance.STK_HK_HOLD_INFO
        ).filter(
            finance.STK_HK_HOLD_INFO.day == end_date
        ).limit(10)
        
        df_hold = finance.run_query(q2)
        if df_hold is not None and not df_hold.empty:
            print(f"   ✅ 获取到 {len(df_hold)} 条记录")
            print(f"   字段: {list(df_hold.columns)}")
            print(df_hold.head())
        else:
            print("   ⚠️ 当日无数据，尝试历史日期...")
            for days_ago in [1, 2, 3, 5]:
                test_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                q2 = query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.day == test_date).limit(10)
                df_hold = finance.run_query(q2)
                if df_hold is not None and not df_hold.empty:
                    print(f"   ✅ {test_date} 获取到 {len(df_hold)} 条记录")
                    print(df_hold.head())
                    break
        
        return True
        
    except Exception as e:
        print(f"❌ 北向资金测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_margin_jqdata(jq_client):
    """测试融资融券数据 - JQData"""
    print("\n" + "="*60)
    print("📈 测试融资融券数据 (JQData)")
    print("="*60)
    
    try:
        import jqdatasdk as jq
        from jqdatasdk import finance, query
        
        end_date = jq_client.get_available_end_date()
        print(f"📅 查询日期: {end_date}")
        
        # 1. 测试 STK_MT_TOTAL - 融资融券汇总
        print("\n📊 STK_MT_TOTAL (融资融券汇总):")
        q = query(
            finance.STK_MT_TOTAL
        ).filter(
            finance.STK_MT_TOTAL.date == end_date
        ).limit(10)
        
        df_mt = finance.run_query(q)
        if df_mt is not None and not df_mt.empty:
            print(f"   ✅ 获取到 {len(df_mt)} 条记录")
            print(f"   字段: {list(df_mt.columns)}")
            print(df_mt)
            
            # 计算汇总
            total_fin = df_mt['fin_balance'].sum() / 100000000 if 'fin_balance' in df_mt.columns else 0
            total_sec = df_mt['sec_balance'].sum() / 100000000 if 'sec_balance' in df_mt.columns else 0
            print(f"\n   📊 汇总: 融资余额={total_fin:.2f}亿, 融券余额={total_sec:.2f}亿")
        else:
            print("   ⚠️ 当日无数据，尝试历史日期...")
            for days_ago in [1, 2, 3, 5, 7]:
                test_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                q = query(finance.STK_MT_TOTAL).filter(finance.STK_MT_TOTAL.date == test_date).limit(10)
                df_mt = finance.run_query(q)
                if df_mt is not None and not df_mt.empty:
                    print(f"   ✅ {test_date} 获取到 {len(df_mt)} 条记录")
                    print(df_mt)
                    break
        
        return True
        
    except Exception as e:
        print(f"❌ 融资融券测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_market_breadth_jqdata(jq_client):
    """测试市场宽度数据 - JQData"""
    print("\n" + "="*60)
    print("📊 测试市场宽度数据 (JQData)")
    print("="*60)
    
    try:
        import jqdatasdk as jq
        
        end_date = jq_client.get_available_end_date()
        print(f"📅 查询日期: {end_date}")
        
        # 获取所有A股
        all_stocks = jq.get_all_securities(types=['stock'], date=end_date)
        print(f"   📈 全市场股票数量: {len(all_stocks)}")
        
        # 随机取样100只股票测试
        sample_stocks = all_stocks.index.tolist()[:100]
        
        # 获取涨跌停价
        print("\n📊 测试涨跌停价获取:")
        df = jq.get_price(
            sample_stocks,
            start_date=end_date,
            end_date=end_date,
            frequency='daily',
            fields=['close', 'high_limit', 'low_limit', 'pre_close', 'volume']
        )
        
        if df is not None and not df.empty:
            print(f"   ✅ 获取到 {len(df)} 条记录")
            print(f"   字段: {list(df.columns)}")
            
            # 统计涨跌停
            if 'high_limit' in df.columns and 'close' in df.columns:
                limit_up = df[df['close'] >= df['high_limit'] * 0.999]
                limit_down = df[df['close'] <= df['low_limit'] * 1.001]
                
                print(f"\n   📈 样本统计 (100只股票):")
                print(f"      涨停: {len(limit_up)} 只")
                print(f"      跌停: {len(limit_down)} 只")
            
            # 统计涨跌
            if 'close' in df.columns and 'pre_close' in df.columns:
                df['change'] = df['close'] - df['pre_close']
                up_count = len(df[df['change'] > 0])
                down_count = len(df[df['change'] < 0])
                flat_count = len(df[df['change'] == 0])
                
                print(f"      上涨: {up_count} 只")
                print(f"      下跌: {down_count} 只")
                print(f"      平盘: {flat_count} 只")
                
                if down_count > 0:
                    print(f"      涨跌比: {up_count/down_count:.2f}")
        else:
            print("   ⚠️ 未获取到行情数据")
        
        return True
        
    except Exception as e:
        print(f"❌ 市场宽度测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_astock_indicators_module(jq_client):
    """测试A股指标模块"""
    print("\n" + "="*60)
    print("🔧 测试 astock_indicators 模块")
    print("="*60)
    
    try:
        from core.astock_indicators import (
            AStockIndicatorAggregator,
            NorthFundAnalyzer,
            MarginAnalyzer,
            MarketBreadthAnalyzer,
            get_astock_indicators
        )
        
        end_date = jq_client.get_available_end_date()
        print(f"📅 分析日期: {end_date}")
        
        # 测试北向资金分析器
        print("\n📊 NorthFundAnalyzer:")
        north_analyzer = NorthFundAnalyzer(jq_client)
        north_result = north_analyzer.analyze(end_date)
        print(f"   当日净买入: {north_result.net_buy_amount:.2f}亿")
        print(f"   沪股通: {north_result.sh_net_buy:.2f}亿")
        print(f"   深股通: {north_result.sz_net_buy:.2f}亿")
        print(f"   5日累计: {north_result.net_buy_5d:.2f}亿")
        print(f"   信号得分: {north_result.signal_score:.1f}")
        print(f"   信号描述: {north_result.signal_description}")
        
        # 测试融资融券分析器
        print("\n📊 MarginAnalyzer:")
        margin_analyzer = MarginAnalyzer(jq_client)
        margin_result = margin_analyzer.analyze(end_date)
        print(f"   融资余额: {margin_result.fin_balance:.2f}亿")
        print(f"   融券余额: {margin_result.sec_balance:.2f}亿")
        print(f"   融资变化率: {margin_result.fin_change_rate:.2f}%")
        print(f"   信号得分: {margin_result.signal_score:.1f}")
        print(f"   信号描述: {margin_result.signal_description}")
        
        # 测试市场宽度分析器
        print("\n📊 MarketBreadthAnalyzer:")
        breadth_analyzer = MarketBreadthAnalyzer(jq_client)
        breadth_result = breadth_analyzer.analyze(end_date)
        print(f"   涨停家数: {breadth_result.limit_up_count}")
        print(f"   跌停家数: {breadth_result.limit_down_count}")
        print(f"   涨跌停比: {breadth_result.limit_up_down_ratio:.2f}")
        print(f"   上涨家数: {breadth_result.up_count}")
        print(f"   下跌家数: {breadth_result.down_count}")
        print(f"   涨跌比: {breadth_result.up_down_ratio:.2f}")
        print(f"   信号得分: {breadth_result.signal_score:.1f}")
        print(f"   信号描述: {breadth_result.signal_description}")
        
        # 测试综合聚合器
        print("\n📊 AStockIndicatorAggregator (综合):")
        aggregator = AStockIndicatorAggregator(jq_client)
        result = aggregator.analyze(end_date)
        print(f"   综合得分: {result.composite_score:.1f}")
        print(f"   信号级别: {result.signal_level}")
        print(f"   建议: {result.recommendation}")
        print(f"   数据源: {result.data_source}")
        
        return result
        
    except Exception as e:
        print(f"❌ A股指标模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_akshare_fallback():
    """测试AKShare备用方案"""
    print("\n" + "="*60)
    print("🔄 测试AKShare备用数据源")
    print("="*60)
    
    try:
        import akshare as ak
        
        # 测试北向资金
        print("\n📊 北向资金 (AKShare):")
        try:
            df = ak.stock_hsgt_north_net_flow_in_em()
            if df is not None and not df.empty:
                print(f"   ✅ 获取到 {len(df)} 条记录")
                print(f"   字段: {list(df.columns)}")
                print(df.tail(3))
            else:
                print("   ⚠️ 未获取到数据")
        except Exception as e:
            print(f"   ❌ 获取失败: {e}")
        
        # 测试涨停池
        print("\n📊 涨停池 (AKShare):")
        try:
            today = datetime.now().strftime('%Y%m%d')
            df_zt = ak.stock_zt_pool_em(date=today)
            if df_zt is not None and not df_zt.empty:
                print(f"   ✅ 今日涨停 {len(df_zt)} 只")
            else:
                print("   ⚠️ 今日无涨停数据")
        except Exception as e:
            print(f"   ❌ 获取失败: {e}")
        
        return True
        
    except ImportError:
        print("   ⚠️ AKShare未安装")
        return False
    except Exception as e:
        print(f"❌ AKShare测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*70)
    print("🚀 A股特色指标数据获取测试")
    print("="*70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 测试JQData连接
    jq_client = test_jqdata_connection()
    
    if jq_client:
        # 2. 测试北向资金
        test_north_fund_jqdata(jq_client)
        
        # 3. 测试融资融券
        test_margin_jqdata(jq_client)
        
        # 4. 测试市场宽度
        test_market_breadth_jqdata(jq_client)
        
        # 5. 测试A股指标模块
        result = test_astock_indicators_module(jq_client)
        
        if result:
            print("\n" + "="*60)
            print("✅ 测试完成 - 汇总结果")
            print("="*60)
            print(f"   日期: {result.date}")
            print(f"   综合得分: {result.composite_score:.1f}")
            print(f"   市场信号: {result.signal_level}")
            print(f"   投资建议: {result.recommendation}")
    else:
        print("\n⚠️ JQData连接失败，测试AKShare备用方案...")
    
    # 6. 测试AKShare备用
    test_akshare_fallback()
    
    print("\n" + "="*70)
    print("🏁 测试结束")
    print("="*70)


if __name__ == "__main__":
    main()

