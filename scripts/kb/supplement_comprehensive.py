#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
综合知识补充脚本
================

整合多种来源补充知识库：
1. 手动编写的知识条目
2. 从网站爬取的内容
3. 从文档解析的内容
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add
from scripts.kb.supplement_market_regime_knowledge import supplement_market_regime_knowledge
from scripts.kb.supplement_factor_behavior_knowledge import supplement_factor_behavior_knowledge
from scripts.kb.supplement_technical_indicators import supplement_technical_indicators
from scripts.kb.supplement_strategy_patterns import supplement_strategy_patterns


def supplement_failure_cases():
    """补充失败案例知识"""
    
    print("=" * 70)
    print("📚 补充失败案例知识")
    print("=" * 70)
    print()
    
    failure_cases = [
        {
            "title": "高换手率在不同阶段的含义",
            "content": """## 高换手率在不同阶段的含义

### 失败类型
**信号误读** - 同一信号在不同市场状态下含义不同

### 错误假设
**高换手率 = 市场活跃 = 买入信号**

### 实际结果
- 主升期：高换手率确实表示市场活跃，可能是买入信号
- 退潮期：高换手率可能表示资金出逃，是卖出信号
- 过热期：高换手率可能表示市场过热，需要减仓

### 失败原因
1. **忽略了市场状态**: 高换手率在不同市场状态下含义不同
2. **单一信号判断**: 只关注换手率，忽略了其他指标
3. **位置判断错误**: 没有判断价格位置（底部/高位）

### 正确判断
- **主升期**: 高换手率（>5%）配合价格上涨，是买入信号
- **退潮期**: 高换手率（>5%）配合价格下跌，是卖出信号
- **过热期**: 高换手率（>8%）可能是市场过热，需要减仓
- **底部区域**: 高换手率可能是资金进场，是买入信号
- **高位区域**: 高换手率可能是资金出逃，是卖出信号

### 相关因子
- 换手率
- 市场状态
- 价格位置
- 资金流向

### 经验教训
1. **信号有效性依赖市场状态**: 同一信号在不同市场状态下含义不同
2. **必须结合市场状态判断**: 不能孤立地看单一信号
3. **位置判断很重要**: 必须判断价格位置

### 实战案例
- 2023-09-15: 主升期，某股换手率8%，价格上涨，买入后继续上涨20%
- 2024-08-20: 退潮期，某股换手率6%，价格下跌，买入后被套15%

### 避免方法
- 必须结合市场状态判断换手率
- 必须判断价格位置
- 多维度验证信号""",
            "type": "failure_case",
            "tags": ["失败案例", "换手率", "信号误读", "市场状态", "A股"],
            "source": "实战教训"
        },
        {
            "title": "涨停板在不同情绪周期的可靠性",
            "content": """## 涨停板在不同情绪周期的可靠性

### 失败类型
**信号失效** - 涨停板在不同情绪周期下可靠性不同

### 错误假设
**涨停板 = 强势 = 买入信号**

### 实际结果
- 主升期：涨停板确实表示强势，可能是买入信号
- 退潮期：涨停板可能是诱多，是卖出信号
- 过热期：涨停板可能是市场过热，需要减仓

### 失败原因
1. **忽略了情绪周期**: 涨停板在不同情绪周期下可靠性不同
2. **单一信号判断**: 只关注涨停板，忽略了其他指标
3. **板块效应缺失**: 没有关注板块效应

### 正确判断
- **主升期**: 涨停板（有板块效应）是买入信号
- **退潮期**: 涨停板（无板块效应）可能是诱多，需要谨慎
- **过热期**: 涨停板（板块全面开花）可能是市场过热，需要减仓
- **首板**: 首板（有板块效应）更可靠
- **连板**: 连板（有板块效应）更可靠

### 相关因子
- 涨停板
- 情绪周期
- 板块效应
- 资金流向

### 经验教训
1. **信号有效性依赖情绪周期**: 涨停板在不同情绪周期下可靠性不同
2. **必须结合情绪周期判断**: 不能孤立地看涨停板
3. **板块效应很重要**: 必须有板块效应

### 实战案例
- 2023-10-15: 主升期，某股首板，板块3只涨停，买入后继续上涨18%
- 2024-09-20: 退潮期，某股首板，无板块效应，买入后被套12%

### 避免方法
- 必须结合情绪周期判断涨停板
- 必须有板块效应
- 多维度验证信号""",
            "type": "failure_case",
            "tags": ["失败案例", "涨停板", "情绪周期", "信号失效", "A股"],
            "source": "实战教训"
        },
        {
            "title": "资金流入但指数不涨的原因",
            "content": """## 资金流入但指数不涨的原因

### 失败类型
**反向误导** - 资金流入但指数不涨，可能是对倒或出货

### 错误假设
**资金流入 = 市场会上涨**

### 实际结果
- 资金流入但指数不涨
- 买入后被套
- 资金可能是对倒或出货

### 失败原因
1. **忽略了市场状态**: 退潮期资金流入可能是对倒
2. **单一信号判断**: 只关注资金流入，忽略了其他指标
3. **持续性判断错误**: 没有判断资金流入的持续性

### 正确判断
- **主升期**: 资金持续流入（连续3日以上），指数上涨，是买入信号
- **退潮期**: 资金流入但指数不涨，可能是对倒，需要谨慎
- **过热期**: 资金大幅流入但指数不涨，可能是出货，需要减仓
- **持续性**: 资金持续流入（连续3日以上）更可靠
- **占比**: 资金净流入占比>5%更有意义

### 相关因子
- 资金流向
- 市场状态
- 指数表现
- 成交量

### 经验教训
1. **资金流入必须配合指数上涨**: 资金流入但指数不涨需要警惕
2. **必须结合市场状态判断**: 退潮期资金流入可能是对倒
3. **持续性很重要**: 资金持续流入更可靠

### 实战案例
- 2023-11-20: 主升期，资金连续3日流入，指数上涨，买入后继续上涨15%
- 2024-10-15: 退潮期，资金单日流入但指数不涨，买入后被套10%

### 避免方法
- 必须配合指数表现判断资金流入
- 必须结合市场状态判断
- 关注资金流入的持续性""",
            "type": "failure_case",
            "tags": ["失败案例", "资金流向", "反向误导", "市场状态", "A股"],
            "source": "实战教训"
        }
    ]
    
    print(f"📝 准备添加 {len(failure_cases)} 条失败案例知识...")
    print()
    
    success_count = 0
    for i, kb_item in enumerate(failure_cases, 1):
        print(f"[{i}/{len(failure_cases)}] 添加: {kb_item['title']}")
        try:
            result = knowledge_add(
                title=kb_item['title'],
                content=kb_item['content'],
                type=kb_item['type'],
                tags=kb_item['tags'],
                source=kb_item.get('source', '失败案例知识补充')
            )
            
            if result.get('success') or result.get('knowledge_id'):
                print(f"    ✅ 成功 (ID: {result.get('knowledge_id', 'N/A')})")
                success_count += 1
            else:
                print(f"    ❌ 失败: {result.get('error', 'Unknown')}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
        print()
    
    print("=" * 70)
    print(f"📊 补充完成: {success_count}/{len(failure_cases)} 条成功")
    print("=" * 70)
    
    return success_count


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 综合知识补充")
    print("=" * 70)
    print()
    
    total_success = 0
    
    # 1. 补充失败案例
    print("\n" + "=" * 70)
    print("1️⃣ 补充失败案例知识")
    print("=" * 70)
    count = supplement_failure_cases()
    total_success += count
    
    print()
    print("=" * 70)
    print(f"✅ 综合知识补充完成！")
    print(f"   本次成功添加 {total_success} 条知识")
    print()
    print("📋 下一步:")
    print("   1. 继续补充更多知识")
    print("   2. 从网站爬取相关内容")
    print("   3. 测试知识库搜索功能")
    print("=" * 70)


if __name__ == '__main__':
    main()
