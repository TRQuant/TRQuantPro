#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴业银锡投资分析报告 - 导入到向量知识库
==========================================

功能：
1. 解析PDF文件（或使用提供的文本内容）
2. 将内容智能分段
3. 使用MCP工具添加到向量知识库
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 确保可从任意工作目录运行
# 脚本位置: /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/kb/import_xingye_yinxi_report.py
# 项目根目录: /home/taotao/.cursor/worktrees/TRQuant/ope
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# PDF文本内容（从websearch结果提取）
PDF_CONTENT = """# 兴业银锡投资分析报告

## 公司概况与业务模式简述

兴业银锡（内蒙古兴业银锡矿业股份有限公司，原名兴业矿业）是一家立足内蒙古的民营有色金属矿企，主营有色金属采选业务，主要产品包括锡、银、锌、铅等金属。公司拥有30余年历史，2011年通过借壳方式在深交所上市。经过多年发展，公司逐步收购了银漫矿业、乾金达矿业、融冠矿业、宇邦矿业等优质矿山资源，目前旗下有多个具备采矿权的矿业子公司。公司产业链涵盖地质勘探、矿石开采、选矿和部分冶炼，实现上游资源到中游精矿的一体化经营。

资源储量方面，兴业银锡在内蒙古和西藏等地拥有丰富的多金属资源。截至2024年底，公司白银矿石储量约2.72万吨，锡矿石储量约18.57万吨，在国内占比居前：白银储量占全国近40%，锡储量占全国近20%。公司主力矿山银漫矿业是国内最大的白银生产矿山之一，盈利能力突出。除银漫外，公司旗下乾金达矿业（主营铅锌银）、融冠矿业（主营铁锌）等在各自区域也处于龙头地位。公司于2023年将证券简称由"兴业矿业"变更为"兴业银锡"，凸显银和锡作为未来主要扩产矿种的核心地位。2025年初，公司完成对宇邦矿业的并购，该矿山拥有亚洲最大、全球排名前七的白银资源，使公司白银储量实现翻倍式增长。目前公司产品涵盖银、锡、铅、锌、铜、铁、锑等多种有色和贵金属，已发展成为大型综合矿业集团。公司同时积极开拓海外资源，布局印尼黄金项目和非洲锡矿项目，迈向全球化发展。

## 最新财务数据分析

根据公司最新披露的财务数据（2024年度报告），兴业银锡业绩增长强劲：2024年全年实现营业收入42.70亿元，同比增长15.23%；归属于上市公司股东的净利润15.30亿元，同比大增57.82%。扣除非经常性损益后的净利润为15.39亿元，同比增长50.23%，与净利润增速基本一致，表明主营业务增长是利润提升的主要来源。公司净利率由2023年的约26%大幅提升至2024年的约36%，利润弹性显著。这得益于矿产品销量增加以及成本管控优化，使利润增长远超收入增长。

分产品来看，2024年公司矿产银产量约229吨，矿产锡产量约8902吨，矿产锌产量约5.97万吨。其中白银产量较2023年增长约15%，主要由于核心矿山全面复产及品位提升；锡产量则与上年相近。产品价格方面，2024年白银平均售价约5554元/千克，较上年上涨29%，而单位生产成本约1890元/千克，较上年下降。锡精矿价格2024年平均在26万元/吨以上，保持高位。毛利率因此显著提高：2024年前三季度公司毛利率达64.3%，净利率38.8%。即使第四季度矿石产量略有下降，全年盈利能力仍创出新高。

现金流方面，公司经营性现金流保持充沛。2024年经营活动产生的现金流量净额为11.72亿元。尽管较2023年的20.36亿元略有下降，主要因报告期内支付并购预付款等影响，但仍大幅高于净利润，体现出矿业业务强劲的现金创造能力。公司2024年自由现金流转正，全年企业自由现金流约10.05亿元。债务结构上，随着盈利和现金流改善，公司积极偿还借款以降低财务杠杆。2024年末资产负债率降至约35%，较2023年末的42%明显下降。财务费用由2023年的1.37亿元下降至2024年的1.19亿元，降低了13.6%，反映出银行借款余额减少、利息支出下降。截至2024年底，公司货币资金余额11.39亿元，较年初增加8亿元，流动性良好，短期偿债压力不大。值得注意的是，2024年公司筹资活动现金流净额为-0.23亿元，同比大幅收窄96%。公司在报告期内适度增加了一些银行借款以支持项目并购和扩产需求。总体来看，公司负债结构稳健，利息保障倍数较高，财务风险可控。

## 估值分析

兴业银锡目前享有较高的盈利增速，但其估值水平在同行中相对合理。以市盈率（P/E）来看，根据2025年盈利预测计算，公司2024年实际净利对应PE约16倍，2025年预测净利对应PE仅约12倍。这一水平在可比公司中处于中等：同行中云南锡业股份（000960.SZ）作为全球最大的锡业公司，2025年预测PE约9.8倍，华锡有色（600301.SH，广西主要锡企）约10.5倍，而盛达资源（000603.SZ，国内白银龙头之一）2025年预测PE约14.6倍。兴业银锡作为同时涉及白银和锡的资源股，成长性高于传统锡企，估值略高于云南锡业、华锡有色但低于纯白银标的盛达资源，相对估值较为合理。

公司的市净率（P/B）约为2.9倍（以2024年末每股净资产4.45元计算）。这一水平反映出市场给予公司丰富资源储量和高成长预期一定溢价：同期云南锡业P/B约1.2倍，华锡有色约3.0倍，盛达资源约3.0倍。兴业银锡PB略高于行业平均，但考虑到公司白银+锡双资源在国内占据的重要地位（银储量全国第一、锡储量全国第二梯队），以及未来产量扩张前景，这一溢价具有一定合理性。

从企业价值/EBITDA指标看，2024年公司EV/EBITDA约8.5倍，处于行业中等水平。考虑到公司未来产能扩张带来的EBITDA增长潜力，以及银锡价格的长期上涨趋势，这一估值水平具有一定吸引力。

## 行业前景与风险因素

### 行业前景
白银和锡作为重要的工业金属，在新能源、电子、光伏等领域的应用持续增长。随着全球新能源转型加速，对白银和锡的需求有望持续增长。同时，供给端受限于矿山资源稀缺性和开采成本上升，供需格局有利于价格上涨。

### 主要风险因素
1. **金属价格波动风险**：公司业绩与银锡价格高度相关，价格波动将直接影响盈利。
2. **产能释放不及预期**：新矿山投产进度可能受到环保、安全等因素影响。
3. **财务杠杆风险**：虽然公司债务结构有所改善，但仍需关注现金流状况。
4. **行业政策风险**：环保政策收紧可能影响矿山生产。

## 投资建议

综合考虑公司基本面、估值水平和行业前景，我们认为兴业银锡当前具备"基本面+技术面"共振的投资机会：基本面上产能释放与银锡高价共振带来盈利高增；技术面和筹码面显示股价趋势良好、筹码稳固。当然，投资者应保持理性预期，密切关注金属价格和项目进展动态。如基本面出现不利变化，应及时调整仓位。总体而言，在合理价格区间布局兴业银锡，中长期有望获得可观收益，建议积极关注并逢低介入。

## 参考来源

- 公司定期报告（2024年年度报告）
- 券商研报：国信证券《立足资源禀赋，全球化布局开展新篇章》（2025/05/16）
- 券商研报：中邮证券《Q3业绩环比下滑，增量项目顺利推进》（2024/11/03）
- 行业资讯：上海有色网、有色金属协会等（锡矿供需及价格）
- 媒体报道：证券时报网、凤凰网财经等（股东户数、MSCI指数纳入等）
- 公司官网及公告（项目进展、并购动态）
"""


