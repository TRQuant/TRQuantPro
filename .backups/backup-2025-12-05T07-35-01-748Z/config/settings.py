"""
系统配置文件
支持开发模式和生产模式
"""
import os
from pathlib import Path
from typing import Dict, Any
import json

# 检测运行模式
def get_project_root():
    """获取项目根目录"""
    # 优先使用环境变量
    if os.getenv('TRQUANT_DEV_MODE') == '1':
        return Path('/home/taotao/dev/QuantTest/TRQuant')
    
    # 检测当前文件位置
    current_file = Path(__file__).resolve()
    current_path = str(current_file)
    
    # 如果在dev目录，使用主项目
    if 'dev/QuantTest/TRQuant' in current_path:
        return Path('/home/taotao/dev/QuantTest/TRQuant')
    
    # 默认使用安装目录
    return Path(__file__).parent.parent

PROJECT_ROOT = get_project_root()

# 数据目录配置
_is_dev_mode = os.getenv('TRQUANT_DEV_MODE') == '1' or 'dev/QuantTest/TRQuant' in str(Path(__file__).resolve())

if _is_dev_mode:
    # 开发模式：数据目录在主项目
    DATA_DIR = PROJECT_ROOT / "data"
    CACHE_DIR = PROJECT_ROOT / "cache"
    LOGS_DIR = PROJECT_ROOT / "logs"
    REPORTS_DIR = PROJECT_ROOT / "reports"
    RESULTS_DIR = PROJECT_ROOT / "results"
else:
    # 生产模式：使用用户数据目录
    user_data_dir = Path.home() / '.local/share/trquant'
    DATA_DIR = user_data_dir / "data"
    CACHE_DIR = user_data_dir / "cache"
    LOGS_DIR = user_data_dir / "logs"
    REPORTS_DIR = user_data_dir / "reports"
    RESULTS_DIR = user_data_dir / "results"

STRATEGIES_DIR = PROJECT_ROOT / "strategies"

# 创建必要的目录
for dir_path in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# 默认回测参数
DEFAULT_BACKTEST_CONFIG = {
    "initial_cash": 1000000,  # 初始资金
    "commission_rate": 0.0003,  # 手续费率
    "slippage": 0.001,  # 滑点
    "benchmark": "000300.XSHG",  # 基准指数（沪深300）
}

# 加载聚宽配置
def load_jqdata_config() -> Dict[str, Any]:
    """加载聚宽配置"""
    config_path = PROJECT_ROOT / "config" / "jqdata_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "jqquant.log"
}

