#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/19 17:10
@description  服务器信息实体类
"""

from ..core.database import db, datetime, tz_beijing


class LinuxInfo(db.Model):
    __tablename__ = 'linux_info'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    server_name = db.Column(db.String(100), nullable=False, comment='服务器名称')
    host = db.Column(db.String(100), nullable=False, comment='主机地址')
    port = db.Column(db.Integer, default=22, comment='端口号')
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    password = db.Column(db.String(200), comment='密码')
    private_key = db.Column(db.Text, comment='私钥')
    description = db.Column(db.Text, comment='描述')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self):
        """
        将服务器信息对象转换为字典

        Returns:
            dict: 服务器信息数据的字典表示
        """
        return {
            'id': self.id,
            'server_name': self.server_name,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'private_key': self.private_key,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<LinuxInfo {self.server_name}>'
