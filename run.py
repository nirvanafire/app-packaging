#!/usr/bin/env python3
"""
Main Entry Point with Flask Integration
Supports both GUI and Web Server modes
"""

import sys
import os
import argparse
import threading


def run_gui():
    """运行 PyQt6 GUI 应用"""
    from src.main import main
    main()


def run_web(host='0.0.0.0', port=5000, debug=False):
    """运行 Flask Web 服务"""
    from src.web.app import run_server
    run_server(host=host, port=port, debug=debug)


def run_both(host='0.0.0.0', port=5000):
    """同时运行 GUI 和 Web 服务"""
    # 在后台线程启动 Flask
    web_thread = threading.Thread(
        target=run_web,
        kwargs={'host': host, 'port': port, 'debug': False},
        daemon=True
    )
    web_thread.start()
    
    print(f"🌐 Web server running at http://{host}:{port}")
    
    # 主线程运行 GUI
    run_gui()


def main():
    parser = argparse.ArgumentParser(description='PyQt6 Web Browser with Flask')
    parser.add_argument('--web', action='store_true', help='Run web server only')
    parser.add_argument('--gui', action='store_true', help='Run GUI only (default)')
    parser.add_argument('--both', action='store_true', help='Run both GUI and web server')
    parser.add_argument('--host', default='0.0.0.0', help='Web server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Web server port (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if args.web:
        print("🌐 Starting Flask Web Server...")
        run_web(host=args.host, port=args.port, debug=args.debug)
    elif args.both:
        print("🖥️ Starting GUI + Web Server...")
        run_both(host=args.host, port=args.port)
    else:
        print("🖥️ Starting PyQt6 GUI...")
        run_gui()


if __name__ == '__main__':
    main()
