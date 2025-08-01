# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/21 10:04
@description
"""

from ..core.database import db, datetime, tz_beijing


class Example(db.Model):
    __tablename__ = 'examples'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
        onupdate=lambda: datetime.now(tz_beijing), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}
