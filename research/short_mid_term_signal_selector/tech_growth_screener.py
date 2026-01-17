"""
科技高成长股票筛选系统
=====================================
目标：识别科技主线板块中的高成长股票
策略：早期布局 + 趋势跟随 + 波段操作

核心逻辑：
1. 聚焦科技主线板块（半导体、AI、新能源、脑机接口等）
2. 高成长性识别（利润增速、营收增速、ROE提升）
3. 趋势确认（价格趋势、量价配合）
4. 波段信号（超买超卖、支撑阻力）
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# JQData
from jqdatasdk import (
    auth, get_price, get_fundamentals, query, valuation, 
    indicator, income, balance, get_concept_stocks, 
    get_all_securities, get_trade_days, normalize_code
)


class GrowthStage(Enum):
    """成长阶段"""
    EARLY = "早期布局"      # 业绩拐点，尚未被市场发现
    GROWTH = "成长期"       # 业绩高速增长，股价跟随
    ACCELERATION = "加速期"  # 业绩加速，主升浪
    MATURE = "成熟期"       # 增速放缓，估值消化
    DECLINE = "衰退期"      # 业绩下滑


class TrendPhase(Enum):
    """趋势阶段"""
    BOTTOM = "底部整理"
    BREAKOUT = "突破启动"
    UPTREND = "上升趋势"
    ACCELERATION = "加速上涨"
    TOP = "顶部区域"
    DOWNTREND = "下降趋势"


@dataclass
class StockAnalysis:
    """股票分析结果"""
    code: str
    name: str
    sector: str
    current_price: float
    
    # 成长性指标
    revenue_growth: float      # 营收增速
    profit_growth: float       # 利润增速
    roe: float                 # ROE
    roe_trend: str            # ROE趋势
    
    # 估值指标
    pe: float
    pb: float
    peg: float
    
    # 趋势指标
    trend_phase: TrendPhase
    trend_score: float         # 趋势得分 0-100
    ma_position: str          # 均线位置
    
    # 量价指标
    volume_ratio: float        # 量比
    turnover_rate: float       # 换手率
    
    # 波段信号
    swing_signal: str          # BUY/HOLD/SELL
    support_price: float       # 支撑位
    resistance_price: float    # 阻力位
    
    # 综合评分
    growth_score: float        # 成长得分 0-100
    total_score: float         # 综合得分 0-100
    growth_stage: GrowthStage
    
    # 推荐
    recommendation: str
    reason: str
    target_price: float
    stop_loss: float
    position_pct: float        # 建议仓位


class TechGrowthScreener:
    """科技高成长股票筛选器"""
    
    # 科技主线板块定义
    TECH_SECTORS = {
        '半导体芯片': {
            'concepts': ['SC0079', 'SC0194', 'SC0050', 'SC0095'],  # 芯片、集成电路、半导体设备
            'keywords': ['芯片', '半导体', '集成电路', 'IC设计', '封测', '晶圆'],
            'weight': 1.2  # 权重系数
        },
        '人工智能': {
            'concepts': ['SC0010', 'SC0377', 'SC0371'],  # AI、机器人、大模型
            'keywords': ['人工智能', 'AI', '机器学习', '深度学习', '大模型', 'GPT'],
            'weight': 1.2
        },
        '新能源电池': {
            'concepts': ['SC0038', 'SC0160', 'SC0340'],  # 锂电池、储能、固态电池
            'keywords': ['锂电池', '储能', '固态电池', '钠电池', '电池材料'],
            'weight': 1.1
        },
        '光伏储能': {
            'concepts': ['SC0046', 'SC0160'],  # 光伏、储能
            'keywords': ['光伏', '太阳能', '储能', '逆变器', '组件'],
            'weight': 1.0
        },
        '脑机接口': {
            'concepts': ['SC0430'],  # 脑机接口
            'keywords': ['脑机接口', '神经科学', '脑电'],
            'weight': 1.3  # 新兴领域高权重
        },
        '人形机器人': {
            'concepts': ['SC0377', 'SC0372'],  # 机器人、人形机器人
            'keywords': ['人形机器人', '机器人', '伺服电机', '减速器', '传感器'],
            'weight': 1.2
        },
        '新材料': {
            'concepts': ['SC0049', 'SC0159'],  # 新材料
            'keywords': ['新材料', '碳纤维', '石墨烯', '稀土', '特种材料'],
            'weight': 1.0
        }
    }
    
    # 高成长筛选标准 - 适度放宽以适应当前市场环境
    # 注意：JQData返回的market_cap单位是亿元
    GROWTH_CRITERIA = {
        'min_revenue_growth': 5,      # 最低营收增速（放宽）
        'min_profit_growth': 10,      # 最低利润增速（放宽）
        'min_roe': 0,                 # 最低ROE（大幅放宽，允许暂时亏损的高成长股）
        'max_pe': 200,                # 最高PE（高成长可以接受较高估值）
        'max_pb': 30,                 # 最高PB
        'min_market_cap': 30,         # 最低市值30亿（单位：亿）
        'max_market_cap': 5000,       # 最高市值5000亿（单位：亿）
    }
    
    def __init__(self, auth_params: Dict[str, str] = None):
        """初始化"""
        if auth_params:
            try:
                auth(auth_params['username'], auth_params['password'])
                print("✅ JQData 已连接")
            except Exception as e:
                print(f"❌ JQData 连接失败: {e}")
        
        self.analysis_date = datetime.now().strftime('%Y-%m-%d')
        self.candidates = []
        self.final_selection = []
    
    def screen(self, top_n: int = 5, date: str = None) -> pd.DataFrame:
        """
        执行筛选流程
        
        Args:
            top_n: 最终选股数量
            date: 分析日期
        
        Returns:
            筛选结果DataFrame
        """
        if date:
            self.analysis_date = date
        
        print(f"\n{'='*70}")
        print(f"🔍 科技高成长股票筛选系统")
        print(f"📅 分析日期: {self.analysis_date}")
        print(f"{'='*70}")
        
        # Step 1: 获取科技板块候选池
        print("\n📊 Step 1: 构建科技板块候选池...")
        candidates = self._get_tech_universe()
        print(f"   候选池规模: {len(candidates)} 只")
        
        if not candidates:
            print("❌ 未找到符合条件的候选股票")
            return pd.DataFrame()
        
        # Step 2: 财务筛选（高成长）
        print("\n📈 Step 2: 财务高成长筛选...")
        growth_stocks = self._filter_high_growth(candidates)
        print(f"   高成长股票: {len(growth_stocks)} 只")
        
        if not growth_stocks:
            print("❌ 未找到符合成长标准的股票")
            return pd.DataFrame()
        
        # Step 3: 技术分析（趋势+波段）
        print("\n📉 Step 3: 技术趋势分析...")
        analyzed_stocks = self._analyze_technicals(growth_stocks)
        print(f"   技术分析完成: {len(analyzed_stocks)} 只")
        
        # Step 4: 综合评分排序
        print("\n🎯 Step 4: 综合评分排序...")
        scored_stocks = self._calculate_scores(analyzed_stocks)
        
        # Step 5: 最终选股
        print(f"\n🏆 Step 5: 最终选股 (Top {top_n})...")
        self.final_selection = self._select_final(scored_stocks, top_n)
        
        # 生成结果DataFrame
        result_df = self._to_dataframe(self.final_selection)
        
        print(f"\n{'='*70}")
        print(f"✅ 筛选完成! 选出 {len(result_df)} 只科技高成长股票")
        print(f"{'='*70}")
        
        return result_df
    
    def _get_tech_universe(self) -> List[str]:
        """获取科技板块股票池"""
        all_stocks = set()
        
        for sector_name, sector_info in self.TECH_SECTORS.items():
            sector_stocks = set()
            
            # 通过概念代码获取
            for concept_code in sector_info.get('concepts', []):
                try:
                    stocks = get_concept_stocks(concept_code)
                    if stocks:
                        sector_stocks.update(stocks)
                except Exception as e:
                    pass
            
            print(f"   {sector_name}: {len(sector_stocks)} 只")
            all_stocks.update(sector_stocks)
        
        # 过滤ST、退市等
        filtered_stocks = []
        all_securities = get_all_securities('stock')
        
        for code in all_stocks:
            if code in all_securities.index:
                name = all_securities.loc[code, 'display_name']
                if 'ST' not in name and '退' not in name:
                    filtered_stocks.append(code)
        
        return filtered_stocks
    
    def _filter_high_growth(self, candidates: List[str]) -> List[Dict]:
        """筛选高成长股票"""
        growth_stocks = []
        
        # 分批查询财务数据
        batch_size = 100
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i+batch_size]
            
            try:
                # 查询估值数据
                q_val = query(
                    valuation.code,
                    valuation.market_cap,
                    valuation.pe_ratio,
                    valuation.pb_ratio,
                    valuation.turnover_ratio
                ).filter(
                    valuation.code.in_(batch)
                )
                df_val = get_fundamentals(q_val, date=self.analysis_date)
                
                # 查询盈利指标
                q_indicator = query(
                    indicator.code,
                    indicator.roe,
                    indicator.inc_revenue_year_on_year,
                    indicator.inc_net_profit_year_on_year,
                    indicator.inc_operation_profit_year_on_year
                ).filter(
                    indicator.code.in_(batch)
                )
                df_ind = get_fundamentals(q_indicator, date=self.analysis_date)
                
                if df_val.empty or df_ind.empty:
                    continue
                
                # 合并数据
                df = df_val.merge(df_ind, on='code', how='inner')
                
                # 应用筛选条件
                for _, row in df.iterrows():
                    try:
                        # 市值筛选 (JQData市值单位是亿元)
                        market_cap = row['market_cap'] if pd.notna(row['market_cap']) else 0
                        if market_cap < self.GROWTH_CRITERIA['min_market_cap']:
                            continue
                        if market_cap > self.GROWTH_CRITERIA['max_market_cap']:
                            continue
                        
                        # PE筛选（允许负PE的高成长股）
                        pe = row['pe_ratio'] if pd.notna(row['pe_ratio']) else 50
                        if pe > self.GROWTH_CRITERIA['max_pe']:
                            continue
                        
                        # 利润增速筛选（允许负增速，但优先选择正增速）
                        profit_growth = row['inc_net_profit_year_on_year'] if pd.notna(row['inc_net_profit_year_on_year']) else 0
                        revenue_growth = row['inc_revenue_year_on_year'] if pd.notna(row['inc_revenue_year_on_year']) else 0
                        
                        # 至少满足一个成长条件：利润增速>10% 或 营收增速>20%
                        if profit_growth < self.GROWTH_CRITERIA['min_profit_growth'] and revenue_growth < 20:
                            continue
                        
                        # ROE筛选（放宽）
                        roe = row['roe'] if pd.notna(row['roe']) else 0
                        if roe < self.GROWTH_CRITERIA['min_roe'] and profit_growth < 50:
                            # ROE低但高增长的保留
                            continue
                        
                        # 通过筛选
                        growth_stocks.append({
                            'code': row['code'],
                            'market_cap': market_cap,
                            'pe': pe,
                            'pb': row['pb_ratio'] if pd.notna(row['pb_ratio']) else 0,
                            'roe': roe,
                            'revenue_growth': row['inc_revenue_year_on_year'] if pd.notna(row['inc_revenue_year_on_year']) else 0,
                            'profit_growth': profit_growth,
                            'turnover_ratio': row['turnover_ratio'] if pd.notna(row['turnover_ratio']) else 0
                        })
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"   查询失败: {e}")
                continue
        
        return growth_stocks
    
    def _analyze_technicals(self, growth_stocks: List[Dict]) -> List[Dict]:
        """技术分析"""
        analyzed = []
        all_securities = get_all_securities('stock')
        
        for stock in growth_stocks:
            code = stock['code']
            
            try:
                # 获取价格数据（60天）
                end_date = self.analysis_date
                start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')
                
                df_price = get_price(
                    code,
                    start_date=start_date,
                    end_date=end_date,
                    fields=['open', 'high', 'low', 'close', 'volume', 'money']
                )
                
                if df_price.empty or len(df_price) < 20:
                    continue
                
                # 计算技术指标
                close = df_price['close']
                volume = df_price['volume']
                
                # 均线
                ma5 = close.rolling(5).mean()
                ma10 = close.rolling(10).mean()
                ma20 = close.rolling(20).mean()
                ma60 = close.rolling(60).mean() if len(close) >= 60 else close.rolling(len(close)).mean()
                
                current_price = close.iloc[-1]
                
                # 均线位置判断
                ma_position = "多头排列"
                if ma5.iloc[-1] < ma10.iloc[-1]:
                    ma_position = "短期调整"
                if ma10.iloc[-1] < ma20.iloc[-1]:
                    ma_position = "中期调整"
                if ma20.iloc[-1] < ma60.iloc[-1]:
                    ma_position = "空头排列"
                
                # 趋势阶段判断
                trend_phase = self._determine_trend_phase(df_price)
                
                # 趋势得分
                trend_score = self._calculate_trend_score(df_price, ma5, ma10, ma20, ma60)
                
                # 量比
                avg_volume_5 = volume.tail(5).mean()
                avg_volume_20 = volume.tail(20).mean()
                volume_ratio = avg_volume_5 / avg_volume_20 if avg_volume_20 > 0 else 1
                
                # 支撑阻力
                support = min(close.tail(20).min(), ma20.iloc[-1] if pd.notna(ma20.iloc[-1]) else close.tail(20).min())
                resistance = max(close.tail(20).max(), current_price * 1.15)
                
                # 波段信号
                swing_signal = self._generate_swing_signal(df_price, ma5, ma10, ma20)
                
                # 识别所属板块
                sector = self._identify_sector(code)
                
                # 获取股票名称
                name = all_securities.loc[code, 'display_name'] if code in all_securities.index else code
                
                # 成长阶段
                growth_stage = self._determine_growth_stage(stock, trend_phase)
                
                analyzed.append({
                    **stock,
                    'name': name,
                    'sector': sector,
                    'current_price': current_price,
                    'trend_phase': trend_phase,
                    'trend_score': trend_score,
                    'ma_position': ma_position,
                    'volume_ratio': volume_ratio,
                    'swing_signal': swing_signal,
                    'support_price': support,
                    'resistance_price': resistance,
                    'growth_stage': growth_stage
                })
                
            except Exception as e:
                continue
        
        return analyzed
    
    def _determine_trend_phase(self, df_price: pd.DataFrame) -> TrendPhase:
        """判断趋势阶段"""
        close = df_price['close']
        
        if len(close) < 20:
            return TrendPhase.BOTTOM
        
        # 计算涨跌幅
        change_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100
        change_5d = (close.iloc[-1] / close.iloc[-5] - 1) * 100
        
        # 计算新高新低
        high_20d = close.tail(20).max()
        low_20d = close.tail(20).min()
        
        is_near_high = close.iloc[-1] >= high_20d * 0.95
        is_near_low = close.iloc[-1] <= low_20d * 1.05
        
        if is_near_low and change_20d < 5:
            return TrendPhase.BOTTOM
        elif change_5d > 5 and change_20d > 10:
            if change_5d > 10:
                return TrendPhase.ACCELERATION
            return TrendPhase.UPTREND
        elif is_near_high and change_5d < 0:
            return TrendPhase.TOP
        elif change_20d < -10:
            return TrendPhase.DOWNTREND
        elif change_20d > 5:
            return TrendPhase.BREAKOUT
        else:
            return TrendPhase.BOTTOM
    
    def _calculate_trend_score(self, df_price, ma5, ma10, ma20, ma60) -> float:
        """计算趋势得分"""
        score = 50  # 基准分
        
        close = df_price['close']
        current = close.iloc[-1]
        
        # 均线多头排列加分
        if current > ma5.iloc[-1] > ma10.iloc[-1] > ma20.iloc[-1]:
            score += 20
        elif current > ma5.iloc[-1] > ma10.iloc[-1]:
            score += 10
        elif current > ma5.iloc[-1]:
            score += 5
        
        # 在60日均线上方加分
        if pd.notna(ma60.iloc[-1]) and current > ma60.iloc[-1]:
            score += 10
        
        # 20日涨幅
        if len(close) >= 20:
            change_20d = (current / close.iloc[-20] - 1) * 100
            if change_20d > 20:
                score += 15
            elif change_20d > 10:
                score += 10
            elif change_20d > 0:
                score += 5
            elif change_20d < -10:
                score -= 15
        
        return min(max(score, 0), 100)
    
    def _generate_swing_signal(self, df_price, ma5, ma10, ma20) -> str:
        """生成波段信号"""
        close = df_price['close']
        current = close.iloc[-1]
        
        # RSI计算
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if pd.notna(rsi.iloc[-1]) else 50
        
        # 均线金叉/死叉
        ma5_cross_ma10 = ma5.iloc[-1] > ma10.iloc[-1] and ma5.iloc[-2] < ma10.iloc[-2]
        ma5_death_ma10 = ma5.iloc[-1] < ma10.iloc[-1] and ma5.iloc[-2] > ma10.iloc[-2]
        
        if current_rsi < 30 or (ma5_cross_ma10 and current > ma20.iloc[-1]):
            return "BUY"
        elif current_rsi > 70 or ma5_death_ma10:
            return "SELL"
        else:
            return "HOLD"
    
    def _identify_sector(self, code: str) -> str:
        """识别股票所属板块"""
        for sector_name, sector_info in self.TECH_SECTORS.items():
            for concept_code in sector_info.get('concepts', []):
                try:
                    stocks = get_concept_stocks(concept_code)
                    if code in stocks:
                        return sector_name
                except:
                    pass
        return "其他科技"
    
    def _determine_growth_stage(self, stock: Dict, trend_phase: TrendPhase) -> GrowthStage:
        """判断成长阶段"""
        profit_growth = stock.get('profit_growth', 0)
        revenue_growth = stock.get('revenue_growth', 0)
        pe = stock.get('pe', 0)
        
        # 早期：业绩拐点，估值尚未反映
        if profit_growth > 100 and pe < 30:
            return GrowthStage.EARLY
        
        # 加速期：业绩加速，股价主升
        if profit_growth > 50 and trend_phase in [TrendPhase.ACCELERATION, TrendPhase.UPTREND]:
            return GrowthStage.ACCELERATION
        
        # 成长期：稳定高增长
        if profit_growth > 30 and revenue_growth > 20:
            return GrowthStage.GROWTH
        
        # 成熟期：增速放缓
        if 0 < profit_growth < 30:
            return GrowthStage.MATURE
        
        return GrowthStage.DECLINE
    
    def _calculate_scores(self, analyzed_stocks: List[Dict]) -> List[Dict]:
        """计算综合评分"""
        for stock in analyzed_stocks:
            # 成长得分 (40%)
            growth_score = 0
            profit_growth = stock.get('profit_growth', 0)
            revenue_growth = stock.get('revenue_growth', 0)
            roe = stock.get('roe', 0)
            
            # 利润增速得分
            if profit_growth > 100:
                growth_score += 40
            elif profit_growth > 50:
                growth_score += 30
            elif profit_growth > 30:
                growth_score += 20
            else:
                growth_score += 10
            
            # 营收增速得分
            if revenue_growth > 50:
                growth_score += 30
            elif revenue_growth > 30:
                growth_score += 20
            elif revenue_growth > 20:
                growth_score += 15
            else:
                growth_score += 5
            
            # ROE得分
            if roe > 20:
                growth_score += 30
            elif roe > 15:
                growth_score += 20
            elif roe > 10:
                growth_score += 15
            else:
                growth_score += 5
            
            stock['growth_score'] = min(growth_score, 100)
            
            # 趋势得分 (30%)
            trend_score = stock.get('trend_score', 50)
            
            # 估值得分 (20%)
            pe = stock.get('pe', 50)
            peg = pe / profit_growth if profit_growth > 0 else 10
            
            valuation_score = 50
            if 0 < peg < 1:
                valuation_score = 90
            elif peg < 1.5:
                valuation_score = 70
            elif peg < 2:
                valuation_score = 50
            else:
                valuation_score = 30
            
            stock['valuation_score'] = valuation_score
            stock['peg'] = peg
            
            # 板块权重 (10%)
            sector = stock.get('sector', '其他科技')
            sector_weight = self.TECH_SECTORS.get(sector, {}).get('weight', 1.0)
            sector_score = sector_weight * 50
            
            # 综合得分
            total_score = (
                growth_score * 0.40 +
                trend_score * 0.30 +
                valuation_score * 0.20 +
                sector_score * 0.10
            )
            
            stock['total_score'] = total_score
        
        # 按综合得分排序
        analyzed_stocks.sort(key=lambda x: x['total_score'], reverse=True)
        
        return analyzed_stocks
    
    def _select_final(self, scored_stocks: List[Dict], top_n: int) -> List[StockAnalysis]:
        """最终选股"""
        final = []
        sector_count = {}
        
        for stock in scored_stocks:
            sector = stock.get('sector', '其他')
            
            # 板块分散化：每个板块最多2只
            if sector_count.get(sector, 0) >= 2:
                continue
            
            sector_count[sector] = sector_count.get(sector, 0) + 1
            
            # 生成推荐理由
            reason = self._generate_reason(stock)
            
            # 目标价和止损
            current_price = stock.get('current_price', 0)
            target_price = current_price * 1.30  # 30%目标
            stop_loss = current_price * 0.92     # 8%止损
            
            # 仓位建议
            position_pct = 100 / top_n
            
            analysis = StockAnalysis(
                code=stock['code'],
                name=stock['name'],
                sector=stock['sector'],
                current_price=current_price,
                revenue_growth=stock.get('revenue_growth', 0),
                profit_growth=stock.get('profit_growth', 0),
                roe=stock.get('roe', 0),
                roe_trend="上升" if stock.get('roe', 0) > 15 else "稳定",
                pe=stock.get('pe', 0),
                pb=stock.get('pb', 0),
                peg=stock.get('peg', 0),
                trend_phase=stock.get('trend_phase', TrendPhase.BOTTOM),
                trend_score=stock.get('trend_score', 50),
                ma_position=stock.get('ma_position', ''),
                volume_ratio=stock.get('volume_ratio', 1),
                turnover_rate=stock.get('turnover_ratio', 0),
                swing_signal=stock.get('swing_signal', 'HOLD'),
                support_price=stock.get('support_price', current_price * 0.9),
                resistance_price=stock.get('resistance_price', current_price * 1.1),
                growth_score=stock.get('growth_score', 50),
                total_score=stock.get('total_score', 50),
                growth_stage=stock.get('growth_stage', GrowthStage.GROWTH),
                recommendation="买入" if stock.get('swing_signal') == 'BUY' else "持有观望",
                reason=reason,
                target_price=target_price,
                stop_loss=stop_loss,
                position_pct=position_pct
            )
            
            final.append(analysis)
            
            if len(final) >= top_n:
                break
        
        return final
    
    def _generate_reason(self, stock: Dict) -> str:
        """生成推荐理由"""
        reasons = []
        
        # 成长性
        profit_growth = stock.get('profit_growth', 0)
        if profit_growth > 100:
            reasons.append(f"利润高速增长{profit_growth:.0f}%")
        elif profit_growth > 50:
            reasons.append(f"利润快速增长{profit_growth:.0f}%")
        
        # 估值
        peg = stock.get('peg', 10)
        if peg < 1:
            reasons.append("PEG<1估值优势明显")
        elif peg < 1.5:
            reasons.append("估值合理")
        
        # 趋势
        trend_phase = stock.get('trend_phase', TrendPhase.BOTTOM)
        if trend_phase == TrendPhase.ACCELERATION:
            reasons.append("主升浪加速")
        elif trend_phase == TrendPhase.UPTREND:
            reasons.append("上升趋势确立")
        elif trend_phase == TrendPhase.BREAKOUT:
            reasons.append("突破启动")
        
        # 板块
        sector = stock.get('sector', '')
        if sector:
            reasons.append(f"属{sector}主线")
        
        return "，".join(reasons) if reasons else "综合指标优秀"
    
    def _to_dataframe(self, selections: List[StockAnalysis]) -> pd.DataFrame:
        """转换为DataFrame"""
        data = []
        for s in selections:
            data.append({
                'code': s.code,
                'name': s.name,
                'sector': s.sector,
                'current_price': s.current_price,
                'profit_growth': s.profit_growth,
                'revenue_growth': s.revenue_growth,
                'roe': s.roe,
                'pe': s.pe,
                'peg': s.peg,
                'trend_phase': s.trend_phase.value,
                'trend_score': s.trend_score,
                'growth_score': s.growth_score,
                'total_score': s.total_score,
                'growth_stage': s.growth_stage.value,
                'swing_signal': s.swing_signal,
                'recommendation': s.recommendation,
                'reason': s.reason,
                'target_price': s.target_price,
                'stop_loss': s.stop_loss,
                'position_pct': s.position_pct
            })
        return pd.DataFrame(data)


def run_screener():
    """运行筛选器"""
    # JQData认证
    auth('18610026017', 'Tt103003!')
    
    screener = TechGrowthScreener()
    results = screener.screen(top_n=5)
    
    if not results.empty:
        print("\n" + "="*70)
        print("🏆 最终选股结果")
        print("="*70)
        
        for i, row in results.iterrows():
            print(f"\n{i+1}. {row['name']} ({row['code']})")
            print(f"   板块: {row['sector']}")
            print(f"   成长阶段: {row['growth_stage']}")
            print(f"   利润增速: {row['profit_growth']:.1f}%")
            print(f"   PEG: {row['peg']:.2f}")
            print(f"   趋势阶段: {row['trend_phase']}")
            print(f"   综合得分: {row['total_score']:.1f}")
            print(f"   推荐理由: {row['reason']}")
            print(f"   目标价: ¥{row['target_price']:.2f}")
            print(f"   止损价: ¥{row['stop_loss']:.2f}")
    
    return results


if __name__ == "__main__":
    run_screener()
