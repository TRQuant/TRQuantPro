"""
文件名: code_6_4_start_daily_pipeline.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4_start_daily_pipeline.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: start_daily_pipeline

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import schedule
import time

def start_daily_pipeline(
    pipeline: FactorPipeline,
    run_time: str = "18:00",  # 默认收盘后运行
    stock_pool: str = "all_a"
):
        """
    start_daily_pipeline函数
    
    **设计原理**：
    - **核心功能**：实现start_daily_pipeline的核心逻辑
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
    pipeline.stock_pool = stock_pool
    
    def run_daily():
        """每日运行函数"""
        logger.info(f"开始每日因子计算流水线: {datetime.now()}")
        try:
            result = pipeline.run_pipeline()
            logger.info(f"每日流水线完成: {result}")
        except Exception as e:
            logger.error(f"每日流水线失败: {e}")
    
    # 配置定时任务
    schedule.every().day.at(run_time).do(run_daily)
    
    logger.info(f"定时任务已配置: 每日 {run_time} 运行")
    
    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次