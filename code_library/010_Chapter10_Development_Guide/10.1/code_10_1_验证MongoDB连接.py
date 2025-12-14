"""
文件名: code_10_1_验证MongoDB连接.py
保存路径: code_library/010_Chapter10_Development_Guide/10.1/code_10_1_验证MongoDB连接.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.1_Environment_Setup_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 验证MongoDB连接

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# test_mongodb.py
from pymongo import MongoClient

try:
    # 设计原理：使用serverSelectionTimeoutMS设置超时时间
    # 原因：避免在MongoDB未启动时长时间等待，快速失败
    # 替代方案：可以使用connectTimeoutMS，但serverSelectionTimeoutMS更准确
    client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
    
    # 设计原理：使用admin.command('ping')进行连接测试
    # 原因：ping命令轻量级，不会产生数据，适合健康检查
    # 替代方案：可以尝试list_database_names()，但ping更快速
    client.admin.command('ping')
    print('✓ MongoDB 连接成功')
except Exception as e:
    print(f'✗ MongoDB 连接失败: {e}')