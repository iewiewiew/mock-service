#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/8/5 10:27
@description  API端点模型实体类
"""

from ..core.database import db, datetime, tz_beijing


class ApiEndpoint(db.Model):
    __tablename__ = 'api_endpoints'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    path = db.Column(db.String(255), nullable=False, comment='API路径')
    method = db.Column(db.String(10), nullable=False, comment='HTTP方法')
    summary = db.Column(db.Text, comment='摘要')
    description = db.Column(db.Text, comment='描述')
    category = db.Column(db.String(100), nullable=False, default='default', comment='分类')
    parent_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'), comment='父节点ID')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    # 关系
    parameters = db.relationship('ApiParameter', backref='endpoint', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """
        将API端点对象转换为字典

        Returns:
            dict: API端点数据的字典表示
        """
        return {
            'id': self.id,
            'path': self.path,
            'method': self.method,
            'summary': self.summary,
            'description': self.description,
            'category': self.category,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'parameters_count': len(self.parameters)
        }

    def __repr__(self):
        return f'<ApiEndpoint {self.method} {self.path}>'
