"""
A股主线识别 - 专业分析引擎

参考PandaAI和机构级量化平台架构设计：
1. 多数据源统一接入（AKShare/TuShare/JQData/Wind）
2. 本地缓存层（MongoDB + 文件）
3. 事件驱动分析框架
4. Cursor IDE集成分析
5. 可视化工作流

核心理念：
- 数据驱动：所有结论基于真实数据
- 过程透明：每一步分析都可追溯
- AI辅助：利用LLM增强分析能力
- 工具集成：与Cursor/IDE无缝协作
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .real_data_fetcher import RealDataFetcher, real_data_fetcher, DataFetchResult

logger = logging.getLogger(__name__)


class AnalysisStage(Enum):
    """分析阶段"""
    DATA_COLLECTION = "data_collection"      # 数据采集
    DATA_VALIDATION = "data_validation"      # 数据验证
    MACRO_ANALYSIS = "macro_analysis"        # 宏观分析
    SECTOR_ANALYSIS = "sector_analysis"      # 板块分析
    CAPITAL_ANALYSIS = "capital_analysis"    # 资金分析
    SENTIMENT_ANALYSIS = "sentiment_analysis"  # 情绪分析
    MAINLINE_SYNTHESIS = "mainline_synthesis"  # 主线综合
    REPORT_GENERATION = "report_generation"   # 报告生成


@dataclass
class AnalysisStep:
    """分析步骤记录"""
    stage: AnalysisStage
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    input_data: Optional[Dict] = None
    output_data: Optional[Any] = None
    data_sources: List[str] = field(default_factory=list)
    method: str = ""
    status: str = "running"
    error: Optional[str] = None
    
    def complete(self, output: Any):
        self.end_time = datetime.now()
        self.output_data = output
        self.status = "completed"
    
    def fail(self, error: str):
        self.end_time = datetime.now()
        self.error = error
        self.status = "failed"
    
    @property
    def duration_ms(self) -> int:
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() * 1000)
        return 0
    
    def to_dict(self) -> Dict:
        return {
            "stage": self.stage.value,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "data_sources": self.data_sources,
            "method": self.method,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class MainlineResult:
    """主线识别结果"""
    name: str
    score: float
    confidence: float
    core_logic: str
    supporting_factors: List[Dict]
    risk_factors: List[str]
    sectors: List[str]
    leading_stocks: List[str]
    data_evidence: List[Dict]  # 数据证据
    analysis_chain: List[str]  # 分析推理链
    recommendation: str
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "score": self.score,
            "confidence": self.confidence,
            "core_logic": self.core_logic,
            "supporting_factors": self.supporting_factors,
            "risk_factors": self.risk_factors,
            "sectors": self.sectors,
            "leading_stocks": self.leading_stocks,
            "data_evidence": self.data_evidence,
            "analysis_chain": self.analysis_chain,
            "recommendation": self.recommendation,
        }


class MainlineAnalysisEngine:
    """
    主线分析引擎
    
    参考PandaAI的工作流架构和机构级量化平台设计：
    1. 数据采集 → 2. 数据验证 → 3. 多维分析 → 4. 主线综合 → 5. 报告生成
    
    每个步骤都记录：
    - 使用的数据源
    - 分析方法
    - 输入输出
    - 执行时间
    """
    
    def __init__(self, data_fetcher: Optional[RealDataFetcher] = None):
        self.data_fetcher = data_fetcher or real_data_fetcher
        self.steps: List[AnalysisStep] = []
        self.raw_data: Dict[str, DataFetchResult] = {}
        self.analysis_results: Dict[str, Any] = {}
        self.mainlines: List[MainlineResult] = []
        
        # 分析配置
        self.config = {
            "min_sector_count": 5,           # 最少板块数
            "top_sector_count": 10,          # 取前N个板块
            "mainline_threshold": 60,        # 主线得分阈值
            "confidence_threshold": 0.7,     # 置信度阈值
        }
    
    def run_full_analysis(self) -> Dict:
        """
        运行完整分析流程
        
        Returns:
            {
                "mainlines": List[MainlineResult],
                "steps": List[AnalysisStep],
                "raw_data": Dict,
                "analysis_results": Dict,
                "summary": Dict,
                "cursor_prompt": str,
            }
        """
        self.steps = []
        self.raw_data = {}
        self.analysis_results = {}
        self.mainlines = []
        
        start_time = datetime.now()
        logger.info("=" * 70)
        logger.info("🚀 开始主线分析引擎")
        logger.info("=" * 70)
        
        try:
            # Step 1: 数据采集
            self._step_data_collection()
            
            # Step 2: 数据验证
            self._step_data_validation()
            
            # Step 3: 板块分析
            self._step_sector_analysis()
            
            # Step 4: 资金分析
            self._step_capital_analysis()
            
            # Step 5: 情绪分析
            self._step_sentiment_analysis()
            
            # Step 6: 主线综合
            self._step_mainline_synthesis()
            
            # Step 7: 生成Cursor分析Prompt
            cursor_prompt = self._generate_cursor_prompt()
            
        except Exception as e:
            logger.error(f"分析失败: {e}")
            import traceback
            traceback.print_exc()
            cursor_prompt = f"分析失败: {e}"
        
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # 生成摘要
        summary = {
            "total_time_ms": int(total_time),
            "steps_completed": len([s for s in self.steps if s.status == "completed"]),
            "steps_failed": len([s for s in self.steps if s.status == "failed"]),
            "data_sources_used": list(set(
                src for step in self.steps for src in step.data_sources
            )),
            "mainlines_found": len(self.mainlines),
            "analysis_time": datetime.now().isoformat(),
        }
        
        logger.info("=" * 70)
        logger.info(f"✅ 分析完成，耗时 {total_time:.0f}ms")
        logger.info(f"   发现 {len(self.mainlines)} 条主线")
        logger.info("=" * 70)
        
        return {
            "mainlines": self.mainlines,
            "steps": self.steps,
            "raw_data": self.raw_data,
            "analysis_results": self.analysis_results,
            "summary": summary,
            "cursor_prompt": cursor_prompt,
        }
    
    def _start_step(self, stage: AnalysisStage, name: str, method: str = "") -> AnalysisStep:
        """开始一个分析步骤"""
        step = AnalysisStep(
            stage=stage,
            name=name,
            start_time=datetime.now(),
            method=method,
        )
        self.steps.append(step)
        logger.info(f"\n📌 {name}")
        return step
    
    # ================================================================
    # Step 1: 数据采集
    # ================================================================
    
    def _step_data_collection(self):
        """数据采集步骤"""
        step = self._start_step(
            AnalysisStage.DATA_COLLECTION,
            "数据采集",
            "从AKShare/MongoDB获取实时市场数据"
        )
        
        try:
            self.raw_data = self.data_fetcher.fetch_all_data()
            
            step.data_sources = [
                f"{key}:{result.source}" 
                for key, result in self.raw_data.items()
            ]
            
            success_count = sum(1 for r in self.raw_data.values() if r.success)
            step.complete({
                "total": len(self.raw_data),
                "success": success_count,
                "sources": step.data_sources,
            })
            
            logger.info(f"   ✅ {success_count}/{len(self.raw_data)} 数据源成功")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    # ================================================================
    # Step 2: 数据验证
    # ================================================================
    
    def _step_data_validation(self):
        """数据验证步骤"""
        step = self._start_step(
            AnalysisStage.DATA_VALIDATION,
            "数据验证",
            "检查数据完整性和时效性"
        )
        
        try:
            validation_results = {}
            
            for key, result in self.raw_data.items():
                validation = {
                    "source": result.source,
                    "success": result.success,
                    "has_data": result.data is not None,
                    "data_count": len(result.data) if isinstance(result.data, list) else 1 if result.data else 0,
                    "fetch_time": result.fetch_time.isoformat(),
                    "is_fresh": (datetime.now() - result.fetch_time).seconds < 3600,  # 1小时内
                }
                validation_results[key] = validation
            
            step.data_sources = list(self.raw_data.keys())
            step.complete(validation_results)
            
            fresh_count = sum(1 for v in validation_results.values() if v["is_fresh"])
            logger.info(f"   ✅ {fresh_count}/{len(validation_results)} 数据新鲜")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    # ================================================================
    # Step 3: 板块分析
    # ================================================================
    
    def _step_sector_analysis(self):
        """板块分析步骤"""
        step = self._start_step(
            AnalysisStage.SECTOR_ANALYSIS,
            "板块分析",
            "分析板块涨跌、资金流向、龙头表现"
        )
        step.data_sources = ["sector_flow", "concept_board"]
        
        try:
            sector_flow = self.raw_data.get("sector_flow")
            concept_board = self.raw_data.get("concept_board")
            
            analysis = {
                "top_sectors": [],
                "hot_concepts": [],
                "sector_rotation": "",
                "leading_themes": [],
            }
            
            # 分析板块资金流向
            if sector_flow and sector_flow.success and sector_flow.data:
                sorted_sectors = sorted(
                    sector_flow.data, 
                    key=lambda x: x.get("main_net_inflow", 0), 
                    reverse=True
                )
                analysis["top_sectors"] = sorted_sectors[:self.config["top_sector_count"]]
                
                # 判断板块轮动
                inflow_sectors = [s["sector_name"] for s in sorted_sectors if s.get("main_net_inflow", 0) > 0]
                outflow_sectors = [s["sector_name"] for s in sorted_sectors if s.get("main_net_inflow", 0) < 0]
                
                if "科技" in str(inflow_sectors) or "人工智能" in str(inflow_sectors):
                    analysis["sector_rotation"] = "科技成长主导"
                elif "消费" in str(inflow_sectors):
                    analysis["sector_rotation"] = "消费复苏"
                elif "金融" in str(inflow_sectors) or "银行" in str(inflow_sectors):
                    analysis["sector_rotation"] = "大金融发力"
                else:
                    analysis["sector_rotation"] = "板块轮动"
            
            # 分析概念板块
            if concept_board and concept_board.success and concept_board.data:
                sorted_concepts = sorted(
                    concept_board.data,
                    key=lambda x: x.get("change_pct", 0),
                    reverse=True
                )
                analysis["hot_concepts"] = sorted_concepts[:10]
                
                # 提取主题
                for concept in sorted_concepts[:5]:
                    name = concept.get("board_name", "")
                    if "AI" in name or "智能" in name or "ChatGPT" in name:
                        analysis["leading_themes"].append("人工智能")
                    elif "芯片" in name or "半导体" in name:
                        analysis["leading_themes"].append("半导体")
                    elif "光" in name and "模块" in name:
                        analysis["leading_themes"].append("光模块")
                    elif "机器人" in name:
                        analysis["leading_themes"].append("机器人")
                    elif "新能源" in name or "光伏" in name:
                        analysis["leading_themes"].append("新能源")
                
                analysis["leading_themes"] = list(set(analysis["leading_themes"]))
            
            self.analysis_results["sector"] = analysis
            step.complete(analysis)
            
            logger.info(f"   ✅ 板块轮动: {analysis['sector_rotation']}")
            logger.info(f"   ✅ 主导主题: {analysis['leading_themes']}")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    # ================================================================
    # Step 4: 资金分析
    # ================================================================
    
    def _step_capital_analysis(self):
        """资金分析步骤"""
        step = self._start_step(
            AnalysisStage.CAPITAL_ANALYSIS,
            "资金分析",
            "分析北向资金、主力资金流向"
        )
        step.data_sources = ["northbound_flow", "sector_flow"]
        
        try:
            northbound = self.raw_data.get("northbound_flow")
            sector_flow = self.raw_data.get("sector_flow")
            
            analysis = {
                "northbound_trend": "",
                "northbound_data": {},
                "main_force_direction": [],
                "capital_consensus": [],
            }
            
            # 北向资金分析
            if northbound and northbound.success and northbound.data:
                data = northbound.data
                today = data.get("today_net", 0)
                week = data.get("week_net", 0)
                month = data.get("month_net", 0)
                
                analysis["northbound_data"] = {
                    "today": today,
                    "week": week,
                    "month": month,
                }
                
                if month > 100:
                    analysis["northbound_trend"] = "大幅流入"
                elif month > 0:
                    analysis["northbound_trend"] = "温和流入"
                elif month > -100:
                    analysis["northbound_trend"] = "温和流出"
                else:
                    analysis["northbound_trend"] = "大幅流出"
            
            # 主力资金方向
            if sector_flow and sector_flow.success and sector_flow.data:
                inflow_sectors = [
                    s["sector_name"] 
                    for s in sector_flow.data 
                    if s.get("main_net_inflow", 0) > 10  # 超过10亿
                ]
                analysis["main_force_direction"] = inflow_sectors[:5]
                
                # 资金共识
                if len(inflow_sectors) >= 3:
                    analysis["capital_consensus"] = inflow_sectors[:3]
            
            self.analysis_results["capital"] = analysis
            step.complete(analysis)
            
            logger.info(f"   ✅ 北向趋势: {analysis['northbound_trend']}")
            logger.info(f"   ✅ 主力方向: {analysis['main_force_direction']}")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    # ================================================================
    # Step 5: 情绪分析
    # ================================================================
    
    def _step_sentiment_analysis(self):
        """情绪分析步骤"""
        step = self._start_step(
            AnalysisStage.SENTIMENT_ANALYSIS,
            "情绪分析",
            "分析涨停跌停、连板、市场情绪"
        )
        step.data_sources = ["market_sentiment", "dragon_tiger"]
        
        try:
            sentiment = self.raw_data.get("market_sentiment")
            dragon = self.raw_data.get("dragon_tiger")
            
            analysis = {
                "sentiment_score": 50,
                "sentiment_level": "中性",
                "limit_up_count": 0,
                "limit_down_count": 0,
                "continuous_limit": {},
                "hot_stocks": [],
            }
            
            if sentiment and sentiment.success and sentiment.data:
                data = sentiment.data
                analysis["sentiment_score"] = data.get("sentiment_score", 50)
                analysis["limit_up_count"] = data.get("up_limit_count", 0)
                analysis["limit_down_count"] = data.get("down_limit_count", 0)
                analysis["continuous_limit"] = data.get("continuous_limit", {})
                
                score = analysis["sentiment_score"]
                if score >= 80:
                    analysis["sentiment_level"] = "极度乐观"
                elif score >= 65:
                    analysis["sentiment_level"] = "乐观"
                elif score >= 50:
                    analysis["sentiment_level"] = "中性偏多"
                elif score >= 35:
                    analysis["sentiment_level"] = "谨慎"
                else:
                    analysis["sentiment_level"] = "悲观"
            
            if dragon and dragon.success and dragon.data:
                analysis["hot_stocks"] = [
                    {"name": d.get("name", ""), "reason": d.get("reason", "")}
                    for d in dragon.data[:5]
                ]
            
            self.analysis_results["sentiment"] = analysis
            step.complete(analysis)
            
            logger.info(f"   ✅ 情绪得分: {analysis['sentiment_score']}")
            logger.info(f"   ✅ 情绪水平: {analysis['sentiment_level']}")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    # ================================================================
    # Step 6: 主线综合
    # ================================================================
    
    def _step_mainline_synthesis(self):
        """主线综合步骤"""
        step = self._start_step(
            AnalysisStage.MAINLINE_SYNTHESIS,
            "主线综合",
            "综合多维度数据识别投资主线"
        )
        step.data_sources = ["sector", "capital", "sentiment"]
        
        try:
            sector = self.analysis_results.get("sector", {})
            capital = self.analysis_results.get("capital", {})
            sentiment = self.analysis_results.get("sentiment", {})
            
            # 识别主线
            mainlines = []
            
            # 主线1: 人工智能
            if "人工智能" in sector.get("leading_themes", []):
                mainline = self._build_mainline(
                    name="人工智能革命",
                    base_score=85,
                    core_logic="AI大模型技术突破引发新一轮科技革命",
                    sectors=["AI算力", "AI应用", "光模块", "数据中心"],
                    stocks=["寒武纪", "中科曙光", "科大讯飞", "中际旭创"],
                    sector_data=sector,
                    capital_data=capital,
                    sentiment_data=sentiment,
                )
                mainlines.append(mainline)
            
            # 主线2: 半导体/国产替代
            if "半导体" in sector.get("leading_themes", []):
                mainline = self._build_mainline(
                    name="国产替代加速",
                    base_score=80,
                    core_logic="外部压力倒逼国产化进程，半导体设备材料受益",
                    sectors=["半导体设备", "半导体材料", "EDA", "先进封装"],
                    stocks=["北方华创", "中微公司", "华大九天", "长电科技"],
                    sector_data=sector,
                    capital_data=capital,
                    sentiment_data=sentiment,
                )
                mainlines.append(mainline)
            
            # 主线3: 新能源
            if "新能源" in sector.get("leading_themes", []):
                mainline = self._build_mainline(
                    name="新能源转型",
                    base_score=70,
                    core_logic="碳中和目标驱动能源结构转型",
                    sectors=["光伏", "储能", "锂电池", "新能源车"],
                    stocks=["隆基绿能", "宁德时代", "阳光电源", "比亚迪"],
                    sector_data=sector,
                    capital_data=capital,
                    sentiment_data=sentiment,
                )
                mainlines.append(mainline)
            
            # 如果没有识别到主线，添加默认主线
            if not mainlines:
                mainline = self._build_mainline(
                    name="科技成长",
                    base_score=65,
                    core_logic="政策支持科技创新，成长风格占优",
                    sectors=["科技", "电子", "计算机"],
                    stocks=["待筛选"],
                    sector_data=sector,
                    capital_data=capital,
                    sentiment_data=sentiment,
                )
                mainlines.append(mainline)
            
            # 按得分排序
            mainlines.sort(key=lambda x: x.score, reverse=True)
            self.mainlines = mainlines
            
            step.complete({
                "mainlines_count": len(mainlines),
                "top_mainline": mainlines[0].name if mainlines else None,
            })
            
            for ml in mainlines:
                logger.info(f"   🔥 {ml.name}: {ml.score:.0f}分")
            
        except Exception as e:
            step.fail(str(e))
            raise
    
    def _build_mainline(
        self,
        name: str,
        base_score: float,
        core_logic: str,
        sectors: List[str],
        stocks: List[str],
        sector_data: Dict,
        capital_data: Dict,
        sentiment_data: Dict,
    ) -> MainlineResult:
        """构建主线结果"""
        
        # 计算调整后得分
        score = base_score
        confidence = 0.7
        supporting_factors = []
        analysis_chain = []
        data_evidence = []
        
        # 1. 板块因素
        top_sectors = sector_data.get("top_sectors", [])
        for sector in sectors:
            for ts in top_sectors:
                if sector in ts.get("sector_name", ""):
                    score += 3
                    confidence += 0.05
                    supporting_factors.append({
                        "factor": f"板块资金流入",
                        "detail": f"{ts['sector_name']}主力净流入{ts.get('main_net_inflow', 0):.1f}亿",
                        "score_impact": 3,
                    })
                    data_evidence.append({
                        "source": "sector_flow",
                        "data": f"{ts['sector_name']}: {ts.get('change_pct', 0):.2f}%",
                    })
                    break
        
        analysis_chain.append(f"板块分析: {sector_data.get('sector_rotation', '未知')}")
        
        # 2. 资金因素
        northbound_trend = capital_data.get("northbound_trend", "")
        if "流入" in northbound_trend:
            score += 5
            confidence += 0.05
            supporting_factors.append({
                "factor": "北向资金流入",
                "detail": northbound_trend,
                "score_impact": 5,
            })
            data_evidence.append({
                "source": "northbound_flow",
                "data": f"本月净流入: {capital_data.get('northbound_data', {}).get('month', 0):.1f}亿",
            })
        
        analysis_chain.append(f"资金分析: {northbound_trend}")
        
        # 3. 情绪因素
        sentiment_level = sentiment_data.get("sentiment_level", "中性")
        sentiment_score = sentiment_data.get("sentiment_score", 50)
        if sentiment_score >= 65:
            score += 5
            confidence += 0.05
            supporting_factors.append({
                "factor": "市场情绪乐观",
                "detail": f"情绪得分{sentiment_score}",
                "score_impact": 5,
            })
        
        data_evidence.append({
            "source": "market_sentiment",
            "data": f"涨停{sentiment_data.get('limit_up_count', 0)}家，跌停{sentiment_data.get('limit_down_count', 0)}家",
        })
        
        analysis_chain.append(f"情绪分析: {sentiment_level}")
        
        # 风险因素
        risk_factors = []
        if score > 85:
            risk_factors.append("估值可能偏高")
        if sentiment_score > 80:
            risk_factors.append("市场过热风险")
        if "流出" in northbound_trend:
            risk_factors.append("外资流出压力")
        
        # 投资建议
        if score >= 85:
            recommendation = "强烈推荐：多维度指标优异，建议积极配置"
        elif score >= 75:
            recommendation = "推荐：整体表现良好，建议适度超配"
        elif score >= 65:
            recommendation = "中性偏多：基本面尚可，建议标配"
        else:
            recommendation = "观望：等待更明确信号"
        
        return MainlineResult(
            name=name,
            score=min(100, score),
            confidence=min(1.0, confidence),
            core_logic=core_logic,
            supporting_factors=supporting_factors,
            risk_factors=risk_factors,
            sectors=sectors,
            leading_stocks=stocks,
            data_evidence=data_evidence,
            analysis_chain=analysis_chain,
            recommendation=recommendation,
        )
    
    # ================================================================
    # 生成Cursor分析Prompt
    # ================================================================
    
    def _generate_cursor_prompt(self) -> str:
        """生成供Cursor分析的Prompt"""
        
        # 收集所有数据
        sector = self.analysis_results.get("sector", {})
        capital = self.analysis_results.get("capital", {})
        sentiment = self.analysis_results.get("sentiment", {})
        
        prompt = f"""# A股主线识别分析请求

