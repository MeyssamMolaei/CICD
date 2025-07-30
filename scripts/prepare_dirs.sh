#!/bin/bash

mkdir -p ./docker/postgres/data
mkdir -p ./docker/mssql/data
mkdir -p ./docker/airflow/dags
mkdir -p ./docker/airflow/data

touch ./docker/postgres/init.sql
touch ./docker/airflow/dags/transfer_dag.py

echo "Folders and placeholder files created."
