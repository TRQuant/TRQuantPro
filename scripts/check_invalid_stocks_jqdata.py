#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查无法转换的股票在JQData中是否存在
"""

import sys
from pathlib import Path

# 添加项目路径
current_dir = Path.cwd()
project_root = None
for parent in [current_dir] + list(current_dir.parents):
    if (parent / 'core').exists() and (parent / 'config').exists():
        project_root = parent
        break

if project_root is None:
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 导入必要的模块
from notebooks.lib import setup_research_environment
import akshare as ak
from datetime import datetime, timezone, timedelta

def cn_today_str():
    """获取中国时间（UTC+8）的当前日期字符串"""
    cn_now = datetime.now(timezone.utc) + timedelta(hours=8)
    return cn_now.strftime('%Y-%m-%d')

def cn_today_str_compact():
    """获取中国时间（UTC+8）的当前日期字符串（紧凑格式YYYYMMDD）"""
    cn_now = datetime.now(timezone.utc) + timedelta(hours=8)
    return cn_now.strftime('%Y%m%d')

def convert_code_to_jq(code):
    """将AKShare股票代码转换为JQData格式"""
    if not code:
        return None
    code_str = str(code)
    if len(code_str) == 6:
        if code_str.startswith('00') or code_str.startswith('30'):
            return f"{code_str}.XSHE"  # 深市
        elif code_str.startswith('60') or code_str.startswith('68'):
            return f"{code_str}.XSHG"  # 沪市
    return None

def check_stock_in_jqdata(jq_code, jq_client):
    """检查股票在JQData中是否存在"""
    try:
        # 方法1: 尝试获取基本信息
        if hasattr(jq_client, 'get_security_info'):
            info = jq_client.get_security_info(jq_code)
            if info:
                return True, info
        else:
            # 使用jqdatasdk
            import jqdatasdk as jq_sdk
            info = jq_sdk.get_security_info(jq_code)
            if info:
                return True, info
        
        # 方法2: 尝试获取价格数据
        if hasattr(jq_client, 'get_price_by_count'):
            price = jq_client.get_price_by_count(
                security=jq_code,
                count=1,
                end_date=cn_today_str(),
                frequency='daily',
                fields=['close']
            )
            if price is not None and not price.empty:
                return True, {"status": "has_price_data"}
        else:
            import jqdatasdk as jq_sdk
            price = jq_sdk.get_price(
                jq_code,
                count=1,
                end_date=cn_today_str(),
                frequency='daily',
                fields=['close']
            )
            if price is not None and not price.empty:
                return True, {"status": "has_price_data"}
        
        return False, None
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("🔍 检查无法转换的股票在JQData中的情况")
    print("=" * 80)
    
    # 初始化环境
    env = setup_research_environment(verbose=False)
    jq = env.get_jqdata_client()
    
    if not jq:
        print("❌ JQData客户端未初始化")
        return
    
    # 获取涨停板数据
    today_str = cn_today_str_compact()
    print(f"\n📅 当前日期: {cn_today_str()}")
    print(f"📊 正在获取涨停板数据...")
    
    try:
        limit_up_data = ak.stock_zt_pool_em(date=today_str)
        if limit_up_data is None or limit_up_data.empty:
            print("⚠️  今日暂无涨停股票")
            return
        
        # 转换为JQData格式
        limit_up_data['jq_code'] = limit_up_data['代码'].apply(convert_code_to_jq)
        
        # 找出无法转换的股票
        invalid_data = limit_up_data[limit_up_data['jq_code'].isna()].copy()
        
        if invalid_data.empty:
            print("✅ 所有股票代码都可以转换！")
            return
        
        print(f"\n📋 找到 {len(invalid_data)} 只无法转换的股票")
        print("=" * 80)
        
        # 尝试其他转换方式
        print("\n🔍 尝试其他转换方式...")
        results = []
        
        for idx, row in invalid_data.iterrows():
            code = str(row['代码'])
            name = row.get('名称', 'N/A')
            
            print(f"\n检查: {code} {name}")
            print(f"  代码长度: {len(code)}")
            print(f"  代码前缀: {code[:2] if len(code) >= 2 else 'N/A'}")
            
            # 尝试手动转换
            jq_code = None
            if len(code) == 6:
                if code.startswith('00') or code.startswith('30'):
                    jq_code = f"{code}.XSHE"
                elif code.startswith('60') or code.startswith('68'):
                    jq_code = f"{code}.XSHG"
                elif code.startswith('43') or code.startswith('83'):
                    # 新三板
                    jq_code = f"{code}.XSHE"
                elif code.startswith('8'):
                    # 北交所
                    jq_code = f"{code}.XSHG"
            
            if jq_code:
                print(f"  尝试JQData代码: {jq_code}")
                exists, info = check_stock_in_jqdata(jq_code, jq)
                if exists:
                    print(f"  ✅ 在JQData中找到！")
                    results.append({
                        'code': code,
                        'name': name,
                        'jq_code': jq_code,
                        'status': 'found',
                        'info': str(info)
                    })
                else:
                    print(f"  ❌ 在JQData中未找到: {info}")
                    results.append({
                        'code': code,
                        'name': name,
                        'jq_code': jq_code,
                        'status': 'not_found',
                        'error': str(info)
                    })
            else:
                print(f"  ⚠️  无法生成JQData代码（代码格式不支持）")
                results.append({
                    'code': code,
                    'name': name,
                    'jq_code': None,
                    'status': 'invalid_format',
                    'error': '代码格式不支持'
                })
        
        # 汇总结果
        print("\n" + "=" * 80)
        print("📊 检查结果汇总")
        print("=" * 80)
        
        found_count = sum(1 for r in results if r['status'] == 'found')
        not_found_count = sum(1 for r in results if r['status'] == 'not_found')
        invalid_format_count = sum(1 for r in results if r['status'] == 'invalid_format')
        
        print(f"\n✅ 在JQData中找到: {found_count} 只")
        print(f"❌ 在JQData中未找到: {not_found_count} 只")
        print(f"⚠️  代码格式不支持: {invalid_format_count} 只")
        
        if found_count > 0:
            print(f"\n✅ 可以在JQData中查询的股票:")
            for r in results:
                if r['status'] == 'found':
                    print(f"   {r['code']} {r['name']} -> {r['jq_code']}")
        
        if not_found_count > 0:
            print(f"\n❌ 在JQData中未找到的股票:")
            for r in results:
                if r['status'] == 'not_found':
                    print(f"   {r['code']} {r['name']} -> {r.get('jq_code', 'N/A')} (错误: {r.get('error', 'N/A')})")
        
        if invalid_format_count > 0:
            print(f"\n⚠️  代码格式不支持的股票:")
            for r in results:
                if r['status'] == 'invalid_format':
                    print(f"   {r['code']} {r['name']} (原因: {r.get('error', 'N/A')})")
        
        # 保存结果供后续使用
        print(f"\n💡 这些股票将用于网络搜索公司简介")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
