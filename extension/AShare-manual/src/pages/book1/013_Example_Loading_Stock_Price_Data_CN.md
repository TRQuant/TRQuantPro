=======
---
title: 示例：加载股票价格数据
layout: /src/layouts/HandbookLayout.astro
lang: zh
alt: /en/013_Example_Loading_Stock_Price_Data_en
---
<div class="page-nav">
  <a href="/012_Strategy_Logic_CN">← 上一章</a>
  <a href="/014_Example_Calculating_Momentum_Factor_CN">下一章 →</a>
</div>

>>>>>>> Stashed changes:src/pages/013_Example_Loading_Stock_Price_Data_CN.md
# 示例：加载股票价格数据

import yfinance as yf

tickers = ["AAPL", "MSFT", "GOOGL"]

data = yf.download(tickers, start="2015-01-01", end="2025-01-01")['Adj Close']

2.2 因子计算

因子是量化策略的核心，用于筛选优质股票和优化投资组合。

常用因子：

技术因子：

动量：过去 30 天的收益率，用于捕捉趋势。

波动率：过去一段时间的价格波动，用于评估风险。

均线：如 MA50（50 日均线）和 MA200，用于识别趋势。

基本面因子：

P/E、P/B、<span class="glossary-term" data-term="ROE" data-definition='{"term":"ROE","fullName":"Return on Equity","description":"净资产收益率，衡量公司利用股东投资创造利润的效率","category":"财务指标","example":"ROE = 净利润 / 股东权益，通常>15%为优秀"}' title="净资产收益率，衡量公司利用股东投资创造利润的效率">ROE</span>、净利润增长率等，用于衡量企业质量。

<div class="nav-links">
  <a href="/012_Strategy_Logic_CN">← 上一章</a>
  <a href="/014_Example_Calculating_Momentum_Factor_CN">下一章 →</a>
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
