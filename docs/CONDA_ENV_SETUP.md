# Conda 环境设置指南

## 概述

本指南说明如何使用 Conda（Miniconda/Anaconda）来管理项目的 Python 环境，**复用已下载的包，避免重复安装**。

## 当前状态

- ✅ 已安装 **Miniconda 3** (conda 25.5.1)
- ✅ 项目已有 `venv` 虚拟环境（使用系统 Python 3.12.3）
- ✅ 项目有 `requirements.txt` 依赖文件

## 为什么使用 Conda？

1. **复用包缓存**：Conda 会在 `~/miniconda3/pkgs/` 中缓存已下载的包，避免重复下载
2. **更好的包管理**：Conda 可以管理 Python 版本和系统依赖
3. **环境隔离**：与系统 Python 和 venv 完全隔离
4. **跨平台**：在不同操作系统上行为一致

## 快速开始

### 方法 1: 使用自动化脚本（推荐）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./setup_conda_env.sh
```

脚本会自动：
- 检查 conda 是否安装
- 创建名为 `trquant` 的 conda 环境（Python 3.12）
- 从 `requirements.txt` 安装所有依赖
- 验证安装结果

### 方法 2: 手动创建环境

```bash
# 1. 创建 conda 环境（Python 3.12，匹配现有 venv）
conda create -n trquant python=3.12 -y

# 2. 激活环境
conda activate trquant

# 3. 升级 pip
pip install --upgrade pip setuptools wheel

# 4. 安装项目依赖
pip install -r requirements.txt
```

## 使用方法

### 激活环境

```bash
conda activate trquant
```

激活后，命令行提示符前会显示 `(trquant)`。

### 运行项目

```bash
# 激活环境
conda activate trquant

# 运行主程序
python main.py

# 运行 Jupyter Notebook
jupyter notebook

# 运行测试
pytest tests/
```

### 退出环境

```bash
conda deactivate
```

## Conda vs Venv 对比

| 特性 | Conda | Venv |
|------|-------|------|
| Python 版本管理 | ✅ 可以管理 Python 版本 | ❌ 依赖系统 Python |
| 包缓存复用 | ✅ 自动缓存和复用 | ⚠️ 部分复用（pip cache） |
| 系统依赖管理 | ✅ 可以管理系统库 | ❌ 只管理 Python 包 |
| 环境大小 | ⚠️ 较大（~500MB） | ✅ 较小（~50MB） |
| 激活速度 | ⚠️ 稍慢 | ✅ 快速 |
| 跨平台 | ✅ 完全一致 | ⚠️ 可能差异 |

## 复用已下载的包

Conda 会自动复用已下载的包：

1. **Conda 包缓存位置**：`~/miniconda3/pkgs/`
2. **pip 包缓存位置**：`~/.cache/pip/`
3. **复用机制**：
   - Conda 会在安装前检查 `pkgs/` 目录
   - 如果包已存在且版本匹配，直接使用，无需重新下载
   - pip 也会检查 pip cache，复用已下载的包

### 查看缓存

```bash
# 查看 conda 缓存大小
du -sh ~/miniconda3/pkgs/

# 查看 conda 缓存中的包
ls ~/miniconda3/pkgs/ | head -20

# 清理 conda 缓存（释放空间）
conda clean --all

# 查看 pip 缓存
pip cache info
```

## 环境管理

### 查看所有环境

```bash
conda env list
```

输出示例：
```
# conda environments:
#
base                   /home/taotao/miniconda3
trquant             *  /home/taotao/miniconda3/envs/trquant
```

`*` 表示当前激活的环境。

### 导出环境配置

```bash
# 导出为 environment.yml（包含所有包和版本）
conda env export > environment.yml

# 导出为 requirements.txt（仅 pip 包）
conda activate trquant
pip freeze > requirements_conda.txt
```

### 从配置文件创建环境

```bash
# 从 environment.yml 创建
conda env create -f environment.yml

# 从 requirements.txt 安装（需先创建环境）
conda create -n new_env python=3.12 -y
conda activate new_env
pip install -r requirements.txt
```

### 删除环境

```bash
conda env remove -n trquant
```

### 克隆环境

```bash
# 克隆现有环境
conda create -n trquant_backup --clone trquant
```

## 包管理

### 安装包

```bash
conda activate trquant

# 使用 conda 安装（推荐用于科学计算包）
conda install numpy pandas matplotlib -y

# 使用 pip 安装（用于 PyPI 专用包）
pip install jqdatasdk plotly PyQt6
```

### 更新包

```bash
conda activate trquant

# 更新所有 conda 包
conda update --all -y

# 更新所有 pip 包
pip install --upgrade -r requirements.txt

# 更新单个包
conda update numpy -y
pip install --upgrade plotly
```

### 查看已安装的包

```bash
conda activate trquant

# 查看 conda 包
conda list

# 查看 pip 包
pip list

# 搜索包
conda search numpy
pip search plotly  # 注意：pip search 已被禁用
```

## 性能优化

### 使用 Conda 的包管理器

对于科学计算包（numpy, pandas, scipy 等），使用 conda 安装通常更快且更可靠：

```bash
conda activate trquant

# 使用 conda 安装核心科学计算包
conda install numpy pandas scipy scikit-learn matplotlib seaborn -y

# 使用 pip 安装其他包
pip install jqdatasdk plotly PyQt6 jupyter
```

### 使用国内镜像源（可选）

如果下载速度慢，可以配置镜像源：

```bash
# Conda 镜像（清华源）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

# pip 镜像（清华源）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 常见问题

### Q1: Conda 和 Venv 可以同时使用吗？

A: 可以，它们是独立的。建议：
- 开发时使用 conda（更好的包管理）
- 生产环境可以使用 venv（更轻量）

### Q2: 如何迁移现有的 venv 到 conda？

A: 不需要迁移，直接创建新的 conda 环境即可：

```bash
# 1. 导出 venv 中的包列表
source venv/bin/activate
pip freeze > requirements_venv.txt

# 2. 创建 conda 环境
conda create -n trquant python=3.12 -y
conda activate trquant

# 3. 安装依赖（conda 会复用已下载的包）
pip install -r requirements_venv.txt
```

### Q3: Conda 环境占用空间太大？

A: 可以定期清理：

```bash
# 清理未使用的包和缓存
conda clean --all -y

# 仅清理缓存（保留已安装的包）
conda clean --packages -y
```

### Q4: 如何同时管理多个项目的 conda 环境？

A: 建议为每个项目创建独立的环境：

```bash
# 项目 1
conda create -n project1 python=3.12 -y
conda activate project1
pip install -r project1/requirements.txt

# 项目 2
conda create -n project2 python=3.11 -y
conda activate project2
pip install -r project2/requirements.txt

# 查看所有环境
conda env list
```

### Q5: Jupyter Notebook 如何使用 conda 环境？

A: 安装 ipykernel 并注册环境：

```bash
conda activate trquant
pip install ipykernel
python -m ipykernel install --user --name trquant --display-name "Python (trquant)"

# 在 Jupyter Notebook 中选择 kernel: Kernel -> Change Kernel -> Python (trquant)
```

## 下一步

1. ✅ 运行 `./setup_conda_env.sh` 创建环境
2. ✅ 激活环境：`conda activate trquant`
3. ✅ 运行项目测试：`python test_backtest.py`
4. ✅ 配置 IDE（VSCode/Cursor）使用 conda 环境

## 参考资源

- [Conda 官方文档](https://docs.conda.io/)
- [Miniconda 下载](https://docs.conda.io/en/latest/miniconda.html)
- [Conda vs Venv 对比](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

