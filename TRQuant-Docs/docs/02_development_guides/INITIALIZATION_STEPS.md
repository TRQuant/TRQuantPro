# BulletTrade 回测初始化步骤详解

## 📋 初始化流程

### 前端初始化（React 组件）
1. **WebSocket 连接**（~1-2秒）
   - 连接到 `ws://localhost:8765`
   - 注册为浏览器客户端
   - 状态：`连接中...` → `已连接`

### 回测初始化（点击"开始回测"后）

#### 步骤 1: 前端发送请求（0%）
- 前端发送 `run_bt_backtest` 消息
- 显示："初始化回测..."

#### 步骤 2: WebSocket 服务器接收（0%）
- 服务器立即广播进度消息
- 消息：`初始化 BulletTrade 回测...`

#### 步骤 3: 导入模块（0% → 2%）
- 执行：`from core.bullettrade import BulletTradeEngine, BTConfig`
- **耗时**：~0.30 秒
- 进度：2%
- 消息：`导入 BulletTrade 模块...`

#### 步骤 4: 创建配置（2% → 5%）
- 创建 `BTConfig` 对象
- **耗时**：<0.001 秒
- 进度：5%
- 消息：`创建回测配置...`

#### 步骤 5: 创建引擎（5% → 10%）
- 创建 `BulletTradeEngine` 对象
- 检查 BulletTrade CLI 可用性（`bullet-trade --version`）
- **耗时**：~0.67 秒（如果检查 CLI）
- 进度：8% → 10%
- 消息：`创建回测引擎（检查 CLI 可用性，最多3秒）...` → `回测引擎创建完成`

#### 步骤 6: 后续步骤（10% → 100%）
- 数据加载
- 策略执行
- 结果计算

## ⏱️ 总耗时估算

- **正常情况**：1-2 秒（模块导入 0.3s + CLI 检查 0.67s + 其他 0.1s）
- **最坏情况**：3-4 秒（如果 CLI 检查超时）

## 🔍 如果卡在"初始化"，可能原因

### 1. WebSocket 连接问题
- **症状**：前端显示"连接中..."或"未连接"
- **检查**：
  ```bash
  # 检查 WebSocket 服务器是否运行
  ps aux | grep websocket_server
  # 或
  curl http://localhost:8765
  ```
- **解决**：启动 WebSocket 服务器

### 2. 模块导入失败
- **症状**：后端日志显示 `ImportError`
- **检查**：
  ```bash
  cd /home/taotao/dev/QuantTest/TRQuant
  python3 -c "from core.bullettrade import BulletTradeEngine"
  ```
- **解决**：检查 Python 路径和依赖

### 3. BulletTrade CLI 检查超时
- **症状**：卡在"创建回测引擎"步骤
- **检查**：
  ```bash
  extension/venv/bin/bullet-trade --version
  ```
- **解决**：
  - 检查 BulletTrade 是否正确安装
  - 检查文件权限
  - 如果持续超时，可以修改代码跳过 CLI 检查

### 4. 文件路径问题
- **症状**：策略文件路径无效
- **检查**：确认策略文件路径正确
- **解决**：使用绝对路径或相对路径

### 5. 网络问题
- **症状**：如果使用 JQData，可能卡在数据连接
- **检查**：检查网络连接和 JQData 配置
- **解决**：配置 JQData 账号或使用本地数据

## 🛠️ 调试方法

### 1. 查看后端日志
```bash
# 如果 WebSocket 服务器在运行，查看日志
tail -f logs/websocket_server.log
```

### 2. 测试初始化步骤
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python3 -c "
from extension.python.bullettrade_bridge import get_bridge
bridge = get_bridge()

def progress(p, m, s=None, st=None):
    print(f'[{p}%] {m} ({s}/{st})')

bridge.set_progress_callback(progress)
result = bridge.run_bt_backtest({
    'strategy_path': 'test.py',
    'start_date': '2025-01-01',
    'end_date': '2025-01-07'
})
"
```

### 3. 检查 WebSocket 消息
- 打开浏览器开发者工具
- 查看 Network → WS 标签
- 查看发送和接收的消息

## ✅ 优化措施

1. **减少 CLI 检查超时**：从 5 秒减少到 3 秒
2. **超时容错**：如果 CLI 检查超时，假设可用并继续
3. **详细进度报告**：每个步骤都有明确的进度百分比
4. **错误处理**：如果引擎创建失败，尝试跳过 CLI 检查

## 📝 初始化步骤总结

| 步骤 | 进度 | 耗时 | 说明 |
|------|------|------|------|
| 发送请求 | 0% | <0.1s | 前端发送回测请求 |
| 导入模块 | 0-2% | ~0.3s | 导入 BulletTrade 模块 |
| 创建配置 | 2-5% | <0.001s | 创建回测配置对象 |
| 创建引擎 | 5-10% | ~0.67s | 创建引擎并检查 CLI |
| 后续步骤 | 10%+ | 可变 | 数据加载、策略执行等 |

**总初始化时间**：约 1-2 秒（正常情况下）
