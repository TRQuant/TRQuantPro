# 韬睿量化平台 - 高效开发原则

## 📋 概述

本文档记录在开发过程中总结的高效开发原则和最佳实践，供后续开发参考。

---

## 🎯 核心开发模式

### GPT深度研究 → Cursor实现 → 报告生成 → 文件管理 → AI阅读

```
┌─────────────────┐
│  GPT深度研究    │  ← 生成专业方案文档（如：A股主线识别量化流程建议书）
└────────┬────────┘
         ▼
┌─────────────────┐
│  Cursor实现     │  ← 根据方案开发具体工具
└────────┬────────┘
         ▼
┌─────────────────┐
│  报告生成       │  ← 自动生成HTML/Markdown报告
└────────┬────────┘
         ▼
┌─────────────────┐
│  文件管理       │  ← 分类存储在文件系统中
└────────┬────────┘
         ▼
┌─────────────────┐
│  Cursor阅读     │  ← AI自动阅读报告，进入下一环节
└─────────────────┘
```

---

## 🔧 技术原则

### 1. 异步优先原则

**问题**: 同步操作阻塞UI，用户体验差
**解决**: 所有耗时操作必须使用QThread异步执行

```python
# ❌ 错误示例 - 同步阻塞
def fetch_data(self):
    data = api.get_data()  # 阻塞UI
    self.update_table(data)

# ✅ 正确示例 - 异步执行
class DataWorker(QThread):
    finished = pyqtSignal(dict)
    
    def run(self):
        data = api.get_data()
        self.finished.emit(data)

def fetch_data(self):
    self.worker = DataWorker()
    self.worker.finished.connect(self._on_data_ready)
    self.worker.start()
```

### 2. 方法论预显示原则

**问题**: 用户不知道工具在做什么
**解决**: 页面加载时即展示完整方法论、参数、表格结构

```python
# 在__init__中就创建好所有UI元素
def __init__(self):
    self._create_methodology_section()  # 方法论说明
    self._create_parameters_section()   # 参数展示
    self._create_data_tables()          # 预显示表格结构
```

### 3. 数据透明原则

**问题**: 数据来源不明，用户不信任
**解决**: 明确显示每个数据的来源、API、更新时间

```python
DATA_SOURCES = {
    "sector_flow": {
        "name": "行业板块资金流向",
        "source": "同花顺 via AKShare",
        "api": "ak.stock_fund_flow_industry",
        "update": "实时",
    }
}
```

### 4. 错误优雅处理原则

**问题**: 错误导致程序崩溃
**解决**: 每个操作都有try-catch，提供友好提示和回退方案

```python
try:
    result = fetcher.fetch_data()
except Exception as e:
    logger.error(f"获取数据失败: {e}")
    # 回退到缓存数据
    result = self._get_cached_data()
    self._show_warning(f"使用缓存数据: {e}")
```

### 5. 报告自动化原则

**问题**: 分析结果难以保存和分享
**解决**: 每个分析工具都自动生成报告

```python
def on_analysis_complete(self, results):
    # 自动生成HTML报告
    report_path = self.generator.generate_html_report(results)
    # 自动打开
    self._open_report(report_path)
```

---

## 📁 目录结构原则

### 模块化组织

```
markets/
├── ashare/                 # A股市场
│   ├── mainline/           # 主线识别模块
│   │   ├── pro_engine.py   # 核心引擎
│   │   ├── report_generator.py
│   │   ├── real_data_fetcher.py
│   │   └── cursor_analyzer.py
│   ├── stock_selection/    # 个股筛选模块（待开发）
│   └── monitoring/         # 实时监控模块（待开发）
├── usstocks/               # 美股市场（待开发）
└── crypto/                 # 加密货币（待开发）
```

### 报告分类管理

```
reports/
├── mainline/
│   ├── daily/      # 每日报告
│   ├── weekly/     # 周度总结
│   └── archive/    # 历史归档
├── prompts/        # Cursor Prompt
└── cursor_analysis/ # AI分析结果
```

---

## 🎨 UI设计原则

### 1. 主题一致性

使用统一的Colors类，不硬编码颜色值：

```python
# ❌ 错误
label.setStyleSheet("color: #ff0000;")

# ✅ 正确
label.setStyleSheet(f"color: {Colors.ERROR};")
```

### 2. 进度反馈

长时间操作必须显示进度：

```python
self.progress_bar.setVisible(True)
self.progress_label.setText("正在抓取数据...")
```

### 3. 状态指示

使用图标和颜色指示状态：

```python
# ✅ 成功 - 绿色
# ⏳ 进行中 - 蓝色
# ❌ 失败 - 红色
# ⚠️ 警告 - 黄色
```

