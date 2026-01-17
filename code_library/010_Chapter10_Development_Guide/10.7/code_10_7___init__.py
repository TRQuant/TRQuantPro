"""
文件名: code_10_7___init__.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# mcp_servers/kb_server.py
class KBMCPServer:
    """知识库MCP服务器"""
    
    def __init__(self):
        # 初始化知识库服务
        self.kb_server = KBServer()
        
        # 加载reranker（可选）
        try:
            self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except:
            self.reranker = None
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        if name == "kb.query":
            # 1. 参数验证
            query = arguments.get("query")
            if not query:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": "查询文本不能为空"}]
                }
            
            # 2. 调用底层服务
            results = self.kb_server.query(
                query=query,
                scope=arguments.get("scope", "both"),
                top_k=arguments.get("top_k", 10),
                use_reranker=arguments.get("use_reranker", False)
            )
            
            # 3. 格式化返回
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(results, ensure_ascii=False, indent=2)
                }]
            }