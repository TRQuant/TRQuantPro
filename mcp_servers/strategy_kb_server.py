#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Strategy KB Server (金融知识库)
========================================

专门为策略生成服务的金融知识库，包含：
- 结构化规则/约束（YAML）
- 研究卡片（Research Cards）
- 回测证据
- 因子/模板版本绑定

运行方式:
    python mcp_servers/strategy_kb_server.py

工具:
    - strategy_kb.rule.get: 获取规则
    - strategy_kb.rule.validate: 校验策略是否符合规则
    - strategy_kb.card.create/update/search/read: 研究卡CRUD
    - strategy_kb.query: 向量检索研究卡+资料
    - strategy_kb.version.get: 获取KB版本
"""

import sys
import json
import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import hashlib

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('StrategyKBServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 导入工程化落地件
from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
from mcp_servers.utils.schema import base_args_schema, merge_schema
from mcp_servers.utils.artifacts import create_artifact_if_needed, artifact_write
from mcp_servers.utils.confirm import verify_confirm_token
from mcp_servers.utils.error_handler import wrap_exception_response

# LangChain生态依赖（用于向量检索）
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_core.documents import Document
    from rank_bm25 import BM25Okapi
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logger.warning(f"LangChain生态依赖未安装，向量检索功能受限: {e}")
    Chroma = None
    Document = None
    HuggingFaceEmbeddings = None
    BM25Okapi = None

# Strategy KB路径
STRATEGY_KB_ROOT = TRQUANT_ROOT / "docs" / "strategy_kb"
RULES_DIR = STRATEGY_KB_ROOT / "rules"
CARDS_DIR = STRATEGY_KB_ROOT / "cards"
MATERIALS_DIR = STRATEGY_KB_ROOT / "materials"
EVIDENCE_DIR = STRATEGY_KB_ROOT / "evidence"

# 全局状态
_rules_cache: Dict[str, Dict] = {}  # 规则缓存
_cards_cache: Dict[str, Dict] = {}  # 研究卡缓存
_vector_store: Optional[Any] = None  # 向量存储（研究卡+资料）
_bm25_index: Optional[Any] = None  # BM25索引
_chunk_metadata: List[Dict] = []  # chunk metadata
_embedding_model = None  # Embedding模型


def _get_embedding_model():
    """获取或创建embedding模型（单例）"""
    global _embedding_model
    if _embedding_model is None and LANGCHAIN_AVAILABLE:
        try:
            _embedding_model = HuggingFaceEmbeddings(
                model_name="paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("Embedding模型已加载: paraphrase-multilingual-MiniLM-L12-v2")
        except Exception as e:
            logger.error(f"加载Embedding模型失败: {e}")
            _embedding_model = None
    return _embedding_model


def _load_rule(rule_name: str) -> Dict:
    """加载规则文件"""
    if rule_name in _rules_cache:
        return _rules_cache[rule_name]
    
    rule_file = RULES_DIR / f"{rule_name}.yml"
    if not rule_file.exists():
        raise FileNotFoundError(f"规则文件不存在: {rule_file}")
    
    with open(rule_file, 'r', encoding='utf-8') as f:
        rule_data = yaml.safe_load(f)
    
    _rules_cache[rule_name] = rule_data
    return rule_data


def _load_all_rules() -> Dict[str, Dict]:
    """加载所有规则"""
    rules = {}
    for rule_file in RULES_DIR.glob("*.yml"):
        rule_name = rule_file.stem
        try:
            rules[rule_name] = _load_rule(rule_name)
        except Exception as e:
            logger.warning(f"加载规则失败 {rule_name}: {e}")
    return rules


def _load_card(card_id: str) -> Dict:
    """加载研究卡"""
    if card_id in _cards_cache:
        card = _cards_cache[card_id].copy()
        # 确保所有值都是JSON可序列化的
        for k, v in card.items():
            if hasattr(v, 'isoformat'):  # date/datetime对象
                card[k] = v.isoformat()
        return card
    
    # 在所有cards子目录中查找
    for card_file in CARDS_DIR.rglob("*.md"):
        if card_file.stem.startswith(card_id) or card_id in card_file.stem:
            # 解析Markdown frontmatter
            content = card_file.read_text(encoding='utf-8')
            if content.startswith("---"):
                # 提取frontmatter
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    # 确保所有值都是JSON可序列化的
                    for k, v in frontmatter.items():
                        if hasattr(v, 'isoformat'):  # date/datetime对象
                            frontmatter[k] = v.isoformat()
                    frontmatter['content'] = parts[2].strip()
                    frontmatter['file_path'] = str(card_file.relative_to(TRQUANT_ROOT))
                    _cards_cache[card_id] = frontmatter
                    return frontmatter
    
    raise FileNotFoundError(f"研究卡不存在: {card_id}")


def _search_cards(query: str, filters: Dict = None) -> List[Dict]:
    """搜索研究卡（简单实现：文件名和内容匹配）"""
    results = []
    filters = filters or {}
    
    for card_file in CARDS_DIR.rglob("*.md"):
        try:
            content = card_file.read_text(encoding='utf-8')
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    card_text = parts[2].strip()
                    
                    # 简单匹配
                    if query.lower() in card_text.lower() or query.lower() in frontmatter.get('title', '').lower():
                        # 应用过滤
                        match = True
                        if filters.get('market') and frontmatter.get('market') != filters['market']:
                            match = False
                        if filters.get('horizon') and frontmatter.get('horizon') != filters['horizon']:
                            match = False
                        if filters.get('status') and frontmatter.get('status') != filters['status']:
                            match = False
                        
                        if match:
                            # 确保所有值都是JSON可序列化的
                            for k, v in frontmatter.items():
                                if hasattr(v, 'isoformat'):  # date/datetime对象
                                    frontmatter[k] = v.isoformat()
                            frontmatter['content'] = card_text
                            frontmatter['file_path'] = str(card_file.relative_to(TRQUANT_ROOT))
                            results.append(frontmatter)
        except Exception as e:
            logger.warning(f"读取研究卡失败 {card_file}: {e}")
    
    return results


def _validate_strategy(strategy_draft: Dict, rule_set: str = "all") -> Tuple[bool, List[str]]:
    """校验策略是否符合规则"""
    errors = []
    
    # 加载规则
    if rule_set == "all":
        rules = _load_all_rules()
    else:
        rules = {rule_set: _load_rule(rule_set)}
    
    # 校验策略约束
    if "strategy_constraints" in rules:
        constraints = rules["strategy_constraints"]
        
        # 检查持仓数
        positions = strategy_draft.get('positions', [])
        num_positions = len(positions)
        if num_positions < constraints.get('min_positions', 0):
            errors.append(f"持仓数{num_positions}小于最小要求{constraints.get('min_positions')}")
        if num_positions > constraints.get('max_positions', 1000):
            errors.append(f"持仓数{num_positions}大于最大要求{constraints.get('max_positions')}")
        
        # 检查单票仓位
        for pos in positions:
            if pos.get('weight', 0) > constraints.get('max_position_size', 1.0):
                errors.append(f"单票仓位{pos.get('weight')}超过最大限制{constraints.get('max_position_size')}")
    
    # 校验数据规则
    if "data_rules" in rules:
        data_rules = rules["data_rules"]
        if strategy_draft.get('use_future_data', False) and data_rules.get('no_future_data', True):
            errors.append("策略使用了未来数据，违反数据规则")
    
    return len(errors) == 0, errors


def _wrap_response(envelope: Dict[str, Any]) -> List[TextContent]:
    """包装响应为MCP格式"""
    return [TextContent(
        type="text",
        text=json.dumps(envelope, ensure_ascii=False, indent=2)
    )]


# 创建MCP服务器
server = Server("trquant-strategy-kb")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="strategy_kb.rule.get",
            description="获取规则（YAML格式）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "rule_name": {
                            "type": "string",
                            "enum": ["strategy_constraints", "data_rules", "risk_model", "cost_model", "universe_rules", "all"],
                            "description": "规则名称，或'all'获取所有规则"
                        },
                        "version": {
                            "type": "string",
                            "description": "规则版本（可选）"
                        }
                    },
                    "required": ["rule_name"]
                }
            )
        ),
        Tool(
            name="strategy_kb.rule.validate",
            description="校验策略是否符合规则",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "strategy_draft": {
                            "type": "object",
                            "description": "策略草案（JSON）"
                        },
                        "rule_set": {
                            "type": "string",
                            "enum": ["all", "strategy_constraints", "data_rules", "risk_model", "cost_model", "universe_rules"],
                            "default": "all",
                            "description": "要校验的规则集"
                        }
                    },
                    "required": ["strategy_draft"]
                }
            )
        ),
        Tool(
            name="strategy_kb.card.create",
            description="创建研究卡",
            inputSchema=merge_schema(
                base_args_schema(mode="execute"),
                {
                    "type": "object",
                    "properties": {
                        "card_data": {
                            "type": "object",
                            "description": "研究卡数据（包含id, title, hypothesis等）"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["momentum", "mean_reversion", "quality_growth", "event_driven", "sector_rotation"],
                            "description": "研究卡分类"
                        }
                    },
                    "required": ["card_data", "category"]
                }
            )
        ),
        Tool(
            name="strategy_kb.card.read",
            description="读取研究卡",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "研究卡ID"
                        }
                    },
                    "required": ["card_id"]
                }
            )
        ),
        Tool(
            name="strategy_kb.card.search",
            description="搜索研究卡",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "filters": {
                            "type": "object",
                            "properties": {
                                "market": {"type": "string"},
                                "horizon": {"type": "string", "enum": ["short", "medium", "long"]},
                                "status": {"type": "string", "enum": ["draft", "validated", "deprecated"]}
                            },
                            "description": "过滤条件"
                        }
                    },
                    "required": ["query"]
                }
            )
        ),
        Tool(
            name="strategy_kb.query",
            description="向量检索研究卡+资料（返回citations）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "查询问题"
                        },
                        "filters": {
                            "type": "object",
                            "properties": {
                                "market": {"type": "string"},
                                "horizon": {"type": "string"},
                                "status": {"type": "string"}
                            },
                            "description": "过滤条件"
                        },
                        "top_k": {
                            "type": "integer",
                            "default": 5,
                            "description": "返回Top-K结果"
                        }
                    },
                    "required": ["query"]
                }
            )
        ),
        Tool(
            name="strategy_kb.version.get",
            description="获取KB版本信息",
            inputSchema=base_schema
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """处理工具调用"""
    trace_id = extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "strategy_kb.rule.get":
            return _handle_rule_get(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.rule.validate":
            return _handle_rule_validate(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.card.create":
            return _handle_card_create(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.card.read":
            return _handle_card_read(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.card.search":
            return _handle_card_search(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.query":
            return _handle_query(arguments, trace_id, artifact_policy)
        elif name == "strategy_kb.version.get":
            return _handle_version_get(arguments, trace_id, artifact_policy)
        else:
            envelope = wrap_error_response(
                error_code="UNKNOWN_TOOL",
                error_message=f"未知工具: {name}",
                server_name="trquant-strategy-kb",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-strategy-kb",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


def _handle_rule_get(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.rule.get"""
    rule_name = arguments.get("rule_name", "all")
    version = arguments.get("version")
    
    try:
        if rule_name == "all":
            rules = _load_all_rules()
        else:
            rules = {rule_name: _load_rule(rule_name)}
        
        result = {
            "rules": rules,
            "version": version or "latest",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        envelope = wrap_error_response(
            error_code="RULE_LOAD_ERROR",
            error_message=f"加载规则失败: {str(e)}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.rule.get",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_rule", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.rule.get",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_rule_validate(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.rule.validate"""
    strategy_draft = arguments.get("strategy_draft", {})
    rule_set = arguments.get("rule_set", "all")
    
    try:
        is_valid, errors = _validate_strategy(strategy_draft, rule_set)
        
        result = {
            "is_valid": is_valid,
            "errors": errors,
            "rule_set": rule_set,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=f"校验失败: {str(e)}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.rule.validate",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_validation", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.rule.validate",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_card_create(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.card.create"""
    card_data = arguments.get("card_data", {})
    category = arguments.get("category")
    mode = arguments.get("mode", "dry_run")
    confirm_token = arguments.get("confirm_token")
    
    if mode == "execute" and not confirm_token:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="execute模式需要confirm_token",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.card.create",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    card_id = card_data.get("id", f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    if mode == "dry_run":
        result = {
            "card_id": card_id,
            "category": category,
            "status": "dry_run",
            "message": "预览模式，未实际创建"
        }
    else:
        try:
            # 创建研究卡文件
            card_dir = CARDS_DIR / category
            card_dir.mkdir(parents=True, exist_ok=True)
            card_file = card_dir / f"{card_id}.md"
            
            # 生成Markdown内容
            frontmatter = {k: v for k, v in card_data.items() if k != "content"}
            content = card_data.get("content", "")
            
            md_content = "---\n"
            md_content += yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False)
            md_content += "---\n\n"
            md_content += content
            
            card_file.write_text(md_content, encoding='utf-8')
            
            # 更新缓存
            _cards_cache[card_id] = card_data
            
            result = {
                "card_id": card_id,
                "category": category,
                "file_path": str(card_file.relative_to(TRQUANT_ROOT)),
                "status": "created"
            }
        except Exception as e:
            envelope = wrap_error_response(
                error_code="CARD_CREATE_ERROR",
                error_message=f"创建研究卡失败: {str(e)}",
                server_name="trquant-strategy-kb",
                tool_name="strategy_kb.card.create",
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_card", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.card.create",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_card_read(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.card.read"""
    card_id = arguments.get("card_id")
    
    try:
        card = _load_card(card_id)
        result = {
            "card": card,
            "timestamp": datetime.now().isoformat()
        }
    except FileNotFoundError:
        envelope = wrap_error_response(
            error_code="CARD_NOT_FOUND",
            error_message=f"研究卡不存在: {card_id}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.card.read",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    except Exception as e:
        envelope = wrap_error_response(
            error_code="CARD_READ_ERROR",
            error_message=f"读取研究卡失败: {str(e)}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.card.read",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_card", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.card.read",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_card_search(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.card.search"""
    query = arguments.get("query", "")
    filters = arguments.get("filters", {})
    
    try:
        cards = _search_cards(query, filters)
        result = {
            "query": query,
            "filters": filters,
            "cards": cards,
            "count": len(cards),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        envelope = wrap_error_response(
            error_code="CARD_SEARCH_ERROR",
            error_message=f"搜索研究卡失败: {str(e)}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.card.search",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_search", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.card.search",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _build_strategy_kb_index():
    """构建Strategy KB向量索引（研究卡+资料）"""
    global _vector_store, _bm25_index, _chunk_metadata
    
    if not LANGCHAIN_AVAILABLE:
        logger.warning("LangChain依赖未安装，无法构建向量索引")
        return False
    
    try:
        # 收集研究卡
        all_chunks = []
        for card_file in CARDS_DIR.rglob("*.md"):
            try:
                content = card_file.read_text(encoding='utf-8')
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        card_text = parts[2].strip()
                        
                        # 创建Document
                        doc_text = f"标题: {frontmatter.get('title', '')}\n假设: {frontmatter.get('hypothesis', '')}\n内容: {card_text}"
                        doc = Document(
                            page_content=doc_text,
                            metadata={
                                "type": "research_card",
                                "card_id": frontmatter.get("id", ""),
                                "title": frontmatter.get("title", ""),
                                "market": frontmatter.get("market", ""),
                                "horizon": frontmatter.get("horizon", ""),
                                "file_path": str(card_file.relative_to(TRQUANT_ROOT)),
                                "chunk_id": hashlib.md5(doc_text.encode()).hexdigest()[:8]
                            }
                        )
                        all_chunks.append(doc)
            except Exception as e:
                logger.warning(f"处理研究卡失败 {card_file}: {e}")
        
        if not all_chunks:
            logger.warning("没有可索引的研究卡")
            return False
        
        # 构建向量索引
        embedding_model = _get_embedding_model()
        if embedding_model is None:
            logger.warning("Embedding模型未加载")
            return False
        
        persist_directory = str(TRQUANT_ROOT / ".taorui" / "strategy_kb_chroma")
        _vector_store = Chroma.from_documents(
            documents=all_chunks,
            embedding=embedding_model,
            persist_directory=persist_directory,
            collection_name="strategy_kb"
        )
        
        # 构建BM25索引
        texts = [chunk.page_content for chunk in all_chunks]
        tokenized_texts = [text.lower().split() for text in texts]
        _bm25_index = BM25Okapi(tokenized_texts)
        
        # 保存metadata
        _chunk_metadata = [chunk.metadata for chunk in all_chunks]
        
        logger.info(f"Strategy KB索引构建完成: {len(all_chunks)} chunks")
        return True
    except Exception as e:
        logger.error(f"构建Strategy KB索引失败: {e}", exc_info=True)
        return False


def _load_strategy_kb_index():
    """加载Strategy KB向量索引（如果存在）"""
    global _vector_store
    
    if _vector_store is not None:
        return True
    
    if not LANGCHAIN_AVAILABLE:
        return False
    
    persist_directory = str(TRQUANT_ROOT / ".taorui" / "strategy_kb_chroma")
    if not Path(persist_directory).exists():
        return False
    
    try:
        embedding_model = _get_embedding_model()
        if embedding_model is None:
            return False
        
        _vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model,
            collection_name="strategy_kb"
        )
        logger.info("已加载Strategy KB向量索引")
        return True
    except Exception as e:
        logger.warning(f"加载Strategy KB索引失败: {e}")
        return False


def _handle_query(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.query - 向量检索研究卡+资料"""
    query = arguments.get("query", "")
    filters = arguments.get("filters", {})
    top_k = arguments.get("top_k", 5)
    
    if not query:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="query是必需的",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.query",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    try:
        # 尝试加载索引
        if not _load_strategy_kb_index():
            # 如果索引不存在，尝试构建
            if not _build_strategy_kb_index():
                # 降级到简单搜索
                logger.warning("向量索引不可用，使用简单搜索")
                cards = _search_cards(query, filters)
                citations = []
                for card in cards[:top_k]:
                    citations.append({
                        "type": "research_card",
                        "card_id": card.get("id", ""),
                        "title": card.get("title", ""),
                        "hypothesis": card.get("hypothesis", ""),
                        "market": card.get("market", ""),
                        "horizon": card.get("horizon", ""),
                        "content_preview": card.get("content", "")[:200] + "..." if len(card.get("content", "")) > 200 else card.get("content", ""),
                        "file_path": card.get("file_path", ""),
                        "version": card.get("version", "unknown"),
                        "score": 0.5  # 默认分数
                    })
                
                result = {
                    "query": query,
                    "filters": filters,
                    "citations": citations,
                    "count": len(citations),
                    "timestamp": datetime.now().isoformat(),
                    "message": "使用简单搜索（向量索引未构建）"
                }
            else:
                # 索引构建成功，使用向量检索
                return _handle_query(arguments, trace_id, artifact_policy)
        else:
            # 使用向量检索
            docs_with_scores = _vector_store.similarity_search_with_score(query, k=top_k * 2)
            
            citations = []
            for doc, score in docs_with_scores:
                # 应用过滤
                metadata = doc.metadata
                match = True
                if filters.get('market') and metadata.get('market') != filters['market']:
                    match = False
                if filters.get('horizon') and metadata.get('horizon') != filters['horizon']:
                    match = False
                
                if match:
                    citations.append({
                        "type": metadata.get("type", "research_card"),
                        "card_id": metadata.get("card_id", ""),
                        "title": metadata.get("title", ""),
                        "hypothesis": "",  # 需要从研究卡加载
                        "market": metadata.get("market", ""),
                        "horizon": metadata.get("horizon", ""),
                        "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "file_path": metadata.get("file_path", ""),
                        "version": "unknown",
                        "score": float(1 - score)  # 转换为相似度分数
                    })
            
            # 按分数排序
            citations.sort(key=lambda x: x["score"], reverse=True)
            citations = citations[:top_k]
            
            result = {
                "query": query,
                "filters": filters,
                "citations": citations,
                "count": len(citations),
                "timestamp": datetime.now().isoformat(),
                "retrieval_method": "vector_search"
            }
        
    except Exception as e:
        logger.error(f"查询失败: {e}", exc_info=True)
        envelope = wrap_error_response(
            error_code="QUERY_ERROR",
            error_message=f"查询失败: {str(e)}",
            server_name="trquant-strategy-kb",
            tool_name="strategy_kb.query",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    result = create_artifact_if_needed(result, "strategy_kb_query", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.query",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_version_get(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理strategy_kb.version.get"""
    # 获取版本信息（简化实现）
    kb_version = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # TODO: 从factor_server和template_server获取版本
    result = {
        "kb_version": kb_version,
        "factor_version": "v1.0.0",  # TODO: 从factor_server获取
        "template_version": "v1.0.0",  # TODO: 从template_server获取
        "rules_version": "v1.0.0",
        "timestamp": datetime.now().isoformat()
    }
    
    result = create_artifact_if_needed(result, "strategy_kb_version", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-strategy-kb",
        tool_name="strategy_kb.version.get",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


# 主程序
if __name__ == "__main__":
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())

