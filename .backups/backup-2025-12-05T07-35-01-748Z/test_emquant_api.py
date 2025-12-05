#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试东方财富Choice API (EMQuantAPI)
评估其作为数据源的可行性
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

try:
    from EmQuantAPI import *
    print("✅ EmQuantAPI 导入成功")
except ImportError as e:
    print(f"❌ EmQuantAPI 导入失败: {e}")
    print("请确保已运行 installEmQuantAPI.py 安装")
    sys.exit(1)

def test_api_availability():
    """测试API基本可用性"""
    print("\n" + "="*60)
    print("测试1: API基本功能检查")
    print("="*60)
    
    # 检查主要函数是否存在
    required_functions = ['start', 'stop', 'cfc', 'cec', 'css', 'cst']
    available_functions = [func for func in dir(c) if not func.startswith('_')]
    
    print(f"可用函数数量: {len(available_functions)}")
    print(f"主要函数检查:")
    for func in required_functions:
        if func in available_functions:
            print(f"  ✅ {func}")
        else:
            print(f"  ❌ {func} (缺失)")
    
    return True

def test_login(username=None, password=None):
    """测试登录功能（需要账号）"""
    print("\n" + "="*60)
    print("测试2: 登录功能")
    print("="*60)
    
    # 首先尝试令牌登录
    print("尝试使用令牌登录（无需账号密码）...")
    try:
        loginResult = c.start("ForceLogin=1", '', None)
        if loginResult.ErrorCode == 0:
            print("✅ 登录成功（使用令牌）")
            return True
    except Exception as e:
        print(f"令牌登录失败: {e}")
    
    # 如果令牌登录失败，尝试账号密码登录
    if username and password:
        print(f"\n尝试使用账号密码登录: {username}")
        try:
            startoptions = f"ForceLogin=1,UserName={username},Password={password}"
            loginResult = c.start(startoptions, '', None)
            if loginResult.ErrorCode == 0:
                print("✅ 登录成功（使用账号密码）")
                return True
            else:
                print(f"⚠️  登录失败: {loginResult.ErrorMsg}")
                return False
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    else:
        print("⚠️  需要账号密码登录，但未提供凭据")
        return False

def test_data_functions():
    """测试数据获取功能"""
    print("\n" + "="*60)
    print("测试3: 数据获取功能")
    print("="*60)
    
    # 测试cfc函数（获取基础数据）
    print("测试 cfc (获取基础数据)...")
    try:
        # 使用测试代码
        data = c.cfc("000001.SZ", "CODE,NAME", "FunType=css")
        if data.ErrorCode == 0:
            print("✅ cfc 调用成功")
            print(f"   返回数据: {data.Data}")
            return True
        else:
            print(f"⚠️  cfc 调用失败: {data.ErrorMsg}")
            return False
    except Exception as e:
        print(f"❌ cfc 调用异常: {e}")
        return False

def test_stock_data():
    """测试股票数据获取"""
    print("\n" + "="*60)
    print("测试4: 股票行情数据")
    print("="*60)
    
    # 测试css函数（获取历史行情）
    print("测试 css (获取历史行情)...")
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        
        data = c.css("000001.SZ", "OPEN,CLOSE,HIGH,LOW,VOLUME", 
                     f"TradeDate={start_date},TradeDate={end_date},Ispandas=0")
        
        if data.ErrorCode == 0:
            print("✅ css 调用成功")
            print(f"   数据条数: {len(data.Data.get('000001.SZ', []))}")
            return True
        else:
            print(f"⚠️  css 调用失败: {data.ErrorMsg}")
            return False
    except Exception as e:
        print(f"❌ css 调用异常: {e}")
        return False

def evaluate_as_data_source():
    """评估作为数据源的可行性"""
    print("\n" + "="*60)
    print("数据源评估")
    print("="*60)
    
    evaluation = {
        "优点": [
            "✅ 官方API，数据质量有保障",
            "✅ 支持实时行情和历史数据",
            "✅ 支持多种数据类型（行情、财务、资讯等）",
            "✅ 有Python3版本，兼容性好",
            "✅ 支持Linux系统",
        ],
        "缺点": [
            "⚠️  需要账号登录（可能需要付费）",
            "⚠️  需要网络连接",
            "⚠️  可能有流量限制",
            "⚠️  需要处理登录状态和重连",
        ],
        "适用场景": [
            "✓ 需要高质量、官方数据源",
            "✓ 需要实时行情数据",
            "✓ 需要财务数据和资讯数据",
            "✓ 作为主要数据源或备用数据源",
        ],
        "集成建议": [
            "1. 创建 EmQuantProvider 类（类似 TuShareProvider）",
            "2. 实现登录管理和自动重连",
            "3. 实现数据缓存机制",
            "4. 集成到 data_center.py 的数据源优先级列表",
            "5. 处理账号认证和配置管理",
        ]
    }
    
    for category, items in evaluation.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")

def main():
    """主测试函数"""
    print("="*60)
    print("东方财富Choice API (EMQuantAPI) 测试")
    print("="*60)
    
    # 基本功能检查
    test_api_availability()
    
    # 尝试登录（从配置文件读取账号密码）
    import json
    from pathlib import Path
    config_file = Path(__file__).parent / "config" / "emquant_config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        username = config.get("username", "")
        password = config.get("password", "")
    else:
        print(f"⚠️  配置文件不存在: {config_file}")
        print("   请创建配置文件并填写账号密码")
        username = ""
        password = ""
    logged_in = test_login(username, password) if username and password else False
    
    if logged_in:
        # 如果登录成功，测试数据功能
        test_data_functions()
        test_stock_data()
        
        # 测试完成后退出
        try:
            c.stop()
            print("\n✅ API已停止")
        except:
            pass
    else:
        print("\n⚠️  未登录，跳过数据功能测试")
    
    # 评估
    evaluate_as_data_source()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)

if __name__ == "__main__":
    main()

