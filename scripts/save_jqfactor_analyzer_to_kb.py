#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将jqfactor-analyzer信息存入向量RAG知识库

功能：
1. 整理jqfactor-analyzer的完整信息
2. 使用MCP工具存入知识库
3. 构建向量索引
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from datetime import datetime
from typing import List, Dict, Any

# 导入MCP工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    from mcp_servers.knowledge_vector_index import build_vector_index
    KB_AVAILABLE = True
except ImportError:
    print("⚠️ 知识库工具不可用")
    KB_AVAILABLE = False


def create_jqfactor_analyzer_kb_items() -> List[Dict[str, Any]]:
    """创建jqfactor-analyzer知识库条目"""
    
    kb_items = []
    
    # 条目1: 概述
    kb_items.append({
        'title': 'jqfactor-analyzer 聚宽因子分析器概述',
        'content': '''
jqfactor-analyzer 是聚宽（JoinQuant）提供的因子分析工具库，用于量化投资中的因子构建、分析和评估。

**基本信息**:
- 包名: jqfactor-analyzer
- 版本: 1.1.0
- 来源: PyPI (https://pypi.org/project/jqfactor-analyzer/)
- 安装: pip install jqfactor-analyzer

**主要功能**:
1. 因子构建和计算
2. 因子有效性分析
3. 因子相关性分析
4. 因子IC分析（信息系数）
5. 因子收益分析
6. 因子可视化

**依赖库**:
- jqdatasdk: 聚宽数据SDK
- pandas: 数据处理
- numpy: 数值计算
- scipy: 科学计算
- statsmodels: 统计模型
- matplotlib: 数据可视化
- seaborn: 统计可视化

**适用场景**:
- 量化因子研究
- 因子有效性验证
- 因子组合优化
- 多因子模型构建
        ''',
        'type': 'api_reference',
        'tags': ['聚宽', '因子分析', '量化投资', 'jqfactor-analyzer', '因子工程'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    # 条目2: 安装和使用
    kb_items.append({
        'title': 'jqfactor-analyzer 安装和使用方法',
        'content': '''
**安装方法**:
```bash
# 在虚拟环境中安装
pip install jqfactor-analyzer

# 或指定版本
pip install jqfactor-analyzer==1.1.0
```

**基本使用流程**:
1. 导入库
```python
import jqdatasdk as jq
from jqfactor_analyzer import FactorAnalyzer
```

2. 连接聚宽数据
```python
jq.auth('username', 'password')
```

3. 获取因子数据
```python
# 使用聚宽现成因子
factors = jq.get_factor_values(
    securities=['000001.XSHE', '000002.XSHE'],
    factors=['size', 'beta', 'momentum'],
    count=1,
    end_date='2025-01-01'
)
```

4. 因子分析
```python
# 使用jqfactor-analyzer进行因子分析
analyzer = FactorAnalyzer(factor_data)
results = analyzer.analyze()
```

**与聚宽其他工具的集成**:
- 与jqdatasdk配合使用获取数据
- 与聚宽回测引擎配合验证因子有效性
- 与聚宽因子库结合使用
        ''',
        'type': 'tutorial',
        'tags': ['聚宽', '因子分析', '安装', '使用方法', 'jqfactor-analyzer'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    # 条目3: 因子类型
    kb_items.append({
        'title': '聚宽因子类型和CNE风格因子',
        'content': '''
**聚宽提供的现成因子类型**:

1. **CNE5风格因子** (5个):
   - size: 市值因子
   - beta: 贝塔因子（市场风险）
   - momentum: 动量因子
   - reversal: 反转因子
   - volatility: 波动率因子

2. **CNE6风格因子Pro** (7个):
   - 包含CNE5的所有因子
   - growth: 成长因子
   - earnings_yield: 盈利收益率因子

**获取方法**:
```python
import jqdatasdk as jq

# 获取CNE5因子
cne5_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility']
values = jq.get_factor_values(
    securities=stocks,
    factors=cne5_factors,
    count=1,
    end_date=date
)

# 获取CNE6因子
cne6_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility', 'growth', 'earnings_yield']
values = jq.get_factor_values(
    securities=stocks,
    factors=cne6_factors,
    count=1,
    end_date=date
)
```

**因子标准化**:
```python
# 因子值通常需要标准化
normalized = (values - values.mean()) / values.std()
```

**因子组合**:
```python
# 多因子组合（等权）
combined = normalized.mean(axis=1)

# 多因子组合（加权）
weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # CNE5等权
combined = (normalized * weights).sum(axis=1)
```
        ''',
        'type': 'api_reference',
        'tags': ['聚宽', '因子', 'CNE5', 'CNE6', '风格因子', '因子组合'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    # 条目4: 因子分析功能
    kb_items.append({
        'title': 'jqfactor-analyzer 因子分析功能',
        'content': '''
**jqfactor-analyzer 提供的分析功能**:

1. **因子IC分析** (Information Coefficient):
   - 计算因子值与未来收益的相关性
   - IC均值、IC标准差
   - IC胜率（IC>0的比例）
   - IC衰减分析

2. **因子收益分析**:
   - 因子分组收益（按因子值分组）
   - 多空收益（做多高因子值，做空低因子值）
   - 因子收益稳定性

3. **因子相关性分析**:
   - 因子间相关性矩阵
   - 因子冗余度分析
   - 因子正交化

4. **因子有效性评估**:
   - 因子信息比率（IR）
   - 因子夏普比率
   - 因子最大回撤

**使用示例**:
```python
from jqfactor_analyzer import FactorAnalyzer

# 创建分析器
analyzer = FactorAnalyzer(
    factor_data=factor_values,
    price_data=price_data,
    groupby='date'
)

# IC分析
ic_result = analyzer.ic_analysis()

# 收益分析
return_result = analyzer.return_analysis()

# 相关性分析
corr_result = analyzer.correlation_analysis()
```

**输出结果**:
- 统计报告
- 可视化图表
- 因子排名
        ''',
        'type': 'api_reference',
        'tags': ['因子分析', 'IC分析', '因子收益', '因子评估', 'jqfactor-analyzer'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    # 条目5: 最佳实践
    kb_items.append({
        'title': 'jqfactor-analyzer 使用最佳实践',
        'content': '''
**因子构建最佳实践**:

1. **数据准备**:
   - 确保数据完整性（处理缺失值）
   - 数据标准化（Z-score或分位数标准化）
   - 异常值处理（Winsorize）

2. **因子选择**:
   - 优先使用聚宽现成因子（CNE5/CNE6）
   - 结合技术指标（ta-lib）
   - 添加自定义因子（基于业务逻辑）

3. **因子分析流程**:
   ```
   数据获取 → 因子计算 → IC分析 → 收益分析 → 因子选择 → 因子组合
   ```

4. **因子有效性标准**:
   - IC均值 > 0.05（显著）
   - IC胜率 > 0.55（稳定）
   - 多空收益 > 0（有效）
   - 信息比率 > 0.5（优秀）

5. **因子组合策略**:
   - 等权组合（简单有效）
   - 基于IC加权（动态调整）
   - 基于收益加权（历史表现）
   - 因子正交化（降低冗余）

**注意事项**:
- 避免过拟合（使用滚动窗口验证）
- 注意因子衰减（定期重新评估）
- 考虑交易成本（实际收益会降低）
- 市场环境适应性（不同市场状态表现不同）
        ''',
        'type': 'practice',
        'tags': ['最佳实践', '因子工程', '因子分析', '量化投资', 'jqfactor-analyzer'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    # 条目6: 与项目集成
    kb_items.append({
        'title': 'jqfactor-analyzer 在TRQuant项目中的集成',
        'content': '''
**项目中的使用位置**:

1. **策略文件**: `strategies/tenbagger_comprehensive_strategy.py`
   - 使用 `jq.get_factor_values()` 获取CNE5/CNE6因子
   - 因子标准化和组合
   - 因子评分计算

2. **因子计算模块**: `core/advisor_v4/multi_factor_calculator.py`
   - 可以集成jqfactor-analyzer进行因子分析
   - 因子有效性验证

3. **回测验证**: 使用因子进行选股和回测

**集成建议**:

1. **创建因子分析模块**:
```python
# core/factors/jqfactor_analyzer_wrapper.py
from jqfactor_analyzer import FactorAnalyzer
import jqdatasdk as jq

class JQFactorAnalyzerWrapper:
    """jqfactor-analyzer包装器"""
    
    def analyze_factor(self, factor_name, stocks, start_date, end_date):
        # 获取因子数据
        factor_data = jq.get_factor_values(...)
        
        # 使用jqfactor-analyzer分析
        analyzer = FactorAnalyzer(factor_data)
        results = analyzer.ic_analysis()
        
        return results
```

2. **在V4.0系统中使用**:
   - 替换当前的手工因子计算
   - 使用现成的CNE5/CNE6因子
   - 利用jqfactor-analyzer进行因子评估

3. **优势**:
   - 减少开发时间
   - 提高因子质量
   - 标准化因子分析流程
        ''',
        'type': 'integration',
        'tags': ['TRQuant', '项目集成', '因子分析', 'jqfactor-analyzer', '开发指南'],
        'source': 'https://pypi.org/project/jqfactor-analyzer/'
    })
    
    return kb_items


def add_to_knowledge_base(kb_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """将知识库条目添加到RAG知识库"""
    if not KB_AVAILABLE:
        return {
            'success': False,
            'error': 'MCP工具不可用',
            'items': kb_items
        }
    
    results = {
        'success': 0,
        'failed': 0,
        'errors': [],
        'knowledge_ids': []
    }
    
    print(f"\n📚 准备存入 {len(kb_items)} 个知识库条目...")
    print("=" * 70)
    
    for i, item in enumerate(kb_items, 1):
        print(f"\n[{i}/{len(kb_items)}] {item['title']}")
        
        try:
            result = knowledge_add(
                title=item['title'],
                content=item['content'],
                type=item['type'],
                tags=item['tags'],
                source=item.get('source', '')
            )
            
            if result.get('success') or result.get('knowledge_id'):
                results['success'] += 1
                kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
                results['knowledge_ids'].append(kb_id)
                print(f"  ✅ 成功存入 (ID: {kb_id})")
            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unknown error')
                results['errors'].append(f"{item['title']}: {error_msg}")
                print(f"  ❌ 失败: {error_msg}")
                
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{item['title']}: {str(e)}")
            print(f"  ❌ 异常: {str(e)}")
    
    print("\n" + "=" * 70)
    print("📊 存入结果")
    print("=" * 70)
    print(f"成功: {results['success']} 个")
    print(f"失败: {results['failed']} 个")
    print(f"总计: {len(kb_items)} 个")
    
    return results


def build_kb_vector_index() -> Dict[str, Any]:
    """构建知识库向量索引"""
    if not KB_AVAILABLE:
        return {'success': False, 'error': 'MCP工具不可用'}
    
    try:
        from pathlib import Path
        DATA_DIR = Path(__file__).parent.parent / 'data'
        KNOWLEDGE_DIR = DATA_DIR / "knowledge"
        kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
        
        if not kb_file.exists():
            return {'success': False, 'error': '知识库文件不存在'}
        
        print("\n🔍 构建向量索引...")
        result = build_vector_index(kb_file, force_rebuild=False)
        
        if result.get('success'):
            print(f"  ✅ 向量索引构建成功")
            print(f"  索引文件: {result.get('index_path', 'unknown')}")
        else:
            print(f"  ⚠️ 向量索引构建: {result.get('message', 'unknown')}")
        
        return result
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    """主函数"""
    print("=" * 70)
    print("jqfactor-analyzer 知识库存储")
    print("=" * 70)
    
    # 1. 创建知识库条目
    print("\n[步骤1] 创建知识库条目...")
    kb_items = create_jqfactor_analyzer_kb_items()
    print(f"  ✅ 创建了 {len(kb_items)} 个条目")
    
    # 2. 存入知识库
    print("\n[步骤2] 存入知识库...")
    results = add_to_knowledge_base(kb_items)
    
    # 3. 构建向量索引
    if results.get('success', 0) > 0:
        print("\n[步骤3] 构建向量索引...")
        index_result = build_kb_vector_index()
    
    # 4. 保存JSON备份
    output_file = Path(__file__).parent.parent / 'docs' / 'knowledge_base' / 'jqfactor_analyzer_kb.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'name': 'jqfactor-analyzer知识库',
                'source': 'https://pypi.org/project/jqfactor-analyzer/',
                'created_at': datetime.now().isoformat(),
                'total_items': len(kb_items)
            },
            'items': kb_items
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 JSON备份已保存: {output_file}")
    
    print("\n" + "=" * 70)
    print("✅ 完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
