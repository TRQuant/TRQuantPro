"""
股票池模拟数据

当真实数据源不可用时，提供模拟数据确保软件能正常运行
"""

import random
from datetime import datetime
from typing import List, Dict

# 模拟主线数据
MOCK_MAINLINES = [
    {"name": "人工智能", "total_score": 88.5, "leader_stock": "科大讯飞", "leader_change": 5.2},
    {"name": "新能源汽车", "total_score": 85.3, "leader_stock": "宁德时代", "leader_change": 3.8},
    {"name": "半导体", "total_score": 82.1, "leader_stock": "中芯国际", "leader_change": 4.5},
    {"name": "军工", "total_score": 80.7, "leader_stock": "中航沈飞", "leader_change": 6.1},
    {"name": "光伏", "total_score": 78.9, "leader_stock": "隆基绿能", "leader_change": 2.9},
    {"name": "医药生物", "total_score": 76.4, "leader_stock": "恒瑞医药", "leader_change": 1.8},
    {"name": "消费电子", "total_score": 74.2, "leader_stock": "立讯精密", "leader_change": 3.2},
    {"name": "储能", "total_score": 72.8, "leader_stock": "阳光电源", "leader_change": 4.7},
]

# 模拟股票数据
MOCK_STOCKS = [
    {"code": "002230", "name": "科大讯飞", "industry": "软件", "sector": "人工智能", "price": 45.6, "change_pct": 5.2, "market_cap": 1200},
    {"code": "300750", "name": "宁德时代", "industry": "电池", "sector": "新能源汽车", "price": 180.5, "change_pct": 3.8, "market_cap": 8500},
    {"code": "688981", "name": "中芯国际", "industry": "半导体", "sector": "半导体", "price": 52.3, "change_pct": 4.5, "market_cap": 4200},
    {"code": "600760", "name": "中航沈飞", "industry": "航空", "sector": "军工", "price": 48.7, "change_pct": 6.1, "market_cap": 1800},
    {"code": "601012", "name": "隆基绿能", "industry": "光伏", "sector": "光伏", "price": 23.4, "change_pct": 2.9, "market_cap": 1780},
    {"code": "600276", "name": "恒瑞医药", "industry": "医药", "sector": "医药生物", "price": 42.1, "change_pct": 1.8, "market_cap": 2680},
    {"code": "002475", "name": "立讯精密", "industry": "电子", "sector": "消费电子", "price": 28.9, "change_pct": 3.2, "market_cap": 2050},
    {"code": "300274", "name": "阳光电源", "industry": "电力设备", "sector": "储能", "price": 68.2, "change_pct": 4.7, "market_cap": 1020},
    {"code": "300059", "name": "东方财富", "industry": "金融", "sector": "互联网金融", "price": 15.8, "change_pct": 2.1, "market_cap": 2580},
    {"code": "002594", "name": "比亚迪", "industry": "汽车", "sector": "新能源汽车", "price": 265.0, "change_pct": 4.2, "market_cap": 7700},
    {"code": "600519", "name": "贵州茅台", "industry": "白酒", "sector": "消费", "price": 1680.0, "change_pct": 0.8, "market_cap": 21100},
    {"code": "000858", "name": "五粮液", "industry": "白酒", "sector": "消费", "price": 145.0, "change_pct": 1.2, "market_cap": 5630},
    {"code": "601318", "name": "中国平安", "industry": "保险", "sector": "金融", "price": 42.5, "change_pct": 0.5, "market_cap": 7750},
    {"code": "600036", "name": "招商银行", "industry": "银行", "sector": "金融", "price": 35.2, "change_pct": 0.3, "market_cap": 8880},
    {"code": "000651", "name": "格力电器", "industry": "家电", "sector": "消费", "price": 38.6, "change_pct": 1.5, "market_cap": 2180},
    {"code": "000333", "name": "美的集团", "industry": "家电", "sector": "消费", "price": 58.3, "change_pct": 1.8, "market_cap": 4070},
    {"code": "601899", "name": "紫金矿业", "industry": "有色金属", "sector": "周期", "price": 15.8, "change_pct": 3.5, "market_cap": 4160},
    {"code": "002415", "name": "海康威视", "industry": "安防", "sector": "科技", "price": 28.5, "change_pct": 2.3, "market_cap": 2670},
    {"code": "300124", "name": "汇川技术", "industry": "工控", "sector": "高端制造", "price": 62.4, "change_pct": 3.8, "market_cap": 1670},
    {"code": "002352", "name": "顺丰控股", "industry": "物流", "sector": "服务", "price": 35.2, "change_pct": 1.2, "market_cap": 1720},
]

# 模拟技术突破股
MOCK_TECH_BREAKOUT = [
    {"code": "300750", "name": "宁德时代", "signals": ["涨停", "放量3倍+"], "score": 55, "price": 180.5, "change_pct": 9.98},
    {"code": "002230", "name": "科大讯飞", "signals": ["大涨7%+", "放量2倍+"], "score": 45, "price": 45.6, "change_pct": 7.5},
    {"code": "688981", "name": "中芯国际", "signals": ["上涨5%+", "活跃换手"], "score": 35, "price": 52.3, "change_pct": 5.2},
    {"code": "600760", "name": "中航沈飞", "signals": ["大涨7%+", "放量3倍+"], "score": 50, "price": 48.7, "change_pct": 8.1},
    {"code": "002594", "name": "比亚迪", "signals": ["涨停", "放量2倍+", "活跃换手"], "score": 60, "price": 265.0, "change_pct": 9.95},
    {"code": "300274", "name": "阳光电源", "signals": ["上涨5%+", "放量2倍+"], "score": 40, "price": 68.2, "change_pct": 6.3},
    {"code": "601899", "name": "紫金矿业", "signals": ["大涨7%+", "活跃换手"], "score": 42, "price": 15.8, "change_pct": 7.8},
    {"code": "300124", "name": "汇川技术", "signals": ["上涨5%+", "放量2倍+"], "score": 38, "price": 62.4, "change_pct": 5.5},
]

