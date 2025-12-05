# -*- coding: utf-8 -*-
"""
TRQuant Extension - 策略管理系统
================================

完整的策略管理功能：
- 策略CRUD操作
- 策略分类（PTrade/QMT/研究/示例）
- 策略模板生成
- 策略验证
- 策略版本管理
- 策略参数管理

此模块独立于桌面系统，可随扩展件打包部署
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

# ============================================================
# 路径配置
# ============================================================

EXTENSION_ROOT = Path(__file__).parent.parent
DATA_ROOT = EXTENSION_ROOT / "data"

# 策略目录
STRATEGY_BASE = DATA_ROOT / "strategies"
STRATEGY_DIRS = {
    "ptrade": STRATEGY_BASE / "ptrade",
    "qmt": STRATEGY_BASE / "qmt",
    "research": STRATEGY_BASE / "research",
    "examples": STRATEGY_BASE / "examples",
    "archived": STRATEGY_BASE / "archived"
}

# 确保目录存在
for dir_path in STRATEGY_DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)


# ============================================================
# 策略模板
# ============================================================

STRATEGY_TEMPLATES = {
    "ptrade_multi_factor": '''# -*- coding: utf-8 -*-
"""
PTrade 多因子策略
==================
策略名称: {name}
创建时间: {created_time}
描述: {description}

因子列表:
{factors_list}
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============ 策略参数 ============
INITIAL_CAPITAL = {initial_capital}
MAX_POSITION = {max_position}  # 单票最大仓位
STOP_LOSS = {stop_loss}  # 止损线
TAKE_PROFIT = {take_profit}  # 止盈线
REBALANCE_DAYS = {rebalance_days}  # 调仓周期

# 因子配置
FACTORS = {factors_config}


def initialize(context):
    """策略初始化"""
    context.run_params = {{
        'initial_capital': INITIAL_CAPITAL,
        'max_position': MAX_POSITION,
        'stop_loss': STOP_LOSS,
        'take_profit': TAKE_PROFIT
    }}
    context.last_rebalance = None
    context.positions = {{}}
    log.info(f"策略初始化完成: {{context.run_params}}")


def before_trading_start(context, data):
    """盘前运行"""
    pass


def handle_data(context, data):
    """盘中运行（每分钟）"""
    # 检查是否需要调仓
    today = context.current_dt.date()
    if context.last_rebalance is None:
        need_rebalance = True
    else:
        days_since = (today - context.last_rebalance).days
        need_rebalance = days_since >= REBALANCE_DAYS
    
    if need_rebalance:
        rebalance(context, data)
        context.last_rebalance = today


def rebalance(context, data):
    """调仓逻辑"""
    log.info("开始调仓...")
    
    # 1. 计算因子得分
    scores = calculate_factor_scores(context, data)
    
    # 2. 选股
    selected = select_stocks(scores, top_n=10)
    
    # 3. 执行交易
    execute_trades(context, selected)
    
    log.info(f"调仓完成，持仓: {{len(context.positions)}}只")


def calculate_factor_scores(context, data):
    """计算因子综合得分"""
    scores = {{}}
    # TODO: 实现因子计算逻辑
    return scores


def select_stocks(scores, top_n=10):
    """根据得分选股"""
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_stocks[:top_n]]


def execute_trades(context, selected):
    """执行交易"""
    capital = context.portfolio.available_cash
    position_size = capital * MAX_POSITION
    
    # 卖出不在列表中的股票
    for stock in list(context.positions.keys()):
        if stock not in selected:
            order_target(stock, 0)
            del context.positions[stock]
    
    # 买入新选中的股票
    for stock in selected:
        if stock not in context.positions:
            order_value(stock, position_size)
            context.positions[stock] = position_size


def after_trading_end(context, data):
    """盘后运行"""
    # 记录当日收益
    log.info(f"当日收益率: {{context.portfolio.returns:.2%}}")
''',

    "ptrade_momentum": '''# -*- coding: utf-8 -*-
"""
PTrade 动量策略
================
策略名称: {name}
创建时间: {created_time}
描述: {description}
"""

