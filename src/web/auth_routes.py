#!/usr/bin/env python3
"""
Authentication Routes - 认证相关路由
"""

from flask import Blueprint, jsonify, request, render_template_string
from .auth import (
    User, login_user, logout_user, login_required, current_user,
    role_required, admin_permission, user_permission
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 登录页面模板
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - PyQt6 Web App</title>
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
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus { outline: none; border-color: #667eea; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .demo-accounts {
            margin-top: 24px;
            padding: 16px;
            background: #f5f5f5;
            border-radius: 8px;
            font-size: 13px;
        }
        .demo-accounts h4 { margin-bottom: 12px; color: #333; }
        .demo-accounts code {
            background: #263238;
            color: #4fc3f7;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .demo-accounts p { margin: 6px 0; color: #666; }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔐 用户登录</h1>
        <div class="error" id="error"></div>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" name="username" required placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" name="password" required placeholder="请输入密码">
            </div>
            <button type="submit">登录</button>
        </form>
        <div class="demo-accounts">
            <h4>📋 测试账号</h4>
            <p><code>admin</code> / <code>admin123</code> - 管理员</p>
            <p><code>editor</code> / <code>editor123</code> - 编辑</p>
            <p><code>user</code> / <code>user123</code> - 普通用户</p>
        </div>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = '/auth/dashboard';
                } else {
                    document.getElementById('error').textContent = data.error || '登录失败';
                    document.getElementById('error').style.display = 'block';
                }
            } catch (err) {
                document.getElementById('error').textContent = '网络错误，请重试';
                document.getElementById('error').style.display = 'block';
            }
        });
    </script>
</body>
</html>
'''

# 控制台模板
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>控制台 - PyQt6 Web App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 24px; }
        .header-right { display: flex; align-items: center; gap: 20px; }
        .user-info { display: flex; align-items: center; gap: 10px; }
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
        }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .logout-btn:hover { background: rgba(255,255,255,0.3); }
        .container { padding: 40px; max-width: 1200px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card h2 { color: #333; margin-bottom: 20px; }
        .api-list { list-style: none; }
        .api-list li {
            padding: 12px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .api-list li:last-child { border-bottom: none; }
        code {
            background: #263238;
            color: #4fc3f7;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 13px;
        }
        .status { color: #4caf50; font-weight: 500; }
        .restricted { color: #ff9800; }
        .admin-only { color: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 控制台</h1>
        <div class="header-right">
            <div class="user-info">
                <span id="username">加载中...</span>
                <span class="badge" id="roles">-</span>
            </div>
            <button class="logout-btn" onclick="logout()">退出登录</button>
        </div>
    </div>
    <div class="container">
        <div class="card">
            <h2>🔐 API 权限说明</h2>
            <ul class="api-list">
                <li>
                    <code>GET /api/status</code>
                    <span class="status">✅ 公开</span>
                </li>
                <li>
                    <code>GET /auth/profile</code>
                    <span class="restricted">🔒 需登录</span>
                </li>
                <li>
                    <code>GET /auth/users</code>
                    <span class="admin-only">👑 仅管理员</span>
                </li>
            </ul>
        </div>
    </div>
    <script>
        async function loadUser() {
            const response = await fetch('/auth/profile');
            if (response.ok) {
                const data = await response.json();
                document.getElementById('username').textContent = data.username;
                document.getElementById('roles').textContent = data.roles.join(', ');
            } else {
                window.location.href = '/auth/login';
            }
        }
        
        async function logout() {
            await fetch('/auth/logout', { method: 'POST' });
            localStorage.removeItem('user');
            window.location.href = '/auth/login';
        }
        
        loadUser();
    </script>
</body>
</html>
'''


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """登录页面和登录处理"""
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
    
    # POST 处理
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    user = User.get_by_username(username)
    
    if user and user.password == password:
        login_user(user)
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'roles': user.roles,
                'email': user.email
            }
        })
    
    return jsonify({'error': '用户名或密码错误'}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """登出"""
    logout_user()
    return jsonify({'success': True, 'message': '已退出登录'})


@auth_bp.route('/profile')
@login_required
def profile():
    """获取当前用户信息"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'roles': current_user.roles,
        'email': current_user.email
    })


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """用户控制台"""
    return render_template_string(DASHBOARD_TEMPLATE)


@auth_bp.route('/users')
@role_required('admin')
def list_users():
    """获取用户列表（仅管理员）"""
    users = []
    for user_data in User.USERS.values():
        users.append({
            'id': user_data['id'],
            'username': user_data['username'],
            'roles': user_data['roles'],
            'email': user_data['email']
        })
    return jsonify({'users': users})


@auth_bp.route('/check-role/<role>')
@login_required
def check_role(role):
    """检查当前用户是否拥有指定角色"""
    return jsonify({
        'has_role': current_user.has_role(role),
        'role': role,
        'user_roles': current_user.roles
    })
