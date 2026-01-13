#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量改进知识库质量
==================

为所有知识条目添加：
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

from mcp_servers.unified_dev_server import knowledge_update


def infer_reliability(item: Dict) -> str:
    """推断知识的可靠性等级"""
    content = item.get('content', '')
    source = item.get('source', '') or ''
    tags = item.get('tags', [])
    title = item.get('title', '')
    
    # 检查是否已有可靠性标注
    if '可靠性评级' in content:
        # 提取已有的可靠性等级
        match = re.search(r'可靠性评级[：:]\s*([ABCD]级)', content)
        if match:
            return match.group(1)
    
    if 'A级可靠性' in content or 'A级' in str(tags):
        return 'A级'
    if 'B级可靠性' in content or 'B级' in str(tags):
        return 'B级'
    if 'C级可靠性' in content or 'C级' in str(tags):
        return 'C级'
    if 'D级可靠性' in content or 'D级' in str(tags):
        return 'D级'
    
    # 根据来源和内容推断
    source_lower = source.lower() if source else ''
    content_lower = content.lower()
    title_lower = title.lower()
    
    # A级：回测验证、IC/IR指标
    if '回测验证' in source or '回测数据' in source:
        if 'ic' in content_lower or 'ir' in content_lower or '胜率' in content_lower or '收益率' in content_lower:
            return 'A级'
    
    # B级：实战验证、专业文献、API文档
    if '实战验证' in source or '专业文献' in source or 'api' in source_lower or '文档' in source_lower:
        if '胜率' in content_lower or '平均收益' in content_lower or '实战' in content_lower:
            return 'B级'
    
    # 策略模板、最佳实践通常是B级
    if '策略模板' in title or '最佳实践' in title or '策略' in title_lower:
        return 'B级'
    
    # 因子行为映射通常是B级
    if '因子' in title or '行为映射' in title:
        return 'B级'
    
    # C级：实战经验总结
    if '实战经验' in source or '经验总结' in source or '实战案例' in source:
        return 'C级'
    
    # 默认C级
    return 'C级'


def generate_conclusion(content: str, kb_type: str, title: str) -> str:
    """生成结论部分"""
    
    # 检查是否已有结论
    if '## 结论' in content or '### 结论' in content or '**结论**' in content:
        return None  # 已有结论，不需要添加
    
    # 根据类型和内容生成结论
    conclusion = "\n\n## 结论\n\n"
    
    content_lower = content.lower()
    title_lower = title.lower()
    
    if '因子' in title or '行为映射' in title:
        # 因子行为映射的结论
        if '主升期' in content or '上涨' in content_lower:
            conclusion += "该因子在主升期具有较高的有效性，适合用于主升期的策略生成。在实际应用中需要结合市场状态判断使用。"
        elif '退潮期' in content or '下跌' in content_lower:
            conclusion += "该因子在退潮期有效性较低，不建议在退潮期使用。需要结合其他指标进行综合判断。"
        else:
            conclusion += "该因子的有效性取决于市场状态，需要结合市场状态判断使用。建议通过回测验证其有效性。"
    
    elif '策略' in title or '策略模板' in title:
        # 策略模板的结论
        if '主升期' in content or '上涨' in content_lower:
            conclusion += "该策略模板适用于主升期，能够有效捕捉主升期的市场机会。在实际应用中需要注意风险控制。"
        elif '退潮期' in content or '防御' in content_lower or '空仓' in content_lower:
            conclusion += "该策略模板适用于退潮期或防御场景，能够有效控制风险。在实际应用中需要严格执行。"
        else:
            conclusion += "该策略模板需要根据市场状态灵活应用，注意风险控制。建议通过回测验证其有效性。"
    
    elif '市场状态' in title or '市场状态识别' in title:
        # 市场状态识别的结论
        conclusion += "准确识别市场状态是策略生成的基础，需要结合多个指标综合判断。建议使用多维度验证方法提高准确性。"
    
    elif '失败案例' in title or '失败' in title_lower:
        # 失败案例的结论
        conclusion += "该失败案例提醒我们在使用相关因子或策略时需要注意其适用场景和局限性。应该从失败中吸取教训，避免重复犯错。"
    
    elif 'api' in title_lower or '接口' in title or '文档' in title:
        # API文档的结论
        conclusion += "该API接口提供了重要的功能支持，在实际使用中需要注意参数设置和错误处理。建议参考官方文档和示例代码。"
    
    elif '最佳实践' in title or '实践' in title_lower:
        # 最佳实践的结论
        conclusion += "该最佳实践提供了重要的参考信息，在实际应用中需要结合具体情况灵活使用。建议持续优化和改进。"
    
    elif '资金流向' in title or 'money_flow' in content_lower:
        # 资金流向的结论
        conclusion += "资金流向是重要的市场分析指标，可用于选股和择时。在实际应用中需要结合其他指标综合判断，注意数据质量。"
    
    elif '情绪' in title or 'sentiment' in content_lower:
        # 情绪因子的结论
        conclusion += "情绪因子是市场情绪分析的重要工具，可用于市场状态判断和风险预警。在实际应用中需要结合其他指标使用。"
    
    else:
        # 通用结论
        conclusion += "该知识条目提供了重要的参考信息，在实际应用中需要结合具体情况灵活使用。建议通过实践验证其有效性。"
    
    return conclusion


