# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/1 19:14
@description
"""

from flask import Blueprint, request, jsonify
from ..services.api_docs_service import ApiDocsService

api_docs_bp = Blueprint('api_docs', __name__)
api_docs_service = ApiDocsService()


@api_docs_bp.route('/api-docs/refresh', methods=['POST'])
def refresh_docs():
    """刷新API文档 - 从Gitee获取最新文档并更新数据库"""
    result = api_docs_service.refresh_docs()
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints', methods=['GET'])
def get_endpoints():
    """获取所有接口端点列表"""
    result = api_docs_service.get_endpoints()
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints/categories', methods=['GET'])
def get_endpoints_by_categories():
    """按分类获取接口端点（用于目录树）"""
    result = api_docs_service.get_endpoints_by_categories()
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints/<int:endpoint_id>', methods=['GET'])
def get_endpoint_detail(endpoint_id):
    """获取特定接口端点的详细信息"""
    result = api_docs_service.get_endpoint_detail(endpoint_id)
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints', methods=['POST'])
def create_endpoint():
    """创建新的接口端点"""
    data = request.get_json()
    result = api_docs_service.create_endpoint(data)
    status_code = 201 if result['code'] == 0 else (409 if '已存在' in result['message'] else 500)
    return jsonify(result), status_code


@api_docs_bp.route('/api-docs/endpoints/<int:endpoint_id>', methods=['PUT'])
def update_endpoint(endpoint_id):
    """更新接口端点"""
    data = request.get_json()
    result = api_docs_service.update_endpoint(endpoint_id, data)
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints/<int:endpoint_id>', methods=['DELETE'])
def delete_endpoint(endpoint_id):
    """删除接口端点"""
    result = api_docs_service.delete_endpoint(endpoint_id)
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints/<int:endpoint_id>/parameters', methods=['GET'])
def get_endpoint_parameters(endpoint_id):
    """获取接口端点的所有参数"""
    result = api_docs_service.get_endpoint_parameters(endpoint_id)
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)


@api_docs_bp.route('/api-docs/endpoints/<int:endpoint_id>/test', methods=['POST'])
def test_endpoint(endpoint_id):
    """测试接口端点"""
    data = request.get_json() or {}
    result = api_docs_service.test_endpoint(endpoint_id, data)
    return jsonify(result) if result['code'] == 0 else (jsonify(result), 500)