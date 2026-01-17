# QMT passorder 下单函数完整指南

> **更新日期**: 2026-01-10  
> **来源**: QMT官方文档示例  
> **已存入知识库**: ✅ 5条示例已添加

---

## 📋 passorder 函数参数说明

```python
passorder(买卖方向, 开平标志, 账号, 股票代码, 价格类型, 价格, 数量/金额, 投资备注, 快速交易参数, ContextInfo)
```

### 参数详解

| 参数位置 | 参数名 | 说明 | 常用值 |
|---------|--------|------|--------|
| 1 | 买卖方向 | 买入/卖出 | `23`=买入, `24`=卖出 |
| 2 | 开平标志 | 开仓/平仓 | `1101`=开仓, `1102`=平仓 |
| 3 | 账号 | 交易账号 | `account` (界面选择) |
| 4 | 股票代码 | 股票代码 | `'000001.SZ'` |
| 5 | 价格类型 | 下单价格类型 | `5`=最新价, `11`=限价, `14`=对手价 |
| 6 | 价格 | 限价价格 | 限价时填具体价格，最新价/对手价填`0`或`-1` |
| 7 | 数量/金额 | 买入数量或金额 | 股数（买入）或金额（元，买入） |
| 8 | 投资备注 | 备注字符串 | 可选，用于区分不同委托 |
| 9 | 快速交易参数 | 下单时机 | `0`=K线走完下单, `1`=当前K线立即下单, `2`=立即下单不等待 |
| 10 | ContextInfo | 上下文对象 | `ContextInfo` |

---

## 📚 示例代码

### 1. 基础下单示例

```python
#coding:gbk
c = 0
s = '000001.SZ'

def init(ContextInfo):
    # 立即下单 用最新价买入股票s 100股，且指定投资备注
    passorder(23,1101,account,s,5,0,100,'1',2,'tzbz',ContextInfo) 
    pass

def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        #历史k线不应该发出实盘信号 跳过
        return

    if ContextInfo.is_last_bar():
        global c
        c +=1 
        if c ==1:
            # 用14.00元限价买入股票s 100股
            passorder(23,1101,account,s,11,14.00,100,1,ContextInfo)  # 当前k线为最新k线 则立即下单
            # 用最新价限价买入股票s 100股
            passorder(23,1101,account,s,5,-1,100,0,ContextInfo)  # K线走完下单
            # 用最新价限价买入股票s 1000元
            passorder(23, 1102, account, s, 5, 0,1000, 2, ContextInfo)  # 不管是不是最新K线，立即下单
```

### 2. 集合竞价下单

```python
#coding:gbk
import time
c = 0
s = '000001.SZ'

def init(ContextInfo):
    # 设置定时器，历史时间表示会在一次间隔时间后开始调用回调函数
    ContextInfo.run_time("myHandlebar","5nSecond","2019-10-14 13:20:00")

def myHandlebar(ContextInfo):
    global c
    now = time.strftime('%H%M%S')
    if c ==0 and '092500' >= now >= '091500':
        c += 1
        passorder(23,1101,account,s,11,14.00,100,2,ContextInfo) # 立即下单

def handlebar(ContextInfo):
    return
```

### 3. 止盈止损示例

```python
#coding:gbk
# 1.账户内所有股票，当股价低于买入价10%止损卖出
# 2.账户内所有股票，当股价高于前一天的收盘价10%时，开始监控一旦股价炸板（开板），以买三价卖出

def init(C):
    C.ratio = 1
    if accountType == 'STOCK':
        C.sell_code = 24
    if accountType == 'CREDIT':
        C.sell_code = 34
    C.spare_list = C.get_stock_list_in_sector('不卖品种')

def handlebar(C):
    if not C.is_last_bar():
        return
    holdings = get_trade_detail_data(account, accountType, 'position')
    stock_list = [holding.m_strInstrumentID + '.' + holding.m_strExchangeID for holding in holdings]
    if stock_list:
        full_tick = C.get_full_tick(stock_list)
        for holding in holdings:
            stock = holding.m_strInstrumentID + '.' + holding.m_strExchangeID
            rate = holding.m_dProfitRate
            volume = holding.m_nCanUseVolume
            if not volume >= 100:
                continue
            if stock in C.spare_list:
                continue
            if rate < -0.1:
                msg = f'{stock} 盈亏比例 {rate} 小于-10% 卖出 {volume}股'
                print(msg)
                passorder(C.sell_code, 1101, account, stock, 14, -1, volume, '减仓模型', 2, msg, C)
                continue
            if stock in full_tick:
                current_price = full_tick[stock]['lastPrice']
                pre_price = full_tick[stock]['lastClose']
                high_price = full_tick[stock]['high']
                stop_price = pre_price * 1.2 if stock[:2] in ['30', '68'] else pre_price * 1.1
                stop_price = round(stop_price, 2)
                ask_price_3 = full_tick[stock]['bidPrice'][2]
                if not ask_price_3:
                    print(f"{stock} {full_tick[stock]} 未取到三档盘口价")
                    continue
                if high_price == stop_price and current_price < stop_price:
                    msg = f"{stock} 涨停后 开板 卖出 {volume}股"
                    print(msg)
                    passorder(C.sell_code, 1101, account, stock, 14, -1, volume, '减仓模型', 2, msg, C)
```

