#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
回测结果迁移工具
================

将output/目录下的JSON回测结果文件迁移到MongoDB。

功能:
- 扫描output/目录下的JSON文件
- 解析JSON文件，转换为EnhancedBacktestResult对象
- 保存到MongoDB（带版本信息）
- 可选：将已迁移的文件移动到archive目录

使用方式:
    python scripts/migrate_backtest_results.py [--dry-run] [--archive]
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.market_trend_storage import MarketTrendStorage
from core.signal_backtest import EnhancedBacktestResult, BacktestConfig, EnhancedSignalRecord
from core.signal_backtest import SignalType, MarketStateCategory

logger = logging.getLogger(__name__)


def parse_json_to_result(json_data: Dict[str, Any], source_file: str) -> Optional[EnhancedBacktestResult]:
    """
    将JSON数据转换为EnhancedBacktestResult对象
    
    Args:
        json_data: JSON数据字典
        source_file: 源文件路径（用于日志）
        
    Returns:
        EnhancedBacktestResult对象，失败返回None
    """
    try:
        # 重建config
        config_dict = json_data.get('config', {})
        config = BacktestConfig(**config_dict)
        
        # 重建signals
        signals = []
        for sig_data in json_data.get('signals', []):
            try:
                # 转换信号类型
                signal_type = SignalType(sig_data.get('signal_type', 'neutral'))
                short_term_signal = SignalType(sig_data.get('short_term_signal', 'neutral'))
                medium_term_signal = SignalType(sig_data.get('medium_term_signal', 'neutral'))
                long_term_signal = SignalType(sig_data.get('long_term_signal', 'neutral'))
                state_category = MarketStateCategory(sig_data.get('state_category', 'VOLATILE'))
                
                signal = EnhancedSignalRecord(
                    date=sig_data['date'],
                    signal_type=signal_type,
                    composite_score=sig_data.get('composite_score', 0.0),
                    short_term_signal=short_term_signal,
                    medium_term_signal=medium_term_signal,
                    long_term_signal=long_term_signal,
                    short_term_score=sig_data.get('short_term_score', 0.0),
                    medium_term_score=sig_data.get('medium_term_score', 0.0),
                    long_term_score=sig_data.get('long_term_score', 0.0),
                    north_fund_score=sig_data.get('north_fund_score', 0.0),
                    margin_score=sig_data.get('margin_score', 0.0),
                    breadth_score=sig_data.get('breadth_score', 0.0),
                    market_state=sig_data.get('market_state', '未知'),
                    state_category=state_category,
                    hmm_state=sig_data.get('hmm_state', 'unknown'),
                    hmm_confidence=sig_data.get('hmm_confidence', 0.0),
                    hmm_signal_aligned=sig_data.get('hmm_signal_aligned', False),
                    ibd_market_status=sig_data.get('ibd_market_status', 'unknown'),
                    ibd_distribution_count=sig_data.get('ibd_distribution_count', 0),
                    ibd_has_ftd=sig_data.get('ibd_has_ftd', False),
                    ibd_signal_aligned=sig_data.get('ibd_signal_aligned', False),
                    model_consensus=sig_data.get('model_consensus', 0),
                    bullish_votes=sig_data.get('bullish_votes', 0.0),
                    bearish_votes=sig_data.get('bearish_votes', 0.0),
                    high_confidence=sig_data.get('high_confidence', False),
                    medium_confidence=sig_data.get('medium_confidence', False),
                    confidence_level=sig_data.get('confidence_level', 'low'),
                    returns_5d=sig_data.get('returns_5d', 0.0),
                    returns_10d=sig_data.get('returns_10d', 0.0),
                    returns_20d=sig_data.get('returns_20d', 0.0),
                    returns_60d=sig_data.get('returns_60d', 0.0),
                    correct_5d=sig_data.get('correct_5d', False),
                    correct_10d=sig_data.get('correct_10d', False),
                    correct_20d=sig_data.get('correct_20d', False),
                    correct_60d=sig_data.get('correct_60d', False),
                    short_correct_5d=sig_data.get('short_correct_5d', False),
                    medium_correct_20d=sig_data.get('medium_correct_20d', False),
                    long_correct_60d=sig_data.get('long_correct_60d', False),
                    state_correct_60d=sig_data.get('state_correct_60d', False),
                )
                signals.append(signal)
            except Exception as e:
                logger.warning(f"解析信号失败，跳过: {e}")
                continue
        
        # 重建result对象
        result = EnhancedBacktestResult(
            config=config,
            phase=json_data.get('phase', 'unknown'),
            total_signals=json_data.get('total_signals', 0),
            bullish_signals=json_data.get('bullish_signals', 0),
            bearish_signals=json_data.get('bearish_signals', 0),
            neutral_signals=json_data.get('neutral_signals', 0),
            accuracy_5d=json_data.get('accuracy_5d', 0.0),
            accuracy_10d=json_data.get('accuracy_10d', 0.0),
            accuracy_20d=json_data.get('accuracy_20d', 0.0),
            accuracy_60d=json_data.get('accuracy_60d', 0.0),
            short_accuracy_5d=json_data.get('short_accuracy_5d', 0.0),
            short_bullish_accuracy=json_data.get('short_bullish_accuracy', 0.0),
            short_bearish_accuracy=json_data.get('short_bearish_accuracy', 0.0),
            medium_accuracy_20d=json_data.get('medium_accuracy_20d', 0.0),
            medium_bullish_accuracy=json_data.get('medium_bullish_accuracy', 0.0),
            medium_bearish_accuracy=json_data.get('medium_bearish_accuracy', 0.0),
            long_accuracy_60d=json_data.get('long_accuracy_60d', 0.0),
            long_bullish_accuracy=json_data.get('long_bullish_accuracy', 0.0),
            long_bearish_accuracy=json_data.get('long_bearish_accuracy', 0.0),
            state_accuracy_60d=json_data.get('state_accuracy_60d', 0.0),
            bull_state_accuracy=json_data.get('bull_state_accuracy', 0.0),
            bear_state_accuracy=json_data.get('bear_state_accuracy', 0.0),
            volatile_state_accuracy=json_data.get('volatile_state_accuracy', 0.0),
            avg_return_bullish_5d=json_data.get('avg_return_bullish_5d', 0.0),
            avg_return_bullish_20d=json_data.get('avg_return_bullish_20d', 0.0),
            avg_return_bearish_5d=json_data.get('avg_return_bearish_5d', 0.0),
            avg_return_bearish_20d=json_data.get('avg_return_bearish_20d', 0.0),
            win_rate_bullish=json_data.get('win_rate_bullish', 0.0),
            win_rate_bearish=json_data.get('win_rate_bearish', 0.0),
            hmm_aligned_signals=json_data.get('hmm_aligned_signals', 0),
            ibd_aligned_signals=json_data.get('ibd_aligned_signals', 0),
            high_confidence_signals=json_data.get('high_confidence_signals', 0),
            medium_confidence_signals=json_data.get('medium_confidence_signals', 0),
            low_confidence_signals=json_data.get('low_confidence_signals', 0),
            high_confidence_accuracy_5d=json_data.get('high_confidence_accuracy_5d', 0.0),
            high_confidence_accuracy_20d=json_data.get('high_confidence_accuracy_20d', 0.0),
            high_confidence_accuracy_60d=json_data.get('high_confidence_accuracy_60d', 0.0),
            medium_confidence_accuracy_5d=json_data.get('medium_confidence_accuracy_5d', 0.0),
            medium_confidence_accuracy_20d=json_data.get('medium_confidence_accuracy_20d', 0.0),
            low_confidence_accuracy_5d=json_data.get('low_confidence_accuracy_5d', 0.0),
            low_confidence_accuracy_20d=json_data.get('low_confidence_accuracy_20d', 0.0),
            hmm_aligned_accuracy_5d=json_data.get('hmm_aligned_accuracy_5d', 0.0),
            hmm_aligned_accuracy_20d=json_data.get('hmm_aligned_accuracy_20d', 0.0),
            ibd_aligned_accuracy_5d=json_data.get('ibd_aligned_accuracy_5d', 0.0),
            ibd_aligned_accuracy_20d=json_data.get('ibd_aligned_accuracy_20d', 0.0),
            signals=signals,
            yearly_stats=json_data.get('yearly_stats', {}),
            backtest_time=json_data.get('backtest_time', ''),
            duration_seconds=json_data.get('duration_seconds', 0.0)
        )
        
        return result
        
    except Exception as e:
        logger.error(f"解析JSON文件失败 {source_file}: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return None


def determine_backtest_type(phase: str, file_name: str) -> str:
    """
    根据phase和文件名确定backtest_type
    
    Args:
        phase: 结果的phase字段
        file_name: 文件名
        
    Returns:
        backtest_type字符串
    """
    if 'phase1' in phase.lower() or 'phase1' in file_name.lower():
        return 'signal_phase1'
    elif 'phase2' in phase.lower() or 'phase2' in file_name.lower():
        return 'signal_phase2'
    else:
        # 根据时间范围推断
        return 'signal_phase1'  # 默认


def migrate_backtest_results(dry_run: bool = False, archive: bool = False) -> Dict[str, Any]:
    """
    迁移回测结果
    
    Args:
        dry_run: 是否为预览模式（不实际保存）
        archive: 是否将已迁移的文件移动到archive目录
        
    Returns:
        迁移结果统计
    """
    output_dir = project_root / "output"
    archive_dir = output_dir / "backtest_archive"
    
    if not output_dir.exists():
        logger.warning(f"output目录不存在: {output_dir}")
        return {'success': 0, 'failed': 0, 'skipped': 0}
    
    # 创建archive目录（如果启用）
    if archive and not dry_run:
        archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 扫描JSON文件
    json_files = list(output_dir.glob("*.json"))
    # 排除一些非回测结果文件
    excluded_patterns = ['reports_index.json', 'config']
    json_files = [f for f in json_files if not any(pattern in f.name for pattern in excluded_patterns)]
    
    logger.info(f"找到 {len(json_files)} 个JSON文件")
    
    # 初始化存储
    storage = MarketTrendStorage()
    if not storage.is_connected():
        logger.error("MongoDB未连接，无法迁移")
        return {'success': 0, 'failed': 0, 'skipped': 0, 'error': 'MongoDB未连接'}
    
    stats = {'success': 0, 'failed': 0, 'skipped': 0, 'files': []}
    
    for json_file in json_files:
        logger.info(f"\n处理文件: {json_file.name}")
        
        try:
            # 读取JSON文件
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 解析为EnhancedBacktestResult对象
            result = parse_json_to_result(json_data, str(json_file))
            if not result:
                logger.warning(f"无法解析文件: {json_file.name}")
                stats['failed'] += 1
                stats['files'].append({'file': json_file.name, 'status': 'failed', 'reason': '解析失败'})
                continue
            
            # 确定backtest_type
            backtest_type = determine_backtest_type(result.phase, json_file.name)
            
            # 构建config字典
            config_dict = result.config.to_dict()
            
            # 检查是否已存在（基于config_hash，不考虑版本）
            config_hash = storage._compute_config_hash(config_dict)
            existing = storage.db[storage.BACKTEST_COLLECTION].find_one({
                'backtest_type': backtest_type,
                'config_hash': config_hash
            })
            
            if existing and not dry_run:
                logger.info(f"结果已存在（ID: {existing['_id']}），跳过")
                stats['skipped'] += 1
                stats['files'].append({
                    'file': json_file.name,
                    'status': 'skipped',
                    'reason': '结果已存在',
                    'result_id': str(existing['_id'])
                })
                continue
            
            if dry_run:
                logger.info(f"[预览] 将迁移: {json_file.name} -> backtest_type={backtest_type}")
                stats['success'] += 1
                stats['files'].append({'file': json_file.name, 'status': 'preview'})
                continue
            
            # 保存到MongoDB（使用legacy版本标识）
            # 注意：save_backtest_result会自动计算算法版本，但我们无法直接设置版本标签
            # 这里使用use_cache=False确保总是保存新记录
            result_id = storage.save_backtest_result(
                result=result,
                config=config_dict,
                backtest_type=backtest_type,
                use_cache=False  # 迁移时不使用缓存检查，总是保存
            )
            
            # 如果保存成功，更新文档添加迁移信息
            if result_id:
                from bson import ObjectId
                storage.db[storage.BACKTEST_COLLECTION].update_one(
                    {'_id': ObjectId(result_id)},
                    {
                        '$set': {
                            'algorithm_version': 'vlegacy',  # 标记为legacy版本
                            'version_tag': None,
                            'migrated_from': str(json_file.relative_to(project_root))
                        }
                    }
                )
            
            if result_id:
                logger.info(f"✅ 迁移成功: {json_file.name} -> ID={result_id}")
                stats['success'] += 1
                stats['files'].append({
                    'file': json_file.name,
                    'status': 'success',
                    'result_id': result_id
                })
                
                # 移动到archive目录
                if archive:
                    archive_path = archive_dir / json_file.name
                    json_file.rename(archive_path)
                    logger.info(f"文件已移动到: {archive_path}")
            else:
                logger.error(f"迁移失败: {json_file.name}")
                stats['failed'] += 1
                stats['files'].append({'file': json_file.name, 'status': 'failed', 'reason': '保存失败'})
                
        except Exception as e:
            logger.error(f"处理文件失败 {json_file.name}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            stats['failed'] += 1
            stats['files'].append({'file': json_file.name, 'status': 'failed', 'reason': str(e)})
    
    return stats


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='迁移回测结果到MongoDB')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际保存')
    parser.add_argument('--archive', action='store_true', help='迁移后将文件移动到archive目录')
    
    args = parser.parse_args()
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("回测结果迁移工具")
    print("=" * 60)
    
    if args.dry_run:
        print("\n⚠️  预览模式：不会实际保存到数据库")
    
    if args.archive:
        print("📁 迁移后将文件移动到archive目录")
    
    print("\n开始迁移...\n")
    
    stats = migrate_backtest_results(dry_run=args.dry_run, archive=args.archive)
    
    print("\n" + "=" * 60)
    print("迁移结果统计")
    print("=" * 60)
    print(f"成功: {stats['success']}")
    print(f"失败: {stats['failed']}")
    print(f"跳过: {stats['skipped']}")
    
    if stats.get('files'):
        print("\n文件详情:")
        for file_info in stats['files']:
            status = file_info['status']
            file_name = file_info['file']
            if status == 'success':
                result_id = file_info.get('result_id', 'N/A')
                print(f"  ✅ {file_name} -> {result_id}")
            elif status == 'skipped':
                reason = file_info.get('reason', 'N/A')
                print(f"  ⏭️  {file_name} ({reason})")
            elif status == 'preview':
                print(f"  👁️  {file_name} (预览)")
            else:
                reason = file_info.get('reason', 'N/A')
                print(f"  ❌ {file_name} ({reason})")


if __name__ == "__main__":
    main()

