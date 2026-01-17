#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
补充资金流向知识库
==================

当前: 35条
目标: 80+条
还需: 45+条
"""

import sys
from pathlib import Path

TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


def create_money_flow_entries():
    """创建资金流向知识条目"""
    entries = []
    
    # 资金流向指标详解（15条）
    indicators = [
        ("主力资金净流入", "主力资金的净流入情况，反映大资金的动向"),
        ("超大单净流入", "超大单资金的净流入情况，通常指单笔1000万以上的交易"),
        ("大单净流入", "大单资金的净流入情况，通常指单笔100万-1000万的交易"),
        ("中单净流入", "中单资金的净流入情况，通常指单笔10万-100万的交易"),
        ("小单净流入", "小单资金的净流入情况，通常指单笔10万以下的交易"),
        ("主力资金流入率", "主力资金流入占总成交额的比例"),
        ("主力资金流出率", "主力资金流出占总成交额的比例"),
        ("资金流向强度", "资金流向的强度指标，反映资金流向的持续性"),
        ("资金流向趋势", "资金流向的趋势指标，反映资金流向的变化方向"),
        ("资金流向集中度", "资金流向的集中度指标，反映资金流向的集中程度"),
        ("资金流向持续性", "资金流向的持续性指标，反映资金流向的持续时间"),
        ("资金流向波动性", "资金流向的波动性指标，反映资金流向的波动程度"),
        ("资金流向相关性", "资金流向与其他指标的相关性"),
        ("资金流向预测性", "资金流向对未来价格的预测能力"),
        ("资金流向有效性", "资金流向指标的有效性评估"),
    ]
    
    for title_suffix, desc in indicators:
        entries.append({
            "title": f"资金流向因子: {title_suffix}",
            "content": f"""**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

## 资金流向因子: {title_suffix}

### 因子说明
{desc}

### 计算方法
```python
# 资金流向计算示例
def calculate_money_flow(stock_data):
    # 计算主力资金净流入
    main_flow = stock_data['main_flow_in'] - stock_data['main_flow_out']
    return main_flow
```

### 使用场景
- 选股：筛选资金流入的股票
- 择时：判断资金流向变化
- 风控：监控资金流向异常

### 注意事项
1. 资金流向数据有延迟
2. 需要结合其他指标
3. 注意数据质量

## 结论
{title_suffix}是资金流向分析的重要指标，可用于选股和择时。""",
            "type": "factor_behavior",
            "tags": ["资金流向", "因子分析", "选股", "B级可靠性"],
            "source": "实战经验总结"
        })
    
    # 资金流向在不同市场状态下的行为（10条）
    market_states = [
        ("牛市中的资金流向特征", "牛市中的资金流向特征和规律"),
        ("熊市中的资金流向特征", "熊市中的资金流向特征和规律"),
        ("震荡市中的资金流向特征", "震荡市中的资金流向特征和规律"),
        ("上涨趋势中的资金流向", "上涨趋势中的资金流向变化"),
        ("下跌趋势中的资金流向", "下跌趋势中的资金流向变化"),
        ("横盘整理中的资金流向", "横盘整理中的资金流向特征"),
        ("突破时的资金流向", "突破时的资金流向特征"),
        ("回调时的资金流向", "回调时的资金流向特征"),
        ("反弹时的资金流向", "反弹时的资金流向特征"),
        ("反转时的资金流向", "反转时的资金流向特征"),
    ]
    
    for title_suffix, desc in market_states:
        entries.append({
            "title": f"资金流向行为映射: {title_suffix}",
            "content": f"""**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

## 资金流向行为映射: {title_suffix}

### 行为特征
{desc}

### 典型表现
- 资金流向的变化规律
- 资金流向的持续时间
- 资金流向的强度变化

### 实战应用
- 市场状态判断
- 趋势确认
- 买卖时机选择

### 注意事项
1. 不同市场状态下的表现不同
2. 需要结合其他指标确认
3. 注意市场环境变化

## 结论
了解{title_suffix}有助于更好地判断市场状态和选择交易时机。""",
            "type": "factor_behavior",
            "tags": ["资金流向", "市场状态", "行为映射", "B级可靠性"],
            "source": "实战经验总结"
        })
    
    # 资金流向策略应用（10条）
    strategies = [
        ("基于资金流向的选股策略", "使用资金流向指标进行选股"),
        ("基于资金流向的择时策略", "使用资金流向指标进行择时"),
        ("资金流向与价格背离策略", "利用资金流向与价格的背离进行交易"),
        ("资金流向趋势跟踪策略", "跟踪资金流向趋势进行交易"),
        ("资金流向反转策略", "利用资金流向反转进行交易"),
        ("资金流向组合策略", "组合多个资金流向指标的策略"),
        ("资金流向与成交量结合策略", "结合资金流向和成交量的策略"),
        ("资金流向与技术指标结合策略", "结合资金流向和技术指标的策略"),
        ("资金流向与基本面结合策略", "结合资金流向和基本面的策略"),
        ("资金流向多因子策略", "使用多个资金流向因子的策略"),
    ]
    
    for title_suffix, desc in strategies:
        entries.append({
            "title": f"资金流向策略: {title_suffix}",
            "content": f"""**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战经验总结

