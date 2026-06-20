"""
data_loading/data_lake_pipeline.py — Local Data Lake ETL Engine
===============================================================
Orchestrates the movement of data from Raw (CSV) to Clean (Parquet)
and into the Curated Feature Store.
"""

import os
import time
import shutil
import logging
import pandas as pd
from pathlib import Path
from src.feature_engineering.feature_store import FeatureEngineeringEngine

logger = logging.getLogger("data_lake")
logging.basicConfig(level=logging.INFO)

# Define Data Lake Paths
LAKE_ROOT = Path("data_lake")
RAW_DIR = LAKE_ROOT / "raw"
CLEAN_DIR = LAKE_ROOT / "clean"
CURATED_DIR = LAKE_ROOT / "curated"

# Ensure directories exist
for d in [RAW_DIR, CLEAN_DIR, CURATED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

class DataLakePipeline:
    """ETL Pipeline that persists data to disk simulating a cloud data lake."""

    def __init__(self):
        self.feature_engine = FeatureEngineeringEngine()

    def ingest_to_raw(self, source_file: Path, original_filename: str) -> Path:
        """Saves an exact copy of the uploaded file to the Immutable Raw Layer."""
        timestamp = int(time.time())
        dest_filename = f"{timestamp}_{original_filename}"
        dest_path = RAW_DIR / dest_filename
        
        shutil.copy2(source_file, dest_path)
        logger.info(f"Ingested to Raw Layer: {dest_path}")
        return dest_path

    def process_to_clean(self, raw_path: Path) -> pd.DataFrame:
        """
        Simulates AWS Glue. Reads the raw file, standardizes it, 
        and saves as a highly-compressed Parquet file.
        """
        # Load Raw
        if raw_path.suffix.lower() == ".csv":
            df = pd.read_csv(raw_path, low_memory=False)
        else:
            df = pd.read_excel(raw_path)
            
        # Clean: Standardize column names (lowercase, no spaces)
        df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
        
        # Save to Clean Layer as Parquet
        clean_path = CLEAN_DIR / "standardized_dataset.parquet"
        df.to_parquet(clean_path, engine="pyarrow", index=False)
        logger.info(f"Processed to Clean Layer: {clean_path}")
        
        return df

    def engineer_to_curated(self, clean_df: pd.DataFrame) -> None:
        """
        Simulates AWS Athena/Feature Store. Generates analytical features 
        and joins them back or saves them as separate Curated tables.
        """
        # Engineer Customer Features (CLV, Churn)
        cust_features = self.feature_engine.engineer_customer_features(clean_df)
        if cust_features is not None:
            cust_path = CURATED_DIR / "feature_store_customers.parquet"
            cust_features.to_parquet(cust_path, engine="pyarrow", index=False)
            logger.info(f"Curated Customer Features saved to: {cust_path}")
            
        # Engineer Product Features
        prod_features = self.feature_engine.engineer_product_features(clean_df)
        if prod_features is not None:
            prod_path = CURATED_DIR / "feature_store_products.parquet"
            prod_features.to_parquet(prod_path, engine="pyarrow", index=False)
            logger.info(f"Curated Product Features saved to: {prod_path}")

    def run_pipeline(self, temp_uploaded_file: Path, original_filename: str) -> pd.DataFrame:
        """Executes the full pipeline and returns the clean DataFrame."""
        # 1. Raw
        raw_path = self.ingest_to_raw(temp_uploaded_file, original_filename)
        # 2. Clean
        clean_df = self.process_to_clean(raw_path)
        # 3. Curated
        self.engineer_to_curated(clean_df)
        
        return clean_df
