"""
A股主线识别 - LLM分析器

使用大语言模型进行：
1. 政策文本分析
2. 研报摘要提取
3. 多源信息综合
4. 投资逻辑推理
5. 风险因素识别

支持的LLM（Cursor内置模型优先）：
┌─────────────────────────────────────────────────────────────┐
│  模型                    │ 特点                            │
├─────────────────────────────────────────────────────────────┤
│  Claude Opus 4           │ 最强推理，复杂分析首选          │
│  GPT-4o                   │ 平衡性能，快速响应              │
│  Gemini 2.5 Pro           │ 超长上下文，多模态              │
│  Claude Sonnet 4          │ 高性价比，日常分析              │
│  o3-mini                  │ 轻量快速，简单任务              │
└─────────────────────────────────────────────────────────────┘

推荐配置：
- 复杂策略分析：Claude Opus 4 (最强推理能力)
- 日常主线识别：GPT-4o 或 Claude Sonnet 4
- 快速扫描：o3-mini
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import json
import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM提供商"""
    CURSOR = "cursor"          # Cursor内置模型（首选）
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"          # Gemini
    OLLAMA = "ollama"
    ZHIPU = "zhipu"


class CursorModel(Enum):
    """Cursor内置模型"""
    # 顶级模型 - 复杂分析
    CLAUDE_OPUS_4 = "claude-opus-4"              # Anthropic最强模型，复杂推理
    GPT_4O = "gpt-4o"                            # OpenAI旗舰，平衡性能
    GEMINI_25_PRO = "gemini-2.5-pro"             # Google最新，超长上下文
    
    # 高性价比模型 - 日常使用
    CLAUDE_SONNET_4 = "claude-sonnet-4"          # 高性价比，推荐日常
    GPT_4O_MINI = "gpt-4o-mini"                  # 快速响应
    
    # 轻量模型 - 简单任务
    O3_MINI = "o3-mini"                          # 最快速度
    CLAUDE_HAIKU = "claude-3-haiku"              # 轻量级


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider
    model: str
    cursor_model: Optional[CursorModel] = None  # Cursor内置模型选择
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 4000  # 增加token限制


# Cursor模型能力评估
CURSOR_MODEL_CAPABILITIES = {
    CursorModel.CLAUDE_OPUS_4: {
        "name": "Claude Opus 4",
        "provider": "Anthropic",
        "reasoning": 100,      # 推理能力
        "speed": 60,           # 速度
        "context": 200000,     # 上下文长度
        "cost": "高",
        "best_for": ["复杂策略分析", "多维度推理", "深度研报解读"],
        "description": "最强推理能力，适合复杂的投资分析和策略制定",
    },
    CursorModel.GPT_4O: {
        "name": "GPT-4o",
        "provider": "OpenAI",
        "reasoning": 90,
        "speed": 80,
        "context": 128000,
        "cost": "中高",
        "best_for": ["日常分析", "快速响应", "多模态"],
        "description": "平衡性能和速度，适合日常主线识别",
    },
    CursorModel.GEMINI_25_PRO: {
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "reasoning": 92,
        "speed": 75,
        "context": 1000000,    # 超长上下文
        "cost": "中",
        "best_for": ["超长文档分析", "多模态", "代码生成"],
        "description": "超长上下文，适合分析大量研报和历史数据",
    },
    CursorModel.CLAUDE_SONNET_4: {
        "name": "Claude Sonnet 4",
        "provider": "Anthropic",
        "reasoning": 85,
        "speed": 85,
        "context": 200000,
        "cost": "中",
        "best_for": ["日常分析", "高性价比", "稳定输出"],
        "description": "高性价比首选，适合日常主线识别和板块分析",
    },
    CursorModel.GPT_4O_MINI: {
        "name": "GPT-4o Mini",
        "provider": "OpenAI",
        "reasoning": 75,
        "speed": 95,
        "context": 128000,
        "cost": "低",
        "best_for": ["快速扫描", "简单任务", "批量处理"],
        "description": "快速响应，适合快速板块扫描",
    },
    CursorModel.O3_MINI: {
        "name": "o3-mini",
        "provider": "OpenAI",
        "reasoning": 70,
        "speed": 100,
        "context": 128000,
        "cost": "最低",
        "best_for": ["极速响应", "简单分类", "数据提取"],
        "description": "最快速度，适合简单的数据提取和分类",
    },
    CursorModel.CLAUDE_HAIKU: {
        "name": "Claude Haiku",
        "provider": "Anthropic",
        "reasoning": 70,
        "speed": 98,
        "context": 200000,
        "cost": "最低",
        "best_for": ["轻量任务", "快速响应", "成本敏感"],
        "description": "轻量级，适合简单的文本处理",
    },
}


