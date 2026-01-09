# -*- coding: utf-8 -*-
"""
最终选股器 (Final Selector)

核心功能：
1. 从候选池浓缩到5个最优投资标的
2. 多维度综合评估
3. 分散化约束（板块/市值）
4. 风险收益平衡
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class SelectionCriteria:
    """筛选标准"""
    # 数量限制
    final_count: int = 5                    # 最终选出数量
    max_per_sector: int = 2                 # 每个板块最多数量
    
    # 分散化约束
    min_sectors: int = 3                    # 最少覆盖板块数
    market_cap_diversity: bool = True       # 是否要求市值分散
    
    # 风险约束
    max_correlation: float = 0.7            # 最大相关性
    min_liquidity_score: float = 60         # 最低流动性得分
    
    # 评分权重
    score_weight: float = 0.4               # 综合得分权重
    growth_weight: float = 0.25             # 成长性权重
    value_weight: float = 0.15              # 估值权重
    momentum_weight: float = 0.20           # 动量权重


@dataclass
class FinalStock:
    """最终入选股票"""
    code: str
    name: str
    sector: str
    
    # 得分
    total_score: float
    growth_score: float
    value_score: float
    momentum_score: float
    
    # 关键指标
    market_cap: float
    pe_ratio: float
    revenue_growth: float
    profit_growth: float
    
    # 排名
    rank: int
    selection_reason: str
    
    # 风控参数
    suggested_weight: float     # 建议仓位
    stop_loss: float           # 止损价位
    target_price: float        # 目标价位


@dataclass
class SelectionResult:
    """筛选结果"""
    date: str
    market_regime: str
    
    # 入选股票
    stocks: List[FinalStock]
    
    # 组合统计
    total_weight: float
    sector_distribution: Dict[str, int]
    avg_score: float
    
    # 元数据
    criteria: SelectionCriteria
    selection_summary: str


class FinalSelector:
    """
    最终选股器
    
    设计原则：
    1. 综合多维度信息做最终决策
    2. 确保投资组合分散化
    3. 考虑市场环境调整参数
    4. 输出可直接执行的投资建议
    """
    
    def __init__(self, 
                 criteria: SelectionCriteria = None,
                 market_regime: str = 'neutral'):
        """
        Args:
            criteria: 筛选标准
            market_regime: 市场环境
        """
        self.criteria = criteria or SelectionCriteria()
        self.market_regime = market_regime
        
        # 根据市场环境调整参数
        self._adjust_for_regime()
    
    def _adjust_for_regime(self):
        """根据市场环境调整参数"""
        if self.market_regime in ['strong_bull', 'bull']:
            # 牛市：可以更集中
            self.criteria.max_per_sector = 3
            self.criteria.momentum_weight = 0.30
        elif self.market_regime in ['bear', 'strong_bear']:
            # 熊市：更分散，更保守
            self.criteria.max_per_sector = 1
            self.criteria.min_sectors = 4
            self.criteria.value_weight = 0.25
            self.criteria.momentum_weight = 0.10
    
    def select(self, 
              candidates: List[Dict],
              as_of_date: str = None) -> SelectionResult:
        """
        从候选池中选出最终5只股票
        
        Args:
            candidates: 候选股票列表
            as_of_date: 基准日期
            
        Returns:
            SelectionResult: 筛选结果
        """
        if as_of_date is None:
            as_of_date = datetime.now().strftime('%Y-%m-%d')
            
        print(f"\n{'='*60}")
        print(f"🎯 最终选股: 从 {len(candidates)} 只候选中选出 {self.criteria.final_count} 只")
        print(f"{'='*60}")
        
        if len(candidates) < self.criteria.final_count:
            print(f"⚠️ 候选数量不足，将选出所有 {len(candidates)} 只")
        
        # Step 1: 计算综合得分
        scored_candidates = self._calculate_composite_scores(candidates)
        
        # Step 2: 应用分散化约束
        diversified = self._apply_diversification(scored_candidates)
        
        # Step 3: 风险过滤
        filtered = self._apply_risk_filter(diversified)
        
        # Step 4: 最终排序选择
        final_stocks = self._final_selection(filtered)
        
        # Step 5: 计算仓位建议
        final_with_weights = self._calculate_weights(final_stocks)
        
        # 构建结果
        result = self._build_result(final_with_weights, as_of_date)
        
        # 打印结果
        self._print_result(result)
        
        return result
    
    def _calculate_composite_scores(self, candidates: List[Dict]) -> List[Dict]:
        """计算综合得分"""
        print(f"\n📊 计算综合得分...")
        
        scored = []
        for c in candidates:
            # 提取各维度得分
            total = c.get('total_score', c.get('综合分', 0)) or 0
            
            # 成长性得分
            growth = self._calc_growth_score(c)
            
            # 估值得分
            value = self._calc_value_score(c)
            
            # 动量得分
            momentum = self._calc_momentum_score(c)
            
            # 加权综合
            composite = (
                self.criteria.score_weight * total +
                self.criteria.growth_weight * growth +
                self.criteria.value_weight * value +
                self.criteria.momentum_weight * momentum
            )
            
            scored.append({
                **c,
                'composite_score': composite,
                'growth_score': growth,
                'value_score': value,
                'momentum_score': momentum
            })
        
        # 按综合分排序
        scored.sort(key=lambda x: x['composite_score'], reverse=True)
        return scored
    
    def _calc_growth_score(self, stock: Dict) -> float:
        """计算成长性得分"""
        revenue_growth = stock.get('revenue_growth', stock.get('营收增长', 0)) or 0
        profit_growth = stock.get('profit_growth', stock.get('利润增长', 0)) or 0
        
        # 标准化到0-100
        growth_score = min(100, max(0, 
            (revenue_growth + profit_growth) / 2 + 50
        ))
        return growth_score
    
    def _calc_value_score(self, stock: Dict) -> float:
        """计算估值得分"""
        pe = stock.get('pe', stock.get('PE', 30)) or 30
        peg = stock.get('peg', stock.get('PEG', 1.5)) or 1.5
        
        # PE得分（低估值高分）
        pe_score = max(0, 100 - pe * 2) if pe > 0 else 0
        
        # PEG得分
        peg_score = max(0, 100 - peg * 40) if peg > 0 else 0
        
        return (pe_score + peg_score) / 2
    
    def _calc_momentum_score(self, stock: Dict) -> float:
        """计算动量得分"""
        trend = stock.get('trend_score', 0) or 0
        stage = stock.get('stage', stock.get('阶段', ''))
        
        # 阶段加分
        stage_bonus = {
            '早期潜力': 30,
            '上升趋势': 20,
            '主升趋势': 10,
            '观望': 0,
        }
        bonus = stage_bonus.get(stage, 0)
        
        return min(100, max(0, trend + bonus))
    
    def _apply_diversification(self, candidates: List[Dict]) -> List[Dict]:
        """应用分散化约束"""
        print(f"\n🔄 应用分散化约束...")
        
        selected = []
        sector_counts = {}
        
        for c in candidates:
            # 兼容多种字段名
            sector = c.get('sector', c.get('sectors', c.get('所属板块', '其他')))
            # 如果是多板块，取第一个
            if isinstance(sector, str) and ',' in sector:
                sector = sector.split(',')[0].strip()
            
            # 检查板块限制
            if sector_counts.get(sector, 0) >= self.criteria.max_per_sector:
                continue
            
            selected.append(c)
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
            
            # 已选够了
            if len(selected) >= self.criteria.final_count * 2:
                break
        
        print(f"   分散化后剩余: {len(selected)} 只")
        print(f"   板块分布: {sector_counts}")
        return selected
    
    def _apply_risk_filter(self, candidates: List[Dict]) -> List[Dict]:
        """应用风险过滤"""
        print(f"\n🛡️ 应用风险过滤...")
        
        filtered = []
        for c in candidates:
            # 流动性检查
            market_cap = c.get('market_cap', c.get('市值', 0)) or 0
            if market_cap < 30:  # 30亿以下流动性可能不足
                continue
            
            # 极端估值检查
            pe = c.get('pe', c.get('PE', 0)) or 0
            if pe > 200 or pe < 0:  # 估值过高或亏损
                continue
            
            filtered.append(c)
        
        print(f"   风险过滤后剩余: {len(filtered)} 只")
        return filtered
    
    def _final_selection(self, candidates: List[Dict]) -> List[Dict]:
        """最终选择"""
        print(f"\n🎯 最终选择 Top {self.criteria.final_count}...")
        
        # 确保板块多样性
        selected = []
        sectors_covered = set()
        
        def get_primary_sector(c):
            """获取主要板块"""
            sector = c.get('sector', c.get('sectors', c.get('所属板块', '其他')))
            if isinstance(sector, str) and ',' in sector:
                sector = sector.split(',')[0].strip()
            return sector
        
        # 第一轮：每个板块选一只
        for c in candidates:
            sector = get_primary_sector(c)
            if sector not in sectors_covered:
                selected.append(c)
                sectors_covered.add(sector)
                if len(selected) >= self.criteria.final_count:
                    break
        
        # 第二轮：如果不够，从高分中补充
        if len(selected) < self.criteria.final_count:
            for c in candidates:
                if c not in selected:
                    selected.append(c)
                    if len(selected) >= self.criteria.final_count:
                        break
        
        print(f"   已选: {len(selected)} 只, 覆盖板块: {sectors_covered}")
        return selected[:self.criteria.final_count]
    
    def _calculate_weights(self, stocks: List[Dict]) -> List[FinalStock]:
        """计算仓位权重"""
        print(f"\n💰 计算仓位建议...")
        
        if not stocks:
            return []
        
        def get_sector(s):
            """获取板块"""
            sector = s.get('sector', s.get('sectors', s.get('所属板块', '')))
            if isinstance(sector, str) and ',' in sector:
                sector = sector.split(',')[0].strip()
            return sector
        
        # 基于得分的权重分配
        total_score = sum(s.get('composite_score', s.get('total_score', 50)) for s in stocks)
        
        final_stocks = []
        for i, s in enumerate(stocks):
            # 基础权重（按得分占比）
            score = s.get('composite_score', s.get('total_score', 50))
            base_weight = score / total_score if total_score > 0 else 1/len(stocks)
            
            # 调整后权重（确保每只至少10%，最多30%）
            weight = max(0.10, min(0.30, base_weight * len(stocks) / self.criteria.final_count))
            
            # 止损和目标价（使用市值估算价格）
            market_cap = s.get('market_cap', 100) or 100
            current_price = market_cap  # 使用市值作为参考
            
            # 根据市场环境设置止损
            if self.market_regime in ['bear', 'strong_bear']:
                stop_loss_pct = 0.05
                target_pct = 0.10
            elif self.market_regime in ['strong_bull']:
                stop_loss_pct = 0.10
                target_pct = 0.30
            else:
                stop_loss_pct = 0.08
                target_pct = 0.20
            
            final_stock = FinalStock(
                code=s.get('code', s.get('股票代码', '')),
                name=s.get('name', s.get('名称', '')),
                sector=get_sector(s),
                total_score=s.get('total_score', s.get('综合分', 0)) or 0,
                growth_score=s.get('growth_score', 0),
                value_score=s.get('value_score', s.get('valuation_score', 0)),
                momentum_score=s.get('momentum_score', s.get('trend_score', 0)),
                market_cap=s.get('market_cap', s.get('市值', 0)) or 0,
                pe_ratio=s.get('pe', s.get('PE', 0)) or 0,
                revenue_growth=s.get('revenue_growth', s.get('营收增长', 0)) or 0,
                profit_growth=s.get('profit_growth', s.get('利润增长', 0)) or 0,
                rank=i + 1,
                selection_reason=self._generate_reason(s),
                suggested_weight=weight,
                stop_loss=current_price * (1 - stop_loss_pct),
                target_price=current_price * (1 + target_pct)
            )
            final_stocks.append(final_stock)
        
        # 归一化权重
        total_weight = sum(s.suggested_weight for s in final_stocks)
        for s in final_stocks:
            s.suggested_weight = s.suggested_weight / total_weight
        
        return final_stocks
    
    def _generate_reason(self, stock: Dict) -> str:
        """生成入选理由"""
        reasons = []
        
        # 成长性
        growth = stock.get('profit_growth', stock.get('利润增长', 0)) or 0
        if growth > 50:
            reasons.append(f"高成长({growth:.0f}%)")
        elif growth > 20:
            reasons.append(f"稳健成长({growth:.0f}%)")
        
        # 估值
        pe = stock.get('pe', stock.get('PE', 0)) or 0
        peg = stock.get('peg', 1.5) or 1.5
        if 0 < peg < 1:
            reasons.append("估值优秀")
        elif 0 < pe < 30:
            reasons.append("估值适中")
        
        # 阶段
        stage = stock.get('stage', stock.get('阶段', ''))
        # 处理带emoji的阶段名
        if '早期潜力' in stage or '早期' in stage:
            reasons.append("早期潜力")
        elif '主升趋势' in stage or '主升' in stage:
            reasons.append("主升趋势")
        elif '上升趋势' in stage or '上升' in stage:
            reasons.append("上升趋势")
        
        # 板块
        sector = stock.get('sector', stock.get('sectors', stock.get('所属板块', '')))
        if isinstance(sector, str) and sector:
            # 取第一个板块
            primary_sector = sector.split(',')[0].strip() if ',' in sector else sector
            if primary_sector:
                reasons.append(f"{primary_sector}")
        
        # 技术面
        if stock.get('is_strong_uptrend'):
            reasons.append("强势上行")
        elif stock.get('is_uptrend'):
            reasons.append("趋势向好")
        
        return '，'.join(reasons) if reasons else '综合评分优秀'
    
    def _build_result(self, stocks: List[FinalStock], date: str) -> SelectionResult:
        """构建结果"""
        # 板块分布
        sector_dist = {}
        for s in stocks:
            sector_dist[s.sector] = sector_dist.get(s.sector, 0) + 1
        
        # 平均得分
        avg_score = np.mean([s.total_score for s in stocks]) if stocks else 0
        
        # 总结
        summary = self._generate_summary(stocks)
        
        return SelectionResult(
            date=date,
            market_regime=self.market_regime,
            stocks=stocks,
            total_weight=1.0,
            sector_distribution=sector_dist,
            avg_score=avg_score,
            criteria=self.criteria,
            selection_summary=summary
        )
    
    def _generate_summary(self, stocks: List[FinalStock]) -> str:
        """生成选股总结"""
        if not stocks:
            return "未筛选到符合条件的股票"
        
        sectors = set(s.sector for s in stocks)
        avg_growth = np.mean([s.profit_growth for s in stocks])
        
        summary = (
            f"本次筛选出{len(stocks)}只优质标的，"
            f"覆盖{len(sectors)}个板块，"
            f"平均利润增速{avg_growth:.1f}%。"
        )
        
        # 市场环境提示
        if self.market_regime in ['bear', 'strong_bear']:
            summary += "当前市场偏弱，建议控制仓位，严格止损。"
        elif self.market_regime in ['strong_bull']:
            summary += "市场强势，可适度集中持仓。"
        else:
            summary += "市场震荡，建议分批建仓。"
        
        return summary
    
    def _print_result(self, result: SelectionResult):
        """打印结果"""
        print(f"\n{'='*70}")
        print(f"🏆 最终投资组合 ({result.date})")
        print(f"{'='*70}")
        print(f"📊 市场环境: {result.market_regime}")
        print(f"📊 覆盖板块: {len(result.sector_distribution)} 个")
        print(f"📊 平均得分: {result.avg_score:.1f}")
        
        print(f"\n{'─'*70}")
        print(f"{'排名':^4} {'代码':^12} {'名称':^10} {'板块':^10} {'权重':^8} {'入选理由'}")
        print(f"{'─'*70}")
        
        for s in result.stocks:
            print(f"{s.rank:^4} {s.code:^12} {s.name:^10} {s.sector:^10} "
                  f"{s.suggested_weight*100:>5.1f}%   {s.selection_reason}")
        
        print(f"{'─'*70}")
        
        print(f"\n💡 操作建议:")
        for s in result.stocks:
            print(f"   {s.code} {s.name}: 止损 ¥{s.stop_loss:.2f}, 目标 ¥{s.target_price:.2f}")
        
        print(f"\n📝 总结: {result.selection_summary}")


def generate_final_report_html(result: SelectionResult, output_path: str = None) -> str:
    """
    生成最终选股HTML报告
    """
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'output/reports/final_selection_{timestamp}.html'
    
    # 确保目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 构建HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>最终投资组合报告 - {result.date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; font-size: 1.1em; }}
        
        .summary {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        
        .stocks-grid {{
            display: grid;
            gap: 20px;
        }}
        
        .stock-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .stock-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .stock-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .stock-rank {{
            background: linear-gradient(135deg, #f093fb, #f5576c);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .stock-name {{ font-size: 1.3em; font-weight: 600; }}
        .stock-code {{ color: #888; font-size: 0.9em; }}
        .stock-sector {{
            background: rgba(102, 126, 234, 0.3);
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .stock-metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .metric {{
            text-align: center;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }}
        .metric-value {{
            font-size: 1.4em;
            font-weight: 600;
            color: #667eea;
        }}
        .metric-label {{
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }}
        
        .stock-action {{
            background: rgba(76, 175, 80, 0.1);
            border: 1px solid rgba(76, 175, 80, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }}
        .action-row {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }}
        .action-label {{ color: #888; }}
        .action-value {{ font-weight: 600; }}
        .stop-loss {{ color: #f44336; }}
        .target {{ color: #4caf50; }}
        
        .reason {{
            background: rgba(255,193,7,0.1);
            border-left: 3px solid #ffc107;
            padding: 10px 15px;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 最终投资组合</h1>
            <div class="meta">
                📅 {result.date} | 📊 市场环境: {result.market_regime} | 
                🎯 {len(result.stocks)} 只标的
            </div>
        </div>
        
        <div class="summary">
            <h3 style="margin-bottom: 10px;">📝 投资策略摘要</h3>
            <p>{result.selection_summary}</p>
        </div>
        
        <div class="stocks-grid">
'''
    
    for s in result.stocks:
        html += f'''
            <div class="stock-card">
                <div class="stock-header">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div class="stock-rank">{s.rank}</div>
                        <div>
                            <div class="stock-name">{s.name}</div>
                            <div class="stock-code">{s.code}</div>
                        </div>
                    </div>
                    <div class="stock-sector">{s.sector}</div>
                </div>
                
                <div class="stock-metrics">
                    <div class="metric">
                        <div class="metric-value">{s.total_score:.0f}</div>
                        <div class="metric-label">综合得分</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.suggested_weight*100:.1f}%</div>
                        <div class="metric-label">建议仓位</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.profit_growth:.1f}%</div>
                        <div class="metric-label">利润增速</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.pe_ratio:.1f}</div>
                        <div class="metric-label">PE估值</div>
                    </div>
                </div>
                
                <div class="stock-action">
                    <div class="action-row">
                        <span class="action-label">🛡️ 止损价位</span>
                        <span class="action-value stop-loss">¥{s.stop_loss:.2f}</span>
                    </div>
                    <div class="action-row">
                        <span class="action-label">🎯 目标价位</span>
                        <span class="action-value target">¥{s.target_price:.2f}</span>
                    </div>
                </div>
                
                <div class="reason">
                    <strong>入选理由：</strong>{s.selection_reason}
                </div>
            </div>
'''
    
    html += f'''
        </div>
        
        <div class="footer">
            <p>⚠️ 风险提示：本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n📄 报告已生成: {output_path}")
    return output_path


if __name__ == '__main__':
    print("🧪 测试最终选股器...")
    
    # 模拟候选数据
    mock_candidates = [
        {'code': '000001.XSHE', 'name': '平安银行', 'sector': '金融', 'total_score': 85, 
         'profit_growth': 15, 'pe': 8, 'market_cap': 2000, 'price': 12},
        {'code': '000002.XSHE', 'name': '万科A', 'sector': '地产', 'total_score': 70,
         'profit_growth': -5, 'pe': 6, 'market_cap': 1500, 'price': 10},
        {'code': '300750.XSHE', 'name': '宁德时代', 'sector': '新能源电池', 'total_score': 90,
         'profit_growth': 35, 'pe': 25, 'market_cap': 8000, 'price': 180},
    ]
    
    selector = FinalSelector(market_regime='neutral')
    result = selector.select(mock_candidates)
