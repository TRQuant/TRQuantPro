---
title: "6.4 因子流水线"
description: "深入解析因子自动化计算流水线，包括定时计算、数据质量检查、错误重试和日志记录"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🔄 6.4 因子流水线

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统的因子自动化计算流水线，包括定时计算、数据获取与检查、因子计算、中性化处理、存储到数据库、绩效监控更新、错误重试和日志记录。通过理解流水线的设计架构、数据质量检查机制、错误处理策略和自动化调度方法，帮助开发者掌握因子流水线的核心实现，为构建稳定可靠的因子自动化计算系统奠定基础。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-6-4-1')">
    <h4>🏗️ 6.4.1 流水线架构</h4>
    <p>流水线设计、模块组成、数据流</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-4-2')">
    <h4>📊 6.4.2 数据获取与检查</h4>
    <p>股票池获取、数据质量检查、异常处理</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-4-3')">
    <h4>⚙️ 6.4.3 因子计算流程</h4>
    <p>批量计算、中性化处理、结果验证</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-4-4')">
    <h4>💾 6.4.4 数据存储与更新</h4>
    <p>因子值存储、绩效监控更新、元数据管理</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-4-5')">
    <h4>🔄 6.4.5 错误处理与重试</h4>
    <p>错误检测、重试策略、日志记录</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-4-6')">
    <h4>⏰ 6.4.6 自动化调度</h4>
    <p>定时任务、调度配置、监控告警</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解流水线架构**：掌握因子流水线的设计架构和模块组成
- **掌握数据获取**：理解股票池获取、数据质量检查和异常处理
- **熟悉计算流程**：理解批量计算、中性化处理和结果验证
- **了解数据存储**：掌握因子值存储、绩效监控更新和元数据管理
- **实现错误处理**：理解错误检测、重试策略和日志记录
- **配置自动化调度**：掌握定时任务配置和监控告警

<h2 id="section-6-4-1">🏗️ 6.4.1 流水线架构</h2>

因子流水线是因子自动化计算的核心组件，负责完成从数据获取到结果存储的全流程。

### 设计原则

<div class="key-points">
  <div class="key-point">
    <h4>🔄 自动化</h4>
    <p>全流程自动化，减少人工干预</p>
  </div>
  <div class="key-point">
    <h4>🛡️ 可靠性</h4>
    <p>完善的错误处理和重试机制</p>
  </div>
  <div class="key-point">
    <h4>📊 可监控</h4>
    <p>详细的日志记录和运行统计</p>
  </div>
  <div class="key-point">
    <h4>⚡ 高性能</h4>
    <p>批量计算、并行处理、缓存优化</p>
  </div>
</div>

### 流水线架构

```python
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pathlib import Path
import logging

from .factor_manager import FactorManager
from .factor_storage import FactorStorage
from .factor_neutralizer import FactorNeutralizer
from .factor_evaluator import FactorEvaluator

class FactorPipeline:
    """
    因子计算流水线
    
    自动化完成：
    1. 数据获取与检查
    2. 因子计算
    3. 中性化处理（可选）
    4. 存储到数据库
    5. 绩效监控更新
    """
    
    def __init__(
        self,
        jq_client=None,
        factor_manager: Optional[FactorManager] = None,
        factor_storage: Optional[FactorStorage] = None,
        stock_pool: str = "all_a",  # 'all_a', 'hs300', 'zz500', 'zz1000'
        neutralize: bool = True,
        log_dir: Optional[Path] = None,
    ):
        """
        初始化流水线
        
        Args:
            jq_client: JQData客户端
            factor_manager: 因子管理器
            factor_storage: 因子存储
            stock_pool: 股票池
            neutralize: 是否进行中性化处理
            log_dir: 日志目录
        """
        self.jq_client = jq_client
        
        self.factor_manager = factor_manager or FactorManager(jq_client=jq_client)
        self.factor_storage = factor_storage or FactorStorage()
        self.neutralizer = FactorNeutralizer(jq_client=jq_client)
        self.evaluator = FactorEvaluator(jq_client=jq_client)
        
        self.stock_pool = stock_pool
        self.neutralize = neutralize
        
        self.log_dir = log_dir or Path.home() / ".local/share/trquant/logs/factors"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 运行统计
        self.run_stats = {
            "start_time": None,
            "end_time": None,
            "total_stocks": 0,
            "success_factors": 0,
            "failed_factors": 0,
            "skipped_stocks": 0,
            "errors": [],
        }
```

<h2 id="section-6-4-2">📊 6.4.2 数据获取与检查</h2>

数据获取与检查是流水线的第一步，确保数据质量。

### 股票池获取

