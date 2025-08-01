#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  环境配置实体类
"""

from ..core.database import db, datetime, tz_beijing


class Environment(db.Model):
    __tablename__ = 'environments'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='环境名称')
    base_url = db.Column(db.String(500), nullable=False, comment='基础URL')
    username = db.Column(db.String(100), comment='用户名')
    password = db.Column(db.String(500), comment='密码')
    description = db.Column(db.Text, comment='描述')
    parameter_count = db.Column(db.Integer, default=0, comment='参数数量')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')
    is_deleted = db.Column(db.Boolean, default=False, comment='是否删除')

    parameters = db.relationship('EnvironmentParameter', backref='environments', lazy=True)

    def to_dict(self):
        """
        将环境对象转换为字典

        Returns:
            dict: 环境数据的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'base_url': self.base_url,
            'username': self.username or '',
            'password': self.password or '',
            'description': self.description or '',
            'parameter_count': self.parameter_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

    def __repr__(self):
        return f'<Environment {self.name}>'


class EnvironmentParameter(db.Model):
    __tablename__ = 'environment_parameters'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    environment_id = db.Column(db.Integer, db.ForeignKey('environments.id'), nullable=False, comment='环境ID')
    param_key = db.Column(db.String(100), nullable=False, comment='参数键')
    param_value = db.Column(db.Text, nullable=False, comment='参数值')
    description = db.Column(db.String(200), comment='描述')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')
    is_deleted = db.Column(db.Boolean, default=False, comment='是否删除')

    def to_dict(self):
        """
        将环境参数对象转换为字典

        Returns:
            dict: 环境参数数据的字典表示
        """
        return {
            'id': self.id,
            'environment_id': self.environment_id,
            'param_key': self.param_key,
            'param_value': self.param_value,
            'description': self.description or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }

    def __repr__(self):
        return f'<EnvironmentParameter {self.param_key}>'