import pandas as pd
import numpy as np

# ============ 策略参数 ============
LOOKBACK_PERIOD = {lookback_period}  # 回看周期
HOLDING_PERIOD = {holding_period}  # 持仓周期
TOP_N = {top_n}  # 选股数量
INITIAL_CAPITAL = {initial_capital}


def initialize(context):
    """策略初始化"""
    context.lookback = LOOKBACK_PERIOD
    context.holding = HOLDING_PERIOD
    context.top_n = TOP_N
    context.last_trade = None
    log.info("动量策略初始化完成")


def handle_data(context, data):
    """盘中运行"""
    today = context.current_dt.date()
    
    # 检查是否需要调仓
    if context.last_trade is None:
        need_trade = True
    else:
        days_since = (today - context.last_trade).days
        need_trade = days_since >= context.holding
    
    if need_trade:
        # 计算动量
        momentum = calculate_momentum(context, data)
        
        # 选股
        selected = momentum.nlargest(context.top_n).index.tolist()
        
        # 调仓
        rebalance_portfolio(context, selected)
        context.last_trade = today


def calculate_momentum(context, data):
    """计算动量因子"""
    # 获取股票池
    stocks = get_index_stocks('000300.XSHG')
    
    # 计算收益率
    prices = history(context.lookback + 1, '1d', 'close', stocks)
    returns = prices.iloc[-1] / prices.iloc[0] - 1
    
    return returns


def rebalance_portfolio(context, selected):
    """调仓"""
    # 平仓不在列表中的
    for stock in context.portfolio.positions:
        if stock not in selected:
            order_target(stock, 0)
    
    # 等权买入
    if selected:
        weight = 1.0 / len(selected)
        for stock in selected:
            order_target_percent(stock, weight)
    
    log.info(f"调仓完成: {{selected}}")
''',

    "qmt_grid": '''# -*- coding: utf-8 -*-
"""
QMT 网格交易策略
=================
策略名称: {name}
创建时间: {created_time}
描述: {description}
"""

from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount

# ============ 策略参数 ============
STOCK_CODE = '{stock_code}'  # 标的代码
GRID_SIZE = {grid_size}  # 网格大小(%)
GRID_AMOUNT = {grid_amount}  # 每格交易金额
BASE_PRICE = {base_price}  # 基准价格
GRID_COUNT = {grid_count}  # 网格数量


class GridStrategy:
    """网格交易策略"""
    
    def __init__(self):
        self.stock_code = STOCK_CODE
        self.grid_size = GRID_SIZE / 100
        self.grid_amount = GRID_AMOUNT
        self.base_price = BASE_PRICE
        self.grid_count = GRID_COUNT
        
        # 计算网格价格
        self.grids = self._calculate_grids()
        self.positions = {{}}
        
    def _calculate_grids(self):
        """计算网格价格"""
        grids = []
        for i in range(-self.grid_count, self.grid_count + 1):
            price = self.base_price * (1 + i * self.grid_size)
            grids.append({{
                'level': i,
                'price': round(price, 2),
                'triggered': False
            }})
        return sorted(grids, key=lambda x: x['price'])
    
    def on_tick(self, tick):
        """行情回调"""
        current_price = tick['lastPrice']
        
        for grid in self.grids:
            if grid['triggered']:
                continue
                
            if grid['level'] > 0 and current_price >= grid['price']:
                # 价格上穿网格，卖出
                self._sell(grid, current_price)
                grid['triggered'] = True
                
            elif grid['level'] < 0 and current_price <= grid['price']:
                # 价格下穿网格，买入
                self._buy(grid, current_price)
                grid['triggered'] = True
    
    def _buy(self, grid, price):
        """买入"""
        amount = int(self.grid_amount / price / 100) * 100
        print(f"[买入] 网格{grid['level']}, 价格{price}, 数量{amount}")
        # TODO: 实际下单
        
    def _sell(self, grid, price):
        """卖出"""
        amount = int(self.grid_amount / price / 100) * 100
        print(f"[卖出] 网格{grid['level']}, 价格{price}, 数量{amount}")
        # TODO: 实际下单


