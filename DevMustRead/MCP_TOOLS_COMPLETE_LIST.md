# TRQuant MCP工具完整清单

> 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
> 工具总数: 约280个

---

## 一、9步投资工作流服务器 (`workflow_9steps_server.py`)

| 工具名称 | 描述 | 必需参数 |
|---------|------|---------|
| `workflow9.get_steps` | 获取9步工作流的所有步骤定义 | 无 |
| `workflow9.create` | 创建新的9步工作流会话 | name(可选) |
| `workflow9.status` | 获取工作流状态 | workflow_id |
| `workflow9.run_step` | 执行指定步骤 | workflow_id, step_id |
| `workflow9.run_all` | 一键执行所有9个步骤 | workflow_id |
| `workflow9.get_context` | 获取工作流上下文 | workflow_id |
| `workflow9.list` | 列出所有保存的工作流 | limit(可选), status(可选) |
| `workflow9.restore` | 从存储恢复工作流 | workflow_id |
| `workflow9.delete` | 删除保存的工作流 | workflow_id |

### 9步工作流定义:
1. **data_source** - 信息获取 (📡)
2. **market_trend** - 市场趋势 (📈)
3. **mainline** - 投资主线 (🔥)
4. **candidate_pool** - 候选池构建 (📦)
5. **factor** - 因子构建 (🧮)
6. **strategy** - 策略生成 (💻)
7. **backtest** - 回测验证 (🔄)
8. **optimization** - 策略优化 (⚙️)
9. **report** - 报告生成 (📄)

---

## 二、十倍股早期识别系统 (`utils/tenbagger_tools.py`)

| 工具名称 | 描述 | 必需参数 |
|---------|------|---------|
| `tenbagger.evaluate` | 综合评估股票的十倍股潜力 | symbol, name |
| `tenbagger.report` | 获取股票的评估报告 | symbol |
| `tenbagger.rank` | 获取所有已评估股票排名 | top_n(可选) |
| `tenbagger.history` | 获取股票评估历史 | symbol |
| `tenbagger.batch` | 批量评估多只股票 | stocks |
| `tenbagger.filter` | 按等级筛选股票 | min_level(可选) |
| `tenbagger.stats` | 获取评估统计信息 | 无 |

### 评估等级: S+ > S > A > B > C > D

### 7维评分卡:
1. 成长维度 (growth)
2. 动量维度 (momentum)
3. 风险维度 (risk)
4. 行业维度 (industry)
5. 阶段维度 (stage)
6. 评分卡维度 (scorecard)
7. 另类数据维度 (altdata)

---

## 三、轩辕剑灵/统一开发服务器 (`unified_dev_server.py`) - 103个工具

### 3.1 会话管理 (session.*)
| 工具名称 | 描述 |
|---------|------|
| `session.init` | 初始化开发会话 |
| `session.summary` | 获取会话摘要 |
| `session.checklist` | 获取开发检查清单 |

### 3.2 快捷操作 (quick.*)
| 工具名称 | 描述 |
|---------|------|
| `quick.start_task` | 一键开始任务 |
| `quick.finish_task` | 一键完成任务 |
| `quick.log` | 快速记录日志 |
| `quick.issue` | 快速创建问题 |

### 3.3 任务管理 (task.*)
| 工具名称 | 描述 |
|---------|------|
| `task.create` | 创建任务 |
| `task.list` | 列出任务 |
| `task.get` | 获取任务详情 |
| `task.update` | 更新任务 |
| `task.complete` | 完成任务 |
| `task.add_note` | 添加任务备注 |
| `task.analyze` | 分析任务复杂度 |
| `task.recommend_mode` | 推荐执行模式 |
| `task.cache_context` | 缓存上下文 |

### 3.4 开发日志 (devlog.*)
| 工具名称 | 描述 |
|---------|------|
| `devlog.add` | 添加开发日志 |
| `devlog.list` | 列出开发日志 |

### 3.5 问题跟踪 (issue.*)
| 工具名称 | 描述 |
|---------|------|
| `issue.create` | 创建问题 |
| `issue.list` | 列出问题 |
| `issue.resolve` | 解决问题 |

### 3.6 里程碑 (milestone.*)
| 工具名称 | 描述 |
|---------|------|
| `milestone.create` | 创建里程碑 |
| `milestone.list` | 列出里程碑 |
| `milestone.progress` | 更新里程碑进度 |

