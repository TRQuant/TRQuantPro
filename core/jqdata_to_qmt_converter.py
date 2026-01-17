"""
JQData → QMT(xtquant) 策略代码转换器
====================================
将聚宽JQData API代码转换为QMT平台的xtquant API代码

QMT(迅投) API 文档参考:
- xtquant官方文档: https://dict.thinktrader.net/nativeApi/xtquant.html

主要转换规则:
1. 导入语句: jqdata → xtquant
2. 数据获取: get_price → xtdata.get_market_data
3. 交易执行: order → xttrader.order_xxx
4. 股票代码: 000001.XSHE → 000001.SZ
"""

import re
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime


class JQDataToQMTConverter:
    """JQData → QMT 代码转换器"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.changes = []
        
        # 股票代码后缀映射
        self.code_suffix_mapping = {
            '.XSHE': '.SZ',   # 深圳
            '.XSHG': '.SH',   # 上海
        }
        
        # API映射表
        self.api_mappings = self._build_api_mappings()
    
    def _build_api_mappings(self) -> Dict:
        """构建API映射表"""
        return {
            # ========== 导入语句 ==========
            'imports': [
                {
                    'pattern': r'from jqdata import \*',
                    'replacement': 'from xtquant import xtdata\nfrom xtquant.xttrader import XtQuantTrader\nfrom xtquant.xttype import StockAccount',
                    'note': 'JQData导入转换为xtquant'
                },
                {
                    'pattern': r'import jqdata',
                    'replacement': 'from xtquant import xtdata',
                    'note': 'JQData导入转换为xtquant'
                },
                {
                    'pattern': r'from kuanke\.user_space_api import \*',
                    'replacement': '# QMT不需要导入kuanke',
                    'note': '删除kuanke导入'
                }
            ],
            
            # ========== 数据获取 ==========
            'data_funcs': [
                {
                    'pattern': r'get_price\s*\(',
                    'replacement': 'xtdata.get_market_data(',
                    'note': 'get_price → xtdata.get_market_data'
                },
                {
                    'pattern': r'get_current_data\s*\(\)',
                    'replacement': 'xtdata.get_full_tick(stock_list)',
                    'note': 'get_current_data → xtdata.get_full_tick'
                },
                {
                    'pattern': r'get_bars\s*\(',
                    'replacement': 'xtdata.get_market_data(',
                    'note': 'get_bars → xtdata.get_market_data'
                },
                {
                    'pattern': r'history\s*\(',
                    'replacement': 'xtdata.get_market_data(',
                    'note': 'history → xtdata.get_market_data'
                },
                {
                    'pattern': r'attribute_history\s*\(',
                    'replacement': 'xtdata.get_market_data(',
                    'note': 'attribute_history → xtdata.get_market_data'
                }
            ],
            
            # ========== 交易执行 ==========
            'trade_funcs': [
                {
                    'pattern': r'order_target_value\s*\(([^,]+),\s*([^)]+)\)',
                    'replacement': r'xt_trader.order_stock(\1, xtconstant.STOCK_BUY, -1, xtconstant.FIX_PRICE, -1, "按金额", \2)',
                    'note': 'order_target_value需要手动计算数量'
                },
                {
                    'pattern': r'order_target\s*\(([^,]+),\s*([^)]+)\)',
                    'replacement': r'xt_trader.order_stock(\1, xtconstant.STOCK_BUY, int(\2), xtconstant.FIX_PRICE, -1)',
                    'note': 'order_target → xt_trader.order_stock'
                },
                {
                    'pattern': r'order\s*\(([^,]+),\s*([^)]+)\)',
                    'replacement': r'xt_trader.order_stock(\1, xtconstant.STOCK_BUY, int(\2), xtconstant.FIX_PRICE, -1)',
                    'note': 'order → xt_trader.order_stock'
                },
                {
                    'pattern': r'order_value\s*\(([^,]+),\s*([^)]+)\)',
                    'replacement': r'xt_trader.order_stock(\1, xtconstant.STOCK_BUY, -1, xtconstant.FIX_PRICE, -1, "按金额", \2)',
                    'note': 'order_value需要计算数量'
                }
            ],
            
            # ========== 持仓查询 ==========
            'position_funcs': [
                {
                    'pattern': r'context\.portfolio\.positions',
                    'replacement': 'xt_trader.query_stock_positions(account)',
                    'note': 'portfolio.positions → query_stock_positions'
                },
                {
                    'pattern': r'context\.portfolio\.total_value',
                    'replacement': 'xt_trader.query_stock_asset(account).total_asset',
                    'note': 'total_value → query_stock_asset().total_asset'
                },
                {
                    'pattern': r'context\.portfolio\.available_cash',
                    'replacement': 'xt_trader.query_stock_asset(account).cash',
                    'note': 'available_cash → query_stock_asset().cash'
                }
            ],
            
            # ========== 日志 ==========
            'log_funcs': [
                {
                    'pattern': r'log\.info\s*\(',
                    'replacement': 'print(',
                    'note': 'log.info → print'
                },
                {
                    'pattern': r'log\.warn\s*\(',
                    'replacement': 'print("WARN:",',
                    'note': 'log.warn → print'
                },
                {
                    'pattern': r'log\.error\s*\(',
                    'replacement': 'print("ERROR:",',
                    'note': 'log.error → print'
                }
            ],
            
            # ========== 时间函数 ==========
            'time_funcs': [
                {
                    'pattern': r'context\.current_dt',
                    'replacement': 'datetime.now()',
                    'note': 'current_dt → datetime.now()'
                },
                {
                    'pattern': r'context\.previous_date',
                    'replacement': '(datetime.now() - timedelta(days=1)).strftime("%Y%m%d")',
                    'note': 'previous_date需要自行计算'
                }
            ]
        }
    
    def convert_stock_code(self, code: str) -> str:
        """
        转换股票代码格式
        JQData: 000001.XSHE → QMT: 000001.SZ
        """
        for jq_suffix, qmt_suffix in self.code_suffix_mapping.items():
            if code.endswith(jq_suffix):
                return code.replace(jq_suffix, qmt_suffix)
        return code
    
    def _convert_stock_codes_in_text(self, text: str) -> str:
        """转换文本中的所有股票代码"""
        # 匹配聚宽格式的股票代码
        pattern = r"(['\"]?)(\d{6})\.(XSHE|XSHG)\1"
        
        def replace_code(match):
            quote = match.group(1)
            code_num = match.group(2)
            suffix = match.group(3)
            new_suffix = 'SZ' if suffix == 'XSHE' else 'SH'
            return f"{quote}{code_num}.{new_suffix}{quote}"
        
        return re.sub(pattern, replace_code, text)
    
    def convert(self, source_code: str, convert_codes: bool = True) -> Tuple[str, List[str], List[str]]:
        """
        转换JQData代码为QMT代码
        
        Args:
            source_code: 源代码
            convert_codes: 是否转换股票代码格式
        
        Returns:
            Tuple[str, List[str], List[str]]: (转换后代码, 警告列表, 变更列表)
        """
        self.warnings = []
        self.errors = []
        self.changes = []
        
        result = source_code
        
        # 1. 转换导入语句
        for mapping in self.api_mappings['imports']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"导入转换: {mapping['note']}")
        
        # 2. 转换数据函数
        for mapping in self.api_mappings['data_funcs']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"数据函数: {mapping['note']}")
        
        # 3. 转换交易函数
        for mapping in self.api_mappings['trade_funcs']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"交易函数: {mapping['note']}")
                self.warnings.append(f"⚠️ {mapping['note']} - 请检查参数是否正确")
        
        # 4. 转换持仓查询
        for mapping in self.api_mappings['position_funcs']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"持仓查询: {mapping['note']}")
        
        # 5. 转换日志函数
        for mapping in self.api_mappings['log_funcs']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"日志: {mapping['note']}")
        
        # 6. 转换时间函数
        for mapping in self.api_mappings['time_funcs']:
            if re.search(mapping['pattern'], result):
                result = re.sub(mapping['pattern'], mapping['replacement'], result)
                self.changes.append(f"时间: {mapping['note']}")
        
        # 7. 转换股票代码格式
        if convert_codes:
            result = self._convert_stock_codes_in_text(result)
            self.changes.append("股票代码: .XSHE/.XSHG → .SZ/.SH")
        
        # 添加必要的导入
        if 'datetime.now()' in result and 'from datetime import' not in result:
            result = 'from datetime import datetime, timedelta\n' + result
            self.changes.append("添加: datetime导入")
        
        # 添加QMT初始化代码提示
        self.warnings.append("⚠️ QMT需要初始化XtQuantTrader和账户连接，请参考QMT文档")
        
        return result, self.warnings, self.changes
    
    def convert_file(self, input_path: str, output_path: str = None) -> Dict:
        """
        转换策略文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（默认添加_qmt后缀）
        
        Returns:
            Dict: 转换结果信息
        """
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.with_name(input_path.stem + '_qmt' + input_path.suffix)
        else:
            output_path = Path(output_path)
        
        # 读取源代码
        source_code = input_path.read_text(encoding='utf-8')
        
        # 转换
        converted_code, warnings, changes = self.convert(source_code)
        
        # 添加转换头注释
        header = f'''"""
