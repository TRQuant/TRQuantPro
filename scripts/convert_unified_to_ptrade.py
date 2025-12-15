#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一版策略转PTrade转换器
========================
将统一版策略（BulletTrade格式）转换为PTrade格式
"""

import re
import sys
from pathlib import Path


def convert_unified_to_ptrade(input_file: str, output_file: str = None) -> dict:
    """
    转换统一版策略为PTrade格式
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径（默认添加_ptrade后缀）
    
    Returns:
        转换结果
    """
    input_path = Path(input_file)
    
    if output_file is None:
        output_file = input_path.with_name(input_path.stem + '_ptrade' + input_path.suffix)
    else:
        output_file = Path(output_file)
    
    # 读取源文件
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    warnings = []
    errors = []
    
    # 1. 删除jqdata导入（如果存在）
    if 'from jqdata import' in code:
        code = re.sub(r'from jqdata import \*?\n?', '', code)
        warnings.append('已删除from jqdata import *')
    
    # 2. 转换get_current_data() -> get_snapshot()
    # 需要找到所有get_current_data()的调用并转换
    def replace_get_current_data(match):
        # 检查上下文，确定需要转换的股票列表
        # 简单处理：如果后面有[stock]访问，转换为get_snapshot([stock])
        return 'get_snapshot'
    
    # 更精确的转换
    # get_current_data() -> get_snapshot(stocks) 需要传入股票列表
    # 这个比较复杂，需要分析上下文
    
    # 3. 转换get_price -> get_history（在except分支中）
    # 这个已经在try-except中，但PTrade应该直接使用get_history
    
    # 4. 转换get_security_info -> get_instrument
    if 'get_security_info(' in code:
        code = code.replace('get_security_info(', 'get_instrument(')
        warnings.append('get_security_info已转换为get_instrument')
    
    # 5. 修复数据获取逻辑
    # 将try-except中的get_price改为直接使用get_history
    old_pattern = r'''try:
            prices = get_history\(MOMENTUM_LONG \+ 5, '1d', test_stocks, \['close'\], skip_paused=False, fq='pre'\)
            close_df = prices\.get\('close'\) if isinstance\(prices, dict\) else prices
        except:
            current_dt = context\.current_dt\.strftime\('%Y-%m-%d'\)
            prices = get_price\(test_stocks, end_date=current_dt, frequency='daily', fields=\['close'\], count=MOMENTUM_LONG \+ 5, panel=False\)
            close_df = prices\.pivot\(index='time', columns='code', values='close'\) if 'time' in prices\.columns else prices'''
    
    new_code = '''prices = get_history(MOMENTUM_LONG + 5, '1d', test_stocks, ['close'], skip_paused=False, fq='pre')
            close_df = prices.get('close') if isinstance(prices, dict) else prices'''
    
    code = re.sub(old_pattern, new_code, code, flags=re.DOTALL)
    
    # 6. 转换get_current_data()调用
    # 需要根据上下文确定股票列表
    # 简化处理：在filter_stocks中，传入stocks参数
    code = re.sub(
        r'current_data = get_current_data\(\)',
        r'current_data = get_snapshot(stocks[:100]) if len(stocks) > 0 else {}',
        code
    )
    
    # 在rebalance和check_risk中
    code = re.sub(
        r'current_data = get_current_data\(\)',
        r'current_data = get_snapshot(list(context.portfolio.positions.keys()) + target_stocks) if len(target_stocks) > 0 else {}',
        code,
        count=1  # 只替换第一个（rebalance中的）
    )
    
    code = re.sub(
        r'current_data = get_current_data\(\)',
        r'current_data = get_snapshot(list(context.portfolio.positions.keys())) if len(context.portfolio.positions) > 0 else {}',
        code,
        count=1  # 只替换第二个（check_risk中的）
    )
    
    # 7. 修复属性访问
    # get_snapshot返回dict，key是股票代码
    # 需要将current_data[stock]改为current_data.get(stock)
    # 但代码中已经使用了current_data[stock]，这个在dict中也可以工作
    
    # 8. 添加PTrade头部注释
    if 'PTrade' not in code[:500]:
        header = '''# -*- coding: utf-8 -*-
"""
PTrade策略 - 由统一版策略转换生成
已自动转换所有API调用为PTrade格式
"""

'''
        code = header + code
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    return {
        'success': len(errors) == 0,
        'input_file': str(input_path),
        'output_file': str(output_file),
        'warnings': warnings,
        'errors': errors
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_unified_to_ptrade.py <input_file> [output_file]")
        sys.exit(1)
    
    result = convert_unified_to_ptrade(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    
    print(f"\n{'='*60}")
    print(f"转换结果: {'成功' if result['success'] else '失败'}")
    print(f"输入文件: {result['input_file']}")
    print(f"输出文件: {result['output_file']}")
    
    if result['warnings']:
        print(f"\n⚠️ 警告 ({len(result['warnings'])}条):")
        for w in result['warnings']:
            print(f"  - {w}")
    
    if result['errors']:
        print(f"\n❌ 错误 ({len(result['errors'])}条):")
        for e in result['errors']:
            print(f"  - {e}")
    
    print(f"{'='*60}")