### 3.7 知识管理 (knowledge.*)
| 工具名称 | 描述 |
|---------|------|
| `knowledge.add` | 添加知识 |
| `knowledge.search` | 搜索知识 |
| `knowledge.get` | 获取知识详情 |
| `knowledge.update` | 更新知识 |
| `knowledge.mark_useful` | 标记有用 |
| `knowledge.stats` | 知识库统计 |

### 3.8 自学习 (learn.*)
| 工具名称 | 描述 |
|---------|------|
| `learn.from_issue` | 从问题学习 |
| `learn.from_experience` | 从经验学习 |
| `learn.suggest` | 智能建议 |
| `learn.auto_extract` | 批量提取知识 |

### 3.9 策略知识库 (kb.*)
| 工具名称 | 描述 |
|---------|------|
| `kb.search` | 搜索策略知识库 |
| `kb.get_strategy` | 获取策略详情 |
| `kb.get_api` | 获取API文档 |
| `kb.best_practices` | 获取最佳实践 |
| `kb.add` | 添加知识条目 |

### 3.10 最佳实践 (practice.*)
| 工具名称 | 描述 |
|---------|------|
| `practice.add` | 添加最佳实践 |
| `practice.list` | 列出最佳实践 |
| `practice.search` | 搜索最佳实践 |

### 3.11 研究笔记 (research.*)
| 工具名称 | 描述 |
|---------|------|
| `research.note` | 添加研究笔记 |
| `research.list` | 列出研究笔记 |
| `research.search` | 搜索研究笔记 |

### 3.12 证据追踪 (evidence.*)
| 工具名称 | 描述 |
|---------|------|
| `evidence.add` | 添加决策证据 |
| `evidence.list` | 列出证据 |
| `evidence.search` | 搜索证据 |

### 3.13 经验记录 (experience.*)
| 工具名称 | 描述 |
|---------|------|
| `experience.add` | 添加经验 |
| `experience.search` | 搜索经验 |
| `experience.mark_useful` | 标记经验有用 |

### 3.14 代码分析 (code.*)
| 工具名称 | 描述 |
|---------|------|
| `code.analyze` | 分析代码 |
| `code.convert` | 代码转换 |
| `code.lint` | 代码检查 |

### 3.15 代码检查 (lint.*)
| 工具名称 | 描述 |
|---------|------|
| `lint.check` | 检查代码 |
| `lint.fix` | 修复代码 |
| `lint.rules` | 列出规则 |

### 3.16 工程工具 (eng.*)
| 工具名称 | 描述 |
|---------|------|
| `eng.build` | 构建项目 |
| `eng.deploy` | 部署项目 |
| `eng.test` | 运行测试 |

### 3.17 GUI开发 (gui.*)
| 工具名称 | 描述 |
|---------|------|
| `gui.status` | GUI状态 |
| `gui.validate` | 验证GUI |
| `gui.generate_html` | 生成HTML |
| `gui.check_csp` | 检查CSP |

### 3.18 面板管理 (panel.*)
| 工具名称 | 描述 |
|---------|------|
| `panel.list` | 列出面板 |
| `panel.get_config` | 获取面板配置 |
| `panel.validate` | 验证面板 |

### 3.19 Webview (webview.*)
| 工具名称 | 描述 |
|---------|------|
| `webview.create_message` | 创建消息 |
| `webview.generate_script` | 生成脚本 |
| `webview.validate_message` | 验证消息 |

### 3.20 网络爬虫 (crawler.*)
| 工具名称 | 描述 |
|---------|------|
| `crawler.fetch` | 抓取网页内容 |
| `crawler.search_docs` | 搜索文档 |
| `crawler.download` | 下载文件 |
| `crawler.extract_code` | 从网页提取代码块 |
| `crawler.api_docs` | 获取API文档 |

### 3.21 调试工具 (debug.*)
| 工具名称 | 描述 |
|---------|------|
| `debug.log` | 记录调试日志 |
| `debug.trace` | 记录操作跟踪 |
| `debug.status` | 调试状态 |

### 3.22 文档管理 (docs.*)
| 工具名称 | 描述 |
|---------|------|
| `docs.get` | 获取文档 |
| `docs.list` | 列出文档 |
| `docs.search` | 搜索文档 |

