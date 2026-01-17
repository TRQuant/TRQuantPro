"""
JQData 因子计算器（V4.0 周频版）- 补充因子
==========================================

定位：
- **补充角色**：作为已验证因子的补充（30%权重），而非主要因子来源
- **主要因子来源**：优先使用ValidatedFactorCalculator（基于历史10%+案例验证的因子，70%权重）

因子来源：
- CNE5风格因子：size, beta, momentum, liquidity, residual_volatility
- Alpha101/191技术因子：alpha_001 ~ alpha_005（Top5）
- 基础财务因子：ROE, PE, PB, 净利润增长率, 营收增长率

注意：
- 本模块不依赖 Notebook 代码
- 所有日期口径以"交易日"为准，但策略/预测口径以"周"为单位
- **重要**：不能简单堆砌聚宽因子库，必须与已验证因子结合使用
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


DEFAULT_CNE5_FACTORS: Tuple[str, ...] = (
    "size",
    "beta",
    "momentum",
    "liquidity",
    "residual_volatility",
)

DEFAULT_ALPHA_TOP: Tuple[str, ...] = (
    "alpha_001",
    "alpha_002",
    "alpha_003",
    "alpha_004",
    "alpha_005",
)


@dataclass
class JQFactorWeights:
    """综合得分权重（精简版）"""

    cne5: float = 0.40
    alpha: float = 0.35
    fundamental: float = 0.25


class JQFactorCalculator:
    """聚宽因子计算器（CNE5 + Alpha101/191 + 基础财务）"""

    def __init__(
        self,
        weights: Optional[JQFactorWeights] = None,
        alpha101_list: Sequence[str] = DEFAULT_ALPHA_TOP,
        alpha191_list: Sequence[str] = DEFAULT_ALPHA_TOP,
        cne5_factors: Sequence[str] = DEFAULT_CNE5_FACTORS,
        verbose: bool = True,
    ):
        self.weights = weights or JQFactorWeights()
        self.alpha101_list = list(alpha101_list)
        self.alpha191_list = list(alpha191_list)
        self.cne5_factors = list(cne5_factors)
        self.verbose = verbose

        self.jq = None
        self._init_jqdata()

    def _init_jqdata(self) -> None:
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager

            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config("jqdata")
            jq.auth(jq_config.get("username"), jq_config.get("password"))
            self.jq = jq
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
            raise

    @staticmethod
    def _zscore(series: pd.Series) -> pd.Series:
        series = pd.to_numeric(series, errors="coerce")
        std = series.std(ddof=0)
        if std == 0 or np.isnan(std):
            return pd.Series(0.0, index=series.index)
        return (series - series.mean()) / std

    @staticmethod
    def _to_long_factor_values(values: Dict[str, pd.DataFrame], codes: List[str], end_date: str) -> pd.DataFrame:
        """将 get_factor_values 的返回格式转换为 DataFrame(code, factor...)"""
        out = pd.DataFrame({"code": codes})
        for f, df in values.items():
            try:
                # 常见结构：index=日期, columns=证券
                if isinstance(df, pd.DataFrame) and len(df) > 0:
                    row = df.iloc[-1]
                    out[f] = [row.get(c, np.nan) for c in codes]
                else:
                    out[f] = np.nan
            except Exception:
                out[f] = np.nan
        return out

    def calculate_cne5_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """获取 CNE5 风格因子（原始值 + zscore）"""
        if not codes:
            return pd.DataFrame(columns=["code"])

        values = self.jq.get_factor_values(
            securities=codes,
            factors=self.cne5_factors,
            count=1,
            end_date=date,
        )
        df = self._to_long_factor_values(values, codes, date)

        # 标准化
        for f in self.cne5_factors:
            df[f"{f}_z"] = self._zscore(df[f])

        df["cne5_score_raw"] = df[[f"{f}_z" for f in self.cne5_factors]].mean(axis=1)
        df["cne5_score"] = df["cne5_score_raw"].rank(pct=True) * 100
        return df

    def calculate_alpha_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """获取 Alpha101/Alpha191 精选因子（原始值 + zscore + 合成得分）"""
        if not codes:
            return pd.DataFrame(columns=["code"])

        import jqdatasdk.alpha101 as a101
        import jqdatasdk.alpha191 as a191

        df = pd.DataFrame({"code": codes})

        # Alpha101: 函数签名一般为 (enddate, index='all')，index可传入股票列表
        for name in self.alpha101_list:
            func = getattr(a101, name, None)
            if func is None:
                df[f"{name}_a101"] = np.nan
                continue
            try:
                s = func(enddate=date, index=codes)
                df[f"{name}_a101"] = df["code"].map(s.to_dict())
            except Exception as e:
                logger.warning(f"Alpha101计算失败 {name}@{date}: {e}")
                df[f"{name}_a101"] = np.nan

        # Alpha191: 函数签名一般为 (code, end_date=None, fq='pre')，code可传入股票列表
        for name in self.alpha191_list:
            func = getattr(a191, name, None)
            if func is None:
                df[f"{name}_a191"] = np.nan
                continue
            try:
                s = func(codes, end_date=date, fq="pre")
                df[f"{name}_a191"] = df["code"].map(s.to_dict())
            except Exception as e:
                logger.warning(f"Alpha191计算失败 {name}@{date}: {e}")
                df[f"{name}_a191"] = np.nan

        # zscore + 平均
        z_cols = []
        for col in df.columns:
            if col == "code":
                continue
            z = f"{col}_z"
            df[z] = self._zscore(df[col])
            z_cols.append(z)

        df["alpha_score_raw"] = df[z_cols].mean(axis=1)
        df["alpha_score"] = df["alpha_score_raw"].rank(pct=True) * 100
        return df

    def calculate_fundamental_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """基础财务因子（精简）"""
        if not codes:
            return pd.DataFrame(columns=["code"])

        q = self.jq.query(
            self.jq.valuation.code,
            self.jq.valuation.market_cap,
            self.jq.valuation.pe_ratio,
            self.jq.valuation.pb_ratio,
            self.jq.indicator.roe,
            self.jq.indicator.inc_net_profit_year_on_year,
            self.jq.indicator.inc_revenue_year_on_year,
        ).filter(self.jq.valuation.code.in_(codes))

        df = self.jq.get_fundamentals(q, date=date)
        if df is None or df.empty:
            return pd.DataFrame({"code": codes})

        df = df.rename(
            columns={
                "inc_net_profit_year_on_year": "growth",
                "inc_revenue_year_on_year": "revenue_growth",
            }
        )

        # 标准化方向：roe/growth/revenue_growth 越大越好；pe/pb 越小越好
        df["roe_z"] = self._zscore(df["roe"])
        df["growth_z"] = self._zscore(df["growth"])
        df["revenue_growth_z"] = self._zscore(df["revenue_growth"])
        df["pe_z"] = -self._zscore(df["pe_ratio"])
        df["pb_z"] = -self._zscore(df["pb_ratio"])

        df["fundamental_score_raw"] = df[["roe_z", "growth_z", "revenue_growth_z", "pe_z", "pb_z"]].mean(axis=1)
        df["fundamental_score"] = df["fundamental_score_raw"].rank(pct=True) * 100
        return df

    def calculate_all_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """
        综合计算并输出综合得分（0~100）
        
        注意：
        - 本方法计算聚宽因子库的因子（CNE5 + Alpha101/191 + 基础财务）
        - 这些因子作为已验证因子的补充，在MultiFactorCalculator中与已验证因子融合
        - 最终得分：70%已验证因子 + 30%聚宽因子
        - 不能简单堆砌聚宽因子库，必须与已验证因子结合使用
        """
        if not codes:
            return pd.DataFrame(columns=["code"])

        cne5 = self.calculate_cne5_factors(codes, date)
        alpha = self.calculate_alpha_factors(codes, date)
        funda = self.calculate_fundamental_factors(codes, date)

        df = pd.DataFrame({"code": codes})
        df = df.merge(cne5, on="code", how="left").merge(alpha, on="code", how="left").merge(funda, on="code", how="left")

        # 组合：使用 score（0~100）做加权
        w = self.weights
        df["composite_score_raw"] = (
            df.get("cne5_score", 50).fillna(50) * w.cne5
            + df.get("alpha_score", 50).fillna(50) * w.alpha
            + df.get("fundamental_score", 50).fillna(50) * w.fundamental
        )
        # 再做一次截面排名到0~100，提升稳健性
        df["composite_score"] = df["composite_score_raw"].rank(pct=True) * 100

        return df

