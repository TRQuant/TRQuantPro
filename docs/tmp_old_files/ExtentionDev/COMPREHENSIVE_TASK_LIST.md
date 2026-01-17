# TRQuant Cursor Extension 综合开发任务列表

> 基于ExtentionDev文件夹所有文档的综合分析
> 创建日期: 2025-12-03
> 目标: 实现类似QuantConnect的完整A股量化投资插件

---

## 📋 任务总览

| 阶段 | 任务数 | 优先级 | 状态 |
|------|--------|--------|------|
| Phase 0: 基础设施验证 | 5 | 🔴 紧急 | ⏳ 进行中 |
| Phase 1: 核心GUI组件 | 8 | 🟠 高 | ⏳ 待开始 |
| Phase 2: MCP深度集成 | 6 | 🟠 高 | ⏳ 待开始 |
| Phase 3: 专业可视化 | 6 | 🟡 中 | ⏳ 待开始 |
| Phase 4: 策略优化器 | 5 | 🟡 中 | ⏳ 待开始 |
| Phase 5: 实盘部署 | 4 | 🟢 低 | ⏳ 待开始 |
| Phase 6: 质量保证 | 5 | 🔴 关键 | ⏳ 待开始 |

---

## 🔴 Phase 0: 基础设施验证 (紧急)

### Task 0.1: 清理并重新编译扩展
- **文件**: `extension/`
- **操作**:
  ```bash
  cd /home/taotao/dev/QuantTest/TRQuant/extension
  rm -rf dist node_modules
  npm install
  npm run compile
  ```
- **验证**: 无TypeScript编译错误
- **状态**: ⏳ 进行中

### Task 0.2: 修复package.json配置
- **文件**: `extension/package.json`
- **检查项**:
  - [ ] activationEvents正确配置
  - [ ] contributes.commands完整
  - [ ] contributes.views正确（暂时禁用未实现的TreeView）
  - [ ] icon路径有效
- **状态**: ⏳ 待验证

### Task 0.3: 打包VSIX安装包
- **操作**:
  ```bash
  cd /home/taotao/dev/QuantTest/TRQuant/extension
  npx @vscode/vsce package --no-dependencies
  ```
- **输出**: `trquant-x.x.x.vsix`
- **状态**: ⏳ 待执行

### Task 0.4: 安装并验证扩展
- **操作**:
  ```bash
  cursor --install-extension trquant-x.x.x.vsix
  ```
- **验证**:
  - [ ] 扩展成功激活
  - [ ] Welcome Panel显示
  - [ ] 命令面板可调用命令
- **状态**: ⏳ 待执行

### Task 0.5: Python Bridge验证
- **文件**: `extension/python/bridge.py`
- **验证**:
  ```bash
  cd /home/taotao/dev/QuantTest/TRQuant/extension/python
  echo '{"action":"get_market_status","params":{}}' | python3 bridge.py
  ```
- **预期**: 返回有效JSON响应
- **状态**: ⏳ 待执行

---

## 🟠 Phase 1: 核心GUI组件 (高优先级)

### Task 1.1: 实现市场状态TreeView
- **文件**: `extension/src/views/marketTreeView.ts`
- **功能**:
  - 显示大盘指数（上证、深证、创业板）
  - 显示市场情绪指标
  - 显示热门行业板块
  - 支持刷新和自动更新
- **API**: 调用`bridge.py`的`get_market_status`
- **状态**: ⏳ 待开发

### Task 1.2: 实现投资主线TreeView
- **文件**: `extension/src/views/mainlineTreeView.ts`
- **功能**:
  - 显示当前热门投资主线（TOP 10）
  - 显示主线评分和详情
  - 支持展开查看相关个股
  - 支持时间维度切换（短期/中期/长期）
- **API**: 调用`bridge.py`的`get_mainlines`
- **状态**: ⏳ 待开发

### Task 1.3: 实现策略管理TreeView
- **文件**: `extension/src/views/strategyTreeView.ts`
- **功能**:
  - 列出所有策略文件
  - 按平台分类（PTrade/QMT）
  - 显示策略状态（草稿/回测中/已验证/已部署）
  - 右键菜单（运行回测、查看结果、部署）
- **状态**: ⏳ 待开发

### Task 1.4: 实现回测历史TreeView
- **文件**: `extension/src/views/backtestHistoryTreeView.ts`
- **功能**:
  - 按时间倒序显示回测记录
  - 显示关键指标（收益率、夏普比率）
  - 支持点击查看详细报告
  - 支持对比多个回测
- **状态**: ⏳ 待开发

### Task 1.5: 更新package.json注册TreeView
- **文件**: `extension/package.json`
- **操作**: 
  - 添加viewsContainers
  - 添加views定义
  - 添加view commands
- **状态**: ⏳ 待开发

