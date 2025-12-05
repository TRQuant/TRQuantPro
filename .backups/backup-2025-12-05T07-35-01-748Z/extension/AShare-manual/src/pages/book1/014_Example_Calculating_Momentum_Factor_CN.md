---
title: 示例：计算动量因子
layout: /src/layouts/HandbookLayout.astro
lang: zh
alt: /en/014_Example_Calculating_Momentum_Factor_en
---
<div class="page-nav">
  <a href="/013_Example_Loading_Stock_Price_Data_CN">← 上一章</a>
  <a href="/015_Example_Building_Equal_Weighted_Portfolio_CN">下一章 →</a>
</div>

# 示例：计算动量因子

momentum = data.pct_change(30).mean(axis=1)

2.3 投资组合构建

通过筛选因子得分最高的股票，分配权重构建投资组合。

常用方法：

等权分配：每只股票权重相等，简单易用。

风险平价：根据波动率调整权重，降低高波动资产的风险。

优化分配：使用数学优化模型（如均值方差模型）寻找最优权重。
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
