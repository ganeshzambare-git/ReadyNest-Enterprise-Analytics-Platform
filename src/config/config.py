"""
config.py — ReadyNest Dashboard Configuration
=============================================
Centralised settings loaded from environment variables (.env file).
All secrets must be stored in .env — never hardcoded here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Project root & .env loading ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "data_loading.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB per file
LOG_BACKUP_COUNT = 3

# ── Data & Export paths ───────────────────────────────────────────────────────
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
EXPORT_DIR = BASE_DIR / os.getenv("EXPORT_DIR", "exports")
EXPORT_DIR.mkdir(exist_ok=True)

# ── Supported file extensions ─────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

# ── UI Settings ───────────────────────────────────────────────────────────────
MAX_PREVIEW_ROWS = int(os.getenv("MAX_PREVIEW_ROWS", "10"))
APP_TITLE = "ReadyNest — Data Loading Module"
APP_ICON = "📦"

# ── PostgreSQL configuration ──────────────────────────────────────────────────
POSTGRES_CONFIG = {
    "host":     os.getenv("PG_HOST", "localhost"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "database": os.getenv("PG_DATABASE", "readynest_db"),
    "user":     os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", ""),
}

# ── MySQL configuration ───────────────────────────────────────────────────────
MYSQL_CONFIG = {
    "host":     os.getenv("MYSQL_HOST", "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "readynest_db"),
    "user":     os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}

# ── SQLAlchemy dialect prefixes ───────────────────────────────────────────────
DB_DIALECT = {
    "postgresql": "postgresql+psycopg2",
    "mysql":      "mysql+pymysql",
}

# ── Data quality thresholds ───────────────────────────────────────────────────
QUALITY_THRESHOLDS = {
    "null_ratio_warn":  0.10,   # Warn if > 10 % nulls in a column
    "null_ratio_error": 0.50,   # Error if > 50 % nulls
    "dup_ratio_warn":   0.05,   # Warn if > 5 % duplicate rows
}
