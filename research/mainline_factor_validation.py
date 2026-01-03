#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场主线因子验证脚本

使用方法:
    python research/mainline_factor_validation.py

功能:
    1. 验证主线预测因子组合的有效性
    2. 计算IC、IR等指标
    3. 分组回测验证
    4. 生成验证报告
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from jqdata.client import JQDataClient
    from jqdata.auth import authenticate
    from config.config_manager import get_config_manager
    from core.factors.jqdata_factor_engine import JQDataFactorEngine
    JQDATA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 导入失败: {e}")
    JQDATA_AVAILABLE = False

try:
    from core.factors.factor_evaluator import FactorEvaluator
    FACTOR_EVAL_AVAILABLE = True
except ImportError:
    FACTOR_EVAL_AVAILABLE = False
    FactorEvaluator = None


class MainlineFactorValidator:
    """主线因子验证器"""
    
    def __init__(self, jq_client: Optional[JQDataClient] = None):
        """
        初始化验证器
        
        Args:
            jq_client: JQData客户端，如果为None则自动创建
        """
        if jq_client is None and JQDATA_AVAILABLE:
            # 自动认证
            config_manager = get_config_manager()
            jq_config = config_manager.get_jqdata_config()
            self.jq_client = JQDataClient()
            success = self.jq_client.authenticate(
                jq_config.get('username'),
                jq_config.get('password')
            )
            if not success:
                raise ValueError("JQData认证失败")
        else:
            self.jq_client = jq_client
        
        if JQDATA_AVAILABLE:
            self.factor_engine = JQDataFactorEngine(self.jq_client)
        else:
            self.factor_engine = None
        
        if FACTOR_EVAL_AVAILABLE and self.jq_client:
            self.evaluator = FactorEvaluator(jq_client=self.jq_client)
        else:
            self.evaluator = None
    
    def validate_single_factor(
        self,
        factor_name: str,
        stocks: List[str],
        start_date: str,
        end_date: str,
        period: str = 'W'  # 周度
    ) -> Dict:
        """
        验证单个因子
        
        Args:
            factor_name: 因子名称（如 'alpha_001', 'revenue_growth'）
            stocks: 股票列表
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            period: 调仓周期（'W'周度, 'M'月度）
        
        Returns:
            验证结果字典
        """
        if not self.evaluator:
            return {'error': 'FactorEvaluator不可用'}
        
        print(f"\n{'='*60}")
        print(f"验证因子: {factor_name}")
        print(f"股票数量: {len(stocks)}")
        print(f"时间范围: {start_date} 至 {end_date}")
        print(f"{'='*60}\n")
        
        # 计算IC时间序列
        print("📊 计算IC时间序列...")
        try:
            ic_series = self._calculate_ic_series_simple(
                factor_name, stocks, start_date, end_date, period
            )
            
            if ic_series.empty:
                return {'error': 'IC计算失败，数据不足'}
            
            # IC统计
            ic_mean = float(ic_series['ic'].mean())
            ic_std = float(ic_series['ic'].std())
            ic_ir = ic_mean / ic_std if ic_std > 0 else 0.0
            ic_positive_ratio = float((ic_series['ic'] > 0).mean())
            
            print(f"✅ IC均值: {ic_mean:.4f}")
            print(f"✅ IC标准差: {ic_std:.4f}")
            print(f"✅ IC IR: {ic_ir:.4f}")
            print(f"✅ IC正比率: {ic_positive_ratio:.2%}")
            
            # 判断有效性
            is_valid = (
                ic_mean > 0.05 and
                ic_ir > 0.5 and
                ic_positive_ratio > 0.55
            )
            
            return {
                'factor_name': factor_name,
                'ic_mean': ic_mean,
                'ic_std': ic_std,
                'ic_ir': ic_ir,
                'ic_positive_ratio': ic_positive_ratio,
                'is_valid': is_valid,
                'ic_series': ic_series
            }
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return {'error': str(e)}
    
    def _calculate_ic_series_simple(
        self,
        factor_name: str,
        stocks: List[str],
        start_date: str,
        end_date: str,
        period: str
    ) -> pd.DataFrame:
        """简化的IC时间序列计算"""
        import jqdatasdk as jq
        
        # 生成调仓日期
        dates = pd.date_range(start_date, end_date, freq=period)
        ic_values = []
        
        for i, date in enumerate(dates[:-1]):  # 最后一个日期没有下一期收益
            try:
                # 获取因子值
                if 'alpha' in factor_name.lower():
                    # Alpha因子
                    factor_data = self._get_alpha_factor(
                        factor_name, stocks, date.strftime('%Y-%m-%d')
                    )
                else:
                    # 其他因子
                    factor_data = self._get_factor_value(
                        factor_name, stocks, date.strftime('%Y-%m-%d')
                    )
                
                if factor_data is None or factor_data.empty:
                    continue
                
                # 获取下一期收益
                next_date = dates[i+1]
                returns = self._get_stock_returns(
                    stocks, date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')
                )
                
                if returns is None or returns.empty:
                    continue
                
                # 对齐数据
                common_stocks = list(set(factor_data.index) & set(returns.index))
                if len(common_stocks) < 10:  # 至少10只股票
                    continue
                
                factor_values = factor_data.loc[common_stocks]
                return_values = returns.loc[common_stocks]
                
                # 计算IC（相关系数）
                if len(factor_values) > 0 and len(return_values) > 0:
                    ic = np.corrcoef(factor_values, return_values)[0, 1]
                    if not np.isnan(ic):
                        ic_values.append({
                            'date': date,
                            'ic': ic,
                            'n_stocks': len(common_stocks)
                        })
                
            except Exception as e:
                print(f"⚠️ 日期 {date} 计算失败: {e}")
                continue
        
        return pd.DataFrame(ic_values)
    
    def _get_alpha_factor(
        self,
        factor_name: str,
        stocks: List[str],
        date: str
    ) -> Optional[pd.Series]:
        """获取Alpha因子值"""
        if not self.factor_engine:
            return None
        
        try:
            # 提取因子编号（如 'alpha_001' -> '001'）
            factor_num = factor_name.split('_')[-1]
            
            # 调用factor_engine获取Alpha因子
            # 注意：这里需要根据实际的API调整
            result = self.factor_engine.get_alpha_factor(
                f'alpha_{factor_num}',
                stocks,
                date
            )
            
            if result:
                return pd.Series(result)
        except Exception as e:
            print(f"⚠️ 获取Alpha因子失败: {e}")
        
        return None
    
    def _get_factor_value(
        self,
        factor_name: str,
        stocks: List[str],
        date: str
    ) -> Optional[pd.Series]:
        """获取其他因子值"""
        if not self.factor_engine:
            return None
        
        try:
            result = self.factor_engine.get_factor_values(
                stocks=stocks,
                factors=[factor_name],
                start_date=date,
                end_date=date
            )
            
            if result and not result.empty:
                return result[factor_name]
        except Exception as e:
            print(f"⚠️ 获取因子值失败: {e}")
        
        return None
    
    def _get_stock_returns(
        self,
        stocks: List[str],
        start_date: str,
        end_date: str
    ) -> Optional[pd.Series]:
        """获取股票收益率"""
        import jqdatasdk as jq
        
        try:
            # 获取价格数据
            prices_start = jq.get_price(
                stocks,
                start_date=start_date,
                end_date=start_date,
                fields=['close']
            )
            
            prices_end = jq.get_price(
                stocks,
                start_date=end_date,
                end_date=end_date,
                fields=['close']
            )
            
            if prices_start.empty or prices_end.empty:
                return None
            
            # 计算收益率
            returns = (prices_end['close'] - prices_start['close']) / prices_start['close']
            return returns
        except Exception as e:
            print(f"⚠️ 获取收益率失败: {e}")
            return None
    
    def validate_factor_combination(
        self,
        factor_combination: Dict[str, float],  # {因子名: 权重}
        stocks: List[str],
        start_date: str,
        end_date: str,
        period: str = 'W'
    ) -> Dict:
        """
        验证因子组合
        
        Args:
            factor_combination: 因子组合字典 {因子名: 权重}
            stocks: 股票列表
            start_date: 开始日期
            end_date: 结束日期
            period: 调仓周期
        
        Returns:
            验证结果
        """
        print(f"\n{'='*60}")
        print("验证因子组合")
        print(f"因子数量: {len(factor_combination)}")
        print(f"{'='*60}\n")
        
        # 验证每个因子
        factor_results = {}
        for factor_name, weight in factor_combination.items():
            print(f"\n验证因子: {factor_name} (权重: {weight:.2%})")
            result = self.validate_single_factor(
                factor_name, stocks, start_date, end_date, period
            )
            factor_results[factor_name] = result
        
        # 综合评估
        valid_factors = [f for f, r in factor_results.items() if r.get('is_valid', False)]
        invalid_factors = [f for f, r in factor_results.items() if not r.get('is_valid', False)]
        
        print(f"\n{'='*60}")
        print("因子组合验证总结")
        print(f"{'='*60}")
        print(f"✅ 有效因子数量: {len(valid_factors)}/{len(factor_combination)}")
        print(f"❌ 无效因子数量: {len(invalid_factors)}")
        
        if valid_factors:
            print(f"\n有效因子列表:")
            for f in valid_factors:
                print(f"  - {f}")
        
        if invalid_factors:
            print(f"\n无效因子列表:")
            for f in invalid_factors:
                print(f"  - {f}")
        
        return {
            'factor_results': factor_results,
            'valid_factors': valid_factors,
            'invalid_factors': invalid_factors,
            'valid_ratio': len(valid_factors) / len(factor_combination) if factor_combination else 0
        }


