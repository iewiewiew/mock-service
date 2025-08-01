# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/8/5 10:27
@description  API参数模型实体类
"""

from datetime import datetime

from ..core.database import db


class ApiParameter(db.Model):
    __tablename__ = 'api_parameters'

    id = db.Column(db.Integer, primary_key=True)
    endpoint_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    param_type = db.Column(db.String(50), nullable=False)  # query/path/body/header
    data_type = db.Column(db.String(50), nullable=False, default='string')
    required = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    example = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'endpoint_id': self.endpoint_id, 'name': self.name, 'param_type': self.param_type,
            'data_type': self.data_type, 'required': self.required, 'description': self.description,
            'example': self.example, 'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}

    def __repr__(self):
        return f'<ApiParameter {self.name} ({self.param_type})>'
