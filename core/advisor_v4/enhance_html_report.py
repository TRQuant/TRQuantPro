#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强HTML报告 - 在交易记录中添加公司名称

功能：
1. 读取BulletTrade生成的HTML报告
2. 从交易记录中提取股票代码
3. 通过JQData API获取公司名称
4. 在交易记录表格中添加"公司名称"列
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict, List, Set
from bs4 import BeautifulSoup
import jqdatasdk

logger = logging.getLogger(__name__)


def get_stock_names(codes: List[str]) -> Dict[str, str]:
    """
    批量获取股票名称
    
    Args:
        codes: 股票代码列表
        
    Returns:
        股票代码到名称的映射字典
    """
    try:
        # 认证JQData
        from config.config_manager import get_config_manager
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config("jqdata")
        jqdatasdk.auth(jq_config.get("username"), jq_config.get("password"))
        
        # 获取股票信息
        securities = jqdatasdk.get_all_securities(['stock'], date=None)
        
        # 构建映射
        name_map = {}
        for code in codes:
            if code in securities.index:
                name_map[code] = securities.loc[code, 'display_name']
            else:
                name_map[code] = code  # 如果找不到，使用代码本身
        
        return name_map
    except Exception as e:
        logger.error(f"获取股票名称失败: {e}")
        return {code: code for code in codes}  # 失败时返回代码本身


def enhance_html_report(html_path: str, output_path: str = None) -> str:
    """
    增强HTML报告，在交易记录中添加公司名称
    
    Args:
        html_path: 原始HTML报告路径
        output_path: 输出路径（如果为None，覆盖原文件）
        
    Returns:
        增强后的HTML文件路径
    """
    html_path = Path(html_path)
    if not html_path.exists():
        raise FileNotFoundError(f"HTML文件不存在: {html_path}")
    
    # 读取HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 使用BeautifulSoup解析
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有表格
    tables = soup.find_all('table', class_='table')
    
    # 提取所有股票代码
    stock_codes: Set[str] = set()
    for table in tables:
        # 查找表头，看是否包含"标的"、"股票代码"或"security"列
        headers = table.find_all('th')
        code_col_idx = None
        for idx, header in enumerate(headers):
            header_text = header.get_text().strip().lower()
            if '标的' in header_text or '股票' in header_text or 'code' in header_text or 'security' in header_text:
                code_col_idx = idx
                break
        
        if code_col_idx is not None:
            # 提取所有股票代码
            rows = table.find_all('tr')[1:]  # 跳过表头
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) > code_col_idx:
                    code = cells[code_col_idx].get_text().strip()
                    # 清理代码格式（移除空格、换行等）
                    code = re.sub(r'\s+', '', code)
                    if code and '.' in code:  # 确保是有效的股票代码格式
                        stock_codes.add(code)
    
    # 获取股票名称
    logger.info(f"找到 {len(stock_codes)} 个不同的股票代码")
    if stock_codes:
        name_map = get_stock_names(list(stock_codes))
        logger.info(f"成功获取 {len(name_map)} 个股票名称")
    else:
        name_map = {}
    
    # 在交易记录表格中添加公司名称列
    for table in tables:
        headers = table.find_all('th')
        code_col_idx = None
        for idx, header in enumerate(headers):
            header_text = header.get_text().strip().lower()
            if '标的' in header_text or '股票' in header_text or 'code' in header_text or 'security' in header_text:
                code_col_idx = idx
                break
        
        if code_col_idx is not None:
            # 检查是否已有"公司名称"列
            has_name_col = any('公司名称' in h.get_text() or '名称' in h.get_text() for h in headers)
            
            if not has_name_col:
                # 在股票代码列后插入"公司名称"列
                # 1. 在表头添加
                code_header = headers[code_col_idx]
                name_header = soup.new_tag('th')
                name_header.string = '公司名称'
                code_header.insert_after(name_header)
                
                # 2. 在数据行添加
                rows = table.find_all('tr')[1:]  # 跳过表头
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) > code_col_idx:
                        code_cell = cells[code_col_idx]
                        code = re.sub(r'\s+', '', code_cell.get_text().strip())
                        
                        # 创建公司名称单元格
                        name_cell = soup.new_tag('td')
                        name_cell.string = name_map.get(code, code)  # 如果找不到名称，使用代码
                        code_cell.insert_after(name_cell)
    
    # 保存增强后的HTML
    output_path = Path(output_path) if output_path else html_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    logger.info(f"增强后的HTML报告已保存: {output_path}")
    return str(output_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python enhance_html_report.py <html_path> [output_path]")
        sys.exit(1)
    
    html_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    enhance_html_report(html_path, output_path)
