"""
Notebook研究工具库
==================
为Jupyter Notebook研究提供统一的工具接口

主要模块：
- research_init: 统一环境初始化
- error_handling: 错误处理工具
- result_saver: 结果保存工具
- research_utils: 研究工具函数
- factor_utils: 因子分析工具
- portfolio_utils: 组合优化工具
- optim_utils: 参数优化工具
- viz_utils: 可视化工具
"""

# ==========================================
# 环境初始化模块（优先导入）
# ==========================================
from .research_init import (
    setup_research_environment,
    get_environment,
    get_project_root,
    get_jqdata_client as init_jqdata_client,
    get_trend_analyzer,
    get_market_evaluator,
    get_signal_provider,
    ResearchEnvironment,
)

# ==========================================
# 错误处理模块
# ==========================================
from .error_handling import (
    safe_call,
    retry_on_failure,
    with_fallback,
    error_context,
    ErrorBoundary,
    get_friendly_message,
    print_error_summary,
)

# ==========================================
# 结果保存模块
# ==========================================
from .result_saver import (
    ResultSaver,
    save_result,
    load_result,
    compare_results,
    ResultMetadata,
)

# ==========================================
# 数据缓存模块
# ==========================================
from .data_cache import (
    DataCache,
    get_data_cache,
    clear_cache,
    cached_get_price,
    cached_get_fundamentals,
)

# ==========================================
# 原有研究工具
# ==========================================
from .research_utils import (
    get_jqdata_client,
    search_knowledge_base,
    save_research_conclusion
)
from .factor_utils import (
    analyze_factor,
    calculate_ic_ir,
    factor_quantile_returns
)
from .portfolio_utils import (
    optimize_portfolio,
    calculate_portfolio_metrics
)
# 参数优化工具（可选，需要 optuna）
try:
    from .optim_utils import (
        optimize_strategy_params,
        create_optuna_study
    )
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    optimize_strategy_params = None
    create_optuna_study = None

# ==========================================
# 可视化模块（可选）
# ==========================================
try:
    from .viz_utils import (
        plot_factor_analysis,
        plot_portfolio_performance,
        plot_optimization_history
    )
    VIZ_AVAILABLE = True
except ImportError:
    VIZ_AVAILABLE = False
    plot_factor_analysis = None
    plot_portfolio_performance = None
    plot_optimization_history = None

# ==========================================
# 统一可视化样式模块
# ==========================================
try:
    from .viz_style import (
        apply_style,
        get_color_scheme,
        ColorScheme,
        ParameterWidgets,
        create_parameter_widgets,
        style_dataframe,
    )
    STYLE_AVAILABLE = True
except ImportError:
    STYLE_AVAILABLE = False
    apply_style = None
    get_color_scheme = None
    ColorScheme = None
    ParameterWidgets = None
    create_parameter_widgets = None
    style_dataframe = None

# ==========================================
# Graphviz 流程图模块（Dark Mode 默认）
# ==========================================
try:
    from .graphviz_utils import (
        create_flowchart,    # 创建流程图
        add_node,            # 添加节点
        add_edge,            # 添加边
        render,              # 渲染显示
        quick_flowchart,     # 快速创建
        DARK_COLORS,         # 颜色方案
    )
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    create_flowchart = None
    add_node = None
    add_edge = None
    render = None
    quick_flowchart = None
    DARK_COLORS = None

__all__ = [
    # research_init
    'setup_research_environment',
    'get_environment',
    'get_project_root',
    'get_trend_analyzer',
    'get_market_evaluator',
    'get_signal_provider',
    'ResearchEnvironment',
    # error_handling
    'safe_call',
    'retry_on_failure',
    'with_fallback',
    'error_context',
    'ErrorBoundary',
    'get_friendly_message',
    'print_error_summary',
    # result_saver
    'ResultSaver',
    'save_result',
    'load_result',
    'compare_results',
    'ResultMetadata',
    # data_cache
    'DataCache',
    'get_data_cache',
    'clear_cache',
    'cached_get_price',
    'cached_get_fundamentals',
    # research_utils
    'get_jqdata_client',
    'search_knowledge_base',
    'save_research_conclusion',
    # factor_utils
    'analyze_factor',
    'calculate_ic_ir',
    'factor_quantile_returns',
    # portfolio_utils
    'optimize_portfolio',
    'calculate_portfolio_metrics',
    # optim_utils
    'optimize_strategy_params',
    'create_optuna_study',
    'OPTUNA_AVAILABLE',
    # viz_utils
    'plot_factor_analysis',
    'plot_portfolio_performance',
    'plot_optimization_history',
    'VIZ_AVAILABLE',
    # viz_style
    'apply_style',
    'get_color_scheme',
    'ColorScheme',
    'ParameterWidgets',
    'create_parameter_widgets',
    'style_dataframe',
    'STYLE_AVAILABLE',
    # graphviz_utils
    'create_flowchart',
    'add_node',
    'add_edge',
    'render',
    'quick_flowchart',
    'DARK_COLORS',
    'GRAPHVIZ_AVAILABLE',
]


# 隐藏代码工具
from notebooks.lib.hide_code import add_hide_code_button
