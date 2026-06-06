#!/bin/bash
set -e

echo "⏳ 等待数据库就绪..."
python manage.py wait_for_db

echo "📦 执行数据库迁移..."
python manage.py migrate

echo "📥 导入初始数据..."
python manage.py import_data

echo "🚀 启动 Gunicorn 服务..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile -
