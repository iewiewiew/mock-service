#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:47
@description  路由包初始化文件
"""

import os

from flask import Flask
from flask_cors import CORS
from flask import redirect

from ..core.config import config
from ..core.database import db, migrate
from ..core.response_logger import ResponseLogger

from .example_routes import example_bp
from .mock import mock_bp
from .project import project_bp
from .api_docs import api_docs_bp
from .environment import environment_bp
from .mock_data import mock_data_bp
from .linux_info import linux_info_bp
from .sql_routes import sql_bp


# 导出所有蓝图，便于统一管理
__all__ = ['example_bp', 'api_docs_bp', 'mock_bp', 'mock_data_bp', 'project_bp', 'environment_bp', 'linux_info_bp', 'sql_bp']



def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    # 注册响应日志记录
    ResponseLogger.init_app(example_bp)
    ResponseLogger.init_app(mock_bp)
    ResponseLogger.init_app(project_bp)
    ResponseLogger.init_app(environment_bp)
    ResponseLogger.init_app(api_docs_bp)
    ResponseLogger.init_app(mock_data_bp)
    ResponseLogger.init_app(linux_info_bp)
    ResponseLogger.init_app(sql_bp)

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

    return app