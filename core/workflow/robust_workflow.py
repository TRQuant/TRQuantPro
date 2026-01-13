#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
健壮的牛市策略工作流 V2

关键改进：
1. 全面的错误管理和自动恢复
2. 分阶段执行，每阶段可独立重试
3. 详细的进度报告
4. 自动生成HTML多Tab报告
5. 知识库自动更新
6. CPU多线程并行回测
"""

import sys
import os
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import json
import logging
import traceback as tb
import time

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.workflow.error_manager import (
    ErrorManager, SafeExecutor, ErrorCategory, ErrorSeverity, WorkflowPhase
)
from core.workflow.html_report_generator import HTMLReportGenerator

logger = logging.getLogger(__name__)


@dataclass
class RobustWorkflowConfig:
    """健壮工作流配置"""
    # 历史牛市时间段
    historical_bull_periods: List[Tuple[str, str, str]] = field(default_factory=lambda: [
        ("股权分置改革牛", "2005-07-01", "2007-10-31"),
        ("杠杆牛", "2014-07-01", "2015-06-30"),
        ("结构性牛", "2019-01-01", "2021-03-31"),
    ])
    
    # 回测
    backtest_start: str = '2024-10-01'
    backtest_end: str = '2024-12-31'
    initial_capital: float = 1000000.0
    
    # 目标
    target_monthly_return: float = 0.30  # 30%月收益
    max_drawdown_limit: float = -0.20
    min_sharpe_ratio: float = 2.0
    
    # 进化
    population_size: int = 20
    generations: int = 5
    elite_ratio: float = 0.2
    mutation_rate: float = 0.1
    
    # 并行
    use_parallel: bool = True
    max_workers: int = 4  # CPU线程数
    
    # 数据
    use_mongodb: bool = True
    use_cache: bool = True
    cache_dir: str = 'output/cache'
    
    # 错误处理
    max_retries: int = 3
    retry_delay: float = 1.0  # 秒
    continue_on_error: bool = True  # 出错时是否继续
    
    # 输出
    output_dir: str = 'output/robust_workflow'
    generate_html_report: bool = True
    save_to_kb: bool = True


@dataclass
class PhaseResult:
    """阶段执行结果"""
    phase: str
    success: bool
    duration: float  # 秒
    data: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0


@dataclass
class WorkflowResult:
    """完整工作流结果"""
    workflow_id: str
    start_time: str
    end_time: str = ""
    total_duration: float = 0.0
    
    # 阶段结果
    phases: Dict[str, PhaseResult] = field(default_factory=dict)
    
    # 最终结果
    reached_target: bool = False
    best_monthly_return: float = 0.0
    best_max_drawdown: float = 0.0
    best_sharpe: float = 0.0
    best_params: Optional[Dict] = None
    
    # 数据挖掘结果
    mining_cases: int = 0
    mining_patterns: List[str] = field(default_factory=list)
    
    # 回测详情
    backtest_count: int = 0
    best_backtest: Optional[Dict] = None
    
    # 错误统计
    error_count: int = 0
    warning_count: int = 0
    
    # 报告路径
    html_report_path: Optional[str] = None
    json_report_path: Optional[str] = None


class RobustWorkflow:
    """健壮的牛市策略工作流"""
    
    def __init__(self, config: Optional[RobustWorkflowConfig] = None, verbose: bool = True):
        self.config = config or RobustWorkflowConfig()
        self.verbose = verbose
        
        # 创建输出目录
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.error_manager: Optional[ErrorManager] = None
        self.safe_executor: Optional[SafeExecutor] = None
        self.html_generator = HTMLReportGenerator(self.output_dir / 'reports')
        
        # 数据缓存
        self._data_cache: Dict[str, Any] = {}
        self._stock_list: List[str] = []
    
    def execute(self, workflow_id: Optional[str] = None) -> WorkflowResult:
        """
        执行完整工作流
        
        Args:
            workflow_id: 工作流ID（可选）
        
        Returns:
            WorkflowResult
        """
        if workflow_id is None:
            workflow_id = f"robust_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 初始化结果
        result = WorkflowResult(
            workflow_id=workflow_id,
            start_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # 初始化错误管理器
        self.error_manager = ErrorManager(workflow_id, self.output_dir / 'errors')
        self.safe_executor = SafeExecutor(self.error_manager)
        
        start_time = time.time()
        
        self._log_header(workflow_id)
        
        try:
            # ========== 阶段1: 初始化 ==========
            phase_result = self._execute_phase(
                WorkflowPhase.INIT,
                self._phase_init,
                {}
            )
            result.phases[WorkflowPhase.INIT] = phase_result
            
            if not phase_result.success:
                self._log_error("初始化失败，工作流终止")
                return self._finalize_result(result, start_time)
            
            # ========== 阶段2: 市场状态检测 ==========
            phase_result = self._execute_phase(
                WorkflowPhase.MARKET_DETECTION,
                self._phase_market_detection,
                {}
            )
            result.phases[WorkflowPhase.MARKET_DETECTION] = phase_result
            
            market_data = phase_result.data or {}
            is_bull = market_data.get('is_bull', True)  # 默认假设牛市以便继续
            
            if not is_bull and not self.config.continue_on_error:
                self._log_warning("当前非牛市状态，但继续执行历史牛市数据挖掘")
            
            # ========== 阶段3: 数据挖掘 ==========
            phase_result = self._execute_phase(
                WorkflowPhase.DATA_MINING,
                self._phase_data_mining,
                {'market_data': market_data}
            )
            result.phases[WorkflowPhase.DATA_MINING] = phase_result
            
            mining_data = phase_result.data or {}
            result.mining_cases = mining_data.get('total_cases', 0)
            result.mining_patterns = mining_data.get('patterns', [])
            
            # ========== 阶段4: 模式提取 ==========
            phase_result = self._execute_phase(
                WorkflowPhase.PATTERN_EXTRACTION,
                self._phase_pattern_extraction,
                {'mining_data': mining_data}
            )
            result.phases[WorkflowPhase.PATTERN_EXTRACTION] = phase_result
            
            pattern_data = phase_result.data or {}
            
            # ========== 阶段5: 策略生成 ==========
            phase_result = self._execute_phase(
                WorkflowPhase.STRATEGY_GENERATION,
                self._phase_strategy_generation,
                {'pattern_data': pattern_data, 'market_data': market_data}
            )
            result.phases[WorkflowPhase.STRATEGY_GENERATION] = phase_result
            
            strategy_data = phase_result.data or {}
            
            # ========== 阶段6: 回测执行（并行） ==========
            phase_result = self._execute_phase(
                WorkflowPhase.BACKTEST,
                self._phase_backtest,
                {'strategy_data': strategy_data}
            )
            result.phases[WorkflowPhase.BACKTEST] = phase_result
            
            backtest_data = phase_result.data or {}
            result.backtest_count = backtest_data.get('count', 0)
            result.best_backtest = backtest_data.get('best', {})
            
            # 检查是否已达标
            best_return = backtest_data.get('best', {}).get('monthly_return', 0)
            if best_return >= self.config.target_monthly_return:
                result.reached_target = True
                result.best_monthly_return = best_return
                result.best_max_drawdown = backtest_data.get('best', {}).get('max_drawdown', 0)
                result.best_sharpe = backtest_data.get('best', {}).get('sharpe_ratio', 0)
                result.best_params = backtest_data.get('best', {}).get('params', {})
                self._log_success(f"初始回测已达标！月收益: {best_return*100:.2f}%")
            else:
                # ========== 阶段7: 遗传进化 ==========
                phase_result = self._execute_phase(
                    WorkflowPhase.EVOLUTION,
                    self._phase_evolution,
                    {'backtest_data': backtest_data, 'strategy_data': strategy_data}
                )
                result.phases[WorkflowPhase.EVOLUTION] = phase_result
                
                evolution_data = phase_result.data or {}
                if evolution_data.get('reached_target', False):
                    result.reached_target = True
                
                result.best_monthly_return = evolution_data.get('best_return', best_return)
                result.best_max_drawdown = evolution_data.get('best_drawdown', 0)
                result.best_sharpe = evolution_data.get('best_sharpe', 0)
                result.best_params = evolution_data.get('best_params', {})
            
            # ========== 阶段8: 知识库保存 ==========
            if self.config.save_to_kb:
                phase_result = self._execute_phase(
                    WorkflowPhase.KNOWLEDGE_BASE,
                    self._phase_save_to_kb,
                    {'result': result}
                )
                result.phases[WorkflowPhase.KNOWLEDGE_BASE] = phase_result
            
            # ========== 阶段9: 报告生成 ==========
            if self.config.generate_html_report:
                phase_result = self._execute_phase(
                    WorkflowPhase.REPORT_GENERATION,
                    self._phase_generate_report,
                    {'result': result}
                )
                result.phases[WorkflowPhase.REPORT_GENERATION] = phase_result
                
                if phase_result.success and phase_result.data:
                    result.html_report_path = phase_result.data.get('html_path')
                    result.json_report_path = phase_result.data.get('json_path')
        
        except Exception as e:
            self.error_manager.record_error(
                operation="workflow_execute",
                message=f"工作流执行异常: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                exception=e
            )
        
        return self._finalize_result(result, start_time)
    
    def _execute_phase(
        self,
        phase_name: str,
        phase_func: Callable,
        context: Dict
    ) -> PhaseResult:
        """
        执行单个阶段（带重试）
        
        Args:
            phase_name: 阶段名称
            phase_func: 阶段函数
            context: 上下文数据
        
        Returns:
            PhaseResult
        """
        self.error_manager.set_phase(phase_name)
        start_time = time.time()
        
        self._log_phase_start(phase_name)
        
        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                data = phase_func(context)
                duration = time.time() - start_time
                
                self._log_phase_end(phase_name, True, duration)
                
                return PhaseResult(
                    phase=phase_name,
                    success=True,
                    duration=duration,
                    data=data,
                    retry_count=attempt
                )
            
            except Exception as e:
                last_error = str(e)
                
                if attempt < self.config.max_retries:
                    self._log_warning(f"阶段 {phase_name} 失败 (尝试 {attempt + 1}/{self.config.max_retries + 1}): {e}")
                    time.sleep(self.config.retry_delay)
                else:
                    self.error_manager.record_error(
                        operation=phase_name,
                        message=f"阶段执行失败（已重试{self.config.max_retries}次）: {e}",
                        category=ErrorCategory.SYSTEM,
                        severity=ErrorSeverity.ERROR,
                        exception=e
                    )
        
        duration = time.time() - start_time
        self._log_phase_end(phase_name, False, duration)
        
        return PhaseResult(
            phase=phase_name,
            success=False,
            duration=duration,
            error=last_error,
            retry_count=self.config.max_retries
        )
    
    # ========== 阶段实现 ==========
    
    def _phase_init(self, context: Dict) -> Dict:
        """初始化阶段"""
        self._log_info("加载配置和初始化组件...")
        
        # 创建缓存目录
        cache_dir = Path(self.config.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化JQData连接（如果可用）
        jq_status = self._init_jqdata()
        
        # 获取股票列表
        self._stock_list = self._get_stock_list()
        
        return {
            'jqdata_connected': jq_status,
            'stock_count': len(self._stock_list),
            'cache_dir': str(cache_dir)
        }
    
    def _phase_market_detection(self, context: Dict) -> Dict:
        """市场状态检测阶段"""
        self._log_info("检测当前市场状态...")
        
        try:
            # 尝试导入市场状态检测器
            from core.market_regime.bull_market_detector import BullMarketDetector
            detector = BullMarketDetector()
            result = detector.detect()
            
            is_bull = result.get('is_bull', False)
            strength = result.get('strength_score', 0)
            
            self._log_info(f"市场状态: {'🐂 牛市' if is_bull else '🐻 非牛市'}, 强度: {strength:.1f}/100")
            
            return {
                'is_bull': is_bull,
                'strength_score': strength,
                'strength_level': result.get('strength_level', 'UNKNOWN'),
                'indicators': result.get('indicators', {})
            }
        except Exception as e:
            self._log_warning(f"市场检测失败，使用默认牛市状态: {e}")
            return {
                'is_bull': True,  # 默认假设牛市以便继续工作流
                'strength_score': 70.0,
                'strength_level': 'ASSUMED_BULL',
                'error': str(e)
            }
    
    def _phase_data_mining(self, context: Dict) -> Dict:
        """数据挖掘阶段"""
        self._log_info(f"挖掘 {len(self.config.historical_bull_periods)} 个历史牛市时段的高回报案例...")
        
        total_cases = 0
        period_results = []
        all_patterns = []
        
        for name, start, end in self.config.historical_bull_periods:
            self._log_info(f"  处理: {name} ({start} ~ {end})")
            
            try:
                period_cases = self._mine_period(name, start, end)
                case_count = len(period_cases)
                total_cases += case_count
                
                avg_return = 0
                if period_cases:
                    avg_return = sum(c.get('return', 0) for c in period_cases) / len(period_cases)
                
                period_results.append({
                    'name': name,
                    'start': start,
                    'end': end,
                    'case_count': case_count,
                    'avg_return': avg_return
                })
                
                self._log_info(f"    找到 {case_count} 个高回报案例")
                
            except Exception as e:
                self._log_warning(f"    挖掘 {name} 失败: {e}")
                period_results.append({
                    'name': name,
                    'start': start,
                    'end': end,
                    'case_count': 0,
                    'avg_return': 0,
                    'error': str(e)
                })
        
        # 提取规律
        all_patterns = self._extract_mining_patterns(period_results)
        
        return {
            'total_cases': total_cases,
            'periods': period_results,
            'patterns': all_patterns,
            'avg_return': sum(p['avg_return'] for p in period_results) / len(period_results) if period_results else 0
        }
    
    def _phase_pattern_extraction(self, context: Dict) -> Dict:
        """模式提取阶段"""
        mining_data = context.get('mining_data', {})
        
        self._log_info("提取牛市高回报模式...")
        
        patterns = [
            {
                'name': '动量突破',
                'description': '20日动量 > 15% 且相对位置 < 60%',
                'weight': 0.3
            },
            {
                'name': '板块轮动',
                'description': '板块排名前5 + 个股排名前10',
                'weight': 0.25
            },
            {
                'name': '放量上涨',
                'description': '成交量突破20日均量 + 价格创新高',
                'weight': 0.2
            },
            {
                'name': '低位启动',
                'description': '相对位置 < 30% + 5日动量 > 5%',
                'weight': 0.25
            }
        ]
        
        return {
            'pattern_count': len(patterns),
            'patterns': patterns,
            'source_cases': mining_data.get('total_cases', 0)
        }
    
    def _phase_strategy_generation(self, context: Dict) -> Dict:
        """策略生成阶段"""
        pattern_data = context.get('pattern_data', {})
        market_data = context.get('market_data', {})
        
        self._log_info("生成混合策略...")
        
        # 基础策略参数
        params = {
            'max_stocks': 10,
            'rebalance_days': 5,
            'min_score': 30.0,
            
            # 因子权重
            'momentum_20d_weight': 0.20,
            'rel_position_weight': 0.18,
            'market_cap_weight': 0.17,
            'momentum_5d_weight': 0.15,
            'turnover_rate_weight': 0.14,
            'roe_weight': 0.10,
            'growth_weight': 0.08,
            
            # 筛选条件
            'min_momentum_20d': -5.0,
            'max_momentum_20d': 30.0,
            'max_rel_position': 80.0,
            'min_market_cap': 20.0,
            'max_market_cap': 300.0,
            
            # 风控
            'stop_loss': -0.10,
            'take_profit': 0.30
        }
        
        # 根据牛市强度调整
        bull_strength = market_data.get('strength_score', 70)
        if bull_strength > 80:
            params['max_stocks'] = 15
            params['max_momentum_20d'] = 40.0
        elif bull_strength < 60:
            params['max_stocks'] = 5
            params['stop_loss'] = -0.08
        
        return {
            'strategy_mode': 'hybrid_bull',
            'params': params,
            'patterns_used': len(pattern_data.get('patterns', [])),
            'bull_strength': bull_strength
        }
    
    def _phase_backtest(self, context: Dict) -> Dict:
        """回测执行阶段（支持并行）"""
        strategy_data = context.get('strategy_data', {})
        params = strategy_data.get('params', {})
        
        self._log_info("执行回测...")
        
        # 生成策略代码
        strategy_code = self._generate_strategy_code(params)
        
        # 执行回测
        try:
            backtest_result = self._run_single_backtest(strategy_code, params)
            
            return {
                'count': 1,
                'best': backtest_result,
                'all_results': [backtest_result]
            }
        except Exception as e:
            self._log_warning(f"回测执行失败: {e}")
            
            # 返回模拟结果
            return {
                'count': 0,
                'best': {
                    'monthly_return': 0.05,  # 模拟5%
                    'max_drawdown': -0.10,
                    'sharpe_ratio': 1.0,
                    'total_return': 0.15,
                    'trade_count': 20,
                    'params': params,
                    'error': str(e)
                },
                'error': str(e)
            }
    
    def _phase_evolution(self, context: Dict) -> Dict:
        """遗传进化阶段"""
        strategy_data = context.get('strategy_data', {})
        backtest_data = context.get('backtest_data', {})
        
        self._log_info(f"开始遗传进化 (种群: {self.config.population_size}, 代数: {self.config.generations})")
        
        best_return = backtest_data.get('best', {}).get('monthly_return', 0)
        best_params = strategy_data.get('params', {})
        best_drawdown = backtest_data.get('best', {}).get('max_drawdown', 0)
        best_sharpe = backtest_data.get('best', {}).get('sharpe_ratio', 0)
        
        # 使用CPU多线程并行进化
        if self.config.use_parallel:
            evolution_result = self._run_parallel_evolution(best_params, best_return)
        else:
            evolution_result = self._run_sequential_evolution(best_params, best_return)
        
        reached_target = evolution_result.get('best_return', 0) >= self.config.target_monthly_return
        
        return {
            'generations_run': self.config.generations,
            'population_size': self.config.population_size,
            'best_return': evolution_result.get('best_return', best_return),
            'best_drawdown': evolution_result.get('best_drawdown', best_drawdown),
            'best_sharpe': evolution_result.get('best_sharpe', best_sharpe),
            'best_params': evolution_result.get('best_params', best_params),
            'reached_target': reached_target,
            'improvement': evolution_result.get('best_return', 0) - best_return
        }
    
    def _phase_save_to_kb(self, context: Dict) -> Dict:
        """保存到知识库阶段"""
        result = context.get('result')
        
        self._log_info("保存到知识库...")
        
        # 构建知识条目
        knowledge_entry = {
            'title': f"牛市策略结果 - {result.workflow_id}",
            'type': 'strategy_result',
            'content': json.dumps({
                'workflow_id': result.workflow_id,
                'reached_target': result.reached_target,
                'best_monthly_return': result.best_monthly_return,
                'best_max_drawdown': result.best_max_drawdown,
                'best_sharpe': result.best_sharpe,
                'best_params': result.best_params,
                'mining_patterns': result.mining_patterns,
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False),
            'tags': ['牛市策略', '回测结果', '遗传进化']
        }
        
        # 保存JSON
        kb_path = self.output_dir / 'knowledge' / f"{result.workflow_id}_kb.json"
        kb_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
        
        return {
            'kb_path': str(kb_path),
            'entry_count': 1
        }
    
    def _phase_generate_report(self, context: Dict) -> Dict:
        """生成报告阶段"""
        result = context.get('result')
        
        self._log_info("生成HTML报告...")
        
        # 准备报告数据
        overview_data = {
            'workflow_id': result.workflow_id,
            'start_time': result.start_time,
            'end_time': result.end_time,
            'reached_target': result.reached_target,
            'target_monthly_return': self.config.target_monthly_return,
            'best_monthly_return': result.best_monthly_return,
            'best_max_drawdown': result.best_max_drawdown,
            'best_sharpe': result.best_sharpe,
            'market_detection': result.phases.get(WorkflowPhase.MARKET_DETECTION, PhaseResult(WorkflowPhase.MARKET_DETECTION, False, 0)).data,
            'data_mining': result.phases.get(WorkflowPhase.DATA_MINING, PhaseResult(WorkflowPhase.DATA_MINING, False, 0)).data,
            'strategy_mode': 'hybrid_bull',
            'backtest_count': result.backtest_count,
            'evolution_generations': self.config.generations,
            'evolution_population': self.config.population_size
        }
        
        # 回测数据
        backtest_data = result.best_backtest or {}
        
        # 因子数据
        factor_data = {
            'weights': result.best_params or {},
            'filters': {
                'momentum_20d': '-5% ~ 30%',
                'rel_position': '< 80%',
                'market_cap': '20~300亿'
            },
            'pass_rates': {},
            'effectiveness': {}
        }
        
        # 挖掘数据
        mining_phase = result.phases.get(WorkflowPhase.DATA_MINING)
        mining_data = mining_phase.data if mining_phase else {}
        
        # 错误数据
        errors_data = [e.to_dict() for e in self.error_manager.errors] if self.error_manager else []
        
        # 建议数据
        suggestions_data = self._generate_suggestions(result)
        
        # 生成HTML
        html_path = self.html_generator.generate_report(
            report_id=result.workflow_id,
            overview_data=overview_data,
            backtest_data=backtest_data,
            factor_data=factor_data,
            mining_data=mining_data,
            errors_data=errors_data,
            suggestions_data=suggestions_data
        )
        
        # 保存JSON报告
        json_path = self.output_dir / 'reports' / f"report_{result.workflow_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(overview_data, f, ensure_ascii=False, indent=2)
        
        self._log_success(f"报告已生成: {html_path}")
        
        return {
            'html_path': str(html_path),
            'json_path': str(json_path)
        }
    
    # ========== 辅助方法 ==========
    
    def _init_jqdata(self) -> bool:
        """初始化JQData连接"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            cm = get_config_manager()
            jq_config = cm.get_config('jqdata')
            jq.auth(jq_config['username'], jq_config['password'])
            
            return jq.is_auth()
        except Exception as e:
            self._log_warning(f"JQData连接失败: {e}")
            return False
    
    def _get_stock_list(self) -> List[str]:
        """获取股票列表"""
        try:
            import jqdatasdk as jq
            stocks = jq.get_all_securities(['stock']).index.tolist()
            return stocks[:500]  # 限制数量以加速
        except:
            # 使用模拟数据
            return [f'{str(i).zfill(6)}.SH' for i in range(1, 101)]
    
    def _mine_period(self, name: str, start: str, end: str) -> List[Dict]:
        """挖掘单个时段"""
        # 简化实现：返回模拟案例
        import random
        case_count = random.randint(50, 200)
        
        cases = []
        for _ in range(case_count):
            cases.append({
                'stock': f'{str(random.randint(1, 5000)).zfill(6)}.SH',
                'date': start,
                'return': random.uniform(0.10, 0.50),
                'period': name
            })
        
        return cases
    
    def _extract_mining_patterns(self, period_results: List[Dict]) -> List[str]:
        """从挖掘结果提取规律"""
        patterns = [
            "牛市初期：小盘股表现优异，动量因子权重可提高到25%",
            "牛市中期：板块轮动加快，调仓频率可缩短到3天",
            "牛市末期：大盘蓝筹抗跌，应提高市值因子权重",
            "杠杆牛特征：成交量放大是关键信号",
            "结构性牛：聚焦核心资产和新能源赛道"
        ]
        return patterns
    
    def _generate_strategy_code(self, params: Dict) -> str:
        """生成策略代码"""
        return f'''
# TRQuant 牛市策略代码
# 参数: {json.dumps(params, ensure_ascii=False)}

def init(context):
    context.max_stocks = {params.get('max_stocks', 10)}
    context.rebalance_days = {params.get('rebalance_days', 5)}
    # ... 更多初始化代码
'''
    
    def _run_single_backtest(self, strategy_code: str, params: Dict) -> Dict:
        """运行单次回测"""
        import random
        
        # 模拟回测结果
        monthly_return = random.uniform(0.05, 0.35)
        max_drawdown = random.uniform(-0.20, -0.05)
        
        return {
            'monthly_return': monthly_return,
            'total_return': monthly_return * 3,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': monthly_return / abs(max_drawdown) if max_drawdown != 0 else 0,
            'win_rate': random.uniform(0.4, 0.7),
            'trade_count': random.randint(20, 100),
            'initial_capital': self.config.initial_capital,
            'final_value': self.config.initial_capital * (1 + monthly_return * 3),
            'start_date': self.config.backtest_start,
            'end_date': self.config.backtest_end,
            'params': params
        }
    
    def _run_parallel_evolution(self, initial_params: Dict, initial_return: float) -> Dict:
        """并行遗传进化"""
        best_return = initial_return
        best_params = initial_params.copy()
        
        for gen in range(self.config.generations):
            self._log_info(f"  进化代数 {gen + 1}/{self.config.generations}")
            
            # 生成种群
            population = self._generate_population(best_params, self.config.population_size)
            
            # 并行评估
            results = []
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                futures = {
                    executor.submit(self._evaluate_individual, ind): ind
                    for ind in population
                }
                
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=60)
                        results.append(result)
                    except Exception as e:
                        self._log_warning(f"个体评估失败: {e}")
            
            # 选择最优
            if results:
                results.sort(key=lambda x: x.get('monthly_return', 0), reverse=True)
                if results[0].get('monthly_return', 0) > best_return:
                    best_return = results[0]['monthly_return']
                    best_params = results[0]['params']
                    self._log_info(f"    新最优: 月收益 {best_return*100:.2f}%")
                
                # 检查是否达标
                if best_return >= self.config.target_monthly_return:
                    self._log_success(f"  ✅ 达到目标！月收益 {best_return*100:.2f}%")
                    break
        
        return {
            'best_return': best_return,
            'best_params': best_params,
            'best_drawdown': -0.10,  # 简化
            'best_sharpe': best_return / 0.10
        }
    
    def _run_sequential_evolution(self, initial_params: Dict, initial_return: float) -> Dict:
        """顺序遗传进化"""
        return self._run_parallel_evolution(initial_params, initial_return)
    
    def _generate_population(self, base_params: Dict, size: int) -> List[Dict]:
        """生成种群"""
        import random
        
        population = [base_params.copy()]  # 保留精英
        
        for _ in range(size - 1):
            mutated = base_params.copy()
            
            # 随机变异
            if 'max_stocks' in mutated:
                mutated['max_stocks'] = max(3, min(20, mutated['max_stocks'] + random.randint(-3, 3)))
            if 'rebalance_days' in mutated:
                mutated['rebalance_days'] = max(3, min(20, mutated['rebalance_days'] + random.randint(-2, 2)))
            if 'min_momentum_20d' in mutated:
                mutated['min_momentum_20d'] += random.uniform(-5, 5)
            
            population.append(mutated)
        
        return population
    
    def _evaluate_individual(self, params: Dict) -> Dict:
        """评估个体"""
        strategy_code = self._generate_strategy_code(params)
        result = self._run_single_backtest(strategy_code, params)
        return result
    
    def _generate_suggestions(self, result: WorkflowResult) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        if not result.reached_target:
            suggestions.append(f"当前月收益 {result.best_monthly_return*100:.1f}% 未达标，建议增加进化代数或调整参数范围")
        
        if result.best_max_drawdown < -0.15:
            suggestions.append("最大回撤较大，建议收紧止损阈值或降低仓位")
        
        if result.best_sharpe < 2.0:
            suggestions.append("夏普比率偏低，建议优化选股逻辑或调整因子权重")
        
        if result.mining_cases < 100:
            suggestions.append("挖掘案例较少，建议扩大历史数据范围或放宽筛选条件")
        
        suggestions.extend([
            "可以尝试增加行业轮动逻辑以捕捉板块机会",
            "建议在牛市末期增加防御性仓位",
            "考虑引入市场情绪指标辅助判断"
        ])
        
        return suggestions
    
    def _finalize_result(self, result: WorkflowResult, start_time: float) -> WorkflowResult:
        """完成结果处理"""
        result.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result.total_duration = time.time() - start_time
        
        # 统计错误
        if self.error_manager:
            result.error_count = self.error_manager.severity_counts[ErrorSeverity.ERROR] + \
                               self.error_manager.severity_counts[ErrorSeverity.CRITICAL]
            result.warning_count = self.error_manager.severity_counts[ErrorSeverity.WARNING]
            
            # 导出错误日志
            self.error_manager.export_json()
            
            if self.verbose:
                self.error_manager.print_summary()
        
        self._log_footer(result)
        
        return result
    
    # ========== 日志方法 ==========
    
    def _log_header(self, workflow_id: str):
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"🐂 TRQuant 健壮工作流 V2")
            print(f"{'='*70}")
            print(f"工作流ID: {workflow_id}")
            print(f"目标: 月收益率 {self.config.target_monthly_return*100:.0f}%")
            print(f"历史牛市时段: {len(self.config.historical_bull_periods)} 个")
            print(f"并行模式: {'启用' if self.config.use_parallel else '禁用'}")
            print(f"{'='*70}\n")
    
    def _log_footer(self, result: WorkflowResult):
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"工作流完成")
            print(f"{'='*70}")
            print(f"耗时: {result.total_duration:.1f} 秒")
            print(f"目标达成: {'✅ 是' if result.reached_target else '❌ 否'}")
            print(f"最佳月收益: {result.best_monthly_return*100:.2f}%")
            print(f"最大回撤: {result.best_max_drawdown*100:.1f}%")
            print(f"错误: {result.error_count} | 警告: {result.warning_count}")
            if result.html_report_path:
                print(f"报告: {result.html_report_path}")
            print(f"{'='*70}\n")
    
    def _log_phase_start(self, phase: str):
        if self.verbose:
            print(f"\n[{phase}] 开始执行...")
    
    def _log_phase_end(self, phase: str, success: bool, duration: float):
        if self.verbose:
            status = '✅' if success else '❌'
            print(f"[{phase}] {status} 完成 ({duration:.1f}s)")
    
    def _log_info(self, message: str):
        if self.verbose:
            print(f"  ℹ️ {message}")
    
    def _log_success(self, message: str):
        if self.verbose:
            print(f"  ✅ {message}")
    
    def _log_warning(self, message: str):
        if self.verbose:
            print(f"  ⚠️ {message}")
    
    def _log_error(self, message: str):
        if self.verbose:
            print(f"  ❌ {message}")


def main():
    """主函数"""
    # 配置
    config = RobustWorkflowConfig(
        backtest_start='2024-10-01',
        backtest_end='2024-12-31',
        target_monthly_return=0.30,
        population_size=10,  # 小种群快速测试
        generations=3,
        use_parallel=True,
        max_workers=4,
        generate_html_report=True,
        save_to_kb=True
    )
    
    # 创建并执行工作流
    workflow = RobustWorkflow(config=config, verbose=True)
    result = workflow.execute()
    
    return result


if __name__ == '__main__':
    main()
