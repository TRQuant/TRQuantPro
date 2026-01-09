#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 运行脚本

使用方法:
    python scripts/run_advisor_v4.py --mode train           # 训练模型
    python scripts/run_advisor_v4.py --mode backtest        # 回测验证（快速）
    python scripts/run_advisor_v4.py --mode multi-backtest  # 多层级回测（Fast→Standard→Precise）
    python scripts/run_advisor_v4.py --mode recommend       # 生成推荐
    python scripts/run_advisor_v4.py --mode optimize        # 参数优化
    python scripts/run_advisor_v4.py --mode generate        # 生成聚宽策略代码
    python scripts/run_advisor_v4.py --mode export          # 导出策略到文件
    python scripts/run_advisor_v4.py --mode full            # 完整流程
    python scripts/run_advisor_v4.py --mode status          # 查看系统状态
"""

import sys
from pathlib import Path

# 设置项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='Investment Advisor V4.0')
    parser.add_argument('--mode', type=str, default='recommend',
                       choices=['train', 'backtest', 'multi-backtest', 'recommend', 
                               'optimize', 'generate', 'export', 'full', 'status'],
                       help='运行模式')
    parser.add_argument('--start-date', type=str, default=None,
                       help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, default=None,
                       help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--top-n', type=int, default=10,
                       help='推荐数量')
    parser.add_argument('--skip-extraction', action='store_true',
                       help='跳过因子提取')
    parser.add_argument('--skip-negative', action='store_true',
                       help='跳过负样本采样')
    parser.add_argument('--rebalance-freq', type=str, default='weekly',
                       choices=['daily', 'weekly', 'monthly'],
                       help='调仓频率')
    parser.add_argument('--backtest-levels', type=str, default='fast',
                       help='回测层级 (fast/standard/precise, 逗号分隔)')
    parser.add_argument('--strategy-name', type=str, default=None,
                       help='策略名称')
    parser.add_argument('--output-dir', type=str, default='strategies/generated',
                       help='策略输出目录')
    parser.add_argument('--save-to-db', action='store_true', default=True,
                       help='保存到MongoDB')
    parser.add_argument('--verbose', action='store_true', default=True,
                       help='详细输出')
    
    # 特征工程参数（新增）
    parser.add_argument('--use-feature-pipeline', action='store_true', default=True,
                       help='使用特征工程流水线（防过拟合）')
    parser.add_argument('--no-feature-pipeline', action='store_true',
                       help='禁用特征流水线')
    parser.add_argument('--top-k-features', type=int, default=10,
                       help='选择Top K特征')
    parser.add_argument('--feature-select-method', type=str, default='combined',
                       choices=['ic', 'xgboost', 'rf', 'mutual_info', 'combined'],
                       help='特征选择方法')
    
    # 交叉验证参数（新增）
    parser.add_argument('--use-cv', action='store_true', default=True,
                       help='使用交叉验证')
    parser.add_argument('--no-cv', action='store_true',
                       help='禁用交叉验证')
    parser.add_argument('--cv-method', type=str, default='walk_forward',
                       choices=['time_series', 'walk_forward'],
                       help='交叉验证方法')
    parser.add_argument('--cv-splits', type=int, default=5,
                       help='时序CV折数')
    
    # 正则化参数（新增）
    parser.add_argument('--use-regularization', action='store_true', default=True,
                       help='使用增强正则化参数')
    parser.add_argument('--no-regularization', action='store_true',
                       help='禁用正则化')
    parser.add_argument('--early-stopping', type=int, default=20,
                       help='早停轮数（0禁用）')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  Investment Advisor V4.0")
    print(f"  运行模式: {args.mode}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 导入工作流
    from core.advisor_v4 import AdvisorV4Workflow, AdvisorV4Config
    from core.advisor_v4.trading_strategy import TradingConfig
    
    # 处理互斥参数
    use_feature_pipeline = not args.no_feature_pipeline if hasattr(args, 'no_feature_pipeline') else True
    use_cv = not args.no_cv if hasattr(args, 'no_cv') else True
    use_regularization = not args.no_regularization if hasattr(args, 'no_regularization') else True
    
    # 创建配置
    trading_config = TradingConfig(
        target_return=0.10,
        stop_loss=-0.05,
        trailing_stop=0.03,
        max_holding_days=5,
        position_size=0.10,
        max_positions=10,
    )
    
    config = AdvisorV4Config(
        trading_config=trading_config,
        test_start=args.start_date or '2025-09-30',
        test_end=args.end_date or '2025-12-31',
        # 特征工程配置
        use_feature_pipeline=use_feature_pipeline,
        top_k_features=args.top_k_features,
        feature_select_method=args.feature_select_method,
        # 交叉验证配置
        use_cv=use_cv,
        cv_method=args.cv_method,
        cv_n_splits=args.cv_splits,
        # 正则化配置
        use_regularization=use_regularization,
        early_stopping_rounds=args.early_stopping,
    )
    
    # 创建工作流
    workflow = AdvisorV4Workflow(config=config, verbose=args.verbose)
    
    # 执行对应模式
    if args.mode == 'train':
        run_train(workflow, args)
    elif args.mode == 'backtest':
        run_backtest(workflow, args)
    elif args.mode == 'multi-backtest':
        run_multi_backtest(workflow, args)
    elif args.mode == 'recommend':
        run_recommend(workflow, args)
    elif args.mode == 'optimize':
        run_optimize(workflow, args)
    elif args.mode == 'generate':
        run_generate_strategy(workflow, args)
    elif args.mode == 'export':
        run_export_strategy(workflow, args)
    elif args.mode == 'full':
        run_full(workflow, args)
    elif args.mode == 'status':
        run_status(workflow, args)
    
    print(f"\n{'='*60}")
    print(f"  运行完成!")
    print(f"{'='*60}\n")


def run_train(workflow, args):
    """运行训练模式（增强版 - 防过拟合）"""
    print("【训练模式】开始训练XGBoost预测模型...\n")
    
    # 显示配置
    print(f"配置:")
    print(f"  特征流水线: {'✅' if workflow.config.use_feature_pipeline else '❌'}")
    print(f"  交叉验证: {'✅ ' + workflow.config.cv_method if workflow.config.use_cv else '❌'}")
    print(f"  正则化: {'✅' if workflow.config.use_regularization else '❌'}")
    print(f"  早停轮数: {workflow.config.early_stopping_rounds}")
    print(f"  Top K特征: {workflow.config.top_k_features}")
    print()
    
    predictor = workflow.train(
        skip_extraction=args.skip_extraction,
        skip_negative_sampling=args.skip_negative,
    )
    
    if predictor:
        print("\n✅ 训练完成!")
        print(f"模型已保存至: {workflow.config.model_path}")
        
        # 显示特征流水线信息
        if workflow.feature_pipeline:
            print(f"特征流水线已保存至: {workflow.config.feature_pipeline_path}")
            selected = workflow.feature_pipeline.get_selected_features()
            print(f"选中特征 ({len(selected)}): {selected}")
        
        # 显示CV结果
        if workflow.cv_result:
            print(f"\n交叉验证结果:")
            print(f"  方法: {workflow.cv_result.method}")
            print(f"  折数: {workflow.cv_result.n_folds}")
            print(f"  AUC: {workflow.cv_result.mean_auc:.4f} ± {workflow.cv_result.std_auc:.4f}")
            print(f"  稳定性: {'✅ 良好' if workflow.cv_result.is_stable else '⚠️ ' + workflow.cv_result.stability_warning}")


def run_backtest(workflow, args):
    """运行回测模式（单层级）"""
    start_date = args.start_date or workflow.config.test_start
    end_date = args.end_date or workflow.config.test_end
    backtest_levels = args.backtest_levels.split(',')
    
    print(f"【回测模式】{start_date} ~ {end_date}")
    print(f"回测层级: {backtest_levels}\n")
    
    result = workflow.backtest(
        start_date=start_date,
        end_date=end_date,
        rebalance_freq=args.rebalance_freq,
        backtest_levels=backtest_levels,
        save_to_db=args.save_to_db
    )
    
    if result:
        print("\n✅ 回测完成!")
        print(f"总收益: {result.total_return:+.2%}")
        print(f"年化收益: {result.annualized_return:+.2%}")
        print(f"夏普比率: {result.sharpe_ratio:.3f}")
        print(f"最大回撤: {result.max_drawdown:.2%}")
        print(f"胜率: {result.win_rate:.1%}")
        print(f"交易次数: {result.total_trades}")


def run_multi_backtest(workflow, args):
    """运行多层级回测（Fast → Standard → Precise）"""
    start_date = args.start_date or workflow.config.test_start
    end_date = args.end_date or workflow.config.test_end
    
    print(f"【多层级回测】{start_date} ~ {end_date}")
    print("将依次运行: Fast → Standard → Precise\n")
    
    results = workflow.run_multi_level_backtest(
        start_date=start_date,
        end_date=end_date,
        generate_strategy=True
    )
    
    if results:
        print("\n✅ 多层级回测完成!")
        for level, result in results.items():
            if result:
                print(f"\n{level.upper()}:")
                print(f"  总收益: {result.total_return:+.2%}")
                print(f"  夏普: {result.sharpe_ratio:.3f}")
                print(f"  最大回撤: {result.max_drawdown:.2%}")


def run_recommend(workflow, args):
    """运行推荐模式"""
    date = args.start_date or datetime.now().strftime('%Y-%m-%d')
    
    print(f"【推荐模式】生成 {date} 的投资推荐...\n")
    
    signals = workflow.recommend(date=date, top_n=args.top_n)
    
    if signals:
        print(f"\n✅ 推荐完成! 共 {len(signals)} 只股票")
    else:
        print("\n⚠️ 未生成推荐")


def run_optimize(workflow, args):
    """运行优化模式"""
    print("【优化模式】使用遗传算法优化策略参数...\n")
    
    result = workflow.optimize(optimization_mode="balanced")
    
    if result:
        print("\n✅ 优化完成!")
        print(f"最佳适应度: {result.best_fitness:.4f}")
        print(f"最佳参数: {result.best_params}")


def run_generate_strategy(workflow, args):
    """生成聚宽策略代码"""
    strategy_name = args.strategy_name or f"V4.0多因子预测策略_{datetime.now().strftime('%Y%m%d')}"
    
    print(f"【策略生成】{strategy_name}\n")
    
    code = workflow.generate_strategy_code(
        strategy_name=strategy_name,
        save_to_db=args.save_to_db,
        save_to_file=True
    )
    
    if code:
        print(f"\n✅ 策略代码生成完成!")
        print(f"代码长度: {len(code)} 字符")
        print(f"代码行数: {len(code.splitlines())} 行")


def run_export_strategy(workflow, args):
    """导出策略到文件"""
    from pathlib import Path
    
    strategy_name = args.strategy_name or f"V4.0策略_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"【策略导出】{strategy_name}")
    print(f"输出目录: {output_dir}\n")
    
    # 生成策略代码
    code = workflow.generate_strategy_code(
        strategy_name=strategy_name,
        save_to_db=args.save_to_db,
        save_to_file=True
    )
    
    if code:
        # 导出到指定目录
        filepath = output_dir / f"{strategy_name.replace(' ', '_')}.py"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"\n✅ 策略已导出!")
        print(f"文件路径: {filepath}")
        print(f"代码长度: {len(code)} 字符")


def run_status(workflow, args):
    """查看系统状态"""
    print("【系统状态】Investment Advisor V4.0\n")
    
    # 数据存储状态
    from core.advisor_v4.data_storage import get_v4_storage
    storage = get_v4_storage()
    stats = storage.get_statistics()
    
    print("📊 数据存储:")
    print(f"  MongoDB连接: {'✅' if stats['mongodb_connected'] else '❌'}")
    print(f"  文件存储目录: {stats['file_storage_dir']}")
    
    if stats['mongodb_connected']:
        print(f"  策略数量: {stats['collections'].get('strategies', 0)}")
        print(f"  回测记录: {stats['collections'].get('backtests', 0)}")
        print(f"  推荐记录: {stats['collections'].get('recommendations', 0)}")
        print(f"  模型数量: {stats['collections'].get('models', 0)}")
    
    # 模型状态
    from pathlib import Path
    model_path = Path(workflow.config.model_path)
    print(f"\n🤖 模型状态:")
    print(f"  模型路径: {model_path}")
    print(f"  模型存在: {'✅' if model_path.exists() else '❌'}")
    
    # 回测引擎状态
    print(f"\n⚙️ 回测引擎:")
    try:
        from core.backtest import UnifiedBacktestManager, BacktestLevel
        print(f"  UnifiedBacktestManager: ✅")
        print(f"  支持层级: {[l.value for l in BacktestLevel]}")
    except Exception as e:
        print(f"  UnifiedBacktestManager: ❌ ({e})")
    
    try:
        from core.bullettrade import BulletTradeEngine
        print(f"  BulletTradeEngine: ✅")
    except Exception as e:
        print(f"  BulletTradeEngine: ⚠️ ({e})")
    
    # JQData状态
    print(f"\n📈 数据源:")
    print(f"  JQData连接: {'✅' if workflow.jq else '❌'}")


def run_full(workflow, args):
    """运行完整流程"""
    print("【完整流程】训练 -> 多层回测 -> 策略生成 -> 推荐\n")
    
    # Step 1: 训练
    print("\n" + "="*60)
    print("Step 1/4: 训练模型")
    print("="*60)
    run_train(workflow, args)
    
    # Step 2: 多层级回测
    print("\n" + "="*60)
    print("Step 2/4: 多层级回测验证")
    print("="*60)
    run_multi_backtest(workflow, args)
    
    # Step 3: 生成策略代码
    print("\n" + "="*60)
    print("Step 3/4: 生成聚宽策略代码")
    print("="*60)
    run_generate_strategy(workflow, args)
    
    # Step 4: 推荐
    print("\n" + "="*60)
    print("Step 4/4: 生成推荐")
    print("="*60)
    run_recommend(workflow, args)


if __name__ == '__main__':
    main()
