# Power BI Integration for ReadyNest

This folder contains resources and documentation for connecting Microsoft Power BI to the ReadyNest Insight Engine backend.

## Connection Instructions

1. Open Power BI Desktop.
2. Click **Get Data** -> **PostgreSQL database**.
3. Use the following parameters (adjust based on your environment):
   - **Server:** `localhost:5432` (or your cloud RDS endpoint)
   - **Database:** `readynest_db`
   - **Data Connectivity mode:** DirectQuery (recommended for real-time analytics) or Import (for better performance on static data).

## Included Resources

- `powerbi_views.sql`: Execute this script in your database to create denormalized views that are optimized for Power BI ingestion.
