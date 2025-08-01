# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/10/19 17:10
@description
"""

from io import StringIO

import paramiko

from ..core.database import db
from ..models.linux_info_model import LinuxInfo


class LinuxInfoService:

    @staticmethod
    def get_all_servers():
        """获取所有服务器信息"""

        return LinuxInfo.query.all()

    @staticmethod
    def get_server_by_id(server_id):
        return LinuxInfo.query.get(server_id)

    @staticmethod
    def create_server(data):
        if LinuxInfo.query.filter_by(host=data['host']).first():
            raise ValueError('Host already exists')

        server = LinuxInfo(server_name=data['server_name'], host=data['host'], port=data.get('port', 22),
            username=data['username'], password=data.get('password'), private_key=data.get('private_key'),
            description=data.get('description'))
        db.session.add(server)
        db.session.commit()
        return server

    @staticmethod
    def update_server(server_id, data):
        server = LinuxInfo.query.get(server_id)
        if not server:
            return None

        for key, value in data.items():
            if hasattr(server, key):
                setattr(server, key, value)

        db.session.commit()
        return server

    @staticmethod
    def delete_server(server_id):
        server = LinuxInfo.query.get(server_id)
        if server:
            db.session.delete(server)
            db.session.commit()
            return True
        return False

    @staticmethod
    def execute_command(server_id, command):
        server = LinuxInfo.query.get(server_id)
        if not server:
            return {'success': False, 'error': 'Server not found'}

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接参数
            connect_params = {'hostname': server.host, 'port': server.port, 'username': server.username, 'timeout': 30}

            if server.private_key:
                # 使用私钥认证
                private_key = paramiko.RSAKey.from_private_key(StringIO(server.private_key))
                connect_params['pkey'] = private_key
            else:
                # 使用密码认证
                connect_params['password'] = server.password

            ssh.connect(**connect_params)

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()

            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            ssh.close()

            return {'success': True, 'output': output, 'error': error, 'exit_status': exit_status}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_server_info(server_id):
        """获取服务器基本信息"""
        commands = {'hostname': 'hostname', 'os_info': 'cat /etc/os-release', 'kernel': 'uname -r', 'uptime': 'uptime',
            'memory': 'free -h', 'disk': 'df -h', 'cpu_info': 'lscpu'}

        results = {}
        for key, command in commands.items():
            result = LinuxInfoService.execute_command(server_id, command)
            if result['success']:
                results[key] = result['output']
            else:
                results[key] = f"Error: {result['error']}"

        return results
