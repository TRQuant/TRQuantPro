# 个股分析模块设计文档

> **创建时间**: 2026-01-06  
> **版本**: v1.0  
> **目的**: 定义个股分析模块在TRQuant系统框架中的位置、功能和应用方式

---

## 📍 模块位置

### 在工作流中的位置

```
研究阶段流程：
R0 数据源检测
  ↓
R1 市场趋势分析
  ↓
R2 主线轮动研究
  ↓
R3 因子组合开发
  ↓
R4 投资标的筛选 ← 输入：候选股票池（10-30只）
  ↓
【新增】R4.5 个股深度分析 ← 本模块位置
  ↓
R5 风控模块设计 ← 输入：个股分析报告（风险评估）
  ↓
R6 策略开发与回测
```

### 架构位置

```
core/
├── candidate_pool_builder.py      # R4: 候选池构建
├── investment_analysis.py         # R4.5: 个股深度分析 ← 新增
├── risk/                          # R5: 风控模块
└── workflow_orchestrator.py       # 工作流编排器（集成本模块）
```

---

## 🎯 核心功能

### 1. 数据收集与整合
- **JQData数据**：历史价格、财务快照、概念标签、技术指标
- **CNINFO数据**：年报/半年报PDF、重要公告、事件链
- **补充数据源**：新闻、政策、行业数据（可选）

### 2. 多维度分析
- **历史验证**：多年收益/回撤/波动、相对指数表现
- **财务分析**：营收/利润/现金流、ROE/ROA、负债结构
- **技术分析**：K线形态、技术指标、成交量分析
- **事件研究**：公告事件窗口、异常波动分析
- **同概念对比**：与同板块/概念股票对比

### 3. 研报级报告生成
- **多Tab HTML报告**：综述、行情、历史验证、财务、事件、对比、年报要点
- **交互式图表**：Plotly图表、数据表格
- **可追溯链接**：年报/公告PDF链接、数据源标注

---

## 🔧 模块设计

### 核心类：`InvestmentAnalyzer`

```python
# core/investment_analysis.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

@dataclass
class StockAnalysisConfig:
    """个股分析配置"""
    stock_code: str
    analysis_date: Optional[str] = None  # 分析基准日期
    include_annual_reports: bool = True   # 是否解析年报
    include_announcements: bool = True   # 是否抓取公告
    benchmark_code: str = "000300.XSHG"  # 基准指数
    peer_concept: Optional[str] = None   # 同概念对比（可选）
    output_dir: Path = Path("output/reports")  # 报告输出目录

@dataclass
class StockAnalysisResult:
    """个股分析结果"""
    stock_code: str
    stock_name: str
    analysis_date: str
    report_path: str  # HTML报告路径
    summary: Dict[str, Any]  # 关键数据摘要
    risk_level: str  # 风险等级：low/medium/high
    recommendation: str  # 投资建议：买入/持有/观望/回避
    confidence: float  # 置信度 0-1

class InvestmentAnalyzer:
    """
    个股深度分析器
    
    功能：
    1. 整合多数据源（JQData + CNINFO + 补充数据）
    2. 生成研报级HTML分析报告
    3. 输出结构化分析结果（用于风控模块）
    """
    
    def __init__(self, config: Optional[StockAnalysisConfig] = None):
        self.config = config
        self.jqdata_client = None
        self.cninfo_crawler = None
        self._init_data_sources()
    
    def analyze(self, stock_code: str, **kwargs) -> StockAnalysisResult:
        """
        分析单只股票
        
        Args:
            stock_code: 股票代码（如 "603778.XSHG"）
            **kwargs: 覆盖配置参数
        
        Returns:
            StockAnalysisResult: 分析结果
        """
        # 1. 收集数据
        price_data = self._fetch_price_data(stock_code)
        financial_data = self._fetch_financial_data(stock_code)
        annual_reports = self._fetch_annual_reports(stock_code) if self.config.include_annual_reports else []
        announcements = self._fetch_announcements(stock_code) if self.config.include_announcements else []
        
        # 2. 计算指标
        historical_perf = self._calculate_historical_performance(price_data)
        technical_indicators = self._calculate_technical_indicators(price_data)
        risk_metrics = self._calculate_risk_metrics(price_data, financial_data)
        
        # 3. 生成报告
        report_path = self._generate_html_report(
            stock_code=stock_code,
            price_data=price_data,
            financial_data=financial_data,
            annual_reports=annual_reports,
            announcements=announcements,
            historical_perf=historical_perf,
            technical_indicators=technical_indicators,
            risk_metrics=risk_metrics
        )
        
        # 4. 生成摘要和建议
        summary = self._generate_summary(price_data, financial_data, risk_metrics)
        risk_level = self._assess_risk_level(risk_metrics)
        recommendation = self._generate_recommendation(summary, risk_level)
        confidence = self._calculate_confidence(summary, risk_metrics)
        
        return StockAnalysisResult(
            stock_code=stock_code,
            stock_name=self._get_stock_name(stock_code),
            analysis_date=self.config.analysis_date or datetime.now().strftime("%Y-%m-%d"),
            report_path=str(report_path),
            summary=summary,
            risk_level=risk_level,
            recommendation=recommendation,
            confidence=confidence
        )
    
    def batch_analyze(self, stock_codes: List[str], **kwargs) -> List[StockAnalysisResult]:
        """
        批量分析多只股票
        
        Args:
            stock_codes: 股票代码列表
            **kwargs: 覆盖配置参数
        
        Returns:
            List[StockAnalysisResult]: 分析结果列表
        """
        results = []
        for code in stock_codes:
            try:
                result = self.analyze(code, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"分析 {code} 失败: {e}")
        return results
```