### 3.23 模块注册 (registry.*)
| 工具名称 | 描述 |
|---------|------|
| `registry.register` | 注册模块 |
| `registry.list` | 列出模块 |
| `registry.status` | 系统状态 |
| `registry.snapshot` | 创建快照 |

### 3.24 风险管理 (risk.*)
| 工具名称 | 描述 |
|---------|------|
| `risk.add` | 添加风险 |
| `risk.assess` | 评估风险 |

### 3.25 进度报告 (progress.*)
| 工具名称 | 描述 |
|---------|------|
| `progress.summary` | 进度摘要 |
| `progress.daily_report` | 生成日报 |

### 3.26 工作流批处理 (workflow.*)
| 工具名称 | 描述 |
|---------|------|
| `workflow.batch` | 批量执行工具 |
| `workflow.check` | 检查开发流程状态 |

### 3.27 其他工具
| 工具名称 | 描述 |
|---------|------|
| `schema.list` | 列出Schema |
| `schema.get` | 获取Schema |
| `schema.validate` | 验证Schema |
| `spec.list` | 列出规范 |
| `spec.get` | 获取规范 |
| `spec.check` | 检查规范 |
| `secrets.list` | 列出密钥 |
| `secrets.get` | 获取密钥 |
| `secrets.set` | 设置密钥 |
| `test.run` | 运行测试 |
| `test.coverage` | 测试覆盖率 |
| `test.report` | 测试报告 |

---

## 四、核心量化服务器 (`trquant_core_server.py`) - 25个工具

### 4.1 数据获取 (data.*)
| 工具名称 | 描述 |
|---------|------|
| `data.get_price` | 获取价格数据 |
| `data.get_index_stocks` | 获取指数成分股 |
| `data.candidate_pool` | 构建候选池 |
| `data.health_check` | 数据源健康检查 |

### 4.2 市场分析 (market.*)
| 工具名称 | 描述 |
|---------|------|
| `market.status` | 获取市场状态 |
| `market.trend` | 获取市场趋势 |
| `market.mainlines` | 获取投资主线 |
| `market.five_dimension_score` | 五维评分 |
| `market.comprehensive` | 综合分析 |

### 4.3 因子计算 (factor.*)
| 工具名称 | 描述 |
|---------|------|
| `factor.list` | 列出因子 |
| `factor.calculate` | 计算因子 |
| `factor.recommend` | 推荐因子 |

### 4.4 策略生成 (strategy.*)
| 工具名称 | 描述 |
|---------|------|
| `strategy.generate` | 生成策略 |
| `strategy.validate` | 验证策略 |
| `strategy.list_templates` | 列出策略模板 |

### 4.5 回测验证 (backtest.*)
| 工具名称 | 描述 |
|---------|------|
| `backtest.quick` | 快速回测 |
| `backtest.run` | 运行回测 |
| `backtest.compare` | 比较回测结果 |

### 4.6 参数优化 (optimizer.*)
| 工具名称 | 描述 |
|---------|------|
| `optimizer.grid_search` | 网格搜索 |
| `optimizer.optuna` | Optuna优化 |
| `optimizer.best_params` | 获取最佳参数 |

### 4.7 性能监控 (perf.*)
| 工具名称 | 描述 |
|---------|------|
| `perf.detailed_stats` | 详细统计 |
| `perf.reset_stats` | 重置统计 |

### 4.8 缓存管理 (cache.*)
| 工具名称 | 描述 |
|---------|------|
| `cache.warmup` | 缓存预热 |

---

## 五、数据源服务器 (`data_source_server_v2.py`) - 9个工具

| 工具名称 | 描述 |
|---------|------|
| `data_source.get_price` | 获取股票历史价格数据 |
| `data_source.get_index_stocks` | 获取指数成分股 |
| `data_source.get_realtime` | 获取实时行情 |
| `data_source.candidate_pool` | 构建候选股票池 |
| `data_source.health_check` | 数据源健康检查 |
| `data_source.status` | 获取数据源状态 |
| `data_source.switch` | 切换数据源 |
| `data_source.cache_stats` | 缓存统计 |
| `data_source.clear_cache` | 清除缓存 |

---

## 六、市场分析服务器 (`market_server_v2.py`) - 11个工具