```python
def get_stock_pool(self, date: Union[str, datetime]) -> List[str]:
    """
    获取股票池
    
    Args:
        date: 日期
    
    Returns:
        List[str]: 股票列表
    """
    if self.jq_client is None:
        raise ValueError("需要JQData客户端")
    
    import jqdatasdk as jq
    
    if self.stock_pool == "hs300":
        return jq.get_index_stocks("000300.XSHG", date=date)
    elif self.stock_pool == "zz500":
        return jq.get_index_stocks("000905.XSHG", date=date)
    elif self.stock_pool == "zz1000":
        return jq.get_index_stocks("000852.XSHG", date=date)
    else:  # all_a
        securities = jq.get_all_securities(types=["stock"], date=date)
        return securities.index.tolist()
```

### 股票过滤

```python
def filter_stocks(self, stocks: List[str], date: Union[str, datetime]) -> List[str]:
    """
    过滤股票（ST、停牌、上市不足等）
    
    Args:
        stocks: 股票列表
        date: 日期
    
    Returns:
        List[str]: 过滤后的股票列表
    """
    if self.jq_client is None:
        return stocks
    
    import jqdatasdk as jq
    
    filtered = []
    
    try:
        # 过滤ST
        st_info = jq.get_extras("is_st", stocks, end_date=date, count=1)
        if not st_info.empty:
            st_stocks = st_info.iloc[0][st_info.iloc[0] == True].index.tolist()
        else:
            st_stocks = []
        
        # 过滤停牌
        paused_info = jq.get_price(
            stocks, end_date=date, count=1, fields=["paused"], panel=False
        )
        if not paused_info.empty:
            paused_stocks = paused_info[paused_info["paused"] == 1]["code"].tolist()
        else:
            paused_stocks = []
        
        # 过滤上市不足N天的股票
        securities = jq.get_all_securities(types=["stock"], date=date)
        min_listing_days = 60  # 至少上市60天
        
        for stock in stocks:
            if stock in st_stocks:
                continue
            if stock in paused_stocks:
                continue
            
            # 检查上市时间
            if stock in securities.index:
                listing_date = securities.loc[stock, "start_date"]
                if isinstance(date, str):
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                else:
                    date_obj = date
                
                days_since_listing = (date_obj - listing_date).days
                if days_since_listing < min_listing_days:
                    continue
            
            filtered.append(stock)
        
        logger.info(f"股票过滤完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    except Exception as e:
        logger.error(f"股票过滤失败: {e}")
        return stocks
```

<h2 id="section-6-4-3">⚙️ 6.4.3 因子计算流程</h2>

因子计算流程是流水线的核心，负责批量计算所有因子。

### 批量计算

```python
def run_pipeline(
    self,
    date: Optional[Union[str, datetime]] = None,
    factor_categories: Optional[List[str]] = None,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    运行完整流水线
    
    Args:
        date: 计算日期（默认今天）
        factor_categories: 因子类别列表（默认所有类别）
        max_retries: 最大重试次数
    
    Returns:
        运行结果统计
    """
    if date is None:
        date = datetime.now()
    
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    
    self.run_stats["start_time"] = datetime.now()
    
    try:
        # 1. 获取股票池
        logger.info(f"步骤1: 获取股票池 ({self.stock_pool})...")
        stocks = self.get_stock_pool(date)
        stocks = self.filter_stocks(stocks, date)
        self.run_stats["total_stocks"] = len(stocks)
        
        if not stocks:
            logger.warning("股票池为空，跳过计算")
            return self.run_stats
        
        # 2. 获取因子列表
        logger.info("步骤2: 获取因子列表...")
        if factor_categories:
            factor_names = []
            for category in factor_categories:
                factor_names.extend(self.factor_manager.list_factors(category))
        else:
            factor_names = self.factor_manager.list_factors()
        
        # 3. 批量计算因子
        logger.info(f"步骤3: 批量计算因子 ({len(factor_names)}个)...")
        success_count = 0
        failed_count = 0
        
        for factor_name in factor_names:
            try:
                # 计算因子
                result = self.factor_manager.calculate_factor(
                    factor_name, stocks, date
                )
                
                if result is None or result.values.empty:
                    logger.warning(f"因子计算返回空结果: {factor_name}")
                    failed_count += 1
                    continue
                
                # 中性化处理（可选）
                if self.neutralize:
                    neutralized_values = self.neutralizer.neutralize(
                        result.values,
                        stocks,
                        date,
                        neutralize_industry=True,
                        neutralize_size=True
                    )
                    result.values = neutralized_values
                
                # 存储因子值
                self.factor_storage.save_factor_values(
                    factor_name,
                    date,
                    result.values,
                    overwrite=True
                )
                
                success_count += 1
                logger.info(f"因子计算成功: {factor_name} ({result.values.notna().sum()}/{len(stocks)})")
            
            except Exception as e:
                logger.error(f"因子计算失败: {factor_name}, 错误: {e}")
                failed_count += 1
                self.run_stats["errors"].append({
                    "factor": factor_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        self.run_stats["success_factors"] = success_count
        self.run_stats["failed_factors"] = failed_count
        
        logger.info(f"流水线完成: 成功 {success_count}, 失败 {failed_count}")
    
    except Exception as e:
        logger.error(f"流水线运行失败: {e}")
        self.run_stats["errors"].append({
            "stage": "pipeline",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    finally:
        self.run_stats["end_time"] = datetime.now()
        self._save_run_log()
    
    return self.run_stats
```

