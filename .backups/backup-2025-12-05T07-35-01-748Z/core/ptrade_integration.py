# -*- coding: utf-8 -*-
"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration




"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration




"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration

"""
PTrade集成模块
实现PTrade策略开发、回测数据读取、实盘数据同步

PTrade接口文档：http://180.169.107.9:7766/hub/help/api
PTrade策略编译环境：Python 3.11
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)


@dataclass
class PTradeConfig:
    """PTrade配置"""
    host: str = ""
    port: int = 8888
    account_id: str = ""
    password: str = ""
    strategy_path: str = ""  # PTrade策略文件目录
    data_path: str = ""      # PTrade数据导出目录
    
    @classmethod
    def load(cls, config_path: str = None) -> 'PTradeConfig':
        """从配置文件加载"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = None):
        """保存到配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "ptrade_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


@dataclass
class PTradeBacktestResult:
    """PTrade回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    trades: List[Dict] = field(default_factory=list)
    daily_returns: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return self.__dict__


class PTradeDataReader:
    """
    PTrade数据读取器
    
    读取PTrade导出的回测结果和实盘交易数据
    """
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            self.data_path = Path(__file__).parent.parent / "data" / "ptrade"
        
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def read_backtest_result(self, result_file: str) -> Optional[PTradeBacktestResult]:
        """
        读取PTrade回测结果文件
        
        Args:
            result_file: 结果文件路径（JSON或CSV）
        
        Returns:
            PTradeBacktestResult: 回测结果
        """
        file_path = Path(result_file)
        
        if not file_path.exists():
            logger.error(f"回测结果文件不存在: {result_file}")
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return PTradeBacktestResult(**data)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                # 解析CSV格式的回测结果
                # PTrade导出的CSV格式需要根据实际格式调整
                return self._parse_csv_result(df)
            
        except Exception as e:
            logger.error(f"读取回测结果失败: {e}")
            return None
    
    def _parse_csv_result(self, df) -> PTradeBacktestResult:
        """解析CSV格式的回测结果"""
        # 根据PTrade实际导出格式调整
        return PTradeBacktestResult(
            strategy_name=df.get('strategy_name', ['Unknown'])[0] if 'strategy_name' in df else 'Unknown',
            start_date=str(df.index[0]) if len(df) > 0 else '',
            end_date=str(df.index[-1]) if len(df) > 0 else '',
            initial_capital=1000000,
            final_capital=1000000,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
        )
    
    def read_trade_records(self, trade_file: str) -> List[Dict]:
        """
        读取交易记录
        
        Args:
            trade_file: 交易记录文件路径
        
        Returns:
            List[Dict]: 交易记录列表
        """
        file_path = Path(trade_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取交易记录失败: {e}")
            return []
    
    def read_positions(self, position_file: str) -> List[Dict]:
        """读取持仓数据"""
        file_path = Path(position_file)
        
        if not file_path.exists():
            return []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_path.suffix == '.csv':
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"读取持仓数据失败: {e}")
            return []
    
    def list_backtest_results(self) -> List[str]:
        """列出所有回测结果文件"""
        results = []
        for file in self.data_path.glob("*.json"):
            if 'backtest' in file.name.lower() or 'result' in file.name.lower():
                results.append(str(file))
        return results


class PTradeStrategyGenerator:
    """
    PTrade策略代码生成器
    
    生成符合PTrade规范的Python策略代码
    """
    
    # PTrade策略模板
    STRATEGY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
