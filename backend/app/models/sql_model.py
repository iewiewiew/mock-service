#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/22 08:54
@description
"""

from ..core.database import db, datetime, tz_beijing


class SQLTemplate(db.Model):
    __tablename__ = 'sql_templates'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='模板名称')
    description = db.Column(db.Text, comment='描述')
    sql_content = db.Column(db.Text, nullable=False, comment='SQL内容')
    category = db.Column(db.String(50), nullable=False, comment='分类')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self):
        """
        将SQL模板对象转换为字典

        Returns:
            dict: SQL模板数据的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sql_content': self.sql_content,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<SQLTemplate {self.name}>'


class QueryHistory(db.Model):
    __tablename__ = 'query_history'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    sql_query = db.Column(db.Text, nullable=False, comment='SQL查询语句')
    execution_time = db.Column(db.Float, comment='执行时间（秒）')
    success = db.Column(db.Boolean, default=True, comment='是否成功')
    error_message = db.Column(db.Text, comment='错误信息')
    connection_id = db.Column(db.Integer, db.ForeignKey('database_connections.id'), nullable=True, comment='连接ID')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')

    def to_dict(self):
        """
        将查询历史对象转换为字典

        Returns:
            dict: 查询历史数据的字典表示
        """
        return {
            'id': self.id,
            'sql_query': self.sql_query,
            'execution_time': self.execution_time,
            'success': self.success,
            'error_message': self.error_message,
            'connection_id': self.connection_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<QueryHistory {self.id}>'