def parse_pdf_text(text: str) -> List[Dict[str, Any]]:
    """
    解析PDF文本内容，智能分段
    
    返回格式：
    [
        {
            "title": "段落标题",
            "content": "段落内容",
            "type": "knowledge_type",
            "tags": ["tag1", "tag2"]
        },
        ...
    ]
    """
    sections = []
    
    # 按一级标题分割
    parts = re.split(r'^#\s+(.+)$', text, flags=re.MULTILINE)
    
    # 第一部分是标题
    main_title = parts[0].strip() if parts else "兴业银锡投资分析报告"
    
    # 处理每个主要章节
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
            
        section_title = parts[i].strip()
        section_content = parts[i + 1].strip()
        
        # 进一步按二级标题分割
        subsections = re.split(r'^##\s+(.+)$', section_content, flags=re.MULTILINE)
        
        if len(subsections) == 1:
            # 没有子标题，整个作为一个条目
            entry = _create_kb_entry(
                title=f"{main_title} - {section_title}",
                content=section_content,
                type="lesson",
                tags=["兴业银锡", "000426", "投资分析", "有色金属", "矿业"]
            )
            sections.append(entry)
        else:
            # 有子标题，每个子标题作为一个条目
            for j in range(1, len(subsections), 2):
                if j + 1 >= len(subsections):
                    break
                    
                subsection_title = subsections[j].strip()
                subsection_content = subsections[j + 1].strip()
                
                entry = _create_kb_entry(
                    title=f"{main_title} - {section_title} - {subsection_title}",
                    content=subsection_content,
                    type=_infer_type(subsection_title),
                    tags=_infer_tags(subsection_title, subsection_content)
                )
                sections.append(entry)
    
    return sections


