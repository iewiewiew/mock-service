# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/22 08:54
@description
"""

from ..core.database import db, datetime


class SQLTemplate(db.Model):
    __tablename__ = 'sql_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sql_content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'sql_content': self.sql_content,
            'category': self.category, 'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()}


class DatabaseConnection(db.Model):
    __tablename__ = 'database_connections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    db_type = db.Column(db.String(20), nullable=False)  # mysql, postgresql, sqlite
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    database = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联查询历史
    query_histories = db.relationship('QueryHistory', backref='connection', lazy=True)


class QueryHistory(db.Model):
    __tablename__ = 'query_history'

    id = db.Column(db.Integer, primary_key=True)
    sql_query = db.Column(db.Text, nullable=False)
    execution_time = db.Column(db.Float)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    connection_id = db.Column(db.Integer, db.ForeignKey('database_connections.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'sql_query': self.sql_query, 'execution_time': self.execution_time,
            'success': self.success, 'error_message': self.error_message, 'created_at': self.created_at.isoformat()}
