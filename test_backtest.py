# -*- coding: utf-8 -*-
"""
测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)


测试回测功能
"""
import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import run_backtest
import logging

logging.basicConfig(level=logging.INFO)

def test_ma_cross_strategy():
    """测试均线交叉策略"""
    print("=" * 60)
    print("测试均线交叉策略回测")
    print("=" * 60)
    
    try:
        # 使用简单的股票池进行测试
        securities = ['000001.XSHE', '600000.XSHG']  # 平安银行、浦发银行
        
        # 使用账号允许的日期范围（根据账号权限调整）
        # 账号权限: 2024-08-17 至 2025-08-24
        results = run_backtest(
            strategy_name='ma_cross',
            start_date='2024-09-01',  # 使用允许范围内的日期
            end_date='2024-10-31',
            securities=securities,
            initial_cash=1000000,
            commission_rate=0.0003,
            slippage=0.001,
            strategy_params={
                'short_window': 5,
                'long_window': 20
            }
        )
        
        if results:
            print("\n✅ 回测测试成功！")
            print(f"总收益: {results['summary']['total_profit_rate']*100:.2f}%")
            print(f"年化收益: {results['metrics']['annual_return']*100:.2f}%")
            print(f"夏普比率: {results['metrics']['sharpe_ratio']:.2f}")
            return True
        else:
            print("\n❌ 回测测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 回测测试出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_ma_cross_strategy()
    sys.exit(0 if success else 1)

