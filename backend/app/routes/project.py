# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/1 19:15
@description
"""

from flask import Blueprint, request, jsonify

from ..services.project_service import ProjectService

project_bp = Blueprint('project', __name__)
project_service = ProjectService()


@project_bp.route('/project', methods=['GET'])
def get_all_projects():
    """获取所有项目"""
    try:
        projects = project_service.get_all_projects()
        return jsonify(projects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects', methods=['GET'])
def get_projects_by_pages():
    """分页获取项目列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name')
        result = project_service.get_projects_by_pages(page, per_page, name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    """根据 ID 获取项目"""
    try:
        project = project_service.get_project_by_id(project_id)
        return jsonify(project)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@project_bp.route('/projects', methods=['POST'])
def create_project():
    """创建项目"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        project = project_service.create_project(data)
        return jsonify(project), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    try:
        data = request.get_json()
        project = project_service.update_project(project_id, data)
        return jsonify(project)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    try:
        project_service.delete_project(project_id)
        return jsonify({'message': 'Project deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@project_bp.route('/projects/<int:project_id>/mock-apis', methods=['GET'])
def get_project_mock_apis(project_id):
    """获取项目的 Mock API 列表"""
    try:
        mock_apis = project_service.get_project_mock_apis(project_id)
        return jsonify(mock_apis)
    except Exception as e:
        return jsonify({'error': str(e)}), 404
