# 市场主线研究完整指南 - 基于聚宽正式账号

> **版本**: v1.0  
> **更新日期**: 2025-01-01  
> **适用账号**: 聚宽股票专业版  
> **目标**: 完善9步工作流中的"投资主线"步骤（步骤3）

---

## 📋 目录

1. [聚宽正式账号配置与使用](#1-聚宽正式账号配置与使用)
2. [市场主线研究框架](#2-市场主线研究框架)
3. [预测主线的因子组合设计](#3-预测主线的因子组合设计)
4. [历史数据验证测试方案](#4-历史数据验证测试方案)
5. [完整工作流集成](#5-完整工作流集成)

---

## 1. 聚宽正式账号配置与使用

### 1.1 账号权限确认

**股票专业版包含的功能**：

✅ **基础数据服务**（全部包含）
- 沪深A股信息服务
- 上市公司财务&相关信息服务
- 基金信息服务
- 指数信息服务
- 债券信息服务

✅ **因子数据服务**（全部包含）
- Alpha101因子（101个因子）
- Alpha191因子（191个因子，扩展版）
- 聚宽因子库（质量类、基础类、成长类、每股类、情绪类、风险类、动量类、技术类）
- 聚宽风险模型（CNE5，10个风格因子）

✅ **技术分析指标**（包含）

✅ **Tick数据**（包含）
- 沪深A股tick高频信息（每日盘后更新）
- 指数tick高频信息
- 场内基金tick高频信息
- 可转债tick高频信息

✅ **其他服务**
- 宏观经济信息服务（附赠）
- 舆情信息服务（附赠）

💰 **需要额外付费的**：
- 聚宽CNE6风格因子（+25000元/年）
- 分钟资金流向（+10000元/年）

### 1.2 账号配置

**配置文件位置**: `/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json`

```json
{
  "username": "your_phone_number",
  "password": "your_password",
  "api_endpoint": "https://dataapi.joinquant.com",
  "timeout": 30,
  "retry_times": 3,
  "data_mode": "historical",
  "permission": {
    "auto_detect": true,
    "start_date": null,
    "end_date": null
  }
}
```

### 1.3 认证与初始化

```python
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

# 方式1: 使用配置文件
config_manager = get_config_manager()
jq_config = config_manager.get_jqdata_config()
jq_client = JQDataClient()
jq_client.authenticate(
    username=jq_config.get('username'),
    password=jq_config.get('password')
)

# 方式2: 直接认证
from jqdata.auth import authenticate
authenticate('your_phone_number', 'your_password')
```

### 1.4 补充数据源

**AKShare**（免费开源）
- 用途：补充宏观数据、行业数据、资金流向数据
- 安装：`pip install akshare`
- 优势：免费、数据源丰富、更新及时

**使用示例**：
```python
import akshare as ak

# 获取行业资金流向
industry_flow = ak.stock_fund_flow_industry()

# 获取北向资金流向
northbound_flow = ak.stock_connect_northbound_capital_flow()

# 获取宏观数据
macro_data = ak.macro_china_gdp()
```

---

## 2. 市场主线研究框架

### 2.1 主线定义

**市场主线**：在一段时间内（短期3-5日、中期15-30日、长期60-180日）能够持续获得超额收益的投资主题或板块。

**主线特征**：
1. **资金集中流入**：主力资金、北向资金、两融资金持续流入
2. **行业景气度高**：收入增长、利润率提升、订单饱满
3. **政策支持**：相关政策利好、产业政策扶持
4. **技术突破**：技术形态突破、量价配合良好
5. **市场情绪高涨**：新闻热度、搜索热度、社交媒体讨论度高

### 2.2 主线识别流程（8步）

基于 `markets/ashare/mainline/engine.py` 的 `AShareMainlineEngine.run_full_analysis()`：

```
Step 1: 宏观前瞻分析
  ├─ 政策周期判断
  ├─ 经济周期判断
  └─ 流动性环境评估

Step 2: 资金流向分析
  ├─ 板块资金流向（主力资金）
  ├─ 北向资金偏好
  └─ 两融资金趋势

Step 3: 行业景气分析
  ├─ 行业表现排名
  ├─ 景气度评估
  └─ 周期位置判断

Step 4: 技术形态分析
  ├─ 强势板块识别
  ├─ 突破板块识别
  └─ 弱势板块识别

Step 5: 估值分析
  ├─ 板块估值水平
  └─ 估值分位数

Step 6: 前瞻指标分析
  ├─ 政策催化剂
  ├─ 事件催化剂
  └─ 业绩催化剂

Step 7: LLM综合分析
  └─ 多维度信息整合

Step 8: 主线识别与评分
  └─ 生成主线列表并评分
```

### 2.3 使用示例

```python
from markets.ashare.mainline.engine import AShareMainlineEngine
from jqdata.client import JQDataClient

# 初始化
jq_client = JQDataClient()
jq_client.authenticate('username', 'password')

engine = AShareMainlineEngine(data_manager=data_manager)

# 运行完整分析
result = engine.run_full_analysis()

# 查看发现的主线
for mainline in result["mainlines"]:
    print(f"主线: {mainline.name}")
    print(f"  得分: {mainline.score.total_score}")
    print(f"  阶段: {mainline.stage}")
    print(f"  相关股票: {mainline.related_stocks[:5]}")
    print()
```

---

## 3. 预测主线的因子组合设计

### 3.1 因子分类体系

#### 3.1.1 宏观因子（权重：20%）

**政策因子**：
- `policy_support_score`：政策支持度评分（0-100）
- `policy_frequency`：政策发布频率（近30天政策数量）
- `policy_intensity`：政策强度（政策级别加权）

**经济因子**：
- `gdp_growth`：GDP增长率
- `pmi_index`：PMI指数
- `m2_growth`：M2增长率

**流动性因子**：
- `liquidity_indicator`：流动性指标（M2-GDP-CPI）
- `interest_rate`：利率水平
- `credit_growth`：信贷增长率

#### 3.1.2 资金流因子（权重：30%）

**主力资金因子**：
- `main_capital_inflow`：主力资金净流入（近5日累计）
- `main_capital_inflow_ratio`：主力资金流入占比（占板块市值比例）
- `main_capital_continuity`：主力资金连续性（连续流入天数）

**北向资金因子**：
- `northbound_flow`：北向资金净流入
- `northbound_ratio`：北向资金占比
- `northbound_trend`：北向资金趋势（5日均线斜率）

**两融因子**：
- `margin_balance`：两融余额
- `margin_ratio`：融资买入占比
- `margin_trend`：两融趋势

#### 3.1.3 行业景气因子（权重：25%）

**基本面因子**（使用聚宽因子库）：
- `revenue_growth`：营收增长率（TTM）
- `profit_growth`：净利润增长率（TTM）
- `roe`：净资产收益率（ROE）
- `roa`：总资产收益率（ROA）
- `gross_margin`：毛利率

**景气度因子**：
- `prosperity_index`：景气度指数（综合评分）
- `order_growth`：订单增长率
- `capacity_utilization`：产能利用率

#### 3.1.4 技术动量因子（权重：15%）

**价格动量因子**（使用Alpha101/191）：
- `alpha_001` - `alpha_191`：Alpha191因子库
- `rsi`：相对强弱指标
- `macd`：MACD指标
- `bollinger_position`：布林带位置

**成交量因子**：
- `volume_ratio`：成交量比率（相对20日均量）
- `volume_trend`：成交量趋势
- `turnover_rate`：换手率

**突破因子**：
- `breakout_score`：突破强度评分
- `breakout_volume`：突破时的成交量
- `resistance_distance`：距离阻力位距离

#### 3.1.5 市场情绪因子（权重：10%）

**新闻热度因子**：
- `news_frequency`：新闻发布频率（近7天）
- `news_sentiment`：新闻情感倾向（正面/负面）
- `news_keyword_density`：关键词密度

**搜索热度因子**：
- `search_index`：搜索指数
- `search_trend`：搜索趋势（上升/下降）

**社交媒体因子**：
- `social_mentions`：社交媒体提及次数
- `social_sentiment`：社交媒体情感倾向

**龙虎榜因子**：
- `lhb_count`：龙虎榜上榜次数
- `lhb_amount`：龙虎榜成交金额

### 3.2 因子组合权重设计

**权重分配原则**：
1. **资金流因子权重最高（30%）**：资金是推动主线的最直接因素
2. **行业景气因子次之（25%）**：基本面支撑主线持续性
3. **宏观因子（20%）**：政策和经济环境是主线产生的背景
4. **技术动量因子（15%）**：技术面验证主线强度
5. **市场情绪因子（10%）**：情绪面反映市场关注度

**因子组合公式**：

```
主线预测得分 = 
  宏观因子得分 × 20% +
  资金流因子得分 × 30% +
  行业景气因子得分 × 25% +
  技术动量因子得分 × 15% +
  市场情绪因子得分 × 10%
```

### 3.3 使用聚宽正式账号获取因子

#### 3.3.1 Alpha因子（Alpha101/191）

```python
from core.factors.jqdata_factor_engine import JQDataFactorEngine

engine = JQDataFactorEngine(jq_client=jq_client)

# 获取Alpha191因子（所有191个因子）
alpha_factors = engine.get_alpha_factors(
    stocks=['000001.XSHE', '600000.XSHG'],
    date='2024-01-15',
    alpha_version='191'  # 或 '101'
)

# 获取特定Alpha因子
alpha_001 = engine.get_alpha_factor('alpha_001', stocks, date)
alpha_002 = engine.get_alpha_factor('alpha_002', stocks, date)
```

#### 3.3.2 聚宽因子库

```python
# 获取财务因子
revenue_growth = engine.get_factor_values(
    stocks=stocks,
    factors=['revenue_growth', 'profit_growth', 'roe', 'roa'],
    start_date='2024-01-01',
    end_date='2024-01-15'
)

# 获取估值因子
valuation_factors = engine.get_factor_values(
    stocks=stocks,
    factors=['pe_ratio', 'pb_ratio', 'ps_ratio', 'market_cap'],
    start_date='2024-01-01',
    end_date='2024-01-15'
)

# 获取技术因子
technical_factors = engine.get_factor_values(
    stocks=stocks,
    factors=['rsi', 'macd', 'bollinger_upper', 'bollinger_lower'],
    start_date='2024-01-01',
    end_date='2024-01-15'
)
```

#### 3.3.3 CNE5风格因子

```python
# 获取CNE5风格因子暴露度
cne5_exposure = engine.get_cne5_exposure(
    stocks=stocks,
    date='2024-01-15'
)

# CNE5包含10个风格因子：
# - size（市值）
# - beta（Beta）
# - momentum（动量）
# - residual_volatility（残差波动率）
# - nonlinear_size（非线性市值）
# - book_to_price（账面市值比）
# - liquidity（流动性）
# - earnings_yield（盈利收益率）
# - growth（成长性）
# - leverage（杠杆）
```

### 3.4 完整因子组合实现示例

```python
from typing import Dict, List
import pandas as pd
import numpy as np
from datetime import datetime

class MainlinePredictionFactorCombination:
    """主线预测因子组合"""
    
    def __init__(self, jq_client, akshare_client=None):
        self.jq_client = jq_client
        self.akshare_client = akshare_client
        self.factor_engine = JQDataFactorEngine(jq_client)
        
        # 权重配置
        self.weights = {
            'macro': 0.20,
            'capital_flow': 0.30,
            'industry_prosperity': 0.25,
            'technical_momentum': 0.15,
            'market_sentiment': 0.10
        }
    
    def calculate_mainline_score(
        self,
        industry_code: str,
        date: str,
        period: str = 'medium'  # short/medium/long
    ) -> Dict[str, float]:
        """
        计算主线预测得分
        
        Args:
            industry_code: 行业代码（如 '801010'）
            date: 日期 'YYYY-MM-DD'
            period: 期限（short/medium/long）
        
        Returns:
            {
                'total_score': 总分,
                'macro_score': 宏观因子得分,
                'capital_flow_score': 资金流因子得分,
                'industry_prosperity_score': 行业景气因子得分,
                'technical_momentum_score': 技术动量因子得分,
                'market_sentiment_score': 市场情绪因子得分
            }
        """
        # 1. 获取行业股票列表
        stocks = self._get_industry_stocks(industry_code, date)
        
        # 2. 计算各类因子得分
        macro_score = self._calculate_macro_score(date)
        capital_flow_score = self._calculate_capital_flow_score(stocks, date)
        industry_score = self._calculate_industry_score(stocks, date)
        technical_score = self._calculate_technical_score(stocks, date)
        sentiment_score = self._calculate_sentiment_score(stocks, date)
        
        # 3. 加权组合
        total_score = (
            macro_score * self.weights['macro'] +
            capital_flow_score * self.weights['capital_flow'] +
            industry_score * self.weights['industry_prosperity'] +
            technical_score * self.weights['technical_momentum'] +
            sentiment_score * self.weights['market_sentiment']
        )
        
        return {
            'total_score': total_score,
            'macro_score': macro_score,
            'capital_flow_score': capital_flow_score,
            'industry_prosperity_score': industry_score,
            'technical_momentum_score': technical_score,
            'market_sentiment_score': sentiment_score
        }
    
    def _calculate_macro_score(self, date: str) -> float:
        """计算宏观因子得分（0-100）"""
        # 使用AKShare获取宏观数据
        # 简化示例，实际需要综合政策、经济、流动性多个指标
        return 70.0  # 示例值
    
    def _calculate_capital_flow_score(self, stocks: List[str], date: str) -> float:
        """计算资金流因子得分（0-100）"""
        # 使用JQData获取资金流向数据
        # 计算主力资金、北向资金、两融资金的综合流入情况
        return 75.0  # 示例值
    
    def _calculate_industry_score(self, stocks: List[str], date: str) -> float:
        """计算行业景气因子得分（0-100）"""
        # 使用聚宽因子库获取财务数据
        factors = self.factor_engine.get_factor_values(
            stocks=stocks,
            factors=['revenue_growth', 'profit_growth', 'roe', 'roa'],
            start_date=date,
            end_date=date
        )
        
        # 综合计算景气度得分
        # 简化示例
        return 80.0  # 示例值
    
    def _calculate_technical_score(self, stocks: List[str], date: str) -> float:
        """计算技术动量因子得分（0-100）"""
        # 使用Alpha191因子
        alpha_factors = self.factor_engine.get_alpha_factors(
            stocks=stocks,
            date=date,
            alpha_version='191'
        )
        
        # 综合多个Alpha因子
        # 简化示例
        return 65.0  # 示例值
    
    def _calculate_sentiment_score(self, stocks: List[str], date: str) -> float:
        """计算市场情绪因子得分（0-100）"""
        # 使用AKShare获取舆情数据
        # 简化示例
        return 70.0  # 示例值
    
    def _get_industry_stocks(self, industry_code: str, date: str) -> List[str]:
        """获取行业股票列表"""
        # 使用JQData获取行业成分股
        import jqdatasdk as jq
        stocks = jq.get_industry_stocks(industry_code, date=date)
        return stocks
```

---

## 4. 历史数据验证测试方案

### 4.1 验证目标

1. **因子有效性验证**：验证因子是否能预测主线
2. **因子组合有效性**：验证因子组合是否优于单个因子
3. **预测准确性**：验证预测的主线是否确实获得超额收益
4. **时间稳定性**：验证因子在不同时间段的有效性

### 4.2 测试设计

#### 4.2.1 回测框架

**时间范围**：
- 训练期：2020-01-01 至 2022-12-31（3年）
- 验证期：2023-01-01 至 2024-12-31（2年）

**测试方法**：
- **滚动窗口回测**：使用滚动窗口训练和验证
- **时间序列交叉验证**：避免未来信息泄露

#### 4.2.2 验证指标

**IC（Information Coefficient）**：
- **定义**：因子值与下一期收益的相关系数
- **计算公式**：
  ```
  IC(t) = corr(Factor(t), Return(t+1))
  ```
- **目标**：IC均值 > 0.05，IC IR > 0.5

**IR（Information Ratio）**：
- **定义**：IC均值 / IC标准差
- **计算公式**：
  ```
  IR = mean(IC) / std(IC)
  ```
- **目标**：IR > 0.5（稳定性要求）

**分组回测**：
- 按因子值分为5组（Q1-Q5）
- 计算各组平均收益
- 验证是否单调递增（Q5收益 > Q4 > ... > Q1）

**多空组合收益**：
- 做多Q5（最高组），做空Q1（最低组）
- 计算多空组合收益
- 目标：年化多空收益 > 10%

#### 4.2.3 测试脚本设计

```python
"""
主线预测因子验证测试
"""
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
import numpy as np
from core.factors.factor_evaluator import FactorEvaluator
from core.factors.jqdata_factor_engine import JQDataFactorEngine
from jqdata.client import JQDataClient

class MainlineFactorValidator:
    """主线因子验证器"""
    
    def __init__(self, jq_client: JQDataClient):
        self.jq_client = jq_client
        self.factor_engine = JQDataFactorEngine(jq_client)
        self.evaluator = FactorEvaluator(jq_client=jq_client)
    
    def validate_factor_combination(
        self,
        industries: List[str],
        start_date: str,
        end_date: str,
        rebalance_freq: str = 'W'  # 周度调仓
    ) -> Dict:
        """
        验证因子组合有效性
        
        Args:
            industries: 行业代码列表
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            rebalance_freq: 调仓频率（'W'周度, 'M'月度）
        
        Returns:
            验证结果字典
        """
        results = {
            'ic_statistics': {},
            'group_backtest': {},
            'long_short_return': {},
            'factor_importance': {}
        }
        
        # 1. IC时间序列分析
        ic_results = self._calculate_ic_series(
            industries, start_date, end_date
        )
        results['ic_statistics'] = {
            'ic_mean': ic_results['ic'].mean(),
            'ic_std': ic_results['ic'].std(),
            'ic_ir': ic_results['ic'].mean() / ic_results['ic'].std(),
            'ic_positive_ratio': (ic_results['ic'] > 0).mean(),
            'ic_series': ic_results
        }
        
        # 2. 分组回测
        group_results = self._group_backtest(
            industries, start_date, end_date, rebalance_freq
        )
        results['group_backtest'] = {
            'group_returns': group_results['group_returns'],
            'is_monotonic': group_results['is_monotonic'],
            'top_group_return': group_results['group_returns']['Q5'],
            'bottom_group_return': group_results['group_returns']['Q1']
        }
        
        # 3. 多空组合收益
        long_short = group_results['group_returns']['Q5'] - group_results['group_returns']['Q1']
        results['long_short_return'] = {
            'total_return': long_short,
            'annualized_return': self._annualize_return(long_short, start_date, end_date),
            'sharpe_ratio': self._calculate_sharpe(long_short)
        }
        
        # 4. 因子重要性分析
        factor_importance = self._analyze_factor_importance(
            industries, start_date, end_date
        )
        results['factor_importance'] = factor_importance
        
        return results
    
    def _calculate_ic_series(
        self,
        industries: List[str],
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """计算IC时间序列"""
        dates = pd.date_range(start_date, end_date, freq='W')
        ic_values = []
        
        for date in dates:
            # 计算当前日期的主线预测得分
            mainline_scores = {}
            for industry in industries:
                score = self._calculate_mainline_score(industry, date.strftime('%Y-%m-%d'))
                mainline_scores[industry] = score['total_score']
            
            # 获取下一期收益（未来1周收益）
            next_date = date + timedelta(days=7)
            if next_date > pd.to_datetime(end_date):
                continue
            
            returns = self._get_industry_returns(industries, next_date.strftime('%Y-%m-%d'))
            
            # 计算IC
            if len(mainline_scores) > 0 and len(returns) > 0:
                ic = np.corrcoef(list(mainline_scores.values()), list(returns.values()))[0, 1]
                ic_values.append({
                    'date': date,
                    'ic': ic if not np.isnan(ic) else 0
                })
        
        return pd.DataFrame(ic_values)
    
    def _group_backtest(
        self,
        industries: List[str],
        start_date: str,
        end_date: str,
        rebalance_freq: str
    ) -> Dict:
        """分组回测"""
        dates = pd.date_range(start_date, end_date, freq=rebalance_freq)
        group_returns = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': [], 'Q5': []}
        
        for date in dates:
            # 计算当前日期的主线预测得分
            scores = {}
            for industry in industries:
                score = self._calculate_mainline_score(industry, date.strftime('%Y-%m-%d'))
                scores[industry] = score['total_score']
            
            # 分组（按得分分5组）
            sorted_industries = sorted(scores.items(), key=lambda x: x[1])
            n = len(sorted_industries)
            groups = {
                'Q1': sorted_industries[:n//5],
                'Q2': sorted_industries[n//5:2*n//5],
                'Q3': sorted_industries[2*n//5:3*n//5],
                'Q4': sorted_industries[3*n//5:4*n//5],
                'Q5': sorted_industries[4*n//5:]
            }
            
            # 计算下一期收益
            next_date = date + timedelta(days=7 if rebalance_freq == 'W' else 30)
            if next_date > pd.to_datetime(end_date):
                break
            
            returns = self._get_industry_returns(
                industries, next_date.strftime('%Y-%m-%d')
            )
            
            # 计算各组平均收益
            for group_name, group_industries in groups.items():
                group_return = np.mean([
                    returns.get(ind, 0) for ind, _ in group_industries
                ])
                group_returns[group_name].append(group_return)
        
        # 计算累计收益
        cumulative_returns = {
            group: (1 + pd.Series(returns)).prod() - 1
            for group, returns in group_returns.items()
        }
        
        # 验证单调性
        is_monotonic = (
            cumulative_returns['Q5'] > cumulative_returns['Q4'] >
            cumulative_returns['Q3'] > cumulative_returns['Q2'] >
            cumulative_returns['Q1']
        )
        
        return {
            'group_returns': cumulative_returns,
            'is_monotonic': is_monotonic
        }
    
    def _calculate_mainline_score(self, industry: str, date: str) -> Dict:
        """计算主线预测得分（调用MainlinePredictionFactorCombination）"""
        # 简化示例，实际应该调用MainlinePredictionFactorCombination
        return {'total_score': np.random.uniform(50, 90)}
    
    def _get_industry_returns(self, industries: List[str], date: str) -> Dict[str, float]:
        """获取行业收益率"""
        # 使用JQData获取行业收益率
        # 简化示例
        return {ind: np.random.uniform(-0.05, 0.05) for ind in industries}
    
    def _annualize_return(self, total_return: float, start_date: str, end_date: str) -> float:
        """年化收益率"""
        days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        years = days / 365.25
        return (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
    
    def _calculate_sharpe(self, returns: List[float]) -> float:
        """计算夏普比率"""
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        return np.mean(returns) / np.std(returns) * np.sqrt(52)  # 假设周度收益
    
    def _analyze_factor_importance(
        self,
        industries: List[str],
        start_date: str,
        end_date: str
    ) -> Dict[str, float]:
        """分析因子重要性（使用相关性分析或机器学习）"""
        # 简化示例，实际可以使用随机森林等模型分析特征重要性
        return {
            'macro': 0.20,
            'capital_flow': 0.30,
            'industry_prosperity': 0.25,
            'technical_momentum': 0.15,
            'market_sentiment': 0.10
        }

# 使用示例
def run_validation():
    """运行验证测试"""
    from jqdata.client import JQDataClient
    from config.config_manager import get_config_manager
    
    # 初始化
    config_manager = get_config_manager()
    jq_config = config_manager.get_jqdata_config()
    jq_client = JQDataClient()
    jq_client.authenticate(jq_config.get('username'), jq_config.get('password'))
    
    validator = MainlineFactorValidator(jq_client)
    
    # 选择测试行业（申万一级行业）
    test_industries = [
        '801010',  # 农林牧渔
        '801020',  # 采掘
        '801030',  # 化工
        # ... 更多行业
    ]
    
    # 运行验证
    results = validator.validate_factor_combination(
        industries=test_industries,
        start_date='2020-01-01',
        end_date='2024-12-31',
        rebalance_freq='W'
    )
    
    # 输出结果
    print("=" * 60)
    print("主线预测因子验证结果")
    print("=" * 60)
    print(f"IC均值: {results['ic_statistics']['ic_mean']:.4f}")
    print(f"IC IR: {results['ic_statistics']['ic_ir']:.4f}")
    print(f"IC正比率: {results['ic_statistics']['ic_positive_ratio']:.2%}")
    print(f"分组单调性: {results['group_backtest']['is_monotonic']}")
    print(f"多空年化收益: {results['long_short_return']['annualized_return']:.2%}")
    print(f"夏普比率: {results['long_short_return']['sharpe_ratio']:.4f}")
    print("=" * 60)

if __name__ == '__main__':
    run_validation()
```

### 4.3 验证标准

**因子有效性标准**：
- ✅ IC均值 > 0.05
- ✅ IC IR > 0.5（稳定性）
- ✅ IC正比率 > 55%（方向一致性）
- ✅ 分组收益单调递增
- ✅ 多空年化收益 > 10%
- ✅ 夏普比率 > 1.0

---

## 5. 完整工作流集成

### 5.1 9步工作流中的位置

**步骤3：投资主线（mainline）**

```
步骤1: 📡 信息获取 (data_source)
  └─ 数据源检测、数据更新
      ↓
步骤2: 📈 市场趋势 (market_trend)
  └─ 市场趋势分析、市场状态判断
      ↓
步骤3: 🔥 投资主线 (mainline) ← 本文档重点
  ├─ 主线识别（使用AShareMainlineEngine）
  ├─ 主线评分（使用因子组合）
  └─ 主线验证（使用历史数据验证）
      ↓
步骤4: 📦 候选池构建 (candidate_pool)
  └─ 根据主线构建候选股票池
      ↓
步骤5: 📊 因子构建 (factor)
  └─ 因子推荐、因子配置
      ↓
步骤6: 🛠️ 策略生成 (strategy)
  └─ 策略代码生成
      ↓
步骤7: 🔄 回测验证 (backtest)
  └─ 策略回测
      ↓
步骤8: ⚙️ 策略优化 (optimization)
  └─ 参数优化
      ↓
步骤9: 📄 报告生成 (report)
  └─ 生成研究报告
```

### 5.2 集成代码示例

```python
"""
9步工作流 - 步骤3：投资主线（完整集成）
"""
from markets.ashare.mainline.engine import AShareMainlineEngine
from core.factors.jqdata_factor_engine import JQDataFactorEngine
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

class MainlineWorkflowStep:
    """主线工作流步骤"""
    
    def __init__(self):
        # 初始化数据源
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        
        self.jq_client = JQDataClient()
        self.jq_client.authenticate(
            jq_config.get('username'),
            jq_config.get('password')
        )
        
        # 初始化引擎
        self.mainline_engine = AShareMainlineEngine()
        self.factor_engine = JQDataFactorEngine(self.jq_client)
        self.factor_combo = MainlinePredictionFactorCombination(self.jq_client)
    
    def execute(
        self,
        market_trend_result: Dict,
        period: str = 'medium'
    ) -> Dict:
        """
        执行主线识别步骤
        
        Args:
            market_trend_result: 步骤2（市场趋势）的结果
            period: 主线期限（short/medium/long）
        
        Returns:
            {
                'mainlines': List[Mainline],
                'mainline_scores': Dict[str, float],
                'validation_results': Dict,
                'data_traces': List[DataTrace],
                'analysis_steps': List[AnalysisStep]
            }
        """
        # 1. 运行主线识别引擎
        mainline_result = self.mainline_engine.run_full_analysis()
        
        # 2. 使用因子组合对每条主线评分
        mainline_scores = {}
        for mainline in mainline_result['mainlines']:
            # 获取主线相关行业
            industries = self._get_mainline_industries(mainline)
            
            # 计算因子组合得分
            score = self.factor_combo.calculate_mainline_score(
                industry_code=industries[0] if industries else None,
                date=datetime.now().strftime('%Y-%m-%d'),
                period=period
            )
            mainline_scores[mainline.name] = score
        
        # 3. 历史数据验证（可选，用于评估因子有效性）
        validation_results = None
        if self._should_validate():
            validation_results = self._run_validation(mainline_result['mainlines'])
        
        return {
            'mainlines': mainline_result['mainlines'],
            'mainline_scores': mainline_scores,
            'validation_results': validation_results,
            'data_traces': mainline_result['data_traces'],
            'analysis_steps': mainline_result['analysis_steps']
        }
    
    def _get_mainline_industries(self, mainline) -> List[str]:
        """获取主线相关行业代码"""
        # 根据主线名称匹配行业代码
        # 简化示例
        return ['801010', '801020']
    
    def _should_validate(self) -> bool:
        """是否应该运行验证（可以设置开关）"""
        return True
    
    def _run_validation(self, mainlines) -> Dict:
        """运行历史数据验证"""
        validator = MainlineFactorValidator(self.jq_client)
        industries = self._get_all_mainline_industries(mainlines)
        
        return validator.validate_factor_combination(
            industries=industries,
            start_date='2020-01-01',
            end_date='2024-12-31'
        )
    
    def _get_all_mainline_industries(self, mainlines) -> List[str]:
        """获取所有主线涉及的行业"""
        all_industries = []
        for mainline in mainlines:
            industries = self._get_mainline_industries(mainline)
            all_industries.extend(industries)
        return list(set(all_industries))
```

---

## 6. 总结与下一步

### 6.1 完成的工作

✅ **聚宽正式账号配置**：确认了账号权限和配置方法  
✅ **市场主线研究框架**：基于8步分析流程  
✅ **因子组合设计**：5大类因子，权重分配合理  
✅ **验证测试方案**：IC/IR分析、分组回测、多空组合  
✅ **工作流集成**：集成到9步工作流的步骤3

### 6.2 下一步优化方向

1. **因子优化**：
   - 使用机器学习方法自动优化因子权重
   - 增加更多Alpha191因子到技术动量因子组合
   - 使用CNE5风格因子进行风险调整

2. **验证完善**：
   - 增加更多历史回测周期
   - 添加不同市场环境下的验证（牛市、熊市、震荡市）
   - 添加因子失效预警机制

3. **实时监控**：
   - 实时计算主线预测得分
   - 主线轮动信号提醒
   - 主线强度变化监控

4. **文档完善**：
   - 添加更多代码示例
   - 添加最佳实践案例
   - 添加常见问题解答

---

*文档版本: v1.0 | 最后更新: 2025-01-01*

