# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/2 14:04
@description
"""

from urllib.parse import urlencode

import requests

from ..core.database import db
from ..models.api_endpoint_model import ApiEndpoint
from ..models.api_parameter_model import ApiParameter


class ApiDocsService:
    """API文档服务类"""

    # 接口：https://gitee.com/api/v5/swagger
    # 刷新接口: http://localhost:5001/api/api-docs/refresh
    def refresh_docs(self):
        """刷新API文档 - 从Gitee获取最新文档并更新数据库"""
        try:
            response = requests.get('https://gitee.com/api/v5/swagger_doc.json')
            response.raise_for_status()
            data = response.json()

            # 清空现有数据
            ApiParameter.query.delete()
            ApiEndpoint.query.delete()

            # 解析接口信息
            endpoints_created = 0
            parameters_created = 0

            for path, methods in data.get('paths', {}).items():
                for method, details in methods.items():
                    # 提取接口分类信息
                    tags = details.get('tags', ['default'])
                    category = tags[0] if tags else 'default'

                    endpoint = ApiEndpoint(path=path, method=method.upper(), summary=details.get('summary', ''),
                        description=details.get('description', ''), category=category)
                    db.session.add(endpoint)
                    db.session.flush()  # 获取ID
                    endpoints_created += 1

                    # 解析参数
                    for param in details.get('parameters', []):
                        api_param = ApiParameter(endpoint_id=endpoint.id, name=param['name'],
                            param_type=param.get('in', 'query'), data_type=param.get('type', 'string'),
                            required=param.get('required', False), description=param.get('description', ''),
                            example=param.get('example'))
                        db.session.add(api_param)
                        parameters_created += 1

            db.session.commit()

            return {'code': 0, 'message': '文档更新成功',
                'data': {'endpoints_created': endpoints_created, 'parameters_created': parameters_created}}

        except Exception as e:
            db.session.rollback()
            return {'code': 1, 'message': f'文档更新失败: {str(e)}'}

    def get_endpoints(self):
        """获取所有接口端点列表"""
        try:
            endpoints = ApiEndpoint.query.all()
            return {'code': 0, 'message': 'success', 'data': [endpoint.to_dict() for endpoint in endpoints]}
        except Exception as e:
            return {'code': 1, 'message': f'获取接口列表失败: {str(e)}'}

    def get_endpoints_by_categories(self):
        """按分类获取接口端点（用于目录树）"""
        try:
            endpoints = ApiEndpoint.query.all()

            # 按分类分组
            categories = {}
            for endpoint in endpoints:
                if endpoint.category not in categories:
                    categories[endpoint.category] = []

                categories[endpoint.category].append(
                    {'id': endpoint.id, 'path': endpoint.path, 'method': endpoint.method, 'summary': endpoint.summary,
                        'description': endpoint.description, 'parameters_count': len(endpoint.parameters)})

            return {'code': 0, 'message': 'success', 'data': categories}
        except Exception as e:
            return {'code': 1, 'message': f'获取分类接口失败: {str(e)}'}

    def get_endpoint_detail(self, endpoint_id):
        """获取特定接口端点的详细信息"""
        try:
            endpoint = ApiEndpoint.query.get(endpoint_id)
            if not endpoint:
                return {'code': 1, 'message': f'接口端点 {endpoint_id} 不存在'}

            parameters = ApiParameter.query.filter_by(endpoint_id=endpoint_id).all()

            return {'code': 0, 'message': 'success',
                'data': {'endpoint': endpoint.to_dict(), 'parameters': [param.to_dict() for param in parameters]}}
        except Exception as e:
            return {'code': 1, 'message': f'获取接口详情失败: {str(e)}'}

    def create_endpoint(self, data):
        """创建新的接口端点"""
        try:
            if not data or 'path' not in data or 'method' not in data:
                return {'code': 1, 'message': '缺少必要字段: path 和 method'}

            # 检查是否已存在
            existing = ApiEndpoint.query.filter_by(path=data['path'], method=data['method'].upper()).first()

            if existing:
                return {'code': 1, 'message': '接口端点已存在'}

            endpoint = ApiEndpoint(path=data['path'], method=data['method'].upper(), summary=data.get('summary', ''),
                description=data.get('description', ''), category=data.get('category', 'default'))

            db.session.add(endpoint)
            db.session.commit()

            return {'code': 0, 'message': '创建成功', 'data': endpoint.to_dict()}

        except Exception as e:
            db.session.rollback()
            return {'code': 1, 'message': f'创建失败: {str(e)}'}

    def update_endpoint(self, endpoint_id, data):
        """更新接口端点"""
        try:
            endpoint = ApiEndpoint.query.get(endpoint_id)
            if not endpoint:
                return {'code': 1, 'message': f'接口端点 {endpoint_id} 不存在'}

            if 'path' in data:
                endpoint.path = data['path']
            if 'method' in data:
                endpoint.method = data['method'].upper()
            if 'summary' in data:
                endpoint.summary = data['summary']
            if 'description' in data:
                endpoint.description = data['description']
            if 'category' in data:
                endpoint.category = data['category']

            db.session.commit()

            return {'code': 0, 'message': '更新成功', 'data': endpoint.to_dict()}

        except Exception as e:
            db.session.rollback()
            return {'code': 1, 'message': f'更新失败: {str(e)}'}

    def delete_endpoint(self, endpoint_id):
        """删除接口端点"""
        try:
            endpoint = ApiEndpoint.query.get(endpoint_id)
            if not endpoint:
                return {'code': 1, 'message': f'接口端点 {endpoint_id} 不存在'}

            db.session.delete(endpoint)
            db.session.commit()

            return {'code': 0, 'message': '删除成功'}

        except Exception as e:
            db.session.rollback()
            return {'code': 1, 'message': f'删除失败: {str(e)}'}

    def get_endpoint_parameters(self, endpoint_id):
        """获取接口端点的所有参数"""
        try:
            parameters = ApiParameter.query.filter_by(endpoint_id=endpoint_id).all()
            return {'code': 0, 'message': 'success', 'data': [param.to_dict() for param in parameters]}
        except Exception as e:
            return {'code': 1, 'message': f'获取参数失败: {str(e)}'}

    def test_endpoint(self, endpoint_id, data):
        """测试接口端点"""
        try:
            endpoint = ApiEndpoint.query.get(endpoint_id)
            if not endpoint:
                return {'code': 1, 'message': f'接口端点 {endpoint_id} 不存在'}

            # 组织参数
            query_params = {}
            path_params = {}
            body_params = {}
            headers = {'Content-Type': 'application/json', 'User-Agent': 'API-Testing-Tool/1.0'}

            # 处理参数
            for param in endpoint.parameters:
                value = data.get(param.name, '')
                if value:
                    if param.param_type == 'query':
                        query_params[param.name] = value
                    elif param.param_type == 'path':
                        path_params[param.name] = value
                    elif param.param_type == 'body':
                        body_params[param.name] = value
                    elif param.param_type == 'header':
                        headers[param.name] = value

            # 构建URL（替换路径参数）
            url = endpoint.path
            for key, value in path_params.items():
                url = url.replace(f'{{{key}}}', str(value))

            # 构建完整URL（添加查询参数）
            if query_params:
                url += '?' + urlencode(query_params)

            # 发送请求
            request_options = {'method': endpoint.method, 'headers': headers}

            if endpoint.method in ['POST', 'PUT', 'PATCH'] and body_params:
                request_options['json'] = body_params

            response = requests.request(**request_options)

            return {'code': 0, 'message': '测试完成', 'data': {
                'request': {'url': url, 'method': endpoint.method, 'headers': headers,
                    'body': body_params if body_params else None},
                'response': {'status_code': response.status_code, 'headers': dict(response.headers),
                    'data': response.json() if response.content else None}}}

        except Exception as e:
            return {'code': 1, 'message': f'测试失败: {str(e)}'}
