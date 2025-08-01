#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  Mock实体类
"""

from sqlalchemy import UniqueConstraint

from ..core.database import db, datetime, tz_beijing


class Mock(db.Model):
    __tablename__ = 'mocks'

    __table_args__ = (UniqueConstraint('path', 'method', name='uq_path_method'),)

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='Mock名称')
    path = db.Column(db.String(200), unique=False, nullable=False, comment='路径')
    method = db.Column(db.String(10), nullable=False, comment='HTTP方法：GET, POST, PUT, DELETE')
    response_status = db.Column(db.Integer, nullable=False, comment='响应状态码')
    response_body = db.Column(db.Text, nullable=False, comment='响应体')
    response_delay = db.Column(db.Integer, default=0, comment='响应延迟（毫秒）')
    description = db.Column(db.Text, comment='描述')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目ID')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self):
        """
        将Mock对象转换为字典

        Returns:
            dict: Mock数据的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'method': self.method,
            'response_status': self.response_status,
            'response_body': self.response_body,
            'response_delay': self.response_delay,
            'description': self.description,
            'project_id': self.project_id,
            'project_name': self.projects.name if self.projects else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Mock {self.method} {self.path}>'
