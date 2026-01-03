"""
M3.3.2: 产业链图谱模块 (Industry Chain Graph)

实现产业链关系图谱

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ChainPosition(Enum):
    UPSTREAM = "upstream"
    MIDSTREAM = "midstream"
    DOWNSTREAM = "downstream"


class RelationType(Enum):
    SUPPLY = "supply"
    CUSTOMER = "customer"
    COMPETE = "compete"
    COOPERATE = "cooperate"


@dataclass
class IndustryNode:
    node_id: str
    name: str
    position: ChainPosition
    chain_name: str
    description: str = ""
    key_products: List[str] = field(default_factory=list)
    stocks: List[str] = field(default_factory=list)
    importance: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "position": self.position.value,
            "chain_name": self.chain_name,
            "description": self.description,
            "key_products": self.key_products,
            "stocks": self.stocks,
            "importance": self.importance
        }


@dataclass
class ChainEdge:
    source_id: str
    target_id: str
    relation_type: RelationType
    weight: float = 1.0
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value,
            "weight": self.weight,
            "description": self.description
        }


class IndustryChainGraph:
    """产业链图谱"""
    
    CHAIN_TEMPLATES = {
        "新能源汽车": {
            "upstream": ["锂矿", "钴矿", "正极材料", "负极材料", "隔膜", "电解液"],
            "midstream": ["电池PACK", "电机", "电控", "热管理"],
            "downstream": ["整车制造", "充电桩", "换电站"]
        },
        "光伏": {
            "upstream": ["多晶硅", "硅片", "银浆", "玻璃"],
            "midstream": ["电池片", "组件", "逆变器"],
            "downstream": ["光伏电站", "分布式光伏", "储能"]
        },
        "半导体": {
            "upstream": ["硅片", "光刻胶", "电子气体", "靶材"],
            "midstream": ["芯片设计", "晶圆代工", "封装测试"],
            "downstream": ["消费电子", "汽车电子", "工业控制"]
        },
        "AI人工智能": {
            "upstream": ["GPU芯片", "存储器", "服务器", "算力基础设施"],
            "midstream": ["大模型", "AI框架", "数据标注"],
            "downstream": ["智能客服", "自动驾驶", "医疗AI", "金融AI"]
        },
        "机器人": {
            "upstream": ["减速器", "伺服电机", "控制器", "传感器"],
            "midstream": ["机器人本体", "系统集成"],
            "downstream": ["工业自动化", "服务机器人", "特种机器人"]
        }
    }
    
    def __init__(self, mongo_uri: Optional[str] = None):
        self._db = None
        self._collection = None
        self._nodes: Dict[str, IndustryNode] = {}
        self._edges: List[ChainEdge] = []
        self._adjacency: Dict[str, List[str]] = {}
        self._stock_to_industries: Dict[str, Set[str]] = {}
        
        if mongo_uri:
            self._init_mongodb(mongo_uri)
        self._init_templates()
    
    def _init_mongodb(self, mongo_uri: str):
        try:
            from pymongo import MongoClient
            client = MongoClient(mongo_uri)
            self._db = client.trquant
            self._collection = self._db.industry_chain
        except Exception as e:
            logger.warning(f"产业链MongoDB连接失败: {e}")
    
    def _init_templates(self):
        for chain_name, positions in self.CHAIN_TEMPLATES.items():
            for pos_name, industries in positions.items():
                position = ChainPosition(pos_name)
                for industry in industries:
                    node_id = f"{chain_name}_{industry}"
                    self.add_node(IndustryNode(
                        node_id=node_id,
                        name=industry,
                        position=position,
                        chain_name=chain_name
                    ))
            self._build_chain_relations(chain_name, positions)
    
    def _build_chain_relations(self, chain_name: str, positions: Dict[str, List[str]]):
        upstream = positions.get("upstream", [])
        midstream = positions.get("midstream", [])
        downstream = positions.get("downstream", [])
        
        for up in upstream:
            for mid in midstream:
                self.add_edge(ChainEdge(
                    source_id=f"{chain_name}_{up}",
                    target_id=f"{chain_name}_{mid}",
                    relation_type=RelationType.SUPPLY
                ))
        
        for mid in midstream:
            for down in downstream:
                self.add_edge(ChainEdge(
                    source_id=f"{chain_name}_{mid}",
                    target_id=f"{chain_name}_{down}",
                    relation_type=RelationType.SUPPLY
                ))
    
    def add_node(self, node: IndustryNode) -> bool:
        if node.node_id in self._nodes:
            return False
        self._nodes[node.node_id] = node
        self._adjacency[node.node_id] = []
        return True
    
    def get_node(self, node_id: str) -> Optional[IndustryNode]:
        return self._nodes.get(node_id)
    
    def find_nodes_by_name(self, name: str) -> List[IndustryNode]:
        return [n for n in self._nodes.values() if name.lower() in n.name.lower()]
    
    def get_chain_nodes(self, chain_name: str) -> Dict[str, List[IndustryNode]]:
        result = {"upstream": [], "midstream": [], "downstream": []}
        for node in self._nodes.values():
            if node.chain_name == chain_name:
                result[node.position.value].append(node)
        return result
    
    def add_edge(self, edge: ChainEdge) -> bool:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            return False
        self._edges.append(edge)
        if edge.source_id not in self._adjacency:
            self._adjacency[edge.source_id] = []
        self._adjacency[edge.source_id].append(edge.target_id)
        return True
    
    def map_stock_to_industry(self, symbol: str, industry_node_id: str):
        if industry_node_id not in self._nodes:
            return
        node = self._nodes[industry_node_id]
        if symbol not in node.stocks:
            node.stocks.append(symbol)
        if symbol not in self._stock_to_industries:
            self._stock_to_industries[symbol] = set()
        self._stock_to_industries[symbol].add(industry_node_id)
    
    def get_stock_industries(self, symbol: str) -> List[IndustryNode]:
        node_ids = self._stock_to_industries.get(symbol, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]
    
    def get_industry_stocks(self, node_id: str) -> List[str]:
        node = self._nodes.get(node_id)
        return node.stocks if node else []
    
    def get_upstream(self, node_id: str, depth: int = 1) -> List[IndustryNode]:
        if depth <= 0:
            return []
        upstream = []
        for edge in self._edges:
            if edge.target_id == node_id and edge.relation_type == RelationType.SUPPLY:
                source_node = self._nodes.get(edge.source_id)
                if source_node:
                    upstream.append(source_node)
                    if depth > 1:
                        upstream.extend(self.get_upstream(edge.source_id, depth - 1))
        return upstream
    
    def get_downstream(self, node_id: str, depth: int = 1) -> List[IndustryNode]:
        if depth <= 0:
            return []
        downstream = []
        for edge in self._edges:
            if edge.source_id == node_id and edge.relation_type == RelationType.SUPPLY:
                target_node = self._nodes.get(edge.target_id)
                if target_node:
                    downstream.append(target_node)
                    if depth > 1:
                        downstream.extend(self.get_downstream(edge.target_id, depth - 1))
        return downstream
    
    def get_related_stocks(self, symbol: str, relation_depth: int = 1) -> Dict[str, List[str]]:
        result = {"same_industry": [], "upstream": [], "downstream": []}
        industries = self.get_stock_industries(symbol)
        
        for industry in industries:
            for stock in industry.stocks:
                if stock != symbol and stock not in result["same_industry"]:
                    result["same_industry"].append(stock)
            
            for upstream_node in self.get_upstream(industry.node_id, relation_depth):
                for stock in upstream_node.stocks:
                    if stock not in result["upstream"]:
                        result["upstream"].append(stock)
            
            for downstream_node in self.get_downstream(industry.node_id, relation_depth):
                for stock in downstream_node.stocks:
                    if stock not in result["downstream"]:
                        result["downstream"].append(stock)
        
        return result
    
    def analyze_chain_impact(self, trigger_node_id: str, impact_type: str = "positive") -> List[Dict[str, Any]]:
        impacts = []
        visited = set()
        
        def propagate(node_id: str, direction: str, depth: int, cumulative_weight: float):
            if node_id in visited or depth > 3:
                return
            visited.add(node_id)
            node = self._nodes.get(node_id)
            if not node:
                return
            
            impact = {
                "node_id": node_id,
                "name": node.name,
                "position": node.position.value,
                "direction": direction,
                "depth": depth,
                "impact_weight": cumulative_weight * node.importance,
                "affected_stocks": node.stocks
            }
            impacts.append(impact)
            
            if direction == "downstream":
                for ds in self.get_downstream(node_id, 1):
                    propagate(ds.node_id, direction, depth + 1, cumulative_weight * 0.7)
            elif direction == "upstream":
                for us in self.get_upstream(node_id, 1):
                    propagate(us.node_id, direction, depth + 1, cumulative_weight * 0.7)
        
        propagate(trigger_node_id, "downstream", 0, 1.0)
        visited.clear()
        propagate(trigger_node_id, "upstream", 0, 1.0)
        
        impacts.sort(key=lambda x: x["impact_weight"], reverse=True)
        return impacts
    
    def get_stats(self) -> Dict[str, Any]:
        chain_stats = {}
        for chain_name in self.CHAIN_TEMPLATES.keys():
            nodes = [n for n in self._nodes.values() if n.chain_name == chain_name]
            chain_stats[chain_name] = {
                "nodes": len(nodes),
                "stocks": sum(len(n.stocks) for n in nodes)
            }
        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "total_stocks_mapped": len(self._stock_to_industries),
            "chains": chain_stats
        }
    
    def list_chains(self) -> List[str]:
        return list(self.CHAIN_TEMPLATES.keys())
    
    def export_to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges],
            "stock_mapping": {s: list(industries) for s, industries in self._stock_to_industries.items()}
        }


_industry_chain: Optional[IndustryChainGraph] = None

def get_industry_chain(mongo_uri: Optional[str] = None) -> IndustryChainGraph:
    global _industry_chain
    if _industry_chain is None:
        _industry_chain = IndustryChainGraph(mongo_uri)
    return _industry_chain
