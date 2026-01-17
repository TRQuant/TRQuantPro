"""
研究环境统一初始化模块
========================

提供统一的环境初始化功能，自动检测项目根目录，
消除硬编码路径，支持多种运行环境。

使用方式:
    from notebooks.lib.research_init import setup_research_environment
    env = setup_research_environment()
    jq = env.get_jqdata_client()
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def detect_project_root() -> Path:
    """
    自动检测项目根目录
    
    检测策略：
    1. 查找包含 'core' 和 'config' 目录的父目录
    2. 查找包含 '.git' 目录的父目录
    3. 使用环境变量 TRQUANT_ROOT
    4. 回退到默认路径
    
    Returns:
        Path: 项目根目录路径
    """
    # 策略1: 从环境变量获取
    env_root = os.environ.get('TRQUANT_ROOT')
    if env_root and Path(env_root).exists():
        return Path(env_root)
    
    # 策略2: 从当前文件位置推断
    current_file = Path(__file__).resolve()
    # notebooks/lib/research_init.py -> 项目根目录
    potential_root = current_file.parent.parent.parent
    
    if _is_valid_project_root(potential_root):
        return potential_root
    
    # 策略3: 从当前工作目录向上查找
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if _is_valid_project_root(parent):
            return parent
    
    # 策略4: 默认路径
    default_paths = [
        Path('/home/taotao/dev/QuantTest/TRQuant'),
        Path.home() / 'dev' / 'QuantTest' / 'TRQuant',
    ]
    
    for path in default_paths:
        if path.exists() and _is_valid_project_root(path):
            return path
    
    raise RuntimeError(
        "无法检测项目根目录。请设置环境变量 TRQUANT_ROOT 或从项目目录运行。"
    )


def _is_valid_project_root(path: Path) -> bool:
    """验证是否为有效的项目根目录"""
    required_dirs = ['core', 'config', 'notebooks']
    return all((path / d).exists() for d in required_dirs)


@dataclass
class ResearchEnvironment:
    """研究环境配置"""
    
    project_root: Path
    config: Dict[str, Any] = field(default_factory=dict)
    
    # 缓存的客户端实例
    _jq_client: Any = field(default=None, repr=False)
    _trend_analyzer: Any = field(default=None, repr=False)
    _evaluator: Any = field(default=None, repr=False)
    _signal_provider: Any = field(default=None, repr=False)
    
    def __post_init__(self):
        """初始化后确保路径在 sys.path 中"""
        root_str = str(self.project_root)
        if root_str not in sys.path:
            sys.path.insert(0, root_str)
        logger.info(f"✅ 项目根目录: {self.project_root}")
    
    def get_jqdata_client(self, force_new: bool = False):
        """
        获取 JQData 客户端（带缓存）
        
        Args:
            force_new: 是否强制创建新实例
            
        Returns:
            JQDataClient 实例
        """
        if self._jq_client is None or force_new:
            try:
                from jqdata.client import JQDataClient
                from config.config_manager import ConfigManager
                
                config_manager = ConfigManager()
                jq_config = config_manager.get_jqdata_config()
                
                self._jq_client = JQDataClient()
                self._jq_client.authenticate(
                    username=jq_config.get('username'),
                    password=jq_config.get('password')
                )
                logger.info("✅ JQData 客户端初始化成功")
            except Exception as e:
                logger.error(f"❌ JQData 客户端初始化失败: {e}")
                raise
        
        return self._jq_client
    
    def get_trend_analyzer(self, force_new: bool = False):
        """获取趋势分析器"""
        if self._trend_analyzer is None or force_new:
            try:
                from core.trend_analyzer import TrendAnalyzer
                jq = self.get_jqdata_client()
                self._trend_analyzer = TrendAnalyzer(jq_client=jq)
                logger.info("✅ TrendAnalyzer 初始化成功")
            except Exception as e:
                logger.error(f"❌ TrendAnalyzer 初始化失败: {e}")
                raise
        return self._trend_analyzer
    
    def get_market_evaluator(self, force_new: bool = False):
        """获取市场环境评估器"""
        if self._evaluator is None or force_new:
            try:
                from core.market_environment_evaluator import get_market_environment_evaluator
                jq = self.get_jqdata_client()
                self._evaluator = get_market_environment_evaluator(jq_client=jq)
                logger.info("✅ MarketEnvironmentEvaluator 初始化成功")
            except Exception as e:
                logger.error(f"❌ MarketEnvironmentEvaluator 初始化失败: {e}")
                raise
        return self._evaluator
    
    def get_signal_provider(self, force_new: bool = False):
        """获取动态信号提供器"""
        if self._signal_provider is None or force_new:
            try:
                from core.dynamic_signals import get_dynamic_signal_provider
                self._signal_provider = get_dynamic_signal_provider()
                logger.info("✅ DynamicSignalProvider 初始化成功")
            except Exception as e:
                logger.error(f"❌ DynamicSignalProvider 初始化失败: {e}")
                raise
        return self._signal_provider
    
    def get_ibd_analyzer(self):
        """获取 IBD 分析器"""
        try:
            from core.ibd_style_analyzer import IBDStyleAnalyzer
            return IBDStyleAnalyzer()
        except Exception as e:
            logger.error(f"❌ IBDStyleAnalyzer 初始化失败: {e}")
            raise
    
    def get_regime_detector(self):
        """获取市场环境检测器"""
        try:
            from core.market_regime.market_regime_detector import get_market_regime_detector
            return get_market_regime_detector()
        except Exception as e:
            logger.error(f"❌ MarketRegimeDetector 初始化失败: {e}")
            raise
    
    def get_chart_engine(self):
        """获取图表引擎"""
        try:
            from core.visualization.chart_engine import ChartEngine
            return ChartEngine()
        except Exception as e:
            logger.error(f"❌ ChartEngine 初始化失败: {e}")
            raise
    
    def get_dashboard(self):
        """获取仪表盘"""
        try:
            from core.visualization.dashboard import MarketDashboard
            return MarketDashboard()
        except Exception as e:
            logger.error(f"❌ MarketDashboard 初始化失败: {e}")
            raise
    
    def load_config(self, config_name: str = 'research') -> Dict[str, Any]:
        """
        加载研究配置
        
        Args:
            config_name: 配置名称（不含扩展名）
            
        Returns:
            配置字典
        """
        config_path = self.project_root / 'notebooks' / 'research' / f'{config_name}.yaml'
        
        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"✅ 加载配置: {config_path}")
            except Exception as e:
                logger.warning(f"⚠️ 加载配置失败: {e}，使用默认配置")
                self.config = {}
        else:
            logger.info(f"配置文件不存在: {config_path}，使用默认配置")
            self.config = {}
        
        return self.config
    
    def get_cache_dir(self) -> Path:
        """获取缓存目录"""
        cache_dir = self.project_root / 'notebooks' / 'research' / '.cache'
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def get_output_dir(self) -> Path:
        """获取输出目录"""
        output_dir = self.project_root / 'notebooks' / 'research' / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def print_status(self):
        """打印环境状态"""
        print("=" * 60)
        print("研究环境状态")
        print("=" * 60)
        print(f"项目根目录: {self.project_root}")
        print(f"Python 版本: {sys.version.split()[0]}")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"JQData 客户端: {'✅ 已初始化' if self._jq_client else '⏳ 未初始化'}")
        print(f"趋势分析器: {'✅ 已初始化' if self._trend_analyzer else '⏳ 未初始化'}")
        print(f"评估引擎: {'✅ 已初始化' if self._evaluator else '⏳ 未初始化'}")
        print("=" * 60)


# 全局环境实例
_global_env: Optional[ResearchEnvironment] = None


def setup_research_environment(
    project_root: Optional[str] = None,
    load_config: bool = True,
    verbose: bool = True
) -> ResearchEnvironment:
    """
    设置研究环境（主入口函数）
    
    Args:
        project_root: 项目根目录（可选，自动检测）
        load_config: 是否自动加载配置
        verbose: 是否显示详细信息
        
    Returns:
        ResearchEnvironment 实例
        
    使用示例:
        >>> env = setup_research_environment()
        >>> jq = env.get_jqdata_client()
        >>> analyzer = env.get_trend_analyzer()
    """
    global _global_env
    
    if project_root:
        root = Path(project_root)
    else:
        root = detect_project_root()
    
    _global_env = ResearchEnvironment(project_root=root)
    
    if load_config:
        _global_env.load_config()
    
    if verbose:
        _global_env.print_status()
    
    return _global_env


def get_environment() -> ResearchEnvironment:
    """获取当前研究环境（如果未初始化则自动初始化）"""
    global _global_env
    if _global_env is None:
        _global_env = setup_research_environment(verbose=False)
    return _global_env


# 便捷函数
def get_project_root() -> Path:
    """获取项目根目录"""
    return get_environment().project_root


def get_jqdata_client():
    """便捷函数：获取 JQData 客户端"""
    return get_environment().get_jqdata_client()


def get_trend_analyzer():
    """便捷函数：获取趋势分析器"""
    return get_environment().get_trend_analyzer()


def get_market_evaluator():
    """便捷函数：获取市场环境评估器"""
    return get_environment().get_market_evaluator()


def get_signal_provider():
    """便捷函数：获取动态信号提供器"""
    return get_environment().get_signal_provider()


# 初始化时的快速检查
if __name__ == '__main__':
    env = setup_research_environment()
    print("\n测试 JQData 连接...")
    try:
        jq = env.get_jqdata_client()
        print("✅ JQData 连接成功")
    except Exception as e:
        print(f"❌ JQData 连接失败: {e}")

