# TRQuant GUI模块

## 📋 模块说明

TRQuant采用**双GUI架构**，分别服务于研究和工程两个阶段。

## 🎯 GUI定位

### 1. 研究型GUI (Research GUI)
**文件位置**: `gui/research/` (待开发/重构)

**定位**: 信息获取 → 因子推荐等研究步骤

**功能**:
- 市场状态分析
- 投资主线识别
- 因子研究和推荐
- 策略思路探索
- 研究报告生成

---

### 2. 工程型GUI (Engineering GUI) ⭐
**文件位置**: `gui/main_window_v2.py`

**定位**: 策略生成 → 回测 → 优化 → 实盘

**功能**:
- ✅ 策略库管理
- ✅ 回测执行（BulletTrade/QMT/快速回测）
- ✅ 回测结果分析
- ✅ 报告查看
- ⏳ 策略优化（开发中）
- ⏳ 券商App回测（开发中）
- ⏳ 实盘交易（待开发）

## 🚀 快速开始

### 启动工程型GUI
```bash
# 方式1: 直接运行
python -m gui.main_window_v2

# 方式2: 使用测试脚本
python scripts/test_gui.py
```

## 📁 文件结构

```
gui/
├── main_window_v2.py              # 工程型主窗口
├── widgets/
│   ├── strategy_manager_panel.py  # 策略管理
│   ├── backtest_progress_panel.py # 回测进度
│   ├── backtest_result_panel.py  # 结果分析
│   └── report_viewer_panel.py    # 报告查看
├── research/                      # 研究型GUI (待开发)
│   └── ...
└── README.md                      # 本文件
```

## 🔗 相关文档

- [GUI架构设计](../docs/GUI_ARCHITECTURE.md)
- [GUI开发完成报告](../docs/GUI_DEVELOPMENT_COMPLETE.md)
