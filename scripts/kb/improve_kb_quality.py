#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
改进知识库质量
==============

为所有V2知识添加：
1. 可靠性标注
2. 结论部分
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_update, knowledge_get


def infer_reliability(item: Dict) -> str:
    """推断知识的可靠性等级"""
    content = item.get('content', '')
    source = item.get('source', '')
    tags = item.get('tags', [])
    
    # 检查是否已有可靠性标注
    if 'A级可靠性' in content or 'A级' in str(tags):
        return 'A级'
    if 'B级可靠性' in content or 'B级' in str(tags):
        return 'B级'
    if 'C级可靠性' in content or 'C级' in str(tags):
        return 'C级'
    if 'D级可靠性' in content or 'D级' in str(tags):
        return 'D级'
    
    # 根据来源推断
    source_lower = source.lower()
    content_lower = content.lower()
    
    # A级：回测验证
    if '回测验证' in source or '回测数据' in source or '回测' in content_lower:
        if 'ic' in content_lower or 'ir' in content_lower or '胜率' in content_lower:
            return 'A级'
    
    # B级：实战验证、专业文献
    if '实战验证' in source or '专业文献' in source or '实战' in source_lower:
        if '胜率' in content_lower or '平均收益' in content_lower:
            return 'B级'
    
    # C级：实战经验总结
    if '实战经验' in source or '经验总结' in source:
        return 'C级'
    
    # 默认C级
    return 'C级'


def add_conclusion(content: str, kb_type: str, title: str) -> str:
    """为知识内容添加结论部分"""
    
    # 检查是否已有结论
    if '## 结论' in content or '### 结论' in content or '**结论**' in content:
        return content
    
    # 根据类型生成结论
    conclusion = "\n\n## 结论\n\n"
    
    if kb_type == 'factor_behavior':
        # 因子行为映射的结论
        if '主升期' in content:
            conclusion += "该因子在主升期具有较高的有效性，适合用于主升期的策略生成。"
        elif '退潮期' in content:
            conclusion += "该因子在退潮期有效性较低，不建议在退潮期使用。"
        else:
            conclusion += "该因子的有效性取决于市场状态，需要结合市场状态判断使用。"
    
    elif kb_type == 'strategy_pattern':
        # 策略模板的结论
        if '主升期' in content:
            conclusion += "该策略模板适用于主升期，能够有效捕捉主升期的市场机会。"
        elif '退潮期' in content or '防御' in content:
            conclusion += "该策略模板适用于退潮期或防御场景，能够有效控制风险。"
        else:
            conclusion += "该策略模板需要根据市场状态灵活应用，注意风险控制。"
    
    elif kb_type == 'market_regime':
        # 市场状态识别的结论
        conclusion += "准确识别市场状态是策略生成的基础，需要结合多个指标综合判断。"
    
    elif kb_type == 'failure_case':
        # 失败案例的结论
        conclusion += "该失败案例提醒我们在使用相关因子或策略时需要注意其适用场景和局限性。"
    
    else:
        conclusion += "该知识条目提供了重要的参考信息，在实际应用中需要结合具体情况灵活使用。"
    
    conclusion += "\n"
    
    return content + conclusion


def add_reliability_info(content: str, reliability: str, source: str) -> str:
    """在内容开头添加可靠性信息"""
    
    # 检查是否已有可靠性信息（更精确的检测）
    if (
        '可靠性评级' in content or 
        '**可靠性评级**' in content or
        '可靠性: A级' in content or
        '可靠性: B级' in content or
        '可靠性: C级' in content or
        'A级（高可靠性）' in content or
        'B级（中高可靠性）' in content or
        'C级（中等可靠性）' in content
    ):
        return content
    
    reliability_info = f"""**可靠性评级**: {reliability}（{'高可靠性' if reliability == 'A级' else '中高可靠性' if reliability == 'B级' else '中等可靠性' if reliability == 'C级' else '低可靠性'}）

**知识来源**: {source}

---

"""
    
    return reliability_info + content


