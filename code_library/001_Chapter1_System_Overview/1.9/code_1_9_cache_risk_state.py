"""
文件名: code_1_9_cache_risk_state.py
保存路径: code_library/001_Chapter1_System_Overview/1.9/code_1_9_cache_risk_state.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.9_Database_Architecture_CN.md
提取时间: 2025-12-13 20:18:07
函数/类名: cache_risk_state

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 风控状态缓存（TTL: 1小时）
def cache_risk_state(account_id: int, state: dict):
    key = f"risk:state:{account_id}"
    r.setex(key, 3600, json.dumps(state))  # 1小时过期

# 获取风控状态
def get_risk_state(account_id: int):
    key = f"risk:state:{account_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None