<h2 id="section-6-4-4">💾 6.4.4 数据存储与更新</h2>

数据存储与更新确保因子值被正确保存，并更新绩效监控数据。

### 因子值存储

```python
def save_factor_values(
    self,
    factor_name: str,
    date: datetime,
    values: pd.Series
):
    """
    保存因子值
    
    Args:
        factor_name: 因子名称
        date: 日期
        values: 因子值
    """
    try:
        # 保存到MongoDB或文件
        success = self.factor_storage.save_factor_values(
            factor_name,
            date,
            values,
            overwrite=True
        )
        
        if success:
            logger.debug(f"因子值保存成功: {factor_name} @ {date}")
        else:
            logger.warning(f"因子值保存失败: {factor_name} @ {date}")
    
    except Exception as e:
        logger.error(f"因子值保存异常: {factor_name}, 错误: {e}")
```

<h2 id="section-6-4-5">🔄 6.4.5 错误处理与重试</h2>

错误处理与重试确保流水线的稳定性和可靠性。

### 错误检测

```python
def _check_data_quality(self, stocks: List[str], date: datetime) -> bool:
    """
    检查数据质量
    
    Args:
        stocks: 股票列表
        date: 日期
    
    Returns:
        bool: 数据质量是否合格
    """
    try:
        import jqdatasdk as jq
        
        # 检查价格数据
        prices = jq.get_price(
            stocks[:100],  # 抽样检查
            end_date=date,
            count=1,
            fields=["close"],
            panel=False
        )
        
        if prices.empty:
            logger.warning("价格数据为空")
            return False
        
        # 检查覆盖率
        coverage = len(prices) / len(stocks[:100])
        if coverage < 0.8:
            logger.warning(f"数据覆盖率过低: {coverage:.2%}")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"数据质量检查失败: {e}")
        return False
```

<h2 id="section-6-4-6">⏰ 6.4.6 自动化调度</h2>

自动化调度支持定时任务和监控告警。

### 定时任务配置

```python
import schedule
import time

def start_daily_pipeline(
    pipeline: FactorPipeline,
    run_time: str = "18:00",  # 默认收盘后运行
    stock_pool: str = "all_a"
):
    """
    启动每日定时流水线
    
    Args:
        pipeline: 因子流水线实例
        run_time: 运行时间（HH:MM格式）
        stock_pool: 股票池
    """
    pipeline.stock_pool = stock_pool
    
    def run_daily():
        """每日运行函数"""
        logger.info(f"开始每日因子计算流水线: {datetime.now()}")
        try:
            result = pipeline.run_pipeline()
            logger.info(f"每日流水线完成: {result}")
        except Exception as e:
            logger.error(f"每日流水线失败: {e}")
    
    # 配置定时任务
    schedule.every().day.at(run_time).do(run_daily)
    
    logger.info(f"定时任务已配置: 每日 {run_time} 运行")
    
    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次
```

## 🔗 相关章节

- **第2章：数据源模块** - 了解数据获取机制，为因子流水线提供数据支撑
- **第6章：因子库** - 了解因子库模块的整体设计
- **第6.1节：因子计算** - 因子计算是流水线的核心
- **第6.2节：因子管理** - 因子管理为流水线提供因子列表
- **第6.3节：因子优化** - 因子优化结果用于流水线验证
- **第10章：开发指南** - 了解因子流水线的开发规范

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了因子流水线，包括自动化计算流程、数据质量检查、错误重试和定时任务配置。通过理解因子流水线的实现，帮助开发者掌握如何构建自动化、可靠的因子计算系统，确保因子计算的及时性和准确性。</p>
  
  <h3>下节预告</h3>
  <p>掌握了因子流水线后，下一节将介绍因子与候选池的集成机制，包括因子评分、主线融合、综合评分和选股信号生成。通过理解因子与候选池的集成，帮助开发者掌握如何将因子库与候选池模块有机结合，实现完整的选股流程。</p>
  
  <a href="/ashare-book6/006_Chapter6_Factor_Library/6.5_Factor_Pool_Integration_CN" class="next-section">
    继续学习：6.5 候选池集成 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12

