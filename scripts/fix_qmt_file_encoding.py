#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复QMT策略文件编码问题
=====================

功能：
1. 将策略文件转换为UTF-8编码
2. 确保Windows QMT可以正确读取
3. 移除可能导致编码问题的字符

使用方法：
    python scripts/fix_qmt_file_encoding.py <策略文件路径>
"""

import sys
from pathlib import Path


def fix_file_encoding(file_path: str):
    """
    修复文件编码问题
    
    Args:
        file_path: 策略文件路径
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    print(f"📁 处理文件: {file_path}")
    
    # 尝试读取文件（多种编码）
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    content = None
    used_encoding = None
    
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                used_encoding = enc
                print(f"✅ 使用 {enc} 编码读取成功")
                break
        except Exception as e:
            print(f"❌ 使用 {enc} 编码读取失败: {e}")
            continue
    
    if content is None:
        print("❌ 无法读取文件，请检查文件编码")
        return False
    
    # 备份原文件
    backup_path = file_path.with_suffix('.py.bak')
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        print(f"✅ 已备份原文件: {backup_path}")
    except Exception as e:
        print(f"⚠️  备份文件失败: {e}")
    
    # 保存为UTF-8编码
    try:
        # 使用二进制模式写入，确保UTF-8编码
        with open(file_path, 'wb') as f:
            # 添加UTF-8 BOM（可选，某些Windows系统需要）
            # f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
            f.write(content.encode('utf-8'))
        
        print(f"✅ 文件已转换为UTF-8编码")
        
        # 验证
        with open(file_path, 'r', encoding='utf-8') as f:
            test_content = f.read()
            if len(test_content) > 0:
                print(f"✅ UTF-8编码验证通过")
                print(f"   文件大小: {len(test_content)} 字符")
                print(f"   文件行数: {len(test_content.splitlines())} 行")
                return True
            else:
                print("❌ 文件内容为空")
                return False
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python scripts/fix_qmt_file_encoding.py <策略文件路径>")
        print("示例: python scripts/fix_qmt_file_encoding.py strategies/qmt/TRQuant_V4_QMT_Research_*.py")
        return 1
    
    file_path = sys.argv[1]
    success = fix_file_encoding(file_path)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
