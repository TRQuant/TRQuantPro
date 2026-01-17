#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场状态知识库
==============

专门用于市场状态识别的知识库模块
支持按市场状态搜索知识、获取策略建议
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.knowledge_search_api import search


class RegimeKnowledgeBase:
    """市场状态知识库"""
    
    # 市场状态定义
    REGIME_TYPES = [
        "冷启动",
        "主升",
        "过热",
        "退潮",
        "崩溃"
    ]
    
    def __init__(self):
        self.kb_type = "market_regime"
    
    def search_by_regime(self, regime_type: str, limit: int = 5) -> List[Dict]:
        """
        按市场状态搜索知识
        
        Args:
            regime_type: 市场状态类型
            limit: 返回数量
            
        Returns:
            知识条目列表
        """
        query = f"市场状态 {regime_type}"
        result = search(query, type_filter=self.kb_type, limit=limit, mode="hybrid")
        
        if result.get('success'):
            return result.get('results', [])
        return []
    
    def get_regime_strategy_suggestions(self, regime_type: str) -> Dict[str, Any]:
        """
        获取市场状态的策略建议
        
        Args:
            regime_type: 市场状态类型
            
        Returns:
            策略建议字典
        """
        knowledge = self.search_by_regime(regime_type, limit=3)
        
        suggestions = {
            "regime": regime_type,
            "knowledge_count": len(knowledge),
            "strategy_implications": [],
            "risk_controls": [],
            "available_strategies": []
        }
        
        # 从知识中提取策略建议
        for item in knowledge:
            content = item.get('content', '')
            
            # 提取策略含义
            if "策略含义" in content or "策略建议" in content:
                # 简单提取（后续可优化为更智能的解析）
                suggestions["strategy_implications"].append({
                    "title": item.get('title', ''),
                    "content": content[:500]
                })
        
        return suggestions
    
    def list_all_regimes(self) -> List[str]:
        """列出所有市场状态类型"""
        return self.REGIME_TYPES


def get_regime_kb() -> RegimeKnowledgeBase:
    """获取市场状态知识库实例"""
    return RegimeKnowledgeBase()
