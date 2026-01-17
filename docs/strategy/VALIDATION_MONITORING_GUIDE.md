# 长期回测验证监控指南

## 📊 当前状态

### 验证进程状态

**进程ID**: 83979  
**状态**: ✅ 正在运行  
**CPU使用率**: 31.6%  
**内存使用**: 0.5%  
**运行时间**: 约4分13秒  

### 验证进度

**验证时间段**:
1. 2014-2016 ⏳ 进行中
2. 2017-2019 ⏳ 等待中
3. 2020-2022 ⏳ 等待中
4. 2023-2024 ⏳ 等待中

**预计完成时间**: 约20-40分钟（总共4个时间段）

---

## 🔍 监控方法

### 方法1: 使用监控脚本（推荐）

#### 快速检查
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/monitor_validation.py
```

#### 实时监控（每10秒更新）
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/monitor_validation_live.py 10
```

#### 使用watch命令
```bash
watch -n 30 'python scripts/monitor_validation.py'
```

### 方法2: 手动检查

#### 检查进程
```bash
ps aux | grep validate_market_type_v7_long_term | grep -v grep
```

#### 检查输出文件
```bash
ls -lth output/market_type_validation/*.md
```

#### 查看最新报告
```bash
tail -50 output/market_type_validation/validation_report_*.md | tail -1
```

---

## 📈 进度估算

### 每个时间段预计时间

| 时间段 | 交易日数 | 采样验证次数 | 预计时间 |
|--------|---------|-------------|---------|
| 2014-2016 | ~733天 | ~140次 | 5-10分钟 |
| 2017-2019 | ~730天 | ~140次 | 5-10分钟 |
| 2020-2022 | ~730天 | ~140次 | 5-10分钟 |
| 2023-2024 | ~500天 | ~100次 | 4-8分钟 |

**总计**: 约20-40分钟

### 进度判断

- **CPU使用率 > 30%**: 正在计算，验证进行中
- **CPU使用率 < 5%**: 可能等待数据或已完成
- **报告文件生成**: 验证已完成

---

## 📁 输出文件

### 报告位置

```
output/market_type_validation/validation_report_YYYYMMDD_HHMMSS.md
```

### 报告内容

1. **总体统计**
   - 总预测数
   - 正确预测数
   - 总体准确率

2. **各类型准确率**
   - 快牛准确率
   - 慢牛准确率
   - 震荡准确率
   - 熊市准确率

3. **参数优化建议**
   - 原始阈值
   - 优化阈值
   - 优化理由

---

## ⚠️ 常见问题

### 1. 进程未运行

**检查**:
```bash
pgrep -f validate_market_type_v7_long_term
```

**如果未运行，重新启动**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
nohup ./venv/bin/python scripts/validate_market_type_v7_long_term.py > validation.log 2>&1 &
```

### 2. 验证时间过长

**可能原因**:
- 数据获取慢（网络问题）
- 计算量大（市场宽度数据）
- 缓存未命中

**解决方案**:
- 检查网络连接
- 增加采样频率（减少验证次数）
- 检查缓存状态

### 3. 报告未生成

**检查**:
```bash
ls -lth output/market_type_validation/
```

**如果目录不存在**:
```bash
mkdir -p output/market_type_validation
```

---

## 🎯 验证完成后的操作

### 1. 查看报告

```bash
cat output/market_type_validation/validation_report_*.md
```

### 2. 分析结果

- 检查总体准确率是否>70%
- 检查各类型准确率
- 查看参数优化建议

### 3. 应用优化参数

根据报告中的优化建议，更新V7分类器的阈值参数。

---

## 📝 监控脚本说明

### monitor_validation.py

**功能**: 快速检查验证状态

**输出**:
- 进程运行状态
- 进程信息（PID、CPU、内存）
- 输出文件状态

### monitor_validation_live.py

**功能**: 实时监控验证进度

**特点**:
- 自动刷新（可设置间隔）
- 进度估算
- 报告预览
- 清屏显示

**使用**:
```bash
python scripts/monitor_validation_live.py [刷新间隔秒数]
```

---

**最后更新**: 2026-01-12  
**文档作者**: TRQuant Team
