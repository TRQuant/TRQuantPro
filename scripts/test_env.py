#!/usr/bin/env python
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

# 添加路径
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope')

try:
    import pandas as pd
    print(f"pandas: {pd.__version__}")
except ImportError as e:
    print(f"pandas error: {e}")

try:
    import numpy as np
    print(f"numpy: {np.__version__}")
except ImportError as e:
    print(f"numpy error: {e}")

try:
    import jqdatasdk as jq
    print("jqdatasdk: OK")
except ImportError as e:
    print(f"jqdatasdk error: {e}")

try:
    from jqdata.auth import authenticate
    print("jqdata.auth: OK")
except ImportError as e:
    print(f"jqdata.auth error: {e}")
