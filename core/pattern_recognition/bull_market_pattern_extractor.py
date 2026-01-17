#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市专属模式提取器

对牛市高回报案例进行聚类分析，识别不同的高回报模式（动量突破、板块轮动、龙头效应等），
并分析每类模式的因子分布特征，生成牛市专属选股条件。
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


@dataclass
class PatternCluster:
    """模式聚类"""
    pattern_name: str            # 模式名称（如：动量突破、低位反弹）
    pattern_type: str            # 模式类型（momentum_breakout, low_bounce, sector_rotation等）
    cluster_id: int              # 聚类ID
    case_count: int              # 案例数量
    avg_return: float            # 平均收益率
    
    # 因子分布特征（中位数）
    momentum_20d_median: float = 0.0
    momentum_5d_median: float = 0.0
    rel_position_median: float = 0.0
    market_cap_median: float = 0.0
    turnover_rate_median: float = 0.0
    roe_median: float = 0.0
    growth_median: float = 0.0
    
    # 因子分布特征（分位数）
    momentum_20d_p25: float = 0.0
    momentum_20d_p75: float = 0.0
    momentum_5d_p25: float = 0.0
    momentum_5d_p75: float = 0.0
    rel_position_p25: float = 0.0
    rel_position_p75: float = 0.0
    
    # 选股条件（提炼）
    selection_conditions: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'pattern_name': self.pattern_name,
            'pattern_type': self.pattern_type,
            'cluster_id': self.cluster_id,
            'case_count': self.case_count,
            'avg_return': self.avg_return,
            'momentum_20d_median': self.momentum_20d_median,
            'momentum_5d_median': self.momentum_5d_median,
            'rel_position_median': self.rel_position_median,
            'market_cap_median': self.market_cap_median,
            'turnover_rate_median': self.turnover_rate_median,
            'roe_median': self.roe_median,
            'growth_median': self.growth_median,
            'momentum_20d_range': (self.momentum_20d_p25, self.momentum_20d_p75),
            'momentum_5d_range': (self.momentum_5d_p25, self.momentum_5d_p75),
            'rel_position_range': (self.rel_position_p25, self.rel_position_p75),
            'selection_conditions': self.selection_conditions,
        }


