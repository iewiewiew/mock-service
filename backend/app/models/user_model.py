#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/27 15:15
@description
"""

import binascii
import hashlib
import json
import os
from ..core.database import db, datetime, tz_beijing

# 密码工具函数
def safe_generate_password_hash(password):
    """
    安全的密码哈希生成，使用 pbkdf2_sha256 避免 scrypt 问题
    """
    # 使用手动实现的 pbkdf2_sha256
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def safe_check_password_hash(hashed_password, password):
    """
    安全的密码验证
    """
    try:
        # 提取盐值和存储的哈希
        salt = hashed_password[:64]
        stored_password = hashed_password[64:]

        # 使用相同的盐值和参数计算密码哈希
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    except Exception:
        return False


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    username = db.Column(db.String(80), unique=True, nullable=False, index=True, comment='用户名')
    email = db.Column(db.String(120), unique=True, nullable=False, index=True, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    full_name = db.Column(db.String(100), nullable=False, comment='全名')
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否激活')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing),
                           onupdate=lambda: datetime.now(tz_beijing), nullable=False, comment='更新时间')

    # 关联角色
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), comment='角色ID')
    role = db.relationship('Role', back_populates='users')

    def set_password(self, password):
        """
        设置密码（自动加密）
        """
        self.password_hash = safe_generate_password_hash(password)

    def check_password(self, password):
        """
        验证密码
        """
        return safe_check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        转换为字典格式，用于JSON序列化
        """
        return {'id': self.id, 'username': self.username, 'email': self.email, 'full_name': self.full_name,
            'is_active': self.is_active, 'role_id': self.role_id, 'role_name': self.role.name if self.role else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}

    def to_simple_dict(self):
        """
        简化的字典格式，不包含敏感信息
        """
        return {'id': self.id, 'username': self.username, 'email': self.email, 'full_name': self.full_name,
            'is_active': self.is_active, 'role_name': self.role.name if self.role else None}

    def has_permission(self, permission):
        """
        检查用户是否拥有指定权限
        """
        if not self.role or not self.role.permissions:
            return False

        try:
            permissions = self.role.get_permissions_list()
            return permission in permissions
        except:
            return False

    def is_admin(self):
        """
        检查用户是否是管理员
        """
        return self.role and self.role.name == 'admin'

    def activate(self):
        """激活用户"""
        self.is_active = True
        self.updated_at = datetime.now(tz_beijing)

    def deactivate(self):
        """禁用用户"""
        self.is_active = False
        self.updated_at = datetime.now(tz_beijing)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_permissions(self):
        """
        获取用户权限列表
        """
        if not self.role:
            return []
        return self.role.get_permissions_list()

    def to_dict_with_permissions(self):
        """
        包含权限信息的字典格式
        """
        data = self.to_dict()
        data['permissions'] = self.get_permissions()
        return data

    def to_full_dict(self):
        """
        完整的用户信息，包含角色详情和权限
        """
        role_data = None
        if self.role:
            role_data = {'role_id': self.role.id, 'role_name': self.role.name,
                'role_description': self.role.description, 'permissions': self.get_permissions()}

        return {'id': self.id, 'username': self.username, 'email': self.email, 'full_name': self.full_name,
            'is_active': self.is_active, 'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None, 'role': role_data}


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='角色名称')
    description = db.Column(db.String(200), comment='角色描述')
    permissions = db.Column(db.Text, default='[]', comment='权限列表（JSON字符串）')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz_beijing), nullable=False, comment='创建时间')
    is_system = db.Column(db.Boolean, default=False, nullable=False, comment='是否为系统角色')

    users = db.relationship('User', back_populates='role')

    def get_permissions_list(self):
        """
        获取权限列表 - 修复后的统一版本
        """
        if not self.permissions:
            return []

        try:
            # 先尝试 JSON 解析
            permissions = json.loads(self.permissions)
            if isinstance(permissions, list):
                return permissions
        except (json.JSONDecodeError, TypeError):
            pass

        # 如果是字符串格式的列表，尝试安全转换
        try:
            import ast
            if isinstance(self.permissions, str):
                permissions = ast.literal_eval(self.permissions)
                if isinstance(permissions, list):
                    return permissions
        except (ValueError, SyntaxError):
            pass

        # 最后尝试字符串分割
        if isinstance(self.permissions, str):
            # 清理字符串：移除方括号和引号，然后分割
            cleaned = self.permissions.strip('[]').replace("'", "").replace('"', '')
            return [p.strip() for p in cleaned.split(',') if p.strip()]

        return []

    def set_permissions(self, permissions_list):
        """
        设置权限列表
        """
        if not isinstance(permissions_list, list):
            permissions_list = []
        self.permissions = json.dumps(permissions_list, ensure_ascii=False)

    def has_permission(self, permission):
        """
        检查角色是否拥有指定权限
        """
        return permission in self.get_permissions_list()

    def add_permission(self, permission):
        """
        添加权限
        """
        permissions = self.get_permissions_list()
        if permission not in permissions:
            permissions.append(permission)
            self.set_permissions(permissions)

    def remove_permission(self, permission):
        """
        移除权限
        """
        permissions = self.get_permissions_list()
        if permission in permissions:
            permissions.remove(permission)
            self.set_permissions(permissions)

    def to_dict(self):
        """
        转换为字典格式
        """
        return {'id': self.id, 'name': self.name, 'description': self.description,
            'permissions': self.get_permissions_list(), 'permissions_raw': self.permissions,
            'created_at': self.created_at.isoformat() if self.created_at else None, 'is_system': self.is_system,
            'user_count': len(self.users)}

    def to_simple_dict(self):
        """
        简化的字典格式
        """
        return {'id': self.id, 'name': self.name, 'description': self.description, 'user_count': len(self.users)}

    def __repr__(self):
        return f'<Role {self.name}>'


