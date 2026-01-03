#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新save_to_knowledge_base函数为结构化版本
这是一个临时脚本，用于更新知识库保存逻辑
"""

# 读取原始文件
with open('scripts/crawl_jqdata_all_subpages_to_kb.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换save_to_knowledge_base函数
old_function = '''def save_to_knowledge_base(page_data: Dict) -> bool:
    """将页面数据存入知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        # 生成标题和内容
        title = page_data['title']
        content = f"""URL: {page_data['url']}
爬取时间: {page_data['crawled_at']}
内容长度: {page_data['content_length']} 字符

{page_data['content']}
"""
        
        # 提取标签
        tags = ['JQData', 'API文档', '聚宽', '官方文档']
        url = page_data['url']
        if 'doc' in url:
            tags.append('API函数文档')
        if 'help' in url:
            tags.append('帮助文档')
        
        # 存入知识库
        result = knowledge_add(
            title=title,
            content=content,
            type='reference',
            tags=tags,
            source=url
        )
        
        if result.get('success'):
            STATS["saved_to_kb"] += 1
            return True
        else:
            print(f"    ⚠️ 存入知识库失败: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False'''

new_function = '''def save_to_knowledge_base(page_data: Dict) -> bool:
    """将页面数据存入知识库（结构化、有条理）"""
    if not KB_AVAILABLE:
        return False
    
    try:
        title = page_data['title']
        url = page_data['url']
        
        # 构建结构化内容（Markdown格式）
        content = f"""# {title}

## 基本信息
- **URL**: {url}
- **爬取时间**: {page_data['crawled_at']}
- **内容长度**: {page_data['content_length']} 字符

## 内容

{page_data['content']}
"""
        
        # 根据URL和标题确定分类标签（有序、有条理）
        tags = ['JQData', '聚宽数据', '官方文档']
        
        # 根据URL路径确定分类
        if 'doc?name=JQDatadoc' in url:
            tags.append('JQDatadoc文档')
            if 'id=' in url:
                tags.append('API函数文档')
        elif 'logon' in url:
            tags.append('登录认证文档')
        elif 'help' in url:
            tags.append('帮助文档')
        
        # 根据标题关键词确定具体分类
        title_lower = title.lower()
        if 'alpha' in title_lower:
            tags.append('Alpha因子')
            if '101' in title_lower:
                tags.append('Alpha101')
            elif '191' in title_lower:
                tags.append('Alpha191')
        elif '因子' in title or 'factor' in title_lower:
            tags.append('因子库')
        elif '风险' in title or 'risk' in title_lower or 'cne' in title_lower:
            tags.append('风险模型')
            if 'cne5' in title_lower:
                tags.append('CNE5风格因子')
            elif 'cne6' in title_lower:
                tags.append('CNE6风格因子')
        elif '技术' in title or 'technical' in title_lower:
            tags.append('技术指标')
        elif '股票' in title or 'stock' in title_lower:
            tags.append('股票数据')
        elif '指数' in title or 'index' in title_lower:
            tags.append('指数数据')
        elif '期货' in title or 'futures' in title_lower:
            tags.append('期货数据')
        elif '基金' in title or 'fund' in title_lower:
            tags.append('基金数据')
        elif '宏观' in title or 'macro' in title_lower:
            tags.append('宏观经济数据')
        elif '试用' in title or '购买' in title or 'purchase' in title_lower:
            tags.append('购买说明')
        
        # 确保标签唯一且有序
        tags = list(dict.fromkeys(tags))  # 保持顺序的去重
        
        # 存入知识库
        result = knowledge_add(
            title=title,
            content=content,
            type='reference',
            tags=tags,
            source=url
        )
        
        if result.get('success') or result.get('id') or result.get('knowledge_id'):
            STATS["saved_to_kb"] += 1
            return True
        else:
            error_msg = result.get('error', 'Unknown')
            print(f"    ⚠️ 存入知识库失败: {error_msg}")
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False'''

# 执行替换
if old_function in content:
    content = content.replace(old_function, new_function)
    with open('scripts/crawl_jqdata_all_subpages_to_kb.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 知识库函数已更新")
else:
    print("⚠️ 未找到目标函数，可能已经被更新")

