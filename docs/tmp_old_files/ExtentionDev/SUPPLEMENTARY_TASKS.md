# TRQuant Cursor Extension 补充开发任务清单

## 📊 任务概览

| Phase | 名称 | 任务数 | 预计工时 | 状态 |
|-------|------|--------|----------|------|
| 4 | 项目管理系统 | 3 | 10天 | 🔴 待开发 |
| 5 | 本地回测引擎 | 3 | 17天 | 🔴 待开发 |
| 6 | 专业可视化 | 3 | 12天 | 🔴 待开发 |
| 7 | 策略优化器 | 3 | 12天 | 🔴 待开发 |
| 8 | 实盘对接 | 3 | 14天 | 🔴 待开发 |
| 9 | 高级MCP工具 | 2 | 8天 | 🔴 待开发 |
| 10 | 数据服务增强 | 2 | 9天 | 🔴 待开发 |

**总计: 19个任务, 82个工作日**

---

## Phase 4: 项目管理系统

### P4-001 项目创建向导
- [ ] 实现多步骤QuickPick向导
- [ ] 项目模板选择（多因子/动量/套利/自定义）
- [ ] 参数配置（股票池/回测周期/资金规模）
- [ ] 生成项目结构和配置文件
- [ ] 创建.trquant/project.json

### P4-002 项目资源管理器
- [ ] 实现TreeDataProvider
- [ ] 左侧边栏Tree View
- [ ] 文件分类（策略/数据/配置/报告）
- [ ] 右键菜单操作
- [ ] 文件状态装饰器

### P4-003 项目配置管理
- [ ] Custom Editor Provider
- [ ] 图形化配置界面
- [ ] JSON Schema验证
- [ ] 实时预览

---

## Phase 5: 本地回测引擎

### P5-001 回测引擎核心
- [ ] 对接TRQuant BacktestEngine
- [ ] 日频回测支持
- [ ] 分钟频回测支持
- [ ] 多股票组合回测
- [ ] 交易成本/滑点模拟
- [ ] 增量数据加载优化

### P5-002 回测任务管理
- [ ] TRQuant: Run Backtest命令
- [ ] 回测队列管理
- [ ] 后台运行机制
- [ ] 进度实时显示
- [ ] 任务取消支持

### P5-003 回测结果管理
- [ ] 结果存储（MongoDB）
- [ ] 历史记录查看
- [ ] 结果对比功能
- [ ] 导出PDF/Excel
- [ ] 自动归档

---

## Phase 6: 专业可视化

### P6-001 图表库集成
- [ ] 集成ECharts
- [ ] K线图实现
- [ ] 收益曲线图
- [ ] 回撤曲线图
- [ ] 因子暴露热力图
- [ ] 相关性矩阵图
- [ ] 图表交互（缩放/标注）

### P6-002 实时监控面板
- [ ] Dashboard布局设计
- [ ] 实时行情组件
- [ ] 持仓监控组件
- [ ] 风险指标组件
- [ ] WebSocket实时推送
- [ ] 可定制布局

### P6-003 报告生成系统
- [ ] 报告模板设计
- [ ] 回测报告生成
- [ ] 策略分析报告
- [ ] 风险评估报告
- [ ] 图表截图嵌入
- [ ] PDF/HTML导出

---

## Phase 7: 策略优化器

### P7-001 参数优化
- [ ] TRQuant: Optimize Strategy命令
- [ ] 参数空间定义
- [ ] 网格搜索实现
- [ ] 并行优化任务
- [ ] 优化结果3D可视化
- [ ] 最优参数推荐

### P7-002 Walk-Forward分析
- [ ] 滚动窗口回测
- [ ] 时间窗口配置
- [ ] 过拟合检测
- [ ] 稳定性评分
- [ ] 结果可视化

### P7-003 因子分析工具
- [ ] 因子IC分析
- [ ] 因子IR分析
- [ ] 因子收益分解
- [ ] 因子相关性检测
- [ ] 因子贡献可视化

---

## Phase 8: 实盘对接

### P8-001 PTrade实盘部署
- [ ] TRQuant: Deploy to PTrade命令
- [ ] 代码格式验证
- [ ] PTrade API对接
- [ ] 一键部署功能
- [ ] 策略状态同步
- [ ] 部署日志记录

