# -*- coding: utf-8 -*-
"""
策略代码转换器
==============
将聚宽/BulletTrade风格的策略代码转换为PTrade规范

核心功能：
1. 模块导入转换
2. API函数映射
3. 参数格式适配
4. 语法兼容性检查
"""

import re
from typing import Dict, List, Tuple
from pathlib import Path


class StrategyConverter:
    """策略代码转换器"""
    
    # 聚宽 -> PTrade API映射
    API_MAPPING = {
        # 数据获取
        'get_price': 'get_history',
        'get_current_data': 'get_snapshot',
        'get_extras': None,  # PTrade无此函数
        'get_security_info': 'get_instrument',
        'get_fundamentals': 'get_fundamentals_n',
        
        # 交易相关
        'order_target_value': 'order_target_value',  # 相同
        'order_target': 'order_target',  # 相同
        'order': 'order',  # 相同
        'order_value': 'order_value',  # 相同
        
        # 设置相关
        'set_benchmark': 'set_benchmark',  # 相同
        'set_slippage': 'set_slippage',  # 参数不同
        'set_order_cost': 'set_commission',  # 名称不同
        
        # 定时任务
        'run_daily': 'run_daily',  # 相同
        'run_weekly': 'run_weekly',  # 相同
        'run_monthly': 'run_monthly',  # 相同
        
        # 指数成分
        'get_index_stocks': 'get_index_stocks',  # 相同
        'get_all_securities': 'get_all_securities',  # 参数可能不同
    }
    
    # 需要删除的导入
    REMOVE_IMPORTS = [
        r'from jqdata import \*',
        r'from jqdata import .*',
        r'import jqdata',
        r'from kuanke.user_space_api import \*',
    ]
    
    # PTrade头部模板
    PTRADE_HEADER = '''# -*- coding: utf-8 -*-
"""
PTrade策略
由TRQuant自动转换生成
"""

'''
    
    def __init__(self):
        self.warnings = []
        self.errors = []
    
    def convert_to_ptrade(self, source_code: str) -> Tuple[str, List[str], List[str]]:
        """
        将策略代码转换为PTrade格式
        
        Args:
            source_code: 原始策略代码
            
        Returns:
            (转换后代码, 警告列表, 错误列表)
        """
        self.warnings = []
        self.errors = []
        
        code = source_code
        
        # 1. 移除聚宽导入
        code = self._remove_jqdata_imports(code)
        
        # 2. 转换set_slippage
        code = self._convert_slippage(code)
        
        # 3. 转换set_order_cost
        code = self._convert_commission(code)
        
        # 4. 转换get_price -> get_history
        code = self._convert_get_price(code)
        
        # 5. 转换get_current_data
        code = self._convert_current_data(code)
        
        # 6. 转换get_extras (ST股票)
        code = self._convert_get_extras(code)
        
        # 7. 检查不兼容的API
        self._check_incompatible_apis(code)
        
        # 8. 添加PTrade头部（如果没有）
        if 'PTrade' not in code[:200]:
            code = self.PTRADE_HEADER + code
        
        return code, self.warnings, self.errors
    
    def _remove_jqdata_imports(self, code: str) -> str:
        """移除聚宽导入语句"""
        for pattern in self.REMOVE_IMPORTS:
            code = re.sub(pattern + r'\n?', '', code)
        return code
    
    def _convert_slippage(self, code: str) -> str:
        """转换滑点设置"""
        # FixedSlippage(0.001) -> 0.001
        code = re.sub(
            r'set_slippage\(FixedSlippage\(([0-9.]+)\)\)',
            r'set_slippage(\1)',
            code
        )
        # PriceRelatedSlippage(0.002) -> 0.002
        code = re.sub(
            r'set_slippage\(PriceRelatedSlippage\(([0-9.]+)\)\)',
            r'set_slippage(\1)',
            code
        )
        return code
    
    def _convert_commission(self, code: str) -> str:
        """转换佣金设置"""
        # set_order_cost(OrderCost(...)) -> set_commission(PerTrade(...))
        
        # 复杂的OrderCost转换
        pattern = r'''set_order_cost\(OrderCost\(
            \s*open_tax\s*=\s*[0-9.]+,?
            \s*close_tax\s*=\s*([0-9.]+),?
            \s*open_commission\s*=\s*([0-9.]+),?
            \s*close_commission\s*=\s*([0-9.]+),?
            \s*min_commission\s*=\s*([0-9.]+)
            \s*\)[^)]*\)'''
        
        def replace_order_cost(match):
            stamp_tax = float(match.group(1))
            buy_commission = float(match.group(2))
            sell_commission = float(match.group(3))
            min_commission = match.group(4)
            # sell_cost = 佣金 + 印花税
            sell_cost = sell_commission + stamp_tax
            self.warnings.append(f'set_order_cost已转换为set_commission(PerTrade)')
            return f'set_commission(PerTrade(buy_cost={buy_commission}, sell_cost={sell_cost}, min_cost={min_commission}))'
        
        code = re.sub(pattern, replace_order_cost, code, flags=re.VERBOSE)
        
        # 如果已经是PerTrade格式，保持不变（PTrade和BulletTrade都支持）
        # 检查是否有错误的格式：set_commission(commission=...)
        code = re.sub(
            r'set_commission\(\s*commission\s*=\s*([0-9.]+),\s*min_commission\s*=\s*([0-9.]+)\s*\)',
            lambda m: f'set_commission(PerTrade(buy_cost={m.group(1)}, sell_cost={float(m.group(1)) + 0.001}, min_cost={m.group(2)}))',
            code
        )
        
        return code
    
    def _convert_get_price(self, code: str) -> str:
        """转换get_price为get_history"""
        # 这个转换比较复杂，需要改变参数结构
        # get_price(stocks, end_date=..., frequency='daily', fields=['close'], count=N, panel=False)
        # -> get_history(N, '1d', stocks, ['close'], skip_paused=False, fq='pre')
        
        pattern = r'''get_price\(
            \s*([^,]+),\s*  # stocks
            end_date\s*=\s*[^,]+,\s*  # end_date
            frequency\s*=\s*['"](daily|1d|minute|1m)['"]\s*,?\s*  # frequency
            fields\s*=\s*(\[[^\]]+\])\s*,?\s*  # fields
            count\s*=\s*([^,]+?)\s*,?\s*  # count
            (?:panel\s*=\s*\w+\s*)?  # panel (optional)
            \)'''
        
        def replace_get_price(match):
            stocks = match.group(1).strip()
            freq = '1d' if match.group(2) in ['daily', '1d'] else '1m'
            fields = match.group(3)
            count = match.group(4).strip()
            self.warnings.append('get_price已转换为get_history，请检查返回格式')
            return f"get_history({count}, '{freq}', {stocks}, {fields}, skip_paused=False, fq='pre')"
        
        code = re.sub(pattern, replace_get_price, code, flags=re.VERBOSE)
        
        # 如果还有未转换的get_price，添加警告
        if 'get_price(' in code:
            self.warnings.append('存在未转换的get_price调用，请手动检查')
        
        return code
    
    def _convert_current_data(self, code: str) -> str:
        """转换get_current_data为get_snapshot"""
        if 'get_current_data()' in code:
            self.warnings.append('get_current_data已保留，PTrade可能使用不同的属性名')
            # 在PTrade中，current_data的属性可能不同
            # day_open -> open, high_limit -> up_limit等
        
        # 转换属性访问
        code = code.replace('.day_open', '.open')
        code = code.replace('.high_limit', '.up_limit')
        code = code.replace('.low_limit', '.down_limit')
        
        return code
    
    def _convert_get_extras(self, code: str) -> str:
        """转换get_extras（ST股票检查）"""
        # PTrade没有get_extras，需要用其他方式检查ST
        pattern = r'''get_extras\(['"](is_st)['"]\s*,\s*[^,]+\s*,
            \s*start_date\s*=\s*[^,]+\s*,
            \s*end_date\s*=\s*[^,]+\s*,
            \s*df\s*=\s*True\)'''
        
        if re.search(pattern, code, flags=re.VERBOSE):
            self.warnings.append('get_extras(is_st)在PTrade中不可用，已注释，请使用股票名称包含ST判断')
            # 注释掉整个try-except块
            code = re.sub(
                r'try:\s*\n\s*st\s*=\s*get_extras.*?except.*?pass',
                '# ST过滤在PTrade中需要使用其他方式（如检查股票名称）\n        pass',
                code,
                flags=re.DOTALL
            )
        
        return code
    
    def _check_incompatible_apis(self, code: str) -> None:
        """检查不兼容的API"""
        incompatible = [
            ('get_extras', 'PTrade不支持get_extras，需要替代方案'),
            ('attribute_history', 'PTrade使用get_history替代'),
            ('get_ticks', 'PTrade tick数据获取方式不同'),
            ('get_bars', 'PTrade K线数据获取方式不同'),
        ]
        
        for api, msg in incompatible:
            if api + '(' in code:
                self.errors.append(f'{api}: {msg}')
    
    def convert_file(self, input_path: str, output_path: str = None) -> Dict:
        """
        转换策略文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（默认在同目录生成_ptrade.py）
            
        Returns:
            转换结果字典
        """
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.with_name(
                input_path.stem + '_ptrade' + input_path.suffix
            )
        else:
            output_path = Path(output_path)
        
        # 读取源文件
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # 转换
        converted_code, warnings, errors = self.convert_to_ptrade(source_code)
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_code)
        
        return {
            'success': len(errors) == 0,
            'input_file': str(input_path),
            'output_file': str(output_path),
            'warnings': warnings,
            'errors': errors,
            'lines_converted': len(converted_code.split('\n'))
        }


def convert_strategy_to_ptrade(input_path: str, output_path: str = None) -> Dict:
    """便捷函数：转换策略文件到PTrade格式"""
    converter = StrategyConverter()
    return converter.convert_file(input_path, output_path)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python strategy_converter.py <strategy_file>")
        sys.exit(1)
    
    result = convert_strategy_to_ptrade(sys.argv[1])
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
