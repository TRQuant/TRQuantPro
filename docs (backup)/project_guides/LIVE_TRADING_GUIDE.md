# 实盘交易操作指南

## 一、系统架构

本系统已集成国金证券的 **Ptrade** 和 **QMT** 两个交易通道，实现了从回测到实盘的完整流程。

### 1.1 交易适配器架构

```
策略层 (BaseStrategy)
    ↓
实盘交易引擎 (LiveTradingEngine)
    ↓
交易适配器 (TradingAdapter)
    ├─ PtradeAdapter (国金证券 Ptrade)
    └─ QMTAdapter (国金证券 QMT)
```

### 1.2 核心组件

- **`brokers/trading_adapter.py`**: 交易适配器基类，定义统一接口
- **`brokers/ptrade_adapter.py`**: 国金证券 Ptrade 适配器
- **`brokers/qmt_adapter.py`**: 国金证券 QMT 适配器
- **`core/live_trading_engine.py`**: 实盘交易引擎
- **`config/broker_config.json`**: 券商配置文件（存储账号信息）

## 二、配置说明

### 2.1 账号配置

账号信息已存储在 `config/broker_config.json`：

```json
{
  "gjzq": {
    "account": "8885019982",
    "password": "774316",
    "ptrade": {
      "enabled": true,
      "host": "ptrade.gjzq.com",
      "port": 7709,
      "account_id": "8885019982"
    },
    "qmt": {
      "enabled": true,
      "qmt_path": "",
      "session_id": 123456,
      "account_id": "8885019982"
    }
  },
  "default_broker": "ptrade"
}
```

### 2.2 风控配置

```json
{
  "risk_control": {
    "max_position_per_stock": 0.2,    // 单只股票最大持仓比例
    "max_daily_loss": 0.05,            // 单日最大亏损比例
    "max_drawdown": 0.15,              // 最大回撤比例
    "min_cash_ratio": 0.1              // 最小现金比例
  }
}
```

## 三、使用步骤

### 3.1 安装依赖

#### Ptrade SDK
- 联系国金证券获取 Ptrade Python SDK
- 按照券商提供的文档安装

#### QMT SDK
```bash
pip install xtquant
```

### 3.2 运行实盘交易

#### 方式一：使用脚本运行

```bash
python scripts/run_live_trading.py
```

#### 方式二：在代码中使用

```python
from brokers.ptrade_adapter import PtradeAdapter
from brokers.qmt_adapter import QMTAdapter
from core.live_trading_engine import LiveTradingEngine
from strategies.examples.adaptive_momentum_a_v2 import AdaptiveMomentumStrategyA_V2
from config.config_manager import get_config_manager

# 加载配置
config_manager = get_config_manager()
broker_config = config_manager.load_config('broker_config.json')
gjzq_config = broker_config['gjzq']

# 创建适配器（选择 Ptrade 或 QMT）
adapter = PtradeAdapter({
    'host': gjzq_config['ptrade']['host'],
    'port': gjzq_config['ptrade']['port'],
    'account': gjzq_config['account'],
    'password': gjzq_config['password'],
    'account_id': gjzq_config['ptrade']['account_id'],
})

# 创建策略
strategy = AdaptiveMomentumStrategyA_V2(
    lookback_days=60,
    rebalance_interval=21,
    top_n=5
)
strategy.securities = ['000001.XSHE', '000002.XSHE']  # 设置股票池

# 创建并启动实盘交易引擎
engine = LiveTradingEngine(adapter, strategy)
engine.start()

# 每日运行（在交易时间调用）
engine.run_daily(datetime.now())

# 停止引擎
engine.stop()
```

## 四、策略开发

### 4.1 策略兼容性

策略代码在回测和实盘模式下**完全兼容**，无需修改：

```python
class MyStrategy(BaseStrategy):
    def handle_data(self, data: pd.DataFrame, date: datetime):
        # 回测模式：data 是历史日线数据
        # 实盘模式：data 是实时行情数据
        # 代码逻辑完全一致
        
        portfolio = self.context['portfolio']
        order_manager = self.context['order_manager']
        
        # 策略逻辑...
        if should_buy:
            order_manager.create_order('000001.XSHE', 100)
```

### 4.2 判断运行模式

```python
def handle_data(self, data: pd.DataFrame, date: datetime):
    if self.is_live_mode():
        # 实盘模式特殊处理
        adapter = self.context['adapter']
        # 可以获取实时行情、查询订单状态等
    else:
        # 回测模式
        pass
```

## 五、交易适配器接口

### 5.1 核心方法

所有交易适配器都实现以下接口：

```python
class TradingAdapter:
    def connect() -> bool                    # 连接券商系统
    def disconnect()                         # 断开连接
    def get_account_info() -> Dict           # 获取账户信息
    def get_positions() -> List[Dict]        # 获取持仓
    def place_order(...) -> str              # 下单
    def cancel_order(order_id) -> bool       # 撤单
    def get_order_status(order_id) -> Dict   # 查询订单状态
    def get_market_data(securities) -> Dict  # 获取实时行情
```

### 5.2 股票代码转换

系统自动处理股票代码格式转换：
- **JQData格式**: `000001.XSHE` (策略中使用)
- **券商格式**: `000001` (发送给券商)

## 六、实盘交易引擎功能

### 6.1 自动功能

- ✅ **持仓同步**: 自动同步券商持仓到投资组合
- ✅ **订单执行**: 自动执行策略生成的订单
- ✅ **风控检查**: 自动进行资金、持仓比例等风控检查
- ✅ **交易时间判断**: 自动判断是否在交易时间
- ✅ **数据格式转换**: 自动将实时行情转换为策略可用的格式

### 6.2 状态监控

```python
status = engine.get_status()
# 返回：
# {
#     'is_running': True,
#     'is_connected': True,
#     'account_info': {...},
#     'position_count': 5,
#     'pending_orders': 2
# }
```

## 七、注意事项

### 7.1 安全提示

1. **账号密码**: 已存储在 `config/broker_config.json`，请妥善保管
2. **生产环境**: 建议使用环境变量或加密存储密码
3. **权限控制**: 确保配置文件权限设置正确

### 7.2 测试建议

1. **模拟环境**: 先在模拟账户测试
2. **小资金验证**: 实盘前先用小资金验证
3. **日志监控**: 密切关注 `logs/live_trading.log`
4. **异常处理**: 确保异常情况下能及时停止交易

### 7.3 SDK安装

- **Ptrade SDK**: 需要联系国金证券获取，当前代码使用模拟模式
- **QMT SDK**: 安装 `xtquant` 包后，取消注释相关代码

## 八、故障排查

### 8.1 连接失败

- 检查网络连接
- 确认账号密码正确
- 检查券商服务器地址和端口
- 查看日志文件 `logs/live_trading.log`

### 8.2 下单失败

- 检查资金是否充足
- 确认股票代码格式正确
- 检查是否在交易时间
- 查看风控规则是否触发

### 8.3 SDK未安装

如果看到 "SDK 未安装" 的警告：
- **Ptrade**: 联系国金证券获取 SDK
- **QMT**: 运行 `pip install xtquant`

## 九、下一步

1. **安装SDK**: 获取并安装 Ptrade/QMT SDK
2. **测试连接**: 使用 `scripts/run_live_trading.py` 测试连接
3. **策略验证**: 在模拟环境验证策略逻辑
4. **实盘部署**: 小资金实盘验证
5. **监控告警**: 建立监控和告警机制

## 十、技术支持

- 查看日志: `logs/live_trading.log`
- 配置文件: `config/broker_config.json`
- 代码位置: `brokers/`, `core/live_trading_engine.py`