QMT策略代码 (由JQData转换)
========================
转换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
源文件: {input_path.name}

注意事项:
1. 需要初始化XtQuantTrader和账户连接
2. 部分API需要手动调整参数
3. 请测试验证转换后的逻辑

转换变更:
{chr(10).join('- ' + c for c in changes)}

警告:
{chr(10).join('- ' + w for w in warnings)}
"""

'''
        
        final_code = header + converted_code
        
        # 写入输出文件
        output_path.write_text(final_code, encoding='utf-8')
        
        return {
            'success': True,
            'input': str(input_path),
            'output': str(output_path),
            'changes': changes,
            'warnings': warnings,
            'changes_count': len(changes)
        }


# 便捷函数
def convert_jqdata_to_qmt(input_path: str, output_path: str = None) -> Dict:
    """
    将JQData策略代码转换为QMT格式
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
    
    Returns:
        Dict: 转换结果
    """
    converter = JQDataToQMTConverter()
    return converter.convert_file(input_path, output_path)


def convert_jqdata_code_to_qmt(source_code: str, convert_codes: bool = True) -> Tuple[str, List[str], List[str]]:
    """
    将JQData代码字符串转换为QMT格式
    
    Args:
        source_code: 源代码字符串
        convert_codes: 是否转换股票代码
    
    Returns:
        Tuple: (转换后代码, 警告, 变更)
    """
    converter = JQDataToQMTConverter()
    return converter.convert(source_code, convert_codes)


if __name__ == '__main__':
    # 测试代码
    test_code = '''
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    g.stock = '000001.XSHE'

def handle_data(context, data):
    current_data = get_current_data()
    price = get_price(g.stock, count=20, fields=['close'])
    
    if context.portfolio.available_cash > 10000:
        order_target_value(g.stock, 10000)
    
    log.info(f"当前时间: {context.current_dt}")
'''
    
    converter = JQDataToQMTConverter()
    converted, warnings, changes = converter.convert(test_code)
    
    print("=== 转换结果 ===")
    print(converted)
    print("\n=== 变更 ===")
    for c in changes:
        print(f"  - {c}")
    print("\n=== 警告 ===")
    for w in warnings:
        print(f"  - {w}")

