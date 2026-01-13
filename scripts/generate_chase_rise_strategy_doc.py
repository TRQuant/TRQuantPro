#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成追涨策略文档

Phase 3.2: 最优策略文档化
- 生成策略详细文档
- 包含最优参数、信号规则、风控规则、回测结果分析
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.evaluate_chase_rise_strategy import load_best_params

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def generate_strategy_doc(best_params: dict, evaluation_results: dict = None) -> str:
    """
    生成策略文档
    
    Args:
        best_params: 最优参数
        evaluation_results: 评估结果（可选）
    
    Returns:
        str: 文档内容
    """
    doc = f"""# 追涨策略最优参数配置文档

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **策略版本**: V1.0  
> **策略类型**: 追涨模式（涨停板信号、强势突破、量价齐升）

---

## 一、策略概述

### 1.1 策略定位

**追涨策略**专注于捕捉市场强势股票的启动信号，在牛市或强势市场中追求高收益。

**核心特点**:
- 聚焦涨停板信号和强势突破
- 周频调仓（每5个交易日）
- 最大持仓2只股票（集中持有）
- 快速止损止盈（-10%止损，+25%止盈）

### 1.2 适用市场环境

- **最佳**: 牛市或强势上涨市场
- **良好**: 震荡偏强市场
- **不适用**: 熊市或持续下跌市场

---

## 二、信号体系

### 2.1 信号类型

| 信号类型 | 条件 | 基础评分 | 加分项 |
|---------|------|---------|--------|
| **首板启动** | 首次涨停 | 75 | 量比>3倍+15分 |
| **连板加速** | 2+连板 | 65 | - |
| **强势突破** | 5日动量>15%+量比>1.5 | 60 | - |
| **量价齐升** | 5日动量>10%+量比>2 | 55 | - |

### 2.2 信号参数（最优配置）

```python
# 信号参数
LIMIT_UP_THRESHOLD = {best_params.get('limit_up_threshold', 0.095):.3f}  # 涨停阈值
VOL_RATIO_THRESHOLD_FIRST = {best_params.get('vol_ratio_threshold_first', 3.0):.1f}  # 首板放量阈值
MOM_5D_THRESHOLD_BREAKOUT = {best_params.get('mom_5d_threshold_breakout', 15.0):.1f}  # 强势突破动量
MOM_5D_THRESHOLD_VOLUME = {best_params.get('mom_5d_threshold_volume', 10.0):.1f}  # 量价齐升动量
VOL_RATIO_THRESHOLD_BREAKOUT = {best_params.get('vol_ratio_threshold_breakout', 1.5):.1f}  # 强势突破量比
VOL_RATIO_THRESHOLD_VOLUME = {best_params.get('vol_ratio_threshold_volume', 2.0):.1f}  # 量价齐升量比
MIN_SIGNAL_SCORE = {best_params.get('min_signal_score', 55.0):.1f}  # 最低信号分数
```

---

## 三、交易参数（最优配置）

```python
# 交易参数
MAX_POSITIONS = {best_params.get('max_positions', 2)}  # 最大持仓数
STOP_LOSS_PCT = {best_params.get('stop_loss_pct', -10.0):.1f}  # 止损比例
TAKE_PROFIT_PCT = {best_params.get('take_profit_pct', 25.0):.1f}  # 止盈比例
REBALANCE_DAYS = {best_params.get('rebalance_days', 5)}  # 调仓周期（交易日）
WARMUP_BARS = {best_params.get('warmup_bars', 22)}  # 预热期（交易日）
```

### 3.1 参数说明

**MAX_POSITIONS = {best_params.get('max_positions', 2)}**:
- 集中持有，追求单票高收益
- 适合小资金（<100万）
- 大资金可调整为3-5只

**STOP_LOSS_PCT = {best_params.get('stop_loss_pct', -10.0):.1f}%**:
- 快速止损，避免深度亏损
- 追涨策略需要严格止损

**TAKE_PROFIT_PCT = {best_params.get('take_profit_pct', 25.0):.1f}%**:
- 及时止盈，锁定收益
- 避免回吐

**REBALANCE_DAYS = {best_params.get('rebalance_days', 5)}**:
- 周频调仓，捕捉短期机会
- 平衡收益和交易成本

---

## 四、风控规则

### 4.1 止损规则

- **绝对止损**: 亏损超过 `{best_params.get('stop_loss_pct', -10.0):.1f}%` 立即卖出
- **执行方式**: 每个交易日检查，触发即执行
- **目的**: 快速止损，避免深度亏损

### 4.2 止盈规则

- **固定止盈**: 盈利达到 `{best_params.get('take_profit_pct', 25.0):.1f}%` 立即卖出
- **执行方式**: 每个交易日检查，触发即执行
- **目的**: 及时锁定收益，避免回吐

### 4.3 仓位管理

- **最大持仓**: `{best_params.get('max_positions', 2)}` 只股票
- **仓位分配**: 等权重分配（每只股票 `{100.0 / best_params.get('max_positions', 2):.1f}%`）
- **现金保留**: 建议保留5-10%现金

---

## 五、回测结果分析

"""

    if evaluation_results:
        doc += f"""
### 5.1 数据集划分

- **训练集**: 2019-01-01~2020-06-30 + 2024-09-01~2025-06-30 (70%)
- **验证集**: 2020-07-01~2021-03-31 (15%)
- **测试集**: 2025-07-01~2026-01-10 (15%)

### 5.2 结果对比

| 指标 | 训练集 | 验证集 | 测试集 |
|------|--------|--------|--------|
| 周平均收益率 | {evaluation_results.get('train', {}).get('weekly_return', 0):.2f}% | {evaluation_results.get('validate', {}).get('weekly_return', 0):.2f}% | {evaluation_results.get('test', {}).get('weekly_return', 0):.2f}% |
| 夏普比率 | {evaluation_results.get('train', {}).get('sharpe_ratio', 0):.2f} | {evaluation_results.get('validate', {}).get('sharpe_ratio', 0):.2f} | {evaluation_results.get('test', {}).get('sharpe_ratio', 0):.2f} |
| 最大回撤 | {evaluation_results.get('train', {}).get('max_drawdown', 0):.2f}% | {evaluation_results.get('validate', {}).get('max_drawdown', 0):.2f}% | {evaluation_results.get('test', {}).get('max_drawdown', 0):.2f}% |
| 胜率 | {evaluation_results.get('train', {}).get('win_rate', 0):.2f}% | {evaluation_results.get('validate', {}).get('win_rate', 0):.2f}% | {evaluation_results.get('test', {}).get('win_rate', 0):.2f}% |

### 5.3 分析结论

"""
        
        analysis = evaluation_results.get('analysis', {})
        if analysis.get('is_overfitting', False):
            doc += "- ⚠️ **策略存在过拟合风险**，建议调整参数或增加正则化。\n"
        elif analysis.get('is_stable', False):
            doc += "- ✅ **策略表现稳定**，可以在测试集上进一步验证。\n"
        else:
            doc += "- ⚠️ **策略稳定性需要进一步观察**。\n"
        
        if 'overfit_ratio_train_validate' in analysis:
            doc += f"- 训练集/验证集夏普比率比: {analysis['overfit_ratio_train_validate']:.2f}\n"
        if 'returns_std' in analysis:
            doc += f"- 收益率标准差: {analysis['returns_std']:.2f}%\n"
    
    doc += """
---

## 六、使用建议

### 6.1 适用场景

- **最佳**: 牛市或强势上涨市场
- **良好**: 震荡偏强市场
- **不适用**: 熊市或持续下跌市场

### 6.2 资金要求

- **最小资金**: 10万元（单票5万）
- **推荐资金**: 50-200万元
- **最大资金**: 500万元（建议分散到多个策略）

### 6.3 风险提示

- ⚠️ 追涨策略风险较高，需要严格止损
- ⚠️ 适合风险承受能力较强的投资者
- ⚠️ 建议在牛市或强势市场使用
- ⚠️ 熊市或震荡市建议暂停或降低仓位

---

## 七、代码使用

### 7.1 QMT回测代码

文件: `strategies/qmt/TRQuant_ChaseRise_V1_*.py`

**使用步骤**:
1. 打开QMT桌面App
2. 进入策略研究环境
3. 导入策略文件
4. 设置回测参数（起始日期、结束日期、初始资金）
5. 运行回测

### 7.2 QMT实盘代码

文件: `strategies/qmt/TRQuant_ChaseRise_V1_Live_*.py`

**使用步骤**:
1. 确认账户配置（accountID）
2. 确认参数配置（与回测代码一致）
3. 小资金测试（建议10-20万）
4. 监控运行状态
5. 根据表现调整仓位

---

## 八、参数调整建议

### 8.1 市场环境调整

**牛市**:
- 可以提高 `MAX_POSITIONS` 至 3-5只
- 可以提高 `TAKE_PROFIT_PCT` 至 30-35%
- 可以降低 `STOP_LOSS_PCT` 至 -8%

**震荡市**:
- 保持当前参数
- 注意市场状态切换

**熊市**:
- 建议暂停策略
- 或大幅降低仓位（只持有1只股票）

### 8.2 资金规模调整

**小资金 (<100万)**:
- 保持 `MAX_POSITIONS = 2`
- 保持当前参数

**中等资金 (100-500万)**:
- 可以调整 `MAX_POSITIONS = 3-4`
- 保持其他参数

**大资金 (>500万)**:
- 建议分散到多个策略
- 或增加 `MAX_POSITIONS` 至 5-10只

---

## 九、常见问题

### 9.1 为什么选不出股票？

可能原因:
- 市场环境不匹配（熊市或震荡市）
- 信号参数过严（建议适当放宽）
- 股票池过小（建议使用全A股）

解决方案:
- 检查市场状态
- 适当放宽信号参数
- 扩大股票池范围

### 9.2 为什么收益不理想？

可能原因:
- 市场环境不匹配
- 止损止盈参数不合理
- 调仓频率不合适

解决方案:
- 确认市场环境
- 根据市场状态调整参数
- 优化调仓频率

---

## 十、联系方式

如有问题，请参考项目文档或联系开发团队。

---

**文档版本**: V1.0  
**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**维护者**: TRQuant Team
"""
    
    return doc


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("生成追涨策略文档")
    logger.info("=" * 70)
    
    # 加载最优参数
    best_params = load_best_params()
    if not best_params:
        logger.warning("未找到最优参数，使用默认参数")
        best_params = {
            'limit_up_threshold': 0.095,
            'vol_ratio_threshold_first': 3.0,
            'mom_5d_threshold_breakout': 15.0,
            'mom_5d_threshold_volume': 10.0,
            'vol_ratio_threshold_breakout': 1.5,
            'vol_ratio_threshold_volume': 2.0,
            'min_signal_score': 55.0,
            'max_positions': 2,
            'stop_loss_pct': -10.0,
            'take_profit_pct': 25.0,
            'rebalance_days': 5,
            'warmup_bars': 22,
        }
    
    # 尝试加载评估结果
    evaluation_results = None
    try:
        eval_dir = PROJECT_ROOT / 'output' / 'chase_rise_evaluation'
        if eval_dir.exists():
            eval_files = list(eval_dir.glob('evaluation_results_*.json'))
            if eval_files:
                latest_file = max(eval_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    evaluation_results = json.load(f)
                logger.info(f"✅ 已加载评估结果: {latest_file.name}")
    except Exception as e:
        logger.warning(f"加载评估结果失败: {e}")
    
    # 生成文档
    doc_content = generate_strategy_doc(best_params, evaluation_results)
    
    # 保存文档
    output_dir = PROJECT_ROOT / 'docs' / 'research'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    doc_path = output_dir / 'CHASE_RISE_STRATEGY_OPTIMIZED.md'
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    logger.info(f"✅ 策略文档已保存: {doc_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("文档生成完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
