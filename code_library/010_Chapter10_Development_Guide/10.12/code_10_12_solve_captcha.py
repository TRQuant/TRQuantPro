"""
文件名: code_10_12_solve_captcha.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12_solve_captcha.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: solve_captcha

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# 使用OCR识别验证码（示例）
from PIL import Image
import pytesseract

def solve_captcha(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text