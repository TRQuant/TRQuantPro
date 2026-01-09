#!/bin/bash
# 安装 venv 中有但 conda base 中缺失的核心包

set -e

echo "🚀 安装缺失的核心包..."
echo "📦 使用 Conda base 环境"
echo ""

# 初始化 conda
eval "$(conda shell.bash hook)"
conda activate base

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip setuptools wheel

# 核心包（优先安装）
echo "📦 安装核心可视化/工具包..."
pip install \
    graphviz \
    networkx \
    TA-Lib \
    Bottleneck \
    openpyxl \
    xlrd \
    GitPython \
    loguru

# 数据源
echo "📦 安装数据源包..."
pip install \
    akshare \
    tushare

# 量化分析（可选，如果不需要可以注释掉）
echo "📦 安装量化分析包..."
pip install \
    bullet-trade \
    alphalens-reloaded \
    empyrical-reloaded \
    pyportfolioopt \
    optuna

# Web/爬虫（可选）
echo "📦 安装 Web/爬虫包..."
pip install \
    scrapy \
    selenium \
    playwright

# 其他工具
echo "📦 安装其他工具包..."
pip install \
    pyqlib \
    pyecharts \
    pymongo \
    redis

echo ""
echo "✅ 核心缺失包安装完成！"
echo ""
echo "📝 验证安装:"
python3 << 'PYEOF'
packages = [
    "graphviz", "networkx", "TA-Lib", "akshare",
    "bullet-trade", "Bottleneck", "openpyxl", "GitPython", "loguru"
]

print("🔍 检查安装状态:")
for pkg in packages:
    try:
        if pkg == "TA-Lib":
            import talib
            version = "installed"
        else:
            mod = __import__(pkg.lower().replace("-", "_"))
            version = getattr(mod, '__version__', 'installed')
        print(f"   ✅ {pkg:20s} - {version}")
    except ImportError:
        print(f"   ❌ {pkg:20s} - 未安装")
PYEOF

