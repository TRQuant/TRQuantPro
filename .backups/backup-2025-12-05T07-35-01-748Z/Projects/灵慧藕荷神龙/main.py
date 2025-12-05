# -*- coding: utf-8 -*-
"""
灵慧藕荷神龙 - 多因子量化策略
=====================================

创建时间: 2025/12/3 16:28:57
回测区间: 2024-09-03 至 2025-09-03
基准指数: 000300.XSHG (沪深300)

策略说明:
本策略基于多因子选股模型
"""

def initialize(context):
    """策略初始化"""
    set_benchmark('000300.XSHG')
    g.stock_num = 10
    g.factor_weights = {
        'value': 0.25,
        'growth': 0.20,
        'quality': 0.25,
        'momentum': 0.20,
        'volatility': 0.10,
    }
    log.info('策略初始化完成: 灵慧藕荷神龙')

def handle_data(context, data):
    """每日执行"""
    pass
