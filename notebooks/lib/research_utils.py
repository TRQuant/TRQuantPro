"""
研究通用工具
============
提供JQData客户端、知识库查询、研究结论存储等功能
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)

# JQData客户端缓存
_jqdata_client = None


def get_jqdata_client():
    """
    获取JQData客户端（单例模式）
    
    Returns:
        JQDataClient: JQData客户端实例
    """
    global _jqdata_client
    
    if _jqdata_client is None:
        try:
            from core.module_registry import get_jqdata_client as _get_client
            _jqdata_client = _get_client()
            logger.info("JQData客户端已初始化")
        except Exception as e:
            logger.error(f"JQData客户端初始化失败: {e}")
            raise
    
    return _jqdata_client


def search_knowledge_base(query: str, type_filter: Optional[str] = None, limit: int = 10) -> Dict:
    """
    搜索知识库
    
    Args:
        query: 搜索关键词
        type_filter: 类型过滤（可选）
        limit: 返回结果数量限制
    
    Returns:
        Dict: 搜索结果
    """
    try:
        from mcp_servers.knowledge_search_api import search as kb_search
        result = kb_search(query=query, type_filter=type_filter, limit=limit, mode="auto")
        return result
    except Exception as e:
        logger.error(f"知识库搜索失败: {e}")
        return {
            "success": False,
            "query": query,
            "results": [],
            "total": 0,
            "error": str(e)
        }


def save_research_conclusion(
    module: str,
    findings: Dict[str, Any],
    recommendation: str,
    valid_until: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> str:
    """
    保存研究结论到知识库
    
    Args:
        module: 研究模块名称（如 "factor_combo", "market_trend"）
        findings: 研究发现（字典格式）
        recommendation: 实战建议
        valid_until: 有效期至（YYYY-MM-DD格式）
        metadata: 额外元数据
    
    Returns:
        str: 存储的知识库条目ID
    """
    try:
        from mcp_servers.unified_dev_server import knowledge_add
        
        # 构建研究结论内容
        content_parts = [
            f"# 研究结论 - {module}",
            f"**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 研究发现",
            "```json",
            json.dumps(findings, indent=2, ensure_ascii=False),
            "```",
            "",
            "## 实战建议",
            recommendation,
        ]
        
        if valid_until:
            content_parts.append(f"\n**有效期至**: {valid_until}")
        
        if metadata:
            content_parts.append("\n## 元数据")
            content_parts.append("```json")
            content_parts.append(json.dumps(metadata, indent=2, ensure_ascii=False))
            content_parts.append("```")
        
        content = "\n".join(content_parts)
        
        # 构建标签
        tags = ["研究结论", "research", module]
        if valid_until:
            tags.append(f"valid_until_{valid_until}")
        
        # 调用知识库存储接口
        result = knowledge_add(
            title=f"研究结论-{module}-{datetime.now().strftime('%Y%m%d')}",
            content=content,
            type="research_conclusion",
            tags=tags
        )
        
        if result.get("success"):
            logger.info(f"研究结论已保存: {result.get('id')}")
            return result.get("id", "")
        else:
            logger.error(f"研究结论保存失败: {result.get('error')}")
            return ""
            
    except Exception as e:
        logger.error(f"保存研究结论时出错: {e}")
        # 降级方案：保存到本地文件
        conclusion_file = PROJECT_ROOT / ".trquant" / "dev" / "research_conclusions" / f"{module}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        conclusion_file.parent.mkdir(parents=True, exist_ok=True)
        
        conclusion_data = {
            "module": module,
            "date": datetime.now().isoformat(),
            "findings": findings,
            "recommendation": recommendation,
            "valid_until": valid_until,
            "metadata": metadata or {}
        }
        
        conclusion_file.write_text(
            json.dumps(conclusion_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        logger.info(f"研究结论已保存到本地文件: {conclusion_file}")
        return str(conclusion_file)


def load_research_conclusions(module: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """
    加载历史研究结论
    
    Args:
        module: 模块名称过滤（可选）
        limit: 返回数量限制
    
    Returns:
        List[Dict]: 研究结论列表
    """
    try:
        # 先尝试从知识库加载
        query = f"研究结论 {module}" if module else "研究结论"
        result = search_knowledge_base(query, type_filter="research_conclusion", limit=limit)
        
        if result.get("success") and result.get("results"):
            return result["results"]
    except Exception as e:
        logger.warning(f"从知识库加载研究结论失败: {e}")
    
    # 降级方案：从本地文件加载
    conclusions_dir = PROJECT_ROOT / ".trquant" / "dev" / "research_conclusions"
    if not conclusions_dir.exists():
        return []
    
    conclusions = []
    pattern = f"{module}_*.json" if module else "*.json"
    
    for file in sorted(conclusions_dir.glob(pattern), reverse=True)[:limit]:
        try:
            data = json.loads(file.read_text(encoding='utf-8'))
            conclusions.append(data)
        except Exception as e:
            logger.warning(f"加载研究结论文件失败 {file}: {e}")
    
    return conclusions

