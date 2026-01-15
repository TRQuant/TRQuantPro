"""
陈小群战法策略库

本库封装了陈小群战法的核心算法，包括：
1. 情绪周期判断
2. 选股逻辑（首板卡位术、龙头战法）
3. 持仓管理（三板加速术、止盈止损）

使用方式：
    from core.strategies.chen_xiaoqun import (
        judge_emotion_cycle,
        select_first_board_stocks,
        select_dragon_stocks,
        analyze_third_board,
        monitor_position,
        judge_stop_loss
    )
"""

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

__all__ = [
    'judge_emotion_cycle',
    'judge_emotion_cycle_with_confirmation',
    'select_first_board_stocks',
    'select_dragon_stocks',
    'identify_exchange_and_convert',
    'analyze_third_board',
    'monitor_position',
    'judge_stop_loss',
    'convert_code_to_jq',
    'validate_market_data',
    'fill_missing_data',
    'get_data_quality_stats',
    'identify_top_themes',
    'is_mainstream_theme',
    'get_theme_priority',
]
