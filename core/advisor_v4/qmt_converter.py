#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QMT策略转换器 - 将BulletTrade/聚宽策略转换为QMT代码

QMT特点:
- 迅投科技提供的量化交易平台
- 使用本地数据（xtdata）
- 事件驱动的回调机制
- 需要手动创建交易对象

主要转换:
1. 股票代码格式
2. 数据获取API (get_price → xtdata.get_market_data)
3. 订单API (order → xt_trader.order_stock)
4. 回调函数 (initialize → on_init)
5. 定时任务需要外部调度器
"""

from __future__ import annotations

import logging
import re
from typing import Dict

from .strategy_converter import StrategyConverter, ConversionResult

logger = logging.getLogger(__name__)


class QMTConverter(StrategyConverter):
    """BulletTrade/聚宽 → QMT 策略转换器"""
    
    # 函数名映射
    FUNCTION_MAPPING = {
        'initialize': 'on_init',
        'before_trading_start': 'before_market_open',
        'after_trading_end': 'after_market_close',
        'handle_data': 'on_data',
    }
    
    # 属性映射
    ATTRIBUTE_MAPPING = {
        'total_value': 'market_value',
        'total_amount': 'total_qty',
        'avg_cost': 'cost_price',
    }
    
    @property
    def target_platform(self) -> str:
        return "QMT"
    
    @property
    def source_platform(self) -> str:
        return "BulletTrade/聚宽"
    
    def _convert_imports(self, code: str) -> str:
        """转换导入语句"""
        result = code
        
        # 移除聚宽特有的导入
        jq_imports = [
            r'from jqdata import \*',
            r'import jqdatasdk.*',
            r'from jqdatasdk import.*',
        ]
        for pattern in jq_imports:
            if re.search(pattern, result):
                self.converted_items['imports'] += 1
                result = re.sub(pattern, '# ' + pattern.replace(r'\*', '*'), result)
                self._add_warning(f"注释掉聚宽导入: {pattern}")
        
        return result
    
    def _convert_function_calls(self, code: str) -> str:
        """转换函数调用（增强版，处理QMT特殊API）"""
        result = super()._convert_function_calls(code)
        
        # 特殊处理: get_price → xtdata.get_market_data
        if 'get_price' in result:
            self._add_warning("get_price需要转换为xtdata.get_market_data，参数格式完全不同")
            result = result.replace('get_price', 'xtdata.get_market_data')
        
        # 特殊处理: order系列函数
        order_funcs = ['order', 'order_value', 'order_target', 'order_target_value']
        for func in order_funcs:
            if func in result and 'xt_trader' not in result:
                self._add_warning(f"{func}需要转换为xt_trader.order_stock，参数格式不同")
        
        # 特殊处理: get_fundamentals
        if 'get_fundamentals' in result:
            self._add_warning("get_fundamentals需要转换为xtdata.get_financial_data")
            result = result.replace('get_fundamentals', 'xtdata.get_financial_data')
        
        return result
    
    def _add_platform_specific_code(self, code: str) -> str:
        """添加QMT平台特定代码"""
        
        # QMT头部模板
        header = '''# -*- coding: utf-8 -*-
"""
策略已转换为QMT平台格式
原始平台: BulletTrade/聚宽
转换时间: 自动生成

QMT使用说明:
1. 需要安装xtquant库: pip install xtquant
2. 需要配置交易账户
3. 需要下载历史数据
4. 定时任务需要使用schedule库

