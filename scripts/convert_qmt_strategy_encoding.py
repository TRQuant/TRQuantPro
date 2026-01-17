#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert QMT strategy file to GBK encoding for Windows QMT compatibility

Usage:
    python scripts/convert_qmt_strategy_encoding.py strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py
"""

import sys
from pathlib import Path

def convert_to_gbk(input_file, output_file=None):
    """
    Convert Python file to GBK encoding (for Windows QMT compatibility)
    
    Args:
        input_file: Input file path
        output_file: Output file path (default: input_file with _GBK suffix)
    """
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_GBK{input_path.suffix}"
    else:
        output_file = Path(output_file)
    
    try:
        # Read as UTF-8
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure pure ASCII (remove any non-ASCII characters)
        ascii_content = content.encode('ascii', 'ignore').decode('ascii')
        
        # Write as GBK (Windows default encoding)
        with open(output_file, 'w', encoding='gbk', newline='\n') as f:
            f.write(ascii_content)
        
        print(f"✅ Converted: {input_path.name} -> {output_file.name}")
        print(f"   Encoding: UTF-8 -> GBK")
        print(f"   Size: {len(ascii_content)} characters")
        
        # Verify
        with open(output_file, 'rb') as f:
            verify_data = f.read()
            try:
                verify_text = verify_data.decode('gbk')
                print(f"   ✅ GBK encoding verified")
            except:
                print(f"   ⚠️  GBK encoding verification failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_qmt_strategy_encoding.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_to_gbk(input_file, output_file)
