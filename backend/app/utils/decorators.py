#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/27 15:17
@description
"""

from functools import wraps
from flask import request, jsonify
from ..services.auth_service import AuthService
import json


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token格式错误'}), 401

        if not token:
            return jsonify({'message': 'Token缺失'}), 401

        current_user = AuthService.get_current_user(token)
        if not current_user:
            return jsonify({'message': 'Token无效或已过期'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if not hasattr(current_user, 'role') or not current_user.role:
                return jsonify({'message': '用户没有分配角色'}), 403

            permissions = getattr(current_user.role, 'permissions', [])
            if isinstance(permissions, str):
                try:
                    # 方法1：使用 ast.literal_eval 安全地转换
                    import ast
                    permissions = ast.literal_eval(permissions)
                except (ValueError, SyntaxError):
                    # 方法2：如果是逗号分隔的字符串
                    permissions = [p.strip() for p in
                        permissions.strip('[]').replace("'", "").split(',')]  # 或者根据你的实际格式调整

            if not isinstance(permissions, list):
                return jsonify({'message': '权限数据格式错误'}), 500

            if permission not in permissions:
                return jsonify({'message': f'缺少权限: {permission}'}), 403
            else:
                # 用户拥有所需权限，传递所有参数给原始处理函数
                return f(current_user, *args, **kwargs)

        return decorated

    return decorator