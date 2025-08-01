# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/19 17:10
@description  服务器信息实体类
"""

from ..core.database import db, datetime


class LinuxInfo(db.Model):
    __tablename__ = 'linux_info'

    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(100), nullable=False)
    host = db.Column(db.String(100), nullable=False)
    port = db.Column(db.Integer, default=22)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200))
    private_key = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'server_name': self.server_name, 'host': self.host, 'port': self.port,
            'username': self.username, 'password': self.password, 'private_key': self.private_key,
            'description': self.description, 'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}
