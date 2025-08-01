#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/27 15:17
@description
"""

from flask import Blueprint, request, jsonify

from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '用户名和密码不能为空'}), 400

    user = AuthService.authenticate_user(data['username'], data['password'])
    if not user:
        return jsonify({'message': '用户名或密码错误'}), 401

    token = AuthService.generate_token(user)

    return jsonify({'message': '登录成功', 'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'message': 'Token格式错误'}), 401

    if not token:
        return jsonify({'message': 'Token缺失'}), 401

    user = AuthService.get_current_user(token)

    if not user:
        return jsonify({'message': 'Token无效或已过期'}), 401

    user_data = AuthService.get_current_user_with_permissions(token)
    if user_data:
        return jsonify({'user': user_data})
