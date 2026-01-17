# Claude AI 开发原则与经验教训

> **版本**: v1.0  
> **创建**: 2026-01-10  
> **目的**: 记录开发原则，避免重复犯错

---

## 📋 核心开发原则

### 1. 研究先行，编码后置
- **充分使用知识库和网络爬虫**，做好深度研究后再开始编码
- 确保**推理的深度**，不要急于写代码
- 理解问题本质，而非表面症状

### 2. 小步迭代，测试验证
- **小步验证**，先确保最简单的情况能工作
- 测试通过后再往前推进
- 每一步都应该是可验证的、可回滚的

### 3. 简单优先，避免过度设计
- **不要在有严重错误的代码上修补**
- 如果代码连续失败2次以上，**重新写代码**而非继续调试
- 先写能工作的简单版本，再逐步增加功能

### 4. 数据驱动，假设验证
- 对于数据挖掘任务：
  - 牛市研究**不需要评分**，指定时间段默认为牛市
  - 挖掘高回报股票的共性因子及**早期识别（预测因子）**
  - 区分短/中/长周期

---

## 🔍 错误案例分析

### 案例: `bull_market_high_return_miner.py` 连续失败

#### 原代码问题

1. **数据提取方式复杂且脆弱**
   - `_extract_field_dataframe` 尝试处理多种返回格式（Panel、MultiIndex、dict）
   - 没有正确处理 JQData 当前返回的长格式 DataFrame

2. **没有设置 `panel=False`**
   ```python
   # ❌ 错误：没有显式指定返回格式
   panel = self.jq.get_price(
       security=batch,
       start_date=start_dt,
       end_date=end_date,
       frequency='daily',
       fields=fields,
       skip_paused=True,
       fq='post'
   )
   
   # ✅ 正确：显式设置 panel=False 返回长格式 DataFrame
   price_data = self.jq.get_price(
       stocks,
       start_date=ext_start,
       end_date=end_date,
       frequency='daily',
       fields=['close', 'volume', 'money'],
       skip_paused=True,
       fq='post',
       panel=False  # 关键！
   )
   ```

3. **过于复杂的架构**
   - 使用了 `HorizonConfig`、`MinerConfig`、`HighReturnCase` 等多层抽象
   - 增加了复杂性和出错可能性

4. **不必要的牛市评分系统**
   - 用户已明确"默认为牛市研究，不需要评分"
   - 增加了 MarketRegimeDetector 依赖，但实际上只需要在指定时间段内筛选高回报案例

#### 正确实现（`simple_high_return_miner.py`）

```python
# 1. 明确使用 panel=False
price_data = self.jq.get_price(
    stocks,
    start_date=ext_start,
    end_date=end_date,
    frequency='daily',
    fields=['close', 'volume', 'money'],
    skip_paused=True,
    fq='post',
    panel=False  # 返回长格式 DataFrame
)

# 2. 标准化列名
if 'time' in price_data.columns:
    price_data = price_data.rename(columns={'time': 'date'})

# 3. 简单的回报率计算
for code, group in price_data.groupby('code'):
    df = group.sort_values('date').copy()
    df['return_5d'] = df['close'].pct_change(5).shift(-5) * 100
    df['return_20d'] = df['close'].pct_change(20).shift(-20) * 100
    df['return_60d'] = df['close'].pct_change(60).shift(-60) * 100
```

---

## 📊 JQData 最佳实践

### 获取股票列表
```python
all_stocks = jq.get_all_securities(types=['stock'], date=end_date)
# 过滤ST、新股
valid = all_stocks[
    ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
    (all_stocks['start_date'].astype(str) < one_year_ago)
]
```

### 批量获取价格数据
```python
# 关键参数：panel=False 返回长格式 DataFrame
price_data = jq.get_price(
    stocks,                    # List[str]
    start_date=start_date,
    end_date=end_date,
    frequency='daily',
    fields=['open', 'close', 'high', 'low', 'volume', 'money'],
    skip_paused=True,
    fq='post',                 # 后复权（推荐）
    panel=False                # 返回 DataFrame，不是 Panel
)

# 返回格式：
# | time       | code        | close  | volume | ... |
# | 2019-01-02 | 000001.XSHE | 10.5   | 12345  | ... |
```

### 处理返回数据
```python
# 标准化列名
if 'time' in price_data.columns:
    price_data = price_data.rename(columns={'time': 'date'})

# 转换为透视表（如需要）
pivot = price_data.pivot(index='date', columns='code', values='close')
```

---

## 🎯 高回报股票挖掘原则

### 周期定义
- **短期**: 5个交易日，阈值 >= 8-10%
- **中期**: 20个交易日，阈值 >= 20-25%
- **长期**: 60个交易日，阈值 >= 50-60%

### 挖掘目标
1. **共性因子**: 高回报股票在买入时有哪些共同特征
2. **预测因子**: 哪些因子能够**提前**识别高回报机会
3. **区分周期**: 短/中/长期高回报的因子可能不同

### 因子类型
- **动量因子**: momentum_5d, momentum_20d, momentum_60d
- **位置因子**: rel_position (相对52周高低的位置)
- **价值因子**: market_cap, pe, pb
- **质量因子**: roe, growth
- **资金因子**: turnover_rate, volume_ratio

---

## ⚠️ 常见陷阱

1. **不要假设 API 返回格式**：始终打印检查返回数据的类型和结构
2. **不要在失败代码上反复修补**：超过2次失败就重写
3. **不要过度抽象**：先写能工作的代码，再考虑抽象
4. **不要忽略测试**：每一步都应该有可验证的输出
5. **不要跳过研究阶段**：充分理解问题再动手编码

