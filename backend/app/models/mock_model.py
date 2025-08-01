#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  Mock实体类
"""

from sqlalchemy import UniqueConstraint

from ..core.database import db, tz_beijing


class Mock(db.Model):
    __tablename__ = 'mocks'

    __table_args__ = (UniqueConstraint('path', 'method', name='uq_path_method'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), unique=False, nullable=False)
    method = db.Column(db.String(10), nullable=False)  # GET, POST, PUT, DELETE
    response_status = db.Column(db.Integer, nullable=False)
    response_body = db.Column(db.Text, nullable=False)
    response_delay = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)  # @todo
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
        onupdate=lambda: datetime.now(tz_beijing), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'path': self.path, 'method': self.method,
            'response_status': self.response_status, 'response_body': self.response_body,
            'response_delay': self.response_delay, 'description': self.description, 'project_id': self.project_id,
            'project_name': self.projects.name if self.projects else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}