class Permission:
    """
    权限常量定义
    """
    # 用户管理权限
    USER_READ = 'user:read'
    USER_WRITE = 'user:write'
    USER_DELETE = 'user:delete'

    # 角色管理权限
    ROLE_READ = 'role:read'
    ROLE_WRITE = 'role:write'

    @classmethod
    def all_permissions(cls):
        """
        获取所有权限列表
        """
        return [cls.USER_READ, cls.USER_WRITE, cls.USER_DELETE, cls.ROLE_READ, cls.ROLE_WRITE]

    @classmethod
    def get_permission_label(cls, permission):
        """
        获取权限的显示标签
        """
        labels = {cls.USER_READ: '查看用户', cls.USER_WRITE: '管理用户', cls.USER_DELETE: '删除用户',
            cls.ROLE_READ: '查看角色', cls.ROLE_WRITE: '管理角色'}
        return labels.get(permission, permission)

    @classmethod
    def get_permission_group(cls, permission):
        """
        获取权限所属的分组
        """
        groups = {cls.USER_READ: '用户管理', cls.USER_WRITE: '用户管理', cls.USER_DELETE: '用户管理',
            cls.ROLE_READ: '角色管理', cls.ROLE_WRITE: '角色管理'}
        return groups.get(permission, '其他')

    @classmethod
    def get_permissions_by_group(cls):
        """
        按分组获取权限
        """
        groups = {}
        for permission in cls.all_permissions():
            group = cls.get_permission_group(permission)
            if group not in groups:
                groups[group] = []
            groups[group].append({'value': permission, 'label': cls.get_permission_label(permission)})
        return groups


# 辅助函数
def init_default_roles():
    """
    初始化默认角色
    """
    try:
        # 管理员角色 - 拥有所有权限
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='系统超级管理员', is_system=True)
            admin_role.set_permissions(Permission.all_permissions())
            db.session.add(admin_role)
            print("✓ 创建管理员角色成功")

        # 普通用户角色 - 只有查看权限
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='普通用户', is_system=True)
            user_role.set_permissions([Permission.USER_READ])
            db.session.add(user_role)
            print("✓ 创建普通用户角色成功")

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"✗ 初始化默认角色失败: {str(e)}")
        return False


def init_default_admin():
    """
    初始化默认管理员账号
    """
    try:
        # 查找管理员角色
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("✗ 管理员角色不存在，请先初始化角色")
            return False

        # 检查管理员账号是否已存在
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', email='admin@example.com', full_name='系统管理员',
                role_id=admin_role.id, is_active=True)
            admin_user.set_password('123456')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ 创建超管管理员账号成功: admin/123456")
            return True
        else:
            print("✓ 超管管理员账号已存在")
            return True

    except Exception as e:
        db.session.rollback()
        print(f"✗ 初始化默认管理员失败: {str(e)}")
        return False


def init_default_test_user():
    """
    初始化默认普通用户: 账号 test / 密码 123456
    """
    try:
        # 确保普通用户角色存在
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='普通用户', is_system=True)
            user_role.set_permissions([Permission.USER_READ])
            db.session.add(user_role)
            db.session.flush()  # 确保 role.id 可用

        # 检查 test 账号是否已存在
        test_user = User.query.filter_by(username='test').first()
        if not test_user:
            test_user = User(username='test', email='test@example.com', full_name='测试用户', role_id=user_role.id,
                is_active=True)
            test_user.set_password('123456')
            db.session.add(test_user)
            db.session.commit()
            print("✓ 创建默认普通用户成功: test/123456")
            return True
        else:
            print("✓ 默认普通用户已存在: test")
            return True

    except Exception as e:
        db.session.rollback()
        print(f"✗ 初始化默认普通用户失败: {str(e)}")
        return False
