# 韬睿量化 - 跨平台打包指南

## 📦 支持的平台和格式

| 平台 | 安装包格式 | 工具 |
|------|-----------|------|
| **Windows** | `.exe` 安装程序 | PyInstaller + Inno Setup |
| **macOS** | `.dmg` 磁盘映像 | PyInstaller + create-dmg |
| **Linux** | `.deb` / `.AppImage` | PyInstaller + dpkg/appimagetool |

---

## 🛠️ 准备工作

### 1. 安装打包依赖

```bash
# 进入项目目录
cd /home/taotao/.local/share/jqquant
source venv/bin/activate

# 安装 PyInstaller
pip install pyinstaller

# 安装图标转换工具（可选）
pip install Pillow
```

### 2. 准备应用图标

在 `gui/resources/icons/` 目录下放置：
- `app_icon.png` - 256x256 PNG 图标（必需）
- `app_icon.ico` - Windows 图标（自动生成）
- `app_icon.icns` - macOS 图标（自动生成）

---

## 🪟 Windows 打包

### 方法1：在 Windows 上打包（推荐）

```powershell
# 1. 克隆项目到 Windows
git clone https://github.com/your-repo/jqquant.git
cd jqquant

# 2. 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 4. 运行打包脚本
python packaging/build_all.py --platform windows

# 5. 使用 Inno Setup 生成安装程序
# 下载 Inno Setup: https://jrsoftware.org/isinfo.php
iscc packaging\windows\setup.iss
```

### 方法2：在 Linux 上交叉编译

```bash
# 使用 Wine + PyInstaller（不推荐，兼容性问题多）
# 建议使用 GitHub Actions 或 Windows VM
```

### 生成文件
- `dist/TaoRuiQuant_Setup_1.0.0_Windows.exe`

---

## 🍎 macOS 打包

### 在 macOS 上打包

```bash
# 1. 安装依赖
brew install create-dmg  # 可选，用于创建美观的 DMG

# 2. 运行打包脚本
python packaging/build_all.py --platform macos
```

### 代码签名（可选但推荐）

```bash
# 需要 Apple Developer 账号
codesign --deep --force --verify --verbose \
    --sign "Developer ID Application: Your Name" \
    dist/TaoRuiQuant.app

# 公证（macOS 10.15+）
xcrun notarytool submit dist/TaoRuiQuant.dmg \
    --apple-id "your@email.com" \
    --password "app-specific-password" \
    --team-id "TEAM_ID"
```

### 生成文件
- `dist/TaoRuiQuant.app` - 应用程序
- `dist/TaoRuiQuant_1.0.0_macOS.dmg` - 安装包

---

## 🐧 Linux 打包

### DEB 包（Debian/Ubuntu）

```bash
# 1. 安装依赖
sudo apt install dpkg-dev

# 2. 运行打包脚本
python packaging/build_all.py --platform linux

# 3. 生成 DEB 包
cd packaging/linux
bash create_deb.sh
```

### AppImage（通用 Linux）

```bash
# 1. 运行打包脚本
python packaging/build_all.py --platform linux

# 2. 生成 AppImage
cd packaging/linux
bash create_appimage.sh
```

### 生成文件
- `dist/TaoRuiQuant_1.0.0_Linux_amd64.deb`
- `dist/TaoRuiQuant-1.0.0-x86_64.AppImage`

### 安装 DEB 包

```bash
sudo dpkg -i TaoRuiQuant_1.0.0_Linux_amd64.deb
# 或
sudo apt install ./TaoRuiQuant_1.0.0_Linux_amd64.deb
```

### 运行 AppImage

```bash
chmod +x TaoRuiQuant-1.0.0-x86_64.AppImage
./TaoRuiQuant-1.0.0-x86_64.AppImage
```

---

## 🔄 使用 GitHub Actions 自动构建

创建 `.github/workflows/build.yml`：

```yaml
name: Build Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: python packaging/build_all.py --platform windows
      - name: Create installer
        run: iscc packaging\windows\setup.iss
      - uses: actions/upload-artifact@v4
        with:
          name: windows-installer
          path: dist/*.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
          brew install create-dmg
      - name: Build
        run: python packaging/build_all.py --platform macos
      - uses: actions/upload-artifact@v4
        with:
          name: macos-dmg
          path: dist/*.dmg

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y libxcb-xinerama0 libxcb-cursor0
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: |
          python packaging/build_all.py --platform linux
          cd packaging/linux && bash create_deb.sh
          cd packaging/linux && bash create_appimage.sh
      - uses: actions/upload-artifact@v4
        with:
          name: linux-packages
          path: |
            dist/*.deb
            dist/*.AppImage
```

---

## 📋 打包命令速查

```bash
# 清理构建目录
python packaging/build_all.py --clean

# 创建应用图标
python packaging/build_all.py --create-icons

# 构建当前平台
python packaging/build_all.py

# 指定平台构建
python packaging/build_all.py --platform windows
python packaging/build_all.py --platform macos
python packaging/build_all.py --platform linux
```

---

## ⚠️ 注意事项

### 1. TA-Lib 依赖
TA-Lib 是 C 库，需要预编译：
- **Windows**: 下载预编译 wheel 或使用 `ta-lib-bin`
- **macOS**: `brew install ta-lib`
- **Linux**: `sudo apt install libta-lib-dev`

### 2. PyQt6 打包
PyQt6 打包可能较大（~100MB），可考虑：
- 使用 UPX 压缩
- 排除不需要的 Qt 模块
- 使用 `--onefile` 模式（启动较慢）

### 3. JQData 认证
打包后的应用仍需要用户配置 JQData 账号：
- 首次运行时引导用户配置
- 配置文件存储在用户目录

### 4. 文件大小
预计安装包大小：
- Windows: 150-200 MB
- macOS: 180-250 MB
- Linux: 120-180 MB

---

## 🎯 发布检查清单

- [ ] 更新版本号 (`APP_VERSION`)
- [ ] 更新 README 和 CHANGELOG
- [ ] 测试所有平台的安装包
- [ ] 代码签名（macOS/Windows）
- [ ] 上传到 GitHub Releases
- [ ] 更新下载链接

---

## 📞 技术支持

如遇打包问题，请检查：
1. Python 版本是否为 3.9+
2. 所有依赖是否正确安装
3. 图标文件是否存在
4. 磁盘空间是否充足（需要 1GB+）

提交 Issue 时请附上：
- 操作系统版本
- Python 版本
- 完整错误日志


