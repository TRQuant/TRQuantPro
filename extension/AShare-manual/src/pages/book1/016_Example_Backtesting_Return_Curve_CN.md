<<<<<<< Updated upstream:src/pages/016_示例：回测收益曲线.md
=======
---
title: 示例：回测收益曲线
layout: /src/layouts/HandbookLayout.astro
lang: zh
alt: /en/016_Example_Backtesting_Return_Curve_en
---
<div class="page-nav">
  <a href="/015_Example_Building_Equal_Weighted_Portfolio_CN">← 上一章</a>
  <a href="/017_Using_scipy_optimize_for_Optimization_CN">下一章 →</a>
</div>

>>>>>>> Stashed changes:src/pages/016_Example_Backtesting_Return_Curve_CN.md
# 示例：回测收益曲线

portfolio_returns = data.pct_change().dot(pd.Series(weights))

cumulative_returns = (1 + portfolio_returns).cumprod()

指标计算公式：

夏普比率： <GlossaryTerm term="Sharpe" /> Ratio=组合年化收益率−无风险利率年化波动率\text{<GlossaryTerm term="Sharpe" /> Ratio} = \frac{\text{组合年化收益率} - \text{无风险利率}}{\text{年化波动率}}

最大回撤： 最大回撤=累计收益的最大值−累计收益的最小值累计收益的最大值\text{最大回撤} = \frac{\text{累计收益的最大值} - \text{累计收益的最小值}}{\text{累计收益的最大值}}

2.5 优化扩展

通过数学模型优化组合权重，实现风险和收益的动态平衡。

均值方差优化： 目标是最大化夏普比率或最小化组合波动率。

from scipy.optimize import minimize

<!-- 图表占位：[示例：回测收益曲线] -->

<div class="nav-links">
  <a href="/015_Example_Building_Equal_Weighted_Portfolio_CN">← 上一章</a>
  <a href="/017_Using_scipy_optimize_for_Optimization_CN">下一章 →</a>
</div>

<style>
  
  
  /* 页面导航样式 - 与底部导航一致 */
  .page-nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 1.5rem 0;
    margin: 2rem 0;
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
  }

  .page-nav a {
    display: inline-flex;
    align-items: center;
    padding: 0.8rem 1.5rem;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    color: white;
    text-decoration: none;
    border-radius: 25px;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(56, 142, 60, 0.3);
  }

  .page-nav a:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, #81C784 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(56, 142, 60, 0.4);
  }

  .page-nav a:first-child {
    background: linear-gradient(135deg, #2196f3 0%, #42a5f5 100%);
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
  }

  .page-nav a:first-child:hover {
    background: linear-gradient(135deg, #42a5f5 0%, #64b5f6 100%);
    box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
  }

  .page-nav a:last-child {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    box-shadow: 0 4px 12px rgba(56, 142, 60, 0.3);
  }

  .page-nav a:last-child:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, #81C784 100%);
    box-shadow: 0 6px 20px rgba(56, 142, 60, 0.4);
  }

  /* 暗色模式适配 */
  [data-theme="dark"] .page-nav a:first-child {
    background: linear-gradient(135deg, #1976d2 0%, #1e88e5 100%);
  }

  [data-theme="dark"] .page-nav a:first-child:hover {
    background: linear-gradient(135deg, #1e88e5 0%, #2196f3 100%);
  }

  /* 响应式设计 */
  @media (max-width: 768px) {
    .page-nav {
      flex-direction: column;
      gap: 1rem;
    }

    .page-nav a {
      font-size: 0.9rem;
      padding: 0.7rem 1.2rem;
    }
  }
</style>
