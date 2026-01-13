#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接改进知识库质量（直接操作JSON文件）
========================================

为所有V2知识添加可靠性标注和结论部分
"""

import sys
import json
from pathlib import Path
from typing import Dict

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))


def infer_reliability(item: Dict) -> str:
    """推断知识的可靠性等级"""
    content = item.get('content', '')
    source = item.get('source', '')
    
    # 检查是否已有可靠性标注
    if 'A级（高可靠性）' in content or '可靠性: A级' in content:
        return 'A级'
    if 'B级（中高可靠性）' in content or '可靠性: B级' in content:
        return 'B级'
    if 'C级（中等可靠性）' in content or '可靠性: C级' in content:
        return 'C级'
    
    # 根据来源推断
    source_lower = source.lower()
    content_lower = content.lower()
    
    # A级：回测验证
    if '回测验证' in source or '回测数据' in source or '回测' in content_lower:
        if 'ic' in content_lower or 'ir' in content_lower or '胜率' in content_lower:
            return 'A级'
    
    # B级：实战验证、专业文献
    if '实战验证' in source or '专业文献' in source:
        if '胜率' in content_lower or '平均收益' in content_lower:
            return 'B级'
    
    # C级：实战经验总结
    if '实战经验' in source or '经验总结' in source:
        return 'C级'
    
    # 默认C级
    return 'C级'


def add_conclusion(content: str, kb_type: str) -> str:
    """为知识内容添加结论部分"""
    
    # 检查是否已有结论
    if '## 结论' in content or '### 结论' in content:
        return content
    
    conclusion = "\n\n## 结论\n\n"
    
    if kb_type == 'factor_behavior':
        conclusion += "该因子的有效性取决于市场状态，需要结合市场状态判断使用。"
    elif kb_type == 'strategy_pattern':
        conclusion += "该策略模板需要根据市场状态灵活应用，注意风险控制。"
    elif kb_type == 'market_regime':
        conclusion += "准确识别市场状态是策略生成的基础，需要结合多个指标综合判断。"
    elif kb_type == 'failure_case':
        conclusion += "该失败案例提醒我们在使用相关因子或策略时需要注意其适用场景和局限性。"
    else:
        conclusion += "该知识条目提供了重要的参考信息，在实际应用中需要结合具体情况灵活使用。"
    
    conclusion += "\n"
    
    return content + conclusion


def add_reliability_info(content: str, reliability: str, source: str) -> str:
    """在内容开头添加可靠性信息"""
    
    # 检查是否已有可靠性信息
    if (
        '可靠性评级' in content or 
        '**可靠性评级**' in content or
        '可靠性: A级' in content or
        '可靠性: B级' in content or
        '可靠性: C级' in content
    ):
        return content
    
    reliability_info = f"""**可靠性评级**: {reliability}（{'高可靠性' if reliability == 'A级' else '中高可靠性' if reliability == 'B级' else '中等可靠性' if reliability == 'C级' else '低可靠性'}）

**知识来源**: {source}

---

"""
    
    return reliability_info + content


def improve_kb_quality_direct():
    """直接改进知识库质量（操作JSON文件）"""
    
    print("=" * 70)
    print("🔧 直接改进知识库质量")
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
    
    print(f"📊 找到 {len(v2_items)} 条V2知识")
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
            continue
        
        # 推断可靠性
        reliability = infer_reliability(item)
        
        # 检查是否需要添加
        needs_reliability = (
            '可靠性评级' not in content and 
            '**可靠性评级**' not in content and
            '可靠性: A级' not in content and
            '可靠性: B级' not in content and
            '可靠性: C级' not in content
        )
        needs_conclusion = (
            '## 结论' not in content and 
            '### 结论' not in content
        )
        
        if not needs_reliability and not needs_conclusion:
            continue
        
        print(f"[{i}/{len(v2_items)}] 更新: {title[:60]}")
        
        # 更新内容
        new_content = content
        
        if needs_reliability:
            new_content = add_reliability_info(new_content, reliability, source)
            reliability_added += 1
            print(f"    + 添加可靠性标注: {reliability}")
        
        if needs_conclusion:
            new_content = add_conclusion(new_content, kb_type)
            conclusion_added += 1
            print(f"    + 添加结论部分")
        
        # 直接更新
        item['content'] = new_content
        item['updated'] = '2026-01-13'
        
        # 更新tags
        tags = item.get('tags', [])
        if f'{reliability}可靠性' not in tags:
            tags.append(f'{reliability}可靠性')
        item['tags'] = tags
        
        improved_count += 1
        print(f"    ✅ 更新成功")
        print()
    
    # 保存知识库
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"📊 改进完成: {improved_count}/{len(v2_items)} 条知识已更新")
    print(f"   - 添加可靠性标注: {reliability_added} 条")
    print(f"   - 添加结论部分: {conclusion_added} 条")
    print("=" * 70)
    
    return improved_count > 0


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 直接改进知识库质量")
    print("=" * 70)
    print()
    
    success = improve_kb_quality_direct()
    
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
