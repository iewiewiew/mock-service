#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  路由包初始化文件
"""

import os

from flask import Flask
from flask import redirect
from flask_cors import CORS

from .api_docs_routes import api_docs_bp
from .auth_routes import auth_bp
from .database_conn_routes import database_conn_bp
from .database_info_routes import database_info_bp
from .environment_routes import environment_bp
from .example_routes import example_bp
from .linux_info_routes import linux_info_bp
from .mock_data_routes import mock_data_bp
from .mock_routes import mock_bp
from .project_routes import project_bp
from .role_routes import role_bp
from .script_management_routes import script_management_bp
from .sql_routes import sql_bp
from .user_routes import user_bp
from ..core.config import config
from ..core.database import db, migrate
from ..core.response_logger import ResponseLogger
from ..services.init_service import InitService
from ..services.script_management_service import script_management_service

# 导出所有蓝图，便于统一管理
__all__ = ['example_bp', 'api_docs_bp', 'mock_bp', 'mock_data_bp', 'project_bp', 'environment_bp', 'linux_info_bp',
    'sql_bp', 'role_bp', 'auth_bp', 'user_bp', 'database_conn_bp', 'database_info_bp', 'script_management_bp']


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # 初始化默认数据
        if InitService.init_default_data():
            print("系统初始化完成")
        else:
            print("系统初始化失败")
        
        # 设置Flask应用实例到脚本管理服务（用于定时任务执行时创建应用上下文）
        script_management_service.set_app(app)
        
        # 加载已存在的定时任务
        try:
            script_management_service.load_existing_scheduled_tasks()
        except Exception as e:
            print(f"加载定时任务失败: {str(e)}")
            import traceback
            traceback.print_exc()

    # 注册响应日志记录
    ResponseLogger.init_app(example_bp)
    ResponseLogger.init_app(mock_bp)
    ResponseLogger.init_app(project_bp)
    ResponseLogger.init_app(environment_bp)
    ResponseLogger.init_app(api_docs_bp)
    ResponseLogger.init_app(mock_data_bp)
    ResponseLogger.init_app(linux_info_bp)
    ResponseLogger.init_app(sql_bp)
    ResponseLogger.init_app(auth_bp)
    ResponseLogger.init_app(role_bp)
    ResponseLogger.init_app(user_bp)
    ResponseLogger.init_app(database_conn_bp)
    ResponseLogger.init_app(database_info_bp)
    ResponseLogger.init_app(script_management_bp)

    @app.route('/')
    def root_redirect():
        """根路径重定向到 /api/mock"""
        return redirect('/api/mock')

    if os.environ.get('FLASK_APP') is None:
        os.environ['FLASK_APP'] = 'app.routes:create_app'

    app.register_blueprint(example_bp, url_prefix='/api')
    app.register_blueprint(mock_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(environment_bp, url_prefix='/api')
    app.register_blueprint(mock_data_bp, url_prefix='/api')
    app.register_blueprint(api_docs_bp, url_prefix='/api')
    app.register_blueprint(linux_info_bp, url_prefix='/api')
    app.register_blueprint(sql_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(role_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(database_conn_bp, url_prefix='/api')
    app.register_blueprint(database_info_bp, url_prefix='/api')
    app.register_blueprint(script_management_bp, url_prefix='/api')

    return app
