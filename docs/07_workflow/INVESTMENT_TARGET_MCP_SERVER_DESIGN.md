# 投资标的筛选与报告生成 MCP Server 设计文档

> **创建时间**: 2026-01-06  
> **版本**: v1.0  
> **目的**: 统一投资标的筛选和个股分析报告生成功能，整合到单一MCP Server

---

## 📋 目录

1. [现有功能分析](#1-现有功能分析)
2. [设计目标](#2-设计目标)
3. [统一架构设计](#3-统一架构设计)
4. [MCP Server实现](#4-mcp-server实现)
5. [代码复用策略](#5-代码复用策略)
6. [验证方案](#6-验证方案)

---

## 1. 现有功能分析

### 1.1 现有MCP Server功能

#### ✅ 已存在的功能

**1. 候选池构建** (`data_source_server_v2.py`, `trquant_core_server.py`)
- `data_source.candidate_pool` - 基于投资主线构建候选股票池
- `data.candidate_pool` - 候选池构建（trquant_core_server）
- 使用 `CandidatePoolBuilder` 从主线构建候选池
- 支持分层候选池（L0-L3）

**2. 十倍股筛选** (`utils/tenbagger_multifactor_tools.py`)
- `tenbagger.multifactor.scan` - 扫描科技主线股票并进行多因子打分
- `tenbagger.multifactor.score` - 单股评分
- `tenbagger.multifactor.stage` - 识别成长阶段(S0-S5)
- `tenbagger.multifactor.backtest` - 回测
- `tenbagger.multifactor.report` - 生成报告

**3. 报告生成** (`report_server.py`)
- `report.generate` - 生成回测报告（HTML/PDF/Markdown/JSON）
- `report.compare` - 策略对比报告
- `report.diagnosis` - 策略诊断报告
- ⚠️ **注意**: 主要是回测报告，不是个股分析报告

**4. 工作流集成** (`workflow_9steps_server.py`)
- 完整的9步工作流，包括候选池构建
- 步骤4: 候选池构建 → `data_source.candidate_pool`

### 1.2 现有实现文件（ope项目）

**筛选相关**:
- `research/short_mid_term_signal_selector/tenbagger_deep_analysis.py` - 十倍股深度分析
- `research/short_mid_term_signal_selector/tenbagger_mainline_screener.py` - 主线题材筛选
- `research/short_mid_term_signal_selector/tenbagger_early_screener.py` - 早期识别筛选
- `research/short_mid_term_signal_selector/tech_growth_screener.py` - 科技高成长筛选

**报告生成相关**:
- `scripts/reports/junsheng_full_analysis_report.py` - 均胜电子分析报告
- `scripts/reports/guosheng_full_analysis_report.py` - 国晟科技分析报告
- 生成多Tab HTML报告（综述、行情、历史验证、财务、事件、对比、年报要点）

### 1.3 路径设置检查

✅ **所有MCP Server路径设置正确**:
- `trquant_core_server.py`: `Path(__file__).parent.parent` → ope项目根目录
- `data_source_server_v2.py`: `Path(__file__).parent.parent` → ope项目根目录
- `workflow_9steps_server.py`: `Path(__file__).parent.parent` → ope项目根目录
- `tenbagger_multifactor_tools.py`: `Path(__file__).parent.parent.parent` → ope项目根目录

### 1.4 缺失的功能

❌ **需要统一的功能**:
1. **统一的筛选接口**: 整合十倍股、主线题材、用户指定、科技高成长等策略
2. **个股深度分析报告**: 类似 `junsheng_full_analysis_report.py` 的功能，但通过MCP调用
3. **批量分析**: 支持批量分析多只股票
4. **报告生成统一接口**: 整合现有的报告生成逻辑

---

## 2. 设计目标

### 2.1 核心目标

1. **统一接口**: 一个MCP Server提供所有投资标的筛选和分析功能
2. **复用现有代码**: 不重复实现，封装现有逻辑
3. **支持多种策略**: 十倍股、主线题材、用户指定、科技高成长
4. **统一报告格式**: 多Tab HTML报告，包含完整分析
5. **易于扩展**: 方便添加新的筛选策略

### 2.2 功能范围

**筛选功能**:
- 十倍股早期识别筛选
- 主线题材股筛选（脑机接口、固态电池、AI等）
- 用户指定股票筛选
- 科技高成长筛选

**分析功能**:
- 单股深度分析（财务、技术、估值、风险）
- 批量分析
- 历史验证（多周期收益、回撤、波动）
- 同概念对比

**报告功能**:
- 生成多Tab HTML分析报告
- 支持不同报告类型（full/summary/financial/technical）
- 包含年报要点、公告事件、技术分析等

---

## 3. 统一架构设计

### 3.1 架构图

```
┌─────────────────────────────────────────────────────────┐
│         investment_target_server.py (MCP Server)        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MCP Tools:                                        │  │
│  │  - investment.screen      (筛选)                   │  │
│  │  - investment.analyze    (分析)                   │  │
│  │  - investment.report     (报告)                   │  │
│  │  - investment.batch_analyze (批量)                │  │
│  │  - investment.list_strategies (策略列表)          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│      core/investment_target_analyzer.py (统一分析器)     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - _init_data_sources()  (JQData, CNINFO)        │  │
│  │  - _init_strategies()    (初始化筛选策略)         │  │
│  │  - screen()              (统一筛选接口)          │  │
│  │  - analyze()             (统一分析接口)          │  │
│  │  - generate_report()     (统一报告生成)           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              现有实现（复用，不修改）                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - TenbaggerDeepAnalyzer                          │  │
│  │  - MainlineScreener                               │  │
│  │  - TechGrowthScreener                             │  │
│  │  - junsheng_full_analysis_report.py (报告模板)    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 3.2 文件结构

```
mcp_servers/
├── investment_target_server.py      # MCP Server主文件（新建）
└── utils/
    └── investment_target_analyzer.py  # 统一分析器（新建）

core/
└── investment_target_analyzer.py    # 或者放在core目录（新建）

research/short_mid_term_signal_selector/
├── tenbagger_deep_analysis.py      # 保留：十倍股分析
├── tenbagger_mainline_screener.py  # 保留：主线筛选
├── tenbagger_early_screener.py     # 保留：早期识别
└── tech_growth_screener.py         # 保留：科技高成长

scripts/reports/
├── junsheng_full_analysis_report.py  # 保留：报告模板
└── guosheng_full_analysis_report.py # 保留：报告模板
```

---

## 4. MCP Server实现

### 4.1 工具定义

```python
# mcp_servers/investment_target_server.py

TOOLS = [
    Tool(
        name="investment.screen",
        description="筛选投资标的（支持多种策略：十倍股、主线题材、用户指定、科技高成长）",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {
                    "type": "string",
                    "enum": ["tenbagger_early", "mainline_theme", "user_specified", "tech_growth"],
                    "description": "筛选策略类型"
                },
                "date": {
                    "type": "string",
                    "description": "分析日期 (YYYY-MM-DD)，默认最近交易日"
                },
                "top_n": {
                    "type": "integer",
                    "default": 10,
                    "description": "返回Top N股票"
                },
                "min_score": {
                    "type": "number",
                    "default": 60.0,
                    "description": "最低得分阈值"
                },
                "mainline_sectors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "主线板块列表（用于mainline_theme策略）"
                },
                "stock_codes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表（用于user_specified策略）"
                },
                "custom_params": {
                    "type": "object",
                    "description": "自定义策略参数"
                }
            },
            "required": ["strategy"]
        }
    ),
    Tool(
        name="investment.analyze",
        description="深度分析单只股票（财务、技术、估值、风险等）",
        inputSchema={
            "type": "object",
            "properties": {
                "stock_code": {
                    "type": "string",
                    "description": "股票代码（如 '600699.XSHG'）"
                },
                "analysis_date": {
                    "type": "string",
                    "description": "分析日期 (YYYY-MM-DD)"
                },
                "include_annual_reports": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否包含年报分析"
                },
                "include_announcements": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否包含公告分析"
                },
                "benchmark_code": {
                    "type": "string",
                    "default": "000300.XSHG",
                    "description": "基准指数代码"
                }
            },
            "required": ["stock_code"]
        }
    ),
    Tool(
        name="investment.report",
        description="生成投资标的分析报告（HTML多Tab格式）",
        inputSchema={
            "type": "object",
            "properties": {
                "stock_code": {
                    "type": "string",
                    "description": "股票代码"
                },
                "stock_name": {
                    "type": "string",
                    "description": "股票名称（可选，自动获取）"
                },
                "analysis_date": {
                    "type": "string",
                    "description": "分析日期"
                },
                "report_type": {
                    "type": "string",
                    "enum": ["full", "summary", "financial", "technical"],
                    "default": "full",
                    "description": "报告类型"
                },
                "output_dir": {
                    "type": "string",
                    "description": "输出目录，默认 output/reports"
                }
            },
            "required": ["stock_code"]
        }
    ),
    Tool(
        name="investment.batch_analyze",
        description="批量分析多只股票",
        inputSchema={
            "type": "object",
            "properties": {
                "stock_codes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "analysis_date": {
                    "type": "string",
                    "description": "分析日期"
                },
                "parallel": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否并行分析"
                }
            },
            "required": ["stock_codes"]
        }
    ),
    Tool(
        name="investment.list_strategies",
        description="列出所有可用的筛选策略及其参数说明",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
]
```

### 4.2 核心分析器实现

```python
# core/investment_target_analyzer.py

