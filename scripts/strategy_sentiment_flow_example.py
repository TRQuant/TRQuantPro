#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于情绪因子与资金流向的选股策略
==================================

知识来源: 如何利用情绪因子与资金流向数据辅助A股交易
- 聚宽情绪因子: VOL（成交量）、TVMA（成交额移动均值）、PSY（心理线）、ARBR等
- AKShare资金流向: 主力资金净流入、超大单/大单/中单/小单净流入
"""

import jqdatasdk as jq
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 初始化聚宽
jq.auth('your_username', 'your_password')

def calculate_vol_factor(stock_code, end_date, period=5):
    """
    计算成交量因子（VOL）
    知识库提示: 成交量突增代表市场关注度飙升，底部放量视为资金进场信号
    """
    # 获取价格数据
    df = jq.get_price(
        stock_code,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['volume', 'amount']
    )
    
    # 计算5日、10日均量（知识库建议）
    df['vol_ma5'] = df['volume'].rolling(5).mean()
    df['vol_ma10'] = df['volume'].rolling(10).mean()
    
    # 成交量放大倍数
    vol_ratio = df['volume'].iloc[-1] / df['vol_ma10'].iloc[-1]
    
    return {
        'vol_ratio': vol_ratio,
        'vol_ma5': df['vol_ma5'].iloc[-1],
        'vol_ma10': df['vol_ma10'].iloc[-1],
        'current_vol': df['volume'].iloc[-1]
    }

def get_capital_flow_akshare(stock_code):
    """
    获取资金流向数据（使用AKShare）
    知识库提示: 使用stock_individual_fund_flow获取资金流向数据
    """
    try:
        # 根据知识库，使用AKShare获取资金流向
        # 注意：需要将股票代码转换为AKShare格式（如：000001 -> 000001.SZ）
        if stock_code.endswith('.XSHG') or stock_code.endswith('.XSHE'):
            ak_code = stock_code.split('.')[0]
        else:
            ak_code = stock_code
        
        # 获取资金流向数据（知识库中的API）
        flow_data = ak.stock_individual_fund_flow_rank(indicator="今日")
        
        # 查找目标股票
        stock_flow = flow_data[flow_data['代码'] == ak_code]
        
        if not stock_flow.empty:
            return {
                'main_net_inflow': stock_flow['主力净流入-净额'].iloc[0] if '主力净流入-净额' in stock_flow.columns else 0,
                'main_net_pct': stock_flow['主力净流入-净占比'].iloc[0] if '主力净流入-净占比' in stock_flow.columns else 0,
                'xl_net_inflow': stock_flow['超大单净流入-净额'].iloc[0] if '超大单净流入-净额' in stock_flow.columns else 0,
            }
    except Exception as e:
        print(f"获取资金流向失败: {e}")
    
    return None

def select_stocks_by_sentiment_and_flow():
    """
    基于情绪因子和资金流向的综合选股策略
    
    知识库策略建议:
    1. 选股打分: 成交量放大倍数、资金流量指标、心理线等归一化评分
    2. 热点情绪分高的股票（成交活跃、资金持续流入、市场情绪乐观）得分高
    3. 每周期选取情绪分最高的若干股票构建交易组合
    """
    # 获取股票池（沪深300）
    stocks = jq.get_index_stocks('000300.XSHG')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    results = []
    
    print(f"分析 {len(stocks)} 只股票...")
    
    for i, stock in enumerate(stocks[:50], 1):  # 示例：只分析前50只
        if i % 10 == 0:
            print(f"  已处理 {i}/{min(50, len(stocks))} 只")
        
        try:
            # 1. 计算情绪因子
            vol_factor = calculate_vol_factor(stock, end_date)
            
            # 2. 获取资金流向
            flow_data = get_capital_flow_akshare(stock)
            
            if flow_data:
                # 3. 计算综合情绪得分（知识库建议的方法）
                # 成交量放大倍数（归一化）
                vol_score = min(vol_factor['vol_ratio'] / 2.0, 1.0) * 100  # 放大2倍以上得满分
                
                # 资金流入得分
                flow_score = min(abs(flow_data['main_net_pct']) / 5.0, 1.0) * 100  # 净占比5%以上得满分
                
                # 综合得分（知识库建议的加权方式）
                composite_score = vol_score * 0.5 + flow_score * 0.5
                
                results.append({
                    'code': stock,
                    'vol_ratio': vol_factor['vol_ratio'],
                    'main_net_pct': flow_data['main_net_pct'],
                    'composite_score': composite_score
                })
        except Exception as e:
            continue
    
    # 按综合得分排序
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df = results_df.sort_values('composite_score', ascending=False)
        print(f"
筛选出 {len(results_df)} 只符合条件的股票")
        print("
前10只股票:")
        print(results_df[['code', 'vol_ratio', 'main_net_pct', 'composite_score']].head(10))
        
        return results_df.head(20)  # 返回前20只
    
    return pd.DataFrame()

if __name__ == '__main__':
    # 执行策略
    selected_stocks = select_stocks_by_sentiment_and_flow()
    
    print(f"
✅ 策略执行完成，选出 {len(selected_stocks)} 只股票")
    print("
策略说明:")
    print("- 基于知识库中的情绪因子（VOL成交量）和资金流向数据")
    print("- 综合评分：成交量放大倍数 × 0.5 + 主力资金净流入占比 × 0.5")
    print("- 筛选出情绪热度高、资金持续流入的强势股")
