#!/bin/bash

mkdir -p ./docker/postgres/data
mkdir -p ./docker/mssql/data
mkdir -p ./docker/airflow/dags
mkdir -p ./docker/airflow/data

sudo chown -R 10001:0 ./docker/mssql/data
sudo chown -R 10001:0 ./docker/postgres/data
sudo chown -R 10001:0 ./docker/airflow/dags
sudo chown -R 10001:0 ./docker/airflow/data


touch ./docker/postgres/init.sql
touch ./docker/airflow/dags/transfer_dag.py
docker rm -f $(docker ps -a) -q || true
echo "Folders and placeholder files created."