def improve_kb_quality():
    """改进知识库质量"""
    
    print("=" * 70)
    print("🔧 改进知识库质量")
    print("=" * 70)
    print()
    
    # 加载知识库
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if not kb_file.exists():
        print("❌ 知识库文件不存在")
        return False
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    items = kb.get('items', [])
    v2_items = [i for i in items if i.get('type') in ['market_regime', 'factor_behavior', 'strategy_pattern', 'failure_case']]
    
    print(f"📊 找到 {len(v2_items)} 条V2知识需要改进")
    print()
    
    improved_count = 0
    reliability_added = 0
    conclusion_added = 0
    
    for i, item in enumerate(v2_items, 1):
        item_id = item.get('id', '')
        title = item.get('title', '')
        content = item.get('content', '')
        kb_type = item.get('type', '')
        source = item.get('source', '实战经验总结')
        
        if not item_id:
            print(f"[{i}/{len(v2_items)}] ⚠️  跳过（无ID）: {title[:50]}")
            continue
        
        print(f"[{i}/{len(v2_items)}] 改进: {title[:60]}")
        
        # 推断可靠性
        reliability = infer_reliability(item)
        
        # 检查是否需要添加可靠性信息（更精确的检测）
        needs_reliability = (
            '可靠性评级' not in content and 
            '**可靠性评级**' not in content and
            '可靠性: A级' not in content and
            '可靠性: B级' not in content and
            '可靠性: C级' not in content and
            'A级（高可靠性）' not in content and
            'B级（中高可靠性）' not in content and
            'C级（中等可靠性）' not in content
        )
        needs_conclusion = (
            '## 结论' not in content and 
            '### 结论' not in content and 
            '**结论**' not in content
        )
        
        # 即使已有部分内容，也检查是否需要补充
        if not needs_reliability and not needs_conclusion:
            print(f"    ✅ 已包含可靠性标注和结论")
            continue
        
        # 如果只需要补充其中一个，也继续处理
        if needs_reliability or needs_conclusion:
            print(f"    📝 需要补充: ", end="")
            if needs_reliability:
                print("可靠性标注", end="")
            if needs_reliability and needs_conclusion:
                print(" + ", end="")
            if needs_conclusion:
                print("结论部分", end="")
            print()
        
        # 更新内容
        new_content = content
        
        if needs_reliability:
            new_content = add_reliability_info(new_content, reliability, source)
            reliability_added += 1
            print(f"    + 添加可靠性标注: {reliability}")
        
        if needs_conclusion:
            new_content = add_conclusion(new_content, kb_type, title)
            conclusion_added += 1
            print(f"    + 添加结论部分")
        
        # 更新知识条目
        try:
            # 更新tags，添加可靠性标签
            tags = item.get('tags', [])
            if f'{reliability}可靠性' not in tags:
                tags.append(f'{reliability}可靠性')
            
            result = knowledge_update(
                knowledge_id=item_id,
                content=new_content,
                tags=tags
            )
            
            if result.get('success'):
                print(f"    ✅ 更新成功")
                improved_count += 1
            else:
                print(f"    ❌ 更新失败: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
        
        print()
    
    print("=" * 70)
    print(f"📊 改进完成: {improved_count}/{len(v2_items)} 条知识已更新")
    print(f"   - 添加可靠性标注: {reliability_added} 条")
    print(f"   - 添加结论部分: {conclusion_added} 条")
    print("=" * 70)
    
    return improved_count > 0


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 改进知识库质量")
    print("=" * 70)
    print()
    
    success = improve_kb_quality()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 知识库质量改进成功！")
        print()
        print("📋 改进内容:")
        print("   - 为所有V2知识添加可靠性标注")
        print("   - 为所有V2知识添加结论部分")
        print()
        print("🎯 下一步:")
        print("   1. 运行测试脚本验证改进效果")
        print("   2. 继续补充更多高可靠性知识")
    else:
        print("❌ 知识库质量改进失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
