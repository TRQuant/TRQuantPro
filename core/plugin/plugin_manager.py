# -*- coding: utf-8 -*-
"""
模块化插件管理器
===============
借鉴VN.Py模块化设计

支持的插件类型:
- DataPlugin: 数据源插件
- StrategyPlugin: 策略插件
- BrokerPlugin: 券商接口插件
- VisualizationPlugin: 可视化插件
- AnalysisPlugin: 分析插件

使用方式:
    from core.plugin import PluginManager, DataPlugin
    
    manager = PluginManager()
    manager.register(MyDataPlugin())
    manager.start_all()
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Type, Callable
from enum import Enum
from datetime import datetime
import importlib
import importlib.util
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class PluginType(Enum):
    """插件类型"""
    DATA = "data"               # 数据源
    STRATEGY = "strategy"       # 策略
    BROKER = "broker"           # 券商接口
    VISUALIZATION = "visualization"  # 可视化
    ANALYSIS = "analysis"       # 分析
    RISK = "risk"               # 风控
    NOTIFICATION = "notification"  # 通知


class PluginStatus(Enum):
    """插件状态"""
    REGISTERED = "registered"   # 已注册
    INITIALIZED = "initialized" # 已初始化
    RUNNING = "running"         # 运行中
    STOPPED = "stopped"         # 已停止
    ERROR = "error"             # 错误


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    type: PluginType
    version: str = "1.0.0"
    author: str = ""
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)


class BasePlugin(ABC):
    """
    插件基类
    
    所有插件必须继承此类
    """
    
    def __init__(self):
        self._status = PluginStatus.REGISTERED
        self._config: Dict[str, Any] = {}
        self._manager: Optional['PluginManager'] = None
    
    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """返回插件信息"""
        pass
    
    @property
    def status(self) -> PluginStatus:
        return self._status
    
    @property
    def name(self) -> str:
        return self.info.name
    
    def configure(self, config: Dict[str, Any]):
        """配置插件"""
        self._config = config
        logger.debug(f"插件 {self.name} 已配置")
    
    def set_manager(self, manager: 'PluginManager'):
        """设置管理器引用"""
        self._manager = manager
    
    def get_plugin(self, name: str) -> Optional['BasePlugin']:
        """获取其他插件（用于插件间通信）"""
        if self._manager:
            return self._manager.get(name)
        return None
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化插件"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """启动插件"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """停止插件"""
        pass
    
    def on_event(self, event_type: str, data: Any):
        """处理事件（可选实现）"""
        pass


class DataPlugin(BasePlugin):
    """
    数据源插件基类
    
    用于获取行情数据
    """
    
    @abstractmethod
    def get_bars(self, symbol: str, start_date: str, end_date: str, 
                 frequency: str = "day") -> List[Dict]:
        """获取K线数据"""
        pass
    
    @abstractmethod
    def get_tick(self, symbol: str) -> Optional[Dict]:
        """获取实时行情"""
        pass
    
    @abstractmethod
    def get_symbols(self, market: str = "") -> List[str]:
        """获取标的列表"""
        pass
    
    def subscribe(self, symbols: List[str], callback: Callable):
        """订阅行情（可选）"""
        pass
    
    def unsubscribe(self, symbols: List[str]):
        """取消订阅（可选）"""
        pass


class StrategyPlugin(BasePlugin):
    """
    策略插件基类
    """
    
    @abstractmethod
    def on_bar(self, bar: Dict) -> List[Dict]:
        """
        处理K线数据，返回信号列表
        
        Returns:
            信号列表 [{"symbol": "xxx", "action": "buy/sell", "volume": 100}, ...]
        """
        pass
    
    def on_tick(self, tick: Dict) -> List[Dict]:
        """处理实时行情（可选）"""
        return []
    
    def on_trade(self, trade: Dict):
        """处理成交回报（可选）"""
        pass
    
    def on_order(self, order: Dict):
        """处理订单回报（可选）"""
        pass


class BrokerPlugin(BasePlugin):
    """
    券商接口插件基类
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """连接券商"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """断开连接"""
        pass
    
    @abstractmethod
    def send_order(self, symbol: str, direction: str, price: float, 
                   volume: int, order_type: str = "limit") -> str:
        """发送订单，返回订单ID"""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """撤销订单"""
        pass
    
    @abstractmethod
    def query_position(self) -> List[Dict]:
        """查询持仓"""
        pass
    
    @abstractmethod
    def query_account(self) -> Dict:
        """查询账户"""
        pass


class VisualizationPlugin(BasePlugin):
    """
    可视化插件基类
    """
    
    @abstractmethod
    def plot_equity_curve(self, equity_data: List[Dict], output_path: str = ""):
        """绘制权益曲线"""
        pass
    
    @abstractmethod
    def plot_returns(self, returns_data: List[float], output_path: str = ""):
        """绘制收益分布"""
        pass
    
    @abstractmethod
    def generate_report(self, backtest_result: Dict, output_path: str = "") -> str:
        """生成回测报告"""
        pass


class AnalysisPlugin(BasePlugin):
    """
    分析插件基类
    """
    
    @abstractmethod
    def analyze_factor(self, factor_data: Any, returns_data: Any) -> Dict:
        """分析因子"""
        pass
    
    @abstractmethod
    def analyze_strategy(self, equity_curve: List[Dict]) -> Dict:
        """分析策略表现"""
        pass


class RiskPlugin(BasePlugin):
    """
    风控插件基类
    """
    
    @abstractmethod
    def check_order(self, order: Dict) -> bool:
        """检查订单是否符合风控规则"""
        pass
    
    @abstractmethod
    def check_position(self, positions: List[Dict]) -> List[str]:
        """检查持仓风险，返回警告列表"""
        pass


class PluginManager:
    """
    插件管理器
    
    借鉴VN.Py的模块化设计：
    - 统一的插件生命周期管理
    - 插件间依赖管理
    - 配置管理
    - 事件分发
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化插件管理器
        
        Args:
            config_path: 配置文件路径
        """
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugins_by_type: Dict[PluginType, List[str]] = {}
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._config: Dict[str, Any] = {}
        
        if config_path:
            self._load_config(config_path)
    
    def _load_config(self, config_path: str):
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            logger.info(f"已加载插件配置: {config_path}")
        except Exception as e:
            logger.warning(f"加载插件配置失败: {e}")
    
    def register(self, plugin: BasePlugin) -> bool:
        """
        注册插件
        
        Args:
            plugin: 插件实例
            
        Returns:
            是否注册成功
        """
        name = plugin.name
        plugin_type = plugin.info.type
        
        if name in self._plugins:
            logger.warning(f"插件 {name} 已存在，跳过注册")
            return False
        
        # 检查依赖
        for dep in plugin.info.dependencies:
            if dep not in self._plugins:
                logger.error(f"插件 {name} 依赖 {dep} 未找到")
                return False
        
        # 注册
        self._plugins[name] = plugin
        plugin.set_manager(self)
        
        # 按类型索引
        if plugin_type not in self._plugins_by_type:
            self._plugins_by_type[plugin_type] = []
        self._plugins_by_type[plugin_type].append(name)
        
        # 应用配置
        if name in self._config:
            plugin.configure(self._config[name])
        
        logger.info(f"✅ 注册插件: {name} ({plugin_type.value})")
        return True
    
    def unregister(self, name: str) -> bool:
        """注销插件"""
        if name not in self._plugins:
            return False
        
        plugin = self._plugins[name]
        
        # 先停止
        if plugin.status == PluginStatus.RUNNING:
            plugin.stop()
        
        # 移除
        del self._plugins[name]
        plugin_type = plugin.info.type
        if plugin_type in self._plugins_by_type:
            self._plugins_by_type[plugin_type].remove(name)
        
        logger.info(f"注销插件: {name}")
        return True
    
    def get(self, name: str) -> Optional[BasePlugin]:
        """获取插件"""
        return self._plugins.get(name)
    
    def get_by_type(self, plugin_type: PluginType) -> List[BasePlugin]:
        """按类型获取插件"""
        names = self._plugins_by_type.get(plugin_type, [])
        return [self._plugins[n] for n in names]
    
    def initialize_all(self) -> Dict[str, bool]:
        """初始化所有插件"""
        results = {}
        for name, plugin in self._plugins.items():
            try:
                success = plugin.initialize()
                plugin._status = PluginStatus.INITIALIZED if success else PluginStatus.ERROR
                results[name] = success
                logger.info(f"初始化插件 {name}: {'✅' if success else '❌'}")
            except Exception as e:
                plugin._status = PluginStatus.ERROR
                results[name] = False
                logger.error(f"初始化插件 {name} 异常: {e}")
        return results
    
    def start_all(self) -> Dict[str, bool]:
        """启动所有插件"""
        results = {}
        for name, plugin in self._plugins.items():
            if plugin.status != PluginStatus.INITIALIZED:
                results[name] = False
                continue
            
            try:
                success = plugin.start()
                plugin._status = PluginStatus.RUNNING if success else PluginStatus.ERROR
                results[name] = success
                logger.info(f"启动插件 {name}: {'✅' if success else '❌'}")
            except Exception as e:
                plugin._status = PluginStatus.ERROR
                results[name] = False
                logger.error(f"启动插件 {name} 异常: {e}")
        return results
    
    def stop_all(self) -> Dict[str, bool]:
        """停止所有插件"""
        results = {}
        for name, plugin in self._plugins.items():
            if plugin.status != PluginStatus.RUNNING:
                results[name] = True
                continue
            
            try:
                success = plugin.stop()
                plugin._status = PluginStatus.STOPPED
                results[name] = success
                logger.info(f"停止插件 {name}: {'✅' if success else '❌'}")
            except Exception as e:
                results[name] = False
                logger.error(f"停止插件 {name} 异常: {e}")
        return results
    
    def emit_event(self, event_type: str, data: Any):
        """分发事件到所有插件"""
        for plugin in self._plugins.values():
            try:
                plugin.on_event(event_type, data)
            except Exception as e:
                logger.error(f"插件 {plugin.name} 处理事件 {event_type} 异常: {e}")
        
        # 调用注册的处理器
        handlers = self._event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"事件处理器异常: {e}")
    
    def on(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def load_plugin_from_file(self, file_path: str, class_name: str) -> Optional[BasePlugin]:
        """
        从文件加载插件
        
        Args:
            file_path: 插件文件路径
            class_name: 插件类名
            
        Returns:
            插件实例或None
        """
        try:
            spec = importlib.util.spec_from_file_location("plugin_module", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                plugin_class = getattr(module, class_name)
                plugin = plugin_class()
                
                if self.register(plugin):
                    return plugin
        except Exception as e:
            logger.error(f"加载插件文件失败 {file_path}: {e}")
        return None
    
    def discover_plugins(self, plugins_dir: str) -> List[str]:
        """
        自动发现插件目录中的插件
        
        Args:
            plugins_dir: 插件目录
            
        Returns:
            发现的插件名称列表
        """
        discovered = []
        plugins_path = Path(plugins_dir)
        
        if not plugins_path.exists():
            logger.warning(f"插件目录不存在: {plugins_dir}")
            return discovered
        
        for py_file in plugins_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            try:
                # 读取文件查找插件类
                content = py_file.read_text(encoding='utf-8')
                if "BasePlugin" in content or "DataPlugin" in content or "StrategyPlugin" in content:
                    # 尝试导入
                    spec = importlib.util.spec_from_file_location(
                        py_file.stem, str(py_file)
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # 查找插件类
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                issubclass(attr, BasePlugin) and 
                                attr not in [BasePlugin, DataPlugin, StrategyPlugin, 
                                           BrokerPlugin, VisualizationPlugin, 
                                           AnalysisPlugin, RiskPlugin]):
                                try:
                                    plugin = attr()
                                    if self.register(plugin):
                                        discovered.append(plugin.name)
                                except Exception as e:
                                    logger.warning(f"实例化插件类 {attr_name} 失败: {e}")
            except Exception as e:
                logger.warning(f"处理插件文件 {py_file} 失败: {e}")
        
        logger.info(f"发现 {len(discovered)} 个插件")
        return discovered
    
    @property
    def stats(self) -> Dict[str, Any]:
        """获取插件统计"""
        status_count = {}
        for plugin in self._plugins.values():
            status = plugin.status.value
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            "total": len(self._plugins),
            "by_type": {k.value: len(v) for k, v in self._plugins_by_type.items()},
            "by_status": status_count,
            "plugins": [
                {
                    "name": p.name,
                    "type": p.info.type.value,
                    "version": p.info.version,
                    "status": p.status.value,
                }
                for p in self._plugins.values()
            ],
        }
    
    def __repr__(self):
        return f"PluginManager(plugins={len(self._plugins)})"


# 全局插件管理器实例
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """获取全局插件管理器"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


def register_plugin(plugin: BasePlugin) -> bool:
    """注册插件到全局管理器"""
    return get_plugin_manager().register(plugin)

