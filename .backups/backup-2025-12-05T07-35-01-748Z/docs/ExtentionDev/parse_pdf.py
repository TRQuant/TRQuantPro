#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析QuantConnect深度研究PDF文档 - 使用PyMuPDF"""

import sys

pdf_path = '/home/taotao/dev/QuantTest/TRQuant/docs/ExtentionDev/QuantConnect 深度研究与 TRQuant Cursor 插件功能规划.pdf'

print(f"正在解析: {pdf_path}")
print("=" * 80)

try:
    import fitz  # PyMuPDF
    
    doc = fitz.open(pdf_path)
    print(f"PDF共有 {len(doc)} 页\n")
    
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            print(f"\n{'='*40} 第 {i+1} 页 {'='*40}\n")
            print(text)
    
    doc.close()
    
except ImportError:
    print("PyMuPDF未安装，尝试使用pypdf...")
    try:
        from pypdf import PdfReader
        
        reader = PdfReader(pdf_path)
        print(f"PDF共有 {len(reader.pages)} 页\n")
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                print(f"\n{'='*40} 第 {i+1} 页 {'='*40}\n")
                print(text)
                
    except ImportError:
        print("pypdf也未安装，请安装: pip install pymupdf 或 pip install pypdf")
        
except Exception as e:
    print(f"解析错误: {e}")
    import traceback
    traceback.print_exc()
