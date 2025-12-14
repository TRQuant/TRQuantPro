"""
文件名: code_10_11_示例.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_Development_Methodology_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 方案设计示例
solution = {
    "problem": "Gist文件无法自动加载",
    "root_cause": "文件名必须是code.mmd",
    "solution": {
        "step1": "创建新的Gist，使用code.mmd文件名",
        "step2": "更新脚本，自动将文件名改为code.mmd",
        "step3": "更新链接，使用新的Gist ID"
    },
    "verification": {
        "criteria": "代码可以自动加载",
        "test": "使用Playwright验证编辑器内容"
    }
}