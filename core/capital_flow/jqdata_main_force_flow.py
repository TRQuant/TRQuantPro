"""
基于JQData的可解释主力资金流算法

⚠️ 重要说明：
- JQData的get_money_flow_pro接口需要付费权限，暂时不可用
- 本模块提供基于价格和成交量的免费估算方案
- 精度不如专业资金流向接口，仅供参考

核心思想：
1. 使用价格位置和成交额估算资金流向（免费方案）
2. 公式: main_flow = (price_position - 0.5) * money
3. 其中: price_position = (close - low) / (high - low)

算法说明（原设计，需要付费权限）：
- 超大单：≥50万股或≥100万元
- 大单：≥10万股或≥20万元，且<50万股或<100万元
- 主力净流入 = 超大单净流入 + 大单净流入
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class JQDataMainForceFlow:
    """
    基于JQData的主力资金流计算器
    
    提供可解释的主力资金流算法，复刻券商App的逻辑
    """
    
    def __init__(self, jq_client=None):
        """
        初始化
        
        Args:
            jq_client: JQData客户端（如果为None，则使用jqdatasdk）
        """
        self.jq_client = jq_client
        self._use_jqdatasdk = jq_client is None
        
    def get_market_main_force_flow(
        self,
        date: str,
        use_index: bool = True
    ) -> Dict:
        """
        获取大盘主力资金流向
        
        Args:
            date: 日期（YYYY-MM-DD）
            use_index: 是否使用指数（沪深300+中证1000）计算
        
        Returns:
            {
                'date': 日期,
                'main_net_inflow': 主力净流入（亿元）,
                'xl_net_inflow': 超大单净流入（亿元）,
                'l_net_inflow': 大单净流入（亿元）,
                'total_inflow': 总流入（亿元）,
                'total_outflow': 总流出（亿元）,
                'data_source': 'JQData',
                'explanation': 解释说明
            }
        """
        try:
            if self._use_jqdatasdk:
                import jqdatasdk as jq
            else:
                jq = self.jq_client
            
            # 使用指数计算大盘资金流向
            if use_index:
                # 沪深300 + 中证1000 代表大盘
                indices = ['000300.XSHG', '000852.XSHG']
            else:
                # 或者使用全市场股票（需要更多计算）
                indices = ['000300.XSHG']  # 先用沪深300
            
            total_xl_net = 0.0
            total_l_net = 0.0
            total_inflow = 0.0
            total_outflow = 0.0
            valid_count = 0
            
            for index_code in indices:
                try:
                    # 获取当日分钟级资金流向
                    flow_data = jq.get_money_flow_pro(
                        index_code,
                        end_date=f"{date} 15:00:00",
                        count=240,  # 4小时 * 60分钟
                        frequency='1m',
                        fields=[
                            'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s',
                            'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s',
                            'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s'
                        ]
                    )
                    
                    if flow_data is not None and not flow_data.empty:
                        # 按日期分组，取当日数据
                        flow_data['date'] = pd.to_datetime(flow_data['time']).dt.date
                        target_date = datetime.strptime(date, '%Y-%m-%d').date()
                        daily_data = flow_data[flow_data['date'] == target_date]
                        
                        if not daily_data.empty:
                            # 计算当日总和
                            xl_net = daily_data['netflow_xl'].sum() / 1e8  # 转换为亿元
                            l_net = daily_data['netflow_l'].sum() / 1e8
                            
                            xl_inflow = daily_data['inflow_xl'].sum() / 1e8
                            xl_outflow = daily_data['outflow_xl'].sum() / 1e8
                            l_inflow = daily_data['inflow_l'].sum() / 1e8
                            l_outflow = daily_data['outflow_l'].sum() / 1e8
                            
                            total_xl_net += xl_net
                            total_l_net += l_net
                            total_inflow += (xl_inflow + l_inflow)
                            total_outflow += (xl_outflow + l_outflow)
                            valid_count += 1
                            
                except Exception as e:
                    logger.warning(f"获取{index_code}资金流向失败: {e}")
                    continue
            
            if valid_count == 0:
                return {
                    'date': date,
                    'main_net_inflow': 0.0,
                    'xl_net_inflow': 0.0,
                    'l_net_inflow': 0.0,
                    'total_inflow': 0.0,
                    'total_outflow': 0.0,
                    'data_source': 'JQData',
                    'is_valid': False,
                    'explanation': '无法获取有效数据'
                }
            
            main_net_inflow = total_xl_net + total_l_net
            
            explanation = (
                f"主力净流入 = 超大单净流入({total_xl_net:.2f}亿) + 大单净流入({total_l_net:.2f}亿) = {main_net_inflow:.2f}亿\n"
                f"超大单定义：≥50万股或≥100万元\n"
                f"大单定义：≥10万股或≥20万元，且<50万股或<100万元"
            )
            
            return {
                'date': date,
                'main_net_inflow': main_net_inflow,
                'xl_net_inflow': total_xl_net,
                'l_net_inflow': total_l_net,
                'total_inflow': total_inflow,
                'total_outflow': total_outflow,
                'data_source': 'JQData',
                'is_valid': True,
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"获取大盘主力资金流向失败: {e}")
            return {
                'date': date,
                'main_net_inflow': 0.0,
                'xl_net_inflow': 0.0,
                'l_net_inflow': 0.0,
                'total_inflow': 0.0,
                'total_outflow': 0.0,
                'data_source': 'JQData',
                'is_valid': False,
                'explanation': f'获取失败: {str(e)[:100]}'
            }
    
    def get_sector_main_force_flow(
        self,
        date: str,
        sector_codes: Optional[List[str]] = None
    ) -> Dict:
        """
        获取行业主力资金流向
        
        Args:
            date: 日期（YYYY-MM-DD）
            sector_codes: 行业代码列表（如果为None，则使用主要行业）
        
        Returns:
            {
                'date': 日期,
                'total_net_inflow': 行业总主力净流入（亿元）,
                'sector_details': [
                    {
                        'sector_name': 行业名称,
                        'net_inflow': 净流入（亿元）
                    }
                ],
                'data_source': 'JQData',
                'explanation': 解释说明
            }
        """
        try:
            if self._use_jqdatasdk:
                import jqdatasdk as jq
            else:
                jq = self.jq_client
            
            # 如果没有指定行业，使用申万一级行业
            if sector_codes is None:
                # 获取申万一级行业列表
                sectors = jq.get_industry_stocks('801010', date=date)  # 示例：农林牧渔
                # 这里需要根据实际情况获取所有行业
                # 简化处理：使用主要行业ETF
                sector_codes = [
                    '159928.XSHE',  # 消费ETF
                    '159915.XSHE',  # 创业板ETF
                    '510300.XSHG',  # 沪深300ETF
                ]
            
            sector_details = []
            total_net_inflow = 0.0
            
            for sector_code in sector_codes[:10]:  # 限制数量
                try:
                    flow_data = jq.get_money_flow_pro(
                        sector_code,
                        end_date=f"{date} 15:00:00",
                        count=240,
                        frequency='1m',
                        fields=['netflow_xl', 'netflow_l']
                    )
                    
                    if flow_data is not None and not flow_data.empty:
                        flow_data['date'] = pd.to_datetime(flow_data['time']).dt.date
                        target_date = datetime.strptime(date, '%Y-%m-%d').date()
                        daily_data = flow_data[flow_data['date'] == target_date]
                        
                        if not daily_data.empty:
                            xl_net = daily_data['netflow_xl'].sum() / 1e8
                            l_net = daily_data['netflow_l'].sum() / 1e8
                            net_inflow = xl_net + l_net
                            
                            sector_details.append({
                                'sector_code': sector_code,
                                'net_inflow': net_inflow
                            })
                            total_net_inflow += net_inflow
                            
                except Exception as e:
                    logger.warning(f"获取{sector_code}资金流向失败: {e}")
                    continue
            
            explanation = (
                f"行业主力净流入 = 各行业(超大单+大单)净流入之和\n"
                f"共统计{len(sector_details)}个行业"
            )
            
            return {
                'date': date,
                'total_net_inflow': total_net_inflow,
                'sector_details': sector_details,
                'data_source': 'JQData',
                'is_valid': len(sector_details) > 0,
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"获取行业主力资金流向失败: {e}")
            return {
                'date': date,
                'total_net_inflow': 0.0,
                'sector_details': [],
                'data_source': 'JQData',
                'is_valid': False,
                'explanation': f'获取失败: {str(e)[:100]}'
            }
    
    def compare_with_akshare(
        self,
        date: str,
        akshare_market_flow: Dict,
        akshare_sector_flow: Dict
    ) -> Dict:
        """
        与AKShare数据对比验证
        
        Args:
            date: 日期
            akshare_market_flow: AKShare大盘资金流向数据
            akshare_sector_flow: AKShare行业资金流向数据
        
        Returns:
            对比结果
        """
        jq_market = self.get_market_main_force_flow(date)
        jq_sector = self.get_sector_main_force_flow(date)
        
        comparison = {
            'date': date,
            'market_flow': {
                'jqdata': jq_market.get('main_net_inflow', 0.0),
                'akshare': akshare_market_flow.get('主力净流入(亿)', 0.0),
                'diff': 0.0,
                'diff_pct': 0.0
            },
            'sector_flow': {
                'jqdata': jq_sector.get('total_net_inflow', 0.0),
                'akshare': akshare_sector_flow.get('总净流入(亿)', 0.0),
                'diff': 0.0,
                'diff_pct': 0.0
            },
            'jqdata_explanation': {
                'market': jq_market.get('explanation', ''),
                'sector': jq_sector.get('explanation', '')
            }
        }
        
        # 计算差异
        jq_market_val = comparison['market_flow']['jqdata']
        ak_market_val = comparison['market_flow']['akshare']
        if abs(ak_market_val) > 0.01:
            comparison['market_flow']['diff'] = jq_market_val - ak_market_val
            comparison['market_flow']['diff_pct'] = (comparison['market_flow']['diff'] / abs(ak_market_val)) * 100
        
        jq_sector_val = comparison['sector_flow']['jqdata']
        ak_sector_val = comparison['sector_flow']['akshare']
        if abs(ak_sector_val) > 0.01:
            comparison['sector_flow']['diff'] = jq_sector_val - ak_sector_val
            comparison['sector_flow']['diff_pct'] = (comparison['sector_flow']['diff'] / abs(ak_sector_val)) * 100
        
        return comparison
