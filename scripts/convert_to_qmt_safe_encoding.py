#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将策略文件转换为QMT安全编码格式
================================

功能：
1. 读取策略文件（自动检测编码）
2. 转换为UTF-8编码
3. 使用二进制模式保存，确保编码正确
4. 验证保存结果

使用方法：
    python scripts/convert_to_qmt_safe_encoding.py <输入文件> [输出文件]
"""

import sys
from pathlib import Path


def convert_to_safe_utf8(input_file: str, output_file: str = None):
    """
    将文件转换为安全的UTF-8编码
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径（可选，默认覆盖原文件）
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        return False
    
    print(f"📁 处理文件: {input_path}")
    
    # 读取文件（二进制模式）
    with open(input_path, 'rb') as f:
        raw_content = f.read()
    
    print(f"   文件大小: {len(raw_content)} 字节")
    
    # 尝试多种编码解码
    encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'latin1', 'cp1252']
    text_content = None
    used_encoding = None
    
    for enc in encodings_to_try:
        try:
            text_content = raw_content.decode(enc)
            used_encoding = enc
            print(f"✅ 使用 {enc} 编码解码成功")
            break
        except (UnicodeDecodeError, LookupError) as e:
            continue
    
    if text_content is None:
        print("❌ 无法解码文件，请检查文件编码")
        return False
    
    # 确定输出文件
    if output_file is None:
        output_path = input_path.with_suffix('.py.utf8')
    else:
        output_path = Path(output_file)
    
    # 备份原文件
    backup_path = input_path.with_suffix('.py.bak')
    try:
        import shutil
        shutil.copy2(input_path, backup_path)
        print(f"✅ 已备份原文件: {backup_path}")
    except Exception as e:
        print(f"⚠️  备份文件失败: {e}")
    
    # 保存为UTF-8编码（二进制模式）
    try:
        with open(output_path, 'wb') as f:
            # 不添加BOM（Python标准）
            f.write(text_content.encode('utf-8'))
        
        print(f"✅ 文件已转换为UTF-8编码: {output_path}")
        
        # 验证
        with open(output_path, 'rb') as f:
            test_bytes = f.read()
            test_text = test_bytes.decode('utf-8')
            
            if len(test_text) > 0:
                print(f"✅ UTF-8编码验证通过")
                print(f"   文件大小: {len(test_text)} 字符")
                print(f"   文件行数: {len(test_text.splitlines())} 行")
                
                # 检查第24行
                lines = test_text.splitlines()
                if len(lines) >= 24:
                    line24 = lines[23]
                    line24_bytes = line24.encode('utf-8')
                    print(f"   第24行内容: {repr(line24[:50])}")
                    print(f"   第24行字节长度: {len(line24_bytes)}")
                    if len(line24_bytes) > 27:
                        print(f"   位置27的字节: 0x{line24_bytes[27]:02x} ({line24_bytes[27:28]})")
                
                return True
            else:
                print("❌ 文件内容为空")
                return False
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python scripts/convert_to_qmt_safe_encoding.py <输入文件> [输出文件]")
        print("示例:")
        print("  python scripts/convert_to_qmt_safe_encoding.py strategies/qmt/TRQuant_V4_QMT_Research_*.py")
        print("  python scripts/convert_to_qmt_safe_encoding.py input.py output.py")
        return 1
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_to_safe_utf8(input_file, output_file)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ 转换完成！")
        print("=" * 70)
        if output_file:
            print(f"\n📁 输出文件: {output_file}")
        else:
            print(f"\n📁 输出文件: {input_file}.utf8")
        print("\n💡 提示: 请将转换后的文件复制到QMT策略目录使用")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
