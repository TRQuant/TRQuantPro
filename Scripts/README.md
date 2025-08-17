# QuantConnect 工具脚本集

这个文件夹包含了用于自动化 QuantConnect Research 环境的各种工具脚本。

## 📁 脚本列表

### 1. `create_research_notebook.py` - 笔记本生成器

**功能**: 快速创建标准化的 QuantConnect Research 笔记本

**用法**:
```bash
# 创建基础笔记本
python create_research_notebook.py my_analysis

# 使用特定模板
python create_research_notebook.py strategy_dev --template strategy
python create_research_notebook.py backtest_analysis --template backtest
python create_research_notebook.py data_study --template data_analysis
```

**可用模板**:
- `basic`: 基础研究模板（默认）
- `backtest`: 回测分析模板
- `data_analysis`: 数据分析模板
- `strategy`: 策略开发模板

**特点**:
- 自动添加标准配置代码
- 预置常用库导入
- 包含示例代码和注释
- 支持多种研究场景

---

### 2. `backtest_analyzer.py` - 回测结果分析器

**功能**: 自动分析回测结果并生成可视化报告

**用法**:
```bash
# 分析单个回测
python backtest_analyzer.py 1230753028

# 指定输出目录
python backtest_analyzer.py 1230753028 --output my_analysis
```

**功能特性**:
- 📊 自动生成权益曲线图
- 📉 绘制回撤图
- 📅 月度收益热力图
- 📈 交易分布分析
- 📋 生成详细分析报告

**输出文件**:
- `{backtest_id}_equity_curve.png` - 权益曲线
- `{backtest_id}_drawdown.png` - 回撤图
- `{backtest_id}_monthly_returns.png` - 月度收益热力图
- `{backtest_id}_trade_distribution.png` - 交易分布图
- `{backtest_id}_analysis_report.md` - 分析报告

---

### 3. `data_downloader.py` - 数据下载器

**功能**: 批量下载和管理 QuantConnect 数据

**用法**:
```bash
# 下载单个股票
python data_downloader.py SPY

# 下载多个股票
python data_downloader.py SPY AAPL GOOGL

# 下载分钟级数据
python data_downloader.py SPY --resolution minute

# 指定日期范围
python data_downloader.py SPY --start-date 2020-01-01 --end-date 2024-01-01

# 下载预设数据
python data_downloader.py --indices      # 主要指数
python data_downloader.py --sectors      # 行业ETF
python data_downloader.py --commodities  # 商品
python data_downloader.py --crypto       # 加密货币

# 检查数据可用性
python data_downloader.py --check SPY AAPL

# 列出可用数据
python data_downloader.py --list
```

**支持的数据类型**:
- 股票 (equity)
- 期货 (future)
- 加密货币 (crypto)
- 外汇 (forex)

**支持的时间分辨率**:
- daily (日线)
- hour (小时线)
- minute (分钟线)
- second (秒线)
- tick (tick数据)

---

### 4. `notebook_manager.py` - 笔记本管理器

**功能**: 批量管理和处理 Jupyter 笔记本

**用法**:
```bash
# 添加标准配置到所有笔记本
python notebook_manager.py batch-add-config

# 清理笔记本输出
python notebook_manager.py batch-clean

# 转换笔记本格式
python notebook_manager.py convert --format py
python notebook_manager.py convert --format html
python notebook_manager.py convert --format pdf

# 备份笔记本
python notebook_manager.py backup
python notebook_manager.py backup --backup-name my_backup

# 恢复笔记本
python notebook_manager.py restore --backup-name my_backup

# 生成笔记本索引
python notebook_manager.py index

# 列出备份
python notebook_manager.py list-backups
```

**功能特性**:
- 🔧 自动添加 QuantConnect 标准配置
- 🧹 清理笔记本输出和执行计数
- 🔄 格式转换 (ipynb ↔ py/html/pdf)
- 💾 备份和恢复笔记本
- 📋 生成笔记本索引
- ⚡ 批量处理功能

---

## 🚀 快速开始

### 1. 设置环境
```bash
# 确保脚本可执行
chmod +x *.py

# 安装依赖（如果需要）
pip install nbformat pandas matplotlib seaborn
```

### 2. 创建工作流
```bash
# 1. 创建新的研究笔记本
python create_research_notebook.py my_strategy --template strategy

# 2. 下载需要的数据
python data_downloader.py SPY AAPL --resolution daily

# 3. 运行回测后分析结果
python backtest_analyzer.py <backtest_id>

# 4. 管理笔记本
python notebook_manager.py batch-add-config
python notebook_manager.py backup
```

### 3. 自动化脚本示例

创建 `setup_workspace.sh`:
```bash
#!/bin/bash
# 设置工作区脚本

echo "🚀 设置 QuantConnect Research 工作区..."

# 下载基础数据
python Scripts/data_downloader.py --indices
python Scripts/data_downloader.py --sectors

# 创建常用笔记本
python Scripts/create_research_notebook.py market_analysis --template data_analysis
python Scripts/create_research_notebook.py strategy_backtest --template strategy

# 添加标准配置
python Scripts/notebook_manager.py batch-add-config

# 生成索引
python Scripts/notebook_manager.py index

echo "✅ 工作区设置完成！"
```

---

## 📋 最佳实践

### 1. 笔记本命名规范
```
{项目名}_{功能}_{日期}.ipynb
示例: 
- spy_momentum_strategy_20240817.ipynb
- market_analysis_daily_20240817.ipynb
- backtest_analysis_1230753028.ipynb
```

### 2. 数据管理
- 定期使用 `data_downloader.py --list` 检查数据完整性
- 使用预设选项批量下载相关数据
- 为不同项目创建专门的数据目录

### 3. 笔记本管理
- 定期备份重要笔记本
- 使用 `notebook_manager.py index` 维护索引
- 清理笔记本输出以减小文件大小

### 4. 回测分析
- 为每个回测创建专门的分析笔记本
- 使用 `backtest_analyzer.py` 生成标准报告
- 保存分析结果和图表

---

## 🔧 故障排除

### 常见问题

1. **脚本权限错误**
   ```bash
   chmod +x Scripts/*.py
   ```

2. **依赖缺失**
   ```bash
   pip install nbformat pandas matplotlib seaborn
   ```

3. **数据下载失败**
   - 检查网络连接
   - 确认 QuantConnect 账户状态
   - 验证符号名称

4. **笔记本转换失败**
   - 确保安装了 `jupyter nbconvert`
   - 检查笔记本格式是否正确

### 获取帮助
```bash
# 查看脚本帮助
python Scripts/create_research_notebook.py --help
python Scripts/backtest_analyzer.py --help
python Scripts/data_downloader.py --help
python Scripts/notebook_manager.py --help
```

---

## 📝 更新日志

- **v1.0** (2025-08-17): 初始版本
  - 笔记本生成器
  - 回测分析器
  - 数据下载器
  - 笔记本管理器

---

**注意**: 这些脚本需要 QuantConnect Lean CLI 环境。请确保已正确安装和配置 Lean CLI。 