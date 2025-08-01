# 基础镜像 https://docker.aityp.com/s/docker.io
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.9

WORKDIR /app

# 安装系统依赖（MySQL客户端等）
RUN rm -f /etc/apt/sources.list /etc/apt/sources.list.d/* && \
    echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get update -o Acquire::Check-Valid-Until=false -o Acquire::AllowInsecureRepositories=true && \
    apt-get install -y build-essential python3-dev libffi-dev default-libmysqlclient-dev default-mysql-client && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 数据库初始化脚本
COPY ./docker/db-init/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# 暴露端口
EXPOSE 5001

# 启动命令（等待数据库就绪后启动）
CMD ["/bin/bash", "-c", "/wait-for-it.sh db:3306 flask run --host=0.0.0.0 --port=5001"]