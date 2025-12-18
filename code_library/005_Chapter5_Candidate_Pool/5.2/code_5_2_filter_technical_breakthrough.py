"""
文件名: code_5_2_filter_technical_breakthrough.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.2/code_5_2_filter_technical_breakthrough.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: filter_technical_breakthrough

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_technical_breakthrough(
    stocks: List[str],
    date: str = None
) -> List[Dict]:
        """
    filter_technical_breakthrough函数
    
    **设计原理**：
    - **核心功能**：实现filter_technical_breakthrough的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    candidates = []
    
    for stock_code in stocks:
        try:
            # 获取价格数据（向前推120天）
            end_dt = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
            start_dt = end_dt - timedelta(days=120)
            start_date = start_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
            
            price_data = get_price_data(stock_code, start_date=start_date, end_date=end_date)
            
            if price_data.empty or len(price_data) < 20:
                continue
            
            # 计算技术指标
            latest = price_data.iloc[-1]
            prev = price_data.iloc[-2] if len(price_data) > 1 else latest
            
            # 涨跌幅
            change_pct = ((latest["close"] - prev["close"]) / prev["close"]) * 100 \
                        if prev["close"] > 0 else 0
            
            # 是否涨停（涨跌幅 >= 9.5%）
            is_limit_up = change_pct >= 9.5
            
            # 是否放量（成交量较前一日放大50%以上）
            volume_ratio = latest["volume"] / prev["volume"] if prev["volume"] > 0 else 1
            is_volume_breakout = volume_ratio >= 1.5
            
            # 是否站上均线
            data_len = len(price_data)
            if data_len >= 60:
                ma60 = price_data["close"].tail(60).mean()
                is_ma_breakthrough = latest["close"] > ma60
            elif data_len >= 30:
                ma30 = price_data["close"].tail(30).mean()
                is_ma_breakthrough = latest["close"] > ma30
            else:
                ma_avg = price_data["close"].mean()
                is_ma_breakthrough = latest["close"] > ma_avg
            
            # 连续上涨天数
            consecutive_up = 0
            for i in range(len(price_data) - 1, 0, -1):
                if price_data.iloc[i]["close"] > price_data.iloc[i - 1]["close"]:
                    consecutive_up += 1
                else:
                    break
            
            # 技术面筛选：至少满足一个条件
            if is_limit_up or is_volume_breakout or is_ma_breakthrough or consecutive_up >= 3:
                candidate = {
                    "code": stock_code,
                    "is_limit_up": is_limit_up,
                    "is_volume_breakout": is_volume_breakout,
                    "is_ma_breakthrough": is_ma_breakthrough,
                    "consecutive_up_days": consecutive_up,
                    "change_pct": round(change_pct, 2)
                }
                candidates.append(candidate)
        
        except Exception as e:
            logger.debug(f"处理股票 {stock_code} 时出错: {e}")
            continue
    
    return candidates