---

## 🔗 工作流集成

### 在 `WorkflowOrchestrator` 中集成

```python
# core/workflow_orchestrator.py

class WorkflowOrchestrator:
    # ... 现有代码 ...
    
    def analyze_candidate_stocks(self, top_n: int = 10) -> WorkflowResult:
        """
        步骤4.5: 对候选池Top N股票进行深度分析
        
        Args:
            top_n: 分析前N只股票（默认10只）
        
        Returns:
            WorkflowResult: 分析结果
        """
        logger.info(f"📊 对候选池Top {top_n}股票进行深度分析...")
        
        try:
            from core.investment_analysis import InvestmentAnalyzer, StockAnalysisConfig
            
            # 1. 获取候选池
            candidate_pool = self._get_candidate_pool()
            if not candidate_pool:
                return WorkflowResult(
                    step_name="analyze_candidate_stocks",
                    success=False,
                    summary="未找到候选池，请先执行 build_candidate_pool()",
                    error="No candidate pool found"
                )
            
            # 2. 取Top N
            top_stocks = candidate_pool[:top_n]
            stock_codes = [s["code"] for s in top_stocks]
            
            # 3. 批量分析
            analyzer = InvestmentAnalyzer()
            results = analyzer.batch_analyze(stock_codes)
            
            # 4. 保存结果到MongoDB
            if self.db:
                for result in results:
                    self.db.stock_analysis.insert_one({
                        "stock_code": result.stock_code,
                        "analysis_date": result.analysis_date,
                        "summary": result.summary,
                        "risk_level": result.risk_level,
                        "recommendation": result.recommendation,
                        "confidence": result.confidence,
                        "report_path": result.report_path,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # 5. 生成汇总报告
            summary_report = self._generate_analysis_summary(results)
            
            return WorkflowResult(
                step_name="analyze_candidate_stocks",
                success=True,
                summary=f"完成 {len(results)} 只股票深度分析",
                details={
                    "analyzed_count": len(results),
                    "reports": [r.report_path for r in results],
                    "summary_report": summary_report,
                    "risk_distribution": self._count_risk_levels(results),
                    "recommendations": self._count_recommendations(results)
                }
            )
            
        except Exception as e:
            logger.error(f"个股分析失败: {e}", exc_info=True)
            return WorkflowResult(
                step_name="analyze_candidate_stocks",
                success=False,
                summary=f"个股分析失败: {str(e)}",
                error=str(e)
            )
```

---

## 📊 应用场景