def main():
    """主函数"""
    strategy = GridStrategy()
    
    # 订阅行情
    xtdata.subscribe_quote(STOCK_CODE, period='tick', callback=strategy.on_tick)
    
    print(f"网格策略启动: {{STOCK_CODE}}")
    print(f"网格数量: {{GRID_COUNT * 2 + 1}}")
    print(f"网格间距: {{GRID_SIZE}}%")
    
    # 保持运行
    xtdata.run()


if __name__ == '__main__':
    main()
''',

    "research_factor": '''# -*- coding: utf-8 -*-
"""
因子研究模板
============
因子名称: {name}
创建时间: {created_time}
描述: {description}

研究目标:
1. 因子计算逻辑
2. 因子分布分析
3. IC/IR分析
4. 分层回测
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ============ 因子参数 ============
FACTOR_NAME = "{name}"
LOOKBACK_PERIOD = {lookback_period}
UNIVERSE = "{universe}"  # 股票池


class FactorResearch:
    """因子研究类"""
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.factor_data = None
        self.returns_data = None
        
    def calculate_factor(self, data):
        """
        计算因子值
        
        Args:
            data: 原始数据DataFrame
            
        Returns:
            pd.Series: 因子值
        """
        # TODO: 实现因子计算逻辑
        factor = pd.Series()
        return factor
    
    def analyze_distribution(self):
        """分析因子分布"""
        if self.factor_data is None:
            raise ValueError("请先计算因子")
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # 直方图
        axes[0].hist(self.factor_data.dropna(), bins=50, edgecolor='black')
        axes[0].set_title(f'{{FACTOR_NAME}} 分布')
        axes[0].set_xlabel('因子值')
        axes[0].set_ylabel('频数')
        
        # QQ图
        stats.probplot(self.factor_data.dropna(), plot=axes[1])
        axes[1].set_title('QQ图')
        
        plt.tight_layout()
        return fig
    
    def calculate_ic(self, returns, periods=[1, 5, 20]):
        """
        计算IC序列
        
        Args:
            returns: 收益率数据
            periods: 收益周期列表
            
        Returns:
            dict: IC统计结果
        """
        results = {{}}
        
        for period in periods:
            forward_returns = returns.shift(-period)
            ic_series = self.factor_data.corrwith(forward_returns)
            
            results[f'IC_{{period}}d'] = {{
                'mean': ic_series.mean(),
                'std': ic_series.std(),
                'ir': ic_series.mean() / ic_series.std() if ic_series.std() > 0 else 0,
                'positive_ratio': (ic_series > 0).mean()
            }}
        
        return results
    
    def layer_backtest(self, n_groups=5):
        """
        分层回测
        
        Args:
            n_groups: 分组数量
            
        Returns:
            pd.DataFrame: 各组收益
        """
        # 按因子值分组
        groups = pd.qcut(self.factor_data, n_groups, labels=False)
        
        # 计算各组收益
        group_returns = {{}}
        for i in range(n_groups):
            mask = groups == i
            group_returns[f'G{{i+1}}'] = self.returns_data[mask].mean()
        
        return pd.DataFrame(group_returns)
    
    def generate_report(self):
        """生成研究报告"""
        report = f"""
# {{FACTOR_NAME}} 因子研究报告

## 1. 基本信息
- 因子名称: {{FACTOR_NAME}}
- 研究周期: {{self.start_date}} ~ {{self.end_date}}
- 股票池: {{UNIVERSE}}

## 2. 因子分布
- 均值: {{self.factor_data.mean():.4f}}
- 标准差: {{self.factor_data.std():.4f}}
- 偏度: {{self.factor_data.skew():.4f}}
- 峰度: {{self.factor_data.kurtosis():.4f}}

## 3. IC分析
{{self._format_ic_results()}}

## 4. 分层回测
{{self._format_layer_results()}}

