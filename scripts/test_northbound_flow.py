#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试北向资金数据获取
====================

测试AKShare和项目封装的北向资金数据获取功能

Author: TRQuant Team
Date: 2026-01-13
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

def test_akshare_direct():
    """测试AKShare直接调用"""
    print("=" * 80)
    print("测试1: AKShare直接调用")
    print("=" * 80)
    
    try:
        import akshare as ak
        
        # 测试1.1: 汇总数据API
        print("\n📊 测试 stock_hsgt_fund_flow_summary_em()...")
        df = ak.stock_hsgt_fund_flow_summary_em()
        
        if df is not None and not df.empty:
            print(f"   ✅ 成功获取数据: {len(df)} 条记录")
            print(f"   字段: {list(df.columns)}")
            
            # 筛选北向资金
            north_df = df[df["资金方向"] == "北向"] if "资金方向" in df.columns else df
            print(f"\n   北向资金数据: {len(north_df)} 条")
            
            if not north_df.empty:
                print("\n   最新数据预览:")
                print(north_df.head().to_string())
                
                # 尝试计算今日净流入
                if "成交净买额" in north_df.columns:
                    total_net = north_df["成交净买额"].sum() / 1e8  # 转换为亿元
                    print(f"\n   今日净流入: {total_net:.2f} 亿元")
        else:
            print("   ⚠️ 数据为空")
    
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试1.2: 北向资金净流入API
    try:
        print("\n📊 测试 stock_hsgt_north_net_flow_in_em()...")
        df2 = ak.stock_hsgt_north_net_flow_in_em()
        
        if df2 is not None and not df2.empty:
            print(f"   ✅ 成功获取数据: {len(df2)} 条记录")
            print(f"   字段: {list(df2.columns)}")
            
            # 获取最新数据
            latest = df2.iloc[-1]
            print(f"\n   最新数据:")
            for col in df2.columns:
                value = latest.get(col, 'N/A')
                print(f"     {col}: {value}")
            
            # 尝试提取净流入
            net_flow = None
            for col in ['北向资金', '当日净买入', '当日净流入', '成交净买额']:
                if col in latest.index:
                    net_flow = latest[col]
                    if isinstance(net_flow, (int, float)):
                        net_flow = net_flow / 1e8 if abs(net_flow) > 1e6 else net_flow
                        print(f"\n   今日净流入: {net_flow:.2f} 亿元")
                    break
        else:
            print("   ⚠️ 数据为空")
    
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_capital_flow_analyzer():
    """测试CapitalFlowAnalyzer"""
    print("\n" + "=" * 80)
    print("测试2: CapitalFlowAnalyzer（项目封装）")
    print("=" * 80)
    
    try:
        from core.capital_flow import CapitalFlowAnalyzer
        
        analyzer = CapitalFlowAnalyzer()
        flows = analyzer.get_northbound_flow(days=5)
        
        if flows:
            print(f"\n   ✅ 成功获取 {len(flows)} 条记录")
            
            # 显示最新数据
            latest = flows[-1]
            print(f"\n   最新数据:")
            print(f"     日期: {latest.date}")
            print(f"     沪股通净流入: {latest.sh_net:.2f} 亿元")
            print(f"     深股通净流入: {latest.sz_net:.2f} 亿元")
            print(f"     总净流入: {latest.total_net:.2f} 亿元")
            print(f"     沪股通买入: {latest.sh_buy:.2f} 亿元")
            print(f"     沪股通卖出: {latest.sh_sell:.2f} 亿元")
            print(f"     深股通买入: {latest.sz_buy:.2f} 亿元")
            print(f"     深股通卖出: {latest.sz_sell:.2f} 亿元")
        else:
            print("   ⚠️ 未获取到数据")
    
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_real_data_fetcher():
    """测试RealDataFetcher"""
    print("\n" + "=" * 80)
    print("测试3: RealDataFetcher（项目封装）")
    print("=" * 80)
    
    try:
        from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
        
        fetcher = RealDataFetcher()
        result = fetcher.fetch_northbound_flow()
        
        if result and result.success:
            print(f"\n   ✅ 数据获取成功")
            print(f"   获取时间: {result.fetch_time}")
            
            if result.data:
                data = result.data
                print(f"\n   数据内容:")
                print(f"     今日净流入: {data.get('today_net', 0):.2f} 亿元")
                print(f"     周净流入: {data.get('week_net', 0):.2f} 亿元")
                print(f"     月净流入: {data.get('month_net', 0):.2f} 亿元")
                print(f"     获取日期: {data.get('fetch_date', 'N/A')}")
                
                if 'details' in data:
                    print(f"\n   详细信息: {len(data['details'])} 条")
                    for detail in data['details'][:3]:  # 显示前3条
                        print(f"     {detail}")
        else:
            print(f"   ⚠️ 数据获取失败: {result.message if result else 'Unknown'}")
    
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_north_fund_analyzer():
    """测试NorthFundAnalyzer"""
    print("\n" + "=" * 80)
    print("测试4: NorthFundAnalyzer（项目封装，支持JQData和AKShare）")
    print("=" * 80)
    
    try:
        from core.astock_indicators import NorthFundAnalyzer
        
        analyzer = NorthFundAnalyzer(jq_client=None)  # 不使用JQData，使用AKShare
        data = analyzer.analyze(target_date=None)  # 使用最新日期
        
        if data:
            print(f"\n   ✅ 分析成功")
            print(f"\n   数据:")
            print(f"     日期: {data.date}")
            print(f"     沪股通净买入: {data.sh_net_buy:.2f} 亿元")
            print(f"     深股通净买入: {data.sz_net_buy:.2f} 亿元")
            print(f"     合计净买入: {data.net_buy_amount:.2f} 亿元")
            print(f"     5日累计: {data.net_buy_5d:.2f} 亿元")
            print(f"     10日累计: {data.net_buy_10d:.2f} 亿元")
            print(f"     信号描述: {data.signal_description}")
            # 打印所有可用属性
            print(f"\n   所有属性:")
            for attr in dir(data):
                if not attr.startswith('_'):
                    try:
                        value = getattr(data, attr)
                        if not callable(value):
                            print(f"     {attr}: {value}")
                    except:
                        pass
        else:
            print("   ⚠️ 未获取到数据")
    
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("北向资金数据获取测试")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目目录: {PROJECT_ROOT}")
    
    # 测试1: AKShare直接调用
    test_akshare_direct()
    
    # 测试2: CapitalFlowAnalyzer
    test_capital_flow_analyzer()
    
    # 测试3: RealDataFetcher
    test_real_data_fetcher()
    
    # 测试4: NorthFundAnalyzer
    test_north_fund_analyzer()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == '__main__':
    main()