## 📅 分析时间
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 真实市场数据摘要

### 板块资金流向
"""
        
        # 添加板块数据
        top_sectors = sector.get("top_sectors", [])
        if top_sectors:
            prompt += "| 板块 | 涨跌幅 | 主力净流入(亿) |\n"
            prompt += "|------|--------|----------------|\n"
            for s in top_sectors[:10]:
                prompt += f"| {s.get('sector_name', '')} | {s.get('change_pct', 0):.2f}% | {s.get('main_net_inflow', 0):.2f} |\n"
        
        prompt += f"""
### 北向资金
- 今日: {capital.get('northbound_data', {}).get('today', 0):.2f}亿
- 本周: {capital.get('northbound_data', {}).get('week', 0):.2f}亿
- 本月: {capital.get('northbound_data', {}).get('month', 0):.2f}亿
- 趋势: {capital.get('northbound_trend', '未知')}

### 市场情绪
- 情绪得分: {sentiment.get('sentiment_score', 50)}/100
- 情绪水平: {sentiment.get('sentiment_level', '中性')}
- 涨停家数: {sentiment.get('limit_up_count', 0)}
- 跌停家数: {sentiment.get('limit_down_count', 0)}

### 初步分析结果
- 板块轮动: {sector.get('sector_rotation', '未知')}
- 主导主题: {', '.join(sector.get('leading_themes', []))}
- 资金共识: {', '.join(capital.get('capital_consensus', []))}

## 🎯 分析任务

请基于以上真实数据，完成深度分析：

1. **验证初步结论**：上述初步分析是否合理？有无遗漏？

2. **主线深度分析**：
   - 识别1-3条最强投资主线
   - 说明核心逻辑和支撑因素
   - 评估持续性和风险

3. **投资建议**：
   - 具体板块和龙头股推荐
   - 仓位配置建议
   - 风控措施

请以JSON格式输出分析结果。
"""
        
        return prompt


# 全局实例
analysis_engine = MainlineAnalysisEngine()

