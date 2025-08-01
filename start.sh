#!/bin/bash

# 删除空镜像资源 需优化
docker system prune -f

# 停止并删除由 docker-compose up 启动的所有容器、网络、数据卷
# docker-compose down -v

# 删除 MySQL 服务
# docker-compos stop mock_db
# docker-compos rm -f mock_db
# docker volume rm mock-service_mysql_data

# 删除容器 可注释
# lsof -i:5001 | awk 'NR!=1 {print $2}' | xargs kill -9

# 删除容器
docker-compose stop mock_backend mock_frontend
docker-compose rm -f mock_backend mock_frontend

# 启动服务
docker-compose up --build -d backend frontend
