"""
文件名: code_4_4_工具定义.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_工具定义.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 工具定义

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

MCPTool(
    name="data_collector.crawl_web",
    description="爬取网页内容，提取文本和链接",
    input_schema={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "目标网页URL"
            },
            "extract_text": {
                "type": "boolean",
                "description": "是否提取文本内容，默认true",
                "default": true
            },
            "max_depth": {
                "type": "integer",
                "description": "最大爬取深度，默认1",
                "default": 1
            },
            "output_dir": {
                "type": "string",
                "description": "输出目录，默认data/collected",
                "default": "data/collected"
            }
        },
        "required": ["url"]
    }
)