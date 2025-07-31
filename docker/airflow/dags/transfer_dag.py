from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import sqlalchemy

PG_CONN_STR = "postgresql+psycopg2://pguser:pgpassword@postgres:5432/pgdb"
MSSQL_CONN_STR = "mssql+pyodbc://sa:P%40ssw0rd2024@mssql:1433/tempdb?driver=ODBC+Driver+17+for+SQL+Server"

TABLES = [
    "users",
    "products",
    "orders",
    "order_items",
    "categories",
    "product_categories",
    "reviews",
    "carts",
    "cart_items",
    "addresses",
    "payments",
]

CREATE_TABLE_QUERIES = {
    "users": """
        IF OBJECT_ID('users', 'U') IS NULL
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name NVARCHAR(50),
            email NVARCHAR(50)
        );
    """,
    "products": """
        IF OBJECT_ID('products', 'U') IS NULL
        CREATE TABLE products (
            id INT PRIMARY KEY,
            name NVARCHAR(100),
            price DECIMAL(10,2)
        );
    """,
    "orders": """
        IF OBJECT_ID('orders', 'U') IS NULL
        CREATE TABLE orders (
            id INT PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT,
            order_date DATETIME
        );
    """,
    "order_items": """
        IF OBJECT_ID('order_items', 'U') IS NULL
        CREATE TABLE order_items (
            id INT PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT
        );
    """,
    "categories": """
        IF OBJECT_ID('categories', 'U') IS NULL
        CREATE TABLE categories (
            id INT PRIMARY KEY,
            name NVARCHAR(50)
        );
    """,
    "product_categories": """
        IF OBJECT_ID('product_categories', 'U') IS NULL
        CREATE TABLE product_categories (
            product_id INT,
            category_id INT,
            PRIMARY KEY (product_id, category_id)
        );
    """,
    "reviews": """
        IF OBJECT_ID('reviews', 'U') IS NULL
        CREATE TABLE reviews (
            id INT PRIMARY KEY,
            product_id INT,
            user_id INT,
            rating INT,
            comment NVARCHAR(MAX),
            created_at DATETIME
        );
    """,
    "carts": """
        IF OBJECT_ID('carts', 'U') IS NULL
        CREATE TABLE carts (
            id INT PRIMARY KEY,
            user_id INT,
            created_at DATETIME
        );
    """,
    "cart_items": """
        IF OBJECT_ID('cart_items', 'U') IS NULL
        CREATE TABLE cart_items (
            id INT PRIMARY KEY,
            cart_id INT,
            product_id INT,
            quantity INT,
            added_at DATETIME
        );
    """,
    "addresses": """
        IF OBJECT_ID('addresses', 'U') IS NULL
        CREATE TABLE addresses (
            id INT PRIMARY KEY,
            user_id INT,
            street NVARCHAR(100),
            city NVARCHAR(50),
            state NVARCHAR(50),
            zip NVARCHAR(20),
            country NVARCHAR(50)
        );
    """,
    "payments": """
        IF OBJECT_ID('payments', 'U') IS NULL
        CREATE TABLE payments (
            id INT PRIMARY KEY,
            order_id INT,
            amount DECIMAL(10,2),
            payment_date DATETIME,
            payment_method NVARCHAR(50)
        );
    """,
}


def transfer_table(table_name):
    # اتصال به دیتابیس‌ها
    pg_engine = sqlalchemy.create_engine(PG_CONN_STR)
    mssql_engine = sqlalchemy.create_engine(MSSQL_CONN_STR)

    # ساخت جدول اگر وجود ندارد
    with mssql_engine.connect() as conn:
        conn.execute(sqlalchemy.text(CREATE_TABLE_QUERIES[table_name]))

    # خواندن داده از PostgreSQL
    df = pd.read_sql(f"SELECT * FROM {table_name}", pg_engine)

    # درج داده در MSSQL (replace if already exists)
    df.to_sql(table_name, mssql_engine, if_exists="append", index=False, method="multi")


default_args = {
    "start_date": datetime(2024, 1, 1),
    "catchup": False,
}

with DAG(
    dag_id="pg_to_mssql_full_transfer",
    schedule=None,
    default_args=default_args,
    description="Transfer all tables from Postgres to MSSQL",
) as dag:

    for tbl in TABLES:
        PythonOperator(
            task_id=f"transfer_{tbl}",
            python_callable=transfer_table,
            op_kwargs={"table_name": tbl},
        )
