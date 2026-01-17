"""
陈小群战法策略库

本库封装了陈小群战法的核心算法，包括：
1. 情绪周期判断
2. 选股逻辑（首板卡位术、龙头战法）
3. 持仓管理（三板加速术、止盈止损）
4. 回测引擎（完整的回测框架）

使用方式：
    from core.strategies.chen_xiaoqun import (
        # 回测引擎
        ChenXiaoqunBacktestConfig,
        ChenXiaoqunBacktestEngine,
        ChenXiaoqunBacktestResult,
        run_chen_xiaoqun_backtest,
        
        # 策略函数
        judge_emotion_cycle,
        select_first_board_stocks,
        select_dragon_stocks,
        analyze_third_board,
        monitor_position,
        judge_stop_loss
    )
"""

from .backtest_engine import (
    ChenXiaoqunBacktestConfig,
    ChenXiaoqunBacktestEngine,
    ChenXiaoqunBacktestResult,
    run_chen_xiaoqun_backtest
)
from .emotion_cycle import judge_emotion_cycle, judge_emotion_cycle_with_confirmation
from .stock_selection import (
    select_first_board_stocks,
    select_dragon_stocks,
    identify_exchange_and_convert
)
from .position_management import (
    analyze_third_board,
    monitor_position,
    judge_stop_loss
)
from .utils import convert_code_to_jq
from .data_validator import (
    validate_market_data,
    fill_missing_data,
    get_data_quality_stats
)
from .theme_analyzer import (
    identify_top_themes,
    is_mainstream_theme,
    get_theme_priority
)
from .consecutive_board_selector import (
    select_consecutive_board_stocks,
    confirm_second_board,
    get_board_count_verified
)
from .exit_decision import (
    should_exit_position,
    should_reduce_position
)

__all__ = [
    # 回测引擎
    'ChenXiaoqunBacktestConfig',
    'ChenXiaoqunBacktestEngine',
    'ChenXiaoqunBacktestResult',
    'run_chen_xiaoqun_backtest',
    # 情绪周期
    'judge_emotion_cycle',
    'judge_emotion_cycle_with_confirmation',
    # 选股
    'select_first_board_stocks',
    'select_dragon_stocks',
    'identify_exchange_and_convert',
    # 持仓管理
    'analyze_third_board',
    'monitor_position',
    'judge_stop_loss',
    # 工具函数
    'convert_code_to_jq',
    'validate_market_data',
    'fill_missing_data',
    'get_data_quality_stats',
    'identify_top_themes',
    'is_mainstream_theme',
    'get_theme_priority',
    'should_exit_position',
    'should_reduce_position',
    # 连板股票选择器
    'select_consecutive_board_stocks',
    'confirm_second_board',
    'get_board_count_verified',
]
