#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 端到端测试脚本
=====================================

功能：
- 完整验证从数据准备到最终推荐的整个流程
- 包括数据验证、GPU加速训练、因子优化、回测验证、推荐生成和报告生成

测试模式：
- 快速模式（默认）：100个案例，快速验证
- 完整模式（--full）：全部案例，完整测试

用法:
    python scripts/test_advisor_v4_e2e.py [--full] [--skip-training] [--skip-optimization]
"""

import sys
from pathlib import Path
import argparse
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import traceback
import logging
import numpy as np

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config
from core.advisor_v4.data_validator import DataValidator, DataQualityConfig
from core.utils.output_manager import OutputCategory, OutputType, get_output_manager
from core.advisor_v4.factor_optimizer import FactorOptimizationConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/advisor_v4/reports/e2e_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class E2ETestResult:
    """端到端测试结果"""
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None
        self.stages = {}
        self.errors = []
        self.warnings = []
        self.summary = {}
    
    def add_stage_result(self, stage_name: str, success: bool, duration: float, details: Dict = None):
        """添加阶段结果"""
        self.stages[stage_name] = {
            'success': success,
            'duration': duration,
            'details': details or {}
        }
        if not success:
            self.errors.append(f"{stage_name}: 失败")
    
    def finalize(self):
        """完成测试"""
        self.end_time = datetime.now()
        self.total_duration = (self.end_time - self.start_time).total_seconds()
        self.success_count = sum(1 for s in self.stages.values() if s['success'])
        self.total_stages = len(self.stages)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_duration': self.total_duration if self.end_time else None,
            'stages': self.stages,
            'errors': self.errors,
            'warnings': self.warnings,
            'summary': self.summary,
            'success_rate': f"{self.success_count}/{self.total_stages}" if self.end_time else None
        }


def check_environment(full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段1: 环境检查"""
    print("\n" + "="*70)
    print("【阶段1】环境检查")
    print("="*70)
    
    results = {
        'jqdata': False,
        'gpu': False,
        'mongodb': False,
        'data_files': False,
        'python_env': False
    }
    details = {}
    
    # 1. JQData连接检查
    print("\n1. 检查JQData连接...")
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        
        if jq_config:
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            if jq.is_auth():
                results['jqdata'] = True
                # 尝试获取权限信息（可能不存在get_permission方法）
                try:
                    perm = jq.get_permission()
                    data_range = f"{perm.start_date} ~ {perm.end_date}" if hasattr(perm, 'start_date') else "N/A"
                    details['jqdata'] = {
                        'status': 'connected',
                        'data_range': data_range,
                        'username': jq_config.get('username', 'N/A')
                    }
                    print(f"   ✅ JQData: 已连接")
                    if data_range != "N/A":
                        print(f"      数据范围: {data_range}")
                except AttributeError:
                    # get_permission方法不存在，跳过
                    details['jqdata'] = {
                        'status': 'connected',
                        'username': jq_config.get('username', 'N/A')
                    }
                    print(f"   ✅ JQData: 已连接")
            else:
                print(f"   ❌ JQData: 认证失败")
        else:
            print(f"   ❌ JQData: 配置不存在")
    except Exception as e:
        print(f"   ❌ JQData: {e}")
        logger.error(f"JQData检查失败: {e}")
    
    # 2. GPU可用性检查
    print("\n2. 检查GPU可用性...")
    try:
        import torch
        if torch.cuda.is_available():
            results['gpu'] = True
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            details['gpu'] = {
                'status': 'available',
                'name': gpu_name,
                'memory_gb': round(gpu_memory, 1),
                'cuda_version': torch.version.cuda
            }
            print(f"   ✅ GPU: {gpu_name}")
            print(f"      显存: {gpu_memory:.1f} GB")
            print(f"      CUDA: {torch.version.cuda}")
        else:
            print(f"   ⚠️  GPU: 不可用（将使用CPU）")
            details['gpu'] = {'status': 'unavailable'}
    except ImportError:
        print(f"   ⚠️  GPU: PyTorch未安装（将使用CPU）")
        details['gpu'] = {'status': 'pytorch_not_installed'}
    except Exception as e:
        print(f"   ⚠️  GPU: 检查失败 - {e}")
        details['gpu'] = {'status': 'error', 'error': str(e)}
    
    # 3. MongoDB连接检查（可选）
    print("\n3. 检查MongoDB连接（可选）...")
    try:
        from core.advisor_v4.data_storage import get_v4_storage
        storage = get_v4_storage()
        if storage.is_connected():
            results['mongodb'] = True
            details['mongodb'] = {'status': 'connected'}
            print(f"   ✅ MongoDB: 已连接")
        else:
            print(f"   ⚠️  MongoDB: 未连接（可选功能）")
            details['mongodb'] = {'status': 'not_connected'}
    except Exception as e:
        print(f"   ⚠️  MongoDB: {e}（可选功能）")
        details['mongodb'] = {'status': 'error', 'error': str(e)}
    
    # 4. 数据文件检查
    print("\n4. 检查必需数据文件...")
    output_manager = get_output_manager()
    cases_file = output_manager.get_path(OutputCategory.ADVISOR_V4, "data", "high_return_cases_full_train.csv")
    
    # 如果不存在，检查results目录
    if not cases_file.exists():
        results_file = PROJECT_ROOT / "results" / "high_return_cases_full_train.csv"
        if results_file.exists():
            print(f"   ℹ️  数据文件在results目录: {results_file}")
            details['data_files'] = {'source': 'results', 'path': str(results_file)}
        else:
            print(f"   ⚠️  数据文件不存在: {cases_file}")
            print(f"      请先运行数据提取脚本生成高收益案例数据")
            details['data_files'] = {'status': 'not_found', 'expected': str(cases_file)}
    else:
        results['data_files'] = True
        file_size = cases_file.stat().st_size / 1024  # KB
        details['data_files'] = {
            'status': 'found',
            'path': str(cases_file),
            'size_kb': round(file_size, 1)
        }
        print(f"   ✅ 数据文件: {cases_file}")
        print(f"      大小: {file_size:.1f} KB")
    
    # 5. Python环境检查
    print("\n5. 检查Python环境...")
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    results['python_env'] = True
    details['python_env'] = {
        'version': python_version,
        'executable': sys.executable
    }
    print(f"   ✅ Python: {python_version}")
    print(f"      路径: {sys.executable}")
    
    # 检查关键依赖
    print("\n6. 检查关键依赖包...")
    required_packages = ['pandas', 'numpy', 'xgboost', 'sklearn', 'jqdatasdk']
    missing = []
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"   ✅ {pkg}")
        except ImportError:
            print(f"   ❌ {pkg}: 未安装")
            missing.append(pkg)
    
    if missing:
        results['python_env'] = False
        details['python_env']['missing_packages'] = missing
    
    # 汇总
    all_critical = results['jqdata'] and results['data_files'] and results['python_env']
    
    print("\n" + "="*70)
    if all_critical:
        print("✅ 环境检查通过（关键项）")
    else:
        print("⚠️  环境检查：部分关键项未通过")
    print("="*70)
    
    return all_critical, {'results': results, 'details': details}