class BullMarketPatternExtractor:
    """牛市专属模式提取器"""
    
    # 因子列
    FACTOR_COLS = [
        'momentum_20d', 'momentum_5d', 'rel_position',
        'market_cap', 'turnover_rate', 'roe', 'growth'
    ]
    
    def __init__(self, n_clusters: int = 4, verbose: bool = True):
        """
        初始化
        
        Args:
            n_clusters: 聚类数量（默认4类：动量突破、低位反弹、板块轮动、龙头效应）
            verbose: 是否输出详细信息
        """
        self.n_clusters = n_clusters
        self.verbose = verbose
        self.scaler = StandardScaler()
    
    def load_cases_from_csv(self, csv_path: str) -> pd.DataFrame:
        """从CSV文件加载案例"""
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        if self.verbose:
            print(f"\n✅ 加载案例: {len(df)} 个")
            print(f"  时间范围: {df['week_start'].min()} ~ {df['week_end'].max()}")
            print(f"  平均收益率: {df['return_pct'].mean():.2f}%")
            print(f"  中位数收益率: {df['return_pct'].median():.2f}%")
        
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """准备特征矩阵"""
        # 选择因子列
        feature_cols = [col for col in self.FACTOR_COLS if col in df.columns]
        
        # 提取特征
        X = df[feature_cols].values
        
        # 处理缺失值（用中位数填充）
        X = pd.DataFrame(X, columns=feature_cols).fillna(
            pd.DataFrame(X, columns=feature_cols).median()
        ).values
        
        # 标准化（用于聚类）
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, feature_cols
    
    def cluster_cases(self, df: pd.DataFrame) -> pd.DataFrame:
        """对案例进行聚类"""
        # 准备特征
        X_scaled, feature_cols = self.prepare_features(df)
        
        # K-means聚类
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        df['cluster_id'] = kmeans.fit_predict(X_scaled)
        
        if self.verbose:
            print(f"\n✅ 聚类完成: {self.n_clusters} 个类别")
            for i in range(self.n_clusters):
                cluster_df = df[df['cluster_id'] == i]
                print(f"  类别 {i}: {len(cluster_df)} 个案例, 平均收益率 {cluster_df['return_pct'].mean():.2f}%")
        
        return df
    
    def identify_pattern_type(self, cluster_df: pd.DataFrame) -> Tuple[str, str]:
        """
        识别模式类型
        
        Returns:
            (pattern_name, pattern_type): 模式名称和类型
        """
        # 计算特征中位数
        med_m20 = cluster_df['momentum_20d'].median()
        med_m5 = cluster_df['momentum_5d'].median()
        med_rp = cluster_df['rel_position'].median()
        med_mc = cluster_df['market_cap'].median()
        avg_return = cluster_df['return_pct'].mean()
        
        # 模式识别逻辑
        if med_m20 > 15.0 and med_rp > 70.0:
            return "动量突破型", "momentum_breakout"
        elif med_m5 < 0 and med_rp < 40.0:
            return "低位反弹型", "low_bounce"
        elif med_mc > 100.0 and med_m20 > 10.0:
            return "龙头效应型", "leader_effect"
        elif med_m20 > 5.0 and med_rp > 50.0 and avg_return > 15.0:
            return "板块轮动型", "sector_rotation"
        else:
            return f"混合型-{int(med_m20)}", "mixed"
    
    def extract_pattern_statistics(self, df: pd.DataFrame) -> List[PatternCluster]:
        """提取每类模式的统计特征"""
        patterns = []
        
        for cluster_id in range(self.n_clusters):
            cluster_df = df[df['cluster_id'] == cluster_id]
            
            if len(cluster_df) == 0:
                continue
            
            # 识别模式类型
            pattern_name, pattern_type = self.identify_pattern_type(cluster_df)
            
            # 计算因子分布（中位数和分位数）
            pattern = PatternCluster(
                pattern_name=pattern_name,
                pattern_type=pattern_type,
                cluster_id=cluster_id,
                case_count=len(cluster_df),
                avg_return=cluster_df['return_pct'].mean(),
                
                # 中位数
                momentum_20d_median=cluster_df['momentum_20d'].median(),
                momentum_5d_median=cluster_df['momentum_5d'].median(),
                rel_position_median=cluster_df['rel_position'].median(),
                market_cap_median=cluster_df['market_cap'].median(),
                turnover_rate_median=cluster_df['turnover_rate'].median(),
                roe_median=cluster_df['roe'].median(),
                growth_median=cluster_df['growth'].median(),
                
                # 分位数
                momentum_20d_p25=cluster_df['momentum_20d'].quantile(0.25),
                momentum_20d_p75=cluster_df['momentum_20d'].quantile(0.75),
                momentum_5d_p25=cluster_df['momentum_5d'].quantile(0.25),
                momentum_5d_p75=cluster_df['momentum_5d'].quantile(0.75),
                rel_position_p25=cluster_df['rel_position'].quantile(0.25),
                rel_position_p75=cluster_df['rel_position'].quantile(0.75),
            )
            
            # 提炼选股条件
            pattern.selection_conditions = self._extract_selection_conditions(cluster_df)
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_selection_conditions(self, cluster_df: pd.DataFrame) -> Dict:
        """提炼选股条件（基于分位数）"""
        conditions = {}
        
        # 动量20日
        m20_p25 = cluster_df['momentum_20d'].quantile(0.25)
        m20_p75 = cluster_df['momentum_20d'].quantile(0.75)
        conditions['momentum_20d'] = (m20_p25, m20_p75)
        
        # 动量5日
        m5_p25 = cluster_df['momentum_5d'].quantile(0.25)
        m5_p75 = cluster_df['momentum_5d'].quantile(0.75)
        conditions['momentum_5d'] = (m5_p25, m5_p75)
        
        # 相对位置
        rp_p25 = cluster_df['rel_position'].quantile(0.25)
        rp_p75 = cluster_df['rel_position'].quantile(0.75)
        conditions['rel_position'] = (rp_p25, rp_p75)
        
        # 市值
        mc_p25 = cluster_df['market_cap'].quantile(0.25)
        mc_p75 = cluster_df['market_cap'].quantile(0.75)
        conditions['market_cap'] = (mc_p25, mc_p75)
        
        # 换手率
        tr_p25 = cluster_df['turnover_rate'].quantile(0.25)
        tr_p75 = cluster_df['turnover_rate'].quantile(0.75)
        conditions['turnover_rate'] = (tr_p25, tr_p75)
        
        # ROE
        roe_p25 = cluster_df['roe'].quantile(0.25)
        roe_p75 = cluster_df['roe'].quantile(0.75)
        conditions['roe'] = (roe_p25, roe_p75)
        
        # 增长率
        growth_p25 = cluster_df['growth'].quantile(0.25)
        growth_p75 = cluster_df['growth'].quantile(0.75)
        conditions['growth'] = (growth_p25, growth_p75)
        
        return conditions
    
    def extract_patterns(self, cases_df: pd.DataFrame) -> List[PatternCluster]:
        """
        提取模式（完整流程）
        
        Args:
            cases_df: 高回报案例DataFrame
        
        Returns:
            模式列表
        """
        if self.verbose:
            print(f"\n开始提取模式...")
            print(f"  案例数量: {len(cases_df)}")
            print(f"  聚类数量: {self.n_clusters}")
        
        # 聚类
        clustered_df = self.cluster_cases(cases_df)
        
        # 提取统计特征
        patterns = self.extract_pattern_statistics(clustered_df)
        
        # 输出结果
        if self.verbose:
            print(f"\n✅ 模式提取完成: {len(patterns)} 个模式")
            for pattern in patterns:
                print(f"\n【{pattern.pattern_name}】 ({pattern.pattern_type})")
                print(f"  案例数量: {pattern.case_count}")
                print(f"  平均收益率: {pattern.avg_return:.2f}%")
                print(f"  因子特征:")
                print(f"    momentum_20d: {pattern.momentum_20d_median:.2f}% ({pattern.momentum_20d_p25:.2f}~{pattern.momentum_20d_p75:.2f})")
                print(f"    momentum_5d: {pattern.momentum_5d_median:.2f}% ({pattern.momentum_5d_p25:.2f}~{pattern.momentum_5d_p75:.2f})")
                print(f"    rel_position: {pattern.rel_position_median:.2f}% ({pattern.rel_position_p25:.2f}~{pattern.rel_position_p75:.2f})")
                print(f"    market_cap: {pattern.market_cap_median:.2f}亿")
                print(f"  选股条件:")
                for factor, (p25, p75) in pattern.selection_conditions.items():
                    print(f"    {factor}: [{p25:.2f}, {p75:.2f}]")
        
        return patterns
    
    def save_patterns(self, patterns: List[PatternCluster], output_path: str):
        """保存模式到JSON文件"""
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        patterns_dict = [pattern.to_dict() for pattern in patterns]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(patterns_dict, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"\n✅ 已保存到: {output_file}")
            print(f"  模式数量: {len(patterns)}")


def main():
    """主函数：示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='提取牛市专属模式')
    parser.add_argument('--input', type=str, required=True, help='输入CSV文件路径（高回报案例）')
    parser.add_argument('--n-clusters', type=int, default=4, help='聚类数量')
    parser.add_argument('--output', type=str, default='data/bull_market_patterns.json', help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    # 创建提取器
    extractor = BullMarketPatternExtractor(n_clusters=args.n_clusters, verbose=True)
    
    # 加载案例
    cases_df = extractor.load_cases_from_csv(args.input)
    
    # 提取模式
    patterns = extractor.extract_patterns(cases_df)
    
    # 保存结果
    if patterns:
        extractor.save_patterns(patterns, args.output)
    else:
        print("⚠️ 未提取到任何模式")


if __name__ == '__main__':
    main()
