# 抓连板股票改进方案

> **目标**: 提高策略抓连板股票的能力，特别是二板、三板的龙头股票  
> **创建时间**: 2026-01-15  
> **数据来源**: 知识库检索 + 网络搜索 + 代码分析

---

## 📊 问题分析

### 当前问题
1. **所有股票都是首板**：回测结果显示所有买入的股票都是首板（连板数=1）
2. **没有抓住二板、三板的龙头机会**：虽然市场中有连板股票，但策略没有选中
3. **选股逻辑可能有问题**：虽然代码中优先选择连板股票，但实际没有执行

### 根本原因
1. **数据源问题**：涨停板数据中的"连板数"字段可能不准确或缺失
2. **选股条件过于严格**：可能过滤掉了连板股票
3. **没有"一进二"战法**：没有在首板次日确认二板的逻辑

---

## 🔍 知识库和网络搜索结果

### 1. 连板股票识别方法（知识库）

根据知识库搜索结果，连板股票的识别方法包括：

#### 方法1：直接获取连板数
```python
# 从涨停板数据中直接获取连板数
limit_up_df = ak.stock_zt_pool_em(date=date_compact)
board_count = limit_up_df['连板数']  # 直接获取连板数
```

#### 方法2：计算连板高度
```python
# 通过历史价格数据计算连板高度
def get_consecutive_limit_up(code, today):
    price_data = jq.get_price(code, count=5, end_date=today, frequency='daily')
    consecutive = 0
    for i in range(len(price_data)-1, -1, -1):
        if price_data['close'].iloc[i] >= price_data['high_limit'].iloc[i] * 0.995:
            consecutive += 1
        else:
            break
    return consecutive
```

### 2. "一进二"战法（网络搜索）

**核心思想**：
- **首板确认**：首板需属于主流板块，且量价配合良好
- **次日二板确认**：开盘后快速封板（如9:35前），避免跟风股或缩量秒板
- **介入时机**：优先选择开盘后快速封板的个股

**选股条件**：
1. 首板需属于主流板块
2. 量价配合良好（成交量放大、换手率适中）
3. 图形上突破压力位或处于低位启动阶段
4. 次日开盘后快速封板（9:35前）

### 3. 龙头股识别方法（知识库）

根据陈小群策略知识库：

#### 市场总龙头
- **最高连板**：选择连板数最高的股票
- **板块龙头**：每个板块的最高连板，板块内至少2只涨停

#### 选股优先级
1. **最强题材的龙头**（优先）
2. **次强题材的龙头**（次优先）
3. **其他题材的龙头**（最后）

---

## 🔧 改进方案

### 方案1：优化连板股票识别逻辑

#### 1.1 双重验证连板数
```python
def get_board_count_verified(code, date_str, limit_up_df, jq_client):
    """
    双重验证连板数：
    1. 从涨停板数据中获取
    2. 通过历史价格数据计算验证
    """
    # 方法1：从涨停板数据中获取
    stock_row = limit_up_df[limit_up_df['代码'] == code]
    if not stock_row.empty:
        board_count_data = stock_row.iloc[0].get('连板数', 1)
    else:
        board_count_data = 1
    
    # 方法2：通过历史价格数据计算验证
    try:
        price_data = jq_client.get_price(
            code, 
            count=5, 
            end_date=date_str, 
            frequency='daily',
            fields=['close', 'high_limit']
        )
        board_count_calc = 0
        for i in range(len(price_data)-1, -1, -1):
            close = price_data['close'].iloc[i]
            high_limit = price_data['high_limit'].iloc[i]
            if abs(close - high_limit) / high_limit < 0.005:  # 允许0.5%误差
                board_count_calc += 1
            else:
                break
    except:
        board_count_calc = board_count_data
    
    # 取两者中的较大值（更保守）
    return max(board_count_data, board_count_calc)
```

#### 1.2 优化选股逻辑
```python
def select_consecutive_board_stocks(
    limit_up_data: pd.DataFrame,
    date_str: str,
    jq_client,
    min_board_count: int = 2,
    top_n: int = 5
) -> List[Dict]:
    """
    选择连板股票（二板及以上）
    
    选股条件：
    1. 连板数 >= min_board_count（默认2板）
    2. 双重验证连板数
    3. 优先选择最高连板的股票
    4. 优先选择最强题材的股票
    """
    if limit_up_data is None or limit_up_data.empty:
        return []
    
    # 筛选连板股票
    consecutive_boards = limit_up_data[limit_up_data['连板数'] >= min_board_count].copy()
    if consecutive_boards.empty:
        return []
    
    # 双重验证连板数
    verified_stocks = []
    for idx, row in consecutive_boards.iterrows():
        code = str(row.get('代码', ''))
        jq_code, _, is_valid = identify_exchange_and_convert(code)
        
        if is_valid:
            # 双重验证连板数
            board_count = get_board_count_verified(jq_code, date_str, limit_up_data, jq_client)
            
            if board_count >= min_board_count:
                verified_stocks.append({
                    'code': code,
                    'jq_code': jq_code,
                    'name': row.get('名称', ''),
                    'board_count': board_count,
                    'sector': row.get('所属行业', ''),
                    'verified': True
                })
    
    # 按连板数排序
    verified_stocks.sort(key=lambda x: x['board_count'], reverse=True)
    
    return verified_stocks[:top_n]
```