注意事项:
- 股票代码已转换为.SH/.SZ格式
- 订单API需要使用xt_trader对象
- 数据API需要使用xtdata模块
"""

'''
        
        # QMT导入和初始化模板
        qmt_imports = '''
# QMT平台导入
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# QMT核心模块
try:
    from xtquant import xttrader, xtdata
    from xtquant import xtconstant
except ImportError:
    print("警告: xtquant未安装，请运行 pip install xtquant")
    xttrader = None
    xtdata = None
    xtconstant = None

# 定时任务调度
try:
    import schedule
except ImportError:
    print("警告: schedule未安装，请运行 pip install schedule")
    schedule = None

# ==================== QMT交易初始化 ====================
# 请根据实际情况配置以下参数
QMT_PATH = r"D:\\国金证券QMT交易端\\userdata_mini"  # QMT路径
SESSION_ID = 123456  # 会话ID
ACCOUNT_ID = "your_account_id"  # 账户ID

# 全局交易对象（在策略启动时初始化）
xt_trader = None
account = None

def init_qmt_trader():
    """初始化QMT交易对象"""
    global xt_trader, account
    if xttrader is None:
        print("错误: xtquant未安装")
        return False
    
    try:
        xt_trader = xttrader.XtQuantTrader(QMT_PATH, SESSION_ID)
        xt_trader.start()
        
        account = xttrader.StockAccount(ACCOUNT_ID)
        xt_trader.subscribe(account)
        
        print("QMT交易对象初始化成功")
        return True
    except Exception as e:
        print(f"QMT初始化失败: {e}")
        return False

# ==================== QMT回调类 ====================
class QMTCallback(xttrader.XtQuantTraderCallback):
    """QMT交易回调"""
    
    def on_order_callback(self, order):
        """订单状态回调"""
        print(f"订单回调: {order.stock_code}, 状态: {order.order_status}")
    
    def on_deal_callback(self, deal):
        """成交回调"""
        print(f"成交回调: {deal.stock_code}, 数量: {deal.traded_qty}")
    
    def on_account_callback(self, account):
        """账户变化回调"""
        print(f"账户回调: {account.account_id}")

'''
        
        # 添加辅助函数
        helper_functions = '''
# ==================== 聚宽API兼容层 ====================
def get_price_compat(security, start_date=None, end_date=None, count=None, frequency='daily', fields=None, panel=False, fq='post'):
    """get_price兼容函数，转换为xtdata.get_market_data"""
    if xtdata is None:
        return None
    
    # 转换股票代码
    if isinstance(security, list):
        stock_list = [s.replace('.XSHG', '.SH').replace('.XSHE', '.SZ') for s in security]
    else:
        stock_list = [security.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')]
    
    # 转换周期
    period_map = {'daily': '1d', '1d': '1d', 'minute': '1m', '1m': '1m'}
    period = period_map.get(frequency, '1d')
    
    # 转换日期格式
    if start_date:
        start_time = start_date.replace('-', '')
    else:
        start_time = ''
    if end_date:
        end_time = end_date.replace('-', '')
    else:
        end_time = ''
    
    # 转换字段
    field_list = fields or ['open', 'high', 'low', 'close', 'volume']
    
    try:
        data = xtdata.get_market_data(
            field_list=field_list,
            stock_list=stock_list,
            period=period,
            start_time=start_time,
            end_time=end_time,
            count=count or -1
        )
        return data
    except Exception as e:
        print(f"获取行情数据失败: {e}")
        return None

def order_compat(security, amount, price=0, order_type='market'):
    """order兼容函数，转换为xt_trader.order_stock"""
    global xt_trader, account
    if xt_trader is None or account is None:
        print("错误: QMT交易对象未初始化")
        return None
    
    # 转换股票代码
    stock_code = security.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
    
    # 确定买卖方向
    if amount > 0:
        direction = xtconstant.STOCK_BUY
    else:
        direction = xtconstant.STOCK_SELL
        amount = abs(amount)
    
    # 确定价格类型
    if order_type == 'market' or price == 0:
        price_type = xtconstant.LATEST_PRICE
        order_price = 0
    else:
        price_type = xtconstant.FIX_PRICE
        order_price = price
    
    try:
        order_id = xt_trader.order_stock(
            account,
            stock_code,
            direction,
            int(amount),
            price_type,
            order_price
        )
        return order_id
    except Exception as e:
        print(f"下单失败: {e}")
        return None

'''
        
        # 组合最终代码
        result = header + qmt_imports + helper_functions + '\n# ==================== 原策略代码 ====================\n' + code
        
        return result
    
    def _post_process(self, code: str) -> str:
        """后处理"""
        result = code
        
        # 移除run_daily/run_weekly（QMT不支持，需要使用schedule）
        if 'run_daily' in result:
            self._add_warning("QMT不支持run_daily，已注释。请使用schedule库实现定时任务")
            result = re.sub(r'run_daily\([^)]+\)', '# run_daily(...) # QMT不支持，请使用schedule', result)
        
        if 'run_weekly' in result:
            self._add_warning("QMT不支持run_weekly，已注释。请使用schedule库实现定时任务")
            result = re.sub(r'run_weekly\([^)]+\)', '# run_weekly(...) # QMT不支持，请使用schedule', result)
        
        # 添加定时任务示例
        if 'schedule' not in result and ('run_daily' in code or 'run_weekly' in code):
            schedule_example = '''
# ==================== 定时任务示例 ====================
# 使用schedule库实现定时任务
# schedule.every().day.at("09:30").do(your_function)
# schedule.every().monday.at("09:30").do(your_function)
# 
# 主循环中运行:
# while True:
#     schedule.run_pending()
#     time.sleep(1)
'''
            result = result + schedule_example
        
        return result


def convert_to_qmt(source_code: str, verbose: bool = True) -> ConversionResult:
    """
    便捷函数：将BulletTrade/聚宽策略转换为QMT格式
    
    Args:
        source_code: 源策略代码
        verbose: 是否输出详细信息
        
    Returns:
        转换结果
    """
    converter = QMTConverter(verbose=verbose)
    return converter.convert(source_code)


# 测试代码
if __name__ == '__main__':
    # 测试代码
    test_code = '''
from jqdata import *

def initialize(context):
    g.stock_pool = get_index_stocks('000300.XSHG')
    run_daily(check_stocks, time='09:30')

def check_stocks(context):
    prices = get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-01-31')
    if context.portfolio.positions['000001.XSHE'].total_value > 10000:
        order('000001.XSHE', -100)
'''
    
    result = convert_to_qmt(test_code)
    print("=" * 60)
    print(f"转换成功: {result.success}")
    print(f"警告数: {len(result.warnings)}")
    print(f"错误数: {len(result.errors)}")
    print(f"转换统计: {result.converted_items}")
    print("=" * 60)
    print("警告信息:")
    for w in result.warnings:
        print(f"  - {w}")
    print("=" * 60)
    print("转换后代码前500字符:")
    print(result.target_code[:500])
