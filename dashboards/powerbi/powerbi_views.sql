-- Optimized views for Power BI ingestion
-- These views pre-join dimensions and facts to simplify the PBIX data model.

CREATE OR REPLACE VIEW pbi_sales_overview AS
SELECT 
    s.sale_id,
    s.sale_date,
    s.amount,
    p.product_name,
    p.category,
    c.customer_segment,
    r.region_name
FROM 
    fact_sales s
JOIN 
    dim_product p ON s.product_id = p.product_id
JOIN 
    dim_customer c ON s.customer_id = c.customer_id
JOIN 
    dim_region r ON s.region_id = r.region_id;

CREATE OR REPLACE VIEW pbi_customer_churn AS
SELECT
    c.customer_id,
    c.acquisition_date,
    c.lifetime_value,
    c.churn_probability,
    CASE 
        WHEN c.churn_probability > 0.7 THEN 'High Risk'
        WHEN c.churn_probability > 0.4 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as churn_risk_category
FROM 
    dim_customer c;
