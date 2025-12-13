# JQQuant GUI 使用指南

## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues







## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues





## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues


## 快速启动

### 方法1: 命令行启动

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动GUI
python JQQuant.py
```

### 方法2: 使用启动脚本

```bash
./start_gui.sh
```

### 方法3: 双击启动 (Linux桌面)

1. 复制 `JQQuant.desktop` 到桌面
2. 双击图标启动

## 界面概览

### 侧边栏导航

- 🚀 **系统控制** - 系统启动/停止、状态监控
- 📝 **策略开发** - 策略代码编辑、参数配置
- 📊 **策略回测** - 历史数据回测、结果分析
- 💹 **实盘交易** - 券商连接、实盘交易
- 📋 **系统日志** - 查看运行日志

## 功能模块

### 1. 系统控制

**功能:**
- 启动/停止系统
- 系统检查（配置、模块、网络）
- 聚宽API连接状态
- 系统日志查看

**使用步骤:**
1. 点击"系统检查"验证环境
2. 点击"启动系统"连接聚宽API
3. 查看状态卡片确认连接成功

### 2. 策略开发

**功能:**
- 浏览现有策略
- 创建新策略
- 代码编辑（语法高亮）
- 参数配置
- 策略保存

**使用步骤:**
1. 从左侧列表选择策略或点击"新建策略"
2. 在代码编辑器中编写策略
3. 切换到"参数配置"标签调整参数
4. 点击"保存策略"保存更改

**策略模板:**
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Strategy")
    
    def handle_data(self, data, date):
        # 交易逻辑
        pass
```

### 3. 策略回测

**功能:**
- 选择回测策略
- 设置回测时间范围
- 配置初始资金和手续费
- 选择股票池
- 查看回测结果
- 导出结果报告

**使用步骤:**
1. 选择要回测的策略
2. 设置开始/结束日期
3. 配置资金和手续费参数
4. 从股票池选择股票
5. 点击"开始回测"
6. 查看结果卡片和详细报告

**注意:**
- 日期范围受聚宽账号权限限制
- 建议先用少量股票测试

### 4. 实盘交易

**支持的券商:**
- 国金PTrade
- 国金QMT
- 更多券商开发中...

**功能:**
- 券商连接配置
- 账户资金查看
- 持仓管理
- 手动下单
- 策略自动交易

**使用步骤:**
1. 选择券商卡片
2. 输入账号、密码、服务器地址
3. 点击"连接"建立连接
4. 查看账户信息和持仓
5. 手动下单或启动策略交易

**⚠️ 警告:**
实盘交易涉及真实资金，请务必：
- 在模拟环境充分测试策略
- 设置合理的止损止盈
- 控制仓位风险

### 5. 系统日志

**功能:**
- 查看系统运行日志
- 按级别筛选（DEBUG/INFO/WARNING/ERROR）
- 关键词搜索
- 自动刷新

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建策略 |
| Ctrl+Q | 退出程序 |

## 常见问题

### Q: 启动时报错 "No module named 'PyQt6'"

**解决方案:**
```bash
source venv/bin/activate
pip install PyQt6 pyqtgraph
```

### Q: 连接聚宽失败

**解决方案:**
1. 检查 `config/jqdata_config.json` 配置是否正确
2. 确认网络连接正常
3. 检查账号密码是否正确

### Q: 回测日期范围错误

**解决方案:**
聚宽账号有数据权限限制，请使用账号允许的日期范围。

### Q: 界面显示异常

**解决方案:**
```bash
# 设置DPI缩放
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python JQQuant.py
```

## 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 运行打包脚本
python build_app.py
```

打包后的文件在 `dist/JQQuant/` 目录下。

## 开发说明

### 目录结构

```
gui/
├── __init__.py
├── main_window.py      # 主窗口
├── styles/             # 样式主题
│   ├── __init__.py
│   └── theme.py
├── widgets/            # 功能面板
│   ├── __init__.py
│   ├── system_panel.py
│   ├── strategy_panel.py
│   ├── backtest_panel.py
│   ├── trading_panel.py
│   └── log_viewer.py
├── dialogs/            # 对话框
│   └── __init__.py
└── resources/          # 资源文件
    └── __init__.py
```

### 添加新功能

1. 在 `gui/widgets/` 创建新的面板类
2. 在 `gui/main_window.py` 中添加导航按钮
3. 将面板添加到页面堆栈

## 联系支持

- 项目文档: `docs/ARCHITECTURE.md`
- 回测文档: `docs/BACKTEST_TEST_RESULTS.md`
- 问题反馈: GitHub Issues