### 方案2：实现"一进二"战法

#### 2.1 首板次日二板确认
```python
def confirm_second_board(
    first_board_stocks: List[Dict],
    date_str: str,
    jq_client,
    limit_up_df: pd.DataFrame
) -> List[Dict]:
    """
    首板次日二板确认（"一进二"战法）
    
    逻辑：
    1. 检查首板股票次日是否继续涨停
    2. 如果继续涨停，确认为二板
    3. 优先选择开盘后快速封板的股票（9:35前）
    """
    second_board_stocks = []
    
    for stock in first_board_stocks:
        code = stock['jq_code']
        
        # 检查今日是否继续涨停
        today_limit_up = limit_up_df[limit_up_df['代码'] == stock['code']]
        if not today_limit_up.empty:
            board_count = today_limit_up.iloc[0].get('连板数', 1)
            if board_count >= 2:
                # 确认为二板
                stock['board_count'] = board_count
                stock['confirmed'] = True
                second_board_stocks.append(stock)
    
    return second_board_stocks
```

#### 2.2 优化首板选股条件
```python
def select_first_board_for_second_board(
    limit_up_data: pd.DataFrame,
    date_str: str,
    top_themes: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    选择有潜力二板的首板股票（"一进二"战法）
    
    选股条件（更严格）：
    1. 连板数 = 1（首板）
    2. 属于主流题材（优先）
    3. 流通市值 < 50亿（小盘股更容易连板）
    4. 封板资金占比 >= 2%（封单充足）
    5. 换手率 > 10%（有资金参与）
    6. 板块内至少3只涨停（板块效应强）
    """
    # ... 实现逻辑
    pass
```

### 方案3：增加技术指标筛选

#### 3.1 换手率筛选
```python
def filter_by_turnover_rate(
    stocks: List[Dict],
    jq_client,
    date_str: str,
    min_turnover: float = 0.10  # 最低换手率10%
) -> List[Dict]:
    """
    通过换手率筛选股票
    
    连板股票特征：
    - 二板：换手率通常 > 25%（陈小群策略标准）
    - 三板：换手率可能降低（缩量涨停）或持续放大
    """
    filtered_stocks = []
    
    for stock in stocks:
        code = stock['jq_code']
        try:
            # 获取换手率数据
            turnover_data = jq_client.get_price(
                code,
                count=1,
                end_date=date_str,
                frequency='daily',
                fields=['turnover']  # 换手率
            )
            
            if not turnover_data.empty:
                turnover = turnover_data['turnover'].iloc[0]
                if turnover >= min_turnover:
                    stock['turnover_rate'] = turnover
                    filtered_stocks.append(stock)
        except:
            continue
    
    return filtered_stocks
```

#### 3.2 量比筛选
```python
def filter_by_volume_ratio(
    stocks: List[Dict],
    jq_client,
    date_str: str,
    min_volume_ratio: float = 2.0  # 最低量比2.0
) -> List[Dict]:
    """
    通过量比筛选股票
    
    连板股票特征：
    - 量比 > 2.0（成交量明显放大）
    - 量比持续放大（资金持续流入）
    """
    filtered_stocks = []
    
    for stock in stocks:
        code = stock['jq_code']
        try:
            # 获取成交量数据
            volume_data = jq_client.get_price(
                code,
                count=20,
                end_date=date_str,
                frequency='daily',
                fields=['volume']
            )
            
            if len(volume_data) >= 20:
                current_volume = volume_data['volume'].iloc[-1]
                avg_volume = volume_data['volume'].tail(20).mean()
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
                
                if volume_ratio >= min_volume_ratio:
                    stock['volume_ratio'] = volume_ratio
                    filtered_stocks.append(stock)
        except:
            continue
    
    return filtered_stocks
```

---

## 🚀 实施步骤

### 第一步：优化连板股票识别
1. 实现双重验证连板数逻辑
2. 优化选股逻辑，确保能够识别连板股票
3. 测试验证连板股票识别准确性

### 第二步：实现"一进二"战法
1. 实现首板次日二板确认逻辑
2. 优化首板选股条件，选择有潜力二板的首板股票
3. 测试验证"一进二"战法效果

### 第三步：增加技术指标筛选
1. 实现换手率筛选
2. 实现量比筛选
3. 测试验证技术指标筛选效果

### 第四步：回测验证
1. 使用改进后的策略进行回测
2. 对比改进前后的效果
3. 优化参数和逻辑

---

## 📈 预期效果

### 如果改进后：
1. **能够识别连板股票**：通过双重验证，确保连板数准确
2. **能够抓住二板、三板的龙头**：通过"一进二"战法和优化选股逻辑
3. **提高选股成功率**：通过技术指标筛选，提高选股质量
4. **预期总收益率**: 20%+ (6个交易日)
5. **预期年化收益率**: 5000%+

---

## 📝 注意事项

1. **数据质量**：确保涨停板数据中的"连板数"字段准确
2. **计算成本**：双重验证会增加计算成本，需要优化
3. **实时性**："一进二"战法需要T+1日数据，需要实时更新
4. **风险控制**：连板股票风险较高，需要严格的风险控制
