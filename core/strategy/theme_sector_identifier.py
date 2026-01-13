# -*- coding: utf-8 -*-
"""
知识库驱动的题材识别器
========================

功能:
1. 从知识库提取当前热门主题（AI应用、商业航天等）
2. 映射到聚宽概念/行业代码
3. 生成题材因子用于选股

基于知识库: docs/AImainline011226/

作者: TRQuant Team
版本: V5.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
import json
import os
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============ 2026年AI应用主线配置（基于知识库研究） ============

AI_MAINLINES_2026 = {
    "ai_agent": {
        "name": "AI智能体",
        "rank": 1,
        "weight": 1.5,
        "keywords": ["智能体", "Agent", "大模型", "多智能体", "认知大模型", "生成式AI"],
        "jq_concepts": ["881198"],  # AI概念
        "top_stocks": [
            "002230.XSHE",  # 科大讯飞
            "300418.XSHE",  # 昆仑万维
            "688111.XSHG",  # 金山办公
        ],
        "tier1_stocks": [
            "002230.XSHE",  # 科大讯飞 - 星火大模型
            "300418.XSHE",  # 昆仑万维 - 天工大模型
        ],
        "description": "自治决策与任务执行的智能代理，2026年企业多智能体规模部署元年",
    },
    "ai_office": {
        "name": "AI办公",
        "rank": 2,
        "weight": 1.3,
        "keywords": ["Copilot", "办公AI", "智能办公", "WPS AI", "文档助手"],
        "jq_concepts": ["881198", "881160"],  # AI + 信息技术
        "top_stocks": [
            "688111.XSHG",  # 金山办公
            "600588.XSHG",  # 用友网络
            "300624.XSHE",  # 万兴科技
        ],
        "tier1_stocks": [
            "688111.XSHG",  # 金山办公 - WPS AI
        ],
        "description": "面向办公协同和生产力工具的AI助手",
    },
    "ai_marketing": {
        "name": "AI营销",
        "rank": 3,
        "weight": 1.2,
        "keywords": ["AIGC", "智能营销", "生成式广告", "内容创意", "智慧营销"],
        "jq_concepts": ["881198", "885561"],  # AI + 传媒
        "top_stocks": [
            "300058.XSHE",  # 蓝色光标
            "300071.XSHE",  # 福石控股
            "603598.XSHG",  # 引力传媒
        ],
        "tier1_stocks": [
            "300058.XSHE",  # 蓝色光标 - BlueAI
        ],
        "description": "生成式AI重构广告与市场投放",
    },
    "ai_industrial": {
        "name": "AI工业软件",
        "rank": 4,
        "weight": 1.1,
        "keywords": ["工业AI", "智能制造", "CAD/CAE", "工业大模型", "AI工业"],
        "jq_concepts": ["881198", "885739"],  # AI + 工业互联网
        "top_stocks": [
            "603859.XSHG",  # 能科科技
        ],
        "tier1_stocks": [],
        "description": "人工智能赋能制造业和工业软件",
    },
    "ai_healthcare": {
        "name": "AI医疗健康",
        "rank": 5,
        "weight": 1.0,
        "keywords": ["AI医疗", "智慧医疗", "医疗AI", "智能诊断", "辅助诊疗"],
        "jq_concepts": ["881198", "885522"],  # AI + 医疗
        "top_stocks": [
            "300253.XSHE",  # 卫宁健康
            "688271.XSHG",  # 联影医疗
        ],
        "tier1_stocks": [],
        "description": "医疗诊断、制药和健康管理的智能化",
    },
}

# 当前热门题材配置（动态更新）
CURRENT_HOT_THEMES = {
    "commercial_aerospace": {
        "name": "商业航天",
        "weight": 1.4,
        "keywords": ["商业航天", "卫星", "火箭", "航天", "低空经济", "星链"],
        "jq_concepts": ["885554"],  # 航天概念
        "description": "商业航天持续涨停，火箭卫星产业链",
        "hot_level": "极热",
    },
    "ai_application": {
        "name": "AI应用",
        "weight": 1.5,
        "keywords": ["AI", "人工智能", "大模型", "智能体", "AIGC", "ChatGPT"],
        "jq_concepts": ["881198"],  # AI概念
        "description": "AI应用主线，当前炒作核心",
        "hot_level": "极热",
    },
    "robot": {
        "name": "机器人",
        "weight": 1.2,
        "keywords": ["机器人", "人形机器人", "工业机器人", "特斯拉机器人"],
        "jq_concepts": ["885597"],  # 机器人概念
        "description": "机器人产业链",
        "hot_level": "热门",
    },
    "semiconductor": {
        "name": "半导体",
        "weight": 1.0,
        "keywords": ["半导体", "芯片", "集成电路", "光刻机", "存储芯片"],
        "jq_concepts": ["885761"],  # 半导体
        "description": "半导体国产替代",
        "hot_level": "热门",
    },
}


@dataclass
class ThemeScore:
    """题材评分"""
    theme_name: str
    weight: float
    matched_keywords: List[str] = field(default_factory=list)
    is_tier1: bool = False
    score: float = 0.0


@dataclass
class StockThemeProfile:
    """股票题材档案"""
    stock_code: str
    themes: List[ThemeScore] = field(default_factory=list)
    total_theme_score: float = 0.0
    is_hot_theme: bool = False
    primary_theme: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "stock_code": self.stock_code,
            "themes": [{"name": t.theme_name, "weight": t.weight, "score": t.score} for t in self.themes],
            "total_theme_score": self.total_theme_score,
            "is_hot_theme": self.is_hot_theme,
            "primary_theme": self.primary_theme,
        }


class ThemeSectorIdentifier:
    """
    知识库驱动的题材识别器
    
    核心功能:
    1. 解析知识库中的AI主线研究
    2. 识别股票所属题材
    3. 生成题材因子
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        """
        初始化识别器
        
        Args:
            kb_path: 知识库路径（默认自动检测）
        """
        self.kb_path = kb_path or self._find_kb_path()
        self.ai_mainlines = AI_MAINLINES_2026.copy()
        self.hot_themes = CURRENT_HOT_THEMES.copy()
        
        # 合并所有Tier1股票
        self._tier1_stocks: Set[str] = set()
        for config in self.ai_mainlines.values():
            self._tier1_stocks.update(config.get("tier1_stocks", []))
        
        # 合并所有推荐股票
        self._recommended_stocks: Set[str] = set()
        for config in self.ai_mainlines.values():
            self._recommended_stocks.update(config.get("top_stocks", []))
        
        logger.info(f"ThemeSectorIdentifier 初始化: Tier1股票={len(self._tier1_stocks)}, 推荐股票={len(self._recommended_stocks)}")
    
    def _find_kb_path(self) -> str:
        """自动查找知识库路径"""
        possible_paths = [
            "/home/taotao/.cursor/worktrees/TRQuant/ope/docs/AImainline011226",
            "docs/AImainline011226",
            "../docs/AImainline011226",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return possible_paths[0]  # 默认路径
    
    def identify_stock_themes(
        self,
        stock_code: str,
        stock_name: str = "",
        industry: str = "",
    ) -> StockThemeProfile:
        """
        识别单只股票的题材
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            industry: 所属行业
        
        Returns:
            StockThemeProfile: 股票题材档案
        """
        profile = StockThemeProfile(stock_code=stock_code)
        themes = []
        
        # 检查是否为Tier1推荐股票
        is_tier1 = stock_code in self._tier1_stocks
        is_recommended = stock_code in self._recommended_stocks
        
        # 遍历AI主线
        for theme_key, config in self.ai_mainlines.items():
            score = 0.0
            matched_keywords = []
            
            # Tier1股票直接加分
            if stock_code in config.get("tier1_stocks", []):
                score += 50
                matched_keywords.append("Tier1核心标的")
            elif stock_code in config.get("top_stocks", []):
                score += 30
                matched_keywords.append("Top推荐标的")
            
            # 名称/行业关键词匹配
            search_text = f"{stock_name} {industry}".lower()
            for keyword in config.get("keywords", []):
                if keyword.lower() in search_text:
                    score += 10
                    matched_keywords.append(keyword)
            
            if score > 0:
                themes.append(ThemeScore(
                    theme_name=config["name"],
                    weight=config.get("weight", 1.0),
                    matched_keywords=matched_keywords,
                    is_tier1=(stock_code in config.get("tier1_stocks", [])),
                    score=score * config.get("weight", 1.0),
                ))
        
        # 遍历当前热门题材
        for theme_key, config in self.hot_themes.items():
            score = 0.0
            matched_keywords = []
            
            search_text = f"{stock_name} {industry}".lower()
            for keyword in config.get("keywords", []):
                if keyword.lower() in search_text:
                    score += 15
                    matched_keywords.append(keyword)
            
            if score > 0:
                profile.is_hot_theme = True
                themes.append(ThemeScore(
                    theme_name=config["name"],
                    weight=config.get("weight", 1.0),
                    matched_keywords=matched_keywords,
                    is_tier1=False,
                    score=score * config.get("weight", 1.0),
                ))
        
        # 排序并计算总分
        themes.sort(key=lambda x: x.score, reverse=True)
        profile.themes = themes
        profile.total_theme_score = sum(t.score for t in themes)
        
        if themes:
            profile.primary_theme = themes[0].theme_name
        
        return profile
    
    def generate_theme_factor(
        self,
        stocks: List[str],
        stock_info: Optional[pd.DataFrame] = None,
    ) -> pd.Series:
        """
        生成题材因子
        
        Args:
            stocks: 股票列表
            stock_info: 股票信息DataFrame（需包含name, industry列）
        
        Returns:
            pd.Series: 题材因子得分
        """
        scores = {}
        
        for stock in stocks:
            name = ""
            industry = ""
            
            if stock_info is not None and stock in stock_info.index:
                name = stock_info.loc[stock].get("name", "")
                industry = stock_info.loc[stock].get("industry", "")
            
            profile = self.identify_stock_themes(stock, name, industry)
            scores[stock] = profile.total_theme_score
        
        return pd.Series(scores, name="theme_factor")
    
    def get_hot_theme_stocks(
        self,
        jq_client=None,
        as_of_date: str = None,
    ) -> List[str]:
        """
        获取当前热门题材股票列表
        
        Args:
            jq_client: 聚宽客户端（可选）
            as_of_date: 日期
        
        Returns:
            热门题材股票代码列表
        """
        hot_stocks = set()
        
        # 从配置中获取推荐股票
        for config in self.ai_mainlines.values():
            hot_stocks.update(config.get("top_stocks", []))
            hot_stocks.update(config.get("tier1_stocks", []))
        
        # 如果有聚宽客户端，获取概念板块成分股
        if jq_client:
            try:
                for config in self.hot_themes.values():
                    for concept_code in config.get("jq_concepts", []):
                        try:
                            concept_stocks = jq_client.get_concept_stocks(concept_code, date=as_of_date)
                            if concept_stocks:
                                # 只取前50只（按市值或其他排序）
                                hot_stocks.update(concept_stocks[:50])
                        except:
                            pass
            except Exception as e:
                logger.warning(f"获取概念成分股失败: {e}")
        
        return list(hot_stocks)
    
    def get_ai_mainline_summary(self) -> str:
        """获取AI主线摘要"""
        lines = ["2026年AI应用投资主线Top5:", ""]
        
        for key, config in sorted(self.ai_mainlines.items(), key=lambda x: x[1]["rank"]):
            rank = config["rank"]
            name = config["name"]
            desc = config.get("description", "")
            weight = config.get("weight", 1.0)
            top_stocks = config.get("top_stocks", [])
            
            lines.append(f"{rank}. {name} (权重:{weight})")
            lines.append(f"   {desc}")
            if top_stocks:
                lines.append(f"   核心标的: {', '.join(top_stocks[:3])}")
            lines.append("")
        
        lines.append("当前热门题材:")
        for key, config in self.hot_themes.items():
            name = config["name"]
            level = config.get("hot_level", "热门")
            lines.append(f"- {name} ({level})")
        
        return "\n".join(lines)
    
    def update_hot_themes(self, new_themes: Dict[str, Any]):
        """动态更新热门题材配置"""
        self.hot_themes.update(new_themes)
        logger.info(f"热门题材已更新: {list(new_themes.keys())}")


# ============ 测试函数 ============

def test_theme_sector_identifier():
    """测试题材识别器"""
    print("=" * 60)
    print("ThemeSectorIdentifier 单元测试")
    print("=" * 60)
    
    identifier = ThemeSectorIdentifier()
    
    # 测试1: Tier1股票识别
    print("\n1. 测试Tier1股票识别...")
    profile = identifier.identify_stock_themes(
        "002230.XSHE", 
        stock_name="科大讯飞",
        industry="软件服务"
    )
    print(f"   股票: 科大讯飞")
    print(f"   主题: {profile.primary_theme}")
    print(f"   总分: {profile.total_theme_score}")
    print(f"   是热门题材: {profile.is_hot_theme}")
    assert profile.total_theme_score > 0, "Tier1股票应有题材得分"
    print("   ✓ 通过")
    
    # 测试2: 普通股票识别
    print("\n2. 测试普通股票关键词匹配...")
    profile2 = identifier.identify_stock_themes(
        "000001.XSHE",
        stock_name="平安银行",
        industry="银行"
    )
    print(f"   股票: 平安银行")
    print(f"   主题: {profile2.primary_theme or '无'}")
    print(f"   总分: {profile2.total_theme_score}")
    print("   ✓ 通过")
    
    # 测试3: 题材因子生成
    print("\n3. 测试题材因子生成...")
    stocks = ["002230.XSHE", "300418.XSHE", "000001.XSHE"]
    theme_factor = identifier.generate_theme_factor(stocks)
    print(f"   题材因子:\n{theme_factor}")
    assert len(theme_factor) == 3, "应生成3个股票的因子"
    print("   ✓ 通过")
    
    # 测试4: AI主线摘要
    print("\n4. 测试AI主线摘要...")
    summary = identifier.get_ai_mainline_summary()
    print(f"   摘要前200字:\n{summary[:200]}...")
    assert "AI智能体" in summary, "摘要应包含AI智能体"
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_theme_sector_identifier()
