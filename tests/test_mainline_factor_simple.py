#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线因子组合简单测试（命令行版本）

用于快速测试因子组合功能，不需要GUI
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_factor_combination():
    """测试因子组合功能"""
    print("=" * 60)
    print("主线因子组合测试")
    print("=" * 60)
    
    try:
        from core.mainline.mainline_workflow_integration import MainlineWorkflowStep
        
        print("\n[1/3] 初始化工作流步骤...")
        workflow_step = MainlineWorkflowStep()
        print("✅ 初始化成功")
        
        print("\n[2/3] 计算因子组合得分...")
        print("  行业代码: 801010 (示例)")
        print("  日期: 2024-12-31")
        print("  期限: medium")
        
        # 计算因子组合得分
        factor_combo = workflow_step.factor_combo
        score_result = factor_combo.calculate_mainline_score(
            industry_code="801010",
            date="2024-12-31",
            period="medium"
        )
        
        print("✅ 计算完成")
        
        print("\n[3/3] 显示结果:")
        print("-" * 60)
        print(f"综合得分: {score_result['total_score']:.2f}")
        print(f"\n各因子得分:")
        print(f"  宏观因子: {score_result['macro_score']:.2f}")
        print(f"  资金流因子: {score_result['capital_flow_score']:.2f}")
        print(f"  行业景气因子: {score_result['industry_prosperity_score']:.2f}")
        print(f"  技术动量因子: {score_result['technical_momentum_score']:.2f}")
        print(f"  市场情绪因子: {score_result['market_sentiment_score']:.2f}")
        
        print(f"\n权重配置:")
        weights = score_result.get('weights_used', {})
        for key, value in weights.items():
            print(f"  {key}: {value*100:.1f}%")
        
        print(f"\n详细信息:")
        print(f"  期限: {score_result.get('period', 'N/A')}")
        print(f"  行业代码: {score_result.get('industry_code', 'N/A')}")
        print(f"  日期: {score_result.get('date', 'N/A')}")
        print(f"  股票数量: {score_result.get('n_stocks', 0)}")
        
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    success = test_factor_combination()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

