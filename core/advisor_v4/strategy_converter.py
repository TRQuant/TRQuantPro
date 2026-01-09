#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略转换器基类 - 将BulletTrade/聚宽策略转换为其他平台代码

支持的目标平台:
- Ptrade (恒生电子)
- QMT (迅投科技)

转换内容:
1. 股票代码格式 (.XSHG/.XSHE → .SH/.SZ)
2. 数据获取API
3. 订单API
4. 持仓/账户查询API
5. 定时任务/回调机制
"""

from __future__ import annotations

import ast
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """转换结果"""
    success: bool
    target_code: str
    source_platform: str
    target_platform: str
    warnings: List[str]
    errors: List[str]
    converted_items: Dict[str, int]  # 转换统计


class StrategyConverter(ABC):
    """策略转换器基类"""
    
    # 股票代码映射规则
    CODE_MAPPING = {
        '.XSHG': '.SH',
        '.XSHE': '.SZ',
    }
    
    # 需要转换的函数名映射 (子类覆盖)
    FUNCTION_MAPPING: Dict[str, str] = {}
    
    # 需要转换的属性映射 (子类覆盖)
    ATTRIBUTE_MAPPING: Dict[str, str] = {}
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.converted_items: Dict[str, int] = {
            'stock_codes': 0,
            'function_calls': 0,
            'attributes': 0,
            'imports': 0,
        }
    
    @property
    @abstractmethod
    def target_platform(self) -> str:
        """目标平台名称"""
        pass
    
    @property
    @abstractmethod
    def source_platform(self) -> str:
        """源平台名称"""
        pass
    
    def convert(self, source_code: str) -> ConversionResult:
        """
        转换策略代码
        
        Args:
            source_code: 源代码字符串
            
        Returns:
            转换结果
        """
        self.warnings = []
        self.errors = []
        self.converted_items = {k: 0 for k in self.converted_items}
        
        try:
            # 1. 转换股票代码格式
            code = self._convert_stock_codes(source_code)
            
            # 2. 转换导入语句
            code = self._convert_imports(code)
            
            # 3. 转换函数调用
            code = self._convert_function_calls(code)
            
            # 4. 转换属性访问
            code = self._convert_attributes(code)
            
            # 5. 添加平台特定代码
            code = self._add_platform_specific_code(code)
            
            # 6. 后处理
            code = self._post_process(code)
            
            success = len(self.errors) == 0
            
        except Exception as e:
            logger.error(f"策略转换失败: {e}")
            self.errors.append(str(e))
            code = source_code
            success = False
        
        return ConversionResult(
            success=success,
            target_code=code,
            source_platform=self.source_platform,
            target_platform=self.target_platform,
            warnings=self.warnings,
            errors=self.errors,
            converted_items=self.converted_items,
        )
    
    def _convert_stock_codes(self, code: str) -> str:
        """转换股票代码格式"""
        result = code
        for old_suffix, new_suffix in self.CODE_MAPPING.items():
            # 匹配股票代码模式: 6位数字.后缀
            pattern = r"(['\"]?\d{6})" + re.escape(old_suffix) + r"(['\"]?)"
            matches = re.findall(pattern, result)
            if matches:
                self.converted_items['stock_codes'] += len(matches)
            result = re.sub(pattern, r"\1" + new_suffix + r"\2", result)
        return result
    
    def _convert_imports(self, code: str) -> str:
        """转换导入语句（子类实现）"""
        return code
    
    def _convert_function_calls(self, code: str) -> str:
        """转换函数调用"""
        result = code
        for old_func, new_func in self.FUNCTION_MAPPING.items():
            # 简单的函数名替换
            pattern = r'\b' + re.escape(old_func) + r'\s*\('
            if re.search(pattern, result):
                self.converted_items['function_calls'] += len(re.findall(pattern, result))
                result = re.sub(pattern, new_func + '(', result)
                if self.verbose:
                    logger.info(f"转换函数: {old_func} → {new_func}")
        return result
    
    def _convert_attributes(self, code: str) -> str:
        """转换属性访问"""
        result = code
        for old_attr, new_attr in self.ATTRIBUTE_MAPPING.items():
            pattern = r'\.' + re.escape(old_attr) + r'(?=\s*[,)\]\n])'
            if re.search(pattern, result):
                self.converted_items['attributes'] += len(re.findall(pattern, result))
                result = re.sub(pattern, '.' + new_attr, result)
        return result
    
    @abstractmethod
    def _add_platform_specific_code(self, code: str) -> str:
        """添加平台特定代码（子类实现）"""
        pass
    
    def _post_process(self, code: str) -> str:
        """后处理（可选，子类覆盖）"""
        return code
    
    def _add_warning(self, message: str):
        """添加警告"""
        self.warnings.append(message)
        if self.verbose:
            logger.warning(message)
    
    def _add_error(self, message: str):
        """添加错误"""
        self.errors.append(message)
        logger.error(message)


class CodeAnalyzer:
    """代码分析器 - 分析源代码中使用的API"""
    
    def __init__(self, code: str):
        self.code = code
        self.tree = None
        try:
            self.tree = ast.parse(code)
        except SyntaxError as e:
            logger.error(f"代码解析失败: {e}")
    
    def get_function_calls(self) -> List[str]:
        """获取所有函数调用"""
        if not self.tree:
            return []
        
        calls = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        return list(set(calls))
    
    def get_imports(self) -> List[Tuple[str, Optional[str]]]:
        """获取所有导入"""
        if not self.tree:
            return []
        
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, alias.asname))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append((f"{module}.{alias.name}", alias.asname))
        return imports
    
    def get_stock_codes(self) -> List[str]:
        """提取所有股票代码"""
        pattern = r'\d{6}\.(XSHG|XSHE|SH|SZ)'
        return list(set(re.findall(pattern, self.code)))
    
    def uses_jqdata_api(self) -> bool:
        """检查是否使用聚宽API"""
        jq_apis = ['get_price', 'get_fundamentals', 'order', 'order_value', 
                   'get_index_stocks', 'run_daily', 'run_weekly']
        calls = self.get_function_calls()
        return any(api in calls for api in jq_apis)


def convert_stock_code(code: str, direction: str = 'jq_to_local') -> str:
    """
    转换单个股票代码
    
    Args:
        code: 股票代码
        direction: 转换方向
            - 'jq_to_local': 聚宽格式 → 本地格式 (.XSHG → .SH)
            - 'local_to_jq': 本地格式 → 聚宽格式 (.SH → .XSHG)
    
    Returns:
        转换后的股票代码
    """
    if direction == 'jq_to_local':
        return code.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
    elif direction == 'local_to_jq':
        return code.replace('.SH', '.XSHG').replace('.SZ', '.XSHE')
    else:
        raise ValueError(f"无效的转换方向: {direction}")


def batch_convert_stock_codes(codes: List[str], direction: str = 'jq_to_local') -> List[str]:
    """批量转换股票代码"""
    return [convert_stock_code(c, direction) for c in codes]
