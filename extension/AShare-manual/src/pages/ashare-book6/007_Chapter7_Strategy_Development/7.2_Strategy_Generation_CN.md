---
title: "7.2 策略生成"
description: "深入解析策略生成器，包括Strategy KB检索、规则验证、策略草案生成、Python代码生成等核心技术"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🛠️ 7.2 策略生成

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统的策略生成器，通过Strategy KB和Workflow Server实现从投资主线到可执行策略代码的自动化生成。通过理解Strategy KB检索、规则验证、策略草案生成和Python代码生成的核心技术，帮助开发者掌握如何自动生成策略代码，为策略开发提供完整的自动化能力。

策略生成是策略开发模块的核心组件，通过Strategy KB和Workflow Server实现从投资主线到可执行策略代码的自动化生成。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-7-2-1')">
    <h4>🔍 7.2.1 Strategy KB检索</h4>
    <p>研究卡检索、规则检索、向量检索、BM25检索、多阶段检索</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-7-2-2')">
    <h4>✅ 7.2.2 规则验证</h4>
    <p>策略约束验证、风险模型验证、成本模型验证、数据规则验证</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-7-2-3')">
    <h4>📝 7.2.3 策略草案生成</h4>
    <p>策略结构定义、参数配置、逻辑生成、引用信息生成</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-7-2-4')">
    <h4>🐍 7.2.4 Python代码生成</h4>
    <p>代码模板应用、参数填充、逻辑代码生成、代码优化</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-7-2-5')">
    <h4>💾 7.2.5 文件保存与版本管理</h4>
    <p>策略文件保存、版本管理、元数据记录、引用信息保存</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-7-2-6')">
    <h4>🔄 7.2.6 工作流集成</h4>
    <p>工作流调用、输入输出、错误处理、自动化流程</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解Strategy KB检索**：掌握研究卡检索、规则检索和向量检索方法
- **掌握规则验证**：理解策略约束验证、风险模型验证和成本模型验证
- **实现策略草案生成**：掌握策略结构定义和参数配置方法
- **生成Python代码**：理解代码模板应用和参数填充机制
- **管理策略文件**：掌握策略文件保存和版本管理方法

## 📚 核心概念

### 模块定位

- **工作流位置**：步骤6 - 🛠️ 策略生成
- **核心职责**：Strategy KB检索、规则验证、策略草案生成、Python代码生成
- **服务对象**：策略优化、回测验证、实盘交易

### 设计理念

策略生成器遵循以下设计理念：

1. **知识驱动**：基于Strategy KB的研究卡和规则生成策略
2. **规则约束**：所有生成的策略必须通过规则验证
3. **可追溯性**：生成的策略包含完整的研究卡和规则引用
4. **自动化**：从投资主线到策略代码的完全自动化
5. **可扩展性**：支持新的策略类型和平台扩展

<h2 id="section-7-2-1">🔍 7.2.1 Strategy KB检索</h2>

Strategy KB检索是策略生成的第一步，通过检索研究卡和规则获取策略生成所需的知识。

### 研究卡检索

研究卡检索通过向量检索和关键词检索从Strategy KB中检索相关的研究卡。

#### 向量检索

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List, Dict, Any