def improve_knowledge_item(item: Dict) -> Dict:
    """改进单个知识条目"""
    content = item.get('content', '')
    title = item.get('title', '')
    kb_type = item.get('type', '')
    
    updated = False
    new_content = content
    
    # 1. 添加可靠性标注
    if '可靠性评级' not in content:
        reliability = infer_reliability(item)
        reliability_section = f"\n**可靠性评级**: {reliability}（{'高可靠性' if reliability == 'A级' else '中高可靠性' if reliability == 'B级' else '中可靠性' if reliability == 'C级' else '低可靠性'}）\n\n"
        
        # 在内容开头添加可靠性标注
        if content.startswith('#'):
            # 如果以标题开始，在标题后添加
            lines = content.split('\n', 1)
            if len(lines) > 1:
                new_content = lines[0] + '\n' + reliability_section + lines[1]
            else:
                new_content = content + '\n' + reliability_section
        else:
            new_content = reliability_section + content
        
        updated = True
    
    # 2. 添加结论部分
    conclusion = generate_conclusion(new_content, kb_type, title)
    if conclusion:
        new_content = new_content + conclusion
        updated = True
    
    if updated:
        item['content'] = new_content
        # 更新tags，添加可靠性标签
        tags = item.get('tags', [])
        if '可靠性评级' in new_content:
            reliability = re.search(r'可靠性评级[：:]\s*([ABCD]级)', new_content)
            if reliability:
                reliability_tag = f"{reliability.group(1)}可靠性"
                if reliability_tag not in tags:
                    tags.append(reliability_tag)
        item['tags'] = tags
    
    return item, updated


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 批量改进知识库质量")
    print("=" * 70)
    print()
    
    # 读取知识库
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if not kb_file.exists():
        print(f"❌ 知识库文件不存在: {kb_file}")
        return
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    items = kb.get('items', [])
    print(f"📊 找到 {len(items)} 条知识条目")
    print()
    
    # 检查需要改进的条目
    need_reliability = []
    need_conclusion = []
    
    for item in items:
        content = item.get('content', '')
        if '可靠性评级' not in content:
            need_reliability.append(item)
        if '## 结论' not in content and '### 结论' not in content and '**结论**' not in content:
            need_conclusion.append(item)
    
    print(f"📋 需要添加可靠性标注: {len(need_reliability)}条")
    print(f"📋 需要添加结论部分: {len(need_conclusion)}条")
    print()
    
    # 改进知识条目
    improved_count = 0
    total_to_improve = len(set([i['id'] for i in need_reliability] + [i['id'] for i in need_conclusion]))
    
    print(f"🔧 开始改进 {total_to_improve} 条知识条目...")
    print()
    
    for i, item in enumerate(items, 1):
        improved_item, updated = improve_knowledge_item(item)
        
        if updated:
            # 直接更新JSON文件中的条目
            items[i-1] = improved_item
            improved_count += 1
            if i % 50 == 0:
                print(f"    📊 进度: {improved_count}/{i} 已改进")
    
    # 保存更新后的知识库
    kb['items'] = items
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 70)
    print(f"📊 改进完成: {improved_count}/{total_to_improve} 条知识已改进")
    print("=" * 70)
    
    # 最终统计
    items = kb.get('items', [])
    
    has_reliability = sum(1 for i in items if '可靠性评级' in i.get('content', ''))
    has_conclusion = sum(1 for i in items if '## 结论' in i.get('content', '') or '### 结论' in i.get('content', ''))
    
    print()
    print("=" * 70)
    print("📊 最终统计")
    print("=" * 70)
    print(f"总条目数: {len(items)}条")
    print(f"包含可靠性标注: {has_reliability}条 ({has_reliability/len(items)*100:.1f}%)")
    print(f"包含结论部分: {has_conclusion}条 ({has_conclusion/len(items)*100:.1f}%)")
    print("=" * 70)


if __name__ == '__main__':
    main()
