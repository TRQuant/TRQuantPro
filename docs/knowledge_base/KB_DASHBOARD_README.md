# 知识库可视化统计仪表板

> **创建时间**: 2026-01-13  
> **用途**: 可视化展示知识库统计信息

---

## 📊 仪表板文件

### 1. HTML仪表板

**文件**: `docs/knowledge_base/kb_dashboard.html`

**特点**:
- 静态HTML页面，无需服务器
- 美观的渐变设计
- 响应式布局
- 进度条可视化

**内容**:
- 总知识条目数统计
- 知识库分类统计
- 知识类型分布
- 可靠性等级分布
- 质量指标（可靠性标注、结论部分等）

### 2. Plotly交互式图表

**文件**: `docs/knowledge_base/kb_dashboard_plotly.html`

**特点**:
- 交互式图表（可缩放、筛选）
- 多种图表类型（条形图、饼图）
- 动态数据展示

**内容**:
- 知识库分类统计（条形图）
- 知识类型分布（饼图）
- 可靠性等级分布（条形图）
- 质量指标（条形图）

---

## 🎯 使用方法

### 查看HTML仪表板

```bash
# 在浏览器中打开
open docs/knowledge_base/kb_dashboard.html
# 或
xdg-open docs/knowledge_base/kb_dashboard.html
```

### 查看Plotly图表

```bash
# 在浏览器中打开
open docs/knowledge_base/kb_dashboard_plotly.html
# 或
xdg-open docs/knowledge_base/kb_dashboard_plotly.html
```

### 重新生成仪表板

```bash
# 运行生成脚本
./venv/bin/python scripts/kb/create_kb_dashboard.py
```

---

## 📊 仪表板内容说明

### 1. 总知识条目数

显示知识库中的总知识条目数量。

### 2. 知识库分类统计

按知识库分类统计：
- 聚宽/JQData
- QMT
- BulletTrade
- 资金流向
- 情绪因子
- 策略开发最佳实践
- 回测引擎对比
- AKShare

### 3. 知识类型分布

按知识类型统计：
- `market_regime` - 市场状态识别
- `factor_behavior` - 因子行为映射
- `strategy_pattern` - 策略模板
- `failure_case` - 失败案例
- `reference` - 参考资料
- `guide` - 指南
- `practice` - 实践
- 其他类型

### 4. 可靠性等级分布

按可靠性等级统计：
- A级（高可靠性）- 回测验证
- B级（中高可靠性）- 实战验证、专业文献
- C级（中可靠性）- 经验总结
- D级（低可靠性）- 理论参考

### 5. 质量指标

质量指标统计：
- 可靠性标注覆盖率
- 结论部分覆盖率
- 标签覆盖率
- 来源覆盖率

---

## 🔧 技术实现

### 依赖库

- `plotly` - 交互式图表（可选）
- `pandas` - 数据处理（可选）

### 脚本位置

`scripts/kb/create_kb_dashboard.py`

### 生成流程

1. 加载知识库JSON文件
2. 分析知识库数据
3. 生成统计信息
4. 创建HTML仪表板
5. 创建Plotly交互式图表（如果可用）

---

## 📝 更新说明

### 2026-01-13

- ✅ 创建初始版本
- ✅ 支持HTML静态仪表板
- ✅ 支持Plotly交互式图表
- ✅ 修复可靠性等级统计问题

---

## 🎯 未来改进

### 计划功能

- [ ] 添加时间趋势分析
- [ ] 添加搜索热词统计
- [ ] 添加知识库使用情况统计
- [ ] 添加导出功能（PDF、PNG）
- [ ] 添加实时更新功能

---

**最后更新**: 2026-01-13  
**维护者**: TRQuant Team
