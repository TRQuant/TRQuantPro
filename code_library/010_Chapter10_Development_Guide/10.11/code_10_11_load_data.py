"""
文件名: code_10_11_load_data.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_load_data.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: load_data

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import logging

logger = logging.getLogger(__name__)

def load_data(self):
    logger.info("开始加载数据")
    try:
        data = self._fetch_data()
        logger.info(f"成功加载 {len(data)} 条记录")
        return data
    except Exception as e:
        logger.error(f"加载失败: {e}", exc_info=True)
        raise