## 5. 结论
TODO: 填写研究结论
"""
        return report
    
    def _format_ic_results(self):
        """格式化IC结果"""
        return "TODO"
    
    def _format_layer_results(self):
        """格式化分层结果"""
        return "TODO"


if __name__ == '__main__':
    # 示例用法
    research = FactorResearch('2024-01-01', '2024-12-01')
    # research.calculate_factor(data)
    # research.analyze_distribution()
    print(f"因子研究模板: {{FACTOR_NAME}}")
'''
}


# ============================================================
# 策略管理类
# ============================================================

class StrategyManager:
    """策略管理器"""
    
    def __init__(self):
        self.strategies_cache = {}
        self._refresh_cache()
    
    def _refresh_cache(self):
        """刷新缓存"""
        self.strategies_cache = {}
        for platform, dir_path in STRATEGY_DIRS.items():
            if dir_path.exists():
                for py_file in dir_path.glob("*.py"):
                    if not py_file.name.startswith("__"):
                        self.strategies_cache[py_file.stem] = {
                            "platform": platform,
                            "path": str(py_file),
                            "name": py_file.stem,
                            "modified": datetime.fromtimestamp(py_file.stat().st_mtime)
                        }
    
    def list_strategies(self, platform: str = None) -> List[Dict]:
        """
        获取策略列表
        
        Args:
            platform: 平台筛选（ptrade/qmt/research/examples）
            
        Returns:
            策略列表
        """
        self._refresh_cache()
        
        strategies = []
        for name, info in self.strategies_cache.items():
            if platform and info["platform"] != platform:
                continue
            
            strategy = self._load_strategy_info(info["path"])
            strategy.update(info)
            strategies.append(strategy)
        
        # 按修改时间排序
        strategies.sort(key=lambda x: x.get("modified", datetime.min), reverse=True)
        return strategies
    
    def _load_strategy_info(self, path: str) -> Dict:
        """加载策略详细信息"""
        info = {
            "description": "",
            "parameters": {},
            "factors": [],
            "size": 0
        }
        
        try:
            file_path = Path(path)
            info["size"] = file_path.stat().st_size
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取描述（docstring）
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if docstring_match:
                info["description"] = docstring_match.group(1).strip()[:200]
            
            # 提取参数
            param_pattern = r'^([A-Z_]+)\s*=\s*(.+?)(?:\s*#.*)?$'
            for match in re.finditer(param_pattern, content, re.MULTILINE):
                param_name = match.group(1)
                param_value = match.group(2).strip()
                info["parameters"][param_name] = param_value
            
            # 提取因子（如果有FACTORS定义）
            factors_match = re.search(r'FACTORS\s*=\s*(\[.*?\]|\{.*?\})', content, re.DOTALL)
            if factors_match:
                try:
                    info["factors"] = eval(factors_match.group(1))
                except:
                    pass
                    
        except Exception as e:
            info["error"] = str(e)
        
        return info
    
    def get_strategy(self, name: str) -> Optional[Dict]:
        """
        获取策略详情
        
        Args:
            name: 策略名称
            
        Returns:
            策略详情
        """
        if name not in self.strategies_cache:
            self._refresh_cache()
        
        if name not in self.strategies_cache:
            return None
        
        info = self.strategies_cache[name]
        strategy = self._load_strategy_info(info["path"])
        strategy.update(info)
        
        # 读取完整代码
        try:
            with open(info["path"], 'r', encoding='utf-8') as f:
                strategy["code"] = f.read()
        except Exception as e:
            strategy["code"] = f"# 读取失败: {e}"
        
        return strategy
    
    def create_strategy(
        self,
        name: str,
        platform: str,
        template: str = None,
        description: str = "",
        parameters: Dict = None
    ) -> Tuple[bool, str]:
        """
        创建新策略
        
        Args:
            name: 策略名称
            platform: 目标平台
            template: 模板类型
            description: 描述
            parameters: 参数
            
        Returns:
            (成功标志, 消息或路径)
        """
        if platform not in STRATEGY_DIRS:
            return False, f"不支持的平台: {platform}"
        
        # 文件名安全处理
        safe_name = re.sub(r'[^\w\-]', '_', name)
        file_path = STRATEGY_DIRS[platform] / f"{safe_name}.py"
        
        if file_path.exists():
            return False, f"策略已存在: {safe_name}"
        
        # 生成代码
        params = parameters or {}
        params.setdefault("name", name)
        params.setdefault("description", description)
        params.setdefault("created_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.setdefault("initial_capital", 1000000)
        params.setdefault("max_position", 0.1)
        params.setdefault("stop_loss", 0.08)
        params.setdefault("take_profit", 0.2)
        params.setdefault("rebalance_days", 5)
        params.setdefault("factors_list", "- ROE\n- PE\n- 动量")
        params.setdefault("factors_config", "['ROE', 'PE', 'MOMENTUM']")
        params.setdefault("lookback_period", 20)
        params.setdefault("holding_period", 5)
        params.setdefault("top_n", 10)
        params.setdefault("stock_code", "600000.SH")
        params.setdefault("grid_size", 2)
        params.setdefault("grid_amount", 10000)
        params.setdefault("base_price", 10.0)
        params.setdefault("grid_count", 5)
        params.setdefault("universe", "沪深300")
        
        # 选择模板
        if template and template in STRATEGY_TEMPLATES:
            code = STRATEGY_TEMPLATES[template].format(**params)
        elif platform == "ptrade":
            code = STRATEGY_TEMPLATES["ptrade_multi_factor"].format(**params)
        elif platform == "qmt":
            code = STRATEGY_TEMPLATES["qmt_grid"].format(**params)
        elif platform == "research":
            code = STRATEGY_TEMPLATES["research_factor"].format(**params)
        else:
            code = f'''# -*- coding: utf-8 -*-
"""
策略名称: {name}
创建时间: {params["created_time"]}
描述: {description}
"""

# TODO: 实现策略逻辑
'''
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            self._refresh_cache()
            return True, str(file_path)
        except Exception as e:
            return False, str(e)
    
    def update_strategy(self, name: str, code: str) -> Tuple[bool, str]:
        """
        更新策略代码
        
        Args:
            name: 策略名称
            code: 新代码
            
        Returns:
            (成功标志, 消息)
        """
        if name not in self.strategies_cache:
            return False, "策略不存在"
        
        path = self.strategies_cache[name]["path"]
        
        try:
            # 备份
            backup_path = Path(path).with_suffix('.py.bak')
            shutil.copy(path, backup_path)
            
            # 写入
            with open(path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            self._refresh_cache()
            return True, "更新成功"
        except Exception as e:
            return False, str(e)
    
    def delete_strategy(self, name: str, archive: bool = True) -> Tuple[bool, str]:
        """
        删除策略
        
        Args:
            name: 策略名称
            archive: 是否归档（而非直接删除）
            
        Returns:
            (成功标志, 消息)
        """
        if name not in self.strategies_cache:
            return False, "策略不存在"
        
        path = Path(self.strategies_cache[name]["path"])
        
        try:
            if archive:
                # 移动到归档目录
                archive_path = STRATEGY_DIRS["archived"] / path.name
                if archive_path.exists():
                    archive_path = STRATEGY_DIRS["archived"] / f"{path.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
                shutil.move(str(path), str(archive_path))
                msg = f"已归档到: {archive_path}"
            else:
                # 直接删除
                path.unlink()
                msg = "已删除"
            
            self._refresh_cache()
            return True, msg
        except Exception as e:
            return False, str(e)
    
    def validate_strategy(self, name: str) -> Dict:
        """
        验证策略
        
        Args:
            name: 策略名称
            
        Returns:
            验证结果
        """
        strategy = self.get_strategy(name)
        if not strategy:
            return {"valid": False, "errors": ["策略不存在"]}
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        code = strategy.get("code", "")
        
        # 语法检查
        try:
            compile(code, strategy["path"], 'exec')
        except SyntaxError as e:
            result["valid"] = False
            result["errors"].append(f"语法错误 (行{e.lineno}): {e.msg}")
        
        # 必要函数检查
        platform = strategy.get("platform", "")
        if platform == "ptrade":
            required_funcs = ["initialize", "handle_data"]
            for func in required_funcs:
                if f"def {func}" not in code:
                    result["warnings"].append(f"缺少函数: {func}")
        
        # 参数检查
        params = strategy.get("parameters", {})
        if "INITIAL_CAPITAL" in params:
            try:
                capital = float(params["INITIAL_CAPITAL"])
                if capital < 10000:
                    result["warnings"].append("初始资金较小，建议至少10万")
            except:
                result["errors"].append("INITIAL_CAPITAL 格式错误")
        
        if "MAX_POSITION" in params:
            try:
                pos = float(params["MAX_POSITION"])
                if pos > 0.5:
                    result["warnings"].append("单票仓位过大，风险较高")
            except:
                result["errors"].append("MAX_POSITION 格式错误")
        
        # 代码质量检查
        if len(code) < 500:
            result["info"].append("代码较短，可能是模板")
        
        if "TODO" in code:
            result["info"].append("代码中存在TODO待完成项")
        
        if result["errors"]:
            result["valid"] = False
        
        return result
    
    def get_templates(self) -> List[Dict]:
        """获取可用模板列表"""
        templates = []
        for key, code in STRATEGY_TEMPLATES.items():
            # 提取描述
            match = re.search(r'"""(.*?)"""', code, re.DOTALL)
            desc = match.group(1).split('\n')[1].strip() if match else key
            
            templates.append({
                "key": key,
                "name": desc,
                "platform": key.split('_')[0] if '_' in key else "general"
            })
        
        return templates
    
    def copy_strategy(self, name: str, new_name: str, target_platform: str = None) -> Tuple[bool, str]:
        """
        复制策略
        
        Args:
            name: 源策略名称
            new_name: 新策略名称
            target_platform: 目标平台（默认同源）
            
        Returns:
            (成功标志, 消息或路径)
        """
        strategy = self.get_strategy(name)
        if not strategy:
            return False, "源策略不存在"
        
        platform = target_platform or strategy["platform"]
        
        # 修改代码中的名称
        code = strategy["code"]
        code = re.sub(r'策略名称:\s*\S+', f'策略名称: {new_name}', code)
        code = re.sub(r'创建时间:\s*\S+', f'创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', code)
        
        # 创建新文件
        safe_name = re.sub(r'[^\w\-]', '_', new_name)
        file_path = STRATEGY_DIRS[platform] / f"{safe_name}.py"
        
        if file_path.exists():
            return False, f"策略已存在: {safe_name}"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            self._refresh_cache()
            return True, str(file_path)
        except Exception as e:
            return False, str(e)


# ============================================================
# 全局实例
# ============================================================

strategy_manager = StrategyManager()


# ============================================================
# API函数（供Flask使用）
# ============================================================

def get_all_strategies(platform: str = None) -> List[Dict]:
    """获取所有策略"""
    return strategy_manager.list_strategies(platform)


def get_strategy_detail(name: str) -> Optional[Dict]:
    """获取策略详情"""
    return strategy_manager.get_strategy(name)


def create_new_strategy(name: str, platform: str, template: str = None, description: str = "", params: Dict = None) -> Dict:
    """创建新策略"""
    success, msg = strategy_manager.create_strategy(name, platform, template, description, params)
    return {"ok": success, "message": msg}


def update_existing_strategy(name: str, code: str) -> Dict:
    """更新策略"""
    success, msg = strategy_manager.update_strategy(name, code)
    return {"ok": success, "message": msg}


def delete_existing_strategy(name: str, archive: bool = True) -> Dict:
    """删除策略"""
    success, msg = strategy_manager.delete_strategy(name, archive)
    return {"ok": success, "message": msg}


def validate_strategy_code(name: str) -> Dict:
    """验证策略"""
    return strategy_manager.validate_strategy(name)


def get_strategy_templates() -> List[Dict]:
    """获取模板列表"""
    return strategy_manager.get_templates()


def copy_existing_strategy(name: str, new_name: str, platform: str = None) -> Dict:
    """复制策略"""
    success, msg = strategy_manager.copy_strategy(name, new_name, platform)
    return {"ok": success, "message": msg}
























































