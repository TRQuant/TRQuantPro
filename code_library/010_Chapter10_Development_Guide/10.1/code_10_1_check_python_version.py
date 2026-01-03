"""
文件名: code_10_1_check_python_version.py
保存路径: code_library/010_Chapter10_Development_Guide/10.1/code_10_1_check_python_version.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.1_Environment_Setup_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: check_python_version

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# scripts/verify_environment.py
#!/usr/bin/env python3
"""环境验证脚本"""
import sys
import importlib

def check_python_version():
        """
    check_python_version函数
    
    **设计原理**：
    - **核心功能**：实现check_python_version的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"✗ Python版本过低: {version.major}.{version.minor}")
        print("  要求: Python 3.11+")
        return False
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name, import_name=None):
    """检查包是否安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装")
        return False

def check_database(host, port, db_type):
    """检查数据库连接"""
    try:
        if db_type == 'mongodb':
            from pymongo import MongoClient
            client = MongoClient(f'mongodb://{host}:{port}', serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            print(f"✓ MongoDB 连接成功 ({host}:{port})")
            return True
        elif db_type == 'postgres':
            import psycopg2
            conn = psycopg2.connect(host=host, port=port, database='trquant', user='trquant', password='')
            conn.close()
            print(f"✓ PostgreSQL 连接成功 ({host}:{port})")
            return True
        elif db_type == 'redis':
            import redis
            r = redis.Redis(host=host, port=port, db=0)
            r.ping()
            print(f"✓ Redis 连接成功 ({host}:{port})")
            return True
    except Exception as e:
        print(f"✗ {db_type.upper()} 连接失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("TRQuant 环境验证")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    print("\n检查核心依赖:")
    packages = [
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('PyQt6', 'PyQt6'),
        ('fastapi', 'fastapi'),
        ('jqdatasdk', 'jqdata'),
    ]
    
    all_ok = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_ok = False
    
    print("\n检查可选依赖:")
    optional_packages = [
        ('pymongo', 'pymongo'),
        ('psycopg2', 'psycopg2'),
        ('redis', 'redis'),
    ]
    
    for package_name, import_name in optional_packages:
        check_package(package_name, import_name)
    
    print("\n检查数据库连接（可选）:")
    # MongoDB
    try:
        check_database('localhost', 27017, 'mongodb')
    except:
        print("⚠ MongoDB 未配置或未运行")
    
    # PostgreSQL
    try:
        check_database('localhost', 5432, 'postgres')
    except:
        print("⚠ PostgreSQL 未配置或未运行")
    
    # Redis
    try:
        check_database('localhost', 6379, 'redis')
    except:
        print("⚠ Redis 未配置或未运行")
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✓ 环境验证通过")
    else:
        print("✗ 环境验证失败，请检查缺失的依赖")
        sys.exit(1)

if __name__ == '__main__':
    main()