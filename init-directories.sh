#!/bin/bash

BASE_DIR="/Users/meyssam/Downloads/CICD"

mkdir -p $BASE_DIR/docker/postgres/data
mkdir -p $BASE_DIR/docker/mssql/data
mkdir -p $BASE_DIR/docker/migrate
mkdir -p $BASE_DIR/.github/workflows

# ایجاد فایل‌ها
touch $BASE_DIR/docker/postgres/Dockerfile
touch $BASE_DIR/docker/postgres/init.sql

touch $BASE_DIR/docker/mssql/Dockerfile

touch $BASE_DIR/docker/migrate/migrate.sh

touch $BASE_DIR/.github/workflows/deploy.yml

touch $BASE_DIR/README.md
touch $BASE_DIR/docker-compose.yml

echo "ساختار پروژه با موفقیت ساخته شد."
