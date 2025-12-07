# BulletTrade 官方文档整理

> 来源：[BulletTrade 官方文档](https://bullettrade.cn/docs/)
> GitHub：https://github.com/BulletTrade/bullet-trade
> 版本：0.5.1

---

## 📚 文档目录

| 章节 | 链接 | 说明 |
|------|------|------|
| 文档首页 | [index.html](https://bullettrade.cn/docs/) | 主入口 |
| 快速上手 | [quickstart.html](https://bullettrade.cn/docs/quickstart.html) | 三步跑通回测/实盘 |
| 研究环境 | [research.html](https://bullettrade.cn/docs/research.html) | JupyterLab 启动 |
| 配置总览 | [config.html](https://bullettrade.cn/docs/config.html) | 环境变量一览 |
| 回测引擎 | [backtest.html](https://bullettrade.cn/docs/backtest.html) | 回测功能说明 |
| 参数优化 | [optimize.html](https://bullettrade.cn/docs/optimize.html) | 多进程并行优化 |
| 实盘引擎 | [live.html](https://bullettrade.cn/docs/live.html) | 本地/远程实盘 |
| Tick 行情指南 | [tick.html](https://bullettrade.cn/docs/tick.html) | Tick 订阅说明 |
| 交易支撑 | [trade-support.html](https://bullettrade.cn/docs/trade-support.html) | 聚宽模拟盘接入 |
| QMT 服务配置 | [qmt-server.html](https://bullettrade.cn/docs/qmt-server.html) | bullet-trade server |
| API 文档 | [api.html](https://bullettrade.cn/docs/api.html) | 策略 API 参考 |
| 数据源指南 | [data/](https://bullettrade.cn/docs/data/DATA_PROVIDER_GUIDE.html) | 聚宽/MiniQMT/TuShare |

---

## 🚀 BulletTrade 简介

BulletTrade 是一套**兼容聚宽 API** 的量化研究与交易框架：
- 支持**多数据源**：JQData、MiniQMT、TuShare、本地缓存
- 支持**多券商接入**：本地 QMT、远程 QMT server、模拟券商
- 覆盖**回测、仿真与本地/远程实盘**

---

## ⚡ 一键安装

```bash
# 推荐 Python 3.10+，创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate.bat  # Windows

# 一键安装
pip install bullet-trade

# 开发模式
pip install -e "bullet-trade[dev]"
cp bullet-trade/env.example bullet-trade/.env

# 验证安装
bullet-trade --version
```

---

## 🔧 常用 CLI 命令

### 回测
```bash
bullet-trade backtest strategies/demo_strategy.py \
  --start 2024-01-01 \
  --end 2024-03-01 \
  --frequency minute \
  --benchmark 000300.XSHG
```

### 参数优化
```bash
bullet-trade optimize strategies/demo_strategy.py \
  --params params.json \
  --start 2020-01-01 \
  --end 2023-12-31 \
  --output optimization.csv
```

### 实盘交易
```bash
# 本地 QMT
bullet-trade live strategies/demo_strategy.py --broker qmt

# 远程 QMT（需配置 .env 中 QMT_SERVER_*）
bullet-trade live strategies/demo_strategy.py --broker qmt-remote
```

### 远程服务（Windows QMT 端）
```bash
bullet-trade server \
  --listen 0.0.0.0 \
  --port 58620 \
  --token secret \
  --enable-data \
  --enable-broker
```

### 报告生成
```bash
bullet-trade report --input backtest_results --format html
```

### 研究环境
```bash
bullet-trade lab  # 启动 JupyterLab
```

---

## 📊 数据源配置

### 支持的数据源

| 数据源 | 环境变量 | 说明 |
|--------|----------|------|
| JQData | `DEFAULT_DATA_PROVIDER=jqdata` | 聚宽数据，需账号 |
| MiniQMT | `DEFAULT_DATA_PROVIDER=miniqmt` | 券商免费行情 |
| TuShare | `DEFAULT_DATA_PROVIDER=tushare` | 免费数据，需 Token |
| 模拟数据 | `DEFAULT_DATA_PROVIDER=simulator` | 本地模拟 |
| 远程 QMT | `DEFAULT_DATA_PROVIDER=qmt-remote` | 通过 server 获取 |

### JQData 配置
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=jqdata
JQDATA_USERNAME=your_username
JQDATA_PASSWORD=your_password
```

### MiniQMT 配置
```bash
# .env 文件
DEFAULT_DATA_PROVIDER=miniqmt
QMT_PATH=C:\国金证券QMT\userdata_mini
```

---

## 🏦 券商配置

### 支持的 Broker

| Broker | 环境变量 | 说明 |
|--------|----------|------|
| QMT | `DEFAULT_BROKER=qmt` | 本地 QMT（Windows） |
| QMT Remote | `DEFAULT_BROKER=qmt-remote` | 远程 QMT（Linux/Mac） |
| Simulator | `DEFAULT_BROKER=simulator` | 模拟交易 |

### 远程 QMT 配置

**Windows 端（QMT Server）：**
```bash
bullet-trade server \
  --listen 0.0.0.0 \
  --port 58620 \
  --token your_secret_token \
  --enable-data \
  --enable-broker
```

**Linux/Mac 端（客户端）：**
```bash
# .env 文件
DEFAULT_BROKER=qmt-remote
QMT_SERVER_HOST=192.168.1.100
QMT_SERVER_PORT=58620
QMT_SERVER_TOKEN=your_secret_token
```

---

## 📝 策略兼容性

BulletTrade 兼容聚宽策略代码：

```python
# 方式一：直接使用聚宽导入
from jqdata import *

# 方式二：使用 BulletTrade 兼容 API
from bullet_trade.compat.api import *

def initialize(context):
    set_benchmark('000300.XSHG')
    g.security = '000001.XSHE'

def handle_data(context, data):
    order(g.security, 100)
```

### 支持的 API

- `initialize(context)` - 初始化
- `handle_data(context, data)` - 数据处理
- `before_trading_start(context)` - 开盘前
- `after_trading_end(context)` - 收盘后
- `order(security, amount)` - 按股数下单
- `order_value(security, value)` - 按金额下单
- `order_target(security, amount)` - 目标持仓下单
- `get_price(security, ...)` - 获取历史价格
- `history(count, ...)` - 获取历史数据
- `set_benchmark(security)` - 设置基准
- `set_commission(...)` - 设置手续费
- `run_daily(func, time)` - 定时执行

---

## ⚠️ 风险与声明

- 量化及实盘有市场与系统风险，任何策略/软件均不保证收益
- 软件不可避免有 BUG，请先小额或模拟验证，自行承担交易风险
- TuShare 数据源受测试账号权限限制，覆盖不完全
- 示例策略以量价数据为主，财务/基本面数据建议通过聚宽模拟环境获取

---

## 🔗 参考链接

- **官方网站**：https://bullettrade.cn/
- **官方文档**：https://bullettrade.cn/docs/
- **GitHub 仓库**：https://github.com/BulletTrade/bullet-trade
- **聚宽远程 Helper**：https://github.com/BulletTrade/bullet-trade/blob/main/helpers/bullet_trade_jq_remote_helper.py
- **聚宽策略示例**：https://github.com/BulletTrade/bullet-trade/blob/main/helpers/jq_remote_strategy_example.py

---

*文档整理自 BulletTrade 官方文档，最后更新：2025-01*



