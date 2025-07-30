Certainly! Here is a comprehensive `README.md` file in English that explains the **project purpose, architecture, all actions, and how everything works, including CI/CD, Docker setup, Airflow usage, volumes, and details about data migration**.

---

````markdown
# Postgres to MSSQL Data Migration with Docker, Airflow & GitHub Actions

## Project Purpose

This project demonstrates a complete CI/CD pipeline for migrating data from a **containerized PostgreSQL database** to a **containerized Microsoft SQL Server (MSSQL)** instance using **Apache Airflow** for orchestration. The entire stack runs on an Ubuntu 24.04 server with Docker, and all deployment steps are automated with GitHub Actions.

---

## Architecture Overview

- **Source Database:** PostgreSQL, containerized with Docker, preloaded with sample tables and data (via `init.sql`)
- **Target Database:** MSSQL Server, containerized with Docker, with persistent volumes for data durability
- **Orchestration:** Apache Airflow (containerized), running Python-based DAG to extract, transfer, and load data from Postgres to MSSQL
- **CI/CD:** GitHub Actions used to deploy, update, and orchestrate the Docker containers and project files on the Ubuntu server
- **Data Durability:** Docker volumes ensure database files persist across container restarts
- **Script Automation:** Bash scripts for initializing directory structures and placeholder files

---

## Directory Structure

```text
your-project/
│
├── .github/
│   └── workflows/
│       └── deploy.yml               # GitHub Actions workflow for CI/CD
│
├── docker/
│   ├── postgres/
│   │   ├── data/                    # Persistent data volume for Postgres
│   │   └── init.sql                 # Schema & test data for Postgres
│   ├── mssql/
│   │   └── data/                    # Persistent data volume for MSSQL
│   └── airflow/
│       ├── dags/
│       │   └── transfer_dag.py      # Airflow DAG for data migration
│       └── data/                    # (Optional) Extra data for DAGs
│
├── scripts/
│   └── prepare_dirs.sh              # Script for directory & file setup
│
├── docker-compose.yml               # Docker Compose setup for all services
└── README.md                        # This documentation
````

---

## Step-by-Step Workflow

### 1. Local Development & Commit

* **Code** (including SQL scripts, DAG, configs) is developed and pushed to your GitHub repository from your local machine (e.g., MacBook).

### 2. GitHub Actions CI/CD

* On each push to the `main` branch:

  * The workflow in `.github/workflows/deploy.yml` runs.
  * It uses SSH to securely copy all project files to the Ubuntu server (`81.231.74.206`).
  * The workflow then runs the setup script and brings up all Docker containers using `docker-compose`.

### 3. Docker Compose Setup

* The `docker-compose.yml` file defines three main services:

  * **Postgres:** Initializes with `init.sql` for tables and test data; data volume ensures persistence.
  * **MSSQL:** Sets up with a persistent data volume.
  * **Airflow:** Mounts DAGs as volumes and connects to both databases for migration tasks.

### 4. Persistent Data with Volumes

* Both databases map their internal data directories to host directories (`./docker/postgres/data`, `./docker/mssql/data`), guaranteeing that data remains intact even if containers restart or are rebuilt.

### 5. Directory Preparation Script

* `scripts/prepare_dirs.sh` creates all required directories and placeholder files, ensuring proper volume mount points exist before Docker Compose starts services.

### 6. Database Initialization

* On first launch, Postgres runs `init.sql`, creating tables and populating them with test data such as users, products, orders, and more.

### 7. Data Migration with Airflow

* The main migration logic is implemented in `docker/airflow/dags/transfer_dag.py`:

  * The DAG iterates through all tables (`users`, `products`, `orders`, etc.), copies their data from Postgres to MSSQL using Pandas and SQLAlchemy, and creates target tables in MSSQL if they do not exist.
  * Data types are mapped to be compatible between Postgres and MSSQL.
  * Dependencies (foreign keys) are handled by migrating tables in an appropriate order (or adjusting as needed).

### 8. Manual & Automated DAG Execution

* You can trigger the Airflow DAG either manually through the Airflow web UI (port 8080) or via Airflow CLI if you prefer automation.

---

## How to Use This Project

### Prerequisites

* **Ubuntu 24.04 server** with Docker & Docker Compose installed
* **GitHub account** with repository set up
* **SSH access** from GitHub Actions to your Ubuntu server (private key in repository secrets)

### One-Time Setup

1. **Clone the repository** to your server (if not automated yet):

   ```sh
   git clone https://github.com/yourusername/your-project.git
   cd your-project
   ```

2. **Run the preparation script** (locally or in your workflow):

   ```sh
   bash scripts/prepare_dirs.sh
   ```

3. **Start all services** (handled by GitHub Actions on push, or manually):

   ```sh
   docker compose up -d --build
   ```

4. **Access Airflow UI:**
   Open `http://your-server-ip:8080` in your browser to manage DAGs.

### Triggering the Migration

* **Manual:** In Airflow web UI, unpause and trigger the `pg_to_mssql_full_transfer` DAG.
* **Automated:** Extend the CI/CD pipeline or use Airflow's CLI/REST API to trigger runs as needed.

---

## Important Files Explained

### docker-compose.yml

Defines all services, their environment variables, ports, and volume mappings. Ensures containers restart automatically and data is never lost.

### docker/postgres/init.sql

Creates tables:

* `users`, `products`, `orders`, `order_items`, `categories`, `product_categories`, `reviews`, `carts`, `cart_items`, `addresses`, `payments`
* Populates them with realistic test data for migration and development.

### docker/airflow/dags/transfer\_dag.py

Python-based Airflow DAG:

* Uses `pandas`, `sqlalchemy`, `pyodbc`, `psycopg2`.
* Reads from Postgres, writes to MSSQL, auto-creates target tables if not exist.
* Each table transfer is a PythonOperator task for modularity.

### scripts/prepare\_dirs.sh

Ensures all required directories and placeholder files exist before Docker Compose runs, preventing issues with missing volumes or files.

### .github/workflows/deploy.yml

CI/CD automation:

* On push, copies the latest code to your server and (re)deploys the containers.
* Uses SSH keys for secure, passwordless deployment.

---

## Example: Airflow DAG Transfer Logic

```python
def transfer_table(table_name):
    # Connect to Postgres and MSSQL using SQLAlchemy
    # Create target table in MSSQL if it doesn't exist
    # Extract all data from Postgres
    # Insert data into MSSQL
    pass  # See transfer_dag.py for full implementation
```

---

## Customization & Extensibility

* Add more tables or change schema in `init.sql` and adjust `transfer_dag.py` as needed.
* Add more sophisticated DAGs (incremental sync, CDC, error handling, data validation).
* Use with other orchestrators or extend for production scenarios.

---

## Troubleshooting & Tips

* Ensure all required Python packages are installed in the Airflow container. You may need to build a custom image for extra requirements (`pandas`, `sqlalchemy`, `pyodbc`, etc).
* MSSQL driver setup in Airflow may need extra OS libraries. Check Airflow logs for missing dependencies.
* Always verify data types for compatibility between Postgres and MSSQL.
* Secure your database passwords and access keys with environment variables or secret managers.

---

## Credits

Project by \[Your Name].
Feel free to use, extend, and adapt for your own migrations!

---

```

---

**If you need a ready-to-use copy-paste version or want any part customized, just let me know!**
```