def _create_kb_entry(title: str, content: str, type: str, tags: List[str]) -> Dict[str, Any]:
    """创建知识库条目"""
    return {
        "title": title,
        "content": content,
        "type": type,
        "tags": tags
    }


def _infer_type(section_title: str) -> str:
    """根据章节标题推断知识类型"""
    title_lower = section_title.lower()
    
    if "风险" in section_title:
        return "practice"
    elif "财务" in section_title or "数据" in section_title:
        return "lesson"
    elif "估值" in section_title:
        return "lesson"
    elif "投资建议" in section_title or "结论" in section_title:
        return "practice"
    else:
        return "lesson"


def _infer_tags(section_title: str, content: str) -> List[str]:
    """根据章节标题和内容推断标签"""
    tags = ["兴业银锡", "000426", "投资分析"]
    
    title_lower = section_title.lower()
    content_lower = content.lower()
    
    # 行业标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["有色金属", "矿业", "银", "锡"]):
        tags.extend(["有色金属", "矿业", "资源股"])
    
    # 财务标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["财务", "营收", "净利润", "现金流"]):
        tags.append("财务分析")
    
    # 估值标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["估值", "PE", "PB", "EV/EBITDA"]):
        tags.append("估值分析")
    
    # 风险标签
    if "风险" in title_lower:
        tags.append("风险分析")
    
    # 投资建议标签
    if any(keyword in title_lower 
           for keyword in ["投资建议", "结论", "建议"]):
        tags.append("投资建议")
    
    return list(dict.fromkeys(tags))  # 去重


