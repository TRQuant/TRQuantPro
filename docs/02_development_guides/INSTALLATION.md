# TRQuant Cursor Extension 安装与使用指南

> 韬睿量化 - A股AI量化投资助手

## 📋 目录

1. [系统要求](#系统要求)
2. [快速安装](#快速安装)
3. [开发者安装](#开发者安装)
4. [首次使用](#首次使用)
5. [功能详解](#功能详解)
6. [调试指南](#调试指南)
7. [常见问题](#常见问题)

---

## 系统要求

### 必需环境

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Cursor IDE | ≥ 0.40.0 | 或 VS Code ≥ 1.85.0 |
| Node.js | ≥ 18.0 | 用于编译扩展 |
| Python | ≥ 3.9 | 后端运行环境 |
| npm | ≥ 9.0 | 包管理器 |

### Python依赖

```bash
# 核心依赖
pip install pandas numpy akshare pymongo

# 可选：JQData（需要账号）
pip install jqdatasdk
```

### 检查环境

```bash
# 检查Node.js
node --version   # 应显示 v18.x.x 或更高

# 检查Python
python --version # 应显示 3.9.x 或更高

# 检查npm
npm --version    # 应显示 9.x.x 或更高
```

---

## 快速安装

### 方式1：从VSIX安装（推荐）

```bash
# 1. 下载最新的.vsix文件
# 位置：extension/trquant-cursor-extension-0.1.0.vsix

# 2. 在Cursor中安装
cursor --install-extension trquant-cursor-extension-0.1.0.vsix

# 3. 重启Cursor
```

### 方式2：从命令面板安装

1. 打开Cursor
2. 按 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
3. 输入 `Extensions: Install from VSIX...`
4. 选择 `trquant-cursor-extension-0.1.0.vsix` 文件
5. 重启Cursor

---

## 开发者安装

### 步骤1：克隆代码

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
```

### 步骤2：安装依赖

```bash
# 安装Node.js依赖
npm install

# 如果遇到权限问题（Linux/Mac）
sudo npm install
```

### 步骤3：编译TypeScript

```bash
# 开发模式（监听变化自动编译）
npm run watch

# 或生产模式（一次性编译）
npm run compile
```

### 步骤4：安装Python依赖

```bash
# 进入Python目录
cd python

# 安装依赖
pip install -r requirements.txt

# 或手动安装
pip install pandas numpy akshare pymongo
```

### 步骤5：调试运行

```bash
# 方式A：使用Cursor调试
# 1. 在Cursor中打开extension文件夹
# 2. 按F5启动调试
# 3. 新窗口中测试扩展

# 方式B：命令行启动开发主机
code --extensionDevelopmentPath=/home/taotao/dev/QuantTest/TRQuant/extension
```

### 步骤6：打包发布

```bash
# 安装打包工具
npm install -g @vscode/vsce

# 打包为.vsix
npx @vscode/vsce package --allow-missing-repository

# 生成文件：trquant-cursor-extension-0.1.0.vsix
```

---

## 首次使用

### 1. 欢迎界面

安装后首次启动，会自动显示欢迎界面：

```
┌─────────────────────────────────────────────────┐
│  📊 TRQuant 韬睿量化                              │
│  A股AI量化投资助手                                │
│                                                 │
│  [➕ 新建量化项目]    [📂 打开已有项目]            │
│                                                 │
│  工作流: 市场分析 → 主线识别 → 因子选择           │
│          → 策略生成 → 回测验证                   │
│                                                 │
│  支持: A股 ✅  PTrade ✅  QMT ✅                  │
└─────────────────────────────────────────────────┘
```

### 2. 创建第一个项目

点击 **新建量化项目** 或按 `Ctrl+Shift+P` 输入 `TRQuant: 新建量化项目`

#### 创建向导步骤：

1. **选择位置**：选择项目存放的文件夹
2. **项目名称**：输入项目名（如：`my_first_strategy`）
3. **策略模板**：选择策略类型
   - 多因子选股（推荐新手）
   - 动量成长
   - 价值投资
   - 市场中性
   - 自定义
4. **目标平台**：选择执行平台
   - PTrade（国金证券）
   - QMT（迅投）
5. **股票池**：选择初始股票范围
   - 沪深300
   - 中证500
   - 创业板指
   - 自定义
6. **回测周期**：设置回测时间范围
7. **风控参数**：设置止损止盈等参数

### 3. 项目结构

创建完成后，项目结构如下：

```
my_first_strategy/
├── .trquant/
│   └── project.json      # 项目配置
├── strategies/
│   └── main_strategy.py  # 策略代码
├── data/                 # 数据目录
├── backtest/             # 回测结果
├── reports/              # 分析报告
├── config/
│   └── backtest.json     # 回测配置
├── README.md
└── .cursorrules          # AI规则
```

---

## 功能详解

### 侧边栏面板

安装后，左侧会出现TRQuant图标，点击打开侧边栏：

| 面板 | 功能 |
|------|------|
| 📁 项目资源 | TreeView显示项目文件结构 |
| 🌐 市场状态 | 当前市场风格和指数走势 |
| 🎯 投资主线 | 热门板块和投资机会 |
| 📜 策略管理 | 策略文件列表 |
| 🧪 回测历史 | 历史回测记录和结果 |

### 命令列表

按 `Ctrl+Shift+P` 后输入 `TRQuant` 查看所有命令：

| 命令 | 功能 |
|------|------|
| `TRQuant: 打开主界面` | 打开Dashboard |
| `TRQuant: 显示欢迎页面` | 显示欢迎引导 |
| `TRQuant: 新建量化项目` | 创建新项目 |
| `TRQuant: 获取市场状态` | 分析当前市场 |
| `TRQuant: 获取投资主线` | 识别热门板块 |
| `TRQuant: 推荐因子` | 智能因子推荐 |
| `TRQuant: 生成策略代码` | AI生成策略 |
| `TRQuant: 运行回测` | 执行回测 |
| `TRQuant: 对比回测结果` | 多策略对比 |
| `TRQuant: 编辑项目配置` | 修改项目设置 |
| `TRQuant: 验证配置` | 检查配置正确性 |
| `TRQuant: 导出配置` | 导出配置文件 |
| `TRQuant: 导入配置` | 导入配置文件 |

### 使用AI生成策略

1. 打开Dashboard或按命令 `TRQuant: 生成策略代码`
2. 选择策略类型和目标平台
3. 等待AI生成代码
4. 代码自动保存到 `strategies/` 目录
5. 可以在编辑器中修改优化

### 运行回测

1. 打开策略文件（.py）
2. 按命令 `TRQuant: 运行回测`
3. 配置回测参数（日期、资金、股票池）
4. 选择数据源（AKShare免费 / JQData付费）
5. 等待回测完成
6. 查看结果报告

---

## 调试指南

### 方式1：F5调试（推荐）

1. 在Cursor中打开 `extension` 文件夹
2. 确保 `.vscode/launch.json` 存在
3. 按 `F5` 启动调试
4. 新开的Cursor窗口中测试扩展

### 方式2：命令行调试

```bash
# Linux/Mac
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run compile
code --extensionDevelopmentPath=$(pwd)

# Windows
cd C:\path\to\TRQuant\extension
npm run compile
code --extensionDevelopmentPath=%cd%
```

### 方式3：查看日志

1. 在Cursor中按 `Ctrl+Shift+U` 打开输出面板
2. 下拉选择 `TRQuant` 通道
3. 查看扩展日志

### Python后端调试

```bash
# 测试bridge.py
cd /home/taotao/dev/QuantTest/TRQuant/extension/python
echo '{"action": "health_check", "params": {}}' | python bridge.py

# 测试回测引擎
python -c "from tools.backtest_engine import BacktestEngine; print('OK')"
```

### 常见调试命令

```bash
# 重新编译
npm run compile

# 清理并重新安装
rm -rf node_modules dist
npm install
npm run compile

# 检查TypeScript错误
npx tsc --noEmit

# 查看打包内容
npx @vscode/vsce ls
```

---

## 常见问题

### Q1: 安装后看不到侧边栏图标

**解决方案**：
1. 重启Cursor
2. 检查扩展是否启用：`Ctrl+Shift+X` → 搜索 `TRQuant`
3. 手动激活：`Ctrl+Shift+P` → `TRQuant: 打开主界面`

### Q2: Python后端连接失败

**解决方案**：
```bash
# 检查Python路径
which python  # Linux/Mac
where python  # Windows

# 设置扩展配置
# Cursor设置 → 搜索 trquant.pythonPath
# 设置为你的Python路径
```

### Q3: 回测没有数据

**解决方案**：
1. 确保网络连接正常
2. 检查AKShare是否可用：
   ```bash
   python -c "import akshare; print(akshare.__version__)"
   ```
3. 尝试更换数据源或日期范围

### Q4: 策略生成失败

**解决方案**：
1. 检查MCP Server是否启用
2. 确保Cursor AI功能正常
3. 查看输出日志排查错误

### Q5: Windows安装遇到权限问题

**解决方案**：
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
npm install
```

---

## 技术支持

- **GitHub Issues**: [提交问题](https://github.com/trquant/issues)
- **文档**: `/docs/` 目录下的所有文档

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 0.1.0 | 2024-12 | 首个版本，支持A股PTrade/QMT |

---

## 许可证

MIT License
