"""
automation/sql_migration.py — Enterprise SQL Deployment Pipeline
================================================================
Automates the migration of Curated Parquet files from the Data Lake
into an Enterprise SQL Server (PostgreSQL/MySQL) for Power BI/Tableau
consumption.
"""

import os
import sys
import logging
from pathlib import Path
import pandas as pd

# Ensure we can import from the parent directory
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.database.connection import SQLConnector
from src.reporting.excel_generator import DataExporter
from dotenv import load_dotenv

logger = logging.getLogger("sql_migration")
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Define Paths
LAKE_ROOT = Path("data_lake")
CURATED_DIR = LAKE_ROOT / "curated"

def run_migration():
    """Reads curated Parquet files and pushes them to SQL."""
    
    # Load SQL Credentials from .env
    db_type = os.getenv("DB_TYPE", "postgresql")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", 5432))
    db_name = os.getenv("DB_NAME", "readynest_prod")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "")
    
    if not db_pass:
        logger.warning("DB_PASS environment variable is missing. The migration might fail if the database requires a password.")
        
    logger.info(f"Connecting to Enterprise Database: {db_type}://{db_host}:{db_port}/{db_name}")
    
    try:
        sql_conn = SQLConnector(
            db_type=db_type,
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_pass
        )
        
        # Test connection before migrating
        res = sql_conn.test_connection()
        if not res.success:
            logger.error(f"Failed to connect to Database: {res.summary}")
            return
        
        logger.info("Database Connection Successful. Locating Curated Parquet files...")
        
        if not CURATED_DIR.exists():
            logger.error(f"Curated directory not found: {CURATED_DIR}")
            return
            
        parquet_files = list(CURATED_DIR.glob("*.parquet"))
        
        if not parquet_files:
            logger.warning("No Curated Parquet files found. Have you uploaded data via the Data Loader UI yet?")
            return
            
        exporter = DataExporter()
        
        for file in parquet_files:
            table_name = file.stem # e.g., 'feature_store_customers'
            logger.info(f"Loading {file.name}...")
            
            # Read Parquet
            df = pd.read_parquet(file, engine="pyarrow")
            
            # Export to SQL
            logger.info(f"Writing {len(df)} rows to SQL Table '{table_name}'...")
            exporter.to_sql(df, sql_conn, table_name=table_name, if_exists="replace")
            logger.info(f"Successfully deployed {file.name} to SQL!")
            
        sql_conn.close()
        logger.info("All Curated tables successfully deployed to the Enterprise SQL Server!")
        logger.info("Power BI and Tableau can now connect directly to this database.")

    except Exception as e:
        logger.error(f"Migration Failed: {e}")

if __name__ == "__main__":
    run_migration()
