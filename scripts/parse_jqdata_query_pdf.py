#!/usr/bin/env python3
"""解析JQData Query PDF文档"""
import sys
import os
from pathlib import Path
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

def parse_pdf(pdf_path):
    """解析PDF"""
    print(f"📄 解析PDF: {pdf_path}")
    
    # 方法1: PyMuPDF
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text_content = []
        images_data = []
        img_dir = Path('/tmp/jqdata_query_pdf_images')
        img_dir.mkdir(exist_ok=True)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(f"=== 第 {page_num + 1} 页 ===\n{text}\n")
            
            # 提取图片
            for img_idx, img in enumerate(page.get_images(), 1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_filename = f"page_{page_num + 1}_img_{img_idx}.{base_image['ext']}"
                img_path = img_dir / img_filename
                with open(img_path, 'wb') as f:
                    f.write(base_image['image'])
                images_data.append({'page': page_num + 1, 'path': str(img_path)})
        
        doc.close()
        return '\n'.join(text_content), images_data
    except Exception as e:
        print(f"PyMuPDF失败: {e}")
        # 备用方法
        try:
            import pdfplumber
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return '\n'.join(text_content), []
        except:
            import PyPDF2
            text_content = []
            with open(pdf_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                for page in pdf.pages:
                    text_content.append(page.extract_text())
            return '\n'.join(text_content), []

if __name__ == "__main__":
    pdf_path = "/home/taotao/dev/QuantTest/TRQuant/DevMustRead/JQDataQuery.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF文件不存在: {pdf_path}")
        sys.exit(1)
    
    text, images = parse_pdf(pdf_path)
    
    # 保存
    with open('/home/taotao/dev/QuantTest/TRQuant/docs/JQDATA_QUERY_PDF_EXTRACTED.md', 'w', encoding='utf-8') as f:
        f.write(f"# JQData Query PDF文档内容\n\n{text}\n\n## 图片\n\n")
        for img in images:
            f.write(f"- {img['path']}\n")
    
    print(f"✅ 已提取 {len(text)} 字符，{len(images)} 张图片")