策略描述: {description}
作者: {author}
创建时间: {created_at}
PTrade版本: Python 3.11
"""

# PTrade内置模块
# from ptrade import *

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
{parameters}


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 设置股票池
    context.stock_pool = {stock_pool}
    
    # 策略参数
{init_params}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    pass


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
{trading_logic}


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    log.info(f"当日持仓: {{len(positions)}} 只股票")
    
    # 记录账户信息
    log.info(f"总资产: {{context.portfolio.total_value:.2f}}")
    log.info(f"可用资金: {{context.portfolio.available_cash:.2f}}")


# ==================== 辅助函数 ====================
{helper_functions}


# ==================== 风险控制 ====================
def risk_control(context):
    """
    风险控制函数
    """
    # 检查最大回撤
    if context.portfolio.total_value < context.portfolio.starting_cash * (1 - MAX_DRAWDOWN):
        log.warn("触发最大回撤限制，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)
        return False
    return True
'''
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "strategies" / "ptrade"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        strategy_name: str,
        description: str = "",
        author: str = "",
        stock_pool: List[str] = None,
        parameters: Dict[str, Any] = None,
        trading_logic: str = "",
        helper_functions: str = ""
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            strategy_name: 策略名称
            description: 策略描述
            author: 作者
            stock_pool: 股票池
            parameters: 策略参数
            trading_logic: 交易逻辑代码
            helper_functions: 辅助函数代码
        
        Returns:
            str: 生成的策略代码
        """
        stock_pool = stock_pool or ["'000001.XSHE'", "'600000.XSHG'"]
        parameters = parameters or {
            'LOOKBACK_PERIOD': 20,
            'MAX_POSITION': 0.2,
            'STOP_LOSS': 0.08,
            'MAX_DRAWDOWN': 0.15,
        }
        
        # 生成参数定义
        params_code = "\n".join([
            f"{k} = {v}" for k, v in parameters.items()
        ])
        
        # 生成初始化参数
        init_params = "\n".join([
            f"    context.{k.lower()} = {k}" for k in parameters.keys()
        ])
        
        # 默认交易逻辑
        if not trading_logic:
            trading_logic = '''    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 获取股票池数据
    for stock in context.stock_pool:
        # 获取历史数据
        df = get_price(stock, count=LOOKBACK_PERIOD, frequency='1d', 
                      fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is None or len(df) < LOOKBACK_PERIOD:
            continue
        
        # 计算信号
        close = df['close'].values
        ma_short = np.mean(close[-5:])
        ma_long = np.mean(close[-20:])
        
        # 交易逻辑
        if stock not in current_positions:
            # 买入条件
            if ma_short > ma_long:
                # 计算可买数量
                cash = context.portfolio.available_cash
                price = close[-1]
                amount = int(cash * MAX_POSITION / price / 100) * 100
                if amount > 0:
                    order(stock, amount)
                    log.info(f"买入 {stock}, 数量: {amount}")
        else:
            # 卖出条件
            position = context.portfolio.positions[stock]
            cost = position.avg_cost
            current_price = close[-1]
            
            # 止损
            if current_price < cost * (1 - STOP_LOSS):
                order_target(stock, 0)
                log.info(f"止损卖出 {stock}")
            # 均线死叉
            elif ma_short < ma_long:
                order_target(stock, 0)
                log.info(f"信号卖出 {stock}")'''
        
        # 默认辅助函数
        if not helper_functions:
            helper_functions = '''def get_stock_industry(stock):
    """获取股票所属行业"""
    try:
        return get_industry(stock)
    except:
        return None


def calculate_ma(prices, period):
    """计算移动平均"""
    return np.mean(prices[-period:])


def calculate_volatility(prices, period=20):
    """计算波动率"""
    returns = np.diff(prices[-period:]) / prices[-period:-1]
    return np.std(returns) * np.sqrt(252)'''
        
        # 生成代码
        code = self.STRATEGY_TEMPLATE.format(
            strategy_name=strategy_name,
            description=description,
            author=author,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parameters=params_code,
            stock_pool=stock_pool,
            init_params=init_params,
            trading_logic=trading_logic,
            helper_functions=helper_functions,
        )
        
        return code
    
    def save(self, code: str, filename: str) -> str:
        """
        保存策略代码到文件
        
        Args:
            code: 策略代码
            filename: 文件名
        
        Returns:
            str: 文件路径
        """
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"策略已保存: {file_path}")
        return str(file_path)


