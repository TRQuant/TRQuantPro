# -*- coding: utf-8 -*-
"""
TRQuant 统一API接口
===================

定义桌面系统和扩展件共用的标准接口。
根据运行环境自动选择实现（完整版core或简化版）。

架构图：
┌─────────────────┐     ┌─────────────────┐
│   桌面系统 GUI  │     │  VS Code 扩展   │
│   (PyQt6)       │     │  (TypeScript)   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │    ┌──────────────────┤
         │    │   shared/api.py  │
         │    │   (统一接口)      │
         │    └──────────────────┘
         │              │
         ▼              ▼
┌─────────────────────────────────────────┐
│            TRQuantAPI                    │
│  ┌─────────────┐  ┌─────────────┐       │
│  │CoreAdapter  │  │MockAdapter  │       │
│  │(完整功能)   │  │(独立部署)   │       │
│  └──────┬──────┘  └──────┬──────┘       │
└─────────┼────────────────┼──────────────┘
          │                │
          ▼                ▼
    ┌───────────┐    ┌───────────┐
    │  core/*   │    │ Mock Data │
    └───────────┘    └───────────┘
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


# ============================================================
# 数据模型（共享定义）
# ============================================================

@dataclass
class WorkflowResult:
    """工作流步骤结果"""
    step_name: str
    success: bool
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None


@dataclass
class MarketStatus:
    """市场状态"""
    regime: str  # risk_on / risk_off / neutral
    score: float
    index_trend: Dict[str, Any]
    style_rotation: List[Dict]
    position_suggestion: str
    strategy_advice: str


@dataclass
class Mainline:
    """投资主线"""
    rank: int
    name: str
    score: float
    change_pct: float
    fund_flow: float
    industries: List[str] = field(default_factory=list)
    stocks: List[str] = field(default_factory=list)


@dataclass
class Factor:
    """量化因子"""
    name: str
    category: str
    weight: float
    reason: str
    ic_mean: float = 0.0
    ir: float = 0.0


@dataclass 
class BacktestResult:
    """回测结果"""
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_loss_ratio: float
    total_trades: int
    report_file: Optional[str] = None


# ============================================================
# 抽象接口
# ============================================================

class TRQuantAPIBase(ABC):
    """TRQuant API 抽象基类"""
    
    @abstractmethod
    def check_data_sources(self) -> WorkflowResult:
        """步骤1: 检测数据源"""
        pass
    
    @abstractmethod
    def analyze_market_trend(self) -> WorkflowResult:
        """步骤2: 市场趋势分析"""
        pass
    
    @abstractmethod
    def identify_mainlines(self, top_n: int = 20) -> WorkflowResult:
        """步骤3: 投资主线识别"""
        pass
    
    @abstractmethod
    def build_candidate_pool(self) -> WorkflowResult:
        """步骤4: 候选池构建"""
        pass
    
    @abstractmethod
    def recommend_factors(self, market_regime: str = None) -> WorkflowResult:
        """步骤5: 因子推荐"""
        pass
    
    @abstractmethod
    def generate_strategy(self, factors: List[str], style: str = 'multi_factor',
                         platform: str = 'ptrade') -> WorkflowResult:
        """步骤6: 策略生成"""
        pass
    
    @abstractmethod
    def run_backtest(self, strategy_file: str = None, 
                    start_date: str = None, end_date: str = None) -> WorkflowResult:
        """步骤7: 回测验证"""
        pass
    
    @abstractmethod
    def check_broker_status(self) -> WorkflowResult:
        """步骤8: 券商状态检查"""
        pass
    
    @abstractmethod
    def run_full_workflow(self, callback: Callable = None) -> Dict:
        """执行完整8步工作流"""
        pass


# ============================================================
# Core适配器 - 调用完整core模块
# ============================================================

class CoreAdapter(TRQuantAPIBase):
    """
    Core模块适配器
    
    调用桌面系统的完整core模块实现
    """
    
    def __init__(self):
        self._orchestrator = None
        self._init_orchestrator()
    
    def _init_orchestrator(self):
        """初始化工作流编排器"""
        try:
            from core.workflow_orchestrator import WorkflowOrchestrator
            self._orchestrator = WorkflowOrchestrator()
            logger.info("CoreAdapter: 工作流编排器初始化成功")
        except ImportError as e:
            logger.error(f"CoreAdapter: 导入失败 - {e}")
            raise
    
    def _convert_result(self, result) -> WorkflowResult:
        """转换core模块的结果格式"""
        return WorkflowResult(
            step_name=result.step_name,
            success=result.success,
            summary=result.summary,
            details=result.details,
            timestamp=result.timestamp if hasattr(result, 'timestamp') else datetime.now().isoformat(),
            error=result.error if hasattr(result, 'error') else None
        )
    
    def check_data_sources(self) -> WorkflowResult:
        result = self._orchestrator.check_data_sources()
        return self._convert_result(result)
    
    def analyze_market_trend(self) -> WorkflowResult:
        result = self._orchestrator.analyze_market_trend()
        return self._convert_result(result)
    
    def identify_mainlines(self, top_n: int = 20) -> WorkflowResult:
        result = self._orchestrator.identify_mainlines()
        return self._convert_result(result)
    
    def build_candidate_pool(self) -> WorkflowResult:
        result = self._orchestrator.build_candidate_pool()
        return self._convert_result(result)
    
    def recommend_factors(self, market_regime: str = None) -> WorkflowResult:
        result = self._orchestrator.recommend_factors()
        return self._convert_result(result)
    
    def generate_strategy(self, factors: List[str], style: str = 'multi_factor',
                         platform: str = 'ptrade') -> WorkflowResult:
        result = self._orchestrator.generate_strategy()
        return self._convert_result(result)
    
    def run_backtest(self, strategy_file: str = None,
                    start_date: str = None, end_date: str = None) -> WorkflowResult:
        # 调用core的回测引擎
        try:
            from core.backtest_engine import create_backtest_engine, BacktestConfig
            
            config = BacktestConfig(
                start_date=start_date or '2024-01-01',
                end_date=end_date or '2024-12-01',
                initial_capital=1000000
            )
            
            if strategy_file:
                engine = create_backtest_engine(config)
                bt_result = engine.run(strategy_file)
                
                return WorkflowResult(
                    step_name='回测验证',
                    success=True,
                    summary=f"年化:{bt_result.get('annual_return', 0)*100:.1f}% 夏普:{bt_result.get('sharpe_ratio', 0):.2f}",
                    details=bt_result
                )
            else:
                return WorkflowResult(
                    step_name='回测验证',
                    success=False,
                    summary='请先生成策略',
                    details={'error': '未找到策略文件'}
                )
        except Exception as e:
            return WorkflowResult(
                step_name='回测验证',
                success=False,
                summary=f'回测失败: {str(e)[:30]}',
                details={'error': str(e)}
            )
    
    def check_broker_status(self) -> WorkflowResult:
        """检查券商连接状态"""
        details = {
            'ptrade': {'status': 'disconnected', 'message': '未配置'},
            'qmt': {'status': 'disconnected', 'message': '未配置'}
        }
        
        # 尝试检测PTrade
        try:
            from core.ptrade_integration import PTradeBridge
            bridge = PTradeBridge()
            if bridge.is_connected():
                details['ptrade'] = {'status': 'connected', 'message': '已连接'}
        except:
            pass
        
        # 尝试检测QMT
        try:
            from core.trading.qmt_interface import QMTTrader
            trader = QMTTrader()
            if trader.is_connected():
                details['qmt'] = {'status': 'connected', 'message': '已连接'}
        except:
            pass
        
        connected = any(v['status'] == 'connected' for v in details.values())
        
        return WorkflowResult(
            step_name='实盘交易',
            success=True,
            summary='✅ 券商已连接' if connected else '⚠️ 未配置券商',
            details=details
        )
    
    def run_full_workflow(self, callback: Callable = None) -> Dict:
        """执行完整工作流"""
        result = self._orchestrator.run_full_workflow(callback=callback)
        return {
            'success': result.success,
            'steps': [self._convert_result(r).__dict__ for r in result.steps],
            'strategy_file': result.strategy_file,
            'total_time': result.total_time
        }


# ============================================================
# Mock适配器 - 独立部署时使用
# ============================================================

class MockAdapter(TRQuantAPIBase):
    """
    Mock适配器
    
    用于扩展件独立部署时提供演示数据
    """
    
    def check_data_sources(self) -> WorkflowResult:
        return WorkflowResult(
            step_name='数据源检测',
            success=True,
            summary='✅ 2/3 数据源正常（演示）',
            details={
                'jqdata': {'connected': True, 'account_type': '试用账户'},
                'akshare': {'connected': True, 'indices': 50},
                'mongodb': {'connected': False, 'error': '请启动MongoDB'}
            }
        )
    
    def analyze_market_trend(self) -> WorkflowResult:
        return WorkflowResult(
            step_name='市场趋势',
            success=True,
            summary='📈 震荡偏多 | 综合评分:65（演示）',
            details={
                'short_term': 'up',
                'mid_term': 'sideways',
                'long_term': 'up',
                'composite_score': 65.0,
                'market_phase': '震荡偏多',
                'position_suggestion': '积极配置，建议70-80%仓位'
            }
        )
    
    def identify_mainlines(self, top_n: int = 20) -> WorkflowResult:
        mainlines = [
            {'rank': 1, 'name': 'AI人工智能', 'score': 9.5, 'change_pct': 3.2, 'fund_flow': 5.2e9},
            {'rank': 2, 'name': '新能源汽车', 'score': 9.1, 'change_pct': 2.1, 'fund_flow': 3.8e9},
            {'rank': 3, 'name': '半导体芯片', 'score': 8.7, 'change_pct': 1.8, 'fund_flow': 2.9e9},
            {'rank': 4, 'name': '医药创新', 'score': 8.3, 'change_pct': 1.2, 'fund_flow': 1.5e9},
            {'rank': 5, 'name': '高端制造', 'score': 7.9, 'change_pct': 0.9, 'fund_flow': 1.2e9},
        ]
        return WorkflowResult(
            step_name='投资主线',
            success=True,
            summary=f'🔥 TOP{top_n}主线（演示）',
            details={'top_mainlines': mainlines[:top_n], 'total_count': top_n}
        )
    
    def build_candidate_pool(self) -> WorkflowResult:
        stocks = [
            {'code': '300750.SZ', 'name': '宁德时代', 'source': '新能源汽车', 'score': 92},
            {'code': '002594.SZ', 'name': '比亚迪', 'source': '新能源汽车', 'score': 88},
            {'code': '688981.SH', 'name': '中芯国际', 'source': '半导体芯片', 'score': 86},
            {'code': '002415.SZ', 'name': '海康威视', 'source': 'AI人工智能', 'score': 85},
            {'code': '300760.SZ', 'name': '迈瑞医疗', 'source': '医药创新', 'score': 84},
        ]
        return WorkflowResult(
            step_name='候选池构建',
            success=True,
            summary='📦 候选池: 50只股票（演示）',
            details={'total_count': 50, 'stocks': stocks}
        )
    
    def recommend_factors(self, market_regime: str = None) -> WorkflowResult:
        factors = [
            {'name': '动量因子', 'category': '技术', 'weight': 0.25, 'reason': '趋势延续'},
            {'name': 'ROE因子', 'category': '质量', 'weight': 0.20, 'reason': '盈利能力'},
            {'name': 'PE因子', 'category': '价值', 'weight': 0.15, 'reason': '估值修复'},
            {'name': '资金流因子', 'category': '资金', 'weight': 0.20, 'reason': '主力动向'},
            {'name': '波动率因子', 'category': '风险', 'weight': 0.20, 'reason': '风险控制'},
        ]
        return WorkflowResult(
            step_name='因子推荐',
            success=True,
            summary='🧮 推荐5个因子（演示）',
            details={'factors': factors, 'market_regime': market_regime or 'neutral'}
        )
    
    def generate_strategy(self, factors: List[str], style: str = 'multi_factor',
                         platform: str = 'ptrade') -> WorkflowResult:
        return WorkflowResult(
            step_name='策略生成',
            success=True,
            summary=f'💻 已生成{platform.upper()}策略（演示）',
            details={
                'platform': platform,
                'style': style,
                'factors': factors,
                'strategy_file': f'strategies/{platform}/demo_strategy.py'
            }
        )
    
    def run_backtest(self, strategy_file: str = None,
                    start_date: str = None, end_date: str = None) -> WorkflowResult:
        return WorkflowResult(
            step_name='回测验证',
            success=True,
            summary='🔄 年化:25.6% 夏普:1.85（演示）',
            details={
                'total_return': 0.256,
                'annual_return': 0.256,
                'sharpe_ratio': 1.85,
                'max_drawdown': 0.123,
                'win_rate': 0.62,
                'profit_loss_ratio': 2.1,
                'total_trades': 156
            }
        )
    
    def check_broker_status(self) -> WorkflowResult:
        return WorkflowResult(
            step_name='实盘交易',
            success=True,
            summary='⚠️ 未配置券商（演示模式）',
            details={
                'ptrade': {'status': 'disconnected', 'message': '演示模式'},
                'qmt': {'status': 'disconnected', 'message': '演示模式'}
            }
        )
    
    def run_full_workflow(self, callback: Callable = None) -> Dict:
        steps = [
            self.check_data_sources(),
            self.analyze_market_trend(),
            self.identify_mainlines(),
            self.build_candidate_pool(),
            self.recommend_factors(),
            self.generate_strategy(['动量因子', 'ROE因子']),
            self.run_backtest(),
            self.check_broker_status()
        ]
        
        return {
            'success': True,
            'steps': [s.__dict__ for s in steps],
            'strategy_file': 'strategies/ptrade/demo_strategy.py',
            'total_time': 5.0
        }


# ============================================================
# API工厂
# ============================================================

class TRQuantAPI:
    """
    TRQuant API 入口
    
    自动检测环境，选择合适的适配器
    """
    
    _instance = None
    _adapter = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_adapter()
        return cls._instance
    
    def _init_adapter(self):
        """初始化适配器"""
        try:
            # 尝试使用完整版core模块
            self._adapter = CoreAdapter()
            self._mode = 'full'
            logger.info("TRQuantAPI: 使用完整版Core模块")
        except ImportError:
            # 回退到Mock模式
            self._adapter = MockAdapter()
            self._mode = 'mock'
            logger.info("TRQuantAPI: 使用Mock模式（独立部署）")
    
    @property
    def mode(self) -> str:
        """当前运行模式"""
        return self._mode
    
    def __getattr__(self, name):
        """代理到适配器"""
        return getattr(self._adapter, name)


def get_api() -> TRQuantAPI:
    """
    获取API实例
    
    用法：
        from shared import get_api
        api = get_api()
        result = api.analyze_market_trend()
    """
    return TRQuantAPI()























































