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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    parameter_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
        onupdate=lambda: datetime.now(tz_beijing), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    parameters = db.relationship('EnvironmentParameter', backref='environments', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'base_url': self.base_url, 'description': self.description or '',
            'parameter_count': self.parameter_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None, 'is_deleted': self.is_deleted}


class EnvironmentParameter(db.Model):
    __tablename__ = 'environment_parameters'

    id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer, db.ForeignKey('environments.id'), nullable=False)
    param_key = db.Column(db.String(100), nullable=False)
    param_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
        onupdate=lambda: datetime.now(tz_beijing), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {'id': self.id, 'environment_id': self.environment_id, 'param_key': self.param_key,
            'param_value': self.param_value, 'description': self.description or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None, 'is_deleted': self.is_deleted}
