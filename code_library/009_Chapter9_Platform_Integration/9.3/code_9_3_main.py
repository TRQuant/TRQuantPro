"""
文件名: code_9_3_main.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.3/code_9_3_main.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.3_Desktop_System_Architecture_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: main

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# TRQuant.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韬睿量化专业版 - TaoRui Quant Professional
双击此文件启动应用
"""
import sys
import os
import logging
from pathlib import Path

# 设置项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# 配置日志
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

log_file = logs_dir / "trquant.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
        """
    main函数
    
    **设计原理**：
    - **核心功能**：实现main的核心逻辑
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
    from PyQt6.QtWidgets import QApplication
    from gui.main_window import MainWindow
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("韬睿量化专业版")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()