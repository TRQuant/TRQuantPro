# TRQuant Windows 安装与测试指南

适用场景：已在 Linux 侧打包/备份完成，将完整项目目录拷贝到 Windows（推荐路径如 `C:\trquant`，避免空格和超长路径），在 Windows 上安装依赖并测试 VS Code 扩展与 Python 模块。

## 环境要求
- Windows 10/11 64-bit
- Python 3.11 64-bit（安装时勾选 “Add Python to PATH”）
- Node.js 18 LTS（含 npm）
- Git（可选，便于后续提交）
- 可选：Anaconda/Miniconda（便于安装 TA-Lib 二进制）
- 如需从源构建 TA-Lib：安装 Visual Studio Build Tools，选择 C++ 构建工具

## 快速方案：使用自动脚本
1) 解压或复制项目到 `C:\trquant`（路径尽量短、无空格）。
2) 以 PowerShell 打开该目录：
   ```powershell
   cd C:\trquant
   # 允许当前会话执行脚本
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   # 虚拟环境方案（默认）
   .\scripts\install_windows.ps1 -ProjectPath C:\trquant
   # 若希望使用 conda 并自动安装 ta-lib，可加：
   # .\scripts\install_windows.ps1 -ProjectPath C:\trquant -UseConda
   ```
3) 完成后脚本会输出 VSIX 位置（若成功打包扩展）与安装结果摘要。

## 手动安装步骤（可替代脚本）
### 1. Python 依赖
```powershell
cd C:\trquant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
```

### 2. TA-Lib 处理（如 pip 安装失败）
- 优先使用 conda：
  ```powershell
  conda create -n trquant python=3.11 -y
  conda install -n trquant -c conda-forge ta-lib -y
  conda run -n trquant pip install --no-cache-dir -r requirements.txt --no-deps
  ```
- 或从 Christoph Gohlke 下载与 Python/平台匹配的 TA-Lib wheel，先 `pip install <wheel>` 再安装其余依赖。

### 3. Extension 后端依赖
```powershell
cd C:\trquant\extension
..\ .venv\Scripts\Activate.ps1   # 或 conda activate trquant
pip install --no-cache-dir -r requirements.txt
```

### 4. 构建 VS Code 扩展
```powershell
cd C:\trquant\extension
npm install
npm run compile
npx vsce package   # 生成 trquant-cursor-extension-*.vsix
```
在 VS Code：扩展视图 > ... > Install from VSIX，选择生成的文件。

### 5. 验证
- `python -c "import talib; print(talib.__version__)"`（若安装 TA-Lib）
- `pip show numpy pandas flask fastapi` 等确认安装
- `cd extension && npm test`（如有测试）或至少 `npm run compile`
- 在 VS Code 中打开命令面板运行 TRQuant 相关命令（如 “TRQuant: 量化工作台”）。

## 常见问题
- TA-Lib 安装失败：优先用 conda，或使用预编译 wheel；必要时安装 VS Build Tools（C++）后重试。
- 路径过长/含空格：放在 `C:\trquant` 等短路径；可启用 `git config --system core.longpaths true`。
- 编译缺少权限：PowerShell 需临时允许脚本执行（已在命令示例中给出）。







