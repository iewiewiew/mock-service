#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/8/5 10:27
@description  API参数模型实体类
"""

from ..core.database import db, datetime, tz_beijing


class ApiParameter(db.Model):
    __tablename__ = 'api_parameters'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    endpoint_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'), nullable=False, comment='端点ID')
    name = db.Column(db.String(100), nullable=False, comment='参数名称')
    param_type = db.Column(db.String(50), nullable=False, comment='参数类型：query/path/body/header')
    data_type = db.Column(db.String(50), nullable=False, default='string', comment='数据类型')
    required = db.Column(db.Boolean, default=False, comment='是否必填')
    description = db.Column(db.Text, comment='描述')
    example = db.Column(db.String(255), comment='示例值')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self):
        """
        将API参数对象转换为字典

        Returns:
            dict: API参数数据的字典表示
        """
        return {
            'id': self.id,
            'endpoint_id': self.endpoint_id,
            'name': self.name,
            'param_type': self.param_type,
            'data_type': self.data_type,
            'required': self.required,
            'description': self.description,
            'example': self.example,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<ApiParameter {self.name} ({self.param_type})>'
