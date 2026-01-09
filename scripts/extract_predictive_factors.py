#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整提取预测因子（支持断点续传）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings
warnings.filterwarnings('ignore')

from core.advisor_v4.predictor_factor_extractor import PredictorFactorExtractor
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    print('='*70)
    print('Investment Advisor V4.0 - 完整提取预测因子')
    print('支持断点续传：每10个案例自动保存，中断后可继续')
    print('='*70)
    
    # 文件路径
    cases_file = 'results/high_return_cases_full_train.csv'
    checkpoint_file = 'results/high_return_cases_full_train_predictive_checkpoint.csv'
    output_file = 'results/predictive_features.csv'
    
    # 初始化提取器
    extractor = PredictorFactorExtractor(verbose=True)
    
    # 检查断点文件
    if Path(checkpoint_file).exists():
        checkpoint_df = pd.read_csv(checkpoint_file)
        print(f'\n✅ 找到断点文件: 已处理 {len(checkpoint_df)} 个案例')
        print(f'   将从断点继续提取剩余 {1024 - len(checkpoint_df)} 个案例\n')
    else:
        print(f'\n📝 未找到断点文件，从头开始提取 1024 个案例\n')
    
    # 开始提取（支持断点续传）
    print('开始提取预测因子（T-5时刻）...')
    print('注意：此过程需要约30分钟，每10个案例自动保存断点')
    print('可以随时中断（Ctrl+C），下次运行会自动继续\n')
    
    try:
        predictive_df = extractor.extract_from_historical_cases(
            cases_file=cases_file,
            lookback_days=5,
            checkpoint_file=checkpoint_file,
            resume=True  # 支持断点续传
        )
        
        # 保存最终结果
        predictive_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f'\n✅ 预测因子提取完成!')
        print(f'最终结果: {output_file}')
        print(f'总记录数: {len(predictive_df)} 条')
        print(f'高收益案例: {(predictive_df["is_high_return"]).sum()} 条')
        
        # 清理断点文件
        if Path(checkpoint_file).exists():
            Path(checkpoint_file).unlink()
            print(f'✅ 已清理断点文件')
        
    except KeyboardInterrupt:
        print('\n\n⚠️ 提取被用户中断')
        if Path(checkpoint_file).exists():
            checkpoint_df = pd.read_csv(checkpoint_file)
            print(f'✅ 已保存断点: {len(checkpoint_df)} 个案例')
            print(f'下次运行将从此处继续')
        sys.exit(0)
    except Exception as e:
        logger.error(f"提取失败: {e}", exc_info=True)
        if Path(checkpoint_file).exists():
            checkpoint_df = pd.read_csv(checkpoint_file)
            print(f'\n⚠️ 提取失败，但已保存断点: {len(checkpoint_df)} 个案例')
        sys.exit(1)
    
    print('\n' + '='*70)


if __name__ == '__main__':
    main()
