# -*- coding: utf-8 -*-
"""
投资主线发现引擎
================

通过分析新闻、市场数据、社交媒体等信息，
自动发现和追踪投资主线。
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from collections import Counter
import re
import logging

logger = logging.getLogger(__name__)


class ThemeDiscovery:
    """投资主线发现引擎"""
    
    # 预定义的主线关键词库
    THEME_KEYWORDS = {
        "AI人工智能": ["AI", "人工智能", "ChatGPT", "大模型", "AIGC", "算力", "GPU", "英伟达", "智能"],
        "新能源汽车": ["新能源", "电动车", "锂电池", "宁德时代", "比亚迪", "充电桩", "储能"],
        "光伏储能": ["光伏", "储能", "太阳能", "风电", "新能源发电", "逆变器"],
        "半导体芯片": ["半导体", "芯片", "晶圆", "光刻机", "封测", "国产替代", "华为"],
        "医药生物": ["医药", "生物", "创新药", "CXO", "医疗器械", "疫苗"],
        "消费复苏": ["消费", "白酒", "免税", "旅游", "餐饮", "复苏"],
        "数字经济": ["数字经济", "数据要素", "信创", "国产软件", "云计算"],
        "军工国防": ["军工", "国防", "航空", "航天", "导弹", "舰船"],
        "房地产": ["房地产", "地产", "楼市", "房企", "保交楼", "城中村"],
        "金融": ["银行", "保险", "券商", "金融", "降息", "降准"],
        "机器人": ["机器人", "人形机器人", "特斯拉", "减速器", "伺服"],
        "低空经济": ["低空", "无人机", "eVTOL", "飞行汽车"],
    }
    
    # 情绪关键词
    SENTIMENT_POSITIVE = ["利好", "上涨", "突破", "创新高", "放量", "涨停", "大涨", "强势"]
    SENTIMENT_NEGATIVE = ["利空", "下跌", "破位", "跌停", "大跌", "暴跌", "风险", "警惕"]
    
    def __init__(self, cache=None, data_manager=None):
        """
        初始化主线发现引擎
        
        Args:
            cache: MongoDB缓存管理器
            data_manager: 数据源管理器
        """
        self.cache = cache
        self.data_manager = data_manager
    
    def discover_themes(self, news_list: List[Dict] = None) -> List[Dict]:
        """
        发现投资主线
        
        Args:
            news_list: 新闻列表，如果为None则自动获取
            
        Returns:
            投资主线列表
        """
        # 1. 获取新闻数据
        if news_list is None and self.data_manager:
            news_list = self.data_manager.get_news(limit=100)
        
        if not news_list:
            logger.warning("没有新闻数据可供分析")
            return self._get_default_themes()
        
        # 2. 分析新闻，提取主线
        themes = self._analyze_news(news_list)
        
        # 3. 保存到缓存
        if self.cache:
            for theme in themes:
                self.cache.save_theme(theme)
        
        return themes
    
    def _analyze_news(self, news_list: List[Dict]) -> List[Dict]:
        """分析新闻提取主线"""
        # 统计主线关键词出现次数
        theme_counts = Counter()
        theme_news = {theme: [] for theme in self.THEME_KEYWORDS}
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = f"{title} {content}"
            
            for theme, keywords in self.THEME_KEYWORDS.items():
                for kw in keywords:
                    if kw in text:
                        theme_counts[theme] += 1
                        if len(theme_news[theme]) < 5:
                            theme_news[theme].append({
                                'title': title,
                                'time': news.get('publish_time', '')
                            })
                        break  # 一条新闻只计一次
        
        # 生成主线列表
        themes = []
        for theme, count in theme_counts.most_common(10):
            if count >= 2:  # 至少出现2次
                sentiment = self._analyze_sentiment(theme_news[theme])
                themes.append({
                    'name': theme,
                    'keywords': self.THEME_KEYWORDS[theme],
                    'heat_score': min(count * 10, 100),
                    'sentiment': sentiment,
                    'news_count': count,
                    'recent_news': theme_news[theme][:3],
                    'related_symbols': self._get_related_symbols(theme),
                    'investment_logic': self._get_investment_logic(theme),
                    'discovered_at': datetime.now().isoformat()
                })
        
        return themes
    
    def _analyze_sentiment(self, news_list: List[Dict]) -> str:
        """分析情绪"""
        positive = 0
        negative = 0
        
        for news in news_list:
            title = news.get('title', '')
            for word in self.SENTIMENT_POSITIVE:
                if word in title:
                    positive += 1
            for word in self.SENTIMENT_NEGATIVE:
                if word in title:
                    negative += 1
        
        if positive > negative:
            return "positive"
        elif negative > positive:
            return "negative"
        else:
            return "neutral"
    
    def _get_related_symbols(self, theme: str) -> List[str]:
        """获取主线相关股票"""
        # 预定义的主线-股票映射
        THEME_STOCKS = {
            "AI人工智能": ["002230.XSHE", "300474.XSHE", "688787.XSHG"],  # 科大讯飞、景嘉微、海光信息
            "新能源汽车": ["300750.XSHE", "002594.XSHE", "601238.XSHG"],  # 宁德时代、比亚迪、广汽集团
            "光伏储能": ["601012.XSHG", "002459.XSHE", "300274.XSHE"],    # 隆基绿能、晶澳科技、阳光电源
            "半导体芯片": ["688981.XSHG", "002371.XSHE", "603501.XSHG"],  # 中芯国际、北方华创、韦尔股份
            "医药生物": ["600276.XSHG", "000858.XSHE", "300760.XSHE"],    # 恒瑞医药、五粮液、迈瑞医疗
            "消费复苏": ["600519.XSHG", "000858.XSHE", "601888.XSHG"],    # 贵州茅台、五粮液、中国中免
            "数字经济": ["000977.XSHE", "600845.XSHG", "002415.XSHE"],    # 浪潮信息、宝信软件、海康威视
            "军工国防": ["600893.XSHG", "000768.XSHE", "600760.XSHG"],    # 航发动力、中航西飞、中航沈飞
            "机器人": ["300124.XSHE", "002747.XSHE", "688772.XSHG"],      # 汇川技术、埃斯顿、珞石科技
            "低空经济": ["002097.XSHE", "300034.XSHE", "688122.XSHG"],    # 山河智能、钢研高纳、西部超导
        }
        
        return THEME_STOCKS.get(theme, [])
    
    def _get_investment_logic(self, theme: str) -> str:
        """获取投资逻辑"""
        THEME_LOGIC = {
            "AI人工智能": "AI大模型持续迭代，算力需求爆发，应用场景逐步落地，关注算力基础设施、模型厂商、应用端公司。",
            "新能源汽车": "渗透率持续提升，产业链降本增效，关注电池、整车、充电桩等环节龙头。",
            "光伏储能": "碳中和政策驱动，装机量持续增长，关注组件、逆变器、储能系统龙头。",
            "半导体芯片": "国产替代加速，设备材料突破，关注设计、制造、封测、设备材料全产业链。",
            "医药生物": "创新药出海，医疗新基建，关注创新药、CXO、医疗器械龙头。",
            "消费复苏": "经济复苏带动消费回暖，关注高端白酒、免税、旅游等可选消费。",
            "数字经济": "数据要素政策落地，信创持续推进，关注数据运营、国产软件、云计算。",
            "军工国防": "国防预算增长，装备升级换代，关注航空航天、导弹、舰船等主机厂。",
            "机器人": "人形机器人产业化临近，关注减速器、伺服、传感器等核心零部件。",
            "低空经济": "政策支持，应用场景丰富，关注无人机、eVTOL、空管系统等。",
        }
        
        return THEME_LOGIC.get(theme, "关注行业龙头，把握结构性机会。")
    
    def _get_default_themes(self) -> List[Dict]:
        """获取默认主线（无新闻时使用）"""
        default_themes = ["AI人工智能", "新能源汽车", "半导体芯片", "消费复苏", "机器人"]
        
        themes = []
        for theme in default_themes:
            themes.append({
                'name': theme,
                'keywords': self.THEME_KEYWORDS.get(theme, []),
                'heat_score': 50,
                'sentiment': 'neutral',
                'news_count': 0,
                'recent_news': [],
                'related_symbols': self._get_related_symbols(theme),
                'investment_logic': self._get_investment_logic(theme),
                'discovered_at': datetime.now().isoformat()
            })
        
        return themes
    
    def get_theme_detail(self, theme_name: str) -> Optional[Dict]:
        """获取主线详情"""
        if self.cache:
            return self.cache.get_theme_by_name(theme_name)
        return None
    
    def update_theme_heat(self, theme_name: str, heat_delta: int = 10):
        """更新主线热度"""
        if self.cache:
            theme = self.cache.get_theme_by_name(theme_name)
            if theme:
                new_heat = min(100, max(0, theme.get('heat_score', 50) + heat_delta))
                self.cache.update_theme_heat(theme_name, new_heat)
    
    def generate_theme_strategy(self, theme: Dict) -> str:
        """
        基于主线生成策略代码框架
        
        Args:
            theme: 主线信息
            
        Returns:
            PTrade策略代码
        """
        symbols = theme.get('related_symbols', [])
        theme_name = theme.get('name', '未知主线')
        logic = theme.get('investment_logic', '')
        
        code = f'''# -*- coding: utf-8 -*-
"""
{theme_name}主题策略
==================

