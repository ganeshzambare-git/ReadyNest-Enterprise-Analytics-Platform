"""
data_loading/connectors.py — SQL Connectivity
=============================================
SQLConnector provides a unified interface for PostgreSQL and MySQL
databases via SQLAlchemy, with connection testing, query execution,
and table introspection.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator, Optional

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.pool import QueuePool

from src.core.logging_manager import get_logger

logger = get_logger("src.database.connection")

# ── Dialect map ───────────────────────────────────────────────────────────────
DIALECT_MAP = {
    "postgresql": "postgresql+psycopg2",
    "mysql":      "mysql+pymysql",
}


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class ConnectionResult:
    """Outcome of a connection test."""
    success: bool
    db_type: str
    host: str
    database: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None

    @property
    def summary(self) -> str:
        if self.success:
            return (
                f"✅ Connected to {self.db_type.upper()} | "
                f"{self.host}/{self.database} | "
                f"Latency: {self.latency_ms:.1f} ms"
            )
        return f"❌ Connection failed: {self.error}"


# ── Connector class ───────────────────────────────────────────────────────────

class SQLConnector:
    """
    Unified SQL connector for PostgreSQL and MySQL.

    Wraps SQLAlchemy to provide:
    - Connection testing with latency measurement
    - Query execution returning DataFrames
    - Table listing and schema inspection
    - Context-manager support for safe resource cleanup

    Example::

        connector = SQLConnector(
            db_type="postgresql",
            host="localhost", port=5432,
            database="readynest_db",
            user="postgres", password="secret"
        )
        result = connector.test_connection()
        df = connector.execute_query("SELECT * FROM sales LIMIT 100")
        connector.close()
    """

    def __init__(
        self,
        db_type: str,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        connect_timeout: int = 10,
    ) -> None:
        """
        Args:
            db_type:         ``'postgresql'`` or ``'mysql'``.
            host:            Database server hostname / IP.
            port:            Server port.
            database:        Target database name.
            user:            Login username.
            password:        Login password.
            pool_size:       SQLAlchemy connection pool size.
            max_overflow:    Max connections above pool_size.
            connect_timeout: Seconds before a connection attempt times out.
        """
        if db_type not in DIALECT_MAP:
            raise ValueError(
                f"Unsupported db_type '{db_type}'. "
                f"Choose from: {list(DIALECT_MAP)}"
            )

        self.db_type = db_type.lower()
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self._password = password
        self._engine: Optional[Engine] = None

        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._connect_timeout = connect_timeout

        logger.info(
            f"SQLConnector initialised: {self.db_type} @ {self.host}:{self.port}/{self.database}"
        )

    # ── Connection URL ────────────────────────────────────────────────────────

    @property
    def connection_url(self) -> str:
        dialect = DIALECT_MAP[self.db_type]
        return (
            f"{dialect}://{self.user}:{self._password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    # ── Engine lifecycle ──────────────────────────────────────────────────────

    def _get_engine(self) -> Engine:
        """Create or return the cached SQLAlchemy engine."""
        if self._engine is None:
            connect_args = {"connect_timeout": self._connect_timeout}
            self._engine = create_engine(
                self.connection_url,
                poolclass=QueuePool,
                pool_size=self._pool_size,
                max_overflow=self._max_overflow,
                connect_args=connect_args,
                echo=False,
            )
            logger.debug("SQLAlchemy engine created.")
        return self._engine

    def close(self) -> None:
        """Dispose of the connection pool and release all resources."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            logger.info("SQLAlchemy engine disposed.")

    @contextmanager
    def _connection(self) -> Generator:
        """Context manager yielding a raw DBAPI connection."""
        engine = self._get_engine()
        conn = engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    # ── Public API ────────────────────────────────────────────────────────────

    def test_connection(self) -> ConnectionResult:
        """
        Verify that the database is reachable and return latency.

        Returns:
            :class:`ConnectionResult` with success flag and latency.
        """
        logger.info(f"Testing connection: {self.db_type} @ {self.host}:{self.port}")
        start = time.perf_counter()
        try:
            with self._connection() as conn:
                conn.execute(text("SELECT 1"))
            latency_ms = (time.perf_counter() - start) * 1000
            result = ConnectionResult(
                success=True,
                db_type=self.db_type,
                host=self.host,
                database=self.database,
                latency_ms=round(latency_ms, 2),
            )
            logger.info(result.summary)
            return result

        except OperationalError as exc:
            err = f"OperationalError: {exc.orig}"
            logger.error(f"Connection test failed: {err}")
            return ConnectionResult(
                success=False,
                db_type=self.db_type,
                host=self.host,
                database=self.database,
                error=err,
            )
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            logger.error(f"Unexpected connection error: {err}")
            return ConnectionResult(
                success=False,
                db_type=self.db_type,
                host=self.host,
                database=self.database,
                error=err,
            )

    def execute_query(self, sql: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a DataFrame.

        Args:
            sql:    Raw SQL string (SELECT statements recommended).
            params: Optional dict of bind parameters.

        Returns:
            ``pd.DataFrame`` with query results.

        Raises:
            SQLAlchemyError: On query execution failure.
            ValueError:      If *sql* is empty.
        """
        if not sql or not sql.strip():
            raise ValueError("SQL query cannot be empty.")

        logger.info(f"Executing query: {sql[:120]}...")
        try:
            with self._connection() as conn:
                df = pd.read_sql(text(sql), conn, params=params)
            logger.info(f"Query returned {len(df):,} rows × {len(df.columns)} cols.")
            return df

        except SQLAlchemyError as exc:
            logger.error(f"Query execution failed: {exc}")
            raise

    def list_tables(self) -> list[str]:
        """
        Return all table names in the connected database.

        Returns:
            Sorted list of table name strings.
        """
        try:
            inspector = inspect(self._get_engine())
            tables = sorted(inspector.get_table_names())
            logger.info(f"Found {len(tables)} tables in '{self.database}'.")
            return tables
        except SQLAlchemyError as exc:
            logger.error(f"Failed to list tables: {exc}")
            raise

    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """
        Return column names and types for *table_name*.

        Args:
            table_name: Target table.

        Returns:
            DataFrame with columns ``['column', 'type', 'nullable']``.
        """
        try:
            inspector = inspect(self._get_engine())
            cols = inspector.get_columns(table_name)
            return pd.DataFrame(
                [
                    {
                        "column":   c["name"],
                        "type":     str(c["type"]),
                        "nullable": c.get("nullable", True),
                    }
                    for c in cols
                ]
            )
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get schema for '{table_name}': {exc}")
            raise

    def write_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace",
        index: bool = False,
        chunksize: int = 1000,
    ) -> None:
        """
        Write a DataFrame to a SQL table.

        Args:
            df:         DataFrame to write.
            table_name: Destination table name.
            if_exists:  ``'replace'``, ``'append'``, or ``'fail'``.
            index:      Whether to write the DataFrame index as a column.
            chunksize:  Rows per batch insert.
        """
        if df is None or df.empty:
            raise ValueError("Cannot write an empty DataFrame to SQL.")

        logger.info(
            f"Writing {len(df):,} rows → '{table_name}' "
            f"(if_exists='{if_exists}', chunksize={chunksize})"
        )
        try:
            df.to_sql(
                table_name,
                con=self._get_engine(),
                if_exists=if_exists,
                index=index,
                chunksize=chunksize,
                method="multi",
            )
            logger.info(f"Successfully wrote {len(df):,} rows to '{table_name}'.")
        except SQLAlchemyError as exc:
            logger.error(f"Failed to write DataFrame to '{table_name}': {exc}")
            raise

    # ── Dunder helpers ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"SQLConnector(db_type={self.db_type!r}, "
            f"host={self.host!r}, "
            f"port={self.port}, "
            f"database={self.database!r})"
        )

    def __enter__(self) -> "SQLConnector":
        return self

    def __exit__(self, *_) -> None:
        self.close()
