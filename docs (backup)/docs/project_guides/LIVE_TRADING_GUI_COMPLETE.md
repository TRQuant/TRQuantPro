# 实盘交易GUI完整元素设计和功能说明

## 📋 目录
1. [界面整体布局](#界面整体布局)
2. [顶部控制栏](#顶部控制栏)
3. [左侧面板](#左侧面板)
4. [右侧面板](#右侧面板)
5. [底部日志面板](#底部日志面板)
6. [交互流程](#交互流程)
7. [数据格式说明](#数据格式说明)
8. [错误处理机制](#错误处理机制)

---

## 界面整体布局

### 布局结构
```
┌──────────────────────────────────────────────────────────────────────────────┐
│  实盘交易管理                                                                 │
│  模块 3：实盘交易管理（连接券商、查看账户/持仓、下单、订单管理）              │
├──────────────────────────────────────────────────────────────────────────────┤
│  [顶部控制栏：券商选择、连接状态、操作按钮]                                  │
├──────────────────────────────────┬───────────────────────────────────────────┤
│  左侧面板 (50%)                  │  右侧面板 (50%)                           │
│  ┌─ 账户信息 ─────────────────┐ │  ┌─ 持仓 ───────────────────────────┐    │
│  │ 总资产: 1,000,000.00       │ │  │ 代码    数量  成本价 当前价 市值 │    │
│  │ 可用资金: 500,000.00       │ │  │ 000001  1000  10.00  10.50  10500│    │
│  │ 持仓市值: 500,000.00       │ │  │ ...                              │    │
│  │ 冻结资金: 0.00             │ │  └──────────────────────────────────┘    │
│  └────────────────────────────┘ │  ┌─ 订单 ───────────────────────────┐    │
│  ┌─ 下单 ─────────────────────┐ │  │ 订单ID  代码  方向 数量 价格 状态│    │
│  │ 股票代码: [000001.XSHE]   │ │  │ QMT_xxx 000001 买入 100  10.00 待成交│
│  │ 数量:     [100]            │ │  │ ...                              │    │
│  │ 价格类型: [市价▼]          │ │  └──────────────────────────────────┘    │
│  │ 限价:     [0.00]           │ │                                          │
│  │ [买入] [卖出]              │ │                                          │
│  └────────────────────────────┘ │                                          │
└──────────────────────────────────┴───────────────────────────────────────────┘
│  ┌─ 交易日志 ───────────────────────────────────────────────────────────┐  │
│  │ [16:30:18] 正在连接 QMT...                                             │  │
│  │ [16:30:19] QMT连接成功                                                  │  │
│  │ [16:30:20] 数据刷新完成                                                 │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 布局参数
- **总宽度**: 920px（自适应）
- **总高度**: 640px（自适应）
- **左右面板比例**: 1:1
- **顶部控制栏高度**: 自动
- **底部日志高度**: 固定约200px

---

## 顶部控制栏

### 元素列表

| 元素 | 类型 | 位置 | 宽度 | 功能 | 状态联动 |
|------|------|------|------|------|----------|
| "券商通道"标签 | Label | row=0, col=0 | 自动 | 静态文本 | - |
| 券商选择下拉框 | Combobox | row=0, col=1 | 18字符 | 选择QMT/Ptrade | 始终启用 |
| "连接状态:"标签 | Label | row=0, col=2 | 自动 | 静态文本 | - |
| 连接状态指示 | Label | row=0, col=3 | 自动 | 显示状态 | 根据`is_connected`变化颜色 |
| 连接按钮 | Button | row=0, col=4 | 12字符 | 连接券商 | 连接中/已连接时禁用 |
| 断开按钮 | Button | row=0, col=5 | 12字符 | 断开连接 | 未连接时禁用 |
| 刷新数据按钮 | Button | row=0, col=6 | 12字符 | 刷新数据 | 未连接时禁用 |

### 详细说明

#### 1. 券商选择下拉框
```python
self.broker_combo = ttk.Combobox(control_frame, state="readonly", width=18)
self.broker_combo["values"] = ["Ptrade（国金）", "QMT（国金）"]
self.broker_combo.current(1)  # 默认QMT
```
- **选项**: "Ptrade（国金）", "QMT（国金）"
- **默认值**: QMT（国金）
- **状态**: 始终可编辑
- **事件**: 无特殊事件处理

#### 2. 连接状态指示
```python
self.connection_status = tk.StringVar(value="未连接")
self.status_indicator = ttk.Label(..., textvariable=self.connection_status, 
                                 foreground="red", font=("Microsoft YaHei", 11, "bold"))
```
- **可能值**: "未连接", "已连接", "连接失败"
- **颜色**: 
  - 未连接/连接失败: 红色 (`foreground="red"`)
  - 已连接: 绿色 (`foreground="green"`)
- **字体**: Microsoft YaHei, 11pt, 粗体

#### 3. 连接按钮
```python
self.connect_btn = ttk.Button(..., text="连接", command=self._connect_broker, width=12)
```
- **点击事件**: `_connect_broker()`
- **执行流程**:
  1. 禁用按钮
  2. 显示"正在连接..."
  3. 后台线程调用`trading_helper.py --action connect`
  4. 成功: `_on_connected()` → 启用断开/刷新/买卖按钮
  5. 失败: `_on_connect_failed()` → 恢复连接按钮

#### 4. 断开按钮
```python
self.disconnect_btn = ttk.Button(..., text="断开", command=self._disconnect_broker, 
                                 width=12, state="disabled")
```
- **点击事件**: `_disconnect_broker()`
- **执行流程**:
  1. 设置`is_connected = False`
  2. 更新状态为"未连接"
  3. 禁用断开/刷新/买卖按钮
  4. 启用连接按钮
  5. 清空所有交易数据

#### 5. 刷新数据按钮
```python
self.refresh_btn = ttk.Button(..., text="刷新数据", command=self._refresh_trading_data, 
                             width=12, state="disabled")
```
- **点击事件**: `_refresh_trading_data()`
- **执行流程**:
  1. 禁用刷新按钮
  2. 后台线程调用`trading_helper.py --action account`和`--action positions`
  3. 更新账户信息和持仓列表
  4. 启用刷新按钮
  5. 记录日志

---

## 左侧面板

### 1. 账户信息面板

#### 布局
```python
account_box = ttk.LabelFrame(left_panel, text="账户信息", padding=10)
self.account_info_text = tk.Text(account_box, height=6, width=40, state="disabled",
                                bg="#fdfaf2", font=("Consolas", 10))
```

#### 显示内容
```
总资产: 1,000,000.00
可用资金: 500,000.00
持仓市值: 500,000.00
冻结资金: 0.00
```

#### 数据字段
| 字段 | 来源 | 格式 | 说明 |
|------|------|------|------|
| total_asset | `get_account_info()` | 千分位，2位小数 | 总资产 |
| cash | `get_account_info()` | 千分位，2位小数 | 可用资金 |
| market_value | `get_account_info()` | 千分位，2位小数 | 持仓市值 |
| frozen_cash | `get_account_info()` | 千分位，2位小数 | 冻结资金 |

#### 更新时机
- 连接成功后自动刷新
- 点击"刷新数据"按钮
- 下单成功后自动刷新

### 2. 下单面板

#### 布局
```python
order_box = ttk.LabelFrame(left_panel, text="下单", padding=10)
order_form = ttk.Frame(order_box)  # 表单容器
order_actions = ttk.Frame(order_box)  # 按钮容器
```

#### 表单字段

##### 股票代码输入框
```python
self.order_code_entry = ttk.Entry(order_form, width=20, font=("Microsoft YaHei", 10))
self.order_code_entry.insert(0, "000001.XSHE")  # 默认值
```
- **格式要求**: JQData格式（`000001.XSHE`, `600000.XSHG`）
- **验证**: 非空检查
- **快速填入**: 双击持仓自动填入

##### 数量输入框
```python
self.order_amount_entry = ttk.Entry(order_form, width=20, font=("Microsoft YaHei", 10))
self.order_amount_entry.insert(0, "100")  # 默认值
```
- **格式要求**: 正整数
- **验证**: 
  - 非空检查
  - 必须 > 0
  - 卖出时检查持仓数量
- **快速填入**: 双击持仓自动填入（100股或持仓10%）

##### 价格类型下拉框
```python
self.order_type_combo = ttk.Combobox(order_form, state="readonly", width=18)
self.order_type_combo["values"] = ["市价", "限价"]
self.order_type_combo.current(0)  # 默认市价
self.order_type_combo.bind("<<ComboboxSelected>>", self._on_order_type_changed)
```
- **选项**: "市价", "限价"
- **默认值**: "市价"
- **事件**: 切换时调用`_on_order_type_changed()`
  - 市价: 禁用限价输入，清空为"0.00"
  - 限价: 启用限价输入

##### 限价输入框
```python
self.order_price_entry = ttk.Entry(order_form, width=20, state="disabled")
self.order_price_entry.insert(0, "0.00")
```
- **状态**: 市价单时禁用，限价单时启用
- **格式要求**: 正浮点数
- **验证**: 限价单时必须 > 0

#### 操作按钮

##### 买入按钮
```python
self.buy_btn = ttk.Button(order_actions, text="买入", style="Miyazaki.TButton",
                          command=lambda: self._place_order("buy"), width=12, state="disabled")
```
- **样式**: 主要按钮（蓝色）
- **点击事件**: `_place_order("buy")`
- **验证**:
  1. 检查连接状态
  2. 检查必填字段
  3. 检查数量格式
  4. 检查限价（如适用）
- **执行**: 调用`trading_helper.py --action place_order --amount <正数>`

##### 卖出按钮
```python
self.sell_btn = ttk.Button(order_actions, text="卖出", style="Miyazaki.Secondary.TButton",
                          command=lambda: self._place_order("sell"), width=12, state="disabled")
```
- **样式**: 次要按钮（灰色）
- **点击事件**: `_place_order("sell")`
- **额外验证**: 检查持仓数量是否足够
- **执行**: 调用`trading_helper.py --action place_order --amount <负数>`

#### 下单流程
```
用户填写/双击填入 → 点击买入/卖出
    ↓
验证必填字段和格式
    ↓
卖出时检查持仓
    ↓
禁用按钮，显示"正在下单..."
    ↓
后台线程调用trading_helper.py
    ↓
成功: _on_order_placed() → 添加到订单列表 → 刷新数据
失败: _on_order_failed() → 显示错误 → 恢复按钮
```

---

## 右侧面板

### 1. 持仓列表

#### 布局
```python
position_box = ttk.LabelFrame(right_panel, text="持仓", padding=8)
self.position_tree = ttk.Treeview(position_tree_frame, 
                                 columns=("code", "amount", "cost", "current", "value"),
                                 show="headings", height=8)
```

#### 列定义
| 列名 | 字段 | 宽度 | 对齐 | 格式 | 说明 |
|------|------|------|------|------|------|
| 代码 | code | 100px | 左 | 字符串 | JQData格式 |
| 数量 | amount | 80px | 右 | 整数 | 持仓数量 |
| 成本价 | cost | 80px | 右 | 2位小数 | 平均成本价 |
| 当前价 | current | 80px | 右 | 2位小数 | 当前市场价格 |
| 市值 | value | 100px | 右 | 千分位，2位小数 | 持仓市值 |

#### 数据来源
- **API**: `trading_helper.py --action positions`
- **返回格式**:
```json
{
  "success": true,
  "data": [
    {
      "code": "000001.XSHE",
      "amount": 1000,
      "cost": 10.00,
      "current": 10.50,
      "value": 10500.00
    }
  ]
}
```

#### 交互功能
- **双击事件**: `_on_position_double_click(event)`
  - 自动填入股票代码
  - 自动填入默认数量（100股或持仓10%）

### 2. 订单列表

#### 布局
```python
order_box2 = ttk.LabelFrame(right_panel, text="订单", padding=8)
self.order_tree = ttk.Treeview(order_tree_frame,
                               columns=("code", "direction", "amount", "price", "status", "filled"),
                               show="headings", height=8)
```

#### 列定义
| 列名 | 字段 | 宽度 | 对齐 | 格式 | 说明 |
|------|------|------|------|------|------|
| 订单ID | #0 (text) | 120px | 左 | 字符串 | 券商返回的订单号 |
| 代码 | code | 100px | 左 | 字符串 | JQData格式 |
| 方向 | direction | 60px | 中 | 中文 | 买入/卖出 |
| 数量 | amount | 80px | 右 | 整数 | 委托数量 |
| 价格 | price | 80px | 右 | 2位小数/市价 | 委托价格 |
| 状态 | status | 80px | 中 | 中文 | 待成交/部分成交/已成交/已撤销/已拒绝 |
| 已成交 | filled | 80px | 右 | 整数 | 已成交数量 |

#### 状态映射
| SDK状态 | 显示文本 | 可撤单 |
|---------|----------|--------|
| pending | 待成交 | ✅ |
| partially_filled | 部分成交 | ✅ |
| filled | 已成交 | ❌ |
| cancelled | 已撤销 | ❌ |
| rejected | 已拒绝 | ❌ |

#### 交互功能

##### 右键菜单
```python
self.order_context_menu = tk.Menu(self, tearoff=0)
self.order_context_menu.add_command(label="撤单", command=self._cancel_selected_order)
self.order_tree.bind("<Button-3>", self._show_order_context_menu)
```
- **显示条件**: 仅"待成交"和"部分成交"订单
- **操作**: 点击"撤单" → 确认 → 调用`trading_helper.py --action cancel_order`

##### 双击事件
```python
self.order_tree.bind("<Double-1>", self._on_order_double_click)
```
- **功能**: 显示订单详情弹窗
- **内容**: 订单ID、代码、方向、数量、价格、状态、已成交

---

## 底部日志面板

### 布局
```python
log_box = ttk.LabelFrame(live_frame, text="交易日志", padding=8)
self.live_output = tk.Text(log_box, height=8, width=90, state="disabled",
                           bg="#fdfaf2", fg=PALETTE["text_primary"],
                           relief="flat", wrap="word", font=("Consolas", 9))
```

### 显示内容
- **格式**: `[HH:MM:SS] 操作描述`
- **示例**:
```
[16:30:18] 正在连接 QMT...
[16:30:19] QMT连接成功
[16:30:20] 数据刷新完成
[16:30:25] 正在下单: 000001.XSHE 买入 100股
[16:30:26] 下单成功: 000001.XSHE 买入 100股, 订单ID: QMT_abc123
[16:30:30] 正在撤单: QMT_abc123
[16:30:31] 撤单成功: QMT_abc123
```

### 特性
- **自动滚动**: 新消息自动滚动到底部
- **字体**: Consolas 9pt（等宽字体）
- **只读**: 用户不可编辑
- **换行**: `wrap="word"` 自动换行

---

## 交互流程

### 完整连接流程
```
1. 用户选择券商通道
   ↓
2. 点击"连接"按钮
   ↓
3. GUI显示"正在连接..."，禁用连接按钮
   ↓
4. 后台线程: subprocess调用trading_helper.py --action connect
   ↓
5. trading_helper.py创建适配器并调用connect()
   ↓
6. 适配器连接SDK（QMT/Ptrade）
   ↓
7. 返回结果（JSON）
   ↓
8. GUI解析结果
   ├─ 成功: _on_connected()
   │   ├─ 更新状态为"已连接"（绿色）
   │   ├─ 禁用连接按钮
   │   ├─ 启用断开/刷新/买卖按钮
   │   └─ 自动刷新数据
   └─ 失败: _on_connect_failed()
       ├─ 更新状态为"连接失败"（红色）
       ├─ 启用连接按钮
       └─ 显示错误弹窗
```

### 完整下单流程
```
1. 用户填写/双击填入下单信息
   ↓
2. 点击"买入"或"卖出"按钮
   ↓
3. 验证
   ├─ 检查连接状态
   ├─ 检查必填字段（代码、数量）
   ├─ 检查数量格式（正整数）
   ├─ 卖出时检查持仓数量
   └─ 限价单检查价格（>0）
   ↓
4. 禁用买卖按钮，显示"正在下单..."
   ↓
5. 后台线程: subprocess调用trading_helper.py --action place_order
   ↓
6. trading_helper.py创建适配器并调用place_order()
   ↓
7. 适配器调用SDK下单接口
   ↓
8. 返回订单ID（JSON）
   ↓
9. GUI解析结果
   ├─ 成功: _on_order_placed()
   │   ├─ 添加到订单列表
   │   ├─ 记录日志
   │   ├─ 自动刷新数据
   │   └─ 恢复按钮
   └─ 失败: _on_order_failed()
       ├─ 记录错误日志
       ├─ 显示错误弹窗
       └─ 恢复按钮
```

### 完整撤单流程
```
1. 用户在订单列表中右键点击订单
   ↓
2. 选择"撤单"菜单项
   ↓
3. 检查订单状态（仅待成交/部分成交可撤）
   ↓
4. 确认弹窗
   ↓
5. 后台线程: subprocess调用trading_helper.py --action cancel_order
   ↓
6. trading_helper.py创建适配器并调用cancel_order()
   ↓
7. 适配器调用SDK撤单接口
   ↓
8. 返回结果（JSON）
   ↓
9. GUI解析结果
   ├─ 成功: _on_order_cancelled()
   │   ├─ 更新订单状态为"已撤销"
   │   ├─ 记录日志
   │   └─ 刷新数据
   └─ 失败: _on_cancel_failed()
       ├─ 记录错误日志
       └─ 显示错误弹窗
```

---

## 数据格式说明

### 股票代码格式
- **JQData格式**: `000001.XSHE`, `600000.XSHG`
- **市场后缀**:
  - 深市: `.XSHE` (00xxxx, 30xxxx)
  - 沪市: `.XSHG` (60xxxx, 68xxxx)
- **转换**: 适配器自动转换券商格式

### 数量格式
- **输入**: 正整数（字符串）
- **内部**: 整数（买入为正，卖出为负）
- **显示**: 绝对值

### 价格格式
- **输入**: 浮点数（字符串）
- **显示**: 2位小数
- **市价**: 显示"市价"文本

### 金额格式
- **显示**: 千分位，2位小数
- **示例**: `1,000,000.00`

---

## 错误处理机制

### 连接错误
- **QMT环境不存在**: 提示"QMT虚拟环境不存在，请先安装xtquant SDK"
- **连接超时**: 10秒超时，显示"连接超时"
- **SDK错误**: 显示SDK返回的错误信息
- **JSON解析失败**: 显示原始输出

### 下单错误
- **未连接**: 提示"请先连接券商"
- **必填字段**: 提示"请填写股票代码和数量"
- **数量格式**: 提示"数量或价格格式错误"
- **持仓不足**: 提示"持仓不足，当前持仓: X股"
- **下单失败**: 显示SDK返回的错误信息

### 撤单错误
- **未选择订单**: 提示"请选择要撤销的订单"
- **订单状态**: 提示"订单状态为X，无法撤单"
- **撤单失败**: 显示SDK返回的错误信息

### 通用错误处理
- **超时**: 所有subprocess调用设置超时（10-15秒）
- **线程安全**: UI更新使用`self.after(0, callback)`
- **日志记录**: 所有错误记录到交易日志
- **用户提示**: 关键错误使用messagebox弹窗

---

## 总结

本GUI实现了完整的实盘交易管理功能，包括：
- ✅ 6个主要功能模块
- ✅ 20+个交互控件
- ✅ 完整的错误处理
- ✅ 用户友好的交互设计
- ✅ 详细的操作日志
- ✅ 线程安全的数据更新

所有功能已完整实现，代码结构清晰，可直接投入使用。