### 4. 获取委托持仓及资金数据

```python
#coding:gbk
def query_info(C):
    # 获取委托
    orders = get_trade_detail_data('8000000213', 'stock', 'order')
    for o in orders:
        print(f'股票代码: {o.m_strInstrumentID}, 市场类型: {o.m_strExchangeID}, 证券名称: {o.m_strInstrumentName}, 买卖方向: {o.m_nOffsetFlag}',
        f'委托数量: {o.m_nVolumeTotalOriginal}, 成交均价: {o.m_dTradedPrice}, 成交数量: {o.m_nVolumeTraded}, 成交金额:{o.m_dTradeAmount}')

    # 获取成交
    deals = get_trade_detail_data('8000000213', 'stock', 'deal')
    for dt in deals:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 买卖方向: {dt.m_nOffsetFlag}', 
        f'成交价格: {dt.m_dPrice}, 成交数量: {dt.m_dVolume}, 成交金额: {dt.m_dTradeAmount}')

    # 获取持仓
    positions = get_trade_detail_data('8000000213', 'stock', 'position')
    for dt in positions:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 持仓量: {dt.m_nVolume}, 可用数量: {dt.m_nCanUseVolume}',
        f'成本价: {dt.m_dOpenPrice:.2f}, 市值: {dt.m_dInstrumentValue:.2f}, 持仓成本: {dt.m_dPositionCost:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')

    # 获取资金
    accounts = get_trade_detail_data('8000000213', 'stock', 'account')
    for dt in accounts:
        print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
        f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')

    return orders, deals, positions, accounts
```

### 5. 调整至目标持仓

```python
#coding:gbk
# 调仓到指定篮子
import time
from datetime import datetime

def f(C):
    now = datetime.now()
    now_timestr = now.strftime("%H%M%S")
    
    # 获取持仓
    position_list = get_trade_detail_data(account, accountType, 'position')
    position_dict = {i.m_strInstrumentID + '.' + i.m_strExchangeID : int(i.m_nVolume) for i in position_list}
    
    # 目标持仓
    final_dict = {"600000.SH" :10000, '000001.SZ' : 20000}
    
    # 获取全推行情
    stock_list = list(position_dict.keys())
    full_tick = C.get_full_tick(stock_list)
    
    for stock in position_dict:
        target_vol = final_dict[stock] if stock in final_dict else 0
        
        # 持仓大于目标持仓 卖出
        if position_dict[stock] > target_vol:
            vol = int((position_dict[stock] - target_vol)/100)*100
            buy_one_price = full_tick[stock]['bidPrice'][0]
            if buy_one_price > 0:
                msg = f"{now.strftime('%Y%m%d%H%M%S')}_{stock}_sell_{vol}股"
                passorder(24,1101,account,stock,14,-1,vol,'调仓策略',2,msg,C)
        
        # 持仓小于目标持仓 买入
        if position_dict[stock] < target_vol:
            vol = int((target_vol-position_dict[stock])/100)*100
            sell_one_price = full_tick[stock]['askPrice'][0]
            if sell_one_price > 0:
                msg = f"{now.strftime('%Y%m%d%H%M%S')}_{stock}_buy_{vol}股"
                passorder(23,1101,account,stock,14,-1,vol,'调仓策略',2,msg,C)
```

---

## ⚠️ 重要说明

### 回测环境 vs 实盘环境

1. **回测环境**:
   - QMT回测环境可能不支持 `passorder` 函数
   - 需要使用手动模拟的 `order_shares` 函数
   - 通过 `ContextInfo.holdings` 和 `ContextInfo.money` 手动更新持仓

2. **实盘环境**:
   - 必须使用 `passorder` 函数进行下单
   - `passorder` 是QMT的标准下单函数
   - 支持投资备注、快速交易参数等高级功能

### 当前策略代码

当前 `TRQuant_Weekly_Factor_V4.py` 使用 `order_shares` 函数（手动模拟），适用于回测环境。

如果需要支持实盘交易，可以：
1. 添加 `passorder` 支持（如果可用）
2. 根据环境自动选择：回测用 `order_shares`，实盘用 `passorder`

---

## 📖 相关文档

- QMT官方文档: `https://qmt.ptradeapi.com/`
- 知识库条目: 已添加5条QMT passorder示例
- 策略文件: `strategies/qmt/TRQuant_Weekly_Factor_V4.py`
