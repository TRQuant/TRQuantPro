#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因子模块真实数据测试
====================

使用聚宽JQData试用账户测试因子模块的完整功能：
1. 数据获取与试用账户测试
2. 验证因子计算正确性
3. 测试多因子组合与选股
4. 模块集成调试

运行方式：
cd /home/taotao/dev/QuantTest/TRQuant
source venv/bin/activate
python tests/test_factors_real.py
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_jqdata_connection():
    """测试JQData连接"""
    print("\n" + "="*60)
    print("1. 测试JQData连接")
    print("="*60)
    
    try:
        from jqdata.client import JQDataClient
        
        client = JQDataClient()
        
        # 尝试认证
        success = client.authenticate()
        
        if success:
            print("✅ JQData认证成功")
            
            # 获取数据权限信息
            perm_info = client.get_permission_info()
            print(f"   权限信息: {perm_info}")
            
            return client
        else:
            print("❌ JQData认证失败")
            return None
            
    except Exception as e:
        print(f"❌ JQData连接失败: {e}")
        return None


def test_factor_calculation(jq_client):
    """测试因子计算"""
    print("\n" + "="*60)
    print("2. 测试因子计算")
    print("="*60)
    
    try:
        from core.factors import FactorManager
        import jqdatasdk as jq
        
        # 创建因子管理器
        factor_manager = FactorManager(jq_client=jq_client)
        
        # 获取沪深300成分股
        available_date = jq_client.get_available_date()
        print(f"可用日期: {available_date}")
        
        stocks = jq.get_index_stocks('000300.XSHG', date=available_date)[:50]  # 取前50只测试
        print(f"测试股票数: {len(stocks)}")
        
        # 测试各类因子
        test_factors = ['EP', 'ROE', 'PriceMomentum', 'Reversal']
        
        for factor_name in test_factors:
            try:
                result = factor_manager.calculate_factor(
                    factor_name, stocks, available_date,
                    winsorize=True, standardize=True
                )
                
                if result and result.valid_count > 0:
                    print(f"✅ {factor_name}: 有效值 {result.valid_count}/{len(stocks)}")
                    print(f"   Top 3: {result.top_n(3)}")
                    print(f"   均值: {result.values.mean():.4f}, 标准差: {result.values.std():.4f}")
                else:
                    print(f"❌ {factor_name}: 无有效值")
                    
            except Exception as e:
                print(f"❌ {factor_name}: 计算失败 - {e}")
        
        return factor_manager, stocks, available_date
        
    except Exception as e:
        print(f"❌ 因子计算测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def test_factor_combination(factor_manager, stocks, date):
    """测试多因子组合"""
    print("\n" + "="*60)
    print("3. 测试多因子组合与选股")
    print("="*60)
    
    try:
        # 计算多个因子
        factor_names = ['EP', 'ROE', 'Reversal']
        
        results = factor_manager.calculate_factors(factor_names, stocks, date)
        print(f"成功计算因子: {list(results.keys())}")
        
        # 等权组合
        combined = factor_manager.combine_factors(results, method='equal')
        print(f"组合因子均值: {combined.mean():.4f}")
        
        # 选股
        selected = factor_manager.select_stocks(combined, top_n=10)
        print(f"选出股票 Top 10: {selected}")
        
        # 自定义权重组合
        weights = {'EP': 0.4, 'ROE': 0.3, 'Reversal': 0.3}
        combined_weighted = factor_manager.combine_factors(results, weights=weights)
        selected_weighted = factor_manager.select_stocks(combined_weighted, top_n=10)
        print(f"加权组合选股 Top 10: {selected_weighted}")
        
        return True
        
    except Exception as e:
        print(f"❌ 多因子组合测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_factor_evaluator(jq_client, factor_manager, stocks, date):
    """测试因子评估器"""
    print("\n" + "="*60)
    print("4. 测试因子评估（IC计算）")
    print("="*60)
    
    try:
        from core.factors import FactorEvaluator
        
        evaluator = FactorEvaluator(jq_client=jq_client)
        
        # 获取因子对象
        factor = factor_manager.get_factor('PriceMomentum')
        
        if factor:
            # 计算因子值
            result = factor.calculate(stocks, date)
            
            # 简单IC测试（使用下一月收益）
            import jqdatasdk as jq
            
            # 获取未来20日收益
            trade_dates = jq.get_trade_days(date, date + timedelta(days=40))
            if len(trade_dates) >= 21:
                future_date = trade_dates[20]
                
                start_prices = jq.get_price(
                    stocks, end_date=date, count=1, fields=['close'], panel=False
                )
                end_prices = jq.get_price(
                    stocks, end_date=future_date, count=1, fields=['close'], panel=False
                )
                
                if not start_prices.empty and not end_prices.empty:
                    start_dict = dict(zip(start_prices['code'], start_prices['close']))
                    end_dict = dict(zip(end_prices['code'], end_prices['close']))
                    
                    returns = {}
                    for stock in stocks:
                        if stock in start_dict and stock in end_dict:
                            if start_dict[stock] > 0:
                                returns[stock] = (end_dict[stock] - start_dict[stock]) / start_dict[stock]
                    
                    forward_returns = pd.Series(returns)
                    
                    # 计算IC
                    ic_result = evaluator.calculate_ic(result.values, forward_returns)
                    
                    print(f"✅ PriceMomentum IC计算完成:")
                    print(f"   Rank IC: {ic_result.rank_ic:.4f}")
                    print(f"   P-value: {ic_result.p_value:.4f}")
                    print(f"   显著性: {'是' if ic_result.is_significant else '否'}")
                    
                    return True
        
        print("❌ 无法完成IC计算")
        return False
        
    except Exception as e:
        print(f"❌ 因子评估测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_factor_neutralization(jq_client, factor_manager, stocks, date):
    """测试因子中性化"""
    print("\n" + "="*60)
    print("5. 测试因子中性化")
    print("="*60)
    
    try:
        from core.factors.factor_neutralizer import FactorNeutralizer, FactorCorrelationAnalyzer
        
        neutralizer = FactorNeutralizer(jq_client=jq_client)
        
        # 计算EP因子
        result = factor_manager.calculate_factor('EP', stocks, date)
        
        if result and result.valid_count > 0:
            original_values = result.values
            
            # 中性化
            neutralized_values = neutralizer.neutralize(
                original_values, stocks, date,
                neutralize_industry=True,
                neutralize_size=True
            )
            
            print(f"✅ 因子中性化完成:")
            print(f"   原始因子 - 均值: {original_values.mean():.4f}, 标准差: {original_values.std():.4f}")
            print(f"   中性化后 - 均值: {neutralized_values.mean():.4f}, 标准差: {neutralized_values.std():.4f}")
            
            # 相关性分析
            analyzer = FactorCorrelationAnalyzer()
            
            factor_dict = {}
            for name in ['EP', 'ROE', 'PriceMomentum']:
                r = factor_manager.calculate_factor(name, stocks, date)
                if r and r.valid_count > 0:
                    factor_dict[name] = r.values
            
            if len(factor_dict) > 1:
                corr_matrix = analyzer.calculate_correlation_matrix(factor_dict)
                print(f"\n   因子相关性矩阵:")
                print(corr_matrix.round(3))
                
                redundant = analyzer.detect_redundant_factors(factor_dict)
                if redundant:
                    print(f"\n   冗余因子对: {redundant}")
                else:
                    print(f"\n   无冗余因子对 (阈值: 0.7)")
            
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ 因子中性化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_extended_factors(jq_client, stocks, date):
    """测试扩展因子"""
    print("\n" + "="*60)
    print("6. 测试扩展因子（规模/波动率/流动性）")
    print("="*60)
    
    try:
        from core.factors.extended_factors import (
            SizeFactor, VolatilityFactor, TurnoverFactor,
            BetaFactor, IlliquidityFactor
        )
        
        factors_to_test = [
            ('Size', SizeFactor(jq_client=jq_client)),
            ('Volatility', VolatilityFactor(jq_client=jq_client)),
            ('Turnover', TurnoverFactor(jq_client=jq_client)),
            ('Beta', BetaFactor(jq_client=jq_client)),
            ('Illiquidity', IlliquidityFactor(jq_client=jq_client)),
        ]
        
        for name, factor in factors_to_test:
            try:
                result = factor.calculate(stocks[:30], date)  # 只测试30只
                
                if result.valid_count > 0:
                    print(f"✅ {name}: 有效值 {result.valid_count}/{len(stocks[:30])}")
                    print(f"   Top 3: {result.top_n(3)}")
                else:
                    print(f"❌ {name}: 无有效值")
                    
            except Exception as e:
                print(f"❌ {name}: 计算失败 - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 扩展因子测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_generation(factor_manager):
    """测试策略代码生成"""
    print("\n" + "="*60)
    print("7. 测试PTrade策略代码生成")
    print("="*60)
    
    try:
        # 生成策略代码
        strategy_code = factor_manager.generate_ptrade_strategy(
            factor_names=['EP', 'ROE', 'Reversal'],
            weights={'EP': 0.4, 'ROE': 0.3, 'Reversal': 0.3},
            stock_pool='000300.XSHG',
            hold_num=30,
            rebalance_freq='monthly'
        )
        
        # 保存策略
        output_dir = project_root / "strategies" / "ptrade"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / "test_multifactor_strategy.py"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(strategy_code)
        
        print(f"✅ 策略代码生成成功")
        print(f"   保存位置: {filepath}")
        print(f"   代码行数: {len(strategy_code.splitlines())}")
        
        return True
        
    except Exception as e:
        print(f"❌ 策略生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("韬睿量化 - 因子模块综合测试")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. 测试JQData连接
    jq_client = test_jqdata_connection()
    results['JQData连接'] = jq_client is not None
    
    if jq_client is None:
        print("\n❌ JQData连接失败，无法继续测试")
        return results
    
    # 2. 测试因子计算
    factor_manager, stocks, date = test_factor_calculation(jq_client)
    results['因子计算'] = factor_manager is not None
    
    if factor_manager is None:
        print("\n❌ 因子计算失败，无法继续测试")
        return results
    
    # 3. 测试多因子组合
    results['多因子组合'] = test_factor_combination(factor_manager, stocks, date)
    
    # 4. 测试因子评估
    results['因子评估'] = test_factor_evaluator(jq_client, factor_manager, stocks, date)
    
    # 5. 测试因子中性化
    results['因子中性化'] = test_factor_neutralization(jq_client, factor_manager, stocks, date)
    
    # 6. 测试扩展因子
    results['扩展因子'] = test_extended_factors(jq_client, stocks, date)
    
    # 7. 测试策略生成
    results['策略生成'] = test_strategy_generation(factor_manager)
    
    # 打印汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n总计: {passed}/{total} 通过")
    
    return results


if __name__ == '__main__':
    run_all_tests()