| 工具名称 | 描述 |
|---------|------|
| `market.status` | 获取当前市场状态（牛市/熊市/震荡） |
| `market.trend` | 获取市场趋势分析（短期/中期/长期） |
| `market.mainlines` | 获取当前市场主线（五维评分） |
| `market.sectors` | 板块轮动分析 |
| `market.capital_flow` | 资金流向分析 |
| `market.macro` | 宏观经济分析 |
| `market.sentiment` | 市场情绪分析 |
| `market.risk` | 市场风险评估 |
| `market.eastmoney_concepts` | 东方财富概念板块 |
| `market.five_dimension_score` | 五维评分系统 |
| `market.comprehensive` | 综合市场分析 |

---

## 七、回测服务器 (`backtest_server_v2.py`) - 9个工具

| 工具名称 | 描述 |
|---------|------|
| `backtest.fast` | 快速回测（<5秒） |
| `backtest.standard` | 标准回测（<30秒） |
| `backtest.bullettrade` | BulletTrade精确回测 |
| `backtest.qmt` | QMT回测 |
| `backtest.bullettrade_batch` | BulletTrade批量回测 |
| `backtest.qmt_batch` | QMT批量回测 |
| `backtest.bullettrade_optimize` | BulletTrade参数优化 |
| `backtest.qmt_optimize` | QMT参数优化 |
| `backtest.data_status` | 回测数据状态 |

---

## 八、策略服务器 (`strategy_server.py`, `strategy_template_server.py`) - 14个工具

| 工具名称 | 描述 |
|---------|------|
| `strategy.generate` | 生成策略代码 |
| `strategy.validate` | 验证策略 |
| `strategy.save` | 保存策略 |
| `strategy.list_templates` | 列出策略模板 |
| `strategy.convert` | 转换策略格式 |
| `strategy.optimize` | 优化策略参数 |
| `strategy_template.list` | 列出策略模板 |
| `strategy_template.info` | 获取模板信息 |
| `strategy_template.generate` | 生成模板代码 |
| `template.list` | 列出模板 |
| `template.get` | 获取模板 |
| `template.generate` | 生成模板 |
| `template.params` | 获取模板参数 |
| `template.export` | 导出模板 |

---

## 九、因子服务器 (`factor_server.py`) - 8个工具

| 工具名称 | 描述 |
|---------|------|
| `factor.list` | 列出所有因子 |
| `factor.get` | 获取因子详情 |
| `factor.calculate` | 计算因子值 |
| `factor.recommend` | 根据市场状态推荐因子 |
| `factor.analyze` | 因子分析 |
| `factor.evaluate` | 因子评估 |
| `factor.decay` | 因子衰减分析 |
| `factor.ic_analysis` | IC分析 |

---

## 十、报告服务器 (`report_server.py`) - 7个工具

| 工具名称 | 描述 |
|---------|------|
| `report.generate` | 生成研究报告 |
| `report.get` | 获取报告 |
| `report.list` | 列出报告 |
| `report.delete` | 删除报告 |
| `report.compare` | 比较报告 |
| `report.summary` | 报告摘要 |
| `report.diagnosis` | 策略诊断 |

---

## 十一、优化服务器 (`optimizer_server.py`) - 6个工具

| 工具名称 | 描述 |
|---------|------|
| `optimizer.grid_search` | 网格搜索优化 |
| `optimizer.evolve` | 进化算法优化 |
| `optimizer.multi_objective` | 多目标优化 |
| `optimizer.optuna` | Optuna贝叶斯优化 |
| `optimizer.sensitivity` | 敏感度分析 |
| `optimizer.best_params` | 获取最佳参数 |

---

## 十二、Utils工具模块

### 12.1 数据源工具 (`datasource_tools.py`)
| 工具名称 | 描述 |
|---------|------|
| `datasource.fetch_price` | 获取价格数据 |
| `datasource.fetch_financial` | 获取财务数据 |
| `datasource.fetch_announcements` | 获取公告 |
| `datasource.fetch_events` | 获取事件 |
| `datasource.fetch_altdata` | 获取另类数据 |
| `datasource.fetch_all` | 获取全部数据 |
| `datasource.stats` | 数据统计 |
| `datasource.clear_cache` | 清除缓存 |

### 12.2 另类数据工具 (`altdata_tools.py`)
| 工具名称 | 描述 |
|---------|------|
| `altdata.bid.query` | 查询招投标数据 |
| `altdata.bid.add` | 添加招投标数据 |
| `altdata.bid.trend` | 招投标趋势 |
| `altdata.job.query` | 查询招聘数据 |
| `altdata.job.add` | 添加招聘数据 |
| `altdata.job.trend` | 招聘趋势 |
| `altdata.batch` | 批量获取 |
| `altdata.signals` | 信号提取 |
| `altdata.stats` | 另类数据统计 |