def run_data_validation(workflow: AdvisorV4Workflow, full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段2: 数据验证和清洗"""
    print("\n" + "="*70)
    print("【阶段2】数据验证和清洗")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 读取原始数据
        cases_file = Path(workflow.config.high_return_cases_path)
        if not cases_file.exists():
            # 尝试从results目录
            results_file = PROJECT_ROOT / "results" / "high_return_cases_full_train.csv"
            if results_file.exists():
                cases_file = results_file
            else:
                raise FileNotFoundError(f"数据文件不存在: {workflow.config.high_return_cases_path}")
        
        import pandas as pd
        raw_cases_df = pd.read_csv(cases_file)
        
        print(f"原始数据: {len(raw_cases_df)} 条记录")
        
        # 快速模式：只验证前100条
        if not full_mode and len(raw_cases_df) > 100:
            print(f"快速模式：只验证前100条")
            raw_cases_df = raw_cases_df.head(100)
        
        # 验证和清洗
        validator = DataValidator(config=DataQualityConfig(), verbose=True)
        validation_result = validator.validate_and_clean(raw_cases_df)
        
        duration = time.time() - start_time
        
        if not validation_result.is_valid:
            print(f"\n❌ 数据验证未通过")
            return False, {
                'success': False,
                'duration': duration,
                'validation_result': {
                    'is_valid': False,
                    'issues': validation_result.issues
                }
            }
        
        # 保存清洗后的数据
        output_manager = get_output_manager()
        cleaned_cases_path = output_manager.get_path(
            OutputCategory.ADVISOR_V4, 
            "data", 
            "high_return_cases_cleaned.csv"
        )
        cleaned_cases_path.parent.mkdir(parents=True, exist_ok=True)
        validation_result.cleaned_data.to_csv(cleaned_cases_path, index=False, encoding='utf-8-sig')
        
        # 保存验证报告
        report_path = cleaned_cases_path.with_suffix('.validation_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(validation_result.report)
        
        print(f"\n✅ 数据验证通过")
        print(f"   数据保留率: {validation_result.valid_records/validation_result.total_records:.1%}")
        print(f"   清洗后数据: {cleaned_cases_path}")
        
        return True, {
            'success': True,
            'duration': duration,
            'validation_result': {
                'is_valid': True,
                'total_records': validation_result.total_records,
                'valid_records': validation_result.valid_records,
                'retention_rate': validation_result.valid_records/validation_result.total_records,
                'issues_count': len(validation_result.issues)
            },
            'cleaned_file': str(cleaned_cases_path)
        }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"数据验证失败: {e}", exc_info=True)
        print(f"\n❌ 数据验证失败: {e}")
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def run_model_training(workflow: AdvisorV4Workflow, full_mode: bool = False, skip_extraction: bool = False) -> Tuple[bool, Dict]:
    """阶段3: 模型训练（GPU加速）"""
    print("\n" + "="*70)
    print("【阶段3】模型训练（GPU加速）")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 快速模式：如果有已有数据就跳过提取，否则执行提取
        if not full_mode:
            # 检查预测因子文件是否存在
            pred_features_path = Path(workflow.config.predictive_features_path)
            if pred_features_path.exists():
                skip_extraction = True
                print("快速模式：使用已有预测因子文件，跳过因子提取")
            else:
                skip_extraction = False
                print("快速模式：预测因子文件不存在，将执行因子提取")
        else:
            skip_extraction = False
        
        # 运行训练
        predictor = workflow.train(
            skip_extraction=skip_extraction,
            skip_negative_sampling=False,
            use_feature_pipeline=True,
            use_cv=True,
            cv_method='walk_forward'
        )
        
        duration = time.time() - start_time
        
        # 获取训练指标
        train_metrics = None
        val_metrics = None
        if hasattr(predictor, 'train_metrics') and predictor.train_metrics:
            train_metrics = {
                'auc': predictor.train_metrics.auc,
                'accuracy': predictor.train_metrics.accuracy,
                'precision': predictor.train_metrics.precision,
                'recall': predictor.train_metrics.recall,
                'f1': predictor.train_metrics.f1
            }
        
        if hasattr(predictor, 'val_metrics') and predictor.val_metrics:
            val_metrics = {
                'auc': predictor.val_metrics.auc,
                'accuracy': predictor.val_metrics.accuracy,
                'precision': predictor.val_metrics.precision,
                'recall': predictor.val_metrics.recall,
                'f1': predictor.val_metrics.f1
            }
        
        # 过拟合检测
        overfitting_report = predictor.detect_overfitting() if hasattr(predictor, 'detect_overfitting') else None
        
        print(f"\n✅ 模型训练完成")
        if val_metrics:
            print(f"   验证集AUC: {val_metrics['auc']:.4f}")
        if overfitting_report:
            if overfitting_report.get('is_overfitting'):
                print(f"   ⚠️  过拟合风险: {overfitting_report.get('severity', 'unknown')}")
            else:
                print(f"   ✅ 模型泛化能力良好")
        
        return True, {
            'success': True,
            'duration': duration,
            'train_metrics': train_metrics,
            'val_metrics': val_metrics,
            'overfitting_report': overfitting_report,
            'model_path': workflow.config.model_path
        }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"模型训练失败: {e}", exc_info=True)
        print(f"\n❌ 模型训练失败: {e}")
        traceback.print_exc()
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def run_factor_optimization(workflow: AdvisorV4Workflow, full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段4: 因子优化（递归优化）"""
    print("\n" + "="*70)
    print("【阶段4】因子优化（递归优化）")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 快速模式：减少迭代次数
        if full_mode:
            config = FactorOptimizationConfig(
                max_iterations=5,
                enable_factor_selection=True,
                enable_weight_optimization=True,
                enable_fusion_optimization=True
            )
        else:
            config = FactorOptimizationConfig(
                max_iterations=1,  # 快速模式：只迭代1次
                enable_factor_selection=False,  # 跳过因子选择
                enable_weight_optimization=True,
                enable_fusion_optimization=False  # 跳过融合优化
            )
            print("快速模式：只进行权重优化，1次迭代")
        
        # 运行优化
        result = workflow.optimize_factors(
            start_date=workflow.config.train_start,
            end_date=workflow.config.test_end,
            config=config
        )
        
        duration = time.time() - start_time
        
        if result and result.best_result:
            best_result = result.best_result
            print(f"\n✅ 因子优化完成")
            print(f"   最佳Sharpe: {best_result.sharpe_ratio:.3f}")
            print(f"   命中率: {best_result.hit_rate:.2%}")
            print(f"   总收益率: {best_result.total_return:.2%}")
            
            return True, {
                'success': True,
                'duration': duration,
                'best_result': {
                    'sharpe_ratio': best_result.sharpe_ratio,
                    'hit_rate': best_result.hit_rate,
                    'total_return': best_result.total_return,
                    'multi_objective_score': best_result.multi_objective_score
                },
                'optimization_time': result.optimization_time_seconds
            }
        else:
            print(f"\n⚠️  因子优化未完成（无结果）")
            return False, {
                'success': False,
                'duration': duration,
                'error': '优化未产生结果'
            }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"因子优化失败: {e}", exc_info=True)
        print(f"\n❌ 因子优化失败: {e}")
        traceback.print_exc()
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def run_backtest(workflow: AdvisorV4Workflow, full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段5: 回测验证"""
    print("\n" + "="*70)
    print("【阶段5】回测验证")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 快速模式：只运行Fast层
        if full_mode:
            backtest_levels = ['fast', 'standard']  # 完整模式：Fast + Standard
        else:
            backtest_levels = ['fast']  # 快速模式：只Fast层
            print("快速模式：只运行Fast层回测")
        
        # 运行回测
        backtest_result = workflow.backtest(
            start_date=workflow.config.test_start,
            end_date=workflow.config.test_end,
            rebalance_freq='weekly',
            backtest_levels=backtest_levels,
            save_to_db=False  # 测试模式不保存到数据库
        )
        
        duration = time.time() - start_time
        
        if backtest_result:
            print(f"\n✅ 回测完成")
            print(f"   总收益率: {backtest_result.total_return:.2%}")
            print(f"   夏普比率: {backtest_result.sharpe_ratio:.3f}")
            print(f"   最大回撤: {backtest_result.max_drawdown:.2%}")
            print(f"   10%+命中率: {backtest_result.hit_10pct_rate:.2%}")
            
            return True, {
                'success': True,
                'duration': duration,
                'backtest_result': {
                    'total_return': backtest_result.total_return,
                    'sharpe_ratio': backtest_result.sharpe_ratio,
                    'max_drawdown': backtest_result.max_drawdown,
                    'hit_10pct_rate': backtest_result.hit_10pct_rate,
                    'win_rate': backtest_result.win_rate
                }
            }
        else:
            print(f"\n⚠️  回测未完成（无结果）")
            return False, {
                'success': False,
                'duration': duration,
                'error': '回测未产生结果'
            }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"回测失败: {e}", exc_info=True)
        print(f"\n❌ 回测失败: {e}")
        traceback.print_exc()
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def run_recommendation(workflow: AdvisorV4Workflow, full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段6: 推荐生成"""
    print("\n" + "="*70)
    print("【阶段6】推荐生成")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 获取当前周锚点日期
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        # 获取本周最后一个交易日作为锚点
        anchor_date = workflow.get_prev_week_anchor(today.strftime('%Y-%m-%d'))
        if anchor_date is None:
            # 如果获取失败，使用今天
            anchor_date = today.strftime('%Y-%m-%d')
        
        # 快速模式：Top 3，完整模式：Top 5
        top_n = 5 if full_mode else 3
        
        print(f"锚点日期: {anchor_date}")
        print(f"推荐数量: Top {top_n}")
        
        # 生成推荐
        layout_plan = workflow.recommend_weekly_layout(
            anchor_date=anchor_date,
            top_n=top_n
        )
        
        duration = time.time() - start_time
        
        if layout_plan and layout_plan.targets:
            print(f"\n✅ 推荐生成完成")
            print(f"   推荐数量: {len(layout_plan.targets)}")
            
            # 保存推荐
            output_manager = get_output_manager()
            rec_dir = output_manager.get_path(OutputCategory.ADVISOR_V4, "recommendations")
            rec_dir.mkdir(parents=True, exist_ok=True)
            rec_file = rec_dir / f"recommendations_{anchor_date.replace('-', '')}.json"
            
            # 修正：entry_plan 和 exit_plan 在 layout_plan 字典中，不在 LayoutTarget 对象中
            targets_data = []
            for t in layout_plan.targets:
                target_data = {
                    'code': t.code,
                    'name': t.name,
                    'score': float(t.score),
                    'reason': t.reason,
                    'tags': list(t.tags) if hasattr(t, 'tags') else [],
                }
                
                # 获取 entry_plan（从 layout_plan.entry_plan 字典中，key 是股票代码）
                entry_plan_obj = layout_plan.entry_plan.get(t.code) if layout_plan.entry_plan else None
                if entry_plan_obj:
                    # EntryPlan 对象转字典
                    stages = []
                    if hasattr(entry_plan_obj, 'stages') and entry_plan_obj.stages:
                        for s in entry_plan_obj.stages:
                            if isinstance(s, dict):
                                stages.append({
                                    'price': float(s.get('price', 0)),
                                    'quantity': float(s.get('quantity', 0))
                                })
                            else:
                                # 如果是对象，尝试提取属性
                                price = getattr(s, 'price', 0)
                                quantity = getattr(s, 'quantity', 0)
                                stages.append({
                                    'price': float(price) if price else 0,
                                    'quantity': float(quantity) if quantity else 0
                                })
                    
                    target_data['entry_plan'] = {
                        'plan_type': getattr(entry_plan_obj, 'plan_type', 'staged'),
                        'stages': stages
                    }
                else:
                    target_data['entry_plan'] = None
                
                # 获取 exit_plan（从 layout_plan.exit_plan 字典中，key 是股票代码）
                exit_plan_obj = layout_plan.exit_plan.get(t.code) if layout_plan.exit_plan else None
                if exit_plan_obj:
                    target_data['exit_plan'] = {
                        'take_profit': float(getattr(exit_plan_obj, 'take_profit', 0.15)),
                        'stop_loss': float(getattr(exit_plan_obj, 'stop_loss', -0.08)),
                        'trailing_stop': float(getattr(exit_plan_obj, 'trailing_stop', 0.03)),
                        'time_stop_days': int(getattr(exit_plan_obj, 'time_stop_days', 10))
                    }
                else:
                    target_data['exit_plan'] = None
                
                targets_data.append(target_data)
            
            rec_data = {
                'anchor_date': anchor_date,
                'targets': targets_data
            }
            
            with open(rec_file, 'w', encoding='utf-8') as f:
                json.dump(rec_data, f, ensure_ascii=False, indent=2)
            
            print(f"   推荐文件: {rec_file}")
            
            return True, {
                'success': True,
                'duration': duration,
                'recommendations_count': len(layout_plan.targets),
                'recommendations_file': str(rec_file),
                'anchor_date': anchor_date
            }
        else:
            print(f"\n⚠️  推荐生成未完成（无推荐）")
            return False, {
                'success': False,
                'duration': duration,
                'error': '未生成推荐'
            }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"推荐生成失败: {e}", exc_info=True)
        print(f"\n❌ 推荐生成失败: {e}")
        traceback.print_exc()
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def generate_report(workflow: AdvisorV4Workflow, test_result: E2ETestResult, full_mode: bool = False) -> Tuple[bool, Dict]:
    """阶段7: 报告生成"""
    print("\n" + "="*70)
    print("【阶段7】报告生成")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 获取当前周锚点日期
        from datetime import datetime, timedelta
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        
        try:
            if hasattr(workflow, 'jq') and workflow.jq:
                anchor_date = workflow.get_prev_week_anchor(today_str)
            else:
                # 如果没有JQData，使用简单计算
                dt = datetime.strptime(today_str, '%Y-%m-%d').date()
                this_week_start = dt - timedelta(days=dt.weekday())
                prev_week_end = this_week_start - timedelta(days=1)
                anchor_date = prev_week_end.strftime('%Y-%m-%d')
            
            if anchor_date is None:
                anchor_date = today_str
        except Exception as e:
            logger.warning(f"获取锚点日期失败: {e}，使用今天")
            anchor_date = today_str
        
        # 快速模式：Top 3，完整模式：Top 5
        top_n = 5 if full_mode else 3
        
        # 生成周度布局报告（快速模式减少股票数量）
        report_path = workflow.generate_weekly_layout_report(
            anchor_date=anchor_date,
            top_n=top_n,
            fast_mode=not full_mode  # 快速模式启用fast_mode
        )
        
        duration = time.time() - start_time
        
        if report_path and Path(report_path).exists():
            print(f"\n✅ 报告生成完成")
            print(f"   报告路径: {report_path}")
            
            return True, {
                'success': True,
                'duration': duration,
                'report_path': str(report_path)
            }
        else:
            print(f"\n⚠️  报告生成未完成")
            return False, {
                'success': False,
                'duration': duration,
                'error': '报告文件不存在'
            }
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"报告生成失败: {e}", exc_info=True)
        print(f"\n❌ 报告生成失败: {e}")
        traceback.print_exc()
        return False, {
            'success': False,
            'duration': duration,
            'error': str(e)
        }


