"""
文件名: code_10_1_verify_postgresql_connection.py
保存路径: code_library/010_Chapter10_Development_Guide/10.1/code_10_1_verify_postgresql_connection.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.1_Environment_Setup_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 验证PostgreSQL连接

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# test_postgres.py
import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='trquant',
        user='trquant',
        password='your_password'
    )
    print('✓ PostgreSQL 连接成功')
    conn.close()
except Exception as e:
    print(f'✗ PostgreSQL 连接失败: {e}')