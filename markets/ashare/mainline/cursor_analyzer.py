"""
A股主线识别 - Cursor交互分析器

将真实数据转换为Cursor可分析的Prompt，
用户可以在Cursor Chat/Composer中进行深度分析。

工作流程：
1. 从AKShare获取真实数据
2. 整理数据生成分析Prompt
3. 用户复制Prompt到Cursor进行AI分析
4. 或者保存Prompt文件，用@file引用分析
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

from .real_data_fetcher import RealDataFetcher, real_data_fetcher, DataFetchResult

logger = logging.getLogger(__name__)


@dataclass
class AnalysisPrompt:
    """分析Prompt"""
    title: str
    prompt: str
    data_sources: List[str]
    data_time: datetime
    file_path: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "prompt": self.prompt,
            "data_sources": self.data_sources,
            "data_time": self.data_time.isoformat(),
            "file_path": self.file_path,
        }


class CursorAnalyzer:
    """
    Cursor交互分析器
    
    使用方法：
    1. 调用 generate_mainline_prompt() 生成分析Prompt
    2. 复制Prompt到Cursor Chat进行分析
    3. 或者调用 save_prompt_file() 保存为文件，用@file引用
    """
    
    def __init__(self, data_fetcher: Optional[RealDataFetcher] = None):
        self.fetcher = data_fetcher or real_data_fetcher
        self.prompt_dir = os.path.expanduser("~/.local/share/trquant/prompts")
        os.makedirs(self.prompt_dir, exist_ok=True)
    
    def generate_mainline_prompt(self) -> AnalysisPrompt:
        """
        生成主线识别分析Prompt
        
        包含真实的市场数据，供Cursor AI分析
        """
        # 获取真实数据
        logger.info("📡 获取真实市场数据...")
        all_data = self.fetcher.fetch_all_data()
        
        # 构建数据摘要
        data_summary = self._build_data_summary(all_data)
        
        # 生成Prompt
        prompt = f"""# A股主线识别分析请求

## 📅 数据时间
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 真实市场数据

{data_summary}

## 🎯 分析任务

请基于以上真实市场数据，完成以下分析：

### 1. 宏观环境判断
- 当前政策周期（宽松/中性/收紧）
- 经济周期阶段（复苏/扩张/过热/衰退）
- 流动性状况

### 2. 资金流向分析
- 主力资金流向哪些板块？
- 北向资金偏好什么方向？
- 资金共识在哪里？

### 3. 主线识别
识别1-3条最强投资主线，每条主线包含：
- 主线名称和核心逻辑
- 支撑因素（政策/资金/产业/技术）
- 相关板块和龙头股
- 风险提示

### 4. 投资建议
- 仓位配置建议
- 买入/卖出时机
- 风控措施

## 📝 输出格式