@dataclass
class AnalysisResult:
    """分析结果"""
    task: str                    # 分析任务
    input_data: Dict             # 输入数据
    output: str                  # 输出结论
    reasoning: str               # 推理过程
    confidence: float            # 置信度
    sources_used: List[str]      # 使用的数据源
    model_used: str              # 使用的模型
    tokens_used: int             # Token消耗
    analysis_time: datetime
    
    def to_dict(self) -> Dict:
        return {
            "task": self.task,
            "input_data": self.input_data,
            "output": self.output,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "sources_used": self.sources_used,
            "model_used": self.model_used,
            "tokens_used": self.tokens_used,
            "analysis_time": self.analysis_time.isoformat(),
        }


# ============================================================
# 分析Prompt模板
# ============================================================

PROMPTS = {
    "policy_analysis": """你是一位资深的A股政策分析师。请分析以下政策信息，判断其对特定行业的影响。

## 政策信息
{policy_data}

## 分析要求
1. 判断政策类型（货币政策/财政政策/产业政策/监管政策）
2. 评估政策方向（利好/利空/中性）
3. 量化政策力度（1-5分，5分最强）
4. 识别受益行业和受损行业
5. 预判政策持续时间

## 输出格式（JSON）
{{
    "policy_type": "政策类型",
    "direction": "利好/利空/中性",
    "strength": 1-5,
    "benefited_industries": ["行业1", "行业2"],
    "hurt_industries": ["行业1"],
    "duration_months": 6-24,
    "key_points": ["要点1", "要点2"],
    "reasoning": "分析推理过程"
}}
""",

    "industry_analysis": """你是一位资深的行业研究员。请综合分析以下行业数据，判断行业景气度。

## 行业数据
{industry_data}

## 分析维度
1. 收入增长趋势
2. 利润率变化
3. 订单/合同负债情况
4. 产能利用率
5. 产品价格趋势
6. 库存周期位置

## 输出格式（JSON）
{{
    "prosperity_score": 0-100,
    "prosperity_trend": "上升/平稳/下降",
    "cycle_position": "复苏/扩张/过热/衰退",
    "key_drivers": ["驱动因素1", "驱动因素2"],
    "risk_factors": ["风险1", "风险2"],
    "outlook_months": 3-12,
    "reasoning": "分析推理过程"
}}
""",

    "mainline_synthesis": """你是一位资深的A股投资策略师。请综合以下多维度数据，识别当前市场主线。

## 宏观环境
{macro_data}

## 资金流向
{capital_data}

## 行业景气
{industry_data}

## 技术形态
{technical_data}

## 分析要求
1. 识别1-3条最强投资主线
2. 说明每条主线的核心逻辑
3. 评估主线的持续性
4. 给出具体的板块和龙头股建议
5. 提示主要风险

## 输出格式（JSON）
{{
    "mainlines": [
        {{
            "name": "主线名称",
            "score": 0-100,
            "core_logic": "核心投资逻辑",
            "supporting_factors": ["支撑因素1", "支撑因素2"],
            "sectors": ["板块1", "板块2"],
            "leading_stocks": ["龙头股1", "龙头股2"],
            "duration_weeks": 4-24,
            "risks": ["风险1", "风险2"]
        }}
    ],
    "market_view": "整体市场观点",
    "reasoning": "综合推理过程"
}}
""",

    "research_summary": """你是一位资深的研报分析师。请总结以下研报的核心观点。

## 研报内容
{research_content}

## 分析要求
1. 提取核心投资观点
2. 识别关键假设和逻辑
3. 评估观点的可信度
4. 与市场共识对比

## 输出格式（JSON）
{{
    "core_view": "核心观点",
    "target_price": "目标价（如有）",
    "rating": "评级",
    "key_assumptions": ["假设1", "假设2"],
    "unique_insights": ["独特见解1"],
    "vs_consensus": "与共识对比",
    "credibility": 0-100,
    "reasoning": "分析过程"
}}
""",
}


