#!/usr/bin/env python3
"""
Web Routes - Additional route definitions
"""

from flask import Blueprint, jsonify, request

# 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'pyqt6-webapp'
    })


@api_bp.route('/browser/history', methods=['GET', 'POST'])
def browser_history():
    """浏览器历史记录"""
    if request.method == 'POST':
        # 添加历史记录
        data = request.get_json() or {}
        return jsonify({
            'success': True,
            'message': 'History recorded'
        })
    else:
        # 获取历史记录
        return jsonify({
            'history': [],
            'total': 0
        })


@api_bp.route('/browser/bookmarks', methods=['GET', 'POST', 'DELETE'])
def bookmarks():
    """书签管理"""
    if request.method == 'GET':
        return jsonify({
            'bookmarks': [
                {'id': 1, 'title': '百度', 'url': 'https://www.baidu.com'},
                {'id': 2, 'title': 'Google', 'url': 'https://www.google.com'},
            ]
        })
    elif request.method == 'POST':
        data = request.get_json() or {}
        return jsonify({
            'success': True,
            'bookmark': data
        }), 201
    else:
        return jsonify({'success': True, 'message': 'Bookmark deleted'})


def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(api_bp)
