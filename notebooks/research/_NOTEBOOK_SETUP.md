# Notebook 路径设置说明

## 问题说明

在 Cursor 中运行 Notebook 时，如果遇到 `ModuleNotFoundError: No module named 'notebooks'` 错误，这是因为 Python 找不到项目模块。

## 解决方案

所有研究 Notebook 的第一个代码单元格都应该包含路径设置代码：

```python
# 添加项目根目录到 Python 路径（必须在导入前执行）
import sys
from pathlib import Path

# 自动检测项目根目录
current_dir = Path.cwd()
project_root = None
for parent in [current_dir] + list(current_dir.parents):
    if (parent / 'core').exists() and (parent / 'config').exists():
        project_root = parent
        break

if project_root is None:
    # 回退到默认路径
    project_root = Path('/home/taotao/dev/QuantTest/TRQuant')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f'✅ 项目根目录已添加到路径: {project_root}')
```

## 验证

运行第一个代码单元格后，应该看到：
```
✅ 项目根目录已添加到路径: /home/taotao/dev/QuantTest/TRQuant
✅ 模块加载完成
```

## 如果仍然失败

1. 确认工作目录正确：
   ```python
   import os
   print(os.getcwd())
   ```

2. 手动设置路径：
   ```python
   import sys
   sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')
   ```

3. 重启 Kernel：
   - 按 `Ctrl+Shift+P`
   - 输入: "Jupyter: Restart Kernel"