def _simple_knowledge_add(title: str, content: str, type: str = "lesson", 
                          tags: List[str] = None, source: str = None) -> Dict[str, Any]:
    """直接添加到知识库JSON文件（不依赖MCP SDK）"""
    import json
    from datetime import datetime
    import hashlib
    
    # 知识库文件路径
    kb_dir = _PROJECT_ROOT / ".trquant" / "dev" / "knowledge"
    kb_dir.mkdir(parents=True, exist_ok=True)
    kb_file = kb_dir / "knowledge_base.json"
    
    # 加载现有知识库
    if kb_file.exists():
        try:
            kb = json.loads(kb_file.read_text(encoding='utf-8'))
        except:
            kb = {"items": [], "stats": {"total": 0, "by_type": {}}}
    else:
        kb = {"items": [], "stats": {"total": 0, "by_type": {}}}
    
    # 生成ID
    kb_id = f"kb_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(title.encode()).hexdigest()[:8]}"
    
    # 创建条目
    item = {
        "id": kb_id,
        "title": title,
        "content": content,
        "type": type,
        "tags": tags or [],
        "source": source,
        "useful_count": 0,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    # 添加到知识库
    kb["items"].insert(0, item)
    kb["stats"]["total"] = len(kb["items"])
    kb["stats"]["by_type"][type] = kb["stats"]["by_type"].get(type, 0) + 1
    
    # 保存
    kb_file.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding='utf-8')
    
    return {"success": True, "knowledge_id": kb_id, "item": item}


def add_to_knowledge_base(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    将知识库条目添加到向量知识库
    
    使用MCP工具或直接调用知识库API
    """
    # 直接使用简化版本（不依赖MCP SDK）
    results = {
        'success': 0,
        'failed': 0,
        'errors': [],
        'knowledge_ids': []
    }
    
    for entry in entries:
        try:
            result = _simple_knowledge_add(
                title=entry['title'],
                content=entry['content'],
                type=entry['type'],
                tags=entry['tags'],
                source="兴业银锡投资分析报告.pdf"
            )
            
            if result.get('success') or result.get('knowledge_id'):
                results['success'] += 1
                kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
                results['knowledge_ids'].append(kb_id)
                print(f"✅ 已添加: {entry['title'][:50]}... (ID: {kb_id})")
            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unknown error')
                results['errors'].append(f"{entry['title']}: {error_msg}")
                print(f"❌ 添加失败: {entry['title'][:50]}... - {error_msg}")
                
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{entry['title']}: {str(e)}")
            print(f"❌ 异常: {entry['title'][:50]}... - {str(e)}")
    
    return results


def main():
    """主函数"""
    print("=" * 80)
    print("📚 兴业银锡投资分析报告 - 导入到向量知识库")
    print("=" * 80)
    print()
    
    # 1. 解析PDF文本
    print("📄 步骤1: 解析PDF文本内容...")
    entries = parse_pdf_text(PDF_CONTENT)
    print(f"   共解析出 {len(entries)} 个知识条目")
    print()
    
    # 2. 显示条目预览
    print("📋 步骤2: 知识条目预览...")
    for i, entry in enumerate(entries[:5], 1):
        print(f"   {i}. {entry['title']}")
        print(f"      类型: {entry['type']}, 标签: {', '.join(entry['tags'][:5])}")
        print(f"      内容: {entry['content'][:100]}...")
        print()
    
    if len(entries) > 5:
        print(f"   ... 还有 {len(entries) - 5} 个条目")
        print()
    
    # 3. 添加到知识库
    print("💾 步骤3: 添加到向量知识库...")
    results = add_to_knowledge_base(entries)
    
    # 4. 显示结果
    print()
    print("=" * 80)
    print("📊 导入结果汇总")
    print("=" * 80)
    print(f"✅ 成功: {results.get('success', 0)} 条")
    print(f"❌ 失败: {results.get('failed', 0)} 条")
    
    if results.get('errors'):
        print()
        print("❌ 错误详情:")
        for error in results['errors'][:5]:
            print(f"   - {error}")
        if len(results['errors']) > 5:
            print(f"   ... 还有 {len(results['errors']) - 5} 个错误")
    
    if results.get('knowledge_ids'):
        print()
        print("📝 知识库ID:")
        for kid in results['knowledge_ids'][:10]:
            print(f"   - {kid}")
        if len(results['knowledge_ids']) > 10:
            print(f"   ... 还有 {len(results['knowledge_ids']) - 10} 个ID")
    
    print()
    print("=" * 80)
    print("✅ 导入完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
