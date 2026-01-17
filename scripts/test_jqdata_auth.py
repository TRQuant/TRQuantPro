#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试聚宽认证
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import jqdatasdk as jq
from config.config_manager import get_config_manager


def test_auth():
    """测试聚宽认证"""
    try:
        # 获取配置
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        
        if not jq_config:
            print("❌ 配置文件不存在或为空")
            print(f"   请检查: {cm.config_dir / 'jqdata_config.json'}")
            return False
        
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if not username or not password:
            print("❌ 用户名或密码未配置")
            print(f"   请检查配置文件: {cm.config_dir / 'jqdata_config.json'}")
            return False
        
        # 认证
        print(f"正在认证用户: {username}...")
        jq.auth(username, password)
        
        # 验证
        if jq.is_auth():
            print("✅ 认证成功！")
            
            # 检查查询次数
            try:
                query_count = jq.get_query_count()
                spare = query_count.get('spare', 'N/A')
                total = query_count.get('total', 'N/A')
                used = total - spare if isinstance(total, int) and isinstance(spare, int) else 'N/A'
                
                print(f"\n📊 查询次数统计:")
                print(f"   剩余查询次数: {spare}")
                print(f"   总查询次数: {total}")
                if isinstance(used, int):
                    print(f"   已使用查询次数: {used}")
            except Exception as e:
                print(f"⚠️  无法获取查询次数: {e}")
            
            # 测试简单查询
            try:
                print(f"\n🧪 测试数据查询...")
                trade_days = jq.get_trade_days(end_date='2025-01-05', count=5)
                print(f"   ✅ 成功获取最近5个交易日: {len(trade_days)} 个")
                print(f"   最近交易日: {trade_days[-1] if trade_days else 'N/A'}")
            except Exception as e:
                print(f"   ⚠️  数据查询测试失败: {e}")
            
            return True
        else:
            print("❌ 认证失败")
            print("   请检查:")
            print("   1. 用户名和密码是否正确")
            print("   2. 网络连接是否正常")
            print("   3. 账号是否有效（未过期）")
            return False
            
    except Exception as e:
        print(f"❌ 认证异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("聚宽（JQData）认证测试")
    print("=" * 60)
    print()
    
    success = test_auth()
    
    print()
    print("=" * 60)
    if success:
        print("✅ 测试通过")
    else:
        print("❌ 测试失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
