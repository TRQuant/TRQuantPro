# region imports
from AlgorithmImports import *
# endregion
#!/usr/bin/env python3
"""
批量删除子节文件中的旧导航条
"""

import os
import re
import glob

def remove_navigation_from_file(file_path):
    """删除单个文件中的导航条"""
    print(f"处理文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 删除顶部导航条 (top-nav)
        content = re.sub(r'<div class="top-nav">.*?</div>\s*\n?', '', content, flags=re.DOTALL)
        
        # 删除底部导航条 (bottom-nav) 及其前面的分隔线
        content = re.sub(r'\n?---\s*\n?<div class="bottom-nav">.*?</div>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="bottom-nav">.*?</div>\s*', '', content, flags=re.DOTALL)
        
        # 删除多余的样式块
        content = re.sub(r'<style>.*?</style>\s*', '', content, flags=re.DOTALL)
        
        # 删除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 确保文件以单个换行符结尾
        content = content.rstrip() + '\n'
        
        # 只有内容发生变化时才写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {file_path}")
            return True
        else:
            print(f"⏭️  无需更新: {file_path}")
            return False
    
    except Exception as e:
        print(f"❌ 处理文件时出错 {file_path}: {e}")
        return False

def main():
    """主函数"""
    # 获取所有子节文件
    patterns = [
        'src/pages/001_Chapter1/[0-9].*_CN.md',
        'src/pages/002_Chapter2/[0-9].*_CN.md', 
        'src/pages/003_Chapter3/[0-9].*_CN.md',
        'src/pages/004_Chapter4/[0-9].*_CN.md',
        'src/pages/005_Chapter5/[0-9].*_CN.md',
        'src/pages/006_Chapter6/[0-9].*_CN.md',
        'src/pages/007_Chapter7/[0-9].*_CN.md',
        'src/pages/008_Chapter8/[0-9].*_CN.md',
        'src/pages/009_Chapter9/[0-9].*_CN.md',
        'src/pages/010_Chapter10/[0-9].*_CN.md',
        'src/pages/011_Appendix/[A-Z].*_CN.md'
    ]
    
    all_files = []
    for pattern in patterns:
        files = glob.glob(pattern)
        all_files.extend(files)
    
    print(f"找到 {len(all_files)} 个子节文件")
    
    updated_count = 0
    for file_path in sorted(all_files):
        if remove_navigation_from_file(file_path):
            updated_count += 1
    
    print(f"\n✅ 完成！共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main() 