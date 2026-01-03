"""
文件名: code_10_7_get_resource.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_get_resource.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: get_resource

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

async def get_resource(self, uri: str) -> dict:
        """
    get_resource函数
    
    **设计原理**：
    - **核心功能**：实现get_resource的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    if uri.startswith("file://"):
        # 文件资源
        file_path = uri.replace("file://", "")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "content": [{
                "type": "text",
                "text": content
            }]
        }
    elif uri.startswith("https://"):
        # URL资源
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                content = await response.text()
        return {
            "content": [{
                "type": "text",
                "text": content
            }]
        }
    else:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"不支持的资源类型: {uri}"}]
        }