请以JSON格式输出分析结果：
```json
{{
    "analysis_time": "分析时间",
    "data_sources": ["数据来源列表"],
    "macro_environment": {{
        "policy_cycle": "政策周期",
        "economic_cycle": "经济周期",
        "liquidity": "流动性状况"
    }},
    "capital_flow": {{
        "main_force_direction": ["主力流向"],
        "northbound_preference": ["北向偏好"],
        "consensus": ["资金共识"]
    }},
    "mainlines": [
        {{
            "name": "主线名称",
            "score": 0-100,
            "core_logic": "核心逻辑",
            "supporting_factors": ["支撑因素"],
            "sectors": ["相关板块"],
            "leading_stocks": ["龙头股"],
            "risks": ["风险"]
        }}
    ],
    "investment_advice": {{
        "position": "仓位建议",
        "timing": "时机建议",
        "risk_control": "风控措施"
    }},
    "reasoning": "完整推理过程"
}}
```
"""
        
        # 记录使用的数据源
        data_sources = [
            f"{key}: {result.source}" 
            for key, result in all_data.items() 
            if result.success
        ]
        
        return AnalysisPrompt(
            title="A股主线识别分析",
            prompt=prompt,
            data_sources=data_sources,
            data_time=datetime.now(),
        )
    
    def _build_data_summary(self, all_data: Dict[str, DataFetchResult]) -> str:
        """构建数据摘要"""
        sections = []
        
        # 板块资金流向
        sector_flow = all_data.get("sector_flow")
        if sector_flow and sector_flow.success and sector_flow.data:
            sections.append("### 📈 板块资金流向（实时）")
            sections.append(f"数据来源: {sector_flow.source}")
            sections.append("")
            sections.append("| 板块 | 涨跌幅 | 主力净流入(亿) | 主力净占比 |")
            sections.append("|------|--------|----------------|------------|")
            for item in sector_flow.data[:15]:
                sections.append(
                    f"| {item['sector_name']} | "
                    f"{item['change_pct']:.2f}% | "
                    f"{item['main_net_inflow']:.2f} | "
                    f"{item['main_net_ratio']:.2f}% |"
                )
            sections.append("")
        
        # 概念板块
        concept = all_data.get("concept_board")
        if concept and concept.success and concept.data:
            sections.append("### 🔥 热门概念板块")
            sections.append(f"数据来源: {concept.source}")
            sections.append("")
            sections.append("| 概念 | 涨跌幅 | 领涨股 | 领涨幅度 |")
            sections.append("|------|--------|--------|----------|")
            for item in concept.data[:15]:
                sections.append(
                    f"| {item['board_name']} | "
                    f"{item['change_pct']:.2f}% | "
                    f"{item['leader_stock']} | "
                    f"{item['leader_change']:.2f}% |"
                )
            sections.append("")
        
        # 北向资金
        north = all_data.get("northbound_flow")
        if north and north.success and north.data:
            sections.append("### 💰 北向资金流向")
            sections.append(f"数据来源: {north.source}")
            sections.append("")
            sections.append(f"- 今日净流入: {north.data.get('today_net', 0):.2f}亿")
            sections.append(f"- 本周净流入: {north.data.get('week_net', 0):.2f}亿")
            sections.append(f"- 本月净流入: {north.data.get('month_net', 0):.2f}亿")
            sections.append("")
        
        # 市场情绪
        sentiment = all_data.get("market_sentiment")
        if sentiment and sentiment.success and sentiment.data:
            sections.append("### 🎭 市场情绪")
            sections.append(f"数据来源: {sentiment.source}")
            sections.append("")
            sections.append(f"- 涨停家数: {sentiment.data.get('up_limit_count', 0)}")
            sections.append(f"- 跌停家数: {sentiment.data.get('down_limit_count', 0)}")
            sections.append(f"- 情绪得分: {sentiment.data.get('sentiment_score', 50)}/100")
            
            continuous = sentiment.data.get('continuous_limit', {})
            if continuous:
                sections.append(f"- 连板分布: {json.dumps(continuous, ensure_ascii=False)}")
            sections.append("")
        
        # 龙虎榜
        dragon = all_data.get("dragon_tiger")
        if dragon and dragon.success and dragon.data:
            sections.append("### 🐉 龙虎榜")
            sections.append(f"数据来源: {dragon.source}")
            sections.append("")
            sections.append("| 股票 | 上榜原因 | 净买额(万) |")
            sections.append("|------|----------|------------|")
            for item in dragon.data[:10]:
                sections.append(
                    f"| {item['name']} | "
                    f"{item['reason'][:15]} | "
                    f"{item['net_buy']:.0f} |"
                )
            sections.append("")
        
        # 宏观数据
        macro = all_data.get("macro_data")
        if macro and macro.success and macro.data:
            sections.append("### 📋 宏观经济数据")
            sections.append(f"数据来源: {macro.source}")
            sections.append("")
            if "pmi" in macro.data:
                sections.append(f"- PMI: {macro.data['pmi'].get('value', 'N/A')}")
            if "m2_growth" in macro.data:
                sections.append(f"- M2增速: {macro.data['m2_growth']}%")
            sections.append("")
        
        return "\n".join(sections)
    
    def save_prompt_file(self, prompt: AnalysisPrompt) -> str:
        """
        保存Prompt到文件，方便在Cursor中用@file引用
        """
        filename = f"mainline_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.prompt_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt.prompt)
        
        prompt.file_path = filepath
        logger.info(f"✅ Prompt已保存: {filepath}")
        
        return filepath
    
    def get_cursor_instructions(self, prompt: AnalysisPrompt) -> str:
        """
        获取Cursor使用说明
        """
        instructions = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🤖 Cursor AI 分析指南                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📊 数据已准备完毕！                                              ║
║                                                                  ║
║  使用方法：                                                       ║
║                                                                  ║
║  方法1: 直接复制分析                                              ║
║  ────────────────────                                            ║
║  1. 复制下方Prompt                                                ║
║  2. 打开Cursor Chat (Cmd+L)                                       ║
║  3. 粘贴并发送                                                    ║
║  4. 选择模型: Claude Opus 4 (推荐) 或 GPT-4o                      ║
║                                                                  ║
║  方法2: 文件引用分析                                              ║
║  ────────────────────                                            ║
║  1. Prompt已保存到: {prompt.file_path or '(未保存)'}
║  2. 在Cursor Chat中输入: @{os.path.basename(prompt.file_path) if prompt.file_path else 'file'}
║  3. 发送分析请求                                                  ║
║                                                                  ║
║  📡 数据来源:                                                     ║
║  {chr(10).join(['║  - ' + s for s in prompt.data_sources[:5]])}
║                                                                  ║
║  ⏰ 数据时间: {prompt.data_time.strftime('%Y-%m-%d %H:%M:%S')}
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return instructions
    
    def run_analysis(self) -> Dict:
        """
        运行完整分析流程
        
        Returns:
            {
                "prompt": AnalysisPrompt,
                "file_path": str,
                "instructions": str,
                "data_status": Dict,
            }
        """
        # 生成Prompt
        prompt = self.generate_mainline_prompt()
        
        # 保存到文件
        file_path = self.save_prompt_file(prompt)
        
        # 获取使用说明
        instructions = self.get_cursor_instructions(prompt)
        
        # 数据状态
        data_status = self.fetcher.get_data_status()
        
        return {
            "prompt": prompt,
            "file_path": file_path,
            "instructions": instructions,
            "data_status": data_status,
        }


# 全局实例
cursor_analyzer = CursorAnalyzer()

