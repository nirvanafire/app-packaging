#!/usr/bin/env python3
"""
Flask Web Application
Provides REST API and web interface for the application
"""

from flask import Flask, jsonify, request, render_template_string
import os
import sys

# 获取资源路径
def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包后环境"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

# 首页模板
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyQt6 Web App Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 28px; }
        .subtitle { color: #666; margin-bottom: 30px; }
        .status {
            background: #e8f5e9;
            border: 1px solid #4caf50;
            color: #2e7d32;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .api-list {
            text-align: left;
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .api-list h3 { margin-bottom: 15px; color: #333; }
        .api-item {
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }
        .api-item:last-child { border-bottom: none; }
        code {
            background: #263238;
            color: #4fc3f7;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 13px;
        }
        .footer { margin-top: 30px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 PyQt6 Web App Server</h1>
        <p class="subtitle">Flask-based web service</p>
        <div class="status">✅ 服务运行中</div>
        <div class="api-list">
            <h3>API 端点</h3>
            <div class="api-item"><code>GET /</code> - 首页</div>
            <div class="api-item"><code>GET /api/status</code> - 服务状态</div>
            <div class="api-item"><code>GET /api/info</code> - 应用信息</div>
            <div class="api-item"><code>POST /api/navigate</code> - 导航控制</div>
        </div>
        <div class="footer">
            Powered by Flask & PyQt6
        </div>
    </div>
</body>
</html>
'''


@app.route('/')
def home():
    """首页"""
    return render_template_string(HOME_TEMPLATE)


@app.route('/api/status')
def api_status():
    """获取服务状态"""
    return jsonify({
        'status': 'running',
        'service': 'Flask Web Server',
        'version': '1.0.0'
    })


@app.route('/api/info')
def api_info():
    """获取应用信息"""
    return jsonify({
        'name': 'PyQt6 Web Browser',
        'version': '1.0.0',
        'features': [
            'PyQt6 GUI',
            'WebEngine Browser',
            'Flask Web Server',
            'REST API'
        ]
    })


@app.route('/api/navigate', methods=['POST'])
def api_navigate():
    """导航控制 API"""
    data = request.get_json() or {}
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # 这里可以与 PyQt 应用通信
    return jsonify({
        'success': True,
        'url': url,
        'message': f'Navigation request sent to {url}'
    })


def create_app():
    """应用工厂函数"""
    return app


def run_server(host='127.0.0.1', port=5000, debug=False):
    """启动 Flask 服务器"""
    print(f"🌐 Flask server starting at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
