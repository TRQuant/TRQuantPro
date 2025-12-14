"""
文件名: code_10_10_cached_query.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_cached_query.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: cached_query

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 缓存查询结果
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query: str, scope: str, top_k: int):
        """
    cached_query函数
    
    **设计原理**：
    - **核心功能**：实现cached_query的核心逻辑
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
    return kb.query(query, scope, top_k)

# 异步检索
import asyncio

async def async_query(query: str, scope: str, top_k: int):
    """异步查询"""
    tasks = []
    if scope in ["manual", "both"]:
        tasks.append(self._async_vector_search(query, "manual", top_k))
    if scope in ["engineering", "both"]:
        tasks.append(self._async_vector_search(query, "engineering", top_k))
    
    results = await asyncio.gather(*tasks)
    return self._merge_results(*results)