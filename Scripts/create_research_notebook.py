#!/usr/bin/env python3
"""
QuantConnect Research 笔记本生成器

用法:
    python create_research_notebook.py [notebook_name] [--template template_name]

模板:
    - basic: 基础研究模板
    - backtest: 回测分析模板
    - data_analysis: 数据分析模板
    - strategy: 策略开发模板
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def create_basic_template():
    """基础研究模板"""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# QuantConnect Research 笔记本\n",
                    f"\n",
                    f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"**作者**: \n",
                    f"**描述**: \n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 标准配置 - 每个笔记本首格必备\n",
                    "from QuantConnect.Configuration import Config\n",
                    "Config.Set(\"data-folder\", \"/Lean/Data\")   # 指向容器挂载点\n",
                    "Config.Set(\"log-level\", \"ERROR\")          # 可选：安静日志\n",
                    "\n",
                    "print(\"配置完成\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 导入必要的库\n",
                    "from QuantConnect.Research import QuantBook\n",
                    "from QuantConnect import Resolution\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "# 设置图表样式\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette(\"husl\")\n",
                    "\n",
                    "print(\"库导入完成\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 初始化 QuantBook\n",
                    "qb = QuantBook()\n",
                    "print(\"QuantBook 初始化完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 数据获取\n",
                    "\n",
                    "在这里添加数据获取代码"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 示例：获取 SPY 数据\n",
                    "symbol = qb.AddEquity(\"SPY\").Symbol\n",
                    "history = qb.History([symbol], 30, Resolution.Daily)\n",
                    "print(f\"获取到 {len(history)} 条数据\")\n",
                    "history.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 分析代码\n",
                    "\n",
                    "在这里添加您的分析代码"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 在这里添加您的分析代码\n",
                    "pass"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.13"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }


def create_backtest_template():
    """回测分析模板"""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 回测分析笔记本\n",
                    f"\n",
                    f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"**回测ID**: \n",
                    f"**策略名称**: \n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 标准配置\n",
                    "from QuantConnect.Configuration import Config\n",
                    "Config.Set(\"data-folder\", \"/Lean/Data\")\n",
                    "Config.Set(\"log-level\", \"ERROR\")\n",
                    "\n",
                    "# 导入库\n",
                    "from QuantConnect.Research import QuantBook\n",
                    "from QuantConnect import Resolution\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import json\n",
                    "from pathlib import Path\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette(\"husl\")\n",
                    "\n",
                    "print(\"环境配置完成\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 加载回测结果\n",
                    "backtest_id = \"\"  # 填入回测ID\n",
                    "backtest_path = f\"../backtests/{backtest_id}\"\n",
                    "\n",
                    "if Path(backtest_path).exists():\n",
                    "    # 加载回测摘要\n",
                    "    with open(f\"{backtest_path}/{backtest_id}-summary.json\", 'r') as f:\n",
                    "        summary = json.load(f)\n",
                    "    \n",
                    "    # 加载订单事件\n",
                    "    with open(f\"{backtest_path}/{backtest_id}-order-events.json\", 'r') as f:\n",
                    "        orders = json.load(f)\n",
                    "    \n",
                    "    print(\"回测数据加载完成\")\n",
                    "    print(f\"回测期间: {summary.get('StartTime', 'N/A')} 到 {summary.get('EndTime', 'N/A')}\")\n",
                    "    print(f\"总收益率: {summary.get('TotalPerformance', {}).get('TotalReturn', 'N/A'):.2%}\")\n",
                    "else:\n",
                    "    print(f\"回测路径不存在: {backtest_path}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 回测结果分析\n",
                    "\n",
                    "### 关键指标"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 分析关键指标\n",
                    "if 'summary' in locals():\n",
                    "    perf = summary.get('TotalPerformance', {})\n",
                    "    \n",
                    "    print(\"=== 回测关键指标 ===\")\n",
                    "    print(f\"总收益率: {perf.get('TotalReturn', 'N/A'):.2%}\")\n",
                    "    print(f\"年化收益率: {perf.get('TotalReturn', 'N/A'):.2%}\")\n",
                    "    print(f\"夏普比率: {perf.get('SharpeRatio', 'N/A'):.2f}\")\n",
                    "    print(f\"最大回撤: {perf.get('Drawdown', 'N/A'):.2%}\")\n",
                    "    print(f\"胜率: {perf.get('WinRate', 'N/A'):.2%}\")\n",
                    "    print(f\"总交易次数: {perf.get('TotalTrades', 'N/A')}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 交易分析"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 分析交易记录\n",
                    "if 'orders' in locals():\n",
                    "    # 转换为DataFrame进行分析\n",
                    "    trades_df = pd.DataFrame(orders)\n",
                    "    \n",
                    "    print(f\"总交易次数: {len(trades_df)}\")\n",
                    "    print(f\"买入交易: {len(trades_df[trades_df['Direction'] == 'Buy'])}\")\n",
                    "    print(f\"卖出交易: {len(trades_df[trades_df['Direction'] == 'Sell'])}\")\n",
                    "    \n",
                    "    # 显示最近的交易\n",
                    "    trades_df.head(10)"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.13"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }


def create_data_analysis_template():
    """数据分析模板"""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 数据分析笔记本\n",
                    f"\n",
                    f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"**数据源**: \n",
                    f"**分析目标**: \n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 标准配置\n",
                    "from QuantConnect.Configuration import Config\n",
                    "Config.Set(\"data-folder\", \"/Lean/Data\")\n",
                    "Config.Set(\"log-level\", \"ERROR\")\n",
                    "\n",
                    "# 导入库\n",
                    "from QuantConnect.Research import QuantBook\n",
                    "from QuantConnect import Resolution\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from scipy import stats\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# 设置图表样式\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette(\"husl\")\n",
                    "plt.rcParams['figure.figsize'] = (12, 8)\n",
                    "\n",
                    "print(\"环境配置完成\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 初始化 QuantBook\n",
                    "qb = QuantBook()\n",
                    "print(\"QuantBook 初始化完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 数据获取与预处理"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 定义要分析的股票列表\n",
                    "symbols = [\"SPY\", \"QQQ\", \"IWM\"]  # 示例股票\n",
                    "\n",
                    "# 获取数据\n",
                    "data = {}\n",
                    "for symbol in symbols:\n",
                    "    try:\n",
                    "        s = qb.AddEquity(symbol).Symbol\n",
                    "        hist = qb.History([s], 252, Resolution.Daily)  # 一年数据\n",
                    "        data[symbol] = hist['close'].unstack(level=0)\n",
                    "        print(f\"{symbol}: 获取到 {len(hist)} 条数据\")\n",
                    "    except Exception as e:\n",
                    "        print(f\"{symbol}: 获取失败 - {e}\")\n",
                    "\n",
                    "# 合并数据\n",
                    "if data:\n",
                    "    df = pd.concat(data.values(), axis=1)\n",
                    "    df.columns = data.keys()\n",
                    "    print(f\"\\n数据形状: {df.shape}\")\n",
                    "    df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 数据探索性分析"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 基本统计信息\n",
                    "if 'df' in locals():\n",
                    "    print(\"=== 基本统计信息 ===\")\n",
                    "    print(df.describe())\n",
                    "    \n",
                    "    print(\"\\n=== 缺失值检查 ===\")\n",
                    "    print(df.isnull().sum())\n",
                    "    \n",
                    "    print(\"\\n=== 数据类型 ===\")\n",
                    "    print(df.dtypes)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 价格走势图\n",
                    "if 'df' in locals():\n",
                    "    plt.figure(figsize=(15, 8))\n",
                    "    for col in df.columns:\n",
                    "        plt.plot(df.index, df[col], label=col, linewidth=2)\n",
                    "    \n",
                    "    plt.title('价格走势对比', fontsize=16)\n",
                    "    plt.xlabel('日期')\n",
                    "    plt.ylabel('价格')\n",
                    "    plt.legend()\n",
                    "    plt.grid(True, alpha=0.3)\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 收益率分析"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 计算收益率\n",
                    "if 'df' in locals():\n",
                    "    returns = df.pct_change().dropna()\n",
                    "    \n",
                    "    print(\"=== 收益率统计 ===\")\n",
                    "    print(returns.describe())\n",
                    "    \n",
                    "    # 累积收益率\n",
                    "    cum_returns = (1 + returns).cumprod()\n",
                    "    \n",
                    "    plt.figure(figsize=(15, 8))\n",
                    "    for col in cum_returns.columns:\n",
                    "        plt.plot(cum_returns.index, cum_returns[col], label=col, linewidth=2)\n",
                    "    \n",
                    "    plt.title('累积收益率对比', fontsize=16)\n",
                    "    plt.xlabel('日期')\n",
                    "    plt.ylabel('累积收益率')\n",
                    "    plt.legend()\n",
                    "    plt.grid(True, alpha=0.3)\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.13"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }


def create_strategy_template():
    """策略开发模板"""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 策略开发笔记本\n",
                    f"\n",
                    f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"**策略名称**: \n",
                    f"**策略描述**: \n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 标准配置\n",
                    "from QuantConnect.Configuration import Config\n",
                    "Config.Set(\"data-folder\", \"/Lean/Data\")\n",
                    "Config.Set(\"log-level\", \"ERROR\")\n",
                    "\n",
                    "# 导入库\n",
                    "from QuantConnect.Research import QuantBook\n",
                    "from QuantConnect import Resolution\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from datetime import datetime, timedelta\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# 设置图表样式\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette(\"husl\")\n",
                    "plt.rcParams['figure.figsize'] = (12, 8)\n",
                    "\n",
                    "print(\"环境配置完成\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 初始化 QuantBook\n",
                    "qb = QuantBook()\n",
                    "print(\"QuantBook 初始化完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 策略参数设置"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 策略参数\n",
                    "class StrategyParams:\n",
                    "    # 交易标的\n",
                    "    SYMBOL = \"SPY\"\n",
                    "    \n",
                    "    # 回测期间\n",
                    "    START_DATE = \"2020-01-01\"\n",
                    "    END_DATE = \"2024-01-01\"\n",
                    "    \n",
                    "    # 策略参数\n",
                    "    LOOKBACK_PERIOD = 20\n",
                    "    THRESHOLD = 0.02\n",
                    "    \n",
                    "    # 资金管理\n",
                    "    INITIAL_CAPITAL = 100000\n",
                    "    POSITION_SIZE = 0.1  # 每次交易使用资金的10%\n",
                    "\n",
                    "params = StrategyParams()\n",
                    "print(\"策略参数设置完成\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 数据获取"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 获取历史数据\n",
                    "symbol = qb.AddEquity(params.SYMBOL).Symbol\n",
                    "history = qb.History([symbol], \n",
                    "                      start=params.START_DATE, \n",
                    "                      end=params.END_DATE, \n",
                    "                      resolution=Resolution.Daily)\n",
                    "\n",
                    "print(f\"获取到 {len(history)} 条数据\")\n",
                    "print(f\"数据期间: {history.index[0]} 到 {history.index[-1]}\")\n",
                    "history.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 策略逻辑实现"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 策略信号生成\n",
                    "def generate_signals(prices, lookback=20, threshold=0.02):\n",
                    "    \"\"\"生成交易信号\"\"\"\n",
                    "    # 计算移动平均\n",
                    "    ma = prices.rolling(window=lookback).mean()\n",
                    "    \n",
                    "    # 计算价格偏离度\n",
                    "    deviation = (prices - ma) / ma\n",
                    "    \n",
                    "    # 生成信号\n",
                    "    signals = pd.Series(0, index=prices.index)\n",
                    "    signals[deviation > threshold] = 1   # 买入信号\n",
                    "    signals[deviation < -threshold] = -1 # 卖出信号\n",
                    "    \n",
                    "    return signals, ma, deviation\n",
                    "\n",
                    "# 应用策略\n",
                    "prices = history['close'].unstack(level=0)[symbol]\n",
                    "signals, ma, deviation = generate_signals(prices, \n",
                    "                                         params.LOOKBACK_PERIOD, \n",
                    "                                         params.THRESHOLD)\n",
                    "\n",
                    "print(f\"生成 {len(signals[signals != 0])} 个交易信号\")\n",
                    "print(f\"买入信号: {len(signals[signals == 1])}\")\n",
                    "print(f\"卖出信号: {len(signals[signals == -1])}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 策略可视化"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 绘制策略图表\n",
                    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))\n",
                    "\n",
                    "# 价格和移动平均\n",
                    "ax1.plot(prices.index, prices, label='价格', linewidth=2)\n",
                    "ax1.plot(ma.index, ma, label=f'{params.LOOKBACK_PERIOD}日移动平均', linewidth=2)\n",
                    "\n",
                    "# 标记交易信号\n",
                    "buy_signals = prices[signals == 1]\n",
                    "sell_signals = prices[signals == -1]\n",
                    "\n",
                    "ax1.scatter(buy_signals.index, buy_signals, color='green', marker='^', s=100, label='买入信号')\n",
                    "ax1.scatter(sell_signals.index, sell_signals, color='red', marker='v', s=100, label='卖出信号')\n",
                    "\n",
                    "ax1.set_title('策略信号图', fontsize=16)\n",
                    "ax1.set_ylabel('价格')\n",
                    "ax1.legend()\n",
                    "ax1.grid(True, alpha=0.3)\n",
                    "\n",
                    "# 偏离度\n",
                    "ax2.plot(deviation.index, deviation, label='价格偏离度', linewidth=2)\n",
                    "ax2.axhline(y=params.THRESHOLD, color='red', linestyle='--', label=f'阈值 (+{params.THRESHOLD:.1%})')\n",
                    "ax2.axhline(y=-params.THRESHOLD, color='red', linestyle='--', label=f'阈值 (-{params.THRESHOLD:.1%})')\n",
                    "ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)\n",
                    "\n",
                    "ax2.set_title('价格偏离度', fontsize=16)\n",
                    "ax2.set_xlabel('日期')\n",
                    "ax2.set_ylabel('偏离度')\n",
                    "ax2.legend()\n",
                    "ax2.grid(True, alpha=0.3)\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.13"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }


def get_template(template_name):
    """获取指定模板"""
    templates = {
        "basic": create_basic_template,
        "backtest": create_backtest_template,
        "data_analysis": create_data_analysis_template,
        "strategy": create_strategy_template
    }
    
    if template_name not in templates:
        print(f"错误: 未知模板 '{template_name}'")
        print(f"可用模板: {', '.join(templates.keys())}")
        return None
    
    return templates[template_name]()


def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("用法: python create_research_notebook.py <notebook_name> [--template template_name]")
        print("示例: python create_research_notebook.py my_analysis --template basic")
        print("可用模板: basic, backtest, data_analysis, strategy")
        return
    
    notebook_name = sys.argv[1]
    template_name = "basic"  # 默认模板
    
    # 解析命令行参数
    if len(sys.argv) > 2 and sys.argv[2] == "--template":
        if len(sys.argv) > 3:
            template_name = sys.argv[3]
        else:
            print("错误: --template 参数后需要指定模板名称")
            return
    
    # 确保文件名有 .ipynb 扩展名
    if not notebook_name.endswith('.ipynb'):
        notebook_name += '.ipynb'
    
    # 获取模板
    template = get_template(template_name)
    if template is None:
        return
    
    # 创建笔记本文件
    try:
        with open(notebook_name, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 成功创建笔记本: {notebook_name}")
        print(f"📝 使用模板: {template_name}")
        print(f"📁 文件位置: {os.path.abspath(notebook_name)}")
        
    except Exception as e:
        print(f"❌ 创建笔记本失败: {e}")


if __name__ == "__main__":
    main() 