# 模拟ETF数据
MOCK_ETFS = [
    {"code": "159915", "name": "创业板ETF", "type": "宽基ETF", "price": 2.35, "change_5d": 8.5, "change_20d": 15.2, "amount": 125.6, "index": "创业板指"},
    {"code": "510300", "name": "沪深300ETF", "type": "宽基ETF", "price": 4.12, "change_5d": 3.2, "change_20d": 8.5, "amount": 210.3, "index": "沪深300"},
    {"code": "512480", "name": "半导体ETF", "type": "主题ETF", "price": 1.28, "change_5d": 12.5, "change_20d": 22.3, "amount": 85.2, "index": "半导体"},
    {"code": "515790", "name": "光伏ETF", "type": "主题ETF", "price": 0.98, "change_5d": 10.2, "change_20d": 18.6, "amount": 62.8, "index": "光伏产业"},
    {"code": "512660", "name": "军工ETF", "type": "主题ETF", "price": 1.15, "change_5d": 9.8, "change_20d": 16.5, "amount": 78.5, "index": "军工指数"},
    {"code": "512010", "name": "医药ETF", "type": "行业ETF", "price": 0.68, "change_5d": 5.5, "change_20d": 12.3, "amount": 45.6, "index": "医药"},
    {"code": "512880", "name": "证券ETF", "type": "行业ETF", "price": 1.05, "change_5d": 6.8, "change_20d": 14.2, "amount": 156.8, "index": "证券"},
    {"code": "159949", "name": "创业板50ETF", "type": "宽基ETF", "price": 1.45, "change_5d": 7.2, "change_20d": 13.8, "amount": 38.5, "index": "创业板50"},
    {"code": "515050", "name": "5GETF", "type": "主题ETF", "price": 0.82, "change_5d": 8.5, "change_20d": 15.6, "amount": 28.5, "index": "5G通信"},
    {"code": "512690", "name": "酒ETF", "type": "行业ETF", "price": 1.32, "change_5d": 2.8, "change_20d": 6.5, "amount": 52.3, "index": "白酒"},
]


def get_mock_mainline_stocks(count: int = 20) -> List[Dict]:
    """获取模拟主线强势股"""
    result = []
    for i, stock in enumerate(MOCK_STOCKS[:count]):
        mainline = MOCK_MAINLINES[i % len(MOCK_MAINLINES)]
        result.append({
            "code": stock["code"],
            "name": stock["name"],
            "source": "mainline",
            "period": "medium",
            "priority": (i % 5) + 1,
            "mainline_score": mainline["total_score"] - random.uniform(0, 5),
            "change_pct": stock["change_pct"] + random.uniform(-1, 1),
            "entry_reason": f"主线强势股：{mainline['name']}，评分{mainline['total_score']:.1f}",
            "sector": mainline["name"],
        })
    return result


def get_mock_tech_stocks(count: int = 15) -> List[Dict]:
    """获取模拟技术突破股"""
    result = []
    for i, stock in enumerate(MOCK_TECH_BREAKOUT[:count]):
        result.append({
            "code": stock["code"],
            "name": stock["name"],
            "source": "tech_breakout",
            "period": "short",
            "priority": 3 if stock["score"] >= 50 else 4,
            "mainline_score": 0,
            "change_pct": stock["change_pct"],
            "entry_reason": f"技术突破：{', '.join(stock['signals'])}",
            "tech_signals": stock["signals"],
        })
    return result


def get_mock_etfs(count: int = 10) -> List[Dict]:
    """获取模拟ETF数据"""
    return MOCK_ETFS[:count]


def get_mock_external_stocks() -> List[Dict]:
    """获取模拟外部推荐股"""
    return [
        {"code": "600519", "name": "贵州茅台", "source": "broker", "reason": "中信证券月度金股，业绩稳定增长"},
        {"code": "000858", "name": "五粮液", "source": "broker", "reason": "华泰证券推荐，白酒龙头"},
        {"code": "601318", "name": "中国平安", "source": "gurufocus", "reason": "GuruFocus价值股，PE 8.5"},
        {"code": "600036", "name": "招商银行", "source": "gurufocus", "reason": "GuruFocus价值股，ROE 16.5%"},
    ]


def generate_progress_updates(total_steps: int = 10):
    """生成进度更新序列"""
    messages = [
        "初始化数据源...",
        "检查网络连接...",
        "加载主线识别结果...",
        "获取成分股数据...",
        "筛选强势股...",
        "计算技术指标...",
        "交叉验证...",
        "排序和去重...",
        "生成报告...",
        "完成！",
    ]
    for i, msg in enumerate(messages[:total_steps]):
        yield (i + 1) * 100 // total_steps, msg




