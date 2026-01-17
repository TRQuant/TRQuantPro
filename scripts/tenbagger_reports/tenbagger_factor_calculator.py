#!/usr/bin/env python3
"""
十倍股因子计算器

基于A股十倍股研究成果，使用JQData实现因子计算

Author: TRQuant Team
Date: 2025-12-20
"""

import sys
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenbaggerFactorCalculator:
    """
    十倍股因子计算器
    
    因子权重体系:
    - 财务因子: 40%
    - 成长动量: 25%
    - 估值因子: 20%
    - 技术因子: 15%
    """
    
    # 因子权重
    FACTOR_WEIGHTS = {
        'financial': 0.40,
        'growth': 0.25,
        'valuation': 0.20,
        'technical': 0.15
    }
    
    # 财务因子阈值
    FINANCIAL_THRESHOLDS = {
        'revenue_growth': {'excellent': 30, 'good': 15, 'ok': 0},
        'profit_growth': {'excellent': 50, 'good': 20, 'ok': 0},
        'gross_margin': {'excellent': 40, 'good': 25, 'ok': 15},
        'roe': {'excellent': 15, 'good': 10, 'ok': 5},
        'net_margin': {'excellent': 15, 'good': 5, 'ok': 0}
    }
    
    # 估值因子阈值
    VALUATION_THRESHOLDS = {
        'pe': {'excellent': 30, 'good': 50, 'ok': 100},
        'peg': {'excellent': 1, 'good': 2, 'ok': 3},
        'market_cap': {'min': 20, 'sweet_spot_max': 100, 'max': 300}
    }
    
    # 技术因子阈值
    TECHNICAL_THRESHOLDS = {
        'relative_strength': {'excellent': 70, 'good': 60},
        'vol_ratio': {'excellent': 1.5, 'good': 1.2}
    }
    
    def __init__(self, jq_client: Optional[JQDataClient] = None):
        """初始化"""
        self.jq_client = jq_client
        if not self.jq_client:
            self._init_jqdata()
    
    def _init_jqdata(self):
        """初始化JQData连接"""
        self.jq_client = JQDataClient()
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        self.jq_client.authenticate(jq_config['username'], jq_config['password'])
        logger.info("JQData 认证成功")
    
    def get_financial_factors(self, symbol: str, date: str = None) -> Dict[str, Any]:
        """
        获取财务因子
        
        使用JQData indicator表
        """
        try:
            from jqdatasdk import query, indicator
            
            if not date:
                date = self.jq_client.get_available_end_date()
            
            q = query(
                indicator.roe,
                indicator.gross_profit_margin,
                indicator.net_profit_margin,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.eps,
                indicator.roa
            ).filter(
                indicator.code == symbol
            )
            
            # 使用date参数获取指定日期能看到的最新数据（indicator表是季度更新的）
            df = self.jq_client.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                logger.warning(f"{symbol}: 未获取到财务数据")
                return {}
            
            row = df.iloc[0]
            return {
                'roe': self._safe_float(row.get('roe')),
                'gross_margin': self._safe_float(row.get('gross_profit_margin')),
                'net_margin': self._safe_float(row.get('net_profit_margin')),
                'revenue_growth': self._safe_float(row.get('inc_revenue_year_on_year')),
                'profit_growth': self._safe_float(row.get('inc_net_profit_year_on_year')),
                'eps': self._safe_float(row.get('eps')),
                'roa': self._safe_float(row.get('roa'))
            }
        except Exception as e:
            logger.error(f"{symbol}: 获取财务因子失败 - {e}")
            return {}
    
    def get_valuation_factors(self, symbol: str, date: str = None) -> Dict[str, Any]:
        """
        获取估值因子
        
        使用JQData valuation表
        """
        try:
            from jqdatasdk import query, valuation, get_fundamentals
            
            if not date:
                date = self.jq_client.get_available_end_date()
            
            q = query(
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio,
                valuation.pcf_ratio,
                valuation.market_cap,
                valuation.circulating_market_cap,
                valuation.turnover_ratio
            ).filter(
                valuation.code == symbol
            )
            
            df = get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                logger.warning(f"{symbol}: 未获取到估值数据")
                return {}
            
            row = df.iloc[0]
            return {
                'pe_ratio': self._safe_float(row.get('pe_ratio')),
                'pb_ratio': self._safe_float(row.get('pb_ratio')),
                'ps_ratio': self._safe_float(row.get('ps_ratio')),
                'pcf_ratio': self._safe_float(row.get('pcf_ratio')),
                'market_cap': self._safe_float(row.get('market_cap')),
                'circulating_market_cap': self._safe_float(row.get('circulating_market_cap')),
                'turnover_ratio': self._safe_float(row.get('turnover_ratio'))
            }
        except Exception as e:
            logger.error(f"{symbol}: 获取估值因子失败 - {e}")
            return {}
    
    def get_technical_factors(self, symbol: str, end_date: str = None, days: int = 60) -> Dict[str, Any]:
        """
        获取技术因子
        
        使用JQData get_price
        """
        try:
            if not end_date:
                end_date = self.jq_client.get_available_end_date()
            
            start_date = (datetime.strptime(end_date, '%Y-%m-%d') - 
                          timedelta(days=days)).strftime('%Y-%m-%d')
            
            prices = self.jq_client.get_price(
                symbol,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close', 'volume', 'high', 'low']
            )
            
            if prices is None or len(prices) < 20:
                logger.warning(f"{symbol}: 价格数据不足")
                return {}
            
            close = prices['close']
            volume = prices['volume']
            
            # 均线
            ma5 = close.tail(5).mean()
            ma20 = close.tail(20).mean()
            ma60 = close.tail(min(60, len(close))).mean()
            
            latest_close = close.iloc[-1]
            
            # 均线多头
            ma_bullish = latest_close > ma5 > ma20
            
            # 成交量比率
            vol_5 = volume.tail(5).mean()
            vol_20 = volume.tail(20).mean()
            vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
            
            # 相对强度（近20日涨幅）
            if len(close) >= 20:
                change_20d = (latest_close / close.iloc[-20] - 1) * 100
                relative_strength = min(100, max(0, 50 + change_20d))
            else:
                relative_strength = 50
            
            # 突破信号
            high_20 = prices['high'].tail(20).max()
            breakout_signal = latest_close >= high_20 * 0.95
            
            return {
                'ma_bullish': ma_bullish,
                'vol_ratio': vol_ratio,
                'relative_strength': relative_strength,
                'latest_close': latest_close,
                'breakout_signal': breakout_signal,
                'ma5': ma5,
                'ma20': ma20,
                'ma60': ma60
            }
        except Exception as e:
            logger.error(f"{symbol}: 获取技术因子失败 - {e}")
            return {}
    
    def calculate_score(self, symbol: str, date: str = None) -> Dict[str, Any]:
        """
        计算十倍股潜力得分
        
        满分100分:
        - 财务因子: 40分
        - 成长动量: 25分（暂未实现完整）
        - 估值因子: 20分
        - 技术因子: 15分
        """
        if not date:
            date = self.jq_client.get_available_end_date()
        
        # 获取数据
        financial = self.get_financial_factors(symbol, date)
        valuation = self.get_valuation_factors(symbol, date)
        technical = self.get_technical_factors(symbol, date)
        
        score = 0
        details = {}
        
        # === 财务因子（40分）===
        financial_score = 0
        
        # 营收增速（10分）
        rev_growth = financial.get('revenue_growth', 0)
        if rev_growth >= 30:
            financial_score += 10
        elif rev_growth >= 15:
            financial_score += 7
        elif rev_growth >= 0:
            financial_score += 3
        details['revenue_growth'] = rev_growth
        
        # 利润增速（10分）
        profit_growth = financial.get('profit_growth', 0)
        if profit_growth >= 50:
            financial_score += 10
        elif profit_growth >= 20:
            financial_score += 7
        elif profit_growth >= 0:
            financial_score += 3
        details['profit_growth'] = profit_growth
        
        # 毛利率（8分）
        gross_margin = financial.get('gross_margin', 0)
        if gross_margin >= 40:
            financial_score += 8
        elif gross_margin >= 25:
            financial_score += 5
        elif gross_margin >= 15:
            financial_score += 2
        details['gross_margin'] = gross_margin
        
        # ROE（7分）
        roe = financial.get('roe', 0)
        if roe >= 15:
            financial_score += 7
        elif roe >= 10:
            financial_score += 5
        elif roe >= 5:
            financial_score += 3
        details['roe'] = roe
        
        # 净利率（5分）
        net_margin = financial.get('net_margin', 0)
        if net_margin >= 15:
            financial_score += 5
        elif net_margin >= 5:
            financial_score += 3
        details['net_margin'] = net_margin
        
        score += financial_score
        details['financial_score'] = financial_score
        
        # === 估值因子（20分）===
        valuation_score = 0
        
        # PE（8分）
        pe = valuation.get('pe_ratio', 0)
        if 0 < pe <= 30:
            valuation_score += 8
        elif 30 < pe <= 50:
            valuation_score += 6
        elif 50 < pe <= 100:
            valuation_score += 3
        details['pe_ratio'] = pe
        
        # PEG（7分）
        if profit_growth > 0 and pe > 0:
            peg = pe / profit_growth
            if peg <= 1:
                valuation_score += 7
            elif peg <= 2:
                valuation_score += 5
            elif peg <= 3:
                valuation_score += 2
            details['peg'] = round(peg, 2)
        else:
            details['peg'] = None
        
        # 市值（5分）
        market_cap = valuation.get('market_cap', 0)
        if 20 <= market_cap <= 100:
            valuation_score += 5
        elif 100 < market_cap <= 300:
            valuation_score += 3
        elif market_cap < 20:
            valuation_score += 2
        details['market_cap'] = market_cap
        
        score += valuation_score
        details['valuation_score'] = valuation_score
        
        # === 技术因子（15分）===
        technical_score = 0
        
        # 均线多头（5分）
        if technical.get('ma_bullish', False):
            technical_score += 5
        details['ma_bullish'] = technical.get('ma_bullish', False)
        
        # 相对强度（5分）
        rs = technical.get('relative_strength', 50)
        if rs >= 70:
            technical_score += 5
        elif rs >= 60:
            technical_score += 3
        details['relative_strength'] = rs
        
        # 成交量趋势（5分）
        vol_ratio = technical.get('vol_ratio', 1)
        if vol_ratio >= 1.5:
            technical_score += 5
        elif vol_ratio >= 1.2:
            technical_score += 3
        details['vol_ratio'] = vol_ratio
        
        score += technical_score
        details['technical_score'] = technical_score
        
        # === 成长动量（25分）===
        # 简化版：使用已有增速数据
        growth_score = 0
        
        # 增速加分（加速信号）
        if rev_growth > 0 and profit_growth > 0:
            if profit_growth > rev_growth:  # 利润增速>营收增速
                growth_score += 10
            growth_score += min(15, (rev_growth + profit_growth) / 10)
        
        score += growth_score
        details['growth_score'] = growth_score
        
        # 总分和等级
        total_score = round(score, 2)
        level = self._get_level(total_score)
        
        return {
            'symbol': symbol,
            'date': date,
            'total_score': total_score,
            'max_score': 100,
            'level': level,
            'is_recommended': level in ['S+', 'S', 'A'],
            'financial_score': financial_score,
            'valuation_score': valuation_score,
            'technical_score': technical_score,
            'growth_score': growth_score,
            'details': details
        }
    
    def _get_level(self, score: float) -> str:
        """根据分数确定等级"""
        if score >= 80:
            return 'S+'
        elif score >= 70:
            return 'S'
        elif score >= 60:
            return 'A'
        elif score >= 50:
            return 'B'
        elif score >= 40:
            return 'C'
        else:
            return 'D'
    
    def _safe_float(self, value, default: float = 0.0) -> float:
        """安全转换为浮点数"""
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    
    def batch_calculate(self, symbols: List[str], date: str = None) -> List[Dict[str, Any]]:
        """批量计算"""
        results = []
        for symbol in symbols:
            try:
                result = self.calculate_score(symbol, date)
                results.append(result)
                logger.info(f"{symbol}: 得分 {result['total_score']} ({result['level']})")
            except Exception as e:
                logger.warning(f"{symbol}: 计算失败 - {e}")
        
        # 按分数排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        return results


def main():
    """主函数：测试因子计算器"""
    print("=" * 70)
    print("⚔️ 轩辕剑灵 - 十倍股因子计算器测试")
    print("=" * 70)
    
    # 初始化
    calculator = TenbaggerFactorCalculator()
    
    # 测试股票
    test_symbols = [
        "300001.XSHE",  # 特锐德
        "000333.XSHE",  # 美的集团
        "600519.XSHG",  # 贵州茅台（如果在权限范围内）
    ]
    
    print("\n📊 开始因子计算...")
    results = calculator.batch_calculate(test_symbols)
    
    print("\n📋 计算结果:")
    print("-" * 50)
    for r in results:
        print(f"\n{r['symbol']} - {r['level']}级 ({r['total_score']}/100)")
        print(f"  推荐: {'✅' if r['is_recommended'] else '❌'}")
        print(f"  财务因子: {r['financial_score']}/40")
        print(f"  估值因子: {r['valuation_score']}/20")
        print(f"  技术因子: {r['technical_score']}/15")
        print(f"  成长动量: {r['growth_score']}/25")
        print(f"  详情:")
        for key, value in r['details'].items():
            if not key.endswith('_score'):
                print(f"    - {key}: {value}")
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    main()

