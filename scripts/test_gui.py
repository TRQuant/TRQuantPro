#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI测试脚本
==========

测试TRQuant GUI功能
"""

import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_gui():
    """测试GUI"""
    try:
        from PyQt6.QtWidgets import QApplication
        from gui.main_window_v2 import MainWindowV2
        
        logger.info("=" * 60)
        logger.info("TRQuant GUI 测试")
        logger.info("=" * 60)
        
        # 创建应用
        app = QApplication(sys.argv)
        app.setApplicationName("TRQuant")
        app.setApplicationVersion("2.0.0")
        
        logger.info("✅ QApplication创建成功")
        
        # 创建主窗口
        window = MainWindowV2()
        logger.info("✅ MainWindowV2创建成功")
        
        # 显示窗口
        window.show()
        logger.info("✅ 窗口已显示")
        logger.info("")
        logger.info("GUI测试启动成功！")
        logger.info("=" * 60)
        
        # 运行应用
        sys.exit(app.exec())
        
    except ImportError as e:
        logger.error(f"❌ 导入失败: {e}")
        logger.error("请确保已安装PyQt6: pip install PyQt6")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ GUI启动失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    test_gui()