"""
投资标的分析器 - 统一封装
==========================

整合：
1. 十倍股筛选逻辑
2. 主线题材筛选逻辑
3. 个股深度分析逻辑
4. 报告生成逻辑
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class InvestmentTargetAnalyzer:
    """投资标的分析器（统一接口）"""
    
    def __init__(self):
        self._init_data_sources()
        self._init_strategies()
    
    def _init_data_sources(self):
        """初始化数据源"""
        # JQData认证
        from config.config_manager import get_config_manager
        import jqdatasdk as jq
        
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        if jq_config:
            jq.auth(jq_config['username'], jq_config['password'])
            self.jq = jq
        
        # CNINFO爬虫
        from mcp_servers.crawlers.cninfo_crawler import CninfoCrawler
        self.cninfo_crawler = CninfoCrawler()
    
    def _init_strategies(self):
        """初始化筛选策略"""
        # 十倍股早期识别
        from research.short_mid_term_signal_selector.tenbagger_deep_analysis import TenbaggerDeepAnalyzer
        self.tenbagger_analyzer = TenbaggerDeepAnalyzer()
        
        # 主线题材筛选
        from research.short_mid_term_signal_selector.tenbagger_mainline_screener import MainlineScreener
        self.mainline_screener = MainlineScreener()
        
        # 科技高成长筛选
        # from research.short_mid_term_signal_selector.tech_growth_screener import TechGrowthScreener
        # self.tech_growth_screener = TechGrowthScreener()
    
    def screen(
        self,
        strategy: str,
        date: Optional[str] = None,
        top_n: int = 10,
        min_score: float = 60.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        筛选投资标的
        
        Args:
            strategy: 筛选策略（tenbagger_early/mainline_theme/user_specified/tech_growth）
            date: 分析日期
            top_n: 返回Top N
            min_score: 最低得分
            **kwargs: 策略特定参数
        
        Returns:
            筛选结果
        """
        if strategy == "tenbagger_early":
            return self._screen_tenbagger_early(date, top_n, min_score, **kwargs)
        elif strategy == "mainline_theme":
            return self._screen_mainline_theme(date, top_n, min_score, **kwargs)
        elif strategy == "user_specified":
            return self._screen_user_specified(date, top_n, **kwargs)
        elif strategy == "tech_growth":
            return self._screen_tech_growth(date, top_n, min_score, **kwargs)
        else:
            raise ValueError(f"未知策略: {strategy}")
    
    def analyze(
        self,
        stock_code: str,
        analysis_date: Optional[str] = None,
        include_annual_reports: bool = True,
        include_announcements: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        深度分析单只股票
        
        Args:
            stock_code: 股票代码
            analysis_date: 分析日期
            include_annual_reports: 是否包含年报
            include_announcements: 是否包含公告
            **kwargs: 其他参数
        
        Returns:
            分析结果
        """
        # 复用 tenbagger_deep_analysis 的逻辑
        result = self.tenbagger_analyzer.analyze_single_stock(
            stock_code,
            analysis_date
        )
        
        # 补充年报和公告
        if include_annual_reports or include_announcements:
            # 使用CNINFO爬虫获取数据
            pass
        
        return result
    
    def generate_report(
        self,
        stock_code: str,
        stock_name: Optional[str] = None,
        analysis_date: Optional[str] = None,
        report_type: str = "full",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成分析报告
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            analysis_date: 分析日期
            report_type: 报告类型（full/summary/financial/technical）
            output_dir: 输出目录
        
        Returns:
            报告信息（包含路径）
        """
        # 复用现有的报告生成逻辑
        # 参考 junsheng_full_analysis_report.py 的结构
        
        # 1. 获取分析数据
        analysis_result = self.analyze(
            stock_code,
            analysis_date,
            include_annual_reports=True,
            include_announcements=True
        )
        
        # 2. 生成HTML报告
        # 使用统一的报告生成器
        
        return {
            "stock_code": stock_code,
            "stock_name": stock_name or analysis_result.get('basic_info', {}).get('name', ''),
            "report_path": "...",
            "report_type": report_type,
            "generated_at": "..."
        }
    
    # 私有方法：各种筛选策略的实现
    def _screen_tenbagger_early(self, date, top_n, min_score, **kwargs):
        """十倍股早期识别筛选"""
        # 复用 tenbagger_early_screener.py 的逻辑
        from research.short_mid_term_signal_selector.tenbagger_early_screener import TenbaggerEarlyScreener
        screener = TenbaggerEarlyScreener()
        results = screener.screen_early_stocks(date=date, top_n=top_n, min_score=min_score)
        return {
            "strategy": "tenbagger_early",
            "date": date,
            "count": len(results),
            "stocks": results
        }
    
    def _screen_mainline_theme(self, date, top_n, min_score, **kwargs):
        """主线题材筛选"""
        # 复用 tenbagger_mainline_screener.py 的逻辑
        mainline_sectors = kwargs.get('mainline_sectors', None)
        results = self.mainline_screener.screen_mainline_stocks(
            date=date,
            top_n=top_n,
            min_score=min_score,
            mainline_sectors=mainline_sectors
        )
        return {
            "strategy": "mainline_theme",
            "date": date,
            "count": len(results),
            "stocks": results
        }
    
    def _screen_user_specified(self, date, top_n, **kwargs):
        """用户指定股票筛选"""
        stock_codes = kwargs.get('stock_codes', [])
        # 对指定股票进行分析和排序
        results = []
        for code in stock_codes[:top_n]:
            analysis = self.analyze(code, date)
            results.append({
                "code": code,
                "name": analysis.get('basic_info', {}).get('name', ''),
                "score": analysis.get('stage_analysis', {}).get('score', 0),
                "analysis": analysis
            })
        results.sort(key=lambda x: x['score'], reverse=True)
        return {
            "strategy": "user_specified",
            "date": date,
            "count": len(results),
            "stocks": results
        }
    
    def _screen_tech_growth(self, date, top_n, min_score, **kwargs):
        """科技高成长筛选"""
        # 复用 tech_growth_screener.py 的逻辑
        from research.short_mid_term_signal_selector.tech_growth_screener import TechGrowthScreener
        screener = TechGrowthScreener()
        results = screener.screen_tech_stocks(date=date, top_n=top_n, min_score=min_score)
        return {
            "strategy": "tech_growth",
            "date": date,
            "count": len(results),
            "stocks": results
        }
```

---

## 5. 代码复用策略

### 5.1 数据获取层（复用）

✅ **已存在，直接使用**:
- JQData认证和查询 → `config/config_manager.py`
- CNINFO爬虫 → `mcp_servers/crawlers/cninfo_crawler.py`
- 配置管理 → `config/config_manager.py`

### 5.2 分析逻辑层（封装）

✅ **已存在，封装调用**:
- 十倍股分析 → `TenbaggerDeepAnalyzer`
- 主线筛选 → `MainlineScreener`
- 早期识别 → `TenbaggerEarlyScreener`
- 科技高成长 → `TechGrowthScreener`

### 5.3 报告生成层（统一）

⚠️ **需要统一**:
- 提取公共HTML模板
- 统一数据格式
- 支持多种报告类型
- 复用 `junsheng_full_analysis_report.py` 的结构

---

## 6. 验证方案

### 6.1 测试用例

```python
# tests/test_investment_target_server.py

def test_screen_tenbagger_early():
    """测试十倍股早期识别筛选"""
    result = analyzer.screen(
        strategy="tenbagger_early",
        date="2025-01-05",
        top_n=5,
        min_score=60.0
    )
    assert len(result['stocks']) <= 5
    assert all(s['score'] >= 60.0 for s in result['stocks'])

def test_screen_mainline_theme():
    """测试主线题材筛选"""
    result = analyzer.screen(
        strategy="mainline_theme",
        date="2025-01-05",
        top_n=10,
        mainline_sectors=["人工智能", "半导体芯片"]
    )
    assert len(result['stocks']) <= 10

def test_analyze_single_stock():
    """测试单股分析"""
    result = analyzer.analyze(
        stock_code="600699.XSHG",
        analysis_date="2025-01-05"
    )
    assert 'basic_info' in result
    assert 'price_analysis' in result
    assert 'financial_analysis' in result

def test_generate_report():
    """测试报告生成"""
    result = analyzer.generate_report(
        stock_code="600699.XSHG",
        report_type="full"
    )
    assert 'report_path' in result
    assert Path(result['report_path']).exists()
```

### 6.2 集成测试

1. **在工作流中测试**: 通过 `workflow_9steps_server.py` 调用
2. **在Notebook中测试**: 通过MCP工具调用
3. **端到端测试**: 从筛选到报告生成的完整流程

---

## 7. 实施计划

### 阶段1: 创建统一分析器
- [ ] 创建 `core/investment_target_analyzer.py`
- [ ] 封装现有筛选逻辑
- [ ] 实现统一接口

### 阶段2: 创建MCP Server
- [ ] 创建 `mcp_servers/investment_target_server.py`
- [ ] 定义MCP工具
- [ ] 实现工具处理函数

### 阶段3: 统一报告生成
- [ ] 提取公共HTML模板
- [ ] 统一数据格式
- [ ] 支持多种报告类型

### 阶段4: 测试验证
- [ ] 单元测试
- [ ] 集成测试
- [ ] 端到端测试

---

## 8. 总结

### 8.1 现有功能状态

✅ **已存在**:
- 候选池构建（`data_source.candidate_pool`）
- 十倍股筛选工具（`tenbagger.multifactor.*`）
- 报告生成（`report.generate`，但主要是回测报告）
- 工作流集成（9步工作流）

❌ **缺失**:
- 统一的投资标的筛选接口
- 个股深度分析报告生成（MCP接口）
- 批量分析功能
- 多种筛选策略的统一封装

### 8.2 实现建议

1. **创建统一分析器**: 封装现有逻辑，提供统一接口
2. **创建MCP Server**: 提供MCP工具接口
3. **统一报告生成**: 提取公共模板，支持多种类型
4. **逐步测试验证**: 确保功能正确

### 8.3 优势

- ✅ 统一接口，降低使用复杂度
- ✅ 复用现有实现，减少重复代码
- ✅ 易于扩展新策略
- ✅ 统一报告格式，便于对比
- ✅ 集成到工作流更简单

---

**最后更新**: 2026-01-06  
**维护者**: TRQuant Team
