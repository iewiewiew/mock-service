#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/21 10:04
@description
"""

from ..core.database import db, datetime, tz_beijing


class Example(db.Model):
    __tablename__ = 'examples'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='名称')
    description = db.Column(db.Text, comment='描述')
    status = db.Column(db.String(20), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self):
        """
        将示例对象转换为字典

        Returns:
            dict: 示例数据的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Example {self.name}>'
