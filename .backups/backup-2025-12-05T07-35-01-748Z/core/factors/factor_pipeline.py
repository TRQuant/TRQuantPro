# -*- coding: utf-8 -*-
"""
因子自动化计算流程
==================

根据《补充因子构建模块完善建议》，实现：
- 定期自动计算因子值
- 存入数据库/文件
- 错误重试和日志记录
- 数据质量检查

使用方式：
1. 命令行运行：python -m core.factors.factor_pipeline
2. 定时任务：配置cron每日收盘后执行
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import logging
import time
import json

from .factor_manager import FactorManager
from .factor_storage import FactorStorage
from .factor_neutralizer import FactorNeutralizer, FactorCorrelationAnalyzer
from .factor_evaluator import FactorEvaluator

logger = logging.getLogger(__name__)


class FactorPipeline:
    """
    因子计算流水线
    
    自动化完成：
    1. 数据获取与检查
    2. 因子计算
    3. 中性化处理（可选）
    4. 存储到数据库
    5. 绩效监控更新
    """
    
    def __init__(
        self,
        jq_client=None,
        factor_manager: Optional[FactorManager] = None,
        factor_storage: Optional[FactorStorage] = None,
        stock_pool: str = 'all_a',  # 'all_a', 'hs300', 'zz500', 'zz1000'
        neutralize: bool = True,
        log_dir: Optional[Path] = None
    ):
        """
        初始化流水线
        
        Args:
            jq_client: JQData客户端
            factor_manager: 因子管理器
            factor_storage: 因子存储
            stock_pool: 股票池
            neutralize: 是否进行中性化处理
            log_dir: 日志目录
        """
        self.jq_client = jq_client
        
        self.factor_manager = factor_manager or FactorManager(jq_client=jq_client)
        self.factor_storage = factor_storage or FactorStorage()
        self.neutralizer = FactorNeutralizer(jq_client=jq_client)
        self.evaluator = FactorEvaluator(jq_client=jq_client)
        
        self.stock_pool = stock_pool
        self.neutralize = neutralize
        
        self.log_dir = log_dir or Path.home() / '.local/share/trquant/logs/factors'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 运行统计
        self.run_stats = {
            'start_time': None,
            'end_time': None,
            'total_stocks': 0,
            'success_factors': 0,
            'failed_factors': 0,
            'skipped_stocks': 0,
            'errors': []
        }
    
    def set_jq_client(self, jq_client):
        """设置JQData客户端"""
        self.jq_client = jq_client
        self.factor_manager.set_jq_client(jq_client)
        self.neutralizer.jq_client = jq_client
        self.evaluator.jq_client = jq_client
    
    def get_stock_pool(self, date: Union[str, datetime]) -> List[str]:
        """
        获取股票池
        
        Args:
            date: 日期
        
        Returns:
            List[str]: 股票列表
        """
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        import jqdatasdk as jq
        
        if self.stock_pool == 'hs300':
            return jq.get_index_stocks('000300.XSHG', date=date)
        elif self.stock_pool == 'zz500':
            return jq.get_index_stocks('000905.XSHG', date=date)
        elif self.stock_pool == 'zz1000':
            return jq.get_index_stocks('000852.XSHG', date=date)
        else:  # all_a
            securities = jq.get_all_securities(types=['stock'], date=date)
            return securities.index.tolist()
    
    def filter_stocks(
        self,
        stocks: List[str],
        date: Union[str, datetime]
    ) -> List[str]:
        """
        过滤股票（ST、停牌、上市不足等）
        
        Args:
            stocks: 股票列表
            date: 日期
        
        Returns:
            List[str]: 过滤后的股票列表
        """
        if self.jq_client is None:
            return stocks
        
        import jqdatasdk as jq
        
        filtered = []
        
        try:
            # 过滤ST
            st_info = jq.get_extras('is_st', stocks, end_date=date, count=1)
            if not st_info.empty:
                st_stocks = st_info.iloc[0][st_info.iloc[0] == True].index.tolist()
            else:
                st_stocks = []
            
            # 过滤停牌
            paused_info = jq.get_price(
                stocks, end_date=date, count=1, 
                fields=['paused'], panel=False
            )
            if not paused_info.empty:
                paused_stocks = paused_info[paused_info['paused'] == 1]['code'].tolist()
            else:
                paused_stocks = []
            
            filtered = [s for s in stocks if s not in st_stocks and s not in paused_stocks]
            
            self.run_stats['skipped_stocks'] = len(stocks) - len(filtered)
            logger.info(f"股票过滤: {len(stocks)} -> {len(filtered)} "
                       f"(ST: {len(st_stocks)}, 停牌: {len(paused_stocks)})")
            
        except Exception as e:
            logger.warning(f"股票过滤失败: {e}")
            filtered = stocks
        
        return filtered
    
    def run_daily(
        self,
        date: Optional[Union[str, datetime]] = None,
        factor_names: Optional[List[str]] = None,
        save_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        运行每日因子计算
        
        Args:
            date: 计算日期（默认今天）
            factor_names: 因子名称列表（默认所有因子）
            save_to_db: 是否保存到数据库
        
        Returns:
            Dict: 运行结果
        """
        self.run_stats = {
            'start_time': datetime.now(),
            'end_time': None,
            'total_stocks': 0,
            'success_factors': 0,
            'failed_factors': 0,
            'skipped_stocks': 0,
            'errors': []
        }
        
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        logger.info(f"========== 开始因子计算 {date.strftime('%Y-%m-%d')} ==========")
        
        # 获取股票池
        try:
            stocks = self.get_stock_pool(date)
            stocks = self.filter_stocks(stocks, date)
            self.run_stats['total_stocks'] = len(stocks)
            logger.info(f"股票池: {len(stocks)}只股票")
        except Exception as e:
            logger.error(f"获取股票池失败: {e}")
            self.run_stats['errors'].append(f"获取股票池失败: {e}")
            self.run_stats['end_time'] = datetime.now()
            return self.run_stats
        
        if not stocks:
            logger.warning("股票池为空")
            self.run_stats['end_time'] = datetime.now()
            return self.run_stats
        
        # 获取因子列表
        if factor_names is None:
            factor_names = self.factor_manager.list_factors()
        
        # 计算每个因子
        factor_results = {}
        
        for factor_name in factor_names:
            try:
                logger.info(f"计算因子: {factor_name}")
                
                result = self.factor_manager.calculate_factor(
                    factor_name, stocks, date,
                    winsorize=True, standardize=True
                )
                
                if result and result.valid_count > 0:
                    factor_results[factor_name] = result.values
                    self.run_stats['success_factors'] += 1
                    logger.info(f"  ✅ {factor_name}: 有效值 {result.valid_count}/{len(stocks)}")
                else:
                    self.run_stats['failed_factors'] += 1
                    logger.warning(f"  ❌ {factor_name}: 无有效值")
                
            except Exception as e:
                self.run_stats['failed_factors'] += 1
                self.run_stats['errors'].append(f"{factor_name}: {e}")
                logger.error(f"  ❌ {factor_name}: {e}")
        
        # 中性化处理
        if self.neutralize and factor_results:
            logger.info("进行因子中性化...")
            try:
                factor_results = self.neutralizer.neutralize_batch(
                    factor_results, stocks, date,
                    neutralize_industry=True,
                    neutralize_size=True
                )
                logger.info("因子中性化完成")
            except Exception as e:
                logger.warning(f"中性化失败: {e}")
        
        # 保存到数据库
        if save_to_db and factor_results:
            logger.info("保存因子值到数据库...")
            for factor_name, values in factor_results.items():
                try:
                    self.factor_storage.save_factor_values(factor_name, date, values)
                except Exception as e:
                    logger.warning(f"保存失败 {factor_name}: {e}")
        
        # 记录运行日志
        self.run_stats['end_time'] = datetime.now()
        self._save_run_log(date)
        
        duration = (self.run_stats['end_time'] - self.run_stats['start_time']).total_seconds()
        logger.info(f"========== 因子计算完成 耗时: {duration:.1f}秒 ==========")
        logger.info(f"成功: {self.run_stats['success_factors']}, "
                   f"失败: {self.run_stats['failed_factors']}")
        
        return self.run_stats
    
    def run_monthly_evaluation(
        self,
        date: Optional[Union[str, datetime]] = None,
        lookback_months: int = 12
    ) -> Dict[str, Any]:
        """
        运行月度因子评估
        
        Args:
            date: 评估日期
            lookback_months: 回看月数
        
        Returns:
            Dict: 评估结果
        """
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        start_date = date - timedelta(days=lookback_months * 30)
        
        logger.info(f"运行因子月度评估: {start_date.strftime('%Y-%m-%d')} ~ {date.strftime('%Y-%m-%d')}")
        
        stocks = self.get_stock_pool(date)
        stocks = self.filter_stocks(stocks, date)
        
        evaluation_results = {}
        
        for factor_name in self.factor_manager.list_factors():
            try:
                factor = self.factor_manager.get_factor(factor_name)
                if factor is None:
                    continue
                
                # 评估因子
                performance = self.evaluator.evaluate_factor(
                    factor, stocks, start_date, date
                )
                
                evaluation_results[factor_name] = performance.to_dict()
                
                # 保存绩效记录
                self.factor_storage.save_factor_performance(
                    factor_name=factor_name,
                    date=date,
                    ic=performance.ic_mean,
                    ic_ir=performance.ic_ir,
                    group_returns={},
                    long_short_return=performance.long_short_return,
                    status=performance.status
                )
                
                logger.info(f"评估 {factor_name}: IC={performance.ic_mean:.4f}, "
                           f"IR={performance.ic_ir:.2f}, 状态={performance.status}")
                
            except Exception as e:
                logger.warning(f"评估失败 {factor_name}: {e}")
        
        return evaluation_results
    
    def _save_run_log(self, date: datetime):
        """保存运行日志"""
        log_file = self.log_dir / f"factor_run_{date.strftime('%Y%m%d')}.json"
        
        log_data = {
            'date': date.strftime('%Y-%m-%d'),
            'start_time': self.run_stats['start_time'].isoformat(),
            'end_time': self.run_stats['end_time'].isoformat(),
            'duration_seconds': (self.run_stats['end_time'] - self.run_stats['start_time']).total_seconds(),
            'total_stocks': self.run_stats['total_stocks'],
            'success_factors': self.run_stats['success_factors'],
            'failed_factors': self.run_stats['failed_factors'],
            'skipped_stocks': self.run_stats['skipped_stocks'],
            'errors': self.run_stats['errors']
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    def get_run_history(self, days: int = 30) -> pd.DataFrame:
        """获取运行历史"""
        records = []
        
        for log_file in sorted(self.log_dir.glob("factor_run_*.json"), reverse=True)[:days]:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    records.append(json.load(f))
            except:
                pass
        
        if records:
            return pd.DataFrame(records)
        return pd.DataFrame()


# 便捷函数
def create_factor_pipeline(jq_client=None, stock_pool='hs300') -> FactorPipeline:
    """创建因子流水线"""
    return FactorPipeline(jq_client=jq_client, stock_pool=stock_pool)


# 命令行入口
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='因子自动计算流水线')
    parser.add_argument('--date', type=str, help='计算日期 (YYYY-MM-DD)')
    parser.add_argument('--pool', type=str, default='hs300', 
                       choices=['all_a', 'hs300', 'zz500', 'zz1000'],
                       help='股票池')
    parser.add_argument('--no-neutralize', action='store_true', help='不进行中性化')
    parser.add_argument('--evaluate', action='store_true', help='运行月度评估')
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化JQData
    try:
        from jqdata.client import JQDataClient
        jq_client = JQDataClient()
        
        # 从配置文件读取凭据
        import json
        config_path = Path.home() / '.local/share/trquant/config/jqdata_config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            jq_client.authenticate(config['username'], config['password'])
        else:
            logger.error("未找到JQData配置文件")
            return
        
    except Exception as e:
        logger.error(f"JQData初始化失败: {e}")
        return
    
    # 创建流水线
    pipeline = FactorPipeline(
        jq_client=jq_client,
        stock_pool=args.pool,
        neutralize=not args.no_neutralize
    )
    
    if args.evaluate:
        # 月度评估
        pipeline.run_monthly_evaluation(date=args.date)
    else:
        # 日常计算
        pipeline.run_daily(date=args.date)


if __name__ == '__main__':
    main()

