#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转PDF工具

将Markdown文档转换为PDF格式
支持中文文档
"""

import sys
from pathlib import Path
from typing import Optional
import re

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def markdown_to_pdf_using_html(md_file: Path, output_pdf: Optional[Path] = None) -> Path:
    """
    通过HTML中间格式将Markdown转换为PDF
    
    方法1: 使用markdown + weasyprint
    方法2: 使用markdown + reportlab（如果方法1失败）
    """
    if output_pdf is None:
        output_pdf = md_file.with_suffix('.pdf')
    
    # 读取markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 方法1: 尝试使用markdown + weasyprint
    try:
        import markdown
        from weasyprint import HTML
        
        # 将markdown转换为HTML
        html = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite', 'toc']
        )
        
        # 添加CSS样式
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: "SimSun", "宋体", "STSong", "Microsoft YaHei", sans-serif;
                    font-size: 12pt;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    font-size: 24pt;
                    font-weight: bold;
                    margin-top: 20pt;
                    margin-bottom: 12pt;
                    border-bottom: 2pt solid #333;
                    padding-bottom: 6pt;
                }}
                h2 {{
                    font-size: 20pt;
                    font-weight: bold;
                    margin-top: 16pt;
                    margin-bottom: 10pt;
                    border-bottom: 1pt solid #666;
                    padding-bottom: 4pt;
                }}
                h3 {{
                    font-size: 16pt;
                    font-weight: bold;
                    margin-top: 12pt;
                    margin-bottom: 8pt;
                }}
                h4 {{
                    font-size: 14pt;
                    font-weight: bold;
                    margin-top: 10pt;
                    margin-bottom: 6pt;
                }}
                p {{
                    margin-bottom: 8pt;
                    text-align: justify;
                }}
                code {{
                    font-family: "Courier New", "Consolas", monospace;
                    background-color: #f5f5f5;
                    padding: 2pt 4pt;
                    border-radius: 3pt;
                    font-size: 10pt;
                }}
                pre {{
                    background-color: #f5f5f5;
                    border: 1pt solid #ddd;
                    border-radius: 4pt;
                    padding: 10pt;
                    overflow-x: auto;
                    font-family: "Courier New", "Consolas", monospace;
                    font-size: 10pt;
                    line-height: 1.4;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 10pt 0;
                }}
                th, td {{
                    border: 1pt solid #ddd;
                    padding: 6pt;
                    text-align: left;
                }}
                th {{
                    background-color: #f0f0f0;
                    font-weight: bold;
                }}
                ul, ol {{
                    margin-bottom: 8pt;
                    padding-left: 20pt;
                }}
                li {{
                    margin-bottom: 4pt;
                }}
                blockquote {{
                    border-left: 4pt solid #ddd;
                    padding-left: 12pt;
                    margin-left: 0;
                    color: #666;
                    font-style: italic;
                }}
                hr {{
                    border: none;
                    border-top: 1pt solid #ddd;
                    margin: 16pt 0;
                }}
            </style>
        </head>
        <body>
        {html}
        </body>
        </html>
        """
        
        # 转换为PDF
        HTML(string=html_with_style).write_pdf(output_pdf)
        print(f"✅ PDF已生成: {output_pdf}")
        return output_pdf
        
    except ImportError:
        print("⚠️ weasyprint不可用，尝试使用reportlab...")
        
        # 方法2: 使用reportlab
        try:
            return markdown_to_pdf_using_reportlab(md_file, output_pdf)
        except Exception as e:
            print(f"❌ reportlab转换失败: {e}")
            raise


def markdown_to_pdf_using_reportlab(md_file: Path, output_pdf: Optional[Path] = None) -> Path:
    """使用reportlab将Markdown转换为PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    
    if output_pdf is None:
        output_pdf = md_file.with_suffix('.pdf')
    
    # 读取markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 注册中文字体
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    
    chinese_font_registered = False
    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                chinese_font_registered = True
                break
            except:
                continue
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    
    styles = getSampleStyleSheet()
    if chinese_font_registered:
        # 创建中文字体样式
        styles.add({
            'ChineseTitle': {
                'fontName': 'ChineseFont',
                'fontSize': 24,
                'leading': 28,
                'alignment': TA_LEFT,
            },
            'ChineseHeading1': {
                'fontName': 'ChineseFont',
                'fontSize': 20,
                'leading': 24,
                'alignment': TA_LEFT,
            },
            'ChineseHeading2': {
                'fontName': 'ChineseFont',
                'fontSize': 16,
                'leading': 20,
                'alignment': TA_LEFT,
            },
            'ChineseNormal': {
                'fontName': 'ChineseFont',
                'fontSize': 12,
                'leading': 18,
                'alignment': TA_LEFT,
            },
        })
    
    story = []
    
    # 解析markdown并转换为PDF元素
    for line in lines:
        line = line.rstrip()
        
        if not line:
            story.append(Spacer(1, 0.3*cm))
            continue
        
        # 处理标题
        if line.startswith('# '):
            title = line[2:].strip()
            if chinese_font_registered:
                from reportlab.platypus import Paragraph
                story.append(Paragraph(title, styles['ChineseTitle']))
            else:
                story.append(Paragraph(title, styles['Heading1']))
            story.append(Spacer(1, 0.5*cm))
        elif line.startswith('## '):
            title = line[3:].strip()
            if chinese_font_registered:
                story.append(Paragraph(title, styles['ChineseHeading1']))
            else:
                story.append(Paragraph(title, styles['Heading2']))
            story.append(Spacer(1, 0.4*cm))
        elif line.startswith('### '):
            title = line[4:].strip()
            if chinese_font_registered:
                story.append(Paragraph(title, styles['ChineseHeading2']))
            else:
                story.append(Paragraph(title, styles['Heading3']))
            story.append(Spacer(1, 0.3*cm))
        else:
            # 处理普通文本
            # 简单的markdown处理（转义特殊字符）
            text = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            if chinese_font_registered:
                story.append(Paragraph(text, styles['ChineseNormal']))
            else:
                story.append(Paragraph(text, styles['Normal']))
    
    doc.build(story)
    print(f"✅ PDF已生成: {output_pdf}")
    return output_pdf


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python markdown_to_pdf.py <markdown_file> [output_pdf]")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"❌ 文件不存在: {md_file}")
        sys.exit(1)
    
    output_pdf = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    try:
        markdown_to_pdf_using_html(md_file, output_pdf)
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

