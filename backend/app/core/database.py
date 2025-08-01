# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author       weimenghua
@time         2025/7/30 17:46
@description  数据库模块
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

tz_beijing = timezone(timedelta(hours=8))

db = SQLAlchemy()
migrate = Migrate()
