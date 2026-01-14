#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股票盘中走势分析器
==================

功能：
1. 分析股票盘中走势（涨停-开板-再涨停）
2. 识别关键时间点（首次涨停、开板、再涨停）
3. 计算回调幅度和持续时间
4. 提供走势分析报告

使用方式：
    from core.stock_intraday_analyzer import StockIntradayAnalyzer
    
    analyzer = StockIntradayAnalyzer()
    result = analyzer.analyze_limit_up_pattern("002400", "2026-01-14")
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# 尝试导入AKShare
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    logger.warning("akshare未安装，盘中走势分析功能不可用")


class StockIntradayAnalyzer:
    """
    股票盘中走势分析器
    
    用于分析股票盘中走势，特别是"涨停-开板-再涨停"的情况
    """
    
    def __init__(self):
        """初始化分析器"""
        self.has_akshare = HAS_AKSHARE
    
    def get_minute_data(
        self,
        code: str,
        date: str,
        period: str = "1"
    ) -> Optional[pd.DataFrame]:
        """
        获取股票分时数据
        
        Args:
            code: 股票代码（6位数字）
            date: 日期（YYYY-MM-DD或YYYYMMDD格式）
            period: 周期（1=1分钟，5=5分钟）
        
        Returns:
            分时数据DataFrame
        """
        if not self.has_akshare:
            logger.error("akshare未安装，无法获取分时数据")
            return None
        
        try:
            # 转换日期格式
            if '-' in date:
                date_compact = date.replace('-', '')
            else:
                date_compact = date
            
            # 获取分时数据
            minute_data = ak.stock_zh_a_hist_min_em(
                symbol=code,
                start_date=date_compact,
                end_date=date_compact,
                period=period,
                adjust=''
            )
            
            if minute_data is not None and not minute_data.empty:
                # 确保时间列为datetime类型
                if '时间' in minute_data.columns:
                    minute_data['时间'] = pd.to_datetime(minute_data['时间'])
                elif 'date' in minute_data.columns:
                    minute_data['date'] = pd.to_datetime(minute_data['date'])
                    minute_data.rename(columns={'date': '时间'}, inplace=True)
                
                return minute_data
            else:
                logger.warning(f"获取{code}的分时数据为空")
                return None
                
        except Exception as e:
            logger.error(f"获取分时数据失败: {e}")
            return None
    
    def analyze_limit_up_pattern(
        self,
        code: str,
        date: str,
        limit_up_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        分析涨停-开板-再涨停模式
        
        Args:
            code: 股票代码
            date: 日期
            limit_up_price: 涨停价（如果为None，则从数据中推断）
        
        Returns:
            分析结果字典
        """
        # 获取分时数据
        minute_data = self.get_minute_data(code, date)
        if minute_data is None or minute_data.empty:
            return {
                'success': False,
                'error': '无法获取分时数据'
            }
        
        # 推断涨停价
        if limit_up_price is None:
            # 涨停价通常是当日的最高价（如果涨停）
            max_price = minute_data['最高'].max()
            # 或者使用收盘价的最大值
            max_close = minute_data['收盘'].max()
            limit_up_price = max(max_price, max_close)
        
        # 判断涨停的标准：收盘价接近涨停价（允许0.5%误差）
        limit_up_threshold = limit_up_price * 0.995
        
        # 标记涨停时间点
        minute_data['是否涨停'] = (
            (minute_data['收盘'] >= limit_up_threshold) & 
            (minute_data['最高'] >= limit_up_threshold)
        )
        
        # 找出涨停和开板的时间段
        limit_up_periods = []
        open_periods = []
        
        current_state = None
        period_start = None
        
        for idx, row in minute_data.iterrows():
            is_limit_up = row['是否涨停']
            
            if current_state is None:
                current_state = '涨停' if is_limit_up else '开板'
                period_start = row['时间']
            elif (current_state == '涨停' and not is_limit_up) or (current_state == '开板' and is_limit_up):
                # 状态变化
                period_end = minute_data.iloc[idx-1]['时间']
                if current_state == '涨停':
                    limit_up_periods.append((period_start, period_end))
                else:
                    open_periods.append((period_start, period_end))
                
                current_state = '涨停' if is_limit_up else '开板'
                period_start = row['时间']
        
        # 处理最后一个时间段
        if period_start is not None:
            period_end = minute_data.iloc[-1]['时间']
            if current_state == '涨停':
                limit_up_periods.append((period_start, period_end))
            else:
                open_periods.append((period_start, period_end))
        
        # 分析每个时间段
        limit_up_details = []
        for i, (start, end) in enumerate(limit_up_periods, 1):
            start_data = minute_data[minute_data['时间'] == start].iloc[0]
            end_data = minute_data[minute_data['时间'] == end].iloc[0]
            period_data = minute_data[(minute_data['时间'] >= start) & (minute_data['时间'] <= end)]
            
            duration_minutes = (end - start).total_seconds() / 60
            total_volume = period_data['成交量'].sum()
            avg_price = period_data['收盘'].mean()
            
            limit_up_details.append({
                'period': i,
                'start_time': start,
                'end_time': end,
                'duration_minutes': duration_minutes,
                'start_price': float(start_data['收盘']),
                'end_price': float(end_data['收盘']),
                'avg_price': float(avg_price),
                'total_volume': int(total_volume)
            })
        
        open_details = []
        for i, (start, end) in enumerate(open_periods, 1):
            period_data = minute_data[(minute_data['时间'] >= start) & (minute_data['时间'] <= end)]
            if not period_data.empty:
                start_data = period_data.iloc[0]
                end_data = period_data.iloc[-1]
                min_price = period_data['最低'].min()
                max_price = period_data['最高'].max()
                
                duration_minutes = (end - start).total_seconds() / 60
                total_volume = period_data['成交量'].sum()
                
                # 计算回调幅度
                start_price = float(start_data['收盘'])
                drawdown = (start_price - min_price) / start_price * 100 if start_price > 0 else 0
                
                open_details.append({
                    'period': i,
                    'start_time': start,
                    'end_time': end,
                    'duration_minutes': duration_minutes,
                    'start_price': float(start_data['收盘']),
                    'end_price': float(end_data['收盘']),
                    'min_price': float(min_price),
                    'max_price': float(max_price),
                    'drawdown_pct': drawdown,
                    'total_volume': int(total_volume)
                })
        
        # 判断走势模式
        pattern = "unknown"
        if len(limit_up_periods) > 1:
            pattern = "limit_up_open_limit_up"  # 涨停-开板-再涨停
        elif len(limit_up_periods) == 1 and len(open_periods) == 0:
            pattern = "direct_limit_up"  # 直接涨停，未开板
        elif len(limit_up_periods) == 1 and len(open_periods) == 1:
            if limit_up_periods[0][0] < open_periods[0][0]:
                pattern = "limit_up_then_open"  # 涨停后开板
            else:
                pattern = "open_then_limit_up"  # 开板后涨停
        
        # 计算关键指标
        first_limit_up_time = limit_up_periods[0][0] if limit_up_periods else None
        last_limit_up_time = limit_up_periods[-1][0] if limit_up_periods else None
        max_drawdown = max([d['drawdown_pct'] for d in open_details]) if open_details else 0
        
        result = {
            'success': True,
            'code': code,
            'date': date,
            'limit_up_price': float(limit_up_price),
            'pattern': pattern,
            'limit_up_count': len(limit_up_periods),
            'open_count': len(open_periods),
            'first_limit_up_time': first_limit_up_time,
            'last_limit_up_time': last_limit_up_time,
            'max_drawdown_pct': max_drawdown,
            'limit_up_periods': limit_up_details,
            'open_periods': open_details,
            'minute_data': minute_data  # 保留原始数据供进一步分析
        }
        
        return result
    
    def interpret_pattern(self, result: Dict[str, Any]) -> str:
        """
        解释走势模式的含义
        
        Args:
            result: analyze_limit_up_pattern返回的结果
        
        Returns:
            解释文本
        """
        if not result.get('success'):
            return "无法分析（数据获取失败）"
        
        pattern = result.get('pattern', 'unknown')
        limit_up_count = result.get('limit_up_count', 0)
        open_count = result.get('open_count', 0)
        max_drawdown = result.get('max_drawdown_pct', 0)
        
        interpretations = {
            'limit_up_open_limit_up': f"""
✅ **涨停-开板-再涨停模式**

📊 特征：
   • 涨停次数：{limit_up_count}次
   • 开板次数：{open_count}次
   • 最大回调：{max_drawdown:.2f}%

💡 市场含义：
   1. **资金博弈激烈**：多次开板说明多空双方分歧较大
   2. **承接力强**：每次开板后都能再次涨停，说明买盘力量较强
   3. **换手充分**：开板期间换手，有利于后续上涨
   4. **风险提示**：如果开板次数过多或回调幅度过大，可能封板不稳

🎯 操作建议：
   • 如果回调幅度<3%且开板次数≤2次：封板较稳，可考虑持有
   • 如果回调幅度>5%或开板次数>3次：封板不稳，需谨慎
   • 关注最后封板时间：越早封板，封板越稳
            """,
            
            'direct_limit_up': """
✅ **直接涨停模式**

📊 特征：
   • 一次涨停后封板，未开板

💡 市场含义：
   1. **买盘强劲**：涨停后买盘持续，无抛压
   2. **封板坚决**：资金态度明确，看好后市
   3. **换手不足**：可能缺乏充分换手，后续可能面临抛压

🎯 操作建议：
   • 封板较稳，但需关注次日开盘表现
   • 如果次日高开，可能继续上涨
   • 如果次日低开，可能面临回调
            """,
            
            'limit_up_then_open': f"""
⚠️ **涨停后开板模式**

📊 特征：
   • 涨停后开板，未再涨停
   • 最大回调：{max_drawdown:.2f}%

💡 市场含义：
   1. **封板不稳**：涨停后遭遇抛压
   2. **资金分歧**：多空双方分歧较大
   3. **风险较高**：可能面临回调

🎯 操作建议：
   • 谨慎持有，关注后续走势
   • 如果回调幅度>5%，建议减仓
   • 关注成交量：放量开板需警惕
            """,
            
            'open_then_limit_up': """
✅ **开板后涨停模式**

📊 特征：
   • 盘中开板，随后涨停

💡 市场含义：
   1. **洗盘充分**：开板期间完成换手
   2. **资金认可**：开板后资金继续买入
   3. **封板较稳**：开板后涨停，说明买盘力量强

🎯 操作建议：
   • 封板较稳，可考虑持有
   • 关注开板期间的成交量
   • 如果开板时间短且回调小，封板更稳
            """
        }
        
        return interpretations.get(pattern, "未知模式，需要进一步分析")


if __name__ == '__main__':
    # 测试
    analyzer = StockIntradayAnalyzer()
    result = analyzer.analyze_limit_up_pattern("002400", "2026-01-14")
    
    if result.get('success'):
        print("分析结果:")
        print(f"模式: {result['pattern']}")
        print(f"涨停次数: {result['limit_up_count']}")
        print(f"开板次数: {result['open_count']}")
        print(f"最大回调: {result['max_drawdown_pct']:.2f}%")
        
        print("\n解释:")
        print(analyzer.interpret_pattern(result))
    else:
        print(f"分析失败: {result.get('error')}")