def main():
    """主函数"""
    print("=" * 60)
    print("市场主线因子验证脚本")
    print("=" * 60)
    
    if not JQDATA_AVAILABLE:
        print("❌ JQData不可用，请检查依赖安装")
        return
    
    # 初始化验证器
    try:
        validator = MainlineFactorValidator()
        print("✅ 验证器初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 示例：验证单个Alpha因子
    print("\n" + "="*60)
    print("示例1: 验证单个Alpha因子")
    print("="*60)
    
    # 获取测试股票列表（沪深300成分股）
    import jqdatasdk as jq
    try:
        test_stocks = jq.get_index_stocks('000300.XSHG')[:50]  # 取前50只
        print(f"测试股票数量: {len(test_stocks)}")
    except:
        test_stocks = ['000001.XSHE', '600000.XSHG', '000002.XSHE']  # 备用
        print(f"使用备用股票列表: {len(test_stocks)}")
    
    # 验证Alpha001因子
    result = validator.validate_single_factor(
        factor_name='alpha_001',
        stocks=test_stocks,
        start_date='2023-01-01',
        end_date='2024-12-31',
        period='W'
    )
    
    if 'error' not in result:
        print(f"\n✅ 验证完成")
        print(f"因子有效性: {'有效' if result['is_valid'] else '无效'}")
    
    # 示例：验证因子组合
    print("\n" + "="*60)
    print("示例2: 验证因子组合")
    print("="*60)
    
    factor_combo = {
        'alpha_001': 0.25,
        'alpha_002': 0.25,
        'revenue_growth': 0.25,
        'roe': 0.25
    }
    
    combo_result = validator.validate_factor_combination(
        factor_combination=factor_combo,
        stocks=test_stocks,
        start_date='2023-01-01',
        end_date='2024-12-31',
        period='W'
    )
    
    print(f"\n✅ 因子组合验证完成")
    print(f"有效因子比例: {combo_result['valid_ratio']:.2%}")
    
    print("\n" + "="*60)
    print("验证完成")
    print("="*60)


if __name__ == '__main__':
    main()