---

## 📁 重要文件位置

- **简单高回报挖掘器**: `core/data_mining/simple_high_return_miner.py`
- **原问题代码**: `core/data_mining/bull_market_high_return_miner.py`
- **第五次牛市数据**: `output/research/fifth_bull_market_cases/`

---

## 🔧 MCP配置和Python路径

### MCP Python路径配置

**工作目录**: `/home/taotao/.cursor/worktrees/TRQuant/ope`  
**venv Python路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3`  
**MCP安装路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/lib/python3.12/site-packages/mcp/`

### MCPClient自动查找逻辑

`MCPClient._find_python_path()` 按以下顺序查找Python解释器：

1. **项目根目录venv** (优先级最高)
   - Linux/Mac: `{project_root}/venv/bin/python3`
   - Windows: `{project_root}/venv/Scripts/python.exe`

2. **TRQUANT_ROOT环境变量venv**
   - Linux/Mac: `{TRQUANT_ROOT}/venv/bin/python3`
   - Windows: `{TRQUANT_ROOT}/venv/Scripts/python.exe`

3. **extension/venv** (备用)
   - Linux/Mac: `{project_root}/extension/venv/bin/python`
   - Windows: `{project_root}/extension/venv/Scripts/python.exe`

4. **系统Python** (最后回退)
   - `sys.executable`

### 常见错误处理

**错误**: `MCP SDK不可用，请安装: pip install mcp`

**原因**: 
- 使用了系统Python而非venv Python
- venv中未安装MCP SDK

**解决方案**:
1. 确保使用venv Python: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3`
2. 在venv中安装MCP: `./venv/bin/pip install mcp`
3. MCPClient会自动查找venv Python，无需手动配置

**验证方法**:
```python
from pathlib import Path
venv_python = Path('/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3')
import subprocess
result = subprocess.run([str(venv_python), '-c', 'import mcp; print(mcp.__file__)'], capture_output=True)
# 应该输出MCP路径，无错误
```

---

## 📊 第五次牛市(2019-2021)因子发现

### 核心预测因子

| 周期 | 买入时5日动量(中位数) | 负动量占比 | 启示 |
|------|----------------------|------------|------|
| 短期 | +3.9% | 30.4% | 追动量 |
| 中期 | +1.8% | - | 适度确认 |
| **长期** | **+0.7%** | **43.8%** | **平静时布局** |

### 关键结论

1. **长期翻倍股的黄金法则**: 在股价平静或小幅回调时买入
   - 43.8%的长期翻倍股在买入时处于下跌状态
   - 5日动量中位数仅0.7%

2. **最佳买入时机**: 
   - 长期：牛市初期(2019-01)或大跌后反弹(2020-04)
   - 短期：行情加速阶段(2020-07)

3. **选股条件（长期布局）**:
   - 5日动量 < 3%
   - 股价处于52周相对低位
   - ROE > 5%

### 详细报告

`output/research/FIFTH_BULL_MARKET_FACTOR_ANALYSIS.md`

---

## 📈 短期动量策略深度研究

### 研究概览

- **样本**: 1000个5日高回报(≥10%)案例
- **时期**: 第五次牛市 2019-01-01 ~ 2021-03-31
- **完整报告**: `output/research/SHORT_TERM_MOMENTUM_STRATEGY_RESEARCH.md`

### 三大推荐策略

| 策略 | 入场条件 | 预期均值 | >50%概率 | 适用场景 |
|------|----------|----------|----------|----------|
| **强动量突破** | mom_5d ≥ 15% | 47.2% | 38.5% | 追强势龙头 |
| **加速突破** | mom_5d>10% & mom_20d>30% | 47.2% | 33.3% | 双因子确认 |
| **回调反弹** | mom_5d<0 & mom_20d>15% | 48.0% | 7.0% | 低吸强势股 |

### 动量分组回报对比

```
5日动量区间    均值回报    极端概率(>50%)
< -5%         39.9%       7.2%
-5% ~ 0%      41.4%       -
0% ~ 5%       39.0%       12.2%
5% ~ 10%      42.6%       17.7%
10% ~ 20%     43.7%       26.4%
> 20%         46.9%       40.4%  ← 最佳
```

### 时间规律

- **最佳月份**: 4月 (均值61.7%)
- **春季躁动**: 2-3月
- **中报行情**: 7月
- **最佳年份**: 2019年 (牛市初期)

### 关键洞察

1. **追动量有效**: 5日动量越高，后续回报越高
2. **双因子更稳**: mom_5d + mom_20d 组合确认性更高
3. **涨停延续**: 近期有涨停的股票继续上涨概率更高
4. **深市主板占优**: 000开头股票占79.2%

### 策略筛选器

**代码位置**: `core/data_mining/momentum_strategy_screener.py`

**使用方法**:
```bash
# 筛选所有策略
python core/data_mining/momentum_strategy_screener.py --strategy all

# 仅强动量突破
python core/data_mining/momentum_strategy_screener.py --strategy strong_breakout

# 指定日期筛选
python core/data_mining/momentum_strategy_screener.py --date 2026-01-09
```

### 风控建议

| 参数 | 建议值 |
|------|--------|
| 单票仓位 | ≤ 10% |
| 止损位 | -8% |
| 止盈位 | +30% |
| 持仓周期 | 5天 |
| 最大持仓 | 10只 |

---

**最后更新**: 2026-01-10