### P8-002 QMT实盘部署
- [ ] TRQuant: Deploy to QMT命令
- [ ] QMT代码格式适配
- [ ] xtquant SDK集成
- [ ] miniQMT连接管理
- [ ] Windows VM远程部署
- [ ] 实盘监控

### P8-003 持仓同步
- [ ] 实盘持仓导入
- [ ] 持仓与策略对比
- [ ] 持仓风险监控
- [ ] 调仓建议生成

---

## Phase 9: 高级MCP工具

### P9-001 扩展MCP工具集
- [ ] trquant_create_project
- [ ] trquant_run_backtest
- [ ] trquant_optimize_params
- [ ] trquant_get_realtime_data
- [ ] trquant_deploy_strategy
- [ ] trquant_get_portfolio
- [ ] trquant_compare_strategies

### P9-002 AI工作流自动化
- [ ] 工具链编排
- [ ] 上下文记忆
- [ ] 自动化流程
- [ ] 研究报告生成

---

## Phase 10: 数据服务增强

### P10-001 数据源管理
- [ ] 数据源适配器接口
- [ ] JQData适配器
- [ ] AKShare适配器
- [ ] Baostock适配器
- [ ] 通达信适配器
- [ ] MongoDB数据缓存
- [ ] 增量更新机制

### P10-002 实时数据订阅
- [ ] WebSocket服务
- [ ] Level-1行情订阅
- [ ] 分钟线实时更新
- [ ] 资金流向监控
- [ ] 新闻/公告推送
- [ ] 订阅管理

---

## 🎯 立即开始的任务

### 本周任务

```
1. P4-001 项目创建向导 (3天)
   - 创建 extension/src/commands/createProject.ts
   - 实现项目模板选择
   - 生成项目结构

2. P4-002 项目资源管理器 (5天)
   - 创建 extension/src/views/projectExplorer.ts
   - 实现TreeDataProvider
   - 添加右键菜单
```

### 下周任务

```
3. P5-001 回测引擎核心 (第1周)
   - 分析TRQuant现有BacktestEngine
   - 设计Extension集成接口
   - 实现基础回测功能
```

---

## 📋 技术准备清单

### 需要安装的依赖

```bash
# 前端图表
npm install echarts

# WebSocket通信
npm install ws

# 报告生成
pip install jinja2 weasyprint
```

### 需要创建的文件

```
extension/
├── src/
│   ├── commands/
│   │   ├── createProject.ts      # 新增
│   │   ├── runBacktest.ts        # 新增
│   │   ├── optimizeStrategy.ts   # 新增
│   │   └── deployStrategy.ts     # 新增
│   ├── views/
│   │   ├── projectExplorer.ts    # 新增
│   │   ├── backtestPanel.ts      # 新增
│   │   ├── dashboardPanel.ts     # 新增
│   │   └── chartPanel.ts         # 新增
│   └── services/
│       ├── backtestRunner.ts     # 新增
│       ├── dataService.ts        # 新增
│       └── deployService.ts      # 新增
├── python/
│   ├── backtest_engine.py        # 新增
│   ├── optimizer.py              # 新增
│   └── data_service.py           # 新增
└── webview/
    ├── charts/                   # 新增
    │   ├── kline.tsx
    │   └── equity.tsx
    └── dashboard/                # 新增
        └── index.tsx
```

---

## ✅ 验收标准

### Phase 4 验收
- [ ] 能创建新项目并生成标准结构
- [ ] 项目资源管理器正常显示
- [ ] 右键菜单功能完整

### Phase 5 验收
- [ ] 能运行完整回测
- [ ] 回测进度实时显示
- [ ] 回测结果正确存储

### Phase 6 验收
- [ ] 专业级图表显示
- [ ] 报告导出功能正常
- [ ] Dashboard实时更新

### Phase 7 验收
- [ ] 参数优化正常运行
- [ ] 优化结果可视化
- [ ] Walk-Forward分析完整

### Phase 8 验收
- [ ] PTrade策略成功部署
- [ ] QMT策略成功部署
- [ ] 持仓同步正常

### Phase 9 验收
- [ ] 所有MCP工具可用
- [ ] AI能自动调用工具链

### Phase 10 验收
- [ ] 多数据源切换正常
- [ ] 实时数据订阅正常

---

*更新日期: 2025-12-02*