class CursorPTradeIntegration:
    """
    Cursor IDE与PTrade集成
    
    提供AI辅助策略开发的Prompt模板和工作流
    """
    
    # Prompt模板
    PROMPTS = {
        'generate_ptrade_strategy': '''请帮我生成一个PTrade量化策略，要求如下：

## 策略描述
{description}

## 策略类型
{strategy_type}

## 股票池
{stock_pool}

## 技术要求
- 使用PTrade Python 3.11环境
- 必须包含 initialize, before_market_open, market_open, after_market_close 函数
- 使用PTrade内置函数：get_price, order, order_target, set_benchmark等
- 实现止损止盈逻辑
- 添加风险控制

## 因子要求
{factors}

## 参数设置
{parameters}

请生成完整的PTrade策略代码，包含详细注释。
''',
        
        'analyze_backtest': '''请分析以下PTrade回测结果：

## 策略信息
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

## 回测指标
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%
- 总交易次数: {total_trades}

## 交易记录
{trade_records}

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议

给出具体的优化方向和代码修改建议。
''',
        
        'optimize_strategy': '''请帮我优化以下PTrade策略代码：

## 当前代码
```python
{code}
```

## 当前回测表现
- 总收益: {total_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}

## 优化目标
{optimization_goals}

## 可用因子
{available_factors}

请给出优化后的完整代码，并解释修改原因。
''',
        
        'convert_to_ptrade': '''请将以下策略代码转换为PTrade格式：

## 原始代码
```python
{original_code}
```

## 转换要求
- 使用PTrade标准函数接口
- 保持原有策略逻辑
- 添加PTrade特有的风控和日志功能
- 确保代码可以在PTrade Python 3.11环境运行

请生成转换后的完整PTrade策略代码。
''',
        
        'factor_strategy': '''请基于以下量化因子生成PTrade策略：

## 因子列表
{factors}

## 因子权重
{weights}

## 选股逻辑
{selection_logic}

## 调仓频率
{rebalance_frequency}

## 风险控制
- 单股最大仓位: {max_position}%
- 止损比例: {stop_loss}%
- 最大回撤限制: {max_drawdown}%

请生成完整的多因子PTrade策略代码。
''',
    }
    
    def __init__(self):
        self.data_reader = PTradeDataReader()
        self.strategy_generator = PTradeStrategyGenerator()
    
    def generate_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        生成Cursor Prompt
        
        Args:
            prompt_type: Prompt类型
            **kwargs: 模板参数
        
        Returns:
            str: 生成的Prompt
        """
        if prompt_type not in self.PROMPTS:
            raise ValueError(f"未知的Prompt类型: {prompt_type}")
        
        template = self.PROMPTS[prompt_type]
        
        # 填充参数
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        return template
    
    def create_strategy_prompt(
        self,
        description: str,
        strategy_type: str = "动量策略",
        stock_pool: str = "沪深300成分股",
        factors: str = "动量因子、价值因子",
        parameters: str = "回看周期20天，持仓上限20%"
    ) -> str:
        """创建策略生成Prompt"""
        return self.generate_prompt(
            'generate_ptrade_strategy',
            description=description,
            strategy_type=strategy_type,
            stock_pool=stock_pool,
            factors=factors,
            parameters=parameters
        )
    
    def create_analysis_prompt(self, backtest_result: PTradeBacktestResult) -> str:
        """创建回测分析Prompt"""
        return self.generate_prompt(
            'analyze_backtest',
            strategy_name=backtest_result.strategy_name,
            start_date=backtest_result.start_date,
            end_date=backtest_result.end_date,
            initial_capital=backtest_result.initial_capital,
            total_return=f"{backtest_result.total_return*100:.2f}",
            annual_return=f"{backtest_result.annual_return*100:.2f}",
            max_drawdown=f"{backtest_result.max_drawdown*100:.2f}",
            sharpe_ratio=f"{backtest_result.sharpe_ratio:.2f}",
            win_rate=f"{backtest_result.win_rate*100:.1f}",
            total_trades=backtest_result.total_trades,
            trade_records=json.dumps(backtest_result.trades[:20], ensure_ascii=False, indent=2)
        )
    
    def create_optimization_prompt(
        self,
        code: str,
        total_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        optimization_goals: str = "提高夏普比率，降低最大回撤",
        available_factors: str = "动量、价值、质量、波动率"
    ) -> str:
        """创建策略优化Prompt"""
        return self.generate_prompt(
            'optimize_strategy',
            code=code,
            total_return=f"{total_return*100:.2f}",
            max_drawdown=f"{max_drawdown*100:.2f}",
            sharpe_ratio=f"{sharpe_ratio:.2f}",
            optimization_goals=optimization_goals,
            available_factors=available_factors
        )
    
    def create_factor_strategy_prompt(
        self,
        factors: List[str],
        weights: Dict[str, float] = None,
        selection_logic: str = "综合评分前20名",
        rebalance_frequency: str = "每周一调仓",
        max_position: float = 10,
        stop_loss: float = 8,
        max_drawdown: float = 15
    ) -> str:
        """创建多因子策略Prompt"""
        weights = weights or {f: 1.0/len(factors) for f in factors}
        
        return self.generate_prompt(
            'factor_strategy',
            factors="\n".join([f"- {f}" for f in factors]),
            weights=json.dumps(weights, ensure_ascii=False, indent=2),
            selection_logic=selection_logic,
            rebalance_frequency=rebalance_frequency,
            max_position=max_position,
            stop_loss=stop_loss,
            max_drawdown=max_drawdown
        )
    
    def save_prompt_to_file(self, prompt: str, filename: str = None) -> str:
        """保存Prompt到文件"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        file_path = prompts_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        return str(file_path)
    
    def copy_to_clipboard(self, prompt: str) -> bool:
        """复制到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(prompt)
            return True
        except ImportError:
            logger.warning("pyperclip未安装")
            return False


# 全局实例
_ptrade_integration = None


def get_ptrade_integration() -> CursorPTradeIntegration:
    """获取PTrade集成实例"""
    global _ptrade_integration
    if _ptrade_integration is None:
        _ptrade_integration = CursorPTradeIntegration()
    return _ptrade_integration












