"""
文件名: code_10_1_核心依赖列表.py
保存路径: code_library/010_Chapter10_Development_Guide/10.1/code_10_1_核心依赖列表.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.1_Environment_Setup_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 核心依赖列表

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# requirements.txt 核心部分
# 数据处理
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0

# 数据源
jqdatasdk>=1.9.0  # 聚宽数据（需要账号）
akshare>=1.11.0   # 免费数据源

# GUI
PyQt6>=6.4.0
pyqtgraph>=0.13.0

# Web框架
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0

# 工具
python-dotenv>=1.0.0
pyyaml>=6.0
tqdm>=4.65.0
requests>=2.31.0