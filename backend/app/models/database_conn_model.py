#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/01/26
@description  数据库连接实体类
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from ..core.database import db, datetime, tz_beijing


class DatabaseConnection(db.Model):
    """数据库连接模型"""
    __tablename__ = 'database_connections'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='连接名称')
    host = db.Column(db.String(255), nullable=False, comment='数据库主机')
    port = db.Column(db.Integer, nullable=False, default=3306, comment='数据库端口')
    database = db.Column(db.String(100), nullable=False, comment='数据库名称')
    username = db.Column(db.String(100), nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    driver = db.Column(db.String(50), nullable=False, default='mysql', comment='数据库驱动')
    charset = db.Column(db.String(50), default='utf8mb4', comment='字符集')
    description = db.Column(db.Text, comment='描述')
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否激活')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                            onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    def to_dict(self, exclude_password=True):
        """转换为字典，默认隐藏密码"""
        # 格式化时间为字符串，去掉时区信息，直接显示本地时间
        def format_datetime(dt):
            if dt is None:
                return None
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        result = {
            'id': self.id,
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'username': self.username,
            'password': self.password if not exclude_password else '******',
            'driver': self.driver,
            'charset': self.charset,
            'description': self.description or '',
            'is_active': self.is_active,
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at)
        }
        return result

    def get_connection_string(self):
        """获取数据库连接字符串"""
        driver = (self.driver or 'mysql').lower()
        if driver in ('mysql', 'pymysql'):
            dialect = 'mysql+pymysql'
        elif driver in ('mysqlconnector', 'mysql+mysqlconnector'):
            dialect = 'mysql+mysqlconnector'
        elif driver in ('postgresql', 'postgres'):
            dialect = 'postgresql'
        else:
            # 默认回退到 PyMySQL 以避免 MySQLdb 依赖
            dialect = 'mysql+pymysql'

        return f"{dialect}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"

    def __repr__(self):
        return f'<DatabaseConnection {self.name}>'