---

## 🔄 开发流程原则

### 1. 先方案后实现

1. 用GPT深度研究生成完整方案文档
2. 根据方案设计模块结构
3. 分步骤实现各模块
4. 生成测试报告验证

### 2. 增量开发

每次只做一个小改动，立即测试：

```bash
# 修改代码后
python -c "from gui.widgets.xxx import XxxPanel; print('OK')"
```

### 3. 及时记录

每个里程碑都更新文档：
- `DEVELOPMENT_MILESTONES.md` - 进展记录
- `DEVELOPMENT_PRINCIPLES.md` - 原则总结
- 模块README - 使用说明

---

## 📊 常见问题解决

### 问题1: Colors属性不存在

**原因**: 使用了不存在的颜色属性
**解决**: 检查theme.py中可用的Colors属性

```python
# 常用属性
Colors.PRIMARY, Colors.SUCCESS, Colors.ERROR, Colors.WARNING
Colors.TEXT_PRIMARY, Colors.TEXT_SECONDARY, Colors.TEXT_MUTED
Colors.BG_PRIMARY, Colors.BG_SECONDARY, Colors.BG_TERTIARY
Colors.BORDER_PRIMARY, Colors.BORDER_LIGHT
```

### 问题2: API参数错误

**原因**: 调用方法时传递了不支持的参数
**解决**: 检查方法签名，移除不支持的参数

```python
# ❌ 错误 - timeout参数不支持
result = fetcher.fetch_data(timeout=10)

# ✅ 正确
result = fetcher.fetch_data()
```

### 问题3: UI阻塞

**原因**: 在主线程执行耗时操作
**解决**: 使用QThread异步执行

---

## 🚀 下一步开发计划

### 优先级排序

1. **热度评分系统** - 复用主线识别的数据和架构
2. **个股筛选工具** - 基于主线识别结果筛选个股
3. **实时监控面板** - 预警和风控
4. **回测集成** - PTrade/QMT/聚宽打通

### 开发顺序建议

```
主线识别 ✅ → 热度评分 → 个股筛选 → 实时监控 → 回测验证
     ↓           ↓           ↓           ↓
  数据层复用   评分模型复用  筛选逻辑    信号触发
```

---

---

## 🤖 AI模型智能选择

### 📌 默认模式: Auto Mode (Claude Sonnet)

**重要**: 从现在起，**默认使用 Auto Mode**。大部分任务都可以用Auto Mode完成。

### 使用流程

```
1. 开始任务
   ↓
2. 运行评估: python scripts/task_evaluator.py
   ↓
3. 查看建议:
   ├─ 建议 Auto (评分 <8) → ✅ 直接继续，用默认的 Auto Mode
   └─ 建议 Max (评分 ≥8)  → ⚠️  切换到 Max Mode 后继续
```

### 模型分级

| 模型 | 适用场景 | 成本 | 何时使用 |
|------|----------|------|----------|
| 🔥 Max Mode (Opus 4.5) | 架构设计、算法开发、疑难Bug | 高 | 评估评分 ≥8 |
| ⚡ Auto Mode (Sonnet) | 功能实现、文档、测试、UI | 中 | **默认模式** |
| ⚡⚡ Fast Mode (Haiku) | 小修改、格式化、查询 | 低 | 简单任务 |

### 快速决策

```
涉及架构/算法/多模块复杂问题？ → 🔥 Max Mode (需手动切换)
按已有模式实现功能？ → ⚡ Auto Mode (默认，直接继续)
简单修改/查询？ → ⚡⚡ Fast Mode (可选)
```

### ⚠️ 注意事项

- **不支持自动切换** - 需要手动在 Cursor 中切换 Max/Auto/Fast Mode
- **默认 Auto Mode** - 大部分任务直接用即可
- **遇到困难时** - 从 Auto 升级到 Max Mode

### 任务拆分策略

将大任务拆分，只在核心部分使用Max Mode：

```
热度评分系统开发:
├── 评分算法设计 → 🔥 Max Mode (核心)
├── GUI面板实现 → ⚡ Auto Mode
├── 报告生成器 → ⚡ Auto Mode
└── 样式微调 → ⚡⚡ Fast Mode
```

### 评估工具

运行 `python scripts/task_evaluator.py` 快速评估任务复杂度

详细策略参见: `docs/AI_MODEL_STRATEGY.md`

---

## 📝 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2024-11-28 | 添加AI模型智能选择策略 |
| 2024-11-28 | 初始版本，记录主线识别开发经验 |

---

*本文档持续更新，记录开发过程中的最佳实践*

