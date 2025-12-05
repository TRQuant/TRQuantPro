#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Extension - Dashboard启动脚本
=====================================

启动独立的文件管理系统Web服务
此脚本位于extension目录内，可随扩展件打包部署

使用方式:
    python start_dashboard.py
    python start_dashboard.py --port 5000
    python start_dashboard.py --debug
"""

import sys
import argparse
import webbrowser
import threading
import time
from pathlib import Path

# 添加当前目录到路径
EXTENSION_ROOT = Path(__file__).parent
sys.path.insert(0, str(EXTENSION_ROOT))


def open_browser(port: int):
    """延迟打开浏览器"""
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{port}')


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TRQuant Extension Dashboard')
    parser.add_argument('--host', default='127.0.0.1', help='服务器地址')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    args = parser.parse_args()
    
    # 检查依赖
    try:
        from flask import Flask
    except ImportError:
        print("❌ 错误: Flask未安装")
        print("请运行: pip install flask flask-cors")
        sys.exit(1)
    
    # 导入服务器
    try:
        from dashboard.server import run_server
    except ImportError as e:
        print(f"❌ 导入Dashboard服务失败: {e}")
        sys.exit(1)
    
    # 在后台线程中打开浏览器
    if not args.no_browser:
        threading.Thread(target=open_browser, args=(args.port,), daemon=True).start()
    
    # 启动服务
    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()























































