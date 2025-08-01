#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  项目实体类
"""

from ..core.database import db, datetime, tz_beijing


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, unique=True, comment='项目名称')
    description = db.Column(db.Text, comment='项目描述')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    # 与Mock的关联关系
    mock = db.relationship('Mock', backref='projects', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """
        将项目对象转换为字典

        Returns:
            dict: 项目数据的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'mock_count': len(self.mock),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Project {self.name}>'
