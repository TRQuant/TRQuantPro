# -*- coding: utf-8 -*-
"""
知识库搜索增强模块

提供增强的搜索功能，专门针对量化研究和策略生成优化
"""

import re
from typing import Dict, List, Optional
from collections import defaultdict


def extract_code_blocks(content: str) -> List[Dict[str, str]]:
    """从内容中提取代码块"""
    code_blocks = []
    
    # 匹配Markdown代码块
    pattern = r'```(?:python|py|javascript|js|java|cpp|c\+\+|go|rust)?\n(.*?)```'
    matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        code = match.group(1).strip()
        if code:
            code_blocks.append({
                'code': code,
                'type': 'code_block',
                'length': len(code)
            })
    
    # 匹配行内代码
    inline_pattern = r'`([^`]+)`'
    inline_matches = re.finditer(inline_pattern, content)
    
    for match in inline_matches:
        code = match.group(1).strip()
        if code and len(code) > 3:
            code_blocks.append({
                'code': code,
                'type': 'inline_code',
                'length': len(code)
            })
    
    return code_blocks


def extract_api_functions(content: str) -> List[str]:
    """从内容中提取API函数名"""
    functions = []
    
    patterns = [
        r'([a-zA-Z_][a-zA-Z0-9_]*)\(',  # function_name(
        r'\.([a-zA-Z_][a-zA-Z0-9_]*)\(',  # .method_name(
        r'from\s+(\w+)\s+import',  # from module import
        r'import\s+(\w+)',  # import module
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            func_name = match.group(1)
            if func_name and len(func_name) > 2:
                functions.append(func_name)
    
    return list(set(functions))


def extract_factor_names(content: str) -> List[str]:
    """从内容中提取因子名称"""
    factors = []
    
    patterns = [
        r'Alpha(\d+)',  # Alpha101, Alpha191
        r'alpha(\d+)',  # alpha101
        r'CNE[56]',  # CNE5, CNE6
        r'cne[56]',  # cne5, cne6
        r'\b[A-Z_][A-Z0-9_]{2,}\b',  # 大写因子名
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            factor = match.group(0)
            if factor and len(factor) > 2:
                factors.append(factor)
    
    return list(set(factors))


def enhance_search_results(
    items: List[Dict],
    query: str,
    exact_match_boost: float = 10.0,
    code_match_boost: float = 8.0,
    tag_match_boost: float = 5.0,
    title_match_boost: float = 3.0,
    content_match_boost: float = 1.0
) -> List[Dict]:
    """
    增强搜索结果评分
    
    Args:
        items: 搜索结果列表
        query: 查询字符串
        各种boost参数: 不同匹配类型的权重
    
    Returns:
        增强后的搜索结果列表（已排序）
    """
    query_lower = query.lower()
    query_words = query_lower.split()
    
    enhanced_items = []
    
    for item in items:
        score = item.get('_score', 0)  # 使用原始分数作为基础
        match_details = {
            'exact_match': False,
            'code_match': False,
            'tag_match': False,
            'title_match': False,
            'content_match': False,
            'api_functions': [],
            'factors': [],
        }
        
        title = item.get('title', '')
        content = item.get('content', '')
        tags = item.get('tags', [])
        source = item.get('source', '')
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        # 1. 精确匹配（最高优先级）
        if query_lower == title_lower:
            score += exact_match_boost * 10
            match_details['exact_match'] = True
        
        # 2. 代码块搜索
        code_blocks = extract_code_blocks(content)
        for code_block in code_blocks:
            code_lower = code_block['code'].lower()
            if query_lower in code_lower:
                score += code_match_boost
                match_details['code_match'] = True
                break
        
        # 3. API函数匹配
        api_functions = extract_api_functions(content)
        for func in api_functions:
            if query_lower == func.lower() or query_lower in func.lower():
                score += code_match_boost * 2
                if func not in match_details['api_functions']:
                    match_details['api_functions'].append(func)
        
        # 4. 因子名匹配
        factors = extract_factor_names(content)
        for factor in factors:
            if query_lower in factor.lower():
                score += code_match_boost * 1.5
                if factor not in match_details['factors']:
                    match_details['factors'].append(factor)
        
        # 5. 标签匹配
        for tag in tags:
            tag_lower = tag.lower()
            if query_lower in tag_lower:
                score += tag_match_boost
                match_details['tag_match'] = True
            # 部分匹配
            for word in query_words:
                if word in tag_lower:
                    score += tag_match_boost * 0.5
        
        # 6. 标题匹配（如果原始搜索没有计算）
        if query_lower in title_lower and not match_details['title_match']:
            score += title_match_boost
            match_details['title_match'] = True
        
        # 7. 内容匹配（如果原始搜索没有计算）
        if query_lower in content_lower and not match_details['content_match']:
            first_pos = content_lower.find(query_lower)
            if first_pos < 500:
                score += content_match_boost * 2
            else:
                score += content_match_boost
            match_details['content_match'] = True
        
        # 8. URL匹配（API文档）
        if 'api' in query_lower and 'api' in source.lower():
            score += 2.0
        
        # 只保留有匹配的结果
        if score > 0:
            enhanced_items.append({
                **item,
                '_score': score,
                '_match_details': match_details
            })
    
    # 按分数排序
    enhanced_items.sort(key=lambda x: x['_score'], reverse=True)
    
    return enhanced_items

