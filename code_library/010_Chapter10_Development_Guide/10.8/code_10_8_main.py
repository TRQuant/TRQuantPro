"""
文件名: code_10_8_main.py
保存路径: code_library/010_Chapter10_Development_Guide/10.8/code_10_8_main.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.8_Version_Release_Mechanism_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: main

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# scripts/version_bump.py
#!/usr/bin/env python3
"""版本号更新脚本"""
import sys
from pathlib import Path
from core.version import increment_version

def main():
    if len(sys.argv) < 2:
        print("用法: python version_bump.py [major|minor|patch]")
        sys.exit(1)
    
    part = sys.argv[1]
    if part not in ["major", "minor", "patch"]:
        print(f"无效的版本部分: {part}")
        sys.exit(1)
    
    old_version = Path("VERSION").read_text().strip()
    new_version = increment_version(part)
    
    print(f"版本更新: {old_version} → {new_version}")
    
    # 更新package.json（如适用）
    import json
    package_json = Path("extension/package.json")
    if package_json.exists():
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['version'] = new_version
        with open(package_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 已更新 extension/package.json")

if __name__ == "__main__":
    main()