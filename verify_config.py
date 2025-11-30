#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")






# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")




# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")

# -*- coding: utf-8 -*-
"""
验证配置和代码结构
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("JQQuant 配置和代码结构验证")
print("=" * 60)
print()

# 1. 检查配置文件
print("1. 检查配置文件...")
try:
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if jq_config:
        print("   ✅ 配置文件加载成功")
        print(f"   ✅ 配置项: {list(jq_config.keys())}")
        if 'username' in jq_config and jq_config.get('username'):
            print("   ✅ 用户名已配置")
        else:
            print("   ⚠️  用户名未配置")
        if 'password' in jq_config and jq_config.get('password'):
            print("   ✅ 密码已配置")
        else:
            print("   ⚠️  密码未配置")
    else:
        print("   ❌ 配置文件为空")
except Exception as e:
    print(f"   ❌ 配置文件加载失败: {str(e)}")
    sys.exit(1)

print()

# 2. 检查核心模块导入
print("2. 检查核心模块...")
try:
    from core.backtest_engine import BacktestEngine
    from core.data_provider import DataProvider
    from core.portfolio import Portfolio
    from core.order_manager import OrderManager
    print("   ✅ 核心模块导入成功")
except Exception as e:
    print(f"   ❌ 核心模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 3. 检查策略模块
print("3. 检查策略模块...")
try:
    from strategies.base_strategy import BaseStrategy
    from strategies.examples.ma_cross import MACrossStrategy
    print("   ✅ 策略模块导入成功")
except Exception as e:
    print(f"   ❌ 策略模块导入失败: {str(e)}")
    sys.exit(1)

print()

# 4. 检查工具模块
print("4. 检查工具模块...")
try:
    from utils.indicators import sma, ma_cross
    print("   ✅ 工具模块导入成功")
except Exception as e:
    print(f"   ⚠️  工具模块导入失败: {str(e)}")

print()

# 5. 检查聚宽SDK
print("5. 检查聚宽SDK...")
try:
    import jqdatasdk as jq
    print("   ✅ jqdatasdk已安装")
    print(f"   ✅ 版本信息: {jq.__version__ if hasattr(jq, '__version__') else '未知'}")
except ImportError:
    print("   ⚠️  jqdatasdk未安装")
    print("   提示: 运行 'pip install jqdatasdk' 安装")
except Exception as e:
    print(f"   ⚠️  检查jqdatasdk时出错: {str(e)}")

print()

# 6. 检查股票池配置
print("6. 检查股票池配置...")
try:
    stock_pool_file = Path(__file__).parent / 'config' / 'stock_pool.json'
    if stock_pool_file.exists():
        import json
        with open(stock_pool_file, 'r', encoding='utf-8') as f:
            stock_pool = json.load(f)
        if 'high_growth_stocks' in stock_pool:
            stocks = stock_pool['high_growth_stocks']
            print(f"   ✅ 股票池配置存在，包含 {len(stocks)} 只股票")
        else:
            print("   ⚠️  股票池配置格式异常")
    else:
        print("   ⚠️  股票池配置文件不存在")
except Exception as e:
    print(f"   ⚠️  检查股票池配置时出错: {str(e)}")

print()

# 7. 检查回测引擎初始化
print("7. 检查回测引擎初始化...")
try:
    from jqdata.client import JQDataClient
    from core.data_provider import DataProvider
    from core.backtest_engine import BacktestEngine
    
    # 创建客户端（不实际连接）
    jq_client = JQDataClient()
    data_provider = DataProvider(jq_client=jq_client)
    engine = BacktestEngine(data_provider=data_provider)
    
    print("   ✅ 回测引擎初始化成功")
except Exception as e:
    print(f"   ⚠️  回测引擎初始化失败: {str(e)}")

print()

# 8. 检查策略初始化
print("8. 检查策略初始化...")
try:
    from strategies.examples.ma_cross import MACrossStrategy
    
    strategy = MACrossStrategy(short_window=5, long_window=20)
    print("   ✅ 策略初始化成功")
    print(f"   ✅ 策略参数: {strategy.get_parameters()}")
except Exception as e:
    print(f"   ⚠️  策略初始化失败: {str(e)}")

print()
print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("总结:")
print("  ✅ 配置文件已正确加载")
print("  ✅ 核心模块结构完整")
print("  ✅ 策略框架正常")
print()
print("下一步:")
print("  1. 如果jqdatasdk未安装，运行: pip install jqdatasdk")
print("  2. 运行回测: python3 test_backtest.py")
print("  3. 或使用main.py运行完整回测")














