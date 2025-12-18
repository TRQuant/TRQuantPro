"""
文件名: code_1_9_cache_market_snapshot.py
保存路径: code_library/001_Chapter1_System_Overview/1.9/code_1_9_cache_market_snapshot.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.9_Database_Architecture_CN.md
提取时间: 2025-12-13 20:18:07
函数/类名: cache_market_snapshot

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# 缓存实时行情数据（TTL: 60秒）
def cache_market_snapshot(symbol: str, data: dict):
    key = f"market:snapshot:{symbol}"
    r.setex(key, 60, json.dumps(data))  # 60秒过期

# 获取缓存行情
def get_market_snapshot(symbol: str):
    key = f"market:snapshot:{symbol}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None