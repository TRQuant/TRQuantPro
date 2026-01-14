#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
陈小群策略知识库导入工具

从xiaoqun_reports目录导入资料到知识库，并支持网络爬取和关键词搜索增强
"""

import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入知识库工具（可选，如果MCP SDK不可用则跳过）
try:
    from mcp_servers.unified_dev_server import knowledge_add, knowledge_search
    MCP_AVAILABLE = True
except Exception:
    MCP_AVAILABLE = False
    print("⚠️  MCP SDK不可用，将只保存到策略知识库，不添加到主知识库")

# 知识库目录
XIAOQUN_REPORTS_DIR = TRQUANT_ROOT / "notebooks" / "research" / "chen_xiaoqun_strategy" / "xiaoqun_reports"
STRATEGY_KB_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "strategy_knowledge"
STRATEGY_KB_DIR.mkdir(parents=True, exist_ok=True)

# 知识库文件
STRATEGY_KB_FILE = STRATEGY_KB_DIR / "chen_xiaoqun_kb.json"


def load_strategy_kb() -> Dict:
    """加载策略知识库"""
    if STRATEGY_KB_FILE.exists():
        with open(STRATEGY_KB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "items": [],
        "stats": {
            "total": 0,
            "by_type": {},
            "by_tag": {}
        },
        "metadata": {
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0"
        }
    }


def save_strategy_kb(kb: Dict):
    """保存策略知识库"""
    kb["metadata"]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STRATEGY_KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


def add_to_strategy_kb(title: str, content: str, source_file: str = None, 
                      tags: List[str] = None, category: str = "strategy") -> str:
    """
    添加知识条目到策略知识库
    
    Args:
        title: 标题
        content: 内容
        source_file: 源文件路径
        tags: 标签列表
        category: 分类（strategy/emotion_cycle/stock_selection/position_management/case_study）
    
    Returns:
        知识条目ID
    """
    kb = load_strategy_kb()
    
    # 生成ID
    kb_id = f"cxq_{len(kb['items']) + 1:04d}"
    
    # 默认标签
    default_tags = ["chen_xiaoqun", "strategy", "trading_method"]
    if tags:
        default_tags.extend(tags)
    
    # 创建条目
    item = {
        "id": kb_id,
        "title": title,
        "content": content,
        "type": category,
        "tags": list(set(default_tags)),  # 去重
        "source": source_file,
        "useful_count": 0,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 添加到知识库
    kb["items"].insert(0, item)
    kb["stats"]["total"] += 1
    kb["stats"]["by_type"][category] = kb["stats"]["by_type"].get(category, 0) + 1
    
    # 更新标签统计
    for tag in item["tags"]:
        kb["stats"]["by_tag"][tag] = kb["stats"]["by_tag"].get(tag, 0) + 1
    
    save_strategy_kb(kb)
    
    # 同时添加到主知识库（用于统一搜索）
    if MCP_AVAILABLE:
        try:
            knowledge_add(
                title=title,
                content=content,
                type=category,
                tags=item["tags"],
                source=source_file
            )
        except Exception as e:
            print(f"⚠️  添加到主知识库失败: {e}")
    
    print(f"✅ 已添加: {kb_id} - {title}")
    return kb_id


def import_file(file_path: Path) -> Optional[str]:
    """导入单个文件"""
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return None
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except Exception as e:
        print(f"❌ 读取文件失败: {file_path}, 错误: {e}")
        return None
    
    if not content:
        print(f"⚠️  文件为空: {file_path}")
        return None
    
    # 根据文件名确定分类和标签
    file_name = file_path.stem
    
    category_map = {
        "30万到10亿投资智慧": ("strategy", ["investment_wisdom", "growth_story", "discipline", "trend_following"]),
        "华胜天成": ("case_study", ["case_study", "dragon_tiger_list", "ai_computing", "2026"]),
        "持仓": ("position_management", ["position_management", "holding_strategy", "concept_stocks"]),
        "游资思维习惯": ("strategy", ["trading_habits", "mindset", "discipline", "risk_control"]),
        "顺势而为": ("strategy", ["trend_following", "market_emotion", "dragon_stock"]),
        "龙虎榜复盘": ("case_study", ["dragon_tiger_list", "dtl_analysis", "quantitative_application"])
    }
    
    category, tags = category_map.get(file_name, ("strategy", []))
    
    # 生成标题
    title = f"陈小群策略 - {file_name}"
    
    # 添加到知识库
    kb_id = add_to_strategy_kb(
        title=title,
        content=content,
        source_file=str(file_path.relative_to(TRQUANT_ROOT)),
        tags=tags,
        category=category
    )
    
    return kb_id


def import_all_files():
    """导入所有文件"""
    print("=" * 80)
    print("开始导入陈小群策略知识库")
    print("=" * 80)
    
    if not XIAOQUN_REPORTS_DIR.exists():
        print(f"❌ 目录不存在: {XIAOQUN_REPORTS_DIR}")
        return
    
    # 获取所有文件
    files = list(XIAOQUN_REPORTS_DIR.iterdir())
    files = [f for f in files if f.is_file() and not f.name.startswith('.')]
    
    print(f"\n找到 {len(files)} 个文件:")
    for f in files:
        print(f"  - {f.name}")
    
    # 导入每个文件
    imported = []
    failed = []
    
    for file_path in files:
        print(f"\n处理: {file_path.name}")
        kb_id = import_file(file_path)
        if kb_id:
            imported.append((file_path.name, kb_id))
        else:
            failed.append(file_path.name)
    
    # 输出统计
    print("\n" + "=" * 80)
    print("导入完成")
    print("=" * 80)
    print(f"✅ 成功导入: {len(imported)} 个文件")
    for name, kb_id in imported:
        print(f"   - {name} → {kb_id}")
    
    if failed:
        print(f"\n❌ 导入失败: {len(failed)} 个文件")
        for name in failed:
            print(f"   - {name}")
    
    # 显示知识库统计
    kb = load_strategy_kb()
    print(f"\n📊 知识库统计:")
    print(f"   总条目数: {kb['stats']['total']}")
    print(f"   按类型分布:")
    for type_name, count in kb['stats']['by_type'].items():
        print(f"     - {type_name}: {count}")
    print(f"   热门标签:")
    sorted_tags = sorted(kb['stats']['by_tag'].items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"     - {tag}: {count}")


if __name__ == "__main__":
    import_all_files()
