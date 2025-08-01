# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/8/5 10:27
@description  API端点模型实体类
"""

from datetime import datetime

from ..core.database import db


class ApiEndpoint(db.Model):
    __tablename__ = 'api_endpoints'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False, default='default')
    parent_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    parameters = db.relationship('ApiParameter', backref='endpoint', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {'id': self.id, 'path': self.path, 'method': self.method, 'summary': self.summary,
            'description': self.description, 'category': self.category, 'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'parameters_count': len(self.parameters)}

    def __repr__(self):
        return f'<ApiEndpoint {self.method} {self.path}>'
