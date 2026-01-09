# Jupyter Notebook Kernel 选择指南

## 📋 概览

本指南说明在 Jupyter Notebook 中如何选择正确的 Python kernel，以及是否需要单独的 TRQuant kernel。

## ✅ 推荐方案：使用 Conda Base 环境

### 方案说明

如果所有 Python 包都安装到 **conda base 环境**，那么：

- ✅ **只需要选择 conda base 环境的 Python3 kernel**
- ✅ **不需要单独的 TRQuant kernel**
- ✅ 所有已安装的包都可以直接使用

### 当前环境信息

- **Conda 环境**: `base`
- **Python 路径**: `/home/taotao/miniconda3/bin/python3`
- **Python 版本**: 3.13.5
- **包安装位置**: `/home/taotao/miniconda3/lib/python3.13/site-packages/`

## 🔍 如何选择 Kernel

### 在 Jupyter Notebook 中选择 Kernel

1. **打开 Jupyter Notebook** (http://localhost:8888)

2. **创建或打开 Notebook 文件**

3. **选择 Kernel**:
   - 点击右上角的 **"Kernel"** 菜单
   - 选择 **"Change Kernel"**
   - 选择 **"Python 3"** 或显示路径为 `/home/taotao/miniconda3/bin/python3` 的 kernel

4. **验证 Kernel**:
   ```python
   import sys
   print(sys.executable)
   # 应该显示: /home/taotao/miniconda3/bin/python3
   
   import numpy
   import pandas
   print("✅ 所有包都可以正常导入")
   ```

### 查看可用的 Kernel

在终端中运行：

```bash
conda activate base
jupyter kernelspec list
```

应该看到类似输出：

```
Available kernels:
  python3    /home/taotao/.local/share/jupyter/kernels/python3
```

## 🔧 如果需要单独的环境

### 场景：使用单独的 trquant conda 环境

如果创建了单独的 `trquant` conda 环境，需要：

1. **创建 conda 环境**:
   ```bash
   conda create -n trquant python=3.12 -y
   conda activate trquant
   ```

2. **在环境中安装包**:
   ```bash
   pip install -r requirements.txt
   ```

3. **注册为 Jupyter Kernel**:
   ```bash
   conda activate trquant
   pip install ipykernel
   python -m ipykernel install --user --name trquant --display-name "Python (trquant)"
   ```

4. **在 Jupyter Notebook 中选择**:
   - Kernel → Change Kernel → Python (trquant)

### 对比两种方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Conda Base** | ✅ 简单，无需额外配置<br>✅ 所有包在一个环境<br>✅ 默认 kernel 即可使用 | ⚠️ 与其他项目共享环境 |
| **单独环境** | ✅ 环境隔离<br>✅ 可以为不同项目使用不同 Python 版本 | ⚠️ 需要额外配置<br>⚠️ 需要注册 kernel |

## 💡 推荐：使用 Conda Base

### 为什么推荐使用 Base 环境？

1. **简单直接**:
   - 所有包安装到一个环境
   - 使用默认的 Python3 kernel
   - 无需额外配置

2. **自动路径管理**:
   - Conda 自动管理 Python 路径
   - Jupyter 自动识别 conda 环境的 kernel
   - 无需手动配置

3. **包复用**:
   - 所有项目共享已安装的包
   - 避免重复安装
   - 节省磁盘空间

### 使用步骤

1. **激活 conda base 环境**:
   ```bash
   conda activate base
   ```

2. **安装依赖** (如果还没有):
   ```bash
   ./install_dependencies.sh
   ```

3. **启动 Jupyter Notebook**:
   ```bash
   ./start_jupyter_notebook.sh
   ```

4. **在 Notebook 中选择 Kernel**:
   - Kernel → Change Kernel → **Python 3**
   - (应该指向 `/home/taotao/miniconda3/bin/python3`)

5. **验证**:
   ```python
   import sys
   import numpy
   import pandas
   import matplotlib
   import plotly
   import PyQt6
   
   print(f"Python: {sys.executable}")
   print("✅ 所有包都可以正常导入")
   ```

## ⚠️ 注意事项

### 1. 确保在正确的环境

在 Jupyter Notebook 中检查：

```python
import sys
print(sys.executable)
# 应该显示: /home/taotao/miniconda3/bin/python3
```

如果不是，说明选择了错误的 kernel。

### 2. 检查包是否可导入

```python
try:
    import numpy
    import pandas
    print("✅ 核心包已安装")
except ImportError as e:
    print(f"❌ 包未安装: {e}")
```

### 3. 如果需要安装缺失的包

```bash
conda activate base
pip install package_name
```

或者在 Jupyter Notebook 中：

```python
import sys
!{sys.executable} -m pip install package_name
```

## 🎯 总结

### 使用 Conda Base 环境（推荐）

- ✅ **只需要选择默认的 Python3 kernel**
- ✅ **不需要单独的 TRQuant kernel**
- ✅ 所有包都安装到 base 环境
- ✅ 使用 base 环境的 Python kernel 即可

### 验证 Kernel 选择

在 Jupyter Notebook 中运行：

```python
import sys
print("Python 路径:", sys.executable)
print("包路径:", sys.path[1])  # site-packages 路径
```

应该显示：
- Python 路径: `/home/taotao/miniconda3/bin/python3`
- 包路径: `/home/taotao/miniconda3/lib/python3.13/site-packages`

## 🔗 相关文档

- [Conda 环境设置指南](CONDA_ENV_SETUP.md)
- [Conda 包安装位置说明](CONDA_PACKAGE_INSTALLATION.md)

