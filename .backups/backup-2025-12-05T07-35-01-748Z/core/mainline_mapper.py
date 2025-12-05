#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线映射模块

将AKShare识别的主线映射到JQData的概念/行业
支持模糊匹配和关键词匹配
"""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 尝试导入JQData
try:
    from jqdata.client import JQDataClient
    JQDATA_AVAILABLE = True
except ImportError:
    JQDATA_AVAILABLE = False
    JQDataClient = None


@dataclass
class MainlineMapping:
    """主线映射结果"""
    akshare_name: str          # AKShare主线名称
    jqdata_code: str          # JQData概念/行业代码
    jqdata_name: str          # JQData概念/行业名称
    mapping_type: str         # 'concept' 或 'industry'
    confidence: float          # 匹配置信度 0-1
    match_method: str         # 匹配方法：'exact', 'fuzzy', 'keyword'


class MainlineMapper:
    """
    主线映射器
    
    功能：
    1. 将AKShare识别的主线名称映射到JQData的概念/行业
    2. 支持精确匹配、模糊匹配、关键词匹配
    3. 缓存映射结果
    """
    
    def __init__(self, jq_client: Optional[JQDataClient] = None):
        """
        初始化映射器
        
        Args:
            jq_client: JQData客户端
        """
        self.jq_client = jq_client
        self.concept_cache = {}  # 概念列表缓存
        self.industry_cache = {}  # 行业列表缓存
        self.mapping_cache = {}  # 映射结果缓存
    
    def map_mainline(
        self,
        akshare_name: str,
        prefer_type: str = 'concept'  # 'concept' 或 'industry' 或 'auto'
    ) -> Optional[MainlineMapping]:
        """
        映射主线名称到JQData
        
        Args:
            akshare_name: AKShare主线名称
            prefer_type: 优先类型（'concept', 'industry', 'auto'）
        
        Returns:
            MainlineMapping: 映射结果，如果未找到则返回None
        """
        # 检查缓存
        cache_key = f"{akshare_name}_{prefer_type}"
        if cache_key in self.mapping_cache:
            return self.mapping_cache[cache_key]
        
        if not self.jq_client or not self.jq_client.is_authenticated():
            logger.warning("JQData未认证，无法进行映射")
            return None
        
        # 加载概念和行业列表
        if not self.concept_cache:
            self._load_concepts()
        if not self.industry_cache:
            self._load_industries()
        
        # 尝试映射
        mapping = None
        
        # 1. 优先在指定类型中查找
        if prefer_type == 'concept':
            mapping = self._find_in_concepts(akshare_name)
        elif prefer_type == 'industry':
            mapping = self._find_in_industries(akshare_name)
        else:  # auto
            # 先尝试概念，再尝试行业
            mapping = self._find_in_concepts(akshare_name)
            if not mapping:
                mapping = self._find_in_industries(akshare_name)
        
        # 缓存结果
        if mapping:
            self.mapping_cache[cache_key] = mapping
        
        return mapping
    
    def map_multiple_mainlines(
        self,
        akshare_names: List[str],
        prefer_type: str = 'auto'
    ) -> Dict[str, Optional[MainlineMapping]]:
        """
        批量映射主线
        
        Args:
            akshare_names: AKShare主线名称列表
            prefer_type: 优先类型
        
        Returns:
            Dict: {akshare_name: MainlineMapping}
        """
        results = {}
        for name in akshare_names:
            results[name] = self.map_mainline(name, prefer_type)
        return results
    
    def _load_concepts(self):
        """加载JQData概念列表"""
        if not self.jq_client:
            return
        
        try:
            concepts = self.jq_client.get_all_concepts()
            if concepts is not None and not concepts.empty:
                for code, row in concepts.iterrows():
                    name = row.get('name', '')
                    self.concept_cache[code] = name
                logger.info(f"✅ 加载概念列表: {len(self.concept_cache)} 个")
        except Exception as e:
            logger.warning(f"加载概念列表失败: {e}")
    
    def _load_industries(self):
        """加载JQData行业列表"""
        if not self.jq_client:
            return
        
        try:
            industries = self.jq_client.get_all_industries()
            if industries is not None and not industries.empty:
                for code, row in industries.iterrows():
                    name = row.get('name', '')
                    self.industry_cache[code] = name
                logger.info(f"✅ 加载行业列表: {len(self.industry_cache)} 个")
        except Exception as e:
            logger.warning(f"加载行业列表失败: {e}")
    
    def _find_in_concepts(self, akshare_name: str) -> Optional[MainlineMapping]:
        """在概念中查找"""
        return self._find_match(akshare_name, self.concept_cache, 'concept')
    
    def _find_in_industries(self, akshare_name: str) -> Optional[MainlineMapping]:
        """在行业中查找"""
        return self._find_match(akshare_name, self.industry_cache, 'industry')
    
    def _find_match(
        self,
        akshare_name: str,
        jqdata_dict: Dict[str, str],
        mapping_type: str
    ) -> Optional[MainlineMapping]:
        """
        查找匹配
        
        匹配策略（按优先级）：
        1. 精确匹配
        2. 包含匹配（akshare_name in jqdata_name 或反之）
        3. 关键词匹配
        """
        akshare_clean = self._clean_name(akshare_name)
        best_match = None
        best_score = 0.0
        best_method = None
        
        for code, jqdata_name in jqdata_dict.items():
            jqdata_clean = self._clean_name(jqdata_name)
            
            # 1. 精确匹配
            if akshare_clean == jqdata_clean:
                return MainlineMapping(
                    akshare_name=akshare_name,
                    jqdata_code=code,
                    jqdata_name=jqdata_name,
                    mapping_type=mapping_type,
                    confidence=1.0,
                    match_method='exact'
                )
            
            # 2. 包含匹配
            if akshare_clean in jqdata_clean:
                score = len(akshare_clean) / len(jqdata_clean)
                if score > best_score:
                    best_score = score
                    best_match = (code, jqdata_name)
                    best_method = 'fuzzy_contain'
            elif jqdata_clean in akshare_clean:
                score = len(jqdata_clean) / len(akshare_clean)
                if score > best_score:
                    best_score = score
                    best_match = (code, jqdata_name)
                    best_method = 'fuzzy_contain'
            
            # 3. 关键词匹配
            akshare_keywords = self._extract_keywords(akshare_clean)
            jqdata_keywords = self._extract_keywords(jqdata_clean)
            
            if akshare_keywords and jqdata_keywords:
                common_keywords = set(akshare_keywords) & set(jqdata_keywords)
                if common_keywords:
                    score = len(common_keywords) / max(len(akshare_keywords), len(jqdata_keywords))
                    if score > best_score:
                        best_score = score
                        best_match = (code, jqdata_name)
                        best_method = 'keyword'
        
        if best_match and best_score >= 0.3:  # 最低置信度阈值
            return MainlineMapping(
                akshare_name=akshare_name,
                jqdata_code=best_match[0],
                jqdata_name=best_match[1],
                mapping_type=mapping_type,
                confidence=best_score,
                match_method=best_method
            )
        
        return None
    
    def _clean_name(self, name: str) -> str:
        """清理名称（去除空格、标点等）"""
        if not name:
            return ""
        # 去除常见后缀
        name = name.replace("概念", "").replace("板块", "").replace("行业", "")
        name = name.replace(" ", "").strip()
        return name
    
    def _extract_keywords(self, name: str) -> List[str]:
        """提取关键词（2-4字）"""
        keywords = []
        if len(name) >= 2:
            # 提取2字词
            for i in range(len(name) - 1):
                keywords.append(name[i:i+2])
        if len(name) >= 3:
            # 提取3字词
            for i in range(len(name) - 2):
                keywords.append(name[i:i+3])
        if len(name) >= 4:
            # 提取4字词
            for i in range(len(name) - 3):
                keywords.append(name[i:i+4])
        return keywords
    
    def get_recommended_features(
        self,
        mapping: MainlineMapping,
        period: str = 'medium'
    ) -> Dict[str, any]:
        """
        获取推荐的特征条件
        
        Args:
            mapping: 主线映射结果
            period: 期限（short/medium/long）
        
        Returns:
            Dict: 推荐的特征条件
        """
        features = {
            'period': period,
            'mainline_type': mapping.mapping_type,
            'momentum_weight': 0.5,
            'growth_weight': 0.5,
            'min_momentum_score': 60.0,
            'min_growth_score': 60.0,
            'min_composite_score': 65.0,
        }
        
        # 根据期限调整权重
        if period == 'short':
            features['momentum_weight'] = 0.7
            features['growth_weight'] = 0.3
            features['min_momentum_score'] = 70.0
        elif period == 'long':
            features['momentum_weight'] = 0.3
            features['growth_weight'] = 0.7
            features['min_growth_score'] = 70.0
        
        # 根据映射类型调整
        if mapping.mapping_type == 'concept':
            # 概念板块通常更关注短期动量
            if period == 'short':
                features['min_momentum_score'] = 75.0
        elif mapping.mapping_type == 'industry':
            # 行业板块更关注长期成长
            if period == 'long':
                features['min_growth_score'] = 75.0
        
        return features

