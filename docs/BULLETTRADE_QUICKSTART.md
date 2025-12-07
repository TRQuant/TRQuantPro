# BulletTrade 快速入门指南

> 基于 [BulletTrade 官方文档](https://bullettrade.cn/)

## 四步从准备到实盘

### 第一步：准备环境

```bash
# 安装 bullet-trade
pip install bullet-trade

# 如果需要 QMT 支持（Windows）
pip install "bullet-trade[qmt]"
```

### 第二步：启动研究

```bash
# 启动 JupyterLab 研究环境
bullet-trade lab

# 设置文件默认在 ~/.bullet-trade/setting.json
```

**研究根目录默认 `.env` 示例：**

```bash
# 根目录：~/bullet-trade（Windows: ~\bullet-trade）
DEFAULT_DATA_PROVIDER=jqdata
DEFAULT_BROKER=simulator
```

### 第三步：运行回测

```bash
# 运行回测
bullet-trade backtest demo_strategy.py --start 2025-01-01 --end 2025-06-01
```

### 第四步：实盘与远程

**本地/模拟实盘：**

```bash
bullet-trade live demo_strategy.py --broker qmt
```

**远程实盘：**

```bash
bullet-trade live demo_strategy.py --broker qmt-remote
```

**服务器运行实盘服务（Windows 端）：**

```bash
bullet-trade server --server-type=qmt --listen 0.0.0.0 --port 58620 --token my_security_123456
```

---

## TRQuant 集成使用

### Python API

```python
from core.bullettrade import (
    BulletTradeEngine,
    BTConfig,
    BrokerType,
    setup_bullet_trade_env,
    check_bullet_trade_installation
)

# 检查安装状态
status = check_bullet_trade_installation()
print(f"BulletTrade 已安装: {status['installed']}")
print(f"版本: {status['version']}")

# 设置环境
config = setup_bullet_trade_env(
    data_provider="jqdata",
    broker="simulator",
    jqdata_username="your_username",
    jqdata_password="your_password"
)

# 创建回测配置
bt_config = BTConfig(
    strategy_path="strategies/my_strategy.py",
    start_date="2020-01-01",
    end_date="2023-12-31",
    frequency="day",
    initial_capital=1000000,
    benchmark="000300.XSHG"
)

# 运行回测
engine = BulletTradeEngine(bt_config)
result = engine.run_backtest()

if result["success"]:
    print(f"总收益率: {result['metrics']['total_return']}%")
    print(f"夏普比率: {result['metrics']['sharpe_ratio']}")
```

### VS Code Extension

1. 打开命令面板 (`Ctrl+Shift+P`)
2. 搜索 `TRQuant: 打开量化工作台`
3. 点击 **策略回测** 或 **实盘交易**

---

## 配置文件说明

### ~/.bullet-trade/setting.json

```json
{
  "data_provider": "jqdata",
  "broker": "simulator",
  "research_root": "/home/user/bullet-trade",
  "server_host": "0.0.0.0",
  "server_port": 58620
}
```

### 项目根目录 .env

```bash
DEFAULT_DATA_PROVIDER=jqdata
DEFAULT_BROKER=simulator
JQDATA_USERNAME=your_username
JQDATA_PASSWORD=your_password
```

---

## 聚宽远程接入

### 1. 上传辅助库到聚宽研究环境

从 GitHub 下载辅助库：
- [bullet_trade_jq_remote_helper.py](https://github.com/BulletTrade/bullet-trade/blob/main/helpers/bullet_trade_jq_remote_helper.py)

### 2. 策略示例

参考官方 demo：
- [jq_remote_strategy_example.py](https://github.com/BulletTrade/bullet-trade/blob/main/helpers/jq_remote_strategy_example.py)

---

## 常见问题

### Q: BulletTrade 未安装怎么办？

```bash
pip install bullet-trade
```

### Q: QMT 支持如何启用？

```bash
# Windows 下安装
pip install "bullet-trade[qmt]"
```

### Q: 如何连接远程 QMT？

1. 在 Windows 机器上启动服务器：
   ```bash
   bullet-trade server --server-type=qmt --listen 0.0.0.0 --port 58620 --token your_token
   ```

2. 在 Linux/Mac 上运行策略：
   ```bash
   bullet-trade live strategy.py --broker qmt-remote
   ```

---

## 参考资料

- [BulletTrade 官网](https://bullettrade.cn/)
- [BulletTrade GitHub](https://github.com/BulletTrade/bullet-trade)
- [聚宽 API 文档](https://www.joinquant.com/help/api/help)

---

*文档版本: v1.0*
*最后更新: 2025-01*



