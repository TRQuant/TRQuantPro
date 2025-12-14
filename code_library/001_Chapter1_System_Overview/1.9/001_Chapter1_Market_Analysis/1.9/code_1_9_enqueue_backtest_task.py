"""
文件名: code_1_9_enqueue_backtest_task.py
保存路径: code_library/001_Chapter1_System_Overview/1.9/001_Chapter1_Market_Analysis/1.9/code_1_9_enqueue_backtest_task.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.9_Database_Architecture_CN.md
提取时间: 2025-12-13 20:05:31
函数/类名: enqueue_backtest_task

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 回测任务队列
def enqueue_backtest_task(backtest_id: int, config: dict):
    r.lpush("queue:backtest", json.dumps({
        "backtest_id": backtest_id,
        "config": config,
        "created_at": datetime.now().isoformat()
    }))

# 处理回测任务
def process_backtest_queue():
    while True:
        task_data = r.brpop("queue:backtest", timeout=1)
        if task_data:
            task = json.loads(task_data[1])
            # 处理任务
            process_backtest(task)