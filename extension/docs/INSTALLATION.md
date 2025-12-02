# TRQuant Cursor Extension 安装指南

## 目录

1. [系统要求](#系统要求)
2. [Linux安装](#linux安装)
3. [Windows安装](#windows安装)
4. [验证安装](#验证安装)
5. [常见问题](#常见问题)

---

## 系统要求

### 软件依赖

| 软件 | 版本要求 | 说明 |
|------|----------|------|
| Cursor IDE | >= 0.40 | 或 VS Code >= 1.85 |
| Node.js | >= 18.x | 用于构建Extension |
| Python | >= 3.9 | 推荐3.10+ |
| npm | >= 9.x | Node包管理器 |

### Python包依赖

```
jqdatasdk>=1.8.0    # JQData数据源
akshare>=1.10.0     # AKShare数据源
pandas>=2.0.0       # 数据处理
numpy>=1.24.0       # 数值计算
pymongo>=4.0.0      # MongoDB连接
```

---

## Linux安装

### 1. 安装系统依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y nodejs npm python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install -y nodejs npm python3 python3-pip

# Arch Linux
sudo pacman -S nodejs npm python python-pip
```

### 2. 克隆项目

```bash
cd /home/$(whoami)/dev
git clone <repo-url> TRQuant
cd TRQuant
```

### 3. 安装Extension依赖

```bash
cd extension
npm install
```

### 4. 配置Python环境

```bash
# 创建虚拟环境（推荐）
cd ..
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

### 5. 构建Extension

```bash
cd extension
npm run compile
```

### 6. 安装到Cursor

**方法A：开发模式**
1. 打开Cursor
2. 按 `F5` 启动调试（会打开新窗口）
3. 在新窗口中使用Extension

**方法B：打包安装**
```bash
# 安装打包工具
npm install -g @vscode/vsce

# 打包
vsce package

# 在Cursor中安装
# Extensions → ⋯ → Install from VSIX
```

### 7. 配置Extension

在Cursor设置中添加：

```json
{
  "trquant.pythonPath": "/home/$(whoami)/dev/TRQuant/venv/bin/python",
  "trquant.serverHost": "127.0.0.1",
  "trquant.serverPort": 5000,
  "trquant.mcpEnabled": true
}
```

---

## Windows安装

### 1. 安装系统依赖

**Node.js**
1. 下载：https://nodejs.org/
2. 运行安装程序
3. 验证：`node --version`

**Python**
1. 下载：https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 验证：`python --version`

### 2. 克隆项目

```powershell
cd C:\Users\%USERNAME%\dev
git clone <repo-url> TRQuant
cd TRQuant
```

### 3. 安装Extension依赖

```powershell
cd extension
npm install
```

### 4. 配置Python环境

```powershell
# 创建虚拟环境
cd ..
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 5. 构建Extension

```powershell
cd extension
npm run compile
```

### 6. 安装到Cursor

**方法A：开发模式**
1. 打开Cursor
2. 按 `F5` 启动调试
3. 在新窗口中测试

**方法B：打包安装**
```powershell
npm install -g @vscode/vsce
vsce package
# 在Cursor中：Extensions → ⋯ → Install from VSIX
```

### 7. 配置Extension

```json
{
  "trquant.pythonPath": "C:\\Users\\%USERNAME%\\dev\\TRQuant\\venv\\Scripts\\python.exe",
  "trquant.serverHost": "127.0.0.1",
  "trquant.serverPort": 5000,
  "trquant.mcpEnabled": true
}
```

---

## 验证安装

### 1. 验证Extension加载

1. 打开Cursor
2. 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac/Linux)
3. 输入 "TRQuant"
4. 应该看到以下命令：
   - TRQuant: 获取市场状态
   - TRQuant: 获取投资主线
   - TRQuant: 推荐因子
   - TRQuant: 生成策略代码
   - ...

### 2. 验证Python后端

```bash
# Linux
cd /home/$(whoami)/dev/TRQuant
source venv/bin/activate
echo '{"action": "get_market_status", "params": {}}' | python extension/python/bridge.py

# Windows
cd C:\Users\%USERNAME%\dev\TRQuant
.\venv\Scripts\activate
echo {"action": "get_market_status", "params": {}} | python extension\python\bridge.py
```

应该返回类似：
```json
{
  "ok": true,
  "data": {
    "regime": "risk_on",
    "summary": "..."
  }
}
```

### 3. 验证MCP Server

```bash
# 启动MCP Server
python extension/python/mcp_server.py

# 另一个终端发送测试请求
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | nc localhost 5001
```

---

## 常见问题

### Q1: "Python not found" 错误

**解决方案：**
1. 检查Python是否安装：`python --version`
2. 检查配置的Python路径是否正确
3. Windows用户确认Python已添加到PATH

### Q2: Extension无法加载

**解决方案：**
1. 检查Node.js版本：`node --version`（需要>=18）
2. 重新安装依赖：`npm install`
3. 重新构建：`npm run compile`
4. 查看Cursor输出面板中的错误日志

### Q3: bridge.py 执行超时

**解决方案：**
1. 检查TRQuant Core是否正确安装
2. 检查MongoDB是否运行
3. 增加超时时间设置

### Q4: MCP Server无法连接

**解决方案：**
1. 检查`.cursor/mcp.json`配置是否正确
2. 重启Cursor
3. 检查端口是否被占用

### Q5: Windows路径问题

**解决方案：**
- 使用正斜杠：`C:/Users/...` 或
- 双反斜杠：`C:\\Users\\...`
- 避免路径中有空格

---

## 获取帮助

- GitHub Issues: <repo-url>/issues
- 文档: extension/docs/
- 日志: Cursor → Output → TRQuant

