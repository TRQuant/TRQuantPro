# 江总投资总结知识库使用指南

> **版本**: v1.0  
> **更新**: 2026-01-15  
> **目的**: 个人投资心得体会和经验教训的知识库

---

## 📋 知识库概述

### 定位

这是**个人投资总结**知识库，用于保存江总的投资心得体会和经验教训，供策略开发、回测等步骤参考使用。

### 特点

- ✅ **个人心得**: 这是个人投资心得体会，用于参考
- ✅ **独立标识**: 使用标签 `jiangzong` 和 `personal_experience` 明确标识
- ✅ **不污染专业知识**: 与专业知识库分离，不会污染专业知识

---

## 📚 已添加的知识条目

### 1. 行业头部企业股票买卖实操方法

**类型**: `investment_experience`  
**标签**: `jiangzong`, `investment_summary`, `industry_leader`, `stock_trading`, `short_term`, `personal_experience`

**核心内容**:
- 目标股票: 市值千亿以上、营收数百亿以上的行业龙头企业
- 买入策略: 连续下跌买入法、业绩预告买入法
- 卖出策略: 快速止盈、短期持有、心理价位止盈
- 仓位控制: 单只股票不超过10%

**评论和建议**:
- 优点: 风险可控、策略清晰、仓位管理好
- 改进建议: 增加止损机制、考虑市场环境、验证基本面
- 风险提示: 业绩不及预期、市场系统性风险、流动性风险

### 2. 头部热门科技大股票打法总结及经验教训

**类型**: `investment_experience`  
**标签**: `jiangzong`, `investment_summary`, `tech_stock`, `hot_stock`, `long_term`, `personal_experience`

**核心内容**:
- 目标股票: 单价极高（超过600元/股）的头部科技股
- 买入策略: 跌破5日或10日均线、连跌2-3天后
- 持仓策略: 长期持有（5-10个交易日）、坚定信念、下跌时加仓
- 止损策略: 跌破8%必须考虑减仓

**评论和建议**:
- 优点: 长期视角、信念坚定、分批加仓
- 改进建议: 明确止损线、降低仓位、结合基本面分析
- 风险提示: 高单价风险、流动性风险、行业风险、估值风险

### 3. 2026年1月15日涨停分析

**类型**: `market_analysis`  
**标签**: `jiangzong`, `investment_summary`, `market_analysis`, `limit_up`, `2026-01-15`, `personal_experience`

**核心内容**:
- 市场概况: 55股涨停，16只连板股，封板率75%
- 焦点股: 博菲电气（8天5板）、人民网（4连板）、外服控股（3连板）、三变科技（7天4板）
- 市场特征: 连板股活跃、板块轮动、封板率较高

**评论和建议**:
- 市场分析: 市场情绪较好，但要注意风险
- 投资建议: 谨慎追高、关注板块轮动、注意风险控制

---

## 🔍 使用方法

### 搜索知识库

```bash
# 搜索江总投资总结
python scripts/kb/kb_manager.py search --query "江总投资总结"

# 搜索行业头部企业策略
python scripts/kb/kb_manager.py search --query "行业头部企业策略"

# 搜索科技股长期持有
python scripts/kb/kb_manager.py search --query "科技股长期持有"

# 搜索涨停分析
python scripts/kb/kb_manager.py search --query "涨停分析"
```

### 查看统计

```bash
python scripts/kb/kb_manager.py stats
```

### 构建向量索引

```bash
python scripts/kb/kb_manager.py build-index
```

---

## ➕ 添加新的投资总结

### 方法1: 使用脚本

```bash
python scripts/kb/add_jiangzong_direct.py
```

### 方法2: 使用命令行工具

```bash
python scripts/kb/kb_manager.py add \
  --title "标题" \
  --content "内容" \
  --type "investment_experience" \
  --tags "jiangzong,investment_summary" \
  --source "江总个人投资总结"
```

### 方法3: 直接编辑脚本

编辑 `scripts/kb/add_jiangzong_direct.py`，添加新的知识条目。

---

## 📝 内容格式规范

### 标题格式

- `[主题] - 江总投资总结`
- 例如: `行业头部企业股票买卖实操方法 - 江总投资总结`

### 内容结构

1. **策略概述** - 简要说明策略的适用场景
2. **目标股票特征** - 描述目标股票的特征
3. **买入策略** - 详细的买入时机和方法
4. **卖出策略** - 详细的卖出时机和方法
5. **评论和建议** - 包含优点、改进建议、风险提示

### 标签规范

- **必须标签**: `jiangzong`, `investment_summary`, `personal_experience`
- **可选标签**: 根据内容添加，如 `industry_leader`, `tech_stock`, `short_term`, `long_term` 等

---

## ⚠️ 注意事项

1. **个人心得**: 这是个人投资心得体会，仅供参考
2. **不污染专业知识**: 使用独立的标签和类型，不会污染专业知识库
3. **持续更新**: 可以随时添加新的投资总结和经验教训
4. **定期复盘**: 建议定期复盘，更新和完善投资策略

---

## 🔄 后续补充

当有新的投资总结时，可以：

1. **整理内容**: 按照格式整理成文档
2. **添加评论**: 给出评论和建议
3. **保存到知识库**: 使用脚本或命令行工具添加
4. **构建索引**: 更新向量索引

---

**最后更新**: 2026-01-15
