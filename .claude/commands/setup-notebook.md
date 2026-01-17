---
name: "初始化Notebook环境"
description: "为新的Notebook设置标准初始化代码"
command: |
  cat > /tmp/notebook_init.py << 'EOF'
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
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f'✅ 项目根目录已添加到路径: {project_root}')

# 使用统一环境初始化
from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)
EOF
  cat /tmp/notebook_init.py
---

# 初始化Notebook环境命令

生成标准的Notebook初始化代码，可以直接复制到Notebook的第一个Cell。

## 使用方式

在Cursor Chat中：
```
@setup-notebook
```

## 输出

标准的Notebook初始化代码，包括：
- 路径设置
- 项目根目录自动检测
- 统一环境初始化
