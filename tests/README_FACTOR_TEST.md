# 主线因子组合测试说明

## 📋 测试文件

### 1. GUI测试界面
**文件**: `test_mainline_factor_combination_gui.py`

**功能**:
- 图形化测试界面
- 可视化展示因子得分
- 支持选择行业代码、日期、期限
- 实时显示计算进度

**使用方法**:
```bash
# 方法1: 直接运行
python tests/test_mainline_factor_combination_gui.py

# 方法2: 使用脚本
./tests/run_factor_test_gui.sh
```

**界面功能**:
- 输入行业代码（如 801010）
- 选择日期（默认今天）
- 选择期限（short/medium/long）
- 点击"计算因子组合得分"按钮
- 查看结果：
  - 综合得分（大字体显示）
  - 各因子得分表格
  - 详细数据（JSON格式）

### 2. 命令行测试
**文件**: `test_mainline_factor_simple.py`

**功能**:
- 快速命令行测试
- 不需要GUI依赖
- 适合自动化测试

**使用方法**:
```bash
python tests/test_mainline_factor_simple.py
```

## 🔧 依赖要求

1. **PyQt6**: GUI测试需要
   ```bash
   pip install PyQt6
   ```

2. **JQData账号**: 需要配置聚宽正式账号
   - 配置文件: `config/jqdata_config.json`
   - 需要包含 `username` 和 `password`

3. **AKShare** (可选): 用于获取宏观数据
   ```bash
   pip install akshare
   ```

## ⚠️ 已知问题

1. **行业代码映射**: 
   - 当前使用简化的行业代码映射
   - 实际使用时需要建立完整的行业名称到代码的映射表

2. **数据获取**:
   - 部分因子可能因为数据源限制返回默认值
   - 需要确保JQData账号有相应权限

3. **GUI面板问题**:
   - 现有主窗口的面板可能存在兼容性问题
   - 本测试使用独立的GUI窗口，避免依赖现有面板

## 📊 测试示例

### 测试行业代码
- `801010`: 申万一级行业示例1
- `801020`: 申万一级行业示例2
- `801030`: 申万一级行业示例3

### 测试期限
- `short`: 短期（3-5日）- 更关注资金流和技术面
- `medium`: 中期（15-30日）- 平衡配置
- `long`: 长期（60-180日）- 更关注宏观和基本面

## 🐛 故障排查

### 问题1: 导入错误
```
ImportError: cannot import name 'MainlinePredictionFactorCombination'
```
**解决**: 确保 `core/mainline/mainline_factor_combination.py` 文件存在

### 问题2: JQData认证失败
```
JQData认证失败
```
**解决**: 
1. 检查 `config/jqdata_config.json` 文件
2. 确认账号密码正确
3. 确认账号有相应权限

### 问题3: 无法获取行业股票
```
无法获取行业股票列表
```
**解决**:
1. 检查行业代码是否正确
2. 确认JQData账号有获取行业数据的权限
3. 尝试使用其他行业代码

### 问题4: GUI无法启动
```
PyQt6相关错误
```
**解决**:
1. 安装PyQt6: `pip install PyQt6`
2. 如果使用PyQt5，需要修改导入语句

## 📝 测试结果说明

### 得分范围
- **0-100分**: 综合得分
- **>=70**: 优秀（绿色显示）
- **50-70**: 良好（黄色显示）
- **<50**: 一般（红色显示）

### 因子权重（medium期限）
- 宏观因子: 20%
- 资金流因子: 30%（权重最高）
- 行业景气因子: 25%
- 技术动量因子: 15%
- 市场情绪因子: 10%

## 🔄 下一步

1. 完善行业代码映射
2. 优化因子计算逻辑
3. 添加更多可视化图表
4. 集成到主窗口面板

