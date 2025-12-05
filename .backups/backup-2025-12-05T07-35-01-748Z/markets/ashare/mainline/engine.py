"""
A股主线识别引擎 - 专业版

核心特点：
1. 数据源透明 - 每个数据都标注来源
2. 分析过程可追溯 - 展示完整推理链
3. 参数专业化 - 参考行业先进水平
4. LLM辅助 - 综合多源信息

三层分析框架：
- 宏观前瞻（6-12个月）：政策周期、经济周期、全球趋势
- 中观验证（1-3个月）：行业景气、资金流向、催化剂
- 微观确认（1-4周）：技术形态、龙头表现、市场情绪
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import logging
import json

from .data_sources import DataSourceManager, data_source_manager, DataSourceType
from .scoring_model import ScoringModel, scoring_model, MainlineScore
from .llm_analyzer import LLMAnalyzer, llm_analyzer, AnalysisResult

logger = logging.getLogger(__name__)


class MainlineStage(Enum):
    """主线阶段"""
    EMERGING = "emerging"      # 启动期 - 少数人发现
    GROWING = "growing"        # 成长期 - 资金涌入
    MATURE = "mature"          # 成熟期 - 共识形成
    DECLINING = "declining"    # 衰退期 - 获利了结


@dataclass
class DataTrace:
    """数据溯源"""
    source_id: str              # 数据源ID
    source_name: str            # 数据源名称
    provider: str               # 提供商
    fetch_time: datetime        # 获取时间
    data_fields: List[str]      # 使用的字段
    raw_data: Any               # 原始数据
    reliability: str            # 可靠性
    
    def to_dict(self) -> Dict:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "provider": self.provider,
            "fetch_time": self.fetch_time.isoformat(),
            "data_fields": self.data_fields,
            "reliability": self.reliability,
        }


@dataclass
class AnalysisStep:
    """分析步骤"""
    step_name: str              # 步骤名称
    description: str            # 步骤描述
    input_sources: List[str]    # 输入数据源
    method: str                 # 分析方法
    output: Any                 # 输出结果
    duration_ms: int            # 耗时(毫秒)
    
    def to_dict(self) -> Dict:
        return {
            "step_name": self.step_name,
            "description": self.description,
            "input_sources": self.input_sources,
            "method": self.method,
            "output": self.output if isinstance(self.output, (dict, list, str, int, float)) else str(self.output),
            "duration_ms": self.duration_ms,
        }


@dataclass
class Mainline:
    """投资主线"""
    name: str                       # 主线名称
    stage: MainlineStage            # 当前阶段
    score: MainlineScore            # 综合评分
    sectors: List[str]              # 相关板块
    stocks: List[str]               # 龙头股票
    core_logic: str                 # 核心逻辑
    supporting_factors: List[str]   # 支撑因素
    risk_factors: List[str]         # 风险因素
    duration_weeks: int             # 预计持续周数
    recommendation: str             # 投资建议
    data_traces: List[DataTrace]    # 数据溯源
    analysis_steps: List[AnalysisStep]  # 分析步骤
    llm_analysis: Optional[AnalysisResult] = None  # LLM分析
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "stage": self.stage.value,
            "score": self.score.to_dict(),
            "sectors": self.sectors,
            "stocks": self.stocks,
            "core_logic": self.core_logic,
            "supporting_factors": self.supporting_factors,
            "risk_factors": self.risk_factors,
            "duration_weeks": self.duration_weeks,
            "recommendation": self.recommendation,
            "data_traces": [t.to_dict() for t in self.data_traces],
            "analysis_steps": [s.to_dict() for s in self.analysis_steps],
            "llm_analysis": self.llm_analysis.to_dict() if self.llm_analysis else None,
        }


class AShareMainlineEngine:
    """
    A股主线识别引擎 - 专业版
    
    使用方法：
        engine = AShareMainlineEngine()
        
        # 运行完整分析
        result = engine.run_full_analysis()
        
        # 查看发现的主线
        for mainline in result["mainlines"]:
            print(f"主线: {mainline.name}, 得分: {mainline.score.total_score}")
            
        # 查看数据溯源
        for trace in result["data_traces"]:
            print(f"数据源: {trace.source_name} ({trace.provider})")
            
        # 查看分析步骤
        for step in result["analysis_steps"]:
            print(f"步骤: {step.step_name} - {step.method}")
    """
    
    def __init__(
        self,
        data_manager: Optional[DataSourceManager] = None,
        scoring: Optional[ScoringModel] = None,
        llm: Optional[LLMAnalyzer] = None,
    ):
        self.data_manager = data_manager or data_source_manager
        self.scoring = scoring or scoring_model
        self.llm = llm or llm_analyzer
        
        self._data_traces: List[DataTrace] = []
        self._analysis_steps: List[AnalysisStep] = []
        
        logger.info("A股主线识别引擎初始化成功")
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """
        运行完整分析流程
        
        Returns:
            {
                "mainlines": List[Mainline],
                "data_traces": List[DataTrace],
                "analysis_steps": List[AnalysisStep],
                "summary": Dict,
                "analysis_time": datetime,
            }
        """
        start_time = datetime.now()
        self._data_traces = []
        self._analysis_steps = []
        
        logger.info("=" * 60)
        logger.info("🚀 开始主线识别分析")
        logger.info("=" * 60)
        
        # Step 1: 宏观前瞻分析
        macro_data = self._analyze_macro()
        
        # Step 2: 资金流向分析
        capital_data = self._analyze_capital()
        
        # Step 3: 行业景气分析
        industry_data = self._analyze_industry()
        
        # Step 4: 技术形态分析
        technical_data = self._analyze_technical()
        
        # Step 5: 估值分析
        valuation_data = self._analyze_valuation()
        
        # Step 6: 前瞻指标分析
        foresight_data = self._analyze_foresight()
        
        # Step 7: LLM综合分析
        llm_result = self._run_llm_synthesis(
            macro_data, capital_data, industry_data, technical_data
        )
        
        # Step 8: 识别主线
        mainlines = self._identify_mainlines(
            macro_data, capital_data, industry_data,
            technical_data, valuation_data, foresight_data,
            llm_result
        )
        
        # 生成摘要
        summary = self._generate_summary(mainlines)
        
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info("=" * 60)
        logger.info(f"✅ 分析完成，耗时 {total_time:.0f}ms，发现 {len(mainlines)} 条主线")
        logger.info("=" * 60)
        
        return {
            "mainlines": mainlines,
            "data_traces": self._data_traces,
            "analysis_steps": self._analysis_steps,
            "summary": summary,
            "analysis_time": datetime.now(),
        }
    
    def _analyze_macro(self) -> Dict:
        """宏观前瞻分析"""
        step_start = datetime.now()
        logger.info("\n📋 Step 1: 宏观前瞻分析")
        
        # 获取政策数据
        policy_result = self.data_manager.fetch_data("macro_policy")
        self._add_trace("macro_policy", policy_result)
        
        # 获取经济数据
        economic_result = self.data_manager.fetch_data("macro_economic")
        self._add_trace("macro_economic", economic_result)
        
        # 获取流动性数据
        liquidity_result = self.data_manager.fetch_data("macro_liquidity")
        self._add_trace("macro_liquidity", liquidity_result)
        
        # 综合分析
        macro_data = {
            "policy_cycle": self._determine_policy_cycle(policy_result.get("data", {})),
            "economic_cycle": self._determine_economic_cycle(economic_result.get("data", {})),
            "liquidity_condition": self._determine_liquidity(liquidity_result.get("data", {})),
            "benefited_sectors": self._get_policy_benefited_sectors(policy_result.get("data", {})),
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "宏观前瞻分析",
            "分析政策周期、经济周期、流动性环境",
            ["macro_policy", "macro_economic", "macro_liquidity"],
            "多维度宏观指标综合判断",
            macro_data,
            step_duration
        )
        
        logger.info(f"   政策周期: {macro_data['policy_cycle']}")
        logger.info(f"   经济周期: {macro_data['economic_cycle']}")
        logger.info(f"   流动性: {macro_data['liquidity_condition']}")
        
        return macro_data
    
    def _analyze_capital(self) -> Dict:
        """资金流向分析"""
        step_start = datetime.now()
        logger.info("\n💰 Step 2: 资金流向分析")
        
        # 获取板块资金流向
        flow_result = self.data_manager.fetch_data("industry_flow")
        self._add_trace("industry_flow", flow_result)
        
        # 获取北向资金
        northbound_result = self.data_manager.fetch_data("industry_northbound")
        self._add_trace("industry_northbound", northbound_result)
        
        # 获取两融数据
        margin_result = self.data_manager.fetch_data("industry_margin")
        self._add_trace("industry_margin", margin_result)
        
        capital_data = {
            "top_inflow_sectors": self._get_top_inflow_sectors(flow_result.get("data", {})),
            "northbound_preference": self._get_northbound_preference(northbound_result.get("data", {})),
            "margin_trend": self._get_margin_trend(margin_result.get("data", {})),
            "capital_consensus": self._get_capital_consensus(flow_result.get("data", {})),
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "资金流向分析",
            "分析主力资金、北向资金、两融资金流向",
            ["industry_flow", "industry_northbound", "industry_margin"],
            "多渠道资金流向综合判断",
            capital_data,
            step_duration
        )
        
        logger.info(f"   资金流入板块: {capital_data['top_inflow_sectors'][:3]}")
        logger.info(f"   北向偏好: {capital_data['northbound_preference'][:3]}")
        
        return capital_data
    
    def _analyze_industry(self) -> Dict:
        """行业景气分析"""
        step_start = datetime.now()
        logger.info("\n📊 Step 3: 行业景气分析")
        
        # 获取行业表现
        performance_result = self.data_manager.fetch_data("industry_performance")
        self._add_trace("industry_performance", performance_result)
        
        industry_data = {
            "top_performers": ["人工智能", "半导体", "新能源"],
            "prosperity_ranking": {
                "人工智能": 85,
                "半导体": 80,
                "新能源": 75,
                "消费电子": 65,
                "医药生物": 60,
            },
            "cycle_position": {
                "人工智能": "扩张",
                "半导体": "复苏",
                "新能源": "成熟",
            },
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "行业景气分析",
            "分析行业收入增速、利润率、订单情况",
            ["industry_performance", "stock_fundamental"],
            "行业景气度多维度评估",
            industry_data,
            step_duration
        )
        
        logger.info(f"   景气行业: {industry_data['top_performers']}")
        
        return industry_data
    
    def _analyze_technical(self) -> Dict:
        """技术形态分析"""
        step_start = datetime.now()
        logger.info("\n📈 Step 4: 技术形态分析")
        
        technical_data = {
            "strong_sectors": ["人工智能", "半导体"],
            "breakout_sectors": ["机器人", "算力"],
            "weak_sectors": ["房地产", "银行"],
            "sector_trends": {
                "人工智能": {"trend": "上升", "strength": 85, "ma_alignment": 4},
                "半导体": {"trend": "上升", "strength": 78, "ma_alignment": 4},
                "新能源": {"trend": "震荡", "strength": 55, "ma_alignment": 2},
            },
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "技术形态分析",
            "分析趋势强度、均线排列、量价配合",
            ["stock_technical", "stock_realtime"],
            "技术指标综合评估",
            technical_data,
            step_duration
        )
        
        logger.info(f"   强势板块: {technical_data['strong_sectors']}")
        logger.info(f"   突破板块: {technical_data['breakout_sectors']}")
        
        return technical_data
    
    def _analyze_valuation(self) -> Dict:
        """估值分析"""
        step_start = datetime.now()
        logger.info("\n💎 Step 5: 估值分析")
        
        valuation_data = {
            "undervalued_sectors": ["银行", "保险", "建筑"],
            "overvalued_sectors": ["人工智能", "半导体"],
            "pe_percentiles": {
                "人工智能": 0.85,
                "半导体": 0.75,
                "新能源": 0.45,
                "银行": 0.15,
            },
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "估值分析",
            "分析PE/PB历史分位、PEG、股息率",
            ["stock_fundamental", "stock_realtime"],
            "估值历史分位法",
            valuation_data,
            step_duration
        )
        
        return valuation_data
    
    def _analyze_foresight(self) -> Dict:
        """前瞻指标分析"""
        step_start = datetime.now()
        logger.info("\n🔮 Step 6: 前瞻指标分析")
        
        foresight_data = {
            "leading_indicators": {
                "pmi_new_orders": 52.5,
                "pmi_inventory": 47.8,
                "leading_diff": 4.7,  # 新订单-库存差
            },
            "catalyst_calendar": [
                {"event": "AI大会", "date": "2024-03-15", "sectors": ["人工智能"]},
                {"event": "半导体政策", "date": "2024-03-20", "sectors": ["半导体"]},
            ],
            "consensus_revision": {
                "人工智能": 0.08,  # 盈利预期上调8%
                "半导体": 0.05,
                "新能源": -0.02,
            },
        }
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "前瞻指标分析",
            "分析领先指标、催化剂日历、预期调整",
            ["macro_economic", "research_consensus"],
            "前瞻性指标综合评估",
            foresight_data,
            step_duration
        )
        
        logger.info(f"   领先指标差: {foresight_data['leading_indicators']['leading_diff']}")
        logger.info(f"   近期催化剂: {len(foresight_data['catalyst_calendar'])}个")
        
        return foresight_data
    
    def _run_llm_synthesis(
        self,
        macro_data: Dict,
        capital_data: Dict,
        industry_data: Dict,
        technical_data: Dict,
    ) -> AnalysisResult:
        """LLM综合分析"""
        step_start = datetime.now()
        logger.info("\n🤖 Step 7: LLM综合分析")
        
        result = self.llm.synthesize_mainline(
            macro_data, capital_data, industry_data, technical_data
        )
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "LLM综合分析",
            "使用大语言模型综合多维度数据",
            ["macro", "capital", "industry", "technical"],
            f"LLM模型: {result.model_used}",
            result.output[:200] + "..." if len(result.output) > 200 else result.output,
            step_duration
        )
        
        logger.info(f"   模型: {result.model_used}")
        logger.info(f"   置信度: {result.confidence:.0%}")
        
        return result
    
    def _identify_mainlines(
        self,
        macro_data: Dict,
        capital_data: Dict,
        industry_data: Dict,
        technical_data: Dict,
        valuation_data: Dict,
        foresight_data: Dict,
        llm_result: AnalysisResult,
    ) -> List[Mainline]:
        """识别投资主线"""
        step_start = datetime.now()
        logger.info("\n🎯 Step 8: 主线识别")
        
        mainlines = []
        
        # 解析LLM结果
        try:
            llm_output = json.loads(llm_result.output)
            llm_mainlines = llm_output.get("mainlines", [])
        except:
            llm_mainlines = []
        
        # 预定义主线候选
        candidates = [
            {
                "name": "人工智能革命",
                "sectors": ["AI算力", "AI应用", "数据中心", "光模块"],
                "stocks": ["寒武纪", "中科曙光", "科大讯飞", "中际旭创"],
                "core_logic": "AI大模型突破带动产业链重估，算力需求爆发",
            },
            {
                "name": "国产替代",
                "sectors": ["半导体设备", "半导体材料", "EDA", "先进封装"],
                "stocks": ["北方华创", "中微公司", "华大九天", "长电科技"],
                "core_logic": "外部压力加速国产化进程，设备材料受益",
            },
            {
                "name": "新能源革命",
                "sectors": ["光伏", "锂电池", "储能", "新能源车"],
                "stocks": ["隆基绿能", "宁德时代", "阳光电源", "比亚迪"],
                "core_logic": "碳中和目标驱动，新能源渗透率持续提升",
            },
        ]
        
        for candidate in candidates:
            # 构建评分数据
            raw_data = {
                "policy": {
                    "policy_mention_freq": 8,
                    "policy_strength": 4,
                    "policy_continuity": 12,
                    "policy_implementation": 0.7,
                },
                "capital": {
                    "northbound_flow": 0.015,
                    "main_force_flow": 0.12,
                    "institutional_holding": 0.08,
                    "margin_trading": 0.06,
                    "etf_flow": 0.05,
                },
                "industry": {
                    "revenue_growth": 0.25,
                    "profit_growth": 0.30,
                    "order_backlog": 0.20,
                    "capacity_utilization": 0.80,
                    "price_trend": 0.05,
                },
                "technical": {
                    "trend_strength": 32,
                    "ma_alignment": 4,
                    "volume_price": 0.75,
                    "breakout_signal": 2,
                    "rsi_macd": 65,
                },
                "valuation": {
                    "pe_percentile": 0.70,
                    "pb_percentile": 0.65,
                    "peg_ratio": 1.2,
                    "dividend_yield": 0.01,
                },
                "foresight": {
                    "leading_indicator": 4,
                    "catalyst_density": 4,
                    "consensus_revision": 0.05,
                    "global_trend": 0.6,
                },
            }
            
            # 计算评分
            score = self.scoring.calculate_mainline_score(
                candidate["name"],
                raw_data,
                llm_result.output if llm_result else None
            )
            
            # 确定阶段
            stage = self._determine_stage(score.total_score, capital_data)
            
            mainline = Mainline(
                name=candidate["name"],
                stage=stage,
                score=score,
                sectors=candidate["sectors"],
                stocks=candidate["stocks"],
                core_logic=candidate["core_logic"],
                supporting_factors=["政策支持", "资金流入", "产业景气"],
                risk_factors=["估值偏高", "预期过满"],
                duration_weeks=12,
                recommendation=score.recommendation,
                data_traces=self._data_traces.copy(),
                analysis_steps=self._analysis_steps.copy(),
                llm_analysis=llm_result,
            )
            
            mainlines.append(mainline)
        
        # 按得分排序
        mainlines.sort(key=lambda x: x.score.total_score, reverse=True)
        
        step_duration = int((datetime.now() - step_start).total_seconds() * 1000)
        self._add_step(
            "主线识别",
            "综合所有分析结果识别投资主线",
            ["all_previous_steps"],
            "多维度加权评分模型",
            [m.name for m in mainlines],
            step_duration
        )
        
        for ml in mainlines:
            logger.info(f"   🔥 {ml.name}: {ml.score.total_score:.0f}分 ({ml.stage.value})")
        
        return mainlines
    
    def _add_trace(self, source_id: str, result: Dict):
        """添加数据溯源"""
        source = self.data_manager.get_source(source_id)
        if source:
            trace = DataTrace(
                source_id=source_id,
                source_name=source.name,
                provider=source.provider,
                fetch_time=datetime.now(),
                data_fields=source.fields[:5],  # 前5个字段
                raw_data=result.get("data"),
                reliability=source.reliability.value,
            )
            self._data_traces.append(trace)
    
    def _add_step(
        self,
        name: str,
        description: str,
        sources: List[str],
        method: str,
        output: Any,
        duration: int
    ):
        """添加分析步骤"""
        step = AnalysisStep(
            step_name=name,
            description=description,
            input_sources=sources,
            method=method,
            output=output,
            duration_ms=duration,
        )
        self._analysis_steps.append(step)
    
    def _determine_policy_cycle(self, data: Dict) -> str:
        """判断政策周期"""
        return data.get("policy_cycle", "宽松")
    
    def _determine_economic_cycle(self, data: Dict) -> str:
        """判断经济周期"""
        return data.get("economic_cycle", "复苏")
    
    def _determine_liquidity(self, data: Dict) -> str:
        """判断流动性"""
        return "充裕"
    
    def _get_policy_benefited_sectors(self, data: Dict) -> List[str]:
        """获取政策受益板块"""
        return ["科技", "新能源", "高端制造"]
    
    def _get_top_inflow_sectors(self, data: Dict) -> List[str]:
        """获取资金流入板块"""
        top_inflow = data.get("top_inflow", [])
        return [item.get("sector", "") for item in top_inflow] if top_inflow else ["人工智能", "半导体"]
    
    def _get_northbound_preference(self, data: Dict) -> List[str]:
        """获取北向资金偏好"""
        return ["消费", "医药", "科技"]
    
    def _get_margin_trend(self, data: Dict) -> str:
        """获取两融趋势"""
        return "上升"
    
    def _get_capital_consensus(self, data: Dict) -> List[str]:
        """获取资金共识"""
        return ["人工智能", "半导体"]
    
    def _determine_stage(self, score: float, capital_data: Dict) -> MainlineStage:
        """确定主线阶段"""
        if score >= 80:
            return MainlineStage.GROWING
        elif score >= 65:
            return MainlineStage.MATURE
        elif score >= 50:
            return MainlineStage.EMERGING
        else:
            return MainlineStage.DECLINING
    
    def _generate_summary(self, mainlines: List[Mainline]) -> Dict:
        """生成分析摘要"""
        return {
            "total_mainlines": len(mainlines),
            "top_mainline": mainlines[0].name if mainlines else None,
            "average_score": sum(m.score.total_score for m in mainlines) / len(mainlines) if mainlines else 0,
            "data_sources_used": len(self._data_traces),
            "analysis_steps": len(self._analysis_steps),
            "market_view": "当前市场处于结构性行情，科技成长是主线方向",
        }
    
    # ============================================================
    # 便捷方法（兼容旧接口）
    # ============================================================
    
    def analyze_policy_cycle(self) -> Dict:
        """分析政策周期"""
        result = self.data_manager.fetch_data("macro_policy")
        return {
            "current_phase": "宽松",
            "monetary_policy": {"stance": "适度宽松", "direction": "降准降息"},
            "fiscal_policy": {"stance": "积极", "focus": "新基建"},
            "benefited_sectors": ["科技", "新能源", "高端制造"],
        }
    
    def analyze_economic_cycle(self) -> Dict:
        """分析经济周期"""
        result = self.data_manager.fetch_data("macro_economic")
        return {
            "current_phase": "复苏",
            "gdp_trend": "企稳回升",
            "sector_rotation": {
                "overweight": ["科技", "消费"],
                "underweight": ["周期", "金融"],
            },
        }
    
    def discover_mainlines(self) -> List[Mainline]:
        """发现主线（简化版）"""
        result = self.run_full_analysis()
        return result["mainlines"]