### Task 1.6: 实现项目创建向导WebView
- **文件**: `extension/src/views/projectWizard.ts`
- **功能**:
  - 步骤1: 选择目标平台（PTrade/QMT）
  - 步骤2: 选择策略类型（趋势/动量/因子等）
  - 步骤3: 配置基本参数
  - 步骤4: 生成项目结构
- **状态**: ⏳ 待开发

### Task 1.7: 实现回测结果WebView
- **文件**: `extension/src/views/backtestResultPanel.ts`
- **功能**:
  - 显示回测统计摘要
  - 显示收益曲线图表
  - 显示交易记录表格
  - 显示风险指标
- **状态**: ⏳ 待开发

### Task 1.8: 实现策略编辑器增强
- **文件**: `extension/src/editors/strategyEditor.ts`
- **功能**:
  - PTrade/QMT语法高亮
  - 代码片段自动补全
  - 内联API文档
  - 错误检测和建议
- **状态**: ⏳ 待开发

---

## 🟠 Phase 2: MCP深度集成 (高优先级)

### Task 2.1: 扩展MCP工具集
- **文件**: `extension/python/mcp_server.py`
- **当前工具**: 6个
- **目标工具**: 12个
- **新增工具**:
  - `analyze_stock`: 分析单只股票
  - `scan_stocks`: 股票筛选
  - `optimize_params`: 参数优化
  - `compare_backtests`: 对比回测
  - `export_strategy`: 导出策略
  - `deploy_live`: 实盘部署
- **状态**: ⏳ 待开发

### Task 2.2: 实现MCP资源服务
- **文件**: `extension/python/mcp_server.py`
- **资源类型**:
  - `strategy://`: 策略文件访问
  - `backtest://`: 回测结果访问
  - `data://`: 市场数据访问
- **状态**: ⏳ 待开发

### Task 2.3: 实现MCP提示词模板
- **文件**: `extension/python/mcp_server.py`
- **模板**:
  - 策略生成提示词
  - 回测分析提示词
  - 优化建议提示词
- **状态**: ⏳ 待开发

### Task 2.4: 优化.cursor/rules规则文件
- **文件**: `extension/rules/*.mdc`
- **内容**:
  - 架构规则 (`trquant-architecture.mdc`)
  - 代码风格 (`trquant-style.mdc`)
  - 提示词模板 (`trquant-prompts.mdc`)
- **状态**: ⏳ 待优化

### Task 2.5: 实现AI工作流自动化
- **文件**: `extension/src/services/aiWorkflow.ts`
- **功能**:
  - 自动分析市场→识别主线→推荐因子→生成策略
  - 支持人工干预和确认
  - 保存工作流历史
- **状态**: ⏳ 待开发

### Task 2.6: 实现上下文管理器
- **文件**: `extension/src/services/contextManager.ts`
- **功能**:
  - 管理当前项目上下文
  - 缓存市场数据
  - 维护会话状态
- **状态**: ⏳ 待开发

---

## 🟡 Phase 3: 专业可视化 (中优先级)

### Task 3.1: 集成ECharts图表库
- **文件**: `extension/src/views/charts/`
- **图表类型**:
  - K线图
  - 收益曲线
  - 回撤图
  - 因子分布图
- **状态**: ⏳ 待开发

### Task 3.2: 实现实时监控面板
- **文件**: `extension/src/views/monitorPanel.ts`
- **功能**:
  - 实时持仓展示
  - 盈亏实时更新
  - 风险指标监控
- **状态**: ⏳ 待开发

### Task 3.3: 实现回测报告生成
- **文件**: `extension/python/tools/report_generator.py`
- **格式**:
  - HTML报告
  - PDF报告
  - JSON数据
- **状态**: ⏳ 待开发

### Task 3.4: 实现对比分析视图
- **文件**: `extension/src/views/comparePanel.ts`
- **功能**:
  - 多策略对比
  - 多回测对比
  - 并排图表显示
- **状态**: ⏳ 待开发

### Task 3.5: 实现因子分析视图
- **文件**: `extension/src/views/factorAnalysisPanel.ts`
- **功能**:
  - 因子IC分析
  - 因子收益归因
  - 因子相关性矩阵
- **状态**: ⏳ 待开发

### Task 3.6: 实现交易日历视图
- **文件**: `extension/src/views/tradingCalendar.ts`
- **功能**:
  - 显示交易日历
  - 标记重要事件
  - 显示回测/交易记录
- **状态**: ⏳ 待开发

---

## 🟡 Phase 4: 策略优化器 (中优先级)

### Task 4.1: 实现参数网格搜索
- **文件**: `extension/python/tools/optimizer.py`
- **功能**:
  - 多参数组合搜索
  - 并行计算支持
  - 结果可视化
- **状态**: ⏳ 待开发