### 12.3 产业链工具 (`industry_chain.py`)
| 工具名称 | 描述 |
|---------|------|
| `chain.list` | 列出产业链 |
| `chain.get` | 获取产业链详情 |
| `chain.find_node` | 查找节点 |
| `chain.get_upstream` | 获取上游 |
| `chain.get_downstream` | 获取下游 |
| `chain.related_stocks` | 相关股票 |
| `chain.map_stock` | 映射股票 |
| `chain.impact_analysis` | 影响分析 |
| `chain.stats` | 产业链统计 |

### 12.4 候选池工具 (`candidate_pool.py`)
| 工具名称 | 描述 |
|---------|------|
| `pool.add_universe` | 添加股票池 |
| `pool.filter_l1` | L1过滤 |
| `pool.filter_l2` | L2过滤 |
| `pool.filter_l3` | L3过滤 |
| `pool.get` | 获取候选池 |
| `pool.search` | 搜索候选池 |
| `pool.stats` | 候选池统计 |

### 12.5 组合管理工具 (`portfolio_tools.py`)
| 工具名称 | 描述 |
|---------|------|
| `portfolio.add_strategy` | 添加策略 |
| `portfolio.list_strategies` | 列出策略 |
| `portfolio.positions` | 持仓查询 |
| `portfolio.orders` | 订单查询 |
| `portfolio.order` | 下单 |
| `portfolio.rebalance` | 再平衡 |
| `portfolio.set_risk` | 设置风控 |
| `portfolio.risk_signals` | 风险信号 |
| `portfolio.update_prices` | 更新价格 |
| `portfolio.stats` | 组合统计 |

### 12.6 策略包工具 (`strategy_pack.py`)
| 工具名称 | 描述 |
|---------|------|
| `strategy.types` | 策略类型 |
| `strategy.create` | 创建策略 |
| `strategy.info` | 策略信息 |
| `strategy.list` | 列出策略 |
| `strategy.select` | 选择策略 |
| `strategy.run` | 运行策略 |
| `strategy.instances` | 策略实例 |
| `strategy.stats` | 策略统计 |

### 12.7 实验管理 (`experiment.py`)
| 工具名称 | 描述 |
|---------|------|
| `experiment.create` | 创建实验 |
| `experiment.list` | 列出实验 |
| `experiment.get` | 获取实验 |
| `experiment.update` | 更新实验 |
| `experiment.complete` | 完成实验 |
| `experiment.compare` | 比较实验 |
| `experiment.best` | 最佳实验 |
| `experiment.clone` | 克隆实验 |
| `experiment.stats` | 实验统计 |

---

## 十三、交易服务器 (`trading_server.py`) - 5个工具

| 工具名称 | 描述 |
|---------|------|
| `trading.status` | 交易状态 |
| `trading.positions` | 持仓查询 |
| `trading.orders` | 订单查询 |
| `trading.simulate` | 模拟交易 |
| `trading.dry_run` | 试运行 |

---

## 十四、配置服务器 (`config_server.py`) - 5个工具

| 工具名称 | 描述 |
|---------|------|
| `config.get` | 获取配置 |
| `config.set` | 设置配置 |
| `config.list` | 列出配置 |
| `config.validate` | 验证配置 |
| `config.reset` | 重置配置 |

---

## 工具命名规范

### 命名空间
- `workflow9.*` - 9步工作流
- `tenbagger.*` - 十倍股识别
- `market.*` - 市场分析
- `data.*` / `data_source.*` - 数据获取
- `factor.*` - 因子计算
- `strategy.*` - 策略管理
- `backtest.*` - 回测验证
- `optimizer.*` - 参数优化
- `report.*` - 报告生成
- `task.*` - 任务管理
- `knowledge.*` - 知识管理
- `quick.*` - 快捷操作

### 工具类型
- `.list` - 列出资源
- `.get` - 获取详情
- `.create` - 创建资源
- `.update` - 更新资源
- `.delete` - 删除资源
- `.search` - 搜索资源
- `.stats` - 统计信息

---

*文档版本: 1.0 | 生成工具: 轩辕剑灵 | 更新时间: 2024-12-19*