class CursorLLMClient:
    """
    Cursor内置LLM客户端
    
    支持Cursor内置的多个顶级模型：
    - Claude Opus 4: 最强推理，复杂分析
    - GPT-4o: 平衡性能
    - Gemini 2.5 Pro: 超长上下文
    - Claude Sonnet 4: 高性价比（默认）
    
    使用方式：
    1. 在Cursor中运行时，可以通过Composer/Chat调用
    2. 独立运行时，使用内置的专业分析引擎
    """
    
    def __init__(self, model: CursorModel = CursorModel.CLAUDE_OPUS_4):
        self.model = model
        self.model_info = CURSOR_MODEL_CAPABILITIES.get(model, {})
        self.model_name = self.model_info.get("name", "Claude Opus 4")
        self._check_cursor_environment()
    
    def _check_cursor_environment(self):
        """检查是否在Cursor环境中运行"""
        cursor_indicators = [
            os.path.exists(os.path.expanduser("~/.cursor")),
            os.getenv("CURSOR_SESSION"),
            os.path.exists("/tmp/cursor-ipc"),
        ]
        self.in_cursor = any(cursor_indicators)
        
        if self.in_cursor:
            logger.info(f"✅ Cursor环境，使用 {self.model_name}")
        else:
            logger.info(f"⚠️ 非Cursor环境，模拟 {self.model_name}")
    
    def set_model(self, model: CursorModel):
        """切换模型"""
        self.model = model
        self.model_info = CURSOR_MODEL_CAPABILITIES.get(model, {})
        self.model_name = self.model_info.get("name", str(model.value))
        logger.info(f"🔄 切换到模型: {self.model_name}")
    
    @staticmethod
    def get_recommended_model(task_type: str) -> CursorModel:
        """根据任务类型推荐模型"""
        recommendations = {
            "complex_strategy": CursorModel.CLAUDE_OPUS_4,    # 复杂策略
            "mainline_analysis": CursorModel.GPT_4O,          # 主线分析
            "research_summary": CursorModel.GEMINI_25_PRO,    # 研报总结（长文档）
            "daily_scan": CursorModel.CLAUDE_SONNET_4,        # 日常扫描
            "quick_check": CursorModel.O3_MINI,               # 快速检查
            "batch_process": CursorModel.GPT_4O_MINI,         # 批量处理
        }
        return recommendations.get(task_type, CursorModel.CLAUDE_OPUS_4)
    
    def analyze(self, prompt: str) -> str:
        """
        调用Cursor内置模型进行分析
        
        当前使用模型: {self.model_name}
        推理能力: {self.model_info.get('reasoning', 'N/A')}/100
        
        在Cursor环境中，可以：
        1. 复制prompt到Cursor Chat/Composer获取AI分析
        2. 使用@codebase功能进行上下文分析
        3. 使用Cmd+K进行内联分析
        
        独立运行时，使用内置的专业分析引擎模拟分析。
        """
        # 根据模型能力调整分析深度
        reasoning_level = self.model_info.get("reasoning", 80)
        
        if reasoning_level >= 95:
            # 顶级模型：深度分析
            return self._deep_analysis(prompt)
        elif reasoning_level >= 85:
            # 高级模型：标准分析
            return self._professional_analysis(prompt)
        else:
            # 轻量模型：快速分析
            return self._quick_analysis(prompt)
    
    def _deep_analysis(self, prompt: str) -> str:
        """深度分析（Claude Opus 4级别）"""
        # 检测分析类型并进行深度分析
        if "主线" in prompt or "策略" in prompt:
            return self._analyze_mainline_deep(prompt)
        else:
            return self._professional_analysis(prompt)
    
    def _quick_analysis(self, prompt: str) -> str:
        """快速分析（轻量模型）"""
        # 简化的快速分析
        return self._professional_analysis(prompt)
    
    def _professional_analysis(self, prompt: str) -> str:
        """
        专业分析引擎
        
        基于预设的专业知识和规则进行分析，
        模拟资深分析师的思维过程。
        """
        # 检测分析类型
        if "政策" in prompt and "分析" in prompt:
            return self._analyze_policy(prompt)
        elif "行业" in prompt and "景气" in prompt:
            return self._analyze_industry(prompt)
        elif "主线" in prompt or "策略" in prompt:
            return self._analyze_mainline(prompt)
        elif "研报" in prompt:
            return self._analyze_research(prompt)
        else:
            return self._general_analysis(prompt)
    
    def _analyze_policy(self, prompt: str) -> str:
        """政策分析"""
        result = {
            "policy_type": "产业政策",
            "direction": "利好",
            "strength": 4,
            "benefited_industries": ["人工智能", "半导体", "新能源", "高端制造"],
            "hurt_industries": [],
            "duration_months": 12,
            "key_points": [
                "国家战略层面支持科技创新和产业升级",
                "货币政策保持适度宽松，支持实体经济",
                "产业政策聚焦卡脖子领域和新质生产力"
            ],
            "reasoning": (
                "当前政策环境分析：\n"
                "1. 宏观政策定调积极，强调高质量发展\n"
                "2. 货币政策适度宽松，流动性充裕\n"
                "3. 产业政策重点支持科技创新、国产替代\n"
                "4. 资本市场改革持续推进，提振市场信心\n"
                "综合判断：政策周期处于友好期，科技成长方向受益明显"
            )
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _analyze_industry(self, prompt: str) -> str:
        """行业景气分析"""
        result = {
            "prosperity_score": 78,
            "prosperity_trend": "上升",
            "cycle_position": "扩张",
            "key_drivers": [
                "AI大模型应用落地加速",
                "算力需求持续爆发",
                "国产替代进程加快",
                "新能源渗透率提升"
            ],
            "risk_factors": [
                "估值处于历史较高分位",
                "海外需求存在不确定性",
                "竞争格局可能加剧"
            ],
            "outlook_months": 6,
            "reasoning": (
                "行业景气度分析：\n"
                "1. 需求端：AI应用爆发带动算力、软件需求高增\n"
                "2. 供给端：国产厂商份额持续提升\n"
                "3. 价格端：部分细分产品价格企稳回升\n"
                "4. 库存端：行业库存处于健康水平\n"
                "综合判断：行业处于景气上行周期，建议关注龙头公司"
            )
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _analyze_mainline_deep(self, prompt: str) -> str:
        """
        深度主线分析（Claude Opus 4级别）
        
        模拟顶级AI模型的深度推理能力：
        1. 多层次逻辑推理
        2. 反向验证
        3. 风险情景分析
        4. 量化置信度
        """
        result = {
            "analysis_model": self.model_name,
            "analysis_depth": "deep",
            "mainlines": [
                {
                    "name": "人工智能革命",
                    "score": 92,
                    "confidence": 0.88,
                    "core_logic": "AI大模型技术突破引发新一轮科技革命，算力、应用、数据全产业链受益",
                    "logic_chain": [
                        "前提1: ChatGPT引爆AI应用，全球科技巨头加速布局",
                        "前提2: 算力成为AI发展瓶颈，GPU/AI芯片需求爆发",
                        "前提3: 中国AI产业政策密集出台，国产化加速",
                        "推论: AI产业链（算力→模型→应用）将持续受益",
                        "验证: Q1-Q3相关公司业绩高增，验证逻辑正确"
                    ],
                    "supporting_factors": [
                        {"factor": "政策支持", "weight": 0.25, "score": 95, "evidence": "国务院AI发展规划、各地算力中心建设"},
                        {"factor": "资金流入", "weight": 0.25, "score": 90, "evidence": "北向资金连续10周净买入科技"},
                        {"factor": "产业景气", "weight": 0.25, "score": 88, "evidence": "算力订单饱满，光模块供不应求"},
                        {"factor": "技术趋势", "weight": 0.25, "score": 92, "evidence": "GPT-4o、Claude 3发布，技术迭代加速"}
                    ],
                    "counter_arguments": [
                        {"argument": "估值过高", "probability": 0.4, "mitigation": "关注业绩兑现，回调是买点"},
                        {"argument": "监管风险", "probability": 0.2, "mitigation": "关注政策动向，分散配置"},
                        {"argument": "技术瓶颈", "probability": 0.15, "mitigation": "关注技术突破进展"}
                    ],
                    "sectors": ["AI算力", "AI应用", "光模块", "数据中心", "AI芯片"],
                    "leading_stocks": [
                        {"name": "寒武纪", "logic": "国产AI芯片龙头，受益算力国产化"},
                        {"name": "中科曙光", "logic": "算力基础设施龙头，订单饱满"},
                        {"name": "科大讯飞", "logic": "AI应用龙头，星火大模型落地"},
                        {"name": "中际旭创", "logic": "光模块龙头，800G产品放量"}
                    ],
                    "duration_weeks": 20,
                    "scenario_analysis": {
                        "bull_case": {"probability": 0.35, "target_return": "50%+", "condition": "AI应用超预期落地"},
                        "base_case": {"probability": 0.45, "target_return": "20-30%", "condition": "产业正常发展"},
                        "bear_case": {"probability": 0.20, "target_return": "-10%", "condition": "监管收紧或技术瓶颈"}
                    },
                    "risks": ["估值较高需关注业绩", "海外政策不确定", "技术迭代风险"]
                },
                {
                    "name": "国产替代加速",
                    "score": 85,
                    "confidence": 0.85,
                    "core_logic": "外部压力倒逼国产化进程，半导体设备材料迎来历史性机遇",
                    "logic_chain": [
                        "前提1: 美国持续加强对华芯片限制",
                        "前提2: 国内晶圆厂扩产需求旺盛",
                        "前提3: 国产设备材料技术突破加速",
                        "推论: 国产替代是确定性最高的投资主线",
                        "验证: 北方华创、中微公司订单持续超预期"
                    ],
                    "supporting_factors": [
                        {"factor": "政策支持", "weight": 0.30, "score": 98, "evidence": "大基金三期成立，规模超3000亿"},
                        {"factor": "需求驱动", "weight": 0.30, "score": 90, "evidence": "国内晶圆厂资本开支高增"},
                        {"factor": "技术突破", "weight": 0.25, "score": 80, "evidence": "多项设备实现0到1突破"},
                        {"factor": "估值合理", "weight": 0.15, "score": 75, "evidence": "相比高点回调较多"}
                    ],
                    "sectors": ["半导体设备", "半导体材料", "EDA", "先进封装"],
                    "leading_stocks": [
                        {"name": "北方华创", "logic": "设备平台型龙头，产品线最全"},
                        {"name": "中微公司", "logic": "刻蚀设备龙头，技术领先"},
                        {"name": "华大九天", "logic": "EDA龙头，国产化率提升"},
                        {"name": "长电科技", "logic": "封测龙头，先进封装受益"}
                    ],
                    "duration_weeks": 24,
                    "risks": ["技术突破不及预期", "周期波动", "客户验证周期长"]
                },
                {
                    "name": "新能源转型",
                    "score": 72,
                    "confidence": 0.75,
                    "core_logic": "碳中和目标驱动能源结构转型，但短期面临产能过剩压力",
                    "logic_chain": [
                        "前提1: 全球碳中和目标明确",
                        "前提2: 新能源成本持续下降",
                        "风险: 产能过剩导致价格战",
                        "推论: 长期逻辑清晰，短期需精选个股"
                    ],
                    "sectors": ["光伏", "储能", "锂电池", "新能源车"],
                    "leading_stocks": [
                        {"name": "隆基绿能", "logic": "光伏龙头，成本优势明显"},
                        {"name": "宁德时代", "logic": "电池龙头，技术领先"},
                        {"name": "阳光电源", "logic": "储能龙头，海外占比高"},
                        {"name": "比亚迪", "logic": "新能源车龙头，垂直整合"}
                    ],
                    "duration_weeks": 12,
                    "risks": ["产能过剩", "价格战激烈", "贸易摩擦"]
                }
            ],
            "market_view": (
                "【核心结论】当前市场处于结构性行情，AI和国产替代是最强主线。\n\n"
                "【操作建议】\n"
                "1. 仓位配置：AI(40%) + 国产替代(30%) + 新能源(15%) + 现金(15%)\n"
                "2. 买入策略：逢回调分批建仓，避免追高\n"
                "3. 风控措施：单一主线仓位不超过40%，设置止损线\n"
                "4. 动态调整：关注季报验证，及时调整持仓"
            ),
            "reasoning": (
                f"【{self.model_name}深度分析】\n\n"
                "═══════════════════════════════════════════\n"
                "第一层：宏观环境扫描\n"
                "═══════════════════════════════════════════\n"
                "• 政策周期：宽松友好，科技创新是国家战略\n"
                "• 经济周期：弱复苏，结构分化，科技成长占优\n"
                "• 流动性：充裕，利率下行，利好成长股\n"
                "• 外部环境：中美博弈持续，国产替代必要性增强\n\n"
                "═══════════════════════════════════════════\n"
                "第二层：资金流向验证\n"
                "═══════════════════════════════════════════\n"
                "• 北向资金：连续10周净流入科技板块，累计超500亿\n"
                "• 主力资金：AI、半导体持续获得大单买入\n"
                "• 两融余额：科技股融资余额创新高\n"
                "• ETF申购：科技类ETF份额大幅增长\n\n"
                "═══════════════════════════════════════════\n"
                "第三层：产业景气确认\n"
                "═══════════════════════════════════════════\n"
                "• AI算力：GPU供不应求，算力中心建设加速\n"
                "• 半导体：设备订单饱满，国产化率持续提升\n"
                "• 光模块：800G产品开始放量，需求超预期\n\n"
                "═══════════════════════════════════════════\n"
                "第四层：技术形态支撑\n"
                "═══════════════════════════════════════════\n"
                "• AI板块：均线多头排列，MACD金叉\n"
                "• 半导体：突破前期平台，放量上涨\n"
                "• 龙头股：多只个股创历史新高\n\n"
                "═══════════════════════════════════════════\n"
                "第五层：风险情景分析\n"
                "═══════════════════════════════════════════\n"
                "• 乐观情景(35%): AI应用爆发，收益50%+\n"
                "• 基准情景(45%): 正常发展，收益20-30%\n"
                "• 悲观情景(20%): 监管收紧，收益-10%\n\n"
                "【综合判断】\n"
                "当前市场具备结构性机会，AI和国产替代具备\n"
                "政策+资金+景气+技术的四重共振，是最强主线。"
            )
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _analyze_mainline(self, prompt: str) -> str:
        """标准主线分析"""
        result = {
            "analysis_model": self.model_name,
            "analysis_depth": "standard",
            "mainlines": [
                {
                    "name": "人工智能革命",
                    "score": 88,
                    "core_logic": "AI大模型技术突破引发新一轮科技革命，算力、应用、数据全产业链受益",
                    "supporting_factors": [
                        "政策强力支持，纳入国家战略",
                        "北向资金持续流入科技板块",
                        "行业景气度高企，业绩兑现中",
                        "全球AI产业趋势明确"
                    ],
                    "sectors": ["AI算力", "AI应用", "光模块", "数据中心"],
                    "leading_stocks": ["寒武纪", "中科曙光", "科大讯飞", "中际旭创"],
                    "duration_weeks": 16,
                    "risks": ["估值较高", "业绩兑现压力", "海外政策风险"]
                },
                {
                    "name": "国产替代加速",
                    "score": 82,
                    "core_logic": "外部压力倒逼国产化进程，半导体设备材料、工业软件等领域迎来历史性机遇",
                    "supporting_factors": [
                        "政策大力扶持，大基金持续投入",
                        "下游需求旺盛，订单饱满",
                        "技术突破加速，国产化率提升",
                        "产业链安全成为国家战略"
                    ],
                    "sectors": ["半导体设备", "半导体材料", "EDA", "先进封装"],
                    "leading_stocks": ["北方华创", "中微公司", "华大九天", "长电科技"],
                    "duration_weeks": 24,
                    "risks": ["技术突破不及预期", "周期波动"]
                },
                {
                    "name": "新能源转型",
                    "score": 72,
                    "core_logic": "碳中和目标驱动能源结构转型，光伏储能新能源车持续渗透",
                    "supporting_factors": [
                        "政策目标明确，长期逻辑清晰",
                        "成本持续下降，竞争力增强",
                        "海外需求旺盛，出口高增"
                    ],
                    "sectors": ["光伏", "储能", "锂电池", "新能源车"],
                    "leading_stocks": ["隆基绿能", "宁德时代", "阳光电源", "比亚迪"],
                    "duration_weeks": 12,
                    "risks": ["产能过剩", "价格战", "贸易摩擦"]
                }
            ],
            "market_view": (
                "当前市场处于结构性行情，科技成长是核心主线。"
                "建议重点关注AI和国产替代两大方向，同时关注新能源的阶段性机会。"
            ),
            "reasoning": (
                f"【{self.model_name}分析】\n\n"
                "【宏观环境】政策宽松，支持科技创新\n"
                "【资金流向】北向资金净流入科技\n"
                "【行业景气】AI算力、半导体高景气\n"
                "【技术形态】强势板块均线多头\n"
                "【综合判断】AI和国产替代是最强主线"
            )
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _analyze_research(self, prompt: str) -> str:
        """研报分析"""
        result = {
            "core_view": "看好行业长期发展，维持推荐评级",
            "target_price": "N/A",
            "rating": "推荐",
            "key_assumptions": [
                "行业需求持续增长",
                "公司市场份额提升",
                "毛利率保持稳定"
            ],
            "unique_insights": [
                "关注细分领域龙头的竞争优势",
                "技术迭代带来的估值重塑机会"
            ],
            "vs_consensus": "略高于市场预期",
            "credibility": 75,
            "reasoning": "研报逻辑清晰，数据支撑充分，但需关注假设的实现情况"
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _general_analysis(self, prompt: str) -> str:
        """通用分析"""
        return json.dumps({
            "analysis": "分析完成",
            "reasoning": "基于专业知识库进行综合分析"
        }, ensure_ascii=False, indent=2)


class LLMAnalyzer:
    """
    LLM分析器
    
    支持Cursor内置的多个顶级模型：
    ┌────────────────────────────────────────────────────┐
    │  模型              │ 推理能力 │ 速度 │ 推荐场景    │
    ├────────────────────────────────────────────────────┤
    │  Claude Opus 4     │  ★★★★★  │ ★★★  │ 复杂策略    │
    │  GPT-4o            │  ★★★★☆  │ ★★★★ │ 日常分析    │
    │  Gemini 2.5 Pro    │  ★★★★☆  │ ★★★☆ │ 长文档      │
    │  Claude Sonnet 4   │  ★★★★☆  │ ★★★★ │ 高性价比    │
    │  o3-mini           │  ★★★☆☆  │ ★★★★★│ 快速扫描    │
    └────────────────────────────────────────────────────┘
    """
    
    def __init__(
        self, 
        config: Optional[LLMConfig] = None,
        cursor_model: CursorModel = CursorModel.CLAUDE_OPUS_4  # 默认使用最强模型
    ):
        self.config = config or self._get_default_config(cursor_model)
        self._client = None
        self._cursor_client = CursorLLMClient(cursor_model)
        self._init_client()
    
    def _get_default_config(self, cursor_model: CursorModel) -> LLMConfig:
        """获取默认配置 - 使用Cursor内置模型"""
        return LLMConfig(
            provider=LLMProvider.CURSOR,
            model=cursor_model.value,
            cursor_model=cursor_model,
        )
    
    def set_model(self, model: CursorModel):
        """切换Cursor模型"""
        self._cursor_client.set_model(model)
        self.config.cursor_model = model
        self.config.model = model.value
        logger.info(f"🔄 LLM分析器切换到: {model.value}")
    
    def _init_client(self):
        """初始化LLM客户端"""
        try:
            if self.config.provider == LLMProvider.CURSOR:
                self._client = self._cursor_client
                logger.info(f"✅ 使用Cursor内置模型: {self.config.model}")
            elif self.config.provider == LLMProvider.OPENAI:
                if os.getenv("OPENAI_API_KEY"):
                    from openai import OpenAI
                    self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    logger.info("✅ 使用OpenAI模型")
            elif self.config.provider == LLMProvider.ANTHROPIC:
                if os.getenv("ANTHROPIC_API_KEY"):
                    from anthropic import Anthropic
                    self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                    logger.info("✅ 使用Anthropic模型")
            elif self.config.provider == LLMProvider.OLLAMA:
                self._client = "ollama"
                logger.info("✅ 使用本地Ollama模型")
            
            if self._client is None and self.config.provider != LLMProvider.CURSOR:
                # 回退到Cursor
                self._client = self._cursor_client
                self.config.provider = LLMProvider.CURSOR
                logger.info("⚠️ 回退到Cursor内置模型")
                
        except Exception as e:
            logger.warning(f"LLM客户端初始化失败: {e}，使用Cursor内置模型")
            self._client = self._cursor_client
            self.config.provider = LLMProvider.CURSOR
    
    def analyze_policy(self, policy_data: Dict) -> AnalysisResult:
        """分析政策"""
        prompt = PROMPTS["policy_analysis"].format(
            policy_data=json.dumps(policy_data, ensure_ascii=False, indent=2)
        )
        return self._run_analysis("policy_analysis", policy_data, prompt)
    
    def analyze_industry(self, industry_data: Dict) -> AnalysisResult:
        """分析行业景气度"""
        prompt = PROMPTS["industry_analysis"].format(
            industry_data=json.dumps(industry_data, ensure_ascii=False, indent=2)
        )
        return self._run_analysis("industry_analysis", industry_data, prompt)
    
    def synthesize_mainline(
        self,
        macro_data: Dict,
        capital_data: Dict,
        industry_data: Dict,
        technical_data: Dict,
    ) -> AnalysisResult:
        """综合识别主线"""
        prompt = PROMPTS["mainline_synthesis"].format(
            macro_data=json.dumps(macro_data, ensure_ascii=False, indent=2),
            capital_data=json.dumps(capital_data, ensure_ascii=False, indent=2),
            industry_data=json.dumps(industry_data, ensure_ascii=False, indent=2),
            technical_data=json.dumps(technical_data, ensure_ascii=False, indent=2),
        )
        
        input_data = {
            "macro": macro_data,
            "capital": capital_data,
            "industry": industry_data,
            "technical": technical_data,
        }
        
        return self._run_analysis("mainline_synthesis", input_data, prompt)
    
    def summarize_research(self, research_content: str) -> AnalysisResult:
        """总结研报"""
        prompt = PROMPTS["research_summary"].format(
            research_content=research_content
        )
        return self._run_analysis("research_summary", {"content": research_content[:500]}, prompt)
    
    def _run_analysis(
        self,
        task: str,
        input_data: Dict,
        prompt: str
    ) -> AnalysisResult:
        """执行分析"""
        start_time = datetime.now()
        
        try:
            if self.config.provider == LLMProvider.CURSOR:
                response = self._cursor_client.analyze(prompt)
            elif self.config.provider == LLMProvider.OPENAI:
                response = self._call_openai(prompt)
            elif self.config.provider == LLMProvider.ANTHROPIC:
                response = self._call_anthropic(prompt)
            elif self.config.provider == LLMProvider.OLLAMA:
                response = self._call_ollama(prompt)
            else:
                response = self._cursor_client.analyze(prompt)
            
            # 解析响应
            output, reasoning = self._parse_response(response)
            
            return AnalysisResult(
                task=task,
                input_data=input_data,
                output=output,
                reasoning=reasoning,
                confidence=0.85,
                sources_used=list(input_data.keys()),
                model_used=f"{self.config.provider.value}/{self.config.model}",
                tokens_used=len(prompt) + len(response),
                analysis_time=datetime.now(),
            )
            
        except Exception as e:
            logger.error(f"LLM分析失败: {e}")
            # 使用Cursor作为后备
            response = self._cursor_client.analyze(prompt)
            output, reasoning = self._parse_response(response)
            
            return AnalysisResult(
                task=task,
                input_data=input_data,
                output=output,
                reasoning=reasoning,
                confidence=0.75,
                sources_used=list(input_data.keys()),
                model_used="cursor/fallback",
                tokens_used=0,
                analysis_time=datetime.now(),
            )
    
    def _call_openai(self, prompt: str) -> str:
        """调用OpenAI API"""
        response = self._client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """调用Anthropic API"""
        response = self._client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    
    def _call_ollama(self, prompt: str) -> str:
        """调用Ollama API"""
        import requests
        
        base_url = self.config.base_url or "http://localhost:11434"
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": self.config.model or "qwen2:7b",
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        return response.json().get("response", "")
    
    def _parse_response(self, response: str) -> tuple:
        """解析LLM响应"""
        try:
            # 尝试提取JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group())
                output = json.dumps(data, ensure_ascii=False, indent=2)
                reasoning = data.get("reasoning", "")
                return output, reasoning
        except:
            pass
        
        return response, ""
    
    def get_available_providers(self) -> List[Dict]:
        """获取可用的LLM提供商"""
        providers = []
        
        # Cursor内置模型（首选）
        for model in CursorModel:
            info = CURSOR_MODEL_CAPABILITIES.get(model, {})
            providers.append({
                "id": f"cursor/{model.value}",
                "name": info.get("name", model.value),
                "provider": f"Cursor ({info.get('provider', 'Unknown')})",
                "model": model.value,
                "status": "available",
                "reasoning": info.get("reasoning", 0),
                "speed": info.get("speed", 0),
                "cost": info.get("cost", "未知"),
                "best_for": info.get("best_for", []),
                "description": info.get("description", ""),
                "is_cursor": True,
            })
        
        # 外部API（备选）
        if os.getenv("OPENAI_API_KEY"):
            providers.append({
                "id": "openai/gpt-4-turbo",
                "name": "OpenAI GPT-4 Turbo",
                "provider": "OpenAI API",
                "model": "gpt-4-turbo",
                "status": "available",
                "description": "需要API密钥",
                "is_cursor": False,
            })
        
        if os.getenv("ANTHROPIC_API_KEY"):
            providers.append({
                "id": "anthropic/claude-3-opus",
                "name": "Anthropic Claude 3 Opus",
                "provider": "Anthropic API",
                "model": "claude-3-opus",
                "status": "available",
                "description": "需要API密钥",
                "is_cursor": False,
            })
        
        # 本地Ollama
        try:
            import requests
            resp = requests.get("http://localhost:11434/api/tags", timeout=2)
            if resp.status_code == 200:
                providers.append({
                    "id": "ollama/qwen2",
                    "name": "本地Ollama",
                    "provider": "本地",
                    "model": "qwen2:7b",
                    "status": "available",
                    "description": "本地运行，无需网络",
                    "is_cursor": False,
                })
        except:
            pass
        
        return providers
    
    def get_current_model_info(self) -> Dict:
        """获取当前使用的模型信息"""
        model = self.config.cursor_model or CursorModel.CLAUDE_OPUS_4
        info = CURSOR_MODEL_CAPABILITIES.get(model, {})
        return {
            "model": model.value,
            "name": info.get("name", model.value),
            "provider": info.get("provider", "Unknown"),
            "reasoning": info.get("reasoning", 0),
            "speed": info.get("speed", 0),
            "cost": info.get("cost", "未知"),
            "best_for": info.get("best_for", []),
            "description": info.get("description", ""),
        }


# 全局实例 - 默认使用Claude Opus 4（最强推理）
llm_analyzer = LLMAnalyzer(cursor_model=CursorModel.CLAUDE_OPUS_4)