class StrategyKBRetriever:
    """Strategy KB检索器"""
    
    def __init__(self, kb_path: str):
        """
        初始化Strategy KB检索器
        
        **设计原理**：
        - **混合检索**：结合向量检索（语义相似度）和关键词检索（精确匹配）
        - **降级策略**：向量数据库不可用时自动降级到关键词检索
        - **多语言支持**：使用多语言embedding模型，支持中英文混合查询
        
        **为什么这样设计**：
        1. **检索质量**：向量检索捕获语义相似度，关键词检索捕获精确匹配
        2. **容错性**：向量数据库不可用时仍能工作（功能可能受限）
        3. **灵活性**：支持中英文混合查询，适应不同场景
        
        **替代方案对比**：
        - **方案A：仅向量检索**
          - 优点：语义理解好
          - 缺点：精确匹配差，需要向量数据库
        - **方案B：仅关键词检索**
          - 优点：简单，无需向量数据库
          - 缺点：语义理解差
        - **当前方案：混合检索+降级**
          - 优点：兼顾语义和精确匹配，容错性好
          - 缺点：实现稍复杂
        """
        self.kb_path = Path(kb_path)
        # 设计原理：使用多语言embedding模型
        # 原因：Strategy KB包含中英文内容，需要支持中英文混合查询
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.vectorstore = None
        self._load_vectorstore()
    
    def _load_vectorstore(self):
        """
        加载向量数据库
        
        **设计原理**：延迟加载，失败时降级
        **原因**：向量数据库可能不存在或加载失败，不应阻塞初始化
        """
        persist_directory = self.kb_path / "vectorstore"
        if persist_directory.exists():
            self.vectorstore = Chroma(
                persist_directory=str(persist_directory),
                embedding_function=self.embeddings
            )
        else:
            logger.warning("向量数据库不存在，将使用关键词检索")
    
    def retrieve_research_cards(
        self,
        query: str,
        mainline: str = None,
        factor_candidates: List[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        检索研究卡
        
        **设计原理**：
        - **查询增强**：将主线、因子等信息合并到查询文本，提高检索精度
        - **向量优先**：优先使用向量检索，失败时降级到关键词检索
        - **结果排序**：按相似度分数排序，返回Top-K结果
        
        **为什么这样设计**：
        1. **上下文增强**：主线、因子等信息提供额外上下文，提高检索精度
        2. **容错性**：向量检索失败时自动降级，保证系统可用性
        3. **效率**：Top-K结果避免返回过多无关结果
        
        **使用场景**：
        - 根据投资主线和因子推荐相关策略研究卡
        - 策略生成时检索相似策略案例
        - 策略优化时检索相关优化方法
        
        Args:
            query: 查询文本
            mainline: 投资主线（可选）
            factor_candidates: 因子候选列表（可选）
            top_k: 返回前K个结果
        
        Returns:
            List[Dict]: 研究卡列表，每个包含title, content, score, file_path等
        """
        # 构建查询文本
        query_text = query
        if mainline:
            query_text += f" 投资主线: {mainline}"
        if factor_candidates:
            query_text += f" 因子: {', '.join(factor_candidates)}"
        
        # 向量检索
        if self.vectorstore:
            results = self.vectorstore.similarity_search_with_score(
                query_text,
                k=top_k
            )
            
            cards = []
            for doc, score in results:
                cards.append({
                    'title': doc.metadata.get('title', ''),
                    'content': doc.page_content,
                    'score': float(score),
                    'file_path': doc.metadata.get('file_path', ''),
                    'card_id': doc.metadata.get('card_id', ''),
                    'strategy_type': doc.metadata.get('strategy_type', ''),
                    'factors': doc.metadata.get('factors', [])
                })
            
            return cards
        else:
            # 降级到关键词检索
            return self._keyword_search(query_text, top_k)
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """关键词检索（降级方案）"""
        cards_dir = self.kb_path / "cards"
        if not cards_dir.exists():
            return []
        
        # 简单的关键词匹配
        query_words = set(query.lower().split())
        results = []
        
        for card_file in cards_dir.rglob("*.md"):
            try:
                with open(card_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_lower = content.lower()
                    
                    # 计算匹配度
                    matches = sum(1 for word in query_words if word in content_lower)
                    score = matches / len(query_words) if query_words else 0
                    
                    if score > 0:
                        # 解析frontmatter
                        frontmatter = self._parse_frontmatter(content)
                        results.append({
                            'title': frontmatter.get('title', card_file.stem),
                            'content': content[:500],  # 截取前500字符
                            'score': score,
                            'file_path': str(card_file),
                            'card_id': frontmatter.get('card_id', ''),
                            'strategy_type': frontmatter.get('strategy_type', ''),
                            'factors': frontmatter.get('factors', [])
                        })
            except Exception as e:
                logger.warning(f"读取研究卡失败 {card_file}: {e}")
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """解析Markdown frontmatter"""
        import yaml
        
        if not content.startswith('---'):
            return {}
        
        try:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                return frontmatter or {}
        except Exception as e:
            logger.warning(f"解析frontmatter失败: {e}")
        
        return {}
```

#### BM25检索

```python
from rank_bm25 import BM25Okapi
import jieba

class BM25Retriever:
    """BM25关键词检索器"""
    
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.corpus = []
        self.metadata = []
        self.bm25 = None
        self._build_index()
    
    def _build_index(self):
        """构建BM25索引"""
        cards_dir = self.kb_path / "cards"
        if not cards_dir.exists():
            return
        
        for card_file in cards_dir.rglob("*.md"):
            try:
                with open(card_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 解析frontmatter
                    frontmatter = self._parse_frontmatter(content)
                    
                    # 提取文本内容
                    text = self._extract_text(content)
                    
                    # 分词
                    tokens = list(jieba.cut(text))
                    
                    self.corpus.append(tokens)
                    self.metadata.append({
                        'file_path': str(card_file),
                        'title': frontmatter.get('title', card_file.stem),
                        'content': text[:500],
                        'card_id': frontmatter.get('card_id', ''),
                        'strategy_type': frontmatter.get('strategy_type', ''),
                        'factors': frontmatter.get('factors', [])
                    })
            except Exception as e:
                logger.warning(f"处理研究卡失败 {card_file}: {e}")
        
        if self.corpus:
            self.bm25 = BM25Okapi(self.corpus)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """BM25搜索"""
        if not self.bm25:
            return []
        
        # 查询分词
        query_tokens = list(jieba.cut(query))
        
        # 计算分数
        scores = self.bm25.get_scores(query_tokens)
        
        # 获取Top-K
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                result = self.metadata[idx].copy()
                result['score'] = float(scores[idx])
                results.append(result)
        
        return results
```

### 规则检索

```python
import yaml
from pathlib import Path
from typing import Dict, List, Any

class RuleRetriever:
    """规则检索器"""
    
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.rules_dir = self.kb_path / "rules"
        self.rules_cache = {}
        self._load_rules()
    
    def _load_rules(self):
        """加载所有规则文件"""
        if not self.rules_dir.exists():
            return
        
        rule_files = {
            'strategy_constraints': 'strategy_constraints.yml',
            'data_rules': 'data_rules.yml',
            'risk_model': 'risk_model.yml',
            'cost_model': 'cost_model.yml',
            'universe_rules': 'universe_rules.yml'
        }
        
        for key, filename in rule_files.items():
            rule_file = self.rules_dir / filename
            if rule_file.exists():
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        self.rules_cache[key] = yaml.safe_load(f)
                except Exception as e:
                    logger.warning(f"加载规则文件失败 {rule_file}: {e}")
    
    def get_rules(
        self,
        rule_type: str = None
    ) -> Dict[str, Any]:
        """
        获取规则
        
        Args:
            rule_type: 规则类型（strategy_constraints/data_rules/risk_model/cost_model/universe_rules）
        
        Returns:
            Dict: 规则字典
        """
        if rule_type:
            return self.rules_cache.get(rule_type, {})
        else:
            return self.rules_cache.copy()
    
    def get_relevant_rules(
        self,
        strategy_type: str = None,
        factors: List[str] = None
    ) -> Dict[str, Any]:
        """
        获取相关规则
        
        Args:
            strategy_type: 策略类型
            factors: 使用的因子列表
        
        Returns:
            Dict: 相关规则字典
        """
        relevant_rules = {}
        
        # 策略约束规则
        constraints = self.rules_cache.get('strategy_constraints', {})
        if strategy_type and strategy_type in constraints.get('strategy_types', {}):
            relevant_rules['constraints'] = constraints['strategy_types'][strategy_type]
        else:
            relevant_rules['constraints'] = constraints.get('default', {})
        
        # 风险模型
        relevant_rules['risk_model'] = self.rules_cache.get('risk_model', {})
        
        # 成本模型
        relevant_rules['cost_model'] = self.rules_cache.get('cost_model', {})
        
        # 数据规则
        relevant_rules['data_rules'] = self.rules_cache.get('data_rules', {})
        
        # 可交易池规则
        relevant_rules['universe_rules'] = self.rules_cache.get('universe_rules', {})
        
        return relevant_rules
```

### 多阶段检索

```python
class MultiStageRetriever:
    """多阶段检索器（BM25 + 向量 + Reranker）"""
    
    def __init__(self, kb_path: str):
        self.bm25_retriever = BM25Retriever(kb_path)
        self.vector_retriever = StrategyKBRetriever(kb_path)
    
    def retrieve(
        self,
        query: str,
        mainline: str = None,
        factor_candidates: List[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        多阶段检索
        
        Args:
            query: 查询文本
            mainline: 投资主线
            factor_candidates: 因子候选列表
            top_k: 返回前K个结果
        
        Returns:
            List[Dict]: 检索结果列表
        """
        # 第一阶段：BM25关键词检索（召回更多候选）
        bm25_results = self.bm25_retriever.search(query, top_k=top_k * 2)
        
        # 第二阶段：向量检索（语义相似）
        vector_results = self.vector_retriever.retrieve_research_cards(
            query, mainline, factor_candidates, top_k=top_k * 2
        )
        
        # 合并结果
        combined = {}
        for result in bm25_results + vector_results:
            card_id = result.get('card_id') or result.get('file_path', '')
            if card_id not in combined:
                combined[card_id] = result
            else:
                # 合并分数（加权平均）
                existing = combined[card_id]
                existing['score'] = (existing['score'] * 0.4 + result['score'] * 0.6)
        
        # 第三阶段：Rerank（按分数排序）
        final_results = sorted(
            combined.values(),
            key=lambda x: x['score'],
            reverse=True
        )[:top_k]
        
        return final_results
```

<h2 id="section-7-2-2">✅ 7.2.2 规则验证</h2>

规则验证确保生成的策略符合Strategy KB的硬约束条件。

### 策略约束验证

```python
class StrategyConstraintValidator:
    """策略约束验证器"""
    
    def __init__(self, rules: Dict[str, Any]):
        self.constraints = rules.get('constraints', {})
    
    def validate(
        self,
        strategy_draft: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        验证策略约束
        
        Args:
            strategy_draft: 策略草案
        
        Returns:
            Tuple[bool, List[str]]: (是否通过, 错误列表)
        """
        errors = []
        
        # 验证必需字段
        required_fields = ['universe', 'entry', 'exit', 'position_sizing', 'risk']
        for field in required_fields:
            if field not in strategy_draft:
                errors.append(f"缺少必需字段: {field}")
        
        # 验证股票池
        if 'universe' in strategy_draft:
            universe = strategy_draft['universe']
            if not isinstance(universe, (list, str)):
                errors.append("universe必须是列表或字符串")
            elif isinstance(universe, list) and len(universe) == 0:
                errors.append("universe不能为空")
        
        # 验证仓位配置
        if 'position_sizing' in strategy_draft:
            position_sizing = strategy_draft['position_sizing']
            max_position = position_sizing.get('max_position', 1.0)
            if max_position > self.constraints.get('max_position_limit', 0.2):
                errors.append(
                    f"单票最大仓位 {max_position} 超过限制 "
                    f"{self.constraints.get('max_position_limit', 0.2)}"
                )
        
        # 验证持仓数量
        if 'position_sizing' in strategy_draft:
            max_stocks = strategy_draft['position_sizing'].get('max_stocks', 0)
            if max_stocks > self.constraints.get('max_stocks_limit', 50):
                errors.append(
                    f"最大持仓数 {max_stocks} 超过限制 "
                    f"{self.constraints.get('max_stocks_limit', 50)}"
                )
        
        return len(errors) == 0, errors
```

### 风险模型验证

```python
class RiskModelValidator:
    """风险模型验证器"""
    
    def __init__(self, risk_model: Dict[str, Any]):
        self.risk_model = risk_model
    
    def validate(
        self,
        strategy_draft: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        验证风险模型
        
        Args:
            strategy_draft: 策略草案
        
        Returns:
            Tuple[bool, List[str]]: (是否通过, 错误列表)
        """
        errors = []
        
        if 'risk' not in strategy_draft:
            return True, []  # 风险配置可选
        
        risk_config = strategy_draft['risk']
        
        # 验证止损配置
        if 'stop_loss' in risk_config:
            stop_loss = risk_config['stop_loss']
            max_stop_loss = self.risk_model.get('max_stop_loss', 0.15)
            if stop_loss > max_stop_loss:
                errors.append(
                    f"止损线 {stop_loss} 超过限制 {max_stop_loss}"
                )
        
        # 验证最大回撤限制
        if 'max_drawdown' in risk_config:
            max_drawdown = risk_config['max_drawdown']
            max_drawdown_limit = self.risk_model.get('max_drawdown_limit', 0.30)
            if max_drawdown > max_drawdown_limit:
                errors.append(
                    f"最大回撤限制 {max_drawdown} 超过限制 {max_drawdown_limit}"
                )
        
        # 验证杠杆比例
        if 'leverage' in risk_config:
            leverage = risk_config['leverage']
            max_leverage = self.risk_model.get('max_leverage', 1.0)
            if leverage > max_leverage:
                errors.append(
                    f"杠杆比例 {leverage} 超过限制 {max_leverage}"
                )
        
        return len(errors) == 0, errors
```

### 成本模型验证

```python
class CostModelValidator:
    """成本模型验证器"""
    
    def __init__(self, cost_model: Dict[str, Any]):
        self.cost_model = cost_model
    
    def validate(
        self,
        strategy_draft: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        验证成本模型
        
        Args:
            strategy_draft: 策略草案
        
        Returns:
            Tuple[bool, List[str]]: (是否通过, 错误列表)
        """
        errors = []
        
        if 'cost' not in strategy_draft:
            return True, []  # 成本配置可选
        
        cost_config = strategy_draft['cost']
        
        # 验证手续费率
        if 'commission_rate' in cost_config:
            commission_rate = cost_config['commission_rate']
            max_commission = self.cost_model.get('max_commission_rate', 0.003)
            if commission_rate > max_commission:
                errors.append(
                    f"手续费率 {commission_rate} 超过限制 {max_commission}"
                )
        
        # 验证滑点
        if 'slippage' in cost_config:
            slippage = cost_config['slippage']
            max_slippage = self.cost_model.get('max_slippage', 0.005)
            if slippage > max_slippage:
                errors.append(
                    f"滑点 {slippage} 超过限制 {max_slippage}"
                )
        
        return len(errors) == 0, errors
```

### 综合验证

```python
class StrategyValidator:
    """策略综合验证器"""
    
    def __init__(self, rules: Dict[str, Any]):
        self.constraint_validator = StrategyConstraintValidator(rules)
        self.risk_validator = RiskModelValidator(rules.get('risk_model', {}))
        self.cost_validator = CostModelValidator(rules.get('cost_model', {}))
    
    def validate(
        self,
        strategy_draft: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        综合验证策略草案
        
        Args:
            strategy_draft: 策略草案
        
        Returns:
            Dict: 验证结果，包含valid, errors, warnings等
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # 约束验证
        constraint_valid, constraint_errors = self.constraint_validator.validate(strategy_draft)
        if not constraint_valid:
            result['valid'] = False
            result['errors'].extend(constraint_errors)
        
        # 风险模型验证
        risk_valid, risk_errors = self.risk_validator.validate(strategy_draft)
        if not risk_valid:
            result['valid'] = False
            result['errors'].extend(risk_errors)
        
        # 成本模型验证
        cost_valid, cost_errors = self.cost_validator.validate(strategy_draft)
        if not cost_valid:
            result['valid'] = False
            result['errors'].extend(cost_errors)
        
        return result
```

<h2 id="section-7-2-3">📝 7.2.3 策略草案生成</h2>

策略草案生成基于检索到的研究卡和规则，生成结构化的策略定义。

### 策略结构定义

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class StrategyDraft:
    """策略草案定义"""
    
    # 基本信息
    name: str                          # 策略名称
    description: str = ""               # 策略描述
    strategy_type: str = ""             # 策略类型
    platform: str = "ptrade"           # 目标平台
    
    # 股票池
    universe: List[str] = field(default_factory=list)  # 股票池
    
    # 选股逻辑
    entry: Dict[str, Any] = field(default_factory=dict)  # 买入条件
    exit: Dict[str, Any] = field(default_factory=dict)   # 卖出条件
    
    # 仓位管理
    position_sizing: Dict[str, Any] = field(default_factory=dict)  # 仓位配置
    
    # 风险控制
    risk: Dict[str, Any] = field(default_factory=dict)  # 风控配置
    
    # 成本配置
    cost: Dict[str, Any] = field(default_factory=dict)  # 成本配置
    
    # 因子配置
    factors: List[str] = field(default_factory=list)  # 使用的因子列表
    factor_weights: Dict[str, float] = field(default_factory=dict)  # 因子权重
    
    # 引用信息
    research_card_refs: List[str] = field(default_factory=list)  # 研究卡引用
    rule_refs: List[str] = field(default_factory=list)  # 规则引用
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'description': self.description,
            'strategy_type': self.strategy_type,
            'platform': self.platform,
            'universe': self.universe,
            'entry': self.entry,
            'exit': self.exit,
            'position_sizing': self.position_sizing,
            'risk': self.risk,
            'cost': self.cost,
            'factors': self.factors,
            'factor_weights': self.factor_weights,
            'research_card_refs': self.research_card_refs,
            'rule_refs': self.rule_refs,
            'created_at': self.created_at,
            'version': self.version
        }
```

### 策略草案生成器

```python
class StrategyDraftGenerator:
    """策略草案生成器"""
    
    def __init__(self, retriever: MultiStageRetriever, rule_retriever: RuleRetriever):
        self.retriever = retriever
        self.rule_retriever = rule_retriever
    
    def generate(
        self,
        mainline: str,
        candidate_pool: List[str],
        factor_candidates: List[str],
        platform: str = "ptrade"
    ) -> StrategyDraft:
        """
        生成策略草案
        
        Args:
            mainline: 投资主线
            candidate_pool: 候选股票池
            factor_candidates: 因子候选列表
            platform: 目标平台
        
        Returns:
            StrategyDraft: 策略草案对象
        """
        # 1. 检索研究卡
        query = f"{mainline} {' '.join(factor_candidates)}"
        research_cards = self.retriever.retrieve(
            query, mainline, factor_candidates, top_k=5
        )
        
        # 2. 检索规则
        rules = self.rule_retriever.get_relevant_rules(
            strategy_type=self._infer_strategy_type(research_cards),
            factors=factor_candidates
        )
        
        # 3. 生成策略草案
        draft = StrategyDraft(
            name=f"{mainline}_策略_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=f"基于投资主线'{mainline}'生成的策略",
            strategy_type=self._infer_strategy_type(research_cards),
            platform=platform,
            universe=candidate_pool,
            factors=factor_candidates,
            research_card_refs=[card.get('card_id', '') for card in research_cards],
            rule_refs=list(rules.keys())
        )
        
        # 4. 从研究卡提取策略逻辑
        self._extract_strategy_logic(draft, research_cards)
        
        # 5. 应用规则约束
        self._apply_rule_constraints(draft, rules)
        
        # 6. 配置因子权重
        self._configure_factor_weights(draft, research_cards)
        
        return draft
    
    def _infer_strategy_type(self, research_cards: List[Dict]) -> str:
        """推断策略类型"""
        if not research_cards:
            return "multi_factor"
        
        # 统计策略类型
        type_counts = {}
        for card in research_cards:
            strategy_type = card.get('strategy_type', '')
            if strategy_type:
                type_counts[strategy_type] = type_counts.get(strategy_type, 0) + 1
        
        if type_counts:
            return max(type_counts.items(), key=lambda x: x[1])[0]
        
        return "multi_factor"
    
    def _extract_strategy_logic(
        self,
        draft: StrategyDraft,
        research_cards: List[Dict]
    ):
        """从研究卡提取策略逻辑"""
        if not research_cards:
            return
        
        # 使用第一个研究卡作为主要参考
        primary_card = research_cards[0]
        
        # 提取买入条件
        draft.entry = {
            'type': 'factor_based',
            'factors': draft.factors,
            'method': 'top_n',
            'top_n': 10
        }
        
        # 提取卖出条件
        draft.exit = {
            'stop_loss': 0.08,
            'take_profit': 0.20,
            'time_based': False
        }
        
        # 从研究卡内容中提取更多信息
        content = primary_card.get('content', '')
        if '止损' in content or 'stop_loss' in content.lower():
            # 尝试提取止损值
            import re
            stop_loss_match = re.search(r'止损[：:]\s*([\d.]+)', content)
            if stop_loss_match:
                draft.exit['stop_loss'] = float(stop_loss_match.group(1))
    
    def _apply_rule_constraints(
        self,
        draft: StrategyDraft,
        rules: Dict[str, Any]
    ):
        """应用规则约束"""
        constraints = rules.get('constraints', {})
        
        # 应用仓位限制
        if 'position_sizing' not in draft.position_sizing:
            draft.position_sizing = {}
        
        max_position = constraints.get('max_position_limit', 0.1)
        draft.position_sizing['max_position'] = min(
            draft.position_sizing.get('max_position', 0.1),
            max_position
        )
        
        max_stocks = constraints.get('max_stocks_limit', 50)
        draft.position_sizing['max_stocks'] = min(
            draft.position_sizing.get('max_stocks', 10),
            max_stocks
        )
        
        # 应用风险限制
        risk_model = rules.get('risk_model', {})
        if 'risk' not in draft.risk:
            draft.risk = {}
        
        max_stop_loss = risk_model.get('max_stop_loss', 0.15)
        if 'stop_loss' in draft.exit:
            draft.exit['stop_loss'] = min(
                draft.exit['stop_loss'],
                max_stop_loss
            )
    
    def _configure_factor_weights(
        self,
        draft: StrategyDraft,
        research_cards: List[Dict]
    ):
        """配置因子权重"""
        if not draft.factors:
            return
        
        # 默认等权
        default_weight = 1.0 / len(draft.factors)
        draft.factor_weights = {
            factor: default_weight for factor in draft.factors
        }
        
        # 从研究卡中提取权重信息
        for card in research_cards:
            factors = card.get('factors', [])
            if factors:
                # 如果有权重信息，使用它
                for factor in draft.factors:
                    if factor in factors:
                        # 可以根据研究卡的重要性调整权重
                        draft.factor_weights[factor] = default_weight * 1.2
```

<h2 id="section-7-2-4">🐍 7.2.4 Python代码生成</h2>

Python代码生成将策略草案转换为可执行的Python策略代码。

### 代码生成器

```python
from core.strategy_template import StrategyTemplate, TemplateLibrary

class PythonCodeGenerator:
    """Python代码生成器"""
    
    def __init__(self, template_library: TemplateLibrary):
        self.template_library = template_library
    
    def generate(
        self,
        strategy_draft: StrategyDraft,
        template_name: str = None
    ) -> str:
        """
        生成Python策略代码
        
        Args:
            strategy_draft: 策略草案
            template_name: 模板名称（可选，自动选择）
        
        Returns:
            str: 生成的Python代码
        """
        # 1. 选择模板
        template = self._select_template(strategy_draft, template_name)
        
        # 2. 准备参数
        parameters = self._prepare_parameters(strategy_draft)
        
        # 3. 生成代码
        code = self._generate_code(template, parameters, strategy_draft)
        
        return code
    
    def _select_template(
        self,
        strategy_draft: StrategyDraft,
        template_name: str = None
    ) -> StrategyTemplate:
        """选择策略模板"""
        if template_name:
            template = self.template_library.get_template(template_name)
            if template:
                return template
        
        # 根据策略类型自动选择
        strategy_type = strategy_draft.strategy_type
        platform = strategy_draft.platform
        
        # 查找匹配的模板
        templates = self.template_library.list_templates(
            platform=PlatformType(platform),
            template_type=TemplateType(strategy_type)
        )
        
        if templates:
            return templates[0]
        
        # 默认使用多因子模板
        return self.template_library.get_template("multi_factor_ptrade")
    
    def _prepare_parameters(self, strategy_draft: StrategyDraft) -> Dict[str, Any]:
        """准备模板参数"""
        return {
            'strategy_name': strategy_draft.name,
            'description': strategy_draft.description,
            'author': 'TRQuant',
            'max_position': strategy_draft.position_sizing.get('max_position', 0.1),
            'stop_loss': strategy_draft.exit.get('stop_loss', 0.08),
            'take_profit': strategy_draft.exit.get('take_profit', 0.2),
            'max_stocks': strategy_draft.position_sizing.get('max_stocks', 10),
            'rebalance_days': strategy_draft.position_sizing.get('rebalance_days', 20),
            'factors': strategy_draft.factors,
            'factor_weights': strategy_draft.factor_weights
        }
    
    def _generate_code(
        self,
        template: StrategyTemplate,
        parameters: Dict[str, Any],
        strategy_draft: StrategyDraft
    ) -> str:
        """生成代码"""
        # 实例化模板
        code = instantiate_template(template, parameters)
        
        # 添加引用注释
        if strategy_draft.research_card_refs:
            ref_comment = "\n# 引用研究卡:\n"
            for ref in strategy_draft.research_card_refs:
                ref_comment += f"# - {ref}\n"
            code = code.replace(
                '"""',
                f'"""\n{ref_comment}',
                1
            )
        
        return code
```

<h2 id="section-7-2-5">💾 7.2.5 文件保存与版本管理</h2>

文件保存与版本管理确保生成的策略代码被正确保存和管理。

### 文件保存

```python
from pathlib import Path
import json
from datetime import datetime

class StrategyFileManager:
    """策略文件管理器"""
    
    def __init__(self, strategies_dir: str = "strategies/generated"):
        self.strategies_dir = Path(strategies_dir)
        self.strategies_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_dir = self.strategies_dir / ".metadata"
        self.metadata_dir.mkdir(exist_ok=True)
    
    def save_strategy(
        self,
        strategy_draft: StrategyDraft,
        code: str,
        platform: str = "ptrade"
    ) -> Dict[str, str]:
        """
        保存策略文件
        
        Args:
            strategy_draft: 策略草案
            code: 策略代码
            platform: 平台类型
        
        Returns:
            Dict: 保存结果，包含file_path, metadata_path等
        """
        # 生成文件名
        safe_name = self._sanitize_filename(strategy_draft.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.py"
        
        # 保存代码文件
        file_path = self.strategies_dir / platform / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 保存元数据
        metadata = {
            'strategy_draft': strategy_draft.to_dict(),
            'file_path': str(file_path),
            'platform': platform,
            'created_at': datetime.now().isoformat(),
            'version': strategy_draft.version
        }
        
        metadata_path = self.metadata_dir / f"{safe_name}_{timestamp}.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {
            'file_path': str(file_path),
            'metadata_path': str(metadata_path),
            'strategy_name': strategy_draft.name,
            'version': strategy_draft.version
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        import re
        # 移除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename
```

<h2 id="section-7-2-6">🔄 7.2.6 工作流集成</h2>

工作流集成将策略生成器集成到完整的投资工作流中。

### 工作流调用

```python
def workflow_strategy_generate_candidate(
    mainline: str,
    candidate_pool: List[str],
    factor_candidates: List[str],
    platform: str = "ptrade",
    mode: str = "execute"  # "dry_run" or "execute"
) -> Dict[str, Any]:
    """
    工作流策略生成工具
    
    Args:
        mainline: 投资主线
        candidate_pool: 候选股票池
        factor_candidates: 因子候选列表
        platform: 目标平台
        mode: 执行模式（dry_run预览或execute执行）
    
    Returns:
        Dict: 生成结果，包含strategy_draft, python_code, file_path等
    """
    try:
        # 1. 初始化组件
        kb_path = "docs/strategy_kb"
        retriever = MultiStageRetriever(kb_path)
        rule_retriever = RuleRetriever(kb_path)
        draft_generator = StrategyDraftGenerator(retriever, rule_retriever)
        template_library = TemplateLibrary("templates/strategies")
        code_generator = PythonCodeGenerator(template_library)
        file_manager = StrategyFileManager()
        validator = StrategyValidator(rule_retriever.get_relevant_rules())
        
        # 2. 生成策略草案
        strategy_draft = draft_generator.generate(
            mainline, candidate_pool, factor_candidates, platform
        )
        
        # 3. 验证策略草案
        validation_result = validator.validate(strategy_draft.to_dict())
        
        if not validation_result['valid']:
            return {
                'success': False,
                'errors': validation_result['errors'],
                'strategy_draft': strategy_draft.to_dict()
            }
        
        # 4. 生成Python代码
        python_code = code_generator.generate(strategy_draft)
        
        # 5. 保存文件（如果不是dry_run模式）
        if mode == "execute":
            save_result = file_manager.save_strategy(
                strategy_draft, python_code, platform
            )
        else:
            save_result = {
                'file_path': None,
                'metadata_path': None,
                'mode': 'dry_run'
            }
        
        return {
            'success': True,
            'strategy_draft': strategy_draft.to_dict(),
            'python_code': python_code,
            'validation_result': validation_result,
            'file_path': save_result.get('file_path'),
            'metadata_path': save_result.get('metadata_path'),
            'research_card_refs': strategy_draft.research_card_refs,
            'rule_refs': strategy_draft.rule_refs
        }
    
    except Exception as e:
        logger.error(f"策略生成失败: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }
```

## 🔗 相关章节

- **7.1 策略模板**：了解策略模板系统，为策略生成提供模板支撑
- **7.3 策略优化**：了解策略优化，对生成的策略进行优化
- **7.4 策略规范化**：了解策略规范化，确保生成的代码符合规范
- **第4章：投资主线识别**：了解投资主线识别，为策略生成提供主线信息
- **第5章：候选池构建**：了解候选池构建，为策略生成提供候选股票池
- **第6章：因子库**：了解因子库，为策略生成提供因子数据

## 💡 关键要点

1. **知识驱动**：基于Strategy KB的研究卡和规则生成策略
2. **规则约束**：所有生成的策略必须通过规则验证
3. **可追溯性**：生成的策略包含完整的研究卡和规则引用
4. **自动化**：从投资主线到策略代码的完全自动化
5. **多阶段检索**：BM25 + 向量检索 + Reranker确保检索质量

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了TRQuant系统的策略生成器，通过Strategy KB和Workflow Server实现从投资主线到可执行策略代码的自动化生成。通过理解Strategy KB检索、规则验证、策略草案生成和Python代码生成的核心技术，帮助开发者掌握如何自动生成策略代码，为策略开发提供完整的自动化能力。</p>
  
  <h3>下节预告</h3>
  <p>掌握了策略生成后，下一节将介绍策略优化，包括参数调优、因子权重优化、风控参数优化和策略逻辑优化。通过理解策略优化的核心技术，帮助开发者掌握如何对生成的策略进行优化，提高策略性能。</p>
  
  <a href="/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN" class="next-section">
    继续学习：7.3 策略优化 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
