#!/usr/bin/env python3
"""
Flask Web Application
Provides REST API and web interface for the application
"""

from flask import Flask, jsonify, request, render_template_string
import os
import sys
from .auth import init_auth


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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 初始化认证模块
init_auth(app)

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
        .login-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .footer { margin-top: 30px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 PyQt6 Web App Server</h1>
        <p class="subtitle">Flask-based web service with Authentication</p>
        <div class="status">✅ 服务运行中</div>
        <div class="api-list">
            <h3>API 端点</h3>
            <div class="api-item"><code>GET /</code> - 首页</div>
            <div class="api-item"><code>GET /api/status</code> - 服务状态</div>
            <div class="api-item"><code>GET /api/info</code> - 应用信息</div>
            <div class="api-item"><code>POST /api/navigate</code> - 导航控制</div>
            <div class="api-item"><code>GET /auth/login</code> - 登录页面</div>
            <div class="api-item"><code>GET /auth/dashboard</code> - 用户控制台 🔒</div>
        </div>
        <a href="/auth/login" class="login-btn">🔐 登录</a>
        <div class="footer">
            Powered by Flask & PyQt6 | Flask-Login & Flask-Principal
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


def register_blueprints(app):
    """注册所有蓝图"""
    from .routes import register_blueprints as register_api
    from .auth_routes import auth_bp
    
    register_api(app)
    app.register_blueprint(auth_bp)
    
    return app


def create_app():
    """应用工厂函数"""
    register_blueprints(app)
    return app


def run_server(host='127.0.0.1', port=5000, debug=False):
    """启动 Flask 服务器"""
    # 确保蓝图已注册
    register_blueprints(app)
    print(f"🌐 Flask server starting at http://{host}:{port}")
    print(f"🔐 Auth module enabled - Login at http://{host}:{port}/auth/login")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
