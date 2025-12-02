#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
韬睿量化 - Web仪表盘启动脚本
启动Flask服务并自动打开浏览器
"""

import webbrowser
import threading
import time
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))


def open_browser(port: int):
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')


def main():
    """主函数"""
    from dashboard.dashboard_server import run_server
    
    port = 5000
    
    # 在后台线程中打开浏览器
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # 启动服务
    run_server(host='127.0.0.1', port=port, debug=False)


if __name__ == '__main__':
    main()