投资逻辑：{logic}

相关标的：{', '.join(symbols[:5])}
"""

# ============================================================
# 策略参数
# ============================================================
THEME_NAME = "{theme_name}"
STOCK_POOL = {symbols[:10]}  # 主线相关股票

# 持仓参数
MAX_HOLD = 5          # 最大持仓数
POSITION_PCT = 0.18   # 单只仓位上限

# 买入条件参数
BUY_MA_SHORT = 5      # 短期均线
BUY_MA_LONG = 20      # 长期均线
BUY_VOLUME_RATIO = 1.5  # 放量倍数

# 卖出条件参数
STOP_LOSS = -0.08     # 止损比例
TAKE_PROFIT = 0.20    # 止盈比例
TRAILING_STOP = 0.05  # 移动止损

# ============================================================
# 初始化
# ============================================================
def initialize(context):
    """策略初始化"""
    log.info("=" * 50)
    log.info(f"{{THEME_NAME}}主题策略初始化")
    log.info(f"股票池: {{len(STOCK_POOL)}}只")
    log.info("=" * 50)
    
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点和手续费
    set_slippage(FixedSlippage(0.02))
    set_commission(PerShare(cost=0.0003, min_cost=5))
    
    # 定时任务
    run_daily(market_open, time='09:30')
    run_daily(check_positions, time='14:30')

# ============================================================
# 盘前选股
# ============================================================
def market_open(context):
    """盘前选股"""
    # 获取当前持仓
    current_holds = list(context.portfolio.positions.keys())
    
    # 筛选符合条件的股票
    buy_list = []
    for stock in STOCK_POOL:
        if stock in current_holds:
            continue
        
        # 获取历史数据
        df = get_price(stock, count=BUY_MA_LONG + 5, 
                       fields=['close', 'volume'])
        if df is None or len(df) < BUY_MA_LONG:
            continue
        
        # 计算指标
        close = df['close']
        volume = df['volume']
        ma_short = close.rolling(BUY_MA_SHORT).mean()
        ma_long = close.rolling(BUY_MA_LONG).mean()
        vol_ma = volume.rolling(5).mean()
        
        # 买入条件：短期均线上穿长期均线 + 放量
        if (ma_short.iloc[-1] > ma_long.iloc[-1] and 
            ma_short.iloc[-2] <= ma_long.iloc[-2] and
            volume.iloc[-1] > vol_ma.iloc[-1] * BUY_VOLUME_RATIO):
            buy_list.append(stock)
    
    # 执行买入
    available_slots = MAX_HOLD - len(current_holds)
    for stock in buy_list[:available_slots]:
        cash = context.portfolio.available_cash
        price = get_current_data()[stock].last_price
        amount = int(cash * POSITION_PCT / price / 100) * 100
        if amount >= 100:
            order(stock, amount)
            log.info(f"买入 {{stock}} {{amount}}股")

# ============================================================
# 持仓检查
# ============================================================
def check_positions(context):
    """检查持仓，执行止盈止损"""
    for stock, position in context.portfolio.positions.items():
        if position.total_amount == 0:
            continue
        
        # 计算盈亏比例
        cost = position.avg_cost
        current = get_current_data()[stock].last_price
        pnl_ratio = (current - cost) / cost
        
        # 止损
        if pnl_ratio <= STOP_LOSS:
            order_target(stock, 0)
            log.info(f"止损卖出 {{stock}}, 亏损 {{pnl_ratio:.2%}}")
        
        # 止盈
        elif pnl_ratio >= TAKE_PROFIT:
            order_target(stock, 0)
            log.info(f"止盈卖出 {{stock}}, 盈利 {{pnl_ratio:.2%}}")

# ============================================================
# 每日收盘后
# ============================================================
def after_trading_end(context):
    """收盘后处理"""
    log.info(f"今日收益: {{context.portfolio.returns:.2%}}")
    log.info(f"持仓: {{list(context.portfolio.positions.keys())}}")
'''
        
        return code





