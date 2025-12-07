# region imports
from AlgorithmImports import *
# endregion
import shutil
import os
from datetime import datetime

def backup_chapter_file():
    """备份第一章文件"""
    source_file = "src/pages/001_第一章：看清自己，看懂世界——投资的认知起点.md"
    backup_file = f"src/pages/001_第一章：看清自己，看懂世界——投资的认知起点_{datetime.now().strftime('%Y%m%d')}_图片重构前备份.md"
    
    try:
        if os.path.exists(source_file):
            shutil.copy2(source_file, backup_file)
            print(f"✅ 备份成功: {backup_file}")
            return True
        else:
            print(f"❌ 源文件不存在: {source_file}")
            return False
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return False

if __name__ == "__main__":
    backup_chapter_file() 