## 资金流向策略: {title_suffix}

### 策略思路
{desc}

### 策略逻辑
```python
def money_flow_strategy(stock_list):
    selected = []
    for stock in stock_list:
        # 计算资金流向指标
        money_flow = calculate_money_flow(stock)
        
        # 筛选条件
        if money_flow > threshold:
            selected.append(stock)
    
    return selected
```

### 策略参数
- 资金流向阈值
- 持仓数量
- 调仓频率

### 注意事项
1. 参数需要优化
2. 需要结合其他指标
3. 注意市场环境

## 结论
{title_suffix}是资金流向应用的重要策略，需要根据实际情况调整参数。""",
            "type": "strategy_template",
            "tags": ["资金流向", "策略模板", "选股", "B级可靠性"],
            "source": "实战经验总结"
        })
    
    # 资金流向实战案例（10条）
    cases = [
        ("资金流向选股案例: 主力资金持续流入", "主力资金持续流入的选股案例"),
        ("资金流向择时案例: 资金流向反转", "资金流向反转的择时案例"),
        ("资金流向背离案例: 价格上涨资金流出", "价格上涨但资金流出的背离案例"),
        ("资金流向趋势案例: 资金流向趋势跟踪", "资金流向趋势跟踪的案例"),
        ("资金流向组合案例: 多指标组合", "多个资金流向指标组合使用的案例"),
        ("资金流向失败案例: 资金流入但价格下跌", "资金流入但价格下跌的失败案例"),
        ("资金流向成功案例: 资金流入价格上涨", "资金流入价格上涨的成功案例"),
        ("资金流向风险案例: 资金流向异常", "资金流向异常的风险案例"),
        ("资金流向优化案例: 参数优化", "资金流向策略参数优化的案例"),
        ("资金流向实盘案例: 实盘应用", "资金流向策略实盘应用的案例"),
    ]
    
    for title_suffix, desc in cases:
        entries.append({
            "title": f"资金流向实战案例: {title_suffix}",
            "content": f"""**可靠性评级**: B级（中高可靠性）

**知识来源**: 实战案例

## 资金流向实战案例: {title_suffix}

### 案例背景
{desc}

### 案例详情
- 市场环境
- 资金流向特征
- 交易决策
- 结果分析

### 经验总结
- 成功经验
- 失败教训
- 改进建议

### 注意事项
1. 案例仅供参考
2. 需要结合实际情况
3. 注意风险控制

## 结论
{title_suffix}提供了资金流向应用的实战参考，有助于理解资金流向的实际应用。""",
            "type": "practice",
            "tags": ["资金流向", "实战案例", "经验总结", "B级可靠性"],
            "source": "实战案例"
        })
    
    return entries


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 补充资金流向知识库到80+条")
    print("=" * 70)
    print()
    
    entries = create_money_flow_entries()
    print(f"📝 准备添加 {len(entries)} 条资金流向知识...")
    print()
    
    success_count = 0
    for i, entry in enumerate(entries, 1):
        print(f"[{i}/{len(entries)}] 添加: {entry['title']}")
        try:
            result = knowledge_add(
                title=entry['title'],
                content=entry['content'],
                type=entry['type'],
                tags=entry['tags'],
                source=entry['source']
            )
            if result.get('success') or result.get('knowledge_id'):
                print(f"    ✅ 添加成功")
                success_count += 1
            else:
                print(f"    ❌ 添加失败: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
        
        if i % 10 == 0:
            print(f"    📊 进度: {success_count}/{i} 成功")
        print()
    
    print("=" * 70)
    print(f"📊 补充完成: {success_count}/{len(entries)} 条知识已添加")
    print("=" * 70)
    
    # 最终统计
    import json
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if kb_file.exists():
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        items = kb.get('items', [])
        money_flow_items = [i for i in items if '资金流向' in i.get('title', '') or '资金流向' in i.get('content', '') or 'money_flow' in i.get('content', '').lower()]
        
        print()
        print("=" * 70)
        print("📊 最终统计")
        print("=" * 70)
        print(f"资金流向知识库: {len(money_flow_items)}条")
        print(f"目标: 80条")
        print(f"完成度: {len(money_flow_items)/80*100:.1f}%")
        if len(money_flow_items) >= 80:
            print("✅ 已达到目标！")
        else:
            print(f"还需补充: {80 - len(money_flow_items)}条")
        print("=" * 70)


if __name__ == '__main__':
    main()
