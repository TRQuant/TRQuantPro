#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JQData账号权限检查脚本
=====================

确认账号类型、数据权限范围和连接状态
"""
import sys
from pathlib import Path
import json
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager

def check_jqdata_account():
    """检查JQData账号信息"""
    print("=" * 70)
    print("JQData账号权限检查")
    print("=" * 70)
    
    try:
        # 读取配置
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        
        print("\n📋 配置信息:")
        print(f"  用户名: {jq_config.get('username', 'N/A')}")
        print(f"  账号类型: {jq_config.get('account_type', 'N/A')}")
        print(f"  备注: {jq_config.get('account_note', 'N/A')}")
        
        # 导入JQData SDK
        try:
            import jqdatasdk as jq
            print("\n✅ jqdatasdk已安装")
        except ImportError:
            print("\n❌ jqdatasdk未安装，无法查询账号信息")
            return
        
        # 认证
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if not username or not password:
            print("\n❌ 配置文件中缺少用户名或密码")
            return
        
        print(f"\n🔐 正在认证账号: {username}")
        try:
            jq.auth(username, password)
            print("✅ 认证成功")
        except Exception as e:
            print(f"❌ 认证失败: {e}")
            return
        
        # 查询账号信息
        print("\n📊 查询账号信息...")
        try:
            account_info = jq.get_account_info()
            print("\n✅ 账号信息:")
            print(json.dumps(account_info, indent=2, ensure_ascii=False))
            
            # 解析账号信息
            print("\n" + "-" * 70)
            print("📋 账号权限详情:")
            print("-" * 70)
            
            # 手机号
            mob = account_info.get('mob', 'N/A')
            print(f"  手机号: {mob}")
            
            # 每日查询限制
            query_limit = account_info.get('query_count_limit', 0)
            if query_limit >= 200000000:
                account_type = "正式账号（高级版）"
                daily_quota = "2亿条/天"
            elif query_limit >= 1000000:
                account_type = "正式账号（标准版）"
                daily_quota = f"{query_limit/10000:.0f}万条/天"
            else:
                account_type = "试用账号"
                daily_quota = f"{query_limit/10000:.0f}万条/天"
            print(f"  账号类型: {account_type}")
            print(f"  每日流量: {daily_quota} ({query_limit:,}条/天)")
            
            # License类型
            license_type = account_info.get('license', 0)
            print(f"  License类型: {license_type}")
            
            # 有效期
            expire_time = account_info.get('expire_time', 'N/A')
            print(f"  有效期至: {expire_time}")
            
            # 数据范围
            date_range_start = account_info.get('date_range_start', 'N/A')
            date_range_end = account_info.get('date_range_end', 'N/A')
            print(f"  数据开始日期: {date_range_start}")
            print(f"  数据结束日期: {date_range_end}")
            
            # 计算数据范围天数
            days_range = None
            if date_range_start != 'N/A' and date_range_end != 'N/A':
                if date_range_start == '*' or date_range_end == '*':
                    # 正式账号，数据范围无限制
                    print(f"\n  ✅ 数据范围: 正式账号（数据范围无限制）")
                    print(f"     可以访问从2005-01-01至今的历史数据")
                    days_range = 999999  # 标记为无限制
                else:
                    try:
                        start_dt = datetime.strptime(date_range_start, "%Y-%m-%d %H:%M:%S")
                        end_dt = datetime.strptime(date_range_end, "%Y-%m-%d %H:%M:%S")
                        days_range = (end_dt - start_dt).days
                        print(f"  数据范围天数: {days_range}天 ({days_range/365:.1f}年)")
                        
                        # 判断账号类型
                        if days_range > 4000:  # 超过11年，肯定是正式账号
                            print(f"\n  ✅ 数据范围: 正式账号（数据范围无限制）")
                            print(f"     可以访问从{start_dt.strftime('%Y-%m-%d')}至今的历史数据")
                        elif days_range > 400:  # 超过1年，可能是正式账号
                            print(f"\n  ⚠️  数据范围: 可能是正式账号（范围{days_range}天）")
                        else:
                            print(f"\n  ⚠️  数据范围: 试用账号（范围{days_range}天，约1年）")
                    except Exception as e:
                        print(f"\n  ⚠️  无法解析日期范围: {e}")
            
            # 测试数据访问
            print("\n" + "-" * 70)
            print("🧪 测试数据访问:")
            print("-" * 70)
            
            # 测试获取股票列表
            try:
                stocks = jq.get_all_securities(types=['stock'], date='2020-01-01')
                stock_count = len(stocks)
                print(f"  ✅ 股票列表: {stock_count}只股票（2020-01-01）")
            except Exception as e:
                print(f"  ❌ 股票列表获取失败: {e}")
            
            # 测试获取历史数据（测试早期日期）
            try:
                test_data = jq.get_price('000001.XSHE', start_date='2005-01-01', end_date='2005-01-10', frequency='daily')
                if len(test_data) > 0:
                    print(f"  ✅ 历史数据: 可以访问2005-01-01的历史数据")
                    print(f"     示例: 000001.XSHE ({len(test_data)}条记录)")
                else:
                    print(f"  ⚠️  历史数据: 2005-01-01无数据（可能不在数据范围内）")
            except Exception as e:
                error_msg = str(e)
                if "超出范围" in error_msg or "不在范围内" in error_msg:
                    print(f"  ⚠️  历史数据: 2005-01-01不在数据范围内（试用账号限制）")
                else:
                    print(f"  ❌ 历史数据获取失败: {e}")
            
            # 测试获取指数成分股
            try:
                index_stocks = jq.get_index_stocks('000300.XSHG', date='2020-01-01')
                print(f"  ✅ 指数成分股: 000300.XSHG ({len(index_stocks)}只，2020-01-01）")
            except Exception as e:
                print(f"  ❌ 指数成分股获取失败: {e}")
            
            # 总结
            print("\n" + "=" * 70)
            print("📋 总结:")
            print("=" * 70)
            
            if query_limit >= 200000000 and (days_range is None or days_range > 4000 or date_range_start == '*'):
                print("  ✅ 账号类型: 正式账号（高级版）")
                print("  ✅ 数据权限: 完整历史数据（2005-01-01至今）")
                print("  ✅ 数据范围: 无限制（*表示无限制）")
                print("  ✅ 每日流量: 2亿条/天")
                print("  ✅ 有效期至: 2027-01-31")
            elif query_limit >= 1000000:
                print("  ✅ 账号类型: 正式账号（标准版）")
                print("  ✅ 数据权限: 完整历史数据")
                print("  ✅ 数据范围: 无限制")
                print(f"  ✅ 每日流量: {daily_quota}")
            else:
                print("  ⚠️  账号类型: 试用账号")
                print("  ⚠️  数据权限: 受限（前15个月~前3个月）")
                if days_range:
                    print(f"  ⚠️  数据范围: {days_range}天")
                print(f"  ⚠️  每日流量: {daily_quota}")
            
            print("\n" + "=" * 70)
            
        except Exception as e:
            print(f"❌ 查询账号信息失败: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        print(f"\n❌ 检查过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_jqdata_account()