### Task 4.2: 实现Walk-Forward分析
- **文件**: `extension/python/tools/walk_forward.py`
- **功能**:
  - 滚动窗口回测
  - 样本内/样本外分析
  - 过拟合检测
- **状态**: ⏳ 待开发

### Task 4.3: 实现蒙特卡洛模拟
- **文件**: `extension/python/tools/monte_carlo.py`
- **功能**:
  - 收益分布模拟
  - 风险评估
  - 置信区间计算
- **状态**: ⏳ 待开发

### Task 4.4: 实现敏感性分析
- **文件**: `extension/python/tools/sensitivity.py`
- **功能**:
  - 参数敏感性测试
  - 鲁棒性评估
- **状态**: ⏳ 待开发

### Task 4.5: 实现优化结果管理
- **文件**: `extension/src/services/optimizationManager.ts`
- **功能**:
  - 保存优化结果
  - 对比不同优化方案
  - 导出最优参数
- **状态**: ⏳ 待开发

---

## 🟢 Phase 5: 实盘部署 (低优先级)

### Task 5.1: PTrade实盘接口
- **文件**: `extension/python/tools/ptrade_deployer.py`
- **功能**:
  - 策略上传
  - 参数配置
  - 状态监控
- **状态**: ⏳ 待开发

### Task 5.2: QMT实盘接口
- **文件**: `extension/python/tools/qmt_deployer.py`
- **功能**:
  - 策略上传
  - 参数配置
  - 状态监控
- **状态**: ⏳ 待开发

### Task 5.3: 持仓同步服务
- **文件**: `extension/python/tools/position_sync.py`
- **功能**:
  - 实时持仓同步
  - 盈亏计算
  - 风险预警
- **状态**: ⏳ 待开发

### Task 5.4: 交易记录管理
- **文件**: `extension/python/tools/trade_log.py`
- **功能**:
  - 交易记录存储
  - 交易分析
  - 导出报表
- **状态**: ⏳ 待开发

---

## 🔴 Phase 6: 质量保证 (关键)

### Task 6.1: 单元测试
- **文件**: `extension/src/test/`
- **覆盖率目标**: >80%
- **测试框架**: Mocha + Chai
- **状态**: ⏳ 待开发

### Task 6.2: 集成测试
- **文件**: `extension/src/test/integration/`
- **测试场景**:
  - 完整工作流测试
  - API调用测试
  - UI交互测试
- **状态**: ⏳ 待开发

### Task 6.3: 跨平台验证
- **平台**:
  - [x] Linux
  - [ ] Windows
  - [ ] macOS
- **状态**: ⏳ 待验证

### Task 6.4: 性能优化
- **目标**:
  - 扩展激活时间 < 1秒
  - API响应时间 < 500ms
  - 内存占用 < 200MB
- **状态**: ⏳ 待优化

### Task 6.5: 文档完善
- **文档**:
  - [ ] 用户手册 (USAGE.md)
  - [ ] 开发者指南 (DEVELOPMENT.md)
  - [ ] API文档 (API.md)
  - [ ] 常见问题 (FAQ.md)
- **状态**: ⏳ 待完善

---

## 📅 执行计划

### 第1周: Phase 0 (基础设施)
- Day 1-2: Task 0.1-0.5 (编译、打包、安装、验证)

### 第2周: Phase 1 (GUI组件)
- Day 1-2: Task 1.1-1.2 (市场TreeView、主线TreeView)
- Day 3-4: Task 1.3-1.4 (策略TreeView、回测TreeView)
- Day 5: Task 1.5 (package.json更新)

### 第3周: Phase 1 + Phase 2
- Day 1-2: Task 1.6-1.8 (WebView组件)
- Day 3-5: Task 2.1-2.3 (MCP工具扩展)

### 第4周: Phase 2 + Phase 3
- Day 1-2: Task 2.4-2.6 (MCP规则和工作流)
- Day 3-5: Task 3.1-3.3 (图表和报告)

### 第5周: Phase 3 + Phase 4
- Day 1-2: Task 3.4-3.6 (分析视图)
- Day 3-5: Task 4.1-4.3 (优化器核心)

### 第6周: Phase 4 + Phase 5
- Day 1-2: Task 4.4-4.5 (优化器完善)
- Day 3-5: Task 5.1-5.4 (实盘部署)

### 第7周: Phase 6 (质量保证)
- Day 1-3: Task 6.1-6.3 (测试)
- Day 4-5: Task 6.4-6.5 (优化和文档)

---

## 📝 备注

1. **时间维度原则**: 所有模块设计需遵循短期(1-5天)、中期(1-4周)、长期(1月+)三周期设计
2. **平台支持**: 优先PTrade，同步开发QMT支持
3. **数据源**: 使用JQData作为主数据源，AKShare作为备选
4. **港股/美股接口**: 预留接口，下一阶段开发
5. **优秀软件工程原则**: 模块化、可测试、可维护、DRY原则







