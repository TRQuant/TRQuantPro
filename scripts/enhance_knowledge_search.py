#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库搜索功能增强 - 针对量化研究和策略生成

优化项：
1. 精确匹配优先级（API函数名、因子名等）
2. 代码块提取和搜索
3. 标签优先匹配
4. 相关性评分增强
5. 分类型搜索（API/因子/策略/数据）
6. 上下文搜索（关联内容）

Author: TRQuant Team
Date: 2026-01-01
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from mcp_servers.unified_dev_server import knowledge_search, knowledge_get
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False


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
        if code and len(code) > 3:  # 过滤太短的
            code_blocks.append({
                'code': code,
                'type': 'inline_code',
                'length': len(code)
            })
    
    return code_blocks


def extract_api_functions(content: str) -> List[str]:
    """从内容中提取API函数名"""
    functions = []
    
    # Python函数调用模式
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
    
    # 因子名称模式（Alpha101/191因子、CNE因子等）
    patterns = [
        r'Alpha(\d+)',  # Alpha101, Alpha191
        r'alpha(\d+)',  # alpha101
        r'CNE[56]',  # CNE5, CNE6
        r'cne[56]',  # cne5, cne6
        r'[A-Z_][A-Z0-9_]{3,}',  # 大写因子名（如ROE, ROA, PE等）
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            factor = match.group(0)
            if factor and len(factor) > 2:
                factors.append(factor)
    
    return list(set(factors))


def enhanced_search(
    query: str,
    category: Optional[str] = None,
    limit: int = 10,
    exact_match_boost: float = 10.0,
    code_match_boost: float = 8.0,
    tag_match_boost: float = 5.0,
    title_match_boost: float = 3.0,
    content_match_boost: float = 1.0
) -> Dict:
    """
    增强的知识库搜索
    
    特点：
    1. 精确匹配优先级（API函数名、因子名）
    2. 代码块内容搜索
    3. 标签优先匹配
    4. 相关性评分增强
    """
    if not KB_AVAILABLE:
        return {"success": False, "error": "知识库工具不可用"}
    
    # 先进行基础搜索（获取更多结果）
    base_result = knowledge_search(query=query, limit=limit * 3)
    
    if not base_result.get('success'):
        return base_result
    
    all_items = base_result.get('results', [])
    query_lower = query.lower()
    query_words = query_lower.split()
    
    enhanced_results = []
    
    for item in all_items:
        score = 0.0
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
                score += code_match_boost * 2  # API函数匹配权重更高
                match_details['api_functions'].append(func)
        
        # 4. 因子名匹配
        factors = extract_factor_names(content)
        for factor in factors:
            if query_lower in factor.lower():
                score += code_match_boost * 1.5
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
        
        # 6. 标题匹配
        if query_lower in title_lower:
            score += title_match_boost
            match_details['title_match'] = True
        
        # 7. 内容匹配
        if query_lower in content_lower:
            # 内容匹配分数根据出现位置调整
            first_pos = content_lower.find(query_lower)
            if first_pos < 500:  # 出现在前500字符
                score += content_match_boost * 2
            else:
                score += content_match_boost
            match_details['content_match'] = True
        
        # 8. URL匹配（API文档URL）
        if 'api' in query_lower and 'api' in source.lower():
            score += 2.0
        
        # 只保留有匹配的结果
        if score > 0:
            enhanced_results.append({
                **item,
                '_score': score,
                '_match_details': match_details
            })
    
    # 按分数排序
    enhanced_results.sort(key=lambda x: x['_score'], reverse=True)
    
    # 限制返回数量
    final_results = enhanced_results[:limit]
    
    return {
        "success": True,
        "query": query,
        "category": category,
        "results": final_results,
        "total": len(enhanced_results),
        "enhanced": True  # 标记为增强搜索
    }


def search_by_category(
    query: str,
    category: str,
    limit: int = 10
) -> Dict:
    """按类别搜索（API/因子/策略/数据）"""
    
    category_filters = {
        'api': ['API函数文档', '交易函数', '数据获取'],
        'factor': ['因子构建', 'Alpha因子', '因子库', 'CNE5风格因子', 'CNE6风格因子'],
        'strategy': ['策略生成', '回测', '优化'],
        'data': ['数据获取', '行情数据', '财务数据', '宏观数据'],
    }
    
    result = enhanced_search(query=query, limit=limit * 2)
    
    if not result.get('success'):
        return result
    
    all_results = result.get('results', [])
    
    if category not in category_filters:
        return result
    
    # 过滤匹配的标签
    filter_tags = category_filters[category]
    filtered_results = []
    
    for item in all_results:
        tags = item.get('tags', [])
        if any(tag in tags for tag in filter_tags):
            filtered_results.append(item)
    
    return {
        "success": True,
        "query": query,
        "category": category,
        "results": filtered_results[:limit],
        "total": len(filtered_results),
        "enhanced": True
    }


def search_api_function(func_name: str, limit: int = 5) -> Dict:
    """搜索API函数（精确匹配）"""
    return enhanced_search(
        query=func_name,
        limit=limit,
        exact_match_boost=20.0,  # 更高的精确匹配权重
        code_match_boost=15.0,
    )


def search_factor(factor_name: str, limit: int = 5) -> Dict:
    """搜索因子（精确匹配）"""
    return enhanced_search(
        query=factor_name,
        limit=limit,
        exact_match_boost=20.0,
        code_match_boost=15.0,
    )


def test_enhanced_search():
    """测试增强搜索功能"""
    print("=" * 70)
    print("知识库增强搜索 - 测试")
    print("=" * 70)
    
    test_cases = [
        # API函数搜索
        ("get_price", "API函数搜索"),
        ("get_fundamentals", "API函数搜索"),
        ("Alpha101", "Alpha因子搜索"),
        ("CNE5", "风格因子搜索"),
        
        # 策略相关
        ("策略", "策略相关搜索"),
        ("回测", "回测相关搜索"),
        
        # 数据相关
        ("财务数据", "财务数据搜索"),
        ("行情", "行情数据搜索"),
    ]
    
    for query, description in test_cases:
        print(f"\n{'='*70}")
        print(f"🔍 {description}: {query}")
        print(f"{'='*70}")
        
        result = enhanced_search(query=query, limit=5)
        
        if result.get('success'):
            items = result.get('results', [])
            print(f"✅ 找到 {len(items)} 个结果")
            
            for i, item in enumerate(items[:3], 1):
                title = item.get('title', 'N/A')
                score = item.get('_score', 0)
                match_details = item.get('_match_details', {})
                
                print(f"\n  {i}. {title[:60]}")
                print(f"     相关性评分: {score:.1f}")
                if match_details.get('api_functions'):
                    print(f"     API函数: {', '.join(match_details['api_functions'][:3])}")
                if match_details.get('factors'):
                    print(f"     因子: {', '.join(match_details['factors'][:3])}")
                if match_details.get('code_match'):
                    print(f"     ✅ 代码匹配")
                if match_details.get('tag_match'):
                    print(f"     ✅ 标签匹配")
        else:
            print(f"❌ 搜索失败: {result.get('error')}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)


if __name__ == "__main__":
    if not KB_AVAILABLE:
        print("❌ 知识库工具不可用")
        sys.exit(1)
    
    test_enhanced_search()