def generate_summary(test_result: E2ETestResult, full_mode: bool = False) -> Dict:
    """阶段8: 结果汇总"""
    print("\n" + "="*70)
    print("【阶段8】结果汇总")
    print("="*70)
    
    test_result.finalize()
    
    # 生成汇总报告
    summary = {
        'test_mode': 'full' if full_mode else 'quick',
        'start_time': test_result.start_time.isoformat(),
        'end_time': test_result.end_time.isoformat(),
        'total_duration_seconds': test_result.total_duration,
        'total_duration_minutes': round(test_result.total_duration / 60, 1),
        'stages': {},
        'summary': {
            'total_stages': test_result.total_stages,
            'successful_stages': test_result.success_count,
            'failed_stages': test_result.total_stages - test_result.success_count,
            'success_rate': f"{test_result.success_count}/{test_result.total_stages}"
        },
        'errors': test_result.errors,
        'warnings': test_result.warnings
    }
    
    # 汇总各阶段结果
    for stage_name, stage_result in test_result.stages.items():
        summary['stages'][stage_name] = {
            'success': stage_result['success'],
            'duration_seconds': round(stage_result['duration'], 2),
            'details': stage_result.get('details', {})
        }
    
    # 保存汇总报告
    output_manager = get_output_manager()
    report_dir = output_manager.get_path(OutputCategory.ADVISOR_V4, "reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = report_dir / f"e2e_test_summary_{timestamp}.json"
    
    # 转换numpy类型为Python原生类型（用于JSON序列化）
    def convert_numpy_types(obj):
        """递归转换numpy类型为Python原生类型"""
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj) if isinstance(obj, np.floating) else int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'item'):  # numpy标量
            return obj.item()
        else:
            return obj
    
    summary = convert_numpy_types(summary)
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 打印汇总
    print(f"\n测试汇总:")
    print(f"  测试模式: {'完整模式' if full_mode else '快速模式'}")
    print(f"  总耗时: {summary['total_duration_minutes']:.1f} 分钟")
    print(f"  成功阶段: {summary['summary']['successful_stages']}/{summary['summary']['total_stages']}")
    print(f"  失败阶段: {summary['summary']['failed_stages']}")
    
    print(f"\n各阶段耗时:")
    for stage_name, stage_data in summary['stages'].items():
        status = "✅" if stage_data['success'] else "❌"
        print(f"  {status} {stage_name}: {stage_data['duration_seconds']:.1f}秒")
    
    if test_result.errors:
        print(f"\n错误列表:")
        for error in test_result.errors:
            print(f"  - {error}")
    
    print(f"\n汇总报告: {summary_file}")
    
    return summary


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Investment Advisor V4.0 端到端测试")
    parser.add_argument('--full', action='store_true', help='完整测试模式（默认：快速模式）')
    parser.add_argument('--skip-training', action='store_true', help='跳过模型训练')
    parser.add_argument('--skip-optimization', action='store_true', help='跳过因子优化')
    parser.add_argument('--skip-backtest', action='store_true', help='跳过回测验证')
    parser.add_argument('--skip-recommendation', action='store_true', help='跳过推荐生成')
    
    args = parser.parse_args()
    
    print("="*70)
    print("Investment Advisor V4.0 端到端测试")
    print("="*70)
    print(f"测试模式: {'完整模式' if args.full else '快速模式'}")
    print(f"跳过项: ", end="")
    skips = []
    if args.skip_training:
        skips.append("训练")
    if args.skip_optimization:
        skips.append("优化")
    if args.skip_backtest:
        skips.append("回测")
    if args.skip_recommendation:
        skips.append("推荐")
    print(", ".join(skips) if skips else "无")
    print("="*70)
    
    # 初始化测试结果
    test_result = E2ETestResult()
    
    # 阶段1: 环境检查
    env_ok, env_details = check_environment(args.full)
    test_result.add_stage_result('环境检查', env_ok, 0, env_details)
    
    if not env_ok:
        print("\n❌ 环境检查未通过，请修复后重试")
        generate_summary(test_result, args.full)
        return 1
    
    # 初始化工作流
    try:
        config = AdvisorV4Config()
        workflow = AdvisorV4Workflow(config=config, verbose=True)
    except Exception as e:
        logger.error(f"工作流初始化失败: {e}", exc_info=True)
        print(f"\n❌ 工作流初始化失败: {e}")
        test_result.add_stage_result('工作流初始化', False, 0, {'error': str(e)})
        generate_summary(test_result, args.full)
        return 1
    
    # 阶段2: 数据验证和清洗
    validation_ok, validation_details = run_data_validation(workflow, args.full)
    test_result.add_stage_result('数据验证和清洗', validation_ok, validation_details.get('duration', 0), validation_details)
    
    # 更新工作流使用清洗后的数据
    if validation_ok and 'cleaned_file' in validation_details:
        workflow.config.high_return_cases_path = validation_details['cleaned_file']
    
    # 阶段3: 模型训练
    if not args.skip_training:
        training_ok, training_details = run_model_training(workflow, args.full, skip_extraction=not args.full)
        test_result.add_stage_result('模型训练', training_ok, training_details.get('duration', 0), training_details)
    else:
        print("\n⏭️  跳过模型训练")
        test_result.add_stage_result('模型训练', True, 0, {'skipped': True})
    
    # 阶段4: 因子优化
    if not args.skip_optimization:
        optimization_ok, optimization_details = run_factor_optimization(workflow, args.full)
        test_result.add_stage_result('因子优化', optimization_ok, optimization_details.get('duration', 0), optimization_details)
    else:
        print("\n⏭️  跳过因子优化")
        test_result.add_stage_result('因子优化', True, 0, {'skipped': True})
    
    # 阶段5: 回测验证
    if not args.skip_backtest:
        backtest_ok, backtest_details = run_backtest(workflow, args.full)
        test_result.add_stage_result('回测验证', backtest_ok, backtest_details.get('duration', 0), backtest_details)
    else:
        print("\n⏭️  跳过回测验证")
        test_result.add_stage_result('回测验证', True, 0, {'skipped': True})
    
    # 阶段6: 推荐生成
    if not args.skip_recommendation:
        recommendation_ok, recommendation_details = run_recommendation(workflow, args.full)
        test_result.add_stage_result('推荐生成', recommendation_ok, recommendation_details.get('duration', 0), recommendation_details)
    else:
        print("\n⏭️  跳过推荐生成")
        test_result.add_stage_result('推荐生成', True, 0, {'skipped': True})
    
    # 阶段7: 报告生成
    report_ok, report_details = generate_report(workflow, test_result, args.full)
    test_result.add_stage_result('报告生成', report_ok, report_details.get('duration', 0), report_details)
    
    # 阶段8: 结果汇总
    summary = generate_summary(test_result, args.full)
    
    # 返回状态码
    if test_result.success_count == test_result.total_stages:
        print("\n" + "="*70)
        print("✅ 端到端测试全部通过！")
        print("="*70)
        return 0
    else:
        print("\n" + "="*70)
        print(f"⚠️  端到端测试部分失败: {test_result.success_count}/{test_result.total_stages}")
        print("="*70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
