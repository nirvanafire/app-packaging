#!/usr/bin/env python3
"""
Authentication and Authorization Module
基于 Flask-Login 和 Flask-Principal 的权限管理
"""

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded
from functools import wraps
from flask import jsonify, request

# 初始化扩展
login_manager = LoginManager()
principal = Principal()

# 定义角色权限
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
editor_permission = Permission(RoleNeed('editor'))


class User(UserMixin):
    """用户模型"""
    
    # 模拟用户数据库
    USERS = {
        'admin': {
            'id': 1,
            'username': 'admin',
            'password': 'admin123',  # 生产环境应使用哈希
            'roles': ['admin', 'user'],
            'email': 'admin@example.com'
        },
        'user': {
            'id': 2,
            'username': 'user',
            'password': 'user123',
            'roles': ['user'],
            'email': 'user@example.com'
        },
        'editor': {
            'id': 3,
            'username': 'editor',
            'password': 'editor123',
            'roles': ['editor', 'user'],
            'email': 'editor@example.com'
        }
    }
    
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password = user_data['password']
        self.roles = user_data.get('roles', [])
        self.email = user_data.get('email', '')
    
    def has_role(self, role):
        """检查用户是否拥有指定角色"""
        return role in self.roles
    
    @classmethod
    def get(cls, user_id):
        """根据 ID 获取用户"""
        for user_data in cls.USERS.values():
            if user_data['id'] == int(user_id):
                return cls(user_data)
        return None
    
    @classmethod
    def get_by_username(cls, username):
        """根据用户名获取用户"""
        if username in cls.USERS:
            return cls(cls.USERS[username])
        return None


@login_manager.user_loader
def load_user(user_id):
    """加载用户回调"""
    return User.get(user_id)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """加载用户身份和角色"""
    if hasattr(current_user, 'id'):
        identity.user = current_user
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))


def role_required(*roles):
    """角色验证装饰器"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': '需要登录'}), 401
            
            if not any(current_user.has_role(role) for role in roles):
                return jsonify({
                    'error': '权限不足',
                    'required_roles': list(roles),
                    'user_roles': current_user.roles
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def api_key_required(f):
    """API Key 验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        # 模拟 API Key 验证
        valid_keys = ['sk-admin-key', 'sk-user-key', 'sk-test-key']
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 401
        
        if api_key not in valid_keys:
            return jsonify({'error': '无效的 API Key'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def init_auth(app):
    """初始化认证模块"""
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_page'
    login_manager.login_message = '请登录以访问此页面'
    
    principal.init_app(app)
    
    return app
