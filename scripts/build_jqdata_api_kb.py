#!/usr/bin/env python3
"""
构建聚宽API知识库

从已抓取的文档中提取：
1. API函数定义
2. 参数说明
3. 返回值说明
4. 示例代码
5. 分类标签

Author: TRQuant Team
Date: 2025-12-19
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 导入MCP知识库工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    # 使用正确的函数名
    mcp_xuanyuan_knowledge_add = knowledge_add
except Exception as e:
    print(f"⚠️ 导入knowledge_add失败: {e}")
    # 如果无法导入，使用占位符
    def mcp_xuanyuan_knowledge_add(*args, **kwargs):
        print(f"知识库添加: {kwargs.get('title', 'Unknown')}")
        return {"success": True}

# 文档目录
DOCS_DIR = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled/texts_enhanced"
JSON_FILE = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled/all_pages_enhanced.json"

# API分类
API_CATEGORIES = {
    "数据获取": ["get_price", "get_fundamentals", "history", "attribute_history", "get_index_stocks", 
                "get_industry_stocks", "get_concept_stocks", "get_all_securities", "get_trade_days"],
    "财务数据": ["get_fundamentals", "get_fundamentals_continuously", "get_valuation", 
                "get_history_fundamentals", "finance.run_query"],
    "交易执行": ["order", "order_target", "order_value", "order_target_value", "cancel_order"],
    "策略设置": ["initialize", "handle_data", "before_trading_start", "after_trading_end", 
                "run_daily", "set_benchmark", "set_option"],
    "因子分析": ["get_factor_values", "get_factor_kanban_values", "alpha_001", "alpha_101"],
    "技术指标": ["GDX", "MA", "MACD", "RSI", "technical_analysis"],
    "融资融券": ["margincash_open", "margincash_close", "marginsec_open", "marginsec_close", 
                "get_mtss", "get_margincash_stocks"],
    "期货": ["get_dominant_future", "get_future_contracts", "futures_margin_rate", "order"],
    "Tick级": ["handle_tick", "subscribe", "unsubscribe", "get_call_auction"],
    "其他": []
}

def extract_function_definitions(text: str) -> List[Dict[str, Any]]:
    """提取函数定义"""
    functions = []
    
    # 匹配函数定义模式
    # 例如: get_price(security, start_date=None, end_date=None, ...)
    pattern = r'([a-z_][a-z0-9_]*)\s*\([^)]*\)'
    
    # 更精确的模式：函数名(参数列表)
    pattern2 = r'([a-z_][a-z0-9_\.]*)\s*\([^)]*\)'
    
    matches = re.finditer(pattern2, text, re.IGNORECASE)
    
    seen = set()
    for match in matches:
        func_name = match.group(1)
        if func_name not in seen and len(func_name) > 2:
            seen.add(func_name)
            # 尝试提取参数
            full_match = match.group(0)
            params_match = re.search(r'\(([^)]*)\)', full_match)
            params = []
            if params_match:
                params_str = params_match.group(1)
                # 简单解析参数
                for p in params_str.split(','):
                    p = p.strip()
                    if p:
                        param_name = p.split('=')[0].strip()
                        params.append(param_name)
            
            functions.append({
                "name": func_name,
                "signature": full_match,
                "params": params
            })
    
    return functions

def extract_code_examples(text: str) -> List[str]:
    """提取代码示例"""
    examples = []
    
    # 匹配代码块（Python代码）
    # 查找包含常见API调用的代码段
    code_patterns = [
        r'```python\n(.*?)```',
        r'```\n(.*?)```',
        r'# 示例[^\n]*\n(.*?)(?=\n\n|\n#|$)',
        r'示例[^\n]*\n(.*?)(?=\n\n|\n#|$)',
    ]
    
    for pattern in code_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            code = match.group(1).strip()
            if len(code) > 20 and ('get_' in code or 'order' in code or 'initialize' in code):
                examples.append(code)
    
    return examples[:10]  # 限制数量

def extract_api_doc(text: str, func_name: str) -> Dict[str, Any]:
    """提取特定API的文档"""
    doc = {
        "name": func_name,
        "description": "",
        "parameters": [],
        "returns": "",
        "examples": [],
        "notes": []
    }
    
    # 查找函数说明段落
    # 通常格式：函数名 + 描述 + 参数 + 返回 + 示例
    func_pattern = rf'{re.escape(func_name)}\s*\([^)]*\)\s*(.*?)(?=\n\n|\n[a-z_][a-z0-9_]*\s*\(|$)'
    match = re.search(func_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if match:
        doc_text = match.group(1)
        
        # 提取参数说明
        param_pattern = r'参数[：:]\s*(.*?)(?=返回|示例|注意|$)'
        param_match = re.search(param_pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if param_match:
            params_text = param_match.group(1)
            # 简单解析参数列表
            lines = params_text.split('\n')
            for line in lines:
                if ':' in line or '：' in line:
                    parts = re.split(r'[:：]', line, 1)
                    if len(parts) == 2:
                        doc["parameters"].append({
                            "name": parts[0].strip(),
                            "description": parts[1].strip()
                        })
        
        # 提取返回值说明
        return_pattern = r'返回[：:]\s*(.*?)(?=示例|注意|$)'
        return_match = re.search(return_pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if return_match:
            doc["returns"] = return_match.group(1).strip()
        
        # 提取示例
        example_pattern = r'示例[：:]\s*(.*?)(?=注意|$)'
        example_match = re.search(example_pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if example_match:
            doc["examples"].append(example_match.group(1).strip())
    
    return doc

def categorize_api(func_name: str) -> List[str]:
    """对API进行分类"""
    categories = []
    func_lower = func_name.lower()
    
    for category, keywords in API_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in func_lower or func_lower in keyword.lower():
                categories.append(category)
                break
    
    if not categories:
        categories.append("其他")
    
    return categories

def parse_all_documents():
    """解析所有文档"""
    print("=" * 70)
    print("构建聚宽API知识库")
    print("=" * 70)
    print()
    
    # 读取JSON文件
    print("📖 Step 1: 读取文档数据...")
    print("-" * 50)
    
    if not os.path.exists(JSON_FILE):
        print(f"  ❌ JSON文件不存在: {JSON_FILE}")
        return
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        all_pages = json.load(f)
    
    print(f"  ✅ 已加载 {len(all_pages)} 个页面")
    print()
    
    # 提取所有API
    print("🔍 Step 2: 提取API函数...")
    print("-" * 50)
    
    all_functions = {}
    all_examples = []
    
    for url, page_data in all_pages.items():
        text = page_data.get("text", "")
        if not text:
            continue
        
        # 提取函数定义
        functions = extract_function_definitions(text)
        for func in functions:
            func_name = func["name"]
            if func_name not in all_functions:
                all_functions[func_name] = {
                    "name": func_name,
                    "signature": func["signature"],
                    "params": func["params"],
                    "categories": categorize_api(func_name),
                    "description": "",
                    "examples": [],
                    "source_urls": []
                }
            
            all_functions[func_name]["source_urls"].append(url)
        
        # 提取代码示例
        examples = extract_code_examples(text)
        all_examples.extend(examples)
    
    print(f"  ✅ 发现 {len(all_functions)} 个API函数")
    print(f"  ✅ 提取 {len(all_examples)} 个代码示例")
    print()
    
    # 提取详细文档
    print("📝 Step 3: 提取详细文档...")
    print("-" * 50)
    
    # 重点API列表（从文档中识别的重要API）
    important_apis = [
        "get_price", "get_fundamentals", "get_index_stocks", "get_industry_stocks",
        "get_concept_stocks", "get_all_securities", "get_trade_days", "get_money_flow",
        "order", "order_target", "order_value", "initialize", "handle_data",
        "history", "attribute_history", "get_valuation", "get_fundamentals_continuously"
    ]
    
    detailed_docs = {}
    for url, page_data in all_pages.items():
        text = page_data.get("text", "")
        if not text:
            continue
        
        for api_name in important_apis:
            if api_name in text and api_name not in detailed_docs:
                doc = extract_api_doc(text, api_name)
                if doc.get("description") or doc.get("parameters"):
                    detailed_docs[api_name] = doc
                    if api_name in all_functions:
                        all_functions[api_name].update(doc)
    
    print(f"  ✅ 提取 {len(detailed_docs)} 个详细API文档")
    print()
    
    # 保存到知识库
    print("💾 Step 4: 保存到知识库...")
    print("-" * 50)
    
    knowledge_entries = []
    
    # 按分类组织
    for category, keywords in API_CATEGORIES.items():
        category_apis = []
        for func_name, func_data in all_functions.items():
            if category in func_data.get("categories", []):
                category_apis.append(func_data)
        
        if category_apis:
            # 创建分类知识条目
            content = f"# {category} API列表\n\n"
            content += f"共 {len(category_apis)} 个API函数\n\n"
            
            for api in category_apis[:20]:  # 限制数量
                content += f"## {api['name']}\n\n"
                if api.get("signature"):
                    content += f"**函数签名**: `{api['signature']}`\n\n"
                if api.get("description"):
                    content += f"**说明**: {api['description']}\n\n"
                if api.get("parameters"):
                    content += "**参数**:\n"
                    for param in api["parameters"][:5]:
                        content += f"- {param.get('name', '')}: {param.get('description', '')}\n"
                    content += "\n"
                if api.get("examples"):
                    content += "**示例**:\n```python\n"
                    content += api["examples"][0][:500] if api["examples"] else ""
                    content += "\n```\n\n"
                content += "---\n\n"
            
            knowledge_entries.append({
                "title": f"聚宽API - {category}",
                "content": content,
                "type": "api_reference",
                "tags": ["joinquant", "api", category.lower(), "reference"]
            })
    
    # 添加重要API的详细文档
    for api_name, api_data in detailed_docs.items():
        if api_name in all_functions:
            func_data = all_functions[api_name]
            content = f"# {api_name}\n\n"
            content += f"**函数签名**: `{func_data.get('signature', '')}`\n\n"
            
            if api_data.get("description"):
                content += f"## 说明\n\n{api_data['description']}\n\n"
            
            if api_data.get("parameters"):
                content += "## 参数\n\n"
                for param in api_data["parameters"]:
                    content += f"- **{param.get('name', '')}**: {param.get('description', '')}\n"
                content += "\n"
            
            if api_data.get("returns"):
                content += f"## 返回值\n\n{api_data['returns']}\n\n"
            
            if api_data.get("examples"):
                content += "## 示例\n\n```python\n"
                content += api_data["examples"][0]
                content += "\n```\n\n"
            
            knowledge_entries.append({
                "title": f"聚宽API - {api_name}",
                "content": content,
                "type": "api_reference",
                "tags": ["joinquant", "api", api_name, "detailed"] + func_data.get("categories", [])
            })
    
    # 批量添加到知识库
    success_count = 0
    for entry in knowledge_entries:
        try:
            result = mcp_xuanyuan_knowledge_add(
                title=entry["title"],
                content=entry["content"],
                type=entry["type"],
                tags=entry["tags"]
            )
            if result.get("success"):
                success_count += 1
                print(f"  ✅ {entry['title']}")
        except Exception as e:
            print(f"  ⚠️ {entry['title']}: {e}")
    
    print(f"\n  ✅ 成功添加 {success_count}/{len(knowledge_entries)} 个知识条目")
    print()
    
    # 保存到JSON文件
    print("💾 Step 5: 保存API索引...")
    print("-" * 50)
    
    api_index = {
        "total_apis": len(all_functions),
        "categories": {cat: len([f for f in all_functions.values() if cat in f.get("categories", [])]) 
                      for cat in API_CATEGORIES.keys()},
        "apis": {name: {
            "name": data["name"],
            "categories": data.get("categories", []),
            "has_detailed_doc": name in detailed_docs
        } for name, data in all_functions.items()},
        "created_at": datetime.now().isoformat()
    }
    
    index_file = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled/api_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(api_index, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ API索引: {index_file}")
    print()
    
    # 生成总结
    print("=" * 70)
    print("📊 知识库构建总结")
    print("=" * 70)
    print(f"""
总API函数: {len(all_functions)}
分类统计:
""")
    for category, count in api_index["categories"].items():
        if count > 0:
            print(f"  - {category}: {count} 个")
    print(f"""
知识库条目: {success_count} 个
API索引文件: {index_file}

构建完成!
""")
    
    return api_index

if __name__ == "__main__":
    try:
        api_index = parse_all_documents()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

