<<<<<<< Updated upstream:src/pages/015_示例：等权构建组合.md
=======
---
title: 示例：等权构建组合
layout: /src/layouts/HandbookLayout.astro
lang: zh
alt: /en/015_Example_Building_Equal_Weighted_Portfolio_en
---
<div class="page-nav">
  <a href="/">← 返回目录</a>
  <a href="/016_Example_Backtesting_Return_Curve_CN">下一章 →</a>
</div>

>>>>>>> Stashed changes:src/pages/015_Example_Building_Equal_Weighted_Portfolio_CN.md
# 示例：等权构建组合

top_n = 5

weights = {ticker: 1 / top_n for ticker in selected_tickers}

2.4 回测分析

通过历史数据验证策略的有效性，评估收益和风险。

回测步骤：

计算每日组合收益：组合收益 = 每只股票收益 × 权重。

累计收益曲线：累计收益 = (1 + 日收益).cumprod()。

计算关键指标：

年化收益率：反映策略长期表现。

最大回撤：衡量潜在风险。

夏普比率：评估风险调整后的收益。

<!-- 图表占位：[示例：等权构建组合] -->

<div class="nav-links">
  <a href="/">← 返回目录</a>
  <a href="/016_Example_Backtesting_Return_Curve_CN">下一章 →</a>
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
