# JQQuant 安装指南

## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南







## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南





## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南


## 安装完成 ✅

所有依赖已成功安装到虚拟环境中！

## 虚拟环境位置

```
/home/taotao/dev/QuantTest/TRQuant/venv/
```

## 使用方法

### 方法1: 使用激活脚本（推荐）

```bash
source activate_env.sh
```

### 方法2: 手动激活

```bash
source venv/bin/activate
```

### 方法3: 直接使用虚拟环境的Python

```bash
venv/bin/python your_script.py
```

## 已安装的依赖包

✅ **核心依赖**:
- numpy>=1.24.0 (已安装: 2.3.5)
- pandas>=2.0.0 (已安装: 2.3.3)
- matplotlib>=3.7.0 (已安装: 3.10.7)
- scikit-learn>=1.3.0 (已安装: 1.7.2)

✅ **聚宽API**:
- jqdatasdk>=1.9.0 (已安装: 1.9.7)

✅ **技术指标**:
- TA-Lib>=0.4.0 (已安装: 0.6.8)

✅ **可视化**:
- plotly>=5.14.0 (已安装: 6.5.0)
- seaborn>=0.12.0 (已安装: 0.13.2)

✅ **工具库**:
- python-dotenv>=1.0.0 (已安装: 1.2.1)
- pyyaml>=6.0 (已安装: 6.0.3)
- tqdm>=4.65.0 (已安装: 4.67.1)

## 验证安装

运行验证脚本：

```bash
source venv/bin/activate
python verify_config.py
```

应该看到所有检查项都显示 ✅

## 运行回测

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

### 2. 运行测试回测

```bash
python test_backtest.py
```

### 3. 运行完整回测

```bash
python main.py \
    --strategy ma_cross \
    --start 2024-08-01 \
    --end 2024-10-31 \
    --securities 000001.XSHE 600000.XSHG
```

### 4. 运行快速脚本

```bash
python run_adaptive_momentum_a_v2.py
```

## 退出虚拟环境

```bash
deactivate
```

## 更新依赖

如果需要更新依赖包：

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 重新安装

如果需要重新创建虚拟环境：

```bash
# 删除旧环境
rm -rf venv

# 创建新环境
python3 -m venv venv

# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认虚拟环境已激活？

A: 激活后，命令行提示符前会显示 `(venv)`，或者运行：
```bash
which python
# 应该显示: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
```

### Q: 安装失败怎么办？

A: 确保：
1. 有网络连接
2. Python版本 >= 3.8
3. pip已更新: `pip install --upgrade pip`

### Q: TA-Lib安装失败？

A: TA-Lib可能需要系统库，可以尝试：
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# 然后重新安装Python包
pip install TA-Lib
```

## 下一步

1. ✅ 依赖已安装
2. ✅ 配置已验证
3. 🚀 可以开始运行回测了！

参考文档：
- `docs/ARCHITECTURE.md` - 项目架构
- `docs/CONFIG_VERIFICATION.md` - 配置验证
- `BACKUP_GUIDE.md` - 备份指南














