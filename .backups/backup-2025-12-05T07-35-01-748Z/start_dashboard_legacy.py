#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
韬睿量化 - 旧版文件管理系统启动脚本
使用端口5001启动完整的Web Dashboard（107513行代码版本）
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
    from dashboard.dashboard_server import app
    
    port = 5001  # 使用不同端口避免冲突
    
    print(f"=" * 60)
    print(f"📊 量化投资文件管理系统（旧版）")
    print(f"=" * 60)
    print(f"  • 端口: {port}")
    print(f"  • 地址: http://127.0.0.1:{port}")
    print(f"  • dashboard_server.py: 107513行代码")
    print(f"=" * 60)
    
    # 在后台线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Flask服务
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)


if __name__ == '__main__':
    main()

