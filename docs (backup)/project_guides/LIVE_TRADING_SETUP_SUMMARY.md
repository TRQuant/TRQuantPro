# 实盘交易系统集成总结

## 项目目标

整合国金证券的 **Ptrade** 和 **QMT** 两个交易通道，实现从回测到实盘的完整量化交易流程。

## 完成步骤总结

### ✅ 步骤1: 验证Python 3.12安装并配置环境
- **状态**: 已完成
- **操作**: 通过Windows商城安装Python 3.12.10
- **验证**: `py -3.12 --version` 确认安装成功
- **位置**: `C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe`

### ✅ 步骤2: 安装xtquant SDK到Python 3.12环境
- **状态**: 已完成
- **操作**: 
  - 创建Python 3.12虚拟环境: `C:\JQQuant\venv_qmt`
  - 复制xtquant_241014到虚拟环境
  - 设置正确的pyd文件（cp312版本）
- **验证**: `import xtquant.xtdata`, `import xtquant.xttrader` 成功
- **关键文件**: 
  - `C:\JQQuant\xtquant_241014\xtquant\` (SDK源文件)
  - `C:\JQQuant\venv_qmt\Lib\site-packages\xtquant\` (安装位置)

### ✅ 步骤3: 测试xtquant导入和基本功能
- **状态**: 已完成
- **验证**: 
  - `xtquant` 模块导入成功
  - `xtquant.xtdata` 和 `xtquant.xttrader` 导入成功
  - `XtQuantTrader` 类可用
  - `StockAccount` 类型可用

### 🔄 步骤4: 更新QMT适配器使用真实SDK
- **状态**: 进行中
- **已完成**:
  - 修正 `XtQuantTrader` 初始化方式（使用 `XtQuantTrader(path, session)` 而非 `connect()`）
  - 更新账户信息查询使用 `StockAccount` 对象
  - 更新持仓查询接口
  - 设置正确的QMT路径: `D:\国金证券QMT交易端\userdata_mini`
- **待完善**:
  - 需要在实际QMT客户端登录后测试真实查询
  - 完善下单、撤单等交易接口
  - 处理QMT客户端未启动的情况

### ⏳ 步骤5: 测试QMT连接和实盘交易功能
- **状态**: 待测试
- **前置条件**:
  1. 启动QMT客户端 (`D:\国金证券QMT交易端`)
  2. 使用账号 8885019982 手动登录
  3. 确保QMT客户端保持运行
- **测试内容**:
  - 连接QMT SDK
  - 查询账户信息
  - 查询持仓
  - 获取实时行情
  - 下单功能（需谨慎测试）

### ⏳ 步骤6: 更新GUI和文档，总结完整流程
- **状态**: 进行中
- **已完成**:
  - GUI已添加"实盘交易"标签页
  - 支持选择Ptrade/QMT
  - 支持测试连接功能
  - 更新脚本使用Python 3.12虚拟环境
- **待完成**:
  - 完善Ptrade适配器（等待Ptrade SDK）
  - 添加实时监控界面
  - 完善文档说明

## 当前系统状态

### 已实现功能

1. **交易适配器框架** ✅
   - `brokers/trading_adapter.py` - 统一接口基类
   - `brokers/ptrade_adapter.py` - 国金Ptrade适配器（框架完成，等待SDK）
   - `brokers/qmt_adapter.py` - 国金QMT适配器（已集成真实SDK）

2. **实盘交易引擎** ✅
   - `core/live_trading_engine.py` - 完整的实盘交易引擎
   - 支持策略在回测和实盘间无缝切换
   - 自动持仓同步、订单执行、风控检查

3. **配置管理** ✅
   - `config/broker_config.json` - 存储账号信息
   - 账号: 8885019982
   - 密码: 已安全存储
   - Ptrade路径: `C:\gjzq\ptrade`
   - QMT路径: `D:\国金证券QMT交易端`

4. **GUI集成** ✅
   - "韬睿量化平台启动器"已添加"实盘交易"标签页
   - 支持选择券商类型
   - 支持测试连接
   - 自动使用Python 3.12虚拟环境运行QMT

### 运行方式

#### 方式1: 通过GUI
1. 打开"韬睿量化平台启动器"
2. 切换到"实盘交易"标签页
3. 选择"QMT（国金）"
4. 点击"测试连接"
5. 查看输出和日志

#### 方式2: 命令行
```bash
# 使用Python 3.12虚拟环境
cd C:\JQQuant
.\venv_qmt\Scripts\python.exe scripts\run_live_trading.py

# 或指定券商类型
$env:BROKER_OVERRIDE="qmt"
.\venv_qmt\Scripts\python.exe scripts\run_live_trading.py
```

#### 方式3: 批处理脚本
```bash
scripts\run_live_trading_qmt.bat
```

## 下一步操作

### 立即可以做的
1. **启动QMT客户端并登录**
   - 打开 `D:\国金证券QMT交易端`
   - 使用账号 8885019982 登录
   - 保持客户端运行

2. **测试QMT连接**
   - 在GUI中点击"测试连接"
   - 或运行 `.\venv_qmt\Scripts\python.exe scripts\run_live_trading.py`
   - 查看是否能获取真实账户信息

3. **获取Ptrade SDK**
   - 联系国金证券获取Ptrade Python SDK
   - 参考文档: http://180.169.107.9:7766/hub/help/api?weworkcfmcode
   - 安装后更新 `brokers/ptrade_adapter.py`

### 需要完善的功能
1. **实时监控界面** - 在GUI中显示持仓、订单、账户信息
2. **持续运行模式** - 支持策略持续运行而非单次测试
3. **异常处理和重连** - QMT客户端断开时的自动重连
4. **风控参数配置** - 在GUI中配置风控规则

## 重要文件位置

- **QMT SDK**: `C:\JQQuant\xtquant_241014\`
- **Python 3.12虚拟环境**: `C:\JQQuant\venv_qmt\`
- **配置文件**: `config/broker_config.json` (已加入.gitignore)
- **运行脚本**: `scripts/run_live_trading.py`
- **日志文件**: `logs/live_trading.log`
- **QMT客户端**: `D:\国金证券QMT交易端`
- **Ptrade客户端**: `C:\gjzq\ptrade`

## 注意事项

1. **QMT需要客户端运行**: 必须先启动QMT客户端并登录，SDK才能连接
2. **Python版本**: QMT SDK需要Python 3.12，已创建独立虚拟环境
3. **账号安全**: `broker_config.json` 包含敏感信息，已加入.gitignore
4. **测试建议**: 先在模拟环境或小资金测试，确认无误后再实盘

## 技术支持

- 查看日志: `logs/live_trading.log`
- QMT文档: `xtquant_241014/xtquant/doc/`
- Ptrade文档: http://180.169.107.9:7766/hub/help/api?weworkcfmcode


