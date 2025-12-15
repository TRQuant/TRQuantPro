# TRQuant回测 GUI 快速启动指南

## 🚀 启动方式

### 方式1: 桌面快捷方式（推荐）
双击桌面上的 **"TRQuant回测"** 图标

### 方式2: 命令行启动
```bash
# 使用启动脚本
./scripts/launch_backtest_gui.sh

# 或直接运行
python3 -m gui.main_window_v2

# 或使用测试脚本
python3 scripts/test_gui.py
```

## 📁 相关文件

### 启动文件
- `scripts/launch_backtest_gui.sh` - 启动脚本
- `scripts/test_gui.py` - 测试脚本
- `scripts/create_desktop_shortcut.sh` - 创建桌面快捷方式

### 图标文件
- `assets/icons/trquant-backtest.png` - PNG格式图标（256x256）
- `assets/icons/trquant-backtest.svg` - SVG格式图标（矢量）

### 桌面快捷方式
- `~/Desktop/TRQuant回测.desktop` - Linux桌面快捷方式文件

## 🎨 LOGO设计

LOGO采用深色背景（#1a1a2e），青色圆形（#00d9ff），绿色边框（#00ff88），中央显示"TRQ回测"文字。

### 颜色方案
- 背景: `#1a1a2e` (深蓝灰)
- 主色: `#00d9ff` (青色)
- 强调: `#00ff88` (绿色)
- 文字: `#1a1a2e` (深色)

## 🔧 故障排除

### 图标不显示
```bash
# 重新创建快捷方式
./scripts/create_desktop_shortcut.sh

# 或手动编辑
nano ~/Desktop/TRQuant回测.desktop
```

### GUI无法启动
```bash
# 检查PyQt6是否安装
python3 -c "import PyQt6; print('OK')"

# 检查模块导入
python3 -c "from gui.main_window_v2 import MainWindowV2; print('OK')"
```

### 权限问题
```bash
# 确保启动脚本有执行权限
chmod +x scripts/launch_backtest_gui.sh
chmod +x ~/Desktop/TRQuant回测.desktop
```

## 📋 功能模块

### 已实现
- ✅ 策略库管理（28个策略）
- ✅ 回测进度显示
- ✅ 回测结果分析
- ✅ 报告查看（12份报告）

### 开发中
- ⏳ 策略优化面板
- ⏳ 券商App回测集成
- ⏳ 实盘交易面板

## 🎯 使用流程

1. **策略管理** - 浏览和选择策略
2. **回测配置** - 设置回测参数
3. **执行回测** - 运行BulletTrade/QMT/快速回测
4. **结果分析** - 查看收益、夏普、回撤等指标
5. **报告导出** - 生成HTML/PDF报告

---

**快速启动完成！** 🎉