### 场景1: 工作流自动分析
```python
# 完整工作流
orchestrator = WorkflowOrchestrator()

# R0-R4: 数据源检测 → 市场分析 → 主线 → 因子 → 候选池
orchestrator.check_data_sources()
orchestrator.analyze_market_trend()
orchestrator.identify_mainlines()
orchestrator.build_candidate_pool()

# R4.5: 个股深度分析（新增）
result = orchestrator.analyze_candidate_stocks(top_n=10)

# R5: 风控模块（使用分析结果）
risk_assessment = orchestrator.design_risk_control(
    stock_analysis_results=result.details["reports"]
)
```

### 场景2: 独立调用（研究工具）
```python
from core.investment_analysis import InvestmentAnalyzer, StockAnalysisConfig

# 分析单只股票
analyzer = InvestmentAnalyzer()
result = analyzer.analyze("603778.XSHG")

print(f"报告路径: {result.report_path}")
print(f"风险等级: {result.risk_level}")
print(f"投资建议: {result.recommendation}")
```

### 场景3: Notebook研究
```python
# notebooks/research/03_stock_analysis.ipynb

from core.investment_analysis import InvestmentAnalyzer

analyzer = InvestmentAnalyzer()

# 分析候选池Top 5
top_5 = ["603778.XSHG", "688270.XSHG", "300515.XSHE", ...]
results = analyzer.batch_analyze(top_5)

# 可视化对比
import pandas as pd
df = pd.DataFrame([{
    "code": r.stock_code,
    "risk": r.risk_level,
    "recommendation": r.recommendation,
    "confidence": r.confidence
} for r in results])

display(df)
```

---

## 📁 文件结构

```
core/
├── investment_analysis.py          # 核心分析器
│   ├── InvestmentAnalyzer          # 主类
│   ├── StockAnalysisConfig         # 配置
│   └── StockAnalysisResult         # 结果
│
scripts/
└── reports/
    └── stock_analysis_report.py    # HTML报告生成器（可复用现有代码）

notebooks/
└── research/
    └── 03_stock_analysis.ipynb     # 个股分析研究Notebook

output/
└── reports/
    └── stock_analysis/
        ├── 603778_20260106.html
        ├── 688270_20260106.html
        └── ...
```

---

## 🔄 与现有模块的关系

### 输入依赖
- **CandidatePoolBuilder** (R4): 提供候选股票池
- **JQDataClient**: 提供价格/财务数据
- **CNINFO Crawler**: 提供年报/公告数据

### 输出供给
- **Risk Control Module** (R5): 提供风险评估数据
- **Strategy Generator** (R6): 提供个股特征数据（可选）

### 数据存储
- **MongoDB**: `trquant.stock_analysis` 集合
- **文件系统**: `output/reports/stock_analysis/` 目录

---

## ✅ 实施步骤

1. **创建核心模块** (`core/investment_analysis.py`)
   - 封装现有的报告生成逻辑
   - 提供统一的API接口

2. **集成到工作流** (`core/workflow_orchestrator.py`)
   - 添加 `analyze_candidate_stocks()` 方法
   - 在 `run_full_workflow()` 中调用

3. **更新系统架构文档** (`notebooks/research/00_system_architecture_workflow.ipynb`)
   - 添加 R4.5 节点
   - 更新核心模块说明

4. **创建研究Notebook** (`notebooks/research/03_stock_analysis.ipynb`)
   - 提供使用示例
   - 可视化分析结果

5. **测试与验证**
   - 单元测试
   - 集成测试（工作流）
   - 报告质量验证

---

## 📝 总结

个股分析模块是**投资工作流程中的关键环节**，位于：
- **R4（投资标的筛选）之后**：对筛选出的候选股票进行深度分析
- **R5（风控模块设计）之前**：为风控模块提供风险评估数据

**核心价值**：
1. **数据整合**：统一多数据源（JQData + CNINFO + 补充数据）
2. **深度分析**：历史验证、财务分析、事件研究、同概念对比
3. **研报级输出**：多Tab HTML报告，可直接用于投资决策
4. **工作流集成**：自动化分析流程，支持批量处理

**应用方式**：
- **工作流自动调用**：在完整工作流中自动执行
- **独立研究工具**：在Notebook中手动调用
- **批量分析**：对候选池Top N股票批量生成报告
