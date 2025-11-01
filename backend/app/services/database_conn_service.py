#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/01/26
@description  数据库连接管理服务层
"""

from sqlalchemy import or_, text
from sqlalchemy.exc import IntegrityError

from ..core.database import db
from ..core.exceptions import APIException
from ..models.database_conn_model import DatabaseConnection


class DatabaseConnService:
    @staticmethod
    def get_all_connections(page=1, per_page=10, search=None):
        """获取所有数据库连接（支持分页和搜索）"""
        
        # 基础查询
        query = DatabaseConnection.query.filter_by(is_active=True)
        
        # 添加搜索条件
        if search:
            query = query.filter(
                or_(
                    DatabaseConnection.name.ilike(f'%{search}%'),
                    DatabaseConnection.host.ilike(f'%{search}%'),
                    DatabaseConnection.database.ilike(f'%{search}%'),
                    DatabaseConnection.description.ilike(f'%{search}%')
                )
            )
        
        # 排序和分页
        pagination = query.order_by(DatabaseConnection.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'data': [conn.to_dict() for conn in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_all_connections_for_select():
        """获取所有数据库连接（用于下拉选择，不分页）"""
        connections = DatabaseConnection.query.filter_by(is_active=True).order_by(DatabaseConnection.name.asc()).all()
        return {
            'data': [conn.to_dict() for conn in connections]
        }
    
    @staticmethod
    def get_connection_by_id(connection_id):
        """获取单个数据库连接详情"""
        
        connection = DatabaseConnection.query.filter_by(id=connection_id, is_active=True).first_or_404()
        return connection.to_dict()
    
    @staticmethod
    def create_connection(data):
        """创建数据库连接"""
        
        # 检查必填字段
        required_fields = ['name', 'host', 'port', 'database', 'username', 'password']
        if not all(field in data for field in required_fields):
            raise APIException('必填字段不能为空', 400)
        
        try:
            connection = DatabaseConnection(
                name=data['name'],
                host=data['host'],
                port=data['port'],
                database=data['database'],
                username=data['username'],
                password=data['password'],
                driver=data.get('driver', 'mysql'),
                charset=data.get('charset', 'utf8mb4'),
                description=data.get('description', '')
            )
            
            db.session.add(connection)
            db.session.commit()
            
            return connection.to_dict()
        
        except IntegrityError as e:
            db.session.rollback()
            raise APIException('数据库错误', 500, {'details': str(e.orig)})
        except Exception as e:
            db.session.rollback()
            raise APIException('创建数据库连接失败', 500, {'details': str(e)})
    
    @staticmethod
    def update_connection(connection_id, data):
        """更新数据库连接"""
        
        connection = DatabaseConnection.query.filter_by(id=connection_id, is_active=True).first_or_404()
        
        try:
            # 更新字段
            if 'name' in data:
                connection.name = data['name']
            if 'host' in data:
                connection.host = data['host']
            if 'port' in data:
                connection.port = data['port']
            if 'database' in data:
                connection.database = data['database']
            if 'username' in data:
                connection.username = data['username']
            if 'password' in data:
                connection.password = data['password']
            if 'driver' in data:
                connection.driver = data['driver']
            if 'charset' in data:
                connection.charset = data['charset']
            if 'description' in data:
                connection.description = data['description']
            
            db.session.commit()
            
            return connection.to_dict()
        
        except IntegrityError as e:
            db.session.rollback()
            raise APIException('数据库错误', 500, {'details': str(e.orig)})
        except Exception as e:
            db.session.rollback()
            raise APIException('更新数据库连接失败', 500, {'details': str(e)})
    
    @staticmethod
    def delete_connection(connection_id):
        """删除数据库连接（软删除）"""
        
        connection = DatabaseConnection.query.filter_by(id=connection_id, is_active=True).first_or_404()
        
        try:
            # 软删除
            connection.is_active = False
            
            db.session.commit()
            
            return {'message': '数据库连接删除成功'}
        
        except Exception as e:
            db.session.rollback()
            raise APIException('删除失败', 500, {'details': str(e)})
    
    @staticmethod
    def test_connection(connection_id):
        """测试数据库连接"""
        
        connection = DatabaseConnection.query.filter_by(id=connection_id, is_active=True).first_or_404()
        
        try:
            from sqlalchemy import create_engine
            engine = create_engine(connection.get_connection_string())
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return {
                'success': True,
                'message': '数据库连接测试成功',
                'connection': connection.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'数据库连接测试失败: {str(e)}',
                'connection': connection.to_dict()
            }
    
    @staticmethod
    def test_connection_params(data):
        """测试数据库连接参数（不保存）"""
        
        try:
            # 如提供了已有连接ID，则用库中已保存的字段补全（尤其是密码）
            existing = None
            connection_id = data.get('id') or data.get('connection_id')
            if connection_id:
                try:
                    existing = DatabaseConnection.query.filter_by(id=connection_id, is_active=True).first()
                except Exception:
                    existing = None

            # 处理密码：前端常用 ****** 掩码或空字符串，回退到已保存密码
            masked_values = {'******', '*****', '****', None, ''}
            if (not data.get('password') or data.get('password') in masked_values) and existing:
                data['password'] = existing.password

            # 其余字段如未提供则尽量回填，避免拼接出不完整连接串
            fallback_fields = ['host', 'port', 'database', 'username', 'driver', 'charset']
            if existing:
                for f in fallback_fields:
                    if data.get(f) in (None, ''):
                        data[f] = getattr(existing, f)

            # 最终校验必填字段
            required_fields = ['host', 'port', 'database', 'username', 'password']
            for f in required_fields:
                if not data.get(f) and data.get(f) != 0:
                    raise APIException(f'必填字段不能为空: {f}', 400)
            
            connection_string = DatabaseConnService._build_connection_string(data)
            from sqlalchemy import create_engine
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return {
                'success': True,
                'message': '数据库连接测试成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'数据库连接测试失败: {str(e)}'
            }

    @staticmethod
    def _build_connection_string(data):
        """
        构建数据库连接字符串

        Args:
            data (dict): 包含连接参数的字典

        Returns:
            str: 数据库连接字符串
        """
        driver = data.get('driver', 'mysql')
        username = data.get('username', '')
        password = data.get('password', '')
        host = data.get('host', '')
        port = data.get('port', 3306)
        database = data.get('database', '')
        charset = data.get('charset', 'utf8mb4')
        
        # 统一映射驱动，避免触发 MySQLdb 依赖
        d = (driver or 'mysql').lower()
        if d in ('mysql', 'pymysql'):
            dialect = 'mysql+pymysql'
        elif d in ('mysqlconnector', 'mysql+mysqlconnector'):
            dialect = 'mysql+mysqlconnector'
        elif d in ('postgresql', 'postgres'):
            dialect = 'postgresql'
        else:
            dialect = 'mysql+pymysql'

        return f"{dialect}://{username}:{password}@{host}:{port}/{database}?charset={charset}"
