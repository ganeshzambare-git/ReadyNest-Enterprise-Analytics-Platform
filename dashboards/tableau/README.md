# Tableau Integration for ReadyNest

This folder contains resources and documentation for connecting Tableau to the ReadyNest Insight Engine backend.

## Connection Instructions

1. Open Tableau Desktop.
2. Under **Connect** -> **To a Server**, select **PostgreSQL**.
3. Use the following connection details:
   - **Server:** `localhost`
   - **Port:** `5432`
   - **Database:** `readynest_db`
   - **Authentication:** Username and Password

## Best Practices
- Utilize the `.tds` (Tableau Data Source) templates provided in this folder to ensure consistent data typing and default aggregations across all organizational workbooks.
