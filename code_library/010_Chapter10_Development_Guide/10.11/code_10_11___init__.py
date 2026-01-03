"""
文件名: code_10_11___init__.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# GUI通过kb_server查询知识库
from mcp_servers.kb_server import KBServer

class AIPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.kb_server = KBServer()
    
    def query_knowledge(self, question):
        results = self.kb_server.query(
            query=question,
            scope="manual",
            top_k=5
